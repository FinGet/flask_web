import time
from fastapi import FastAPI, Request
from routers.test import router as test_router
from routers.user import router as user_router
from routers.user_db import router as user_db_router
from config import Settings
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class CustomHeaderMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request, call_next):
    response = await call_next(request)
    response.headers["X-Custom"] = "Example"
    return response
  
middleware = [
  Middleware(CustomHeaderMiddleware)
]

app = FastAPI(middleware=middleware)

settings = Settings()

app.include_router(test_router)
app.include_router(user_router)
app.include_router(user_db_router)

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
