import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Bill(Base):
    __tablename__ = "bills"

    bill_id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    amount: float = Column(String, nullable=False)
    description: str = Column(Text, nullable=True)
    date: datetime = Column(DateTime, default=datetime.utcnow)
    s3_url: str = Column(String, nullable=False)

    user = relationship("User", back_populates="bill")