from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import aioredis
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
    await request.app.state.redis.set('my-key', 'value')
    value = await request.app.state.redis.get('my-key')
    return {"Hello": "World", "Redis Value": value}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)