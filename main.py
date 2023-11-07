import time
from fastapi import FastAPI, Request
from routers.test import router as test_router
from config import Settings

app = FastAPI()

settings = Settings()

app.include_router(test_router)

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
