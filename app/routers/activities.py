from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.core.dependencies import get_db
from app.database.models import Activity, Destination

router = APIRouter(prefix="/api/activities", tags=["activities"])

def activity_to_dict(act):
    """Serialize Activity ORM object."""
    return {
        "id": act.id,
        "destination_id": act.destination_id,
        "name": act.name,
        "description": act.description,
        "category": act.category,
        "duration_hours": act.duration_hours,
        "estimated_cost": act.estimated_cost,
        "image": act.image,
        "rating": act.rating,
        "destination_city": act.destination.city if act.destination else None,
        "destination_country": act.destination.country if act.destination else None,
    }

@router.get("/")
def list_activities(
    destination_id: Optional[int] = None,
    category: Optional[str] = None,
    min_cost: Optional[float] = None,
    max_cost: Optional[float] = None,
    min_rating: Optional[float] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Activity)
        if destination_id:
            query = query.filter(Activity.destination_id == destination_id)
        if category:
            query = query.filter(Activity.category == category)
        if min_cost is not None:
            query = query.filter(Activity.estimated_cost >= min_cost)
        if max_cost is not None:
            query = query.filter(Activity.estimated_cost <= max_cost)
        if min_rating is not None:
            query = query.filter(Activity.rating >= min_rating)
        if search:
            s = f"%{search}%"
            query = query.filter(or_(Activity.name.ilike(s), Activity.description.ilike(s)))

        total = query.count()

        if sort == "cost_asc":
            query = query.order_by(Activity.estimated_cost.asc())
        elif sort == "cost_desc":
            query = query.order_by(Activity.estimated_cost.desc())
        elif sort == "rating":
            query = query.order_by(Activity.rating.desc())
        else:
            query = query.order_by(Activity.rating.desc())

        activities = query.offset(offset).limit(limit).all()
        data = [activity_to_dict(a) for a in activities]

        # Get categories for filter
        categories = db.query(Activity.category).distinct().all()

        return {
            "success": True,
            "data": data,
            "total": total,
            "categories": [c[0] for c in categories],
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_ACTIVITIES_FAILED", "message": str(e)}}

@router.get("/{activity_id}")
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    try:
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return {"success": False, "data": None, "error": {"code": "NOT_FOUND", "message": "Activity not found"}}
        return {"success": True, "data": activity_to_dict(activity), "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_ACTIVITY_FAILED", "message": str(e)}}
