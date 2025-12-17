
from sqlalchemy import select
from app.db.schemas.expense_schema import Expense
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import current_active_user

class ExpenseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_expense(self, expense: Expense) -> Expense:
        self.session.add(expense)
        await self.session.commit()
        await self.session.refresh(expense)
        return expense

    async def get_expense(self, expense_id: str) -> Expense | None:
        return await self.session.get(Expense, expense_id)

    async def get_expenses(self, skip: int = 0, limit: int = 10) -> list[Expense]:
        result = await self.session.execute(
            select(Expense).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def delete_expense(self, expense_id: str) -> None:
        expense = await self.get_expense(expense_id)
        if expense:
            await self.session.delete(expense)
            await self.session.commit()
        return
    
    async def get_expenses_by_date_range(self, start_date: str, end_date: str) -> list[Expense]:
        result = await self.session.execute(
            select(Expense).where(Expense.date >= start_date, Expense.date <= end_date)
        )
        return result.scalars().all()
    
    async def filter_expenses(self, **filters) -> list[Expense]:
        allowed_filters = {'category_id'}
        query = select(Expense)
        for attr, value in filters.items():
            if attr in allowed_filters:
                query = query.where(getattr(Expense, attr) == value)
            else:
                raise ValueError(f"Filtering by {attr} is not allowed.")
        result = await self.session.execute(query)
        return result.scalars().all()