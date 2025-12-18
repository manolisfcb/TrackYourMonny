from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from .base import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    bill = relationship("Bill", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    nickname: str = Column(String, unique=False, nullable=True)