import datetime
from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel
from typing import Annotated, Any, Optional, Union
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from jose import ExpiredSignatureError, JWTError, jwt

router = APIRouter() 

fake_user_db = [
  {"username": "foo", "password": '123456' },
  {"username": "admin", "password": '123321' },
]

class User(BaseModel):
  username: str
  password: str

@router.post("/users/me")
async def read_user_me(user: User):
  is_user = False
  for db_user in fake_user_db:
    if db_user["username"] == user.username and db_user["password"] == user.password:
      is_user = True
      break

  return {"is_user": is_user}

security = HTTPBasic()

# basic auth
@router.post("/users/login")
async def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
  return {"username": credentials.username, "password": credentials.password}



# 加密密钥
SECRET_KEY = '3c2291a895c805b34abdd2c52e2b121c170d13b3c60316cf6468724da9d606e1'

# 设置过期时间 现在时间 + 10小时
expire = datetime.datetime.utcnow() + datetime.timedelta(hours=10)

to_encode = {"exp": expire, "username": "admin", "password": "123321"}

# 加密生成token
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
print(encoded_jwt)

# 解密token
decoded_jwt = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=["HS256"])

# 错误的token

try: 
  payload = jwt.decode(encoded_jwt, "wrong_key", algorithms=["HS256"])
except ExpiredSignatureError:
  print("token过期")
except JWTError:
  print("token错误")

# Union[str, Any]表示一个可以是str类型或者任何其他类型的变量
def create_access_token(subject: Union[str, Any], expires_delta: datetime.timedelta = None):
  if expires_delta:
    expire = datetime.datetime.utcnow() + expires_delta
  else:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=10)

  to_encode = {"exp": expire, "sub": str(subject)}
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

  return encoded_jwt


# Optional[str] 表示可选参数 等价于 Union[str, None]
# Header(...) 是一个装饰器，用于获取请求头的值
def check_jwt_token(token: Optional[str] = Header(..., alias="Authorization")):
  print(token)
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
  except ExpiredSignatureError:
    return 'token过期'
  except (JWTError, AttributeError):
    return 'token错误'
  
@router.post("/login/token")
def login_get_token(user: User):
  is_user = False
  for db_user in fake_user_db:
    if db_user["username"] == user.username and db_user["password"] == user.password:
      is_user = True
      break

  if is_user:
    return {"token": create_access_token(user.username)}
  else:
    return {"token": None}
  
@router.post('/login/check')
def login_check(token: Union[str, Any] = Depends(check_jwt_token)):
  return {"user_info": token}

# Depends是一个用于依赖注入的FastAPI框架中的装饰器。
# 它的作用是将依赖项注入到函数中，以便在函数被调用时使用这些依赖项。
# 依赖项可以是其他函数、类、对象或任何可调用的对象。
# 在上面的代码片段中，Depends装饰器用于指定login_check函数依赖于
# check_jwt_token函数的返回值作为参数。
# 这意味着在调用login_check函数之前，
# 将调用check_jwt_token函数并将其返回值作为token参数传递给login_check函数。

# Depends装饰器在FastAPI框架中广泛应用，用于处理请求和响应之前的验证、
# 身份验证、数据库连接、日志记录等依赖项。
# 它提供了一种优雅和可扩展的方式来管理应用程序的依赖关系。