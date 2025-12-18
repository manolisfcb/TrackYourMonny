
from sqlalchemy import select
from app.db.schemas.expense_schema import Expense
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import current_active_user
from app.models.expense_model import ExpenseCreateModel, ExpenseReadModel
from datetime import datetime
import uuid
class ExpenseService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_expense(self, expense: ExpenseCreateModel) -> ExpenseReadModel:
        orm_expense = Expense(
            user_id=expense.user_id,
            amount=expense.amount,
            description=expense.description,
            category_id=expense.category_id,
            expense_date=datetime.fromisoformat(expense.expense_date),
            payment_method=expense.payment_method,
            currency=expense.currency
        )
        self.session.add(orm_expense)
        await self.session.commit()
        await self.session.refresh(orm_expense)
        return ExpenseReadModel.model_validate(orm_expense)

    async def get_expense(self, expense_id: str) -> ExpenseReadModel | None:
        expense = await self.session.get(Expense, expense_id)
        return ExpenseReadModel.model_validate(expense) if expense else None

    async def get_expenses(self, skip: int = 0, limit: int = 10) -> list[ExpenseReadModel]:
        result = await self.session.execute(
            select(Expense).offset(skip).limit(limit)
        )
        expenses = result.scalars().all()
        return [ExpenseReadModel.model_validate(e) for e in expenses]
    
    async def delete_expense(self, expense_id: str) -> None:
        expense = await self.get_expense(expense_id)
        if expense:
            await self.session.delete(expense)
            await self.session.commit()
        return
    
    async def get_expenses_by_date_range(self, start_date: str, end_date: str) -> list[ExpenseReadModel]:
        result = await self.session.execute(
            select(Expense).where(Expense.expense_date >= start_date, Expense.expense_date <= end_date)
        )
        expenses = result.scalars().all()
        return [ExpenseReadModel.model_validate(e) for e in expenses]
    
    async def filter_expenses(self, **filters) -> list[ExpenseReadModel]:
        allowed_filters = {'category_id'}
        query = select(Expense)
        for attr, value in filters.items():
            if attr in allowed_filters:
                query = query.where(getattr(Expense, attr) == value)
            else:
                raise ValueError(f"Filtering by {attr} is not allowed.")
        result = await self.session.execute(query)
        expenses = result.scalars().all()
        return [ExpenseReadModel.model_validate(e) for e in expenses]