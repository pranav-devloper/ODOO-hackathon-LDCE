from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.core.dependencies import get_db, get_current_user_required
from app.schemas.trip import TripCreate, TripUpdate, TripStopCreate, ReorderStopsRequest
from app.services import trip_service
from app.database.models import User

router = APIRouter(prefix="/api/trips", tags=["trips"])

@router.get("/")
def list_trips(filter: Optional[str] = None, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trips = trip_service.get_user_trips(db, user.id, filter)
        trips_data = []
        for trip in trips:
            trips_data.append({
                "id": trip.id,
                "name": trip.name,
                "description": trip.description,
                "start_date": str(trip.start_date) if trip.start_date else None,
                "end_date": str(trip.end_date) if trip.end_date else None,
                "cover_image": trip.cover_image,
                "estimated_budget": trip.estimated_budget,
                "is_public": trip.is_public,
                "share_token": trip.share_token,
                "total_cities": len(trip.stops) if trip.stops else 0,
            })
        return {"success": True, "data": trips_data, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_TRIPS_FAILED", "message": str(e)}}

@router.post("/")
def create_trip(request: TripCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        if request.start_date >= request.end_date:
            return {"success": False, "data": None, "error": {"code": "INVALID_DATES", "message": "Start date must be before end date"}}
        trip_data = request.model_dump(exclude_unset=True)
        trip = trip_service.create_trip(db, user.id, trip_data)
        return {"success": True, "data": {"id": trip.id, "name": trip.name}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "CREATE_TRIP_FAILED", "message": str(e)}}

@router.get("/{trip_id}")
def get_trip(trip_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trip = trip_service.get_trip(db, trip_id)
        if not trip:
            return {"success": False, "data": None, "error": {"code": "TRIP_NOT_FOUND", "message": "Trip not found"}}
        if trip.user_id != user.id:
            return {"success": False, "data": None, "error": {"code": "UNAUTHORIZED", "message": "You do not own this trip"}}
        stops_data = []
        for stop in sorted(trip.stops, key=lambda s: s.stop_order):
            stops_data.append({
                "id": stop.id,
                "destination_id": stop.destination_id,
                "city": stop.destination.city if stop.destination else "",
                "country": stop.destination.country if stop.destination else "",
                "start_date": str(stop.start_date) if stop.start_date else None,
                "end_date": str(stop.end_date) if stop.end_date else None,
                "stop_order": stop.stop_order,
                "notes": stop.notes,
                "latitude": stop.destination.latitude if stop.destination else None,
                "longitude": stop.destination.longitude if stop.destination else None,
            })
        trip_data = {
            "id": trip.id,
            "name": trip.name,
            "description": trip.description,
            "start_date": str(trip.start_date) if trip.start_date else None,
            "end_date": str(trip.end_date) if trip.end_date else None,
            "cover_image": trip.cover_image,
            "estimated_budget": trip.estimated_budget,
            "is_public": trip.is_public,
            "share_token": trip.share_token,
            "stops": stops_data,
            "total_days": (trip.end_date - trip.start_date).days + 1 if trip.start_date and trip.end_date else 0,
            "total_cities": len(stops_data),
        }
        return {"success": True, "data": trip_data, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_TRIP_FAILED", "message": str(e)}}

@router.patch("/{trip_id}")
def update_trip(trip_id: int, request: TripUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trip_data = request.model_dump(exclude_unset=True, exclude_none=True)
        updated_trip = trip_service.update_trip(db, trip_id, user.id, trip_data)
        return {"success": True, "data": {"id": updated_trip.id, "name": updated_trip.name}, "error": None}
    except ValueError as e:
        return {"success": False, "data": None, "error": {"code": "UPDATE_TRIP_FAILED", "message": str(e)}}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "UPDATE_TRIP_ERROR", "message": str(e)}}

@router.delete("/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        success = trip_service.delete_trip(db, trip_id, user.id)
        if not success:
            return {"success": False, "data": None, "error": {"code": "DELETE_TRIP_FAILED", "message": "Trip not found or unauthorized"}}
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "DELETE_TRIP_ERROR", "message": str(e)}}

@router.post("/{trip_id}/stops")
def add_stop(trip_id: int, request: TripStopCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        stop = trip_service.add_stop(
            db, trip_id, user.id, request.destination_id,
            start_date=request.start_date, end_date=request.end_date, notes=request.notes
        )
        return {"success": True, "data": {
            "id": stop.id,
            "destination_id": stop.destination_id,
            "city": stop.destination.city if stop.destination else "",
            "stop_order": stop.stop_order,
        }, "error": None}
    except ValueError as e:
        return {"success": False, "data": None, "error": {"code": "ADD_STOP_FAILED", "message": str(e)}}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "ADD_STOP_ERROR", "message": str(e)}}

@router.delete("/{trip_id}/stops/{stop_id}")
def remove_stop(trip_id: int, stop_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        success = trip_service.remove_stop(db, trip_id, stop_id, user.id)
        if not success:
            return {"success": False, "data": None, "error": {"code": "REMOVE_STOP_FAILED", "message": "Stop not found or unauthorized"}}
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "REMOVE_STOP_ERROR", "message": str(e)}}

@router.patch("/{trip_id}/stops/reorder")
def reorder_stops(trip_id: int, request: ReorderStopsRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        success = trip_service.reorder_stops(db, trip_id, user.id, request.stop_ids)
        if not success:
            return {"success": False, "data": None, "error": {"code": "REORDER_FAILED", "message": "Trip not found or unauthorized"}}
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "REORDER_ERROR", "message": str(e)}}
