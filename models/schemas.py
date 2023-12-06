from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: str
    jobNum: Optional[int] = None
    studentNum: Optional[int] = None
    sex: str = "man"
    age: int