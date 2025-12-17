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

from .schemas.base import Base
from .schemas.user_schema import User
from .schemas.bill_schema import Bill
from .schemas.expense_schema import Expense
from .schemas.category_schema import Category

DATABASE_URL = "sqlite+aiosqlite:///./trackyourmonny.db"


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