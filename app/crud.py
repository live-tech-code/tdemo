from sqlalchemy.orm import Session
from . import models

def create_user(db: Session, username: str, email: str, password_hash: str):
    db_user = models.User(username=username, email=email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def approve_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.approved = True
        db.commit()
        db.refresh(db_user)
    return db_user

# def get_users(db: Session):
#     db_user = db.query(models.User).scalars().all()
#     if db_user:
#         db.commit()
#         db.refresh(db_user)
#     return db_user 
    
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
