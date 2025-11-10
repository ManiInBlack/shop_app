import sqlite3

import sqlalchemy.exc
from pydantic import EmailStr
from sqlalchemy import select
from utils import hashing
import models
from sqlalchemy.orm import Session
from sqlalchemy import exists


def create_user(db: Session, email: EmailStr, password: str) -> bool:
    #Create new user
    try:
        new_user = models.User(email=str(email), password_hash=hashing.get_password_hash(password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    ##User already exists
    except sqlalchemy.exc.IntegrityError:
        return False

    return True

def get_user_by_email(db: Session, email: EmailStr) -> bool:
    result = db.execute(select(exists().where(models.User.email == email)))
    return result.scalar()


def verify_password(db: Session, email: EmailStr, password: str) -> bool:
    user_hash = db.execute(select(models.User.password_hash).where(models.User.email == email)).scalar()
    return hashing.verify_password(password, user_hash)
