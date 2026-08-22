from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time

class ItineraryActivityCreate(BaseModel):
    trip_stop_id: int
    activity_id: int
    date: date
    start_time: Optional[str] = None  # HH:MM format
    end_time: Optional[str] = None
    custom_cost: Optional[float] = None
    notes: Optional[str] = None

class ItineraryActivityResponse(BaseModel):
    id: int
    trip_stop_id: int
    activity_id: int
    date: date
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    custom_cost: Optional[float] = None
    activity_order: int = 0
    notes: Optional[str] = None
    activity: Optional[dict] = None
    destination_city: Optional[str] = None

    class Config:
        from_attributes = True

class ReorderActivitiesRequest(BaseModel):
    activity_ids: List[int]

class ItineraryDayGroup(BaseModel):
    date: date
    day_number: int
    city: str
    activities: List[ItineraryActivityResponse] = []
    day_cost: float = 0

class ItineraryResponse(BaseModel):
    success: bool = True
    trip_id: int
    days: List[ItineraryDayGroup] = []
    total_activities: int = 0
