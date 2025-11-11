from datetime import timedelta, datetime, timezone

from dotenv import load_dotenv
import os
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
HASH_ALGORITH = os.getenv("HASH_ALGORITH")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITH)
    return encoded_jwt
