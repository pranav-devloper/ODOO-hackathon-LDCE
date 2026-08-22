from pydantic import BaseModel, Field
from typing import Optional, List

class DestinationResponse(BaseModel):
    id: int
    city: str
    country: str
    region: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    cost_index: int = 3
    popularity: int = 50
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_saved: bool = False

    class Config:
        from_attributes = True

class DestinationListResponse(BaseModel):
    success: bool = True
    data: List[DestinationResponse] = []
    total: int = 0
