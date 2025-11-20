
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.utils import jwt_handling
from app import models, schemas
from typing import Annotated
from app import crud



router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: Annotated[models.User, Depends(jwt_handling.get_current_active_user)]) -> schemas.User:
    return current_user

@router.get("/role", response_model=schemas.UserRole)
def read_my_role(current_user: Annotated[models.User, Depends(jwt_handling.get_current_active_user)], db: Session = Depends(get_db)) -> schemas.UserRole:
    return crud.get_user_role(db, current_user.user_id)

