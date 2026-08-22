from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_required
from app.services import share_service, trip_service
from app.database.models import User

router = APIRouter(prefix="/api", tags=["public"])

@router.post("/trips/{trip_id}/share")
def enable_sharing(trip_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trip = trip_service.get_trip(db, trip_id)
        if not trip or trip.user_id != user.id:
            return {"success": False, "data": None, "error": {"code": "UNAUTHORIZED", "message": "Trip not found or unauthorized"}}
        share_token = share_service.enable_sharing(db, trip_id)
        return {"success": True, "data": {"share_token": share_token}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "ENABLE_SHARE_FAILED", "message": str(e)}}

@router.delete("/trips/{trip_id}/share")
def disable_sharing(trip_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trip = trip_service.get_trip(db, trip_id)
        if not trip or trip.user_id != user.id:
            return {"success": False, "data": None, "error": {"code": "UNAUTHORIZED", "message": "Trip not found or unauthorized"}}
        share_service.disable_sharing(db, trip_id)
        return {"success": True, "data": None, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "DISABLE_SHARE_FAILED", "message": str(e)}}

@router.post("/share/{share_token}/copy")
def copy_trip(share_token: str, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        new_trip = share_service.copy_trip(db, share_token, user.id)
        return {"success": True, "data": {"trip_id": new_trip.id}, "error": None}
    except ValueError as e:
        return {"success": False, "data": None, "error": {"code": "COPY_TRIP_FAILED", "message": str(e)}}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "COPY_TRIP_ERROR", "message": str(e)}}
