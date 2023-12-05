from sqlalchemy import NullPool, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建数据库连接
# mysql+pymysql://用户名:密码@主机地址:端口/数据库名称?charset=utf8mb4
engine = create_engine(
    "mysql+pymysql://root:handy2023@localhost:3306/course?charset=utf8mb4",
    echo=True,
    poolclass=NullPool,
)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建数据库基类
Base = declarative_base()
