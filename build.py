import sqlite3

SQLITE_DB_PATH = 'test.db' # SQLite 数据库文件路径
SQLITE_DB_SCHEMA = 'test.sql' # SQLite 数据库架构文件路径

with open(SQLITE_DB_SCHEMA) as f: # 打开数据库架构文件
  create_db_sql = f.read() # 读取文件内容

db = sqlite3.connect(SQLITE_DB_PATH) # 连接数据库

with db: # with 创建一个上下文环境，当代码块执行完毕后，自动关闭数据库连接
  db.executescript(create_db_sql) # 执行数据库架构文件中的 SQL 语句

with db:
  db.execute("PRAGMA foreign_keys = ON") # 开启外键约束
  db.execute(
    'INSERT INTO members (account, password) VALUES ("finget", "0000")',
  ) # 插入一条数据
