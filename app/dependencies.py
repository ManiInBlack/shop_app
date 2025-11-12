import re
import crud
from sqlalchemy.orm import Session
from utils import hashing


def register_user(db: Session, email: str, password: str) -> bool:
    if crud.user_exists(db, email) or not validate_password(password):
        return False
    password_hash = hashing.hash_password(password)
    return crud.create_user(db, email, password_hash)


#Temporary password policy
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if len(password) > 64:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True
