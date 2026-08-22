import uuid
from typing import Optional
from sqlalchemy.orm import Session
from app.database.models import Trip, TripStop, ItineraryActivity, BudgetExpense
from app.core.security import generate_share_token

def enable_sharing(db: Session, trip_id: int, user_id: int) -> str:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        raise ValueError("Trip not found or unauthorized")
        
    token = generate_share_token()
    trip.is_public = True
    trip.share_token = token
    db.commit()
    return token

def disable_sharing(db: Session, trip_id: int, user_id: int) -> bool:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        return False
        
    trip.is_public = False
    trip.share_token = None
    db.commit()
    return True

def get_shared_trip(db: Session, share_token: str) -> Optional[Trip]:
    return db.query(Trip).filter(Trip.share_token == share_token, Trip.is_public == True).first()

def copy_trip(db: Session, share_token: str, user_id: int) -> Trip:
    orig = get_shared_trip(db, share_token)
    if not orig:
        raise ValueError("Shared trip not found")
        
    new_trip = Trip(
        user_id=user_id,
        name=f"Copy of {orig.name}",
        description=orig.description,
        start_date=orig.start_date,
        end_date=orig.end_date,
        cover_image=orig.cover_image,
        estimated_budget=orig.estimated_budget,
        is_public=False,
        share_token=generate_share_token()
    )
    db.add(new_trip)
    db.flush() # To get the new_trip.id
    
    for orig_stop in orig.trip_stops:
        new_stop = TripStop(
            trip_id=new_trip.id,
            destination_id=orig_stop.destination_id,
            start_date=orig_stop.start_date,
            end_date=orig_stop.end_date,
            stop_order=orig_stop.stop_order,
            notes=orig_stop.notes
        )
        db.add(new_stop)
        db.flush() # To get the new_stop.id
        
        for orig_act in orig_stop.itinerary_activities:
            new_act = ItineraryActivity(
                trip_stop_id=new_stop.id,
                activity_id=orig_act.activity_id,
                date=orig_act.date,
                start_time=orig_act.start_time,
                end_time=orig_act.end_time,
                custom_cost=orig_act.custom_cost,
                activity_order=orig_act.activity_order,
                notes=orig_act.notes
            )
            db.add(new_act)
            
    for orig_exp in orig.budget_expenses:
        new_exp = BudgetExpense(
            trip_id=new_trip.id,
            category=orig_exp.category,
            description=orig_exp.description,
            amount=orig_exp.amount,
            date=orig_exp.date,
            notes=orig_exp.notes
        )
        db.add(new_exp)
        
    db.commit()
    db.refresh(new_trip)
    return new_trip
