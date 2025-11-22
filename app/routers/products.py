from typing import List, Annotated

from sqlalchemy.sql.functions import current_user

from app.database import get_db
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
import app.models as models
import app.crud as crud
import app.schemas as schemas
import app.utils.jwt_handling as jwt
from app.routers.user import read_user_permissions

router = APIRouter(prefix="/products", tags=["products"])


## Categories
@router.post("/add_category", response_model=bool)
def add_category(category_id: int, category_name: str, db: Session = Depends(get_db)) -> bool:
    crud.add_category(db, category_id, category_name)
    return True


@router.get("/list_categories", response_model=List[schemas.CategoryResponse])
def list_categories(db: Session = Depends(get_db)) -> List[models.Category | None]:
    return crud.list_categories(db)


## Products
#
# @router.post("/add_product", response_model=None)
# def add_product(user: Annotated[models.User, Depends(jwt.get_current_user)], db: Session = Depends(get_db)) -> List[models.RolePermissions]:
