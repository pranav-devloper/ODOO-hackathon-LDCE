from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class TripCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: date
    end_date: date
    cover_image: Optional[str] = None
    estimated_budget: float = Field(default=0, ge=0)
    destinations: Optional[List[int]] = None

class TripUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    cover_image: Optional[str] = None
    estimated_budget: Optional[float] = Field(None, ge=0)
    is_public: Optional[bool] = None

class TripStopCreate(BaseModel):
    destination_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None

class TripStopResponse(BaseModel):
    id: int
    trip_id: int
    destination_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    stop_order: int
    notes: Optional[str] = None
    destination: Optional[dict] = None

    class Config:
        from_attributes = True

class ReorderStopsRequest(BaseModel):
    stop_ids: List[int]

class TripResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    cover_image: Optional[str] = None
    estimated_budget: float = 0
    is_public: bool = False
    share_token: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    stops: List[TripStopResponse] = []
    total_days: int = 0
    total_cities: int = 0
    total_cost: float = 0

    class Config:
        from_attributes = True

class TripListResponse(BaseModel):
    success: bool = True
    data: List[TripResponse] = []
