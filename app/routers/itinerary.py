from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import time as time_type
from app.core.dependencies import get_db, get_current_user_required
from app.schemas.itinerary import ItineraryActivityCreate, ReorderActivitiesRequest
from app.services import itinerary_service, trip_service
from app.database.models import User

router = APIRouter(prefix="/api", tags=["itinerary"])

@router.get("/trips/{trip_id}/itinerary")
def get_itinerary(trip_id: int, db: Session = Depends(get_db)):
    try:
        result = itinerary_service.get_trip_itinerary(db, trip_id)
        return {"success": True, "data": result, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_ITINERARY_FAILED", "message": str(e)}}

@router.post("/trips/{trip_id}/itinerary")
def add_itinerary_activity(trip_id: int, request: ItineraryActivityCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trip = trip_service.get_trip(db, trip_id)
        if not trip or trip.user_id != user.id:
            return {"success": False, "data": None, "error": {"code": "UNAUTHORIZED", "message": "Trip not found or unauthorized"}}

        # Parse time strings
        start_time = None
        end_time = None
        if request.start_time:
            parts = request.start_time.split(":")
            start_time = time_type(int(parts[0]), int(parts[1]))
        if request.end_time:
            parts = request.end_time.split(":")
            end_time = time_type(int(parts[0]), int(parts[1]))

        activity = itinerary_service.add_itinerary_activity(
            db,
            trip_stop_id=request.trip_stop_id,
            activity_id=request.activity_id,
            date_val=request.date,
            start_time=start_time,
            end_time=end_time,
            custom_cost=request.custom_cost,
            notes=request.notes
        )
        return {"success": True, "data": {
            "id": activity.id,
            "activity_id": activity.activity_id,
            "date": str(activity.date),
            "activity_order": activity.activity_order,
        }, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "ADD_ACTIVITY_FAILED", "message": str(e)}}

@router.delete("/itinerary/{itinerary_activity_id}")
def remove_itinerary_activity(itinerary_activity_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        success = itinerary_service.remove_itinerary_activity(db, itinerary_activity_id)
        if not success:
            return {"success": False, "data": None, "error": {"code": "NOT_FOUND", "message": "Activity not found"}}
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "REMOVE_ACTIVITY_FAILED", "message": str(e)}}

@router.patch("/trips/{trip_id}/itinerary/reorder")
def reorder_activities(trip_id: int, request: ReorderActivitiesRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trip = trip_service.get_trip(db, trip_id)
        if not trip or trip.user_id != user.id:
            return {"success": False, "data": None, "error": {"code": "UNAUTHORIZED", "message": "Unauthorized"}}
        itinerary_service.reorder_itinerary_activities(db, trip_id, request.activity_ids)
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "REORDER_FAILED", "message": str(e)}}
