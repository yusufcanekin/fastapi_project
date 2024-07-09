from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# This class creates a schema. When you pass an object of this class to a get method, 
# data fields of that object must be provided in the specified type.
class PostBase(BaseModel):
    title: str
    content: str = None,

class Post(PostBase):
    id:int
    created_at: datetime
    

class PostCreate(PostBase):
    pass

class UserBase(BaseModel):
    email:EmailStr #imported from pydantic, checks whether it is a valid e-mail

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    id:int
    created_at:datetime
