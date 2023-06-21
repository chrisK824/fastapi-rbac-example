from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    password = Column(String)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    role = Column(String)
    register_date = Column(DateTime, default=func.now())

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
