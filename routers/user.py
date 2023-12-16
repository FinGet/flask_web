from datetime import datetime
import traceback
from typing import Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Header, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from core.init_db import get_db
from models.crud import db_create_user, get_role_name, get_user_by_username
from models.schemas import UserChangepassword, UserCreate, UserLogin, UsernameRole
from sqlalchemy.orm import Session
from common.logs import logger
from common.jsontools import response
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def decode_redis_hash(hash_dict):
    """
    将从 Redis 获取的字节串字典转换为字符串字典
    """
    return {key.decode('utf-8'): value.decode('utf-8') for key, value in hash_dict.items()}


@router.post('/create')
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("创建用户")
    if len(user.username) < 2 or len(user.username) > 16:
        return response(100106, "用户名长度不符合要求", "")
    if user.age < 18 or user.age > 65:
        return response(100103, "年龄不符合要求", "")
    if(user.role == "student" and user.studentNum == None) or (user.role == "teacher" and user.jobNum == None) or (
        user.role not in ["student", "teacher"]
    ):
        return response(100104, "角色不符合要求", "")
    
    # 判断用户名是否存在
    db_crest = get_user_by_username(db, user.username)
    if db_crest:
        return response(100105, "用户名已存在", "")
    
    try: 
        user.password = get_password_hash(user.password)
    except Exception as e:
        logger.exception(e)
        return response(100107, "密码加密失败", "")
    try:
        # 数据库 创建用户
        user = db_create_user(db, user)
        logger.info("创建用户成功")
        return response(200, "创建用户成功", {
            "username" : user.username,
        })
    except Exception as e:
        logger.exception(e)
        return response(100108, "创建用户失败", "")
    
@router.post('/login')
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    db_crest = get_user_by_username(db, user.username)
    if not db_crest:
        return response(100109, "用户名不存在", "")
    verifyPassword = verify_password(user.password, db_crest.password)
    if verifyPassword:
        user_redis = await request.app.state.redis.get(user.username)
        if not user_redis:
            try:
                token = create_access_token({"sub": user.username})
            except Exception as e:
                logger.exception(e)
                return response(100110, "生成token失败", "")
            await request.app.state.redis.setex(user.username, ACCESS_TOKEN_EXPIRE_MINUTES * 60, token)
            return response(200, "登录成功", {
                "token" : token,
            })
        else:
            return response(100111, "用户已登录", "")
    else:
        key = user.username+"_password"
        result_bytes = await request.app.state.redis.hgetall(key)
        if not result_bytes:
            times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            await request.app.state.redis.hmset(key, mapping={'num': 0, 'times': times})
        else:
            result = decode_redis_hash(result_bytes)
            errornum = int(result['num'])
            # strptime 将字符串转换为时间格式
            numtime = (datetime.now() - datetime.strptime(result['times'], "%Y-%m-%d %H:%M:%S")).seconds / 60
            
            if errornum < 5:
                errornum += 1
                await request.app.state.redis.hmset(key, mapping={'num': errornum})
                return response(100113, "密码错误", "")
            elif errornum >= 5 and numtime < 30:
                errornum += 1
                await request.app.state.redis.hmset(key, mapping = {'num': errornum})
                return response(100112, "密码错误次数过多，请30分钟后再试", "")
            else:
                errornum = 1
                times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                await request.app.state.redis.hmset(key, mapping={'num': errornum, 'times': times})
                return response(100113, "密码错误", "")
            
async def get_cure_user(request: Request, token: Optional[str] = Header(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    credentials_FOR_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="用户未登录或者token失效",   
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(payload) # {'sub': '张三'}
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        userCache = await request.app.state.redis.get(username)
        if not userCache and userCache != token:
            raise credentials_FOR_exception
        userRole = get_role_name(db, get_user_by_username(db, username).role)
        user = UsernameRole(username=username, role=userRole)
        return user
    except jwt.JWTError:
        logger.error(traceback.format_exc())
        raise credentials_exception
    
@router.get('/getCurrentUser')
async def get_current_user(user: UsernameRole = Depends(get_cure_user), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    data = {
        "username": db_user.username,
        "sex": db_user.sex,
        "age": db_user.age,
        "role": db_user.role,
    }
    if user.role == "student":
        data["studentNum"] = db_user.studentNum
    else:
        data["jobNum"] = db_user.jobNum

    return response(code=200, message="成功", data=data)

@router.post('/changepassword')
async def change_password(request: Request, changePwd: UserChangepassword, user = Depends(get_cure_user),  db: Session = Depends(get_db)):
    if changePwd.oldPassword == "" or changePwd.newPassword == "":
        return response(code=400, message="密码不能为空")
    if changePwd.newPassword == changePwd.oldPassword:
        return response(code=400, message="新密码不能与旧密码相同")
    db_user = get_user_by_username(db, user.username)
    print(db_user.password, changePwd.oldPassword, changePwd.newPassword)
    isVerify = verify_password(changePwd.oldPassword, db_user.password)
    if isVerify:
        hashPwd = get_password_hash(changePwd.newPassword)
        # db_user.update({"password": hashPwd})
        db_user.password = hashPwd
        print(db_user)
        try: 
            db.commit()
            db.refresh(db_user)
        except Exception as e:
            logger.exception(e)
            return response(code=500, message="修改密码失败")   
        
        request.app.state.redis.delete(user.username)
        request.app.state.redis.delete(user.username + "_password")
        return response(code=200, message="修改密码成功")
    return response(code=400, message="旧密码错误", data = '')