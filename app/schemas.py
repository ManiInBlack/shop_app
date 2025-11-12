from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    email: EmailStr | None = None

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
    access_token: str
    token_type: str
