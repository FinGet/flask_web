from sqlalchemy.orm import Session
from models.models import Role, User
from models.schemas import UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id, User.status == False).first()

def db_create_user(db: Session, user: UserCreate):
    roles = db.query(Role).filter(Role.name == user.role).first()
    # db_user = User(**user.dict())
    db_user = User(user.model_dump())
    db_user.role = roles.id
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username, User.status == False).first()