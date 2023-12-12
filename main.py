from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from redis import asyncio as aioredis
import uvicorn
from core.init_db import init_db
from routers import user
import sys

from config import *
init_db()

print('now env is:', sys.executable) # check which python interpreter is used


# async def get_redis():
#     redis = await create_redis_pool(f"redis://:@"+redishost+":"+redisport+"/"+redisdb+"?encoding=utf-8")
#     return redis

# @app.on_event("startup")
# async def startup():
#     app.state.redis = await get_redis()

# @app.on_event("shutdown")
# async def shutdown():
#     app.state.redis.close()
#     await app.state.redis.wait_closed()

async def get_redis():
    redis = await aioredis.from_url(f"redis://:@"+redishost+":"+redisport+"/"+redisdb+"?encoding=utf-8")
    return redis
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await get_redis()
    try:
        yield
    finally:
        await app.state.redis.close()

app = FastAPI(lifespan=lifespan) 

app.include_router(user.router, prefix="/user", tags=["user"])

@app.get("/")
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
    

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)