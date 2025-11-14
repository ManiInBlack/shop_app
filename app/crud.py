import sqlalchemy.exc
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import exists, update, MetaData
from app import models
from app.utils import hashing


##User

def create_user(db: Session, email: str, password: bytes) -> bool:
    new_user = models.User(
        email=email,
        password_hash=password
    )
    try:
        db.add(new_user)
        db.commit()

    except sqlalchemy.exc.IntegrityError:
        return False

    return True

def get_user(db: Session, email: str) -> models.User:
    stmt = (
        select(models.User)
        .where(models.User.email == email)
    )
    user = db.execute(stmt).scalar()
    return user


def get_user_hash(db: Session, email: str) -> bytes:
    stmt = (
        select(
            models.User.password_hash)
            .where(models.User.email == email)
    )
    user_hash = db.execute(stmt)

    return user_hash.scalar()

def user_exists(db: Session, email: str) -> bool:
    stmt = select(exists()
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



##Products
