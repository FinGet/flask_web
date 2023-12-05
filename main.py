from fastapi import FastAPI
from core.init_db import init_db
init_db()

app = FastAPI()

