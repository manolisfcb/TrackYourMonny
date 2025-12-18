from fastapi import APIRouter, Depends, HTTPException

from app.models.expense_model import ExpenseCreateModel, ExpenseReadModel, ExpenseUpdateModel
from app.db.schema import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.expense_service import ExpenseService

router = APIRouter()


@router.post("/expenses/", response_model=ExpenseReadModel)
async def create_expense(expense: ExpenseCreateModel, session: AsyncSession = Depends(get_session)):
    expense_service = ExpenseService(session)
    return await expense_service.create_expense(expense)


@router.get("/expenses/{expense_id}", response_model=ExpenseReadModel)
async def read_expense(expense_id: str, session: AsyncSession = Depends(get_session)):
    expense_service = ExpenseService(session)
    expense = await expense_service.get_expense(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.get("/expenses/", response_model=list[ExpenseReadModel])
async def read_expenses(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)):
    expense_service = ExpenseService(session)
    return await expense_service.get_expenses(skip=skip, limit=limit)

@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: str, session: AsyncSession = Depends(get_session)):
    expense_service = ExpenseService(session)
    await expense_service.delete_expense(expense_id)
    return {"detail": "Expense deleted"}

@router.get("/expenses/date-range/", response_model=list[ExpenseReadModel])
async def get_expenses_by_date_range(start_date: str, end_date: str, session: AsyncSession = Depends(get_session)):
    expense_service = ExpenseService(session)
    return await expense_service.get_expenses_by_date_range(start_date, end_date)

@router.get("/expenses/filter/", response_model=list[ExpenseReadModel])
async def filter_expenses(session: AsyncSession = Depends(get_session), **filters):
    expense_service = ExpenseService(session)
    return await expense_service.filter_expenses(**filters)

