import sqlite3
import dependencies
import sqlalchemy.exc
from pydantic import EmailStr
from sqlalchemy import select
from utils import hashing
import models
from sqlalchemy.orm import Session
from sqlalchemy import exists


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


def user_exists(db: Session, email: str) -> bool:
    result = db.execute(
        select(
            exists().where(models.User.email == email)
        )
    )
    return result.scalar()


def verify_password(db: Session, email: str, password: str) -> bool:
    if not user_exists(db, email) or not dependencies.validate_password(password):
        return False

    user_hash = db.execute(
        select(
            models.User.password_hash
        ).where(
            models.User.email == email
        )
    ).scalar()

    return hashing.verify_password(password, user_hash)
