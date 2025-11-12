from fastapi import APIRouter
from app import models
from app.schemas import Token

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me", response_model=models.User)
def get_me(request: Token):
    return