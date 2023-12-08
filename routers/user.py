from datetime import datetime
from fastapi import APIRouter, Depends, Request
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from core.init_db import get_db
from models.crud import db_create_user, get_user_by_username
from models.schemas import UserCreate, UserLogin
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
    db_crest = get_user_by_username(db, user.username)
    if db_crest:
        return response(100105, "用户名已存在", "")
    
    try: 
        user.password = get_password_hash(user.password)
    except Exception as e:
        logger.exception(e)
        return response(100107, "密码加密失败", "")
    try:
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
        result = await request.app.state.redis.hgetall(user.username+"_password", encoding = "utf-8")
        if not result:
            times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            await request.app.state.redis.hmset_dict(user.username+"_password", num = 0, times = times)
        else:
            errornum = int(result["num"])
            numtime = (datetime.now() - datetime.strptime(result["times"], "%Y-%m-%d %H:%M:%S")).seconds / 60

            if errornum < 5 and numtime < 30:
                errornum += 1
                await request.app.state.redis.hmset_dict(user.username+"_password", num = errornum)
                return response(100113, "密码错误", "")
            elif errornum < 5 and numtime >= 30:
                errornum = 1
                times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                request.app.state.redis.hmset_dict(user.username+"_password", num = errornum, times = times)
                return response(100113, "密码错误", "")
            elif errornum > 5 and numtime < 30:
                errornum += 1
                await request.app.state.redis.hmset_dict(user.username+"_password", num = errornum)
                return response(100112, "密码错误次数过多，请30分钟后再试", "")
            else:
                errornum = 1
                times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                request.app.state.redis.hmset_dict(user.username+"_password", num = errornum, times = times)
                return response(100113, "密码错误", "")