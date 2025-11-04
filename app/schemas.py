
# pylint: disable=C0115

from pydantic import BaseModel, conint
from datetime import datetime
from pydantic import EmailStr
from typing import Optional


class PostBase(BaseModel):
    title : str
    content : str
    published : bool=True

class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostOut(BaseModel):
    Post: Post 
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Userlogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional [int] = None
    

class Vote(BaseModel):
    post_id: int
    dir: conint (le=1)


class Config:
    orm_mode=True