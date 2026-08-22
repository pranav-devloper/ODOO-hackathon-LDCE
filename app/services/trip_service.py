from datetime import datetime, date
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import Trip, TripStop, Destination

def create_trip(db: Session, user_id: int, trip_data: Dict[str, Any]) -> Trip:
    destinations = trip_data.pop('destinations', None)
    trip = Trip(user_id=user_id, **trip_data)
    db.add(trip)
    db.commit()
    db.refresh(trip)
    
    if destinations:
        for idx, dest_id in enumerate(destinations):
            if dest_id:  # skip empty
                stop = TripStop(
                    trip_id=trip.id,
                    destination_id=int(dest_id),
                    stop_order=idx + 1
                )
                db.add(stop)
        db.commit()
    
    return trip

def get_user_trips(db: Session, user_id: int, filter_type: Optional[str] = None) -> List[Trip]:
    query = db.query(Trip).filter(Trip.user_id == user_id)
    today = date.today()
    
    if filter_type == 'upcoming':
        query = query.filter(Trip.start_date > today)
    elif filter_type == 'completed':
        query = query.filter(Trip.end_date < today)
    elif filter_type == 'draft':
        pass # Draft filter not explicitly defined in requirements
    elif filter_type == 'public':
        query = query.filter(Trip.is_public == True)
        
    return query.all()

def get_trip(db: Session, trip_id: int) -> Optional[Trip]:
    return db.query(Trip).filter(Trip.id == trip_id).first()

def update_trip(db: Session, trip_id: int, user_id: int, trip_data: Dict[str, Any]) -> Optional[Trip]:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        raise ValueError("Trip not found or unauthorized")
        
    for key, value in trip_data.items():
        if hasattr(trip, key):
            setattr(trip, key, value)
            
    db.commit()
    db.refresh(trip)
    return trip

def delete_trip(db: Session, trip_id: int, user_id: int) -> bool:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        return False
        
    db.delete(trip)
    db.commit()
    return True

def add_stop(db: Session, trip_id: int, user_id: int, destination_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None, notes: Optional[str] = None) -> TripStop:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        raise ValueError("Trip not found or unauthorized")
        
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise ValueError("Destination not found")
        
    max_order = db.query(func.max(TripStop.stop_order)).filter(TripStop.trip_id == trip_id).scalar()
    next_order = 1 if max_order is None else max_order + 1
    
    stop = TripStop(
        trip_id=trip_id,
        destination_id=destination_id,
        start_date=start_date,
        end_date=end_date,
        stop_order=next_order,
        notes=notes
    )
    
    db.add(stop)
    db.commit()
    db.refresh(stop)
    return stop

def remove_stop(db: Session, trip_id: int, stop_id: int, user_id: int) -> bool:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        return False
        
    stop = db.query(TripStop).filter(TripStop.id == stop_id, TripStop.trip_id == trip_id).first()
    if not stop:
        return False
        
    db.delete(stop)
    
    # Recalculate stop orders
    remaining_stops = db.query(TripStop).filter(TripStop.trip_id == trip_id).order_by(TripStop.stop_order).all()
    for idx, s in enumerate(remaining_stops):
        s.stop_order = idx + 1
        
    db.commit()
    return True

def reorder_stops(db: Session, trip_id: int, user_id: int, stop_ids: List[int]) -> bool:
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        return False
        
    stops = db.query(TripStop).filter(TripStop.trip_id == trip_id).all()
    stop_map = {s.id: s for s in stops}
    
    for idx, s_id in enumerate(stop_ids):
        if s_id in stop_map:
            stop_map[s_id].stop_order = idx + 1
            
    db.commit()
    return True

def get_trip_stops(db: Session, trip_id: int) -> List[TripStop]:
    return db.query(TripStop).filter(TripStop.trip_id == trip_id).order_by(TripStop.stop_order).all()
