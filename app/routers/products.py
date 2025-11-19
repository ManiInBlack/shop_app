from app.database import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
import app.models as models
import app.crud as crud
import app.schemas as schemas

router = APIRouter(prefix="/products", tags=["products"])

## Categories
@router.post("/add_category", response_model=schemas.CategoryResponse)
def add_category(category_id: int, category_name: str, db: Session = Depends(get_db)) -> None:
      crud.add_category(db, category_id, category_name)

@router.post("/get_category", response_model=schemas.CategoryResponse)
def get_category(request: schemas.CategoryRequest, db: Session = Depends(get_db)) -> models.Category | None:
    return crud.get_category(db, request.category_id)

@router.get("/list_categories")
def list_categories(db: Session = Depends(get_db)):
    return crud.list_categories(db)