from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from db_models import User
from database import get_db
from fastapi import Depends, HTTPException, status
from typing import List
from permissions.base import ModelPermission
from permissions.roles import get_role_permissions


class BearAuthException(Exception):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "dummy_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: str):
    to_encode = {"sub": data}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        payload_sub: str = payload.get("sub")
        if payload_sub is None:
            raise BearAuthException("Token could not be validated")
        return payload_sub
    except JWTError:
        raise BearAuthException("Token could not be validated")


def authenticate_user(db: Session, user_email: str, password: str):
    user = db.query(User).filter(User.email == user_email).first()
    print(user_email)
    print(password)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        user_email = get_token_payload(token)
    except BearAuthException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate bearer token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized, could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


class PermissionChecker:
    def __init__(self, permissions_required: List[ModelPermission]):
        self.permissions_required = permissions_required

    def __call__(self, user: User = Depends(get_current_user)):
        for permission_required in self.permissions_required:
            if permission_required not in get_role_permissions(user.role):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions to access this resource")
        return user
