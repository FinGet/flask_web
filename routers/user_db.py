from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import SessionLocal
from pydantic import BaseModel

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/db/create_user", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/db/get_user/{id}", response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


## 嵌套模型
class Obj(BaseModel):
    user_id: int
    item: schemas.ItemCreate  # 子模型


@router.post("/db/create_item")
async def create_item(obj: Obj, db: Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=obj.item, user_id=obj.user_id)


@router.get("/db/get_items")
async def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db=db)
