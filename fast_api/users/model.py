from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import Session
from configs.database import Base
from . import schema
from auth import oauth2

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name =  Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

def get_user_by_id(db_session:Session,id:int):
    return db_session.query(User).filter(User.id== id).first()
    
def get_user_by_email(db_session:Session,email:str):
    return db_session.query(User).filter(User.email== email).first()

def get_all_users(db_session: Session, skip: int = 0, limit: int = 100):
    return db_session.query(User).offset(skip).limit(limit).all()

def create_user(db_session:Session, user:schema.User):
    hashed_password = oauth2.get_password_hash(user.password)
    db_user = User(name=user.name,email=user.email,password=hashed_password)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

