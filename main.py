import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from routers.test import router as test_router
from routers.user import router as user_router
from routers.user_db import router as user_db_router
from routers.oauth2 import router as oauth2_router
from config import Settings
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from log import logger


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Custom"] = "Example"
        return response


class CustomExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error("error: ", e)
            print("error: ", e)
            return JSONResponse(
                status_code=500,
                content={"message": "Server Error"},
            )
        return response


middleware = [
    Middleware(CustomHeaderMiddleware),
    Middleware(CustomExceptionMiddleware),
]

app = FastAPI(middleware=middleware, title="FastAPI 学习文档", description="FastAPI Demo")

settings = Settings()

logger_ac = logging.getLogger("uvicorn.access")
logger_ac.handlers = []

# 静态文件
# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(test_router)
app.include_router(user_router)
app.include_router(user_db_router)
app.include_router(oauth2_router)


@app.get("/error")
async def error():
    logger.info("请求错误接口")
    print(a)
    b = 1 / 0
    # try:
    #   print(a)
    #   b = 1 / 0
    # except Exception as e:
    #   print('err: ', e)
    #   raise HTTPException(status_code=500, detail="Server Error")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/setting")
async def get_settings():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
        "model_config": settings.model_config,
    }
