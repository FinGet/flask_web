# 在线课程学习系统

> poetry init

## 项目结构

```bash
.
├── Dockerfile
├── README.md
├── common
│   ├── __init__.py
│   ├── jsontools.py
│   └── logs.py
├── config.py
├── logs
├── main.py
├── models
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── get_db.py
│   ├── models.py
│   ├── schemas.py
│   └── testDatabase.py
├── pyproject.toml
├── router.md
├── routers
│   ├── __init__.py
│   ├── course.py
│   ├── file.py
│   ├── user.py
│   └── websoocket.py
└── test
    ├── __init__.py
    └── testmain.py
```
## 虚拟环境 启动项目
```base
/usr/bin/env /Users/xxxx/Library/Caches/pypoetry/virtualenvs/fast-course-xlbmpjxb-py3.10/bin/python -m uvicorn main:app --reload
```

## 安装 redis
```bash
brew install redis

# 启动 redis & run in background
brew services start redis 
```