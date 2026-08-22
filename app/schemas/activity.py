from pydantic import BaseModel, Field
from typing import Optional, List

class ActivityResponse(BaseModel):
    id: int
    destination_id: int
    name: str
    description: Optional[str] = None
    category: str
    duration_hours: float = 2.0
    estimated_cost: float = 0
    image: Optional[str] = None
    rating: float = 4.0
    destination_city: Optional[str] = None

    class Config:
        from_attributes = True

class ActivityListResponse(BaseModel):
    success: bool = True
    data: List[ActivityResponse] = []
    total: int = 0
