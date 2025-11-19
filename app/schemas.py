from pydantic import BaseModel, EmailStr
from datetime import datetime

## Users and authentication
class User(BaseModel):
    user_id: int
    email: str
    last_login: datetime

class TokenData(BaseModel):
    username: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    email: EmailStr
    password: str

class PasswordChangeBase(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str

## Categories
class CategoryRequest(BaseModel):
    category_id: int

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
