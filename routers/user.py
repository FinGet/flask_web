from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from core.init_db import get_db
from models.crud import db_create_user, get_user_by_username
from models.schemas import UserCreate
from sqlalchemy.orm import Session
from common.logs import logger
from common.jsontools import response
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

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
        return response(200, "创建用户成功", user.model_dump())
    except Exception as e:
        logger.exception(e)
        return response(100108, "创建用户失败", "")
    


