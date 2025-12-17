import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Category(Base):
    __tablename__ = "category"

    category_id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: str = Column(String, nullable=False)
    description: str = Column(Text, nullable=True)


    category = relationship("Expense", back_populates="category")