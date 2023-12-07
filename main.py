from contextlib import asynccontextmanager
from fastapi import FastAPI
from aioredis import create_redis_pool, Redis
from core.init_db import init_db
from routers import user

from config import *
init_db()



async def get_redis():
    redis = await create_redis_pool(f"redis://:@"+redishost+":"+redisport+"/"+redisdb+"?encoding=utf-8")
    return redis

# @app.on_event("startup")
# async def startup():
#     app.state.redis = await get_redis()

# @app.on_event("shutdown")
# async def shutdown():
#     app.state.redis.close()
#     await app.state.redis.wait_closed()

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await get_redis()
    yield
    app.state.redis.close()
    await app.state.redis.wait_closed()

app = FastAPI(lifespan=lifespan) 


app.include_router(user.router, prefix="/user", tags=["user"])

