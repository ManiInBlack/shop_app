from typing import List
import sqlalchemy.exc
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from sqlalchemy import exists, update, MetaData
from app import models
from app.utils import hashing


##User

def create_user(db: Session, email: str, password: bytes) -> None:
    new_user = models.User(
        email=email,
        password_hash=password
    )
    try:
        db.add(new_user)
        db.commit()

    except sqlalchemy.exc.IntegrityError as error:
        raise error
    return


def get_user(db: Session, email: str) -> models.User:
    stmt = (
        select(models.User)
        .where(models.User.email == email)
    )
    user = db.execute(stmt).scalar()
    return user


def get_user_hash(db: Session, email: str) -> bytes:
    stmt = (
        select(models.User.password_hash)
        .where(models.User.email == email)
    )
    user_hash = db.execute(stmt)

    return user_hash.scalar()


def user_exists(db: Session, email: str) -> bool:
    stmt = select(
        exists()
        .where(models.User.email == email)
    )
    result = db.execute(stmt)

    return result.scalar()


def update_password(db: Session, email: str, password: str) -> None:
    meta = MetaData()
    meta.reflect(bind=db.bind)

    password_hash = hashing.hash_password(password)

    pwd_change_stmt = (
        update(models.User)
        .values({"password_hash": bytes(password_hash)})
        .where(models.User.email == email)
    )

    db.execute(pwd_change_stmt)
    db.commit()
    return


## Roles
def get_user_role(db: Session, user_id: int) -> models.UserRole:
    stmt = (
        select(models.UserRole)
        .where(models.UserRole.user_id == user_id)
    )
    user = db.execute(stmt).scalar()
    return user


def get_role_name(db: Session, role_id: int) -> models.Roles.name:
    stmt = (
        select(models.Roles.name)
        .where(models.Roles.role_id == role_id)
    )
    role = db.execute(stmt).scalar()
    return role if role else None


def get_role_permissions(db: Session, role_id: int) -> List[models.RolePermissions.permission_id]:
    stmt = (
        select(models.RolePermissions.permission_id)
        .where(models.RolePermissions.role_id == role_id)
    )
    permission_id = list(db.execute(stmt).scalars().all())
    return permission_id if permission_id else None


def get_permission(db: Session, permission_id: int) -> models.Permissions.name:
    stmt = (
        select(models.Permissions.name)
        .where(models.Permissions.permission_id == permission_id)
    )
    permission = db.execute(stmt).scalar()
    return permission if permission else None


## Categories
def add_category(db: Session, category_id: int, category_name: str) -> bool:
    category = models.Category(
        id=category_id,
        name=category_name
    )
    try:
        db.add(category)
        db.commit()
    except sqlalchemy.exc.IntegrityError as error:
        raise error
    return True


def list_categories(db: Session) -> List[models.Category]:
    stmt = (
        select(models.Category)
    )
    categories = list(db.execute(stmt).scalars().all())
    return categories


# Products
def list_all_products(db: Session) -> List[models.Product]:
    stmt = (
        select(models.Product)
    )
    products = list(db.execute(stmt).scalars().all())
    return products


def list_products_by_category(db: Session, category_id: int) -> List[models.Product]:
    stmt = (
        select(models.Product)
        .where(models.Product.category_id == category_id)
    )
    products = list(db.execute(stmt).scalars().all())
    return products


def add_product(db: Session, product_id: int, name: str, price: float, category_id: int, quantity: int) -> None:
    product = models.Product(
        id=product_id,
        name=name,
        price=price,
        category_id=category_id,
        quantity=quantity
    )
    try:
        db.add(product)
        db.commit()

    except sqlalchemy.exc.IntegrityError as error:
        raise error
    return


def delete_product(db: Session, product_id: int) -> None:
    stmt = (
        delete(models.Product)
        .where(models.Product.id == product_id)
    )
    db.execute(stmt)
    db.commit()
    return
