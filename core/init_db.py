from models.models import Base
from models.database import engine, SessionLocal
from common.logs import logger
def init_db(is_drop=False):
    '''初始化数据库
    
      Base 不能直接从 models.database 导入
    '''
    # 如果 is_drop 为 True 则删除数据库
    if is_drop:
        Base.metadata.drop_all(bind=engine)
    
    try:
        # 创建数据库表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库初始化成功")
    except Exception as e:
        logger.error("数据库初始化失败")
        logger.error(e)
  
def get_db():
    '''获取数据库会话'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()