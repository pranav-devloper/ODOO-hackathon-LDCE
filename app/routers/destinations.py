from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.core.dependencies import get_db, get_current_user, get_current_user_required
from app.database.models import Destination, SavedDestination, User

router = APIRouter(prefix="/api/destinations", tags=["destinations"])

def destination_to_dict(dest, user_id=None, db=None):
    """Serialize a Destination ORM object to dict."""
    is_saved = False
    if user_id and db:
        saved = db.query(SavedDestination).filter_by(user_id=user_id, destination_id=dest.id).first()
        is_saved = saved is not None
    return {
        "id": dest.id,
        "city": dest.city,
        "country": dest.country,
        "region": dest.region,
        "description": dest.description,
        "image": dest.image,
        "cost_index": dest.cost_index,
        "popularity": dest.popularity,
        "latitude": dest.latitude,
        "longitude": dest.longitude,
        "is_saved": is_saved,
    }

@router.get("/")
def list_destinations(
    q: Optional[str] = None,
    country: Optional[str] = None,
    region: Optional[str] = None,
    cost_index: Optional[int] = None,
    sort: Optional[str] = "popularity",
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    try:
        query = db.query(Destination)
        if q:
            search = f"%{q}%"
            query = query.filter(or_(
                Destination.city.ilike(search),
                Destination.country.ilike(search),
                Destination.description.ilike(search)
            ))
        if country:
            query = query.filter(Destination.country == country)
        if region:
            query = query.filter(Destination.region == region)
        if cost_index:
            query = query.filter(Destination.cost_index == cost_index)

        total = query.count()

        if sort == "popularity":
            query = query.order_by(Destination.popularity.desc())
        elif sort == "cost_index":
            query = query.order_by(Destination.cost_index.asc())
        elif sort == "city":
            query = query.order_by(Destination.city.asc())
        else:
            query = query.order_by(Destination.popularity.desc())

        destinations = query.offset(offset).limit(limit).all()
        user_id = user.id if user else None
        data = [destination_to_dict(d, user_id, db) for d in destinations]

        # Get unique countries and regions for filters
        countries = db.query(Destination.country).distinct().all()
        regions = db.query(Destination.region).filter(Destination.region.isnot(None)).distinct().all()

        return {
            "success": True,
            "data": data,
            "total": total,
            "countries": [c[0] for c in countries],
            "regions": [r[0] for r in regions],
            "error": None
        }
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_DESTINATIONS_FAILED", "message": str(e)}}

@router.get("/{destination_id}")
def get_destination(destination_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        dest = db.query(Destination).filter(Destination.id == destination_id).first()
        if not dest:
            return {"success": False, "data": None, "error": {"code": "NOT_FOUND", "message": "Destination not found"}}
        user_id = user.id if user else None
        return {"success": True, "data": destination_to_dict(dest, user_id, db), "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "FETCH_DESTINATION_FAILED", "message": str(e)}}

@router.post("/{destination_id}/save")
def save_destination(destination_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        dest = db.query(Destination).filter(Destination.id == destination_id).first()
        if not dest:
            return {"success": False, "data": None, "error": {"code": "NOT_FOUND", "message": "Destination not found"}}
        existing = db.query(SavedDestination).filter_by(user_id=user.id, destination_id=destination_id).first()
        if not existing:
            saved = SavedDestination(user_id=user.id, destination_id=destination_id)
            db.add(saved)
            db.commit()
        return {"success": True, "data": {"message": "Destination saved"}, "error": None}
    except Exception as e:
        db.rollback()
        return {"success": False, "data": None, "error": {"code": "SAVE_FAILED", "message": str(e)}}

@router.delete("/{destination_id}/save")
def unsave_destination(destination_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user_required)):
    try:
        existing = db.query(SavedDestination).filter_by(user_id=user.id, destination_id=destination_id).first()
        if existing:
            db.delete(existing)
            db.commit()
        return {"success": True, "data": {"message": "Destination unsaved"}, "error": None}
    except Exception as e:
        db.rollback()
        return {"success": False, "data": None, "error": {"code": "UNSAVE_FAILED", "message": str(e)}}
