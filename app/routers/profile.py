from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user_required
from app.schemas.user import UserUpdate
from app.services import auth_service
from app.database.models import User, Trip, SavedDestination

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/")
def get_profile(db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        trips_count = db.query(Trip).filter(Trip.user_id == user.id).count()
        saved_count = db.query(SavedDestination).filter(SavedDestination.user_id == user.id).count()
        stats = {"trips_planned": trips_count, "destinations_saved": saved_count}
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "language": user.language,
            "profile_image": user.profile_image
        }
        return {"success": True, "data": {"user": user_data, "stats": stats}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_PROFILE_FAILED", "message": str(e)}}

@router.patch("/")
def update_profile(request: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        update_data = request.model_dump(exclude_unset=True)
        updated_user = auth_service.update_user(db, user.id, **update_data)
        user_data = {
            "id": updated_user.id,
            "name": updated_user.name,
            "email": updated_user.email,
            "language": updated_user.language,
            "profile_image": updated_user.profile_image
        }
        return {"success": True, "data": {"user": user_data}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "UPDATE_PROFILE_FAILED", "message": str(e)}}
