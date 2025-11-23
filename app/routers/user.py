from anyio import current_effective_deadline
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.utils import jwt_handling
from app import models, schemas
from typing import Annotated
from app import crud

router = APIRouter(prefix="/user", tags=["user"])



##FIX THIS
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: Annotated[models.User, Depends(jwt_handling.get_current_active_user)]) -> schemas.User:
    return current_user


@router.get("/list_permissions", response_model=list)
def read_user_permissions(current_user: Annotated[models.User, Depends(jwt_handling.get_current_active_user)],
                          db: Session = Depends(get_db)) -> List[models.Permissions.name]:
    user_role = crud.get_user_role(db, current_user.user_id)
    if user_role.role_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized",
                            headers={"WWW-Authenticate": "Bearer"}
                            )

    user_permissions = crud.get_role_permissions(db, user_role.role_id)
    permissions = []
    for i in user_permissions:
        permissions.append(crud.get_permissions_name(db, i))

    return permissions
