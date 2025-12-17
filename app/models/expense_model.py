from pydantic import BaseModel, Field

class ExpenseBaseModel(BaseModel):
    amount: float = Field(..., gt=0, description="Amount of the expense")
    description: str = Field(..., max_length=255, description="Description of the expense")
    category: str = Field(..., max_length=100, description="Category of the expense")
    date: str = Field(..., description="Date of the expense in YYYY-MM-DD format")

    class Config:
        orm_mode = True
        
class ExpenseCreateModel(ExpenseBaseModel):
    pass

class ExpenseUpdateModel(ExpenseBaseModel):
    pass
        
class ExpenseReadModel(ExpenseBaseModel):
    id: str = Field(..., description="Unique identifier for the expense")