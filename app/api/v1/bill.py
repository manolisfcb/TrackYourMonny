from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from app.services.user_service import UserService
from app.models.user_model import UserCreate, UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.schema import get_session

router = APIRouter()

def get_user_service() -> UserService:
    # Placeholder for user service dependency
    return UserService()

@router.get("/upload-bill")
def upload_bill_form(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    pass  # To be implemented: handle file upload and save to database