from sqlalchemy.orm import Session
from db_models import User
import schemas as schemas
from sqlalchemy.exc import IntegrityError
from authentication import get_password_hash


class DuplicateError(Exception):
    pass


def add_user(db: Session, user: schemas.UserSignUp):
    user = User(
        email=user.email,
        password=get_password_hash(user.password),
        name=user.name,
        surname=user.surname,
        role=user.role
    )
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateError(
            f"Email {user.email} is already attached to a registered user.")
    return user


def get_users(db: Session):
    users = list(db.query(User).all())
    return users


def update_user(db: Session, email: str, user_update: schemas.UserUpdate):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise ValueError(
            f"There isn't any user with username {email}")

    updated_user = user_update.dict(exclude_unset=True)
    for key, value in updated_user.items():
        setattr(user, key, value)
    db.commit()
    return user


def delete_user(db: Session, email: str):
    user_cursor = db.query(User).filter(User.email == email)
    if not user_cursor.first():
        raise ValueError(f"There is no user with email {email}")
    else:
        user_cursor.delete()
        db.commit()


