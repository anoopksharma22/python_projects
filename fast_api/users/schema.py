from pydantic import BaseModel
from typing import Optional


# class User(BaseModel):
#     id: Optional[int] = None
#     name:str
#     email:str
#     password:str
    
class UserBase(BaseModel):
    name: str
    email:str

class CreateUser(UserBase):
    password: str

class User(UserBase):  
    id: int
    class Config:
        orm_mode=True
    
    