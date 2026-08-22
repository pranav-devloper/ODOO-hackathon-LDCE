from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_admin_user
from app.database.models import User, Trip, Destination, Activity

router = APIRouter(prefix="/api/admin", tags=["admin"])

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.core.dependencies import get_db, get_admin_user
from app.database.models import User, Trip, Destination, Activity, TripStop, SavedDestination, ItineraryActivity
import datetime

router = APIRouter(prefix="/api/admin", tags=["admin"])

# --- USERS ---
@router.get("/users")
def get_users(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    users = db.query(User).order_by(User.id.desc()).all()
    result = []
    for u in users:
        trips_count = db.query(Trip).filter(Trip.user_id == u.id).count()
        result.append({
            "id": u.id, "name": u.name, "email": u.email, 
            "is_active": u.is_active, "is_admin": u.is_admin,
            "created_at": u.created_at.strftime("%Y-%m-%d") if u.created_at else None,
            "trips_count": trips_count
        })
    return {"success": True, "data": result}

@router.put("/users/{user_id}/status")
def update_user_status(user_id: int, is_active: bool = Body(...), db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id and not is_active:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")
    user.is_active = is_active
    db.commit()
    return {"success": True, "message": "User status updated"}

@router.put("/users/{user_id}/role")
def update_user_role(user_id: int, is_admin: bool = Body(...), db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id and not is_admin:
        raise HTTPException(status_code=400, detail="Cannot remove your own admin privileges")
    user.is_admin = is_admin
    db.commit()
    return {"success": True, "message": "User role updated"}

# --- DESTINATIONS ---
@router.get("/destinations")
def get_destinations(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    dests = db.query(Destination).order_by(Destination.id.desc()).all()
    result = []
    for d in dests:
        usage = db.query(TripStop).filter(TripStop.destination_id == d.id).count()
        saved = db.query(SavedDestination).filter(SavedDestination.destination_id == d.id).count()
        result.append({
            "id": d.id, "city": d.city, "country": d.country, "region": d.region,
            "popularity": d.popularity, "usage_count": usage, "saved_count": saved
        })
    return {"success": True, "data": result}

@router.post("/destinations")
def create_destination(data: dict = Body(...), db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    dest = Destination(
        city=data.get("city"), country=data.get("country"), region=data.get("region"),
        description=data.get("description"), cost_index=data.get("cost_index", 3), popularity=data.get("popularity", 50)
    )
    db.add(dest)
    db.commit()
    return {"success": True, "message": "Destination created"}

@router.put("/destinations/{dest_id}")
def update_destination(dest_id: int, data: dict = Body(...), db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    dest = db.query(Destination).filter(Destination.id == dest_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    if "city" in data: dest.city = data["city"]
    if "country" in data: dest.country = data["country"]
    if "region" in data: dest.region = data["region"]
    
    db.commit()
    return {"success": True, "message": "Destination updated"}

@router.delete("/destinations/{dest_id}")
def delete_destination(dest_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    dest = db.query(Destination).filter(Destination.id == dest_id).first()
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Check references
    usage = db.query(TripStop).filter(TripStop.destination_id == dest_id).count()
    saved = db.query(SavedDestination).filter(SavedDestination.destination_id == dest_id).count()
    activities = db.query(Activity).filter(Activity.destination_id == dest_id).count()
    
    if usage > 0 or saved > 0 or activities > 0:
        raise HTTPException(status_code=400, detail=f"Cannot delete destination. It is referenced by {usage} trip stops, {saved} saves, and {activities} activities.")
        
    db.delete(dest)
    db.commit()
    return {"success": True, "message": "Destination deleted"}

# --- ACTIVITIES ---
@router.get("/activities")
def get_activities(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    acts = db.query(Activity).join(Destination).all()
    result = []
    for a in acts:
        usage = db.query(ItineraryActivity).filter(ItineraryActivity.activity_id == a.id).count()
        result.append({
            "id": a.id, "name": a.name, "category": a.category, "destination": a.destination.city,
            "rating": a.rating, "usage_count": usage
        })
    return {"success": True, "data": result}

@router.post("/activities")
def create_activity(data: dict = Body(...), db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    act = Activity(
        name=data.get("name"), destination_id=data.get("destination_id"),
        category=data.get("category"), description=data.get("description"),
        duration_hours=data.get("duration_hours", 2.0), estimated_cost=data.get("estimated_cost", 0.0)
    )
    db.add(act)
    db.commit()
    return {"success": True, "message": "Activity created"}

@router.put("/activities/{act_id}")
def update_activity(act_id: int, data: dict = Body(...), db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    act = db.query(Activity).filter(Activity.id == act_id).first()
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    if "name" in data: act.name = data["name"]
    if "category" in data: act.category = data["category"]
    
    db.commit()
    return {"success": True, "message": "Activity updated"}

@router.delete("/activities/{act_id}")
def delete_activity(act_id: int, db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    act = db.query(Activity).filter(Activity.id == act_id).first()
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    usage = db.query(ItineraryActivity).filter(ItineraryActivity.activity_id == act_id).count()
    if usage > 0:
        raise HTTPException(status_code=400, detail=f"Cannot delete activity. It is used in {usage} itineraries.")
        
    db.delete(act)
    db.commit()
    return {"success": True, "message": "Activity deleted"}

# --- TRIPS ---
@router.get("/trips")
def get_trips(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    trips = db.query(Trip).join(User).order_by(Trip.created_at.desc()).all()
    result = []
    for t in trips:
        city_count = db.query(TripStop).filter(TripStop.trip_id == t.id).count()
        result.append({
            "id": t.id, "name": t.name, "owner": t.user.name,
            "start_date": t.start_date.strftime("%Y-%m-%d"),
            "end_date": t.end_date.strftime("%Y-%m-%d"),
            "is_public": t.is_public, "city_count": city_count,
            "created_at": t.created_at.strftime("%Y-%m-%d") if t.created_at else None
        })
    return {"success": True, "data": result}
