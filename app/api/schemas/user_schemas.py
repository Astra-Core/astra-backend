from pydantic import BaseModel, EmailStr
from typing import Optional


class UserName(BaseModel):
    username: str

class UserBase(UserName):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: str

class UserCreateResponse(UserBase):
    class Config:
        from_attributes = True