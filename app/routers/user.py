
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from app.utils import jwt_handling
from app import models, schemas
from typing import Annotated
import os


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: Annotated[models.User, Depends(jwt_handling.get_current_active_user)]):
    return current_user

