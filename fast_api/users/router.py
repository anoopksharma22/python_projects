from fastapi import APIRouter,status, Depends,HTTPException
from sqlalchemy.orm.session import Session
from users.schema import User,CreateUser
from . import model
from typing import List
from configs.database import get_db

from auth.oauth2 import oauth2_scheme,current_user_from_token



router = APIRouter(tags=["user"],prefix="/users",)


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        

@router.get("/",response_model=List[User])
def get_all_users(db_session: Session = Depends(get_db),skip: int = 0, limit: int = 100,user: User = Depends(current_user_from_token)):
    all_users = model.get_all_users(db_session=db_session,skip=skip,limit=limit)
    if len(all_users) == 0:
        raise UserNotFoundException()
    return all_users

@router.get("/{user_id}/",response_model=User)
def get_users(user_id:int,db_session: Session = Depends(get_db),user: User = Depends(current_user_from_token)):
    user = model.get_user_by_id(db_session=db_session,id=user_id)
    if user:
        return user
    raise UserNotFoundException()

@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)
def create_user( user:CreateUser, db_session:Session = Depends(get_db)):
    user_by_email = model.get_user_by_email(db_session=db_session,email=user.email)
    if user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return model.create_user(db_session=db_session, user=user)  