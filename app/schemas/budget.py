from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class ExpenseCreate(BaseModel):
    category: str = Field(..., pattern="^(transport|accommodation|activities|meals|other)$")
    description: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0)
    date: Optional[date] = None
    notes: Optional[str] = None

class ExpenseUpdate(BaseModel):
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[date] = None
    notes: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    trip_id: int
    category: str
    description: str
    amount: float
    date: Optional[date] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class BudgetCategoryBreakdown(BaseModel):
    category: str
    total: float
    percentage: float = 0
    count: int = 0

class BudgetSummary(BaseModel):
    success: bool = True
    trip_id: int
    estimated_budget: float = 0
    total_spent: float = 0
    remaining: float = 0
    percentage_used: float = 0
    average_per_day: float = 0
    total_days: int = 0
    status: str = "ON_TRACK"  # ON_TRACK, WARNING, OVER_BUDGET
    categories: List[BudgetCategoryBreakdown] = []
    expenses: List[ExpenseResponse] = []
    daily_alerts: List[dict] = []
