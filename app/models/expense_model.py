from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import uuid
from datetime import datetime

class ExpenseBaseModel(BaseModel):
    amount: float = Field(..., gt=0, description="Amount of the expense")
    description: Optional[str] = Field(None, max_length=255, description="Description of the expense")
    category_id: uuid.UUID = Field(..., description="Category ID of the expense")
    expense_date: datetime = Field(..., description="Date of the expense")
    payment_method: str = Field(..., description="Payment method")
    currency: str = Field(..., description="Currency")

    model_config = ConfigDict(from_attributes=True)
        
class ExpenseCreateModel(ExpenseBaseModel):
    expense_date: str = Field(..., description="Date of the expense in YYYY-MM-DD format")
    user_id: uuid.UUID = Field(..., description="User ID")

class ExpenseUpdateModel(ExpenseBaseModel):
    pass
        
class ExpenseReadModel(ExpenseBaseModel):
    expense_id: str = Field(..., description="Unique identifier for the expense")
    user_id: uuid.UUID = Field(..., description="User ID")
    created_at: Optional[datetime]