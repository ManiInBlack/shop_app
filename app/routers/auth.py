from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud
from app import database
from app.dependencies import validate_password
from app.schemas import UserBase, Token, PasswordChangeBase
from app.utils import hashing, jwt_handling
from typing import Annotated
from app import models

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)) -> Token:
    return jwt_handling.grant_access_token(db, form_data.username, form_data.password)


@router.post("/signup", response_model=Token)
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


##Check change_password if JWT handles correctly
@router.post("/change_password")
def change_password(token: Annotated[models.User, Depends(jwt_handling.get_current_user)], request: PasswordChangeBase, db: Session = Depends(database.get_db)) -> dict:
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
