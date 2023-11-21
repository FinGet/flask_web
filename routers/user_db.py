from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import crud, schemas
from db.database import SessionLocal

router = APIRouter()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@router.post('/db/create_user', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
  return crud.create_user(db=db, user=user)

@router.get('/db/get_user/{id}', response_model=schemas.User)
async def get_user(id: int, db: Session = Depends(get_db)):
  user = crud.get_user(db, user_id=id)
  if user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return user
  