from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from permissions.roles import Role


class UserSignUp(BaseModel):
    email: EmailStr
    password: Optional[str]
    name: str
    surname: Optional[str] = None
    role: Role


class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    roles: Optional[Role]


class User(BaseModel):
    email: EmailStr
    name: str
    surname: Optional[str]
    role: Role
    register_date: Optional[datetime]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ItemIn(BaseModel):
    name: str


class ItemUpdate(BaseModel):
    name: str


class Item(ItemIn):
    id: int

    class Config:
        from_attributes = True
