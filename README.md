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

### redis 操作

```python
async def read_root(request: Request):
    # 使用 Redis 执行命令

    # await request.app.state.redis.set('my-key', 'value')
    # value = await request.app.state.redis.get('my-key')

    # hash
    # await request.app.state.redis.hmset('my-key1', {
    #     "a": "1",
    #     "b": "2",
    # })
    # value = await request.app.state.redis.hmget('my-key1', ["a", "b"])
    # print(value) # [b'1', b'2']
    # # value = decode_redis_hash(value)
    # return {"Hello": "World", "Redis Value": value}

    # list 
    # lpush 将一个或多个值插入到列表头部
    # rpush 将一个或多个值插入到列表尾部
    # lrange 获取列表指定范围内的元素
    # await request.app.state.redis.lpush('my-key2', "1", "2", "3")
    # value = await request.app.state.redis.lrange('my-key2', 0, -1)
    # print(value)
    # return {"Hello": "World", "Redis Value": value}

    # set
    # sadd 向集合添加一个或多个成员
    # smembers 返回集合中的所有成员
    # sismember 判断 member 元素是否是集合 key 的成员
    # srem 移除集合中一个或多个成员
    await request.app.state.redis.sadd('my-key3', "1", "2", "3")
    value = await request.app.state.redis.smembers('my-key3')
    print(value)
    return {"Hello": "World", "Redis Value": value}

    # 发布订阅
    #await request.app.state.redis.publish('channel:1', 'hello')
    # 订阅
    # await request.app.state.redis.subscribe('channel:1') 
```