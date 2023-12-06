from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from .database import Base

class User(Base):
  '''用户基础表'''
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(length = 32), unique=True, index=True) # 用户名
  password = Column(String(length = 252)) # 密码
  status = Column(Integer, default = 0) # 状态 0:正常 1:禁用
  jobNum = Column(Integer, nullable = True) # 工号
  studentNum = Column(Integer, nullable = True) # 学号
  age = Column(Integer) # 年龄
  sex = Column(String(length = 8), default = "man") # 性别
  role = Column(String(length = 32)) # 角色
  createTime = Column(DateTime, default = datetime.now) # 添加时间

class Role(Base):
  '''角色表'''
  __tablename__ = "roles"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(length = 32), unique=True, index=True) # 角色名称
  createTime = Column(DateTime, default = datetime.now) # 添加时间

class Course(Base):
  '''课程表'''
  __tablename__ = "courses"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String(length = 32), unique=True, index=True) # 课程名称
  icon = Column(String(length = 252), nullable = True) # 课程图标
  desc = Column(String(length = 252), nullable = True) # 课程描述
  status = Column(Boolean, default = False) # 课程状态
  onsale = Column(Boolean, default = False) # 是否上架
  catalog = Column(Text, nullable=True) # 课程目录
  owner = Column(Integer, ForeignKey('users.id')) # 课程拥有者
  likeNum = Column(Integer, default = 0) # 点赞数
  createTime = Column(DateTime, default = datetime.now) # 添加时间

class StudentCourse(Base):
  '''学生课程表'''
  __tablename__ = "student_courses"
  id = Column(Integer, primary_key=True, index=True)
  students = Column(Integer, ForeignKey('users.id')) # 学生
  course = Column(Integer, ForeignKey('courses.id')) # 课程
  createTime = Column(DateTime, default = datetime.now) # 添加时间
  updateTime = Column(DateTime, default = createTime) # 更新时间
  status = Column(Integer, default = 0) # 课程状态 0:正常 1:删除

class CommentCourse(Base):
  '''课程评论表'''
  __tablename__ = "comment_courses"
  id = Column(Integer, primary_key=True, index=True)
  course = Column(Integer, ForeignKey('courses.id')) # 课程
  users = Column(Integer, ForeignKey('users.id')) # 用户
  pid = Column(Integer, nullable = True) # 父级评论
  createTime = Column(DateTime, default = datetime.now) # 添加时间
  top = Column(Boolean, default = False) # 是否置顶
  content = Column(Text) # 评论内容
  status = Column(Integer, default = 0) # 评论状态 0:正常 1:删除

class Message(Base):
  '''消息表'''
  __tablename__ = "messages"
  id = Column(Integer, primary_key=True, index=True)
  sender = Column(Integer, ForeignKey('users.id')) # 发送者
  accepter = Column(Integer, ForeignKey('users.id')) # 接收者
  read = Column(Boolean, default = False) # 是否已读
  sendTime = Column(String(length=252)) # 发送时间
  pid = Column(Integer, nullable = True) # 父级消息
  createTime = Column(DateTime, default = datetime.now) # 添加时间
  content = Column(Text) # 消息内容
  status = Column(Integer, default = 0) # 消息状态 0:正常 1:删除
