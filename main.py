from fastapi import FastAPI
from core.init_db import init_db
from routers import user

init_db()

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["user"])

