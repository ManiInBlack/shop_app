from typing import List
from app.database import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import app.models as models
import app.crud as crud
import app.schemas as schemas

router = APIRouter(prefix="/products", tags=["products"])

## Categories
@router.post("/add_category", response_model=bool)
def add_category(category_id: int, category_name: str, db: Session = Depends(get_db)) -> bool:
      crud.add_category(db, category_id, category_name)
      return True

@router.post("/get_category", response_model=schemas.CategoryResponse)
def get_category(request: schemas.CategoryRequest, db: Session = Depends(get_db)) -> models.Category | None:
    return crud.get_category(db, request.category_id)

@router.get("/list_categories", response_model=List[schemas.CategoryResponse])
def list_categories(db: Session = Depends(get_db)) -> List[models.Category | None]:
    return crud.list_categories(db)

## Products

# @router.post("/add_product", response_model=bool)
# def add_product(token: Annotated[models.User, Depends(jwt.get_current_user)], db: Session = Depends(get_db)) -> bool:

