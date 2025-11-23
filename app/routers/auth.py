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
from app import dependencies
router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(database.get_db)) -> Token:
    return jwt_handling.grant_access_token(db, form_data.username, form_data.password)


@router.post("/signup", response_model=dict)
def signup(user_in: UserBase, db: Session = Depends(database.get_db)):
    return dependencies.signup(user_in, db)


##Check change_password if JWT handles correctly
@router.post("/change_password")
def change_password(token: Annotated[models.User, Depends(jwt_handling.get_current_user)], request: PasswordChangeBase,
                    db: Session = Depends(database.get_db)) -> dict:
    return dependencies.change_password(token, request, db)