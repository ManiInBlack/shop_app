from app import crud
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db

### VALIDATE PERMISSIONS

def validate_permission(user_id: int, permission_id: int, db: Session = Depends(get_db)) -> bool:
    user_role = crud.get_user_role(db, user_id)
    permissions = crud.get_role_permissions(db, user_role.role_id)
    if permission_id not in permissions:
        return False
    return True