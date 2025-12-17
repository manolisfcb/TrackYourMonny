from fastapi import FastAPI
from app.services.user_service import auth_backend, fastapi_users, current_active_user
from app.db.schema import create_db_and_tables, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from app.models.user_model import UserRead, UserCreate, UserUpdate
from app.api.v1.expense import router as expense_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database and tables
    await create_db_and_tables()
    yield
    # Shutdown: any cleanup can be done here

app = FastAPI(lifespan=lifespan)
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])
app.include_router(expense_router, prefix="/api/v1", tags=["expenses"])


@app.get("/hello-world")
def home():
    return {"message": "Welcome to trackyourmony!"}