import re

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from app import database, crud, models
from app.schemas import UserBase, PasswordChangeBase
from app.utils import hashing, jwt_handling


# Temporary password policy
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if len(password) > 64:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def signup(request: UserBase, db: Session = Depends(database.get_db)) -> dict:
    if crud.user_exists(db, str(request.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if not validate_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password doesn't match password policy."
        )

    password_hash = hashing.hash_password(request.password)
    crud.create_user(db, str(request.email), password_hash)

    return {"message": "Successfully registered user"}

def change_password(token: Annotated[models.User, Depends(jwt_handling.get_current_user)], request: PasswordChangeBase,
                    db: Session = Depends(database.get_db)) -> dict:
    not_authorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token.email != request.email:
        raise not_authorized
    user = crud.user_exists(db, str(request.email))
    if not user:
        raise not_authorized
    user_hash = crud.get_user_hash(db, str(request.email))
    if not hashing.verify_password(request.old_password, user_hash):
        raise not_authorized

    crud.update_password(db, str(request.email), request.new_password)
    return {"message": "Password changed successfully"}