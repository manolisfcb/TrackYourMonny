import uuid
from sqlalchemy import Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Expense(Base):
    __tablename__ = "expenses"

    expense_id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    amount: float = Column(Float, nullable=False)
    description: str = Column(Text, nullable=True)
    category_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("category.category_id"))
    expense_date: datetime = Column(DateTime, default=datetime.utcnow)
    payment_method: str = Column(String, nullable=False)
    currency: str = Column(String, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    
    
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")