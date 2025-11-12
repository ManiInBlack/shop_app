from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import schemas, models
from dotenv import load_dotenv
import os
import jwt
from app.utils import hashing
from typing import cast

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise Exception("SECRET_KEY is not set")

HASH_ALGORITHM = os.getenv("HASH_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt


def grant_access_token(db: Session, email: str, password: str) -> schemas.Token:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not hashing.verify_password(password, cast(bytes, user.password_hash)):
        raise HTTPException(status_code=401,
                            detail="Incorrect Username or Password",
                            headers={"WWW-Authenticate": "Basic"}
                            )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
