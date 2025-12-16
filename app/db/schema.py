# from sqlalchemy import MetaData, String, create_engine
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from collections.abc import AsyncGenerator
import uuid
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import MetaData, String, ForeignKey, Column, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from fastapi import Depends


DATABASE_URL = "sqlite+aiosqlite:///./trackyourmonny.db"

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    bill = relationship("Bill", back_populates="user")
    nickname: str = Column(String, unique=False, nullable=True)
    
# PostgreSQL connection with pooling
# engine = create_async_engine(
#     DATABASE_URL,
#     pool_size=5,
#     max_overflow=5,
#     pool_pre_ping=True,
# )

class Bill(Base):
    __tablename__ = "bills"
    
    bill_id: str = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    amount: float = Column(String, nullable=False)
    description: str = Column(Text, nullable=True)
    date: datetime = Column(DateTime, default=datetime.utcnow)
    s3_url: str = Column(String, nullable=False)
    
    user = relationship("User", back_populates="bill")


engine = create_async_engine(DATABASE_URL, echo=True) # Remove SQLite for production use   
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        
async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)