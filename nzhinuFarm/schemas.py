from pydantic import BaseModel, EmailStr
from typing import List
from enum import Enum


class Role(Enum):
    user = "user"
    admin = "admin"
    superAdmin = "superAdmin"

class Item(BaseModel):
    title : str
    description : str

class ItemCreate(Item):
    owner_id:int

class ItemBase(Item):
    id: int
    owner_id:int
    
class User(BaseModel):
    id:int
    email : EmailStr
    username : str
    role : str
    items : List[Item] = []
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    username : str
    password : str
    role : str
