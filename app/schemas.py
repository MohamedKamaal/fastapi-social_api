from pydantic import BaseModel , EmailStr
from datetime import datetime
from typing import Optional
#requests

class Post(BaseModel):
    title : str
    content : str
    user_id :Optional[int]=None

#response 
class User(BaseModel):
    email : EmailStr
    password : str

class PostResponse(BaseModel):
    title : str
    time : datetime=datetime.now()
    owner : User
    class config:
        orm_mode=True


class UserResponse(BaseModel):
    email : EmailStr
    class config:
        orm_mode=True

class UserInfo(BaseModel):
    id : int
    email : str
    class config:
        orm_mode = True

class token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int]=None


class Vote(BaseModel):
    post_id : int
    status : int =1