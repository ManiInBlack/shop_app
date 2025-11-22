from pydantic import BaseModel, EmailStr
from datetime import datetime


## Users and authentication
class User(BaseModel):
    user_id: int
    email: str
    last_login: datetime
    role_id: int | None = None


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserRole(BaseModel):
    user_id: int
    role_id: int


class UserPermissions(BaseModel):
    role_id: int | None = None
    permission_id: int


class PasswordChangeBase(BaseModel):
    email: EmailStr
    old_password: str
    new_password: str


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


## Categories
class CategoryRequest(BaseModel):
    category_id: int


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

## Products
