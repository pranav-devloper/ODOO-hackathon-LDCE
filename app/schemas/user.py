from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    profile_image: Optional[str] = None
    language: str = "en"
    is_active: bool = True
    is_admin: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_image: Optional[str] = None
    language: Optional[str] = None

class UserStats(BaseModel):
    total_trips: int = 0
    total_cities: int = 0
    total_activities: int = 0
    total_countries: int = 0
