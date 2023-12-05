from pydantic import BaseModel
from sqlalchemy import Column, Integer


class User(BaseModel):
  '''用户基础表'''
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)