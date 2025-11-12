from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import crud
from app import database
from app.dependencies import validate_password
from app.schemas import UserBase, Token, PasswordChangeBase
from app.utils.jwt_handling import grant_access_token
from app.utils import hashing

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/token", response_model=Token)
def login(request: UserBase, db: Session = Depends(database.get_db)):
    return grant_access_token(db, str(request.email), request.password)


@router.post("/signup", response_model=Token)
def signup(request: UserBase, db: Session = Depends(database.get_db)) -> bool:
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
    return True


@router.post("/change_password")
def change_password(request: PasswordChangeBase, db: Session = Depends(database.get_db)) -> bool:
    user = crud.user_exists(db, str(request.email))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Not Authorize"
        )
    user_hash = crud.get_user_hash(db, str(request.email))
    if not hashing.verify_password(request.old_password, user_hash):
        raise HTTPException(
            status_code=401,
            detail="Not Authorized"
        )

    crud.update_password(db, str(request.email), request.new_password)
    return True
