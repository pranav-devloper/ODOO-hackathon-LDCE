from datetime import date, time
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.models import Trip, TripStop, ItineraryActivity, Activity

def get_trip_itinerary(db: Session, trip_id: int) -> Dict[str, Any]:
    stops = db.query(TripStop).filter(TripStop.trip_id == trip_id).order_by(TripStop.stop_order).all()
    
    itinerary = {}
    day_costs = {}
    day_number = 1
    
    for stop in stops:
        activities = db.query(ItineraryActivity).filter(ItineraryActivity.trip_stop_id == stop.id).order_by(ItineraryActivity.date, ItineraryActivity.activity_order).all()
        
        for act in activities:
            d = act.date
            if not d:
                continue
                
            d_str = d.isoformat()
            if d_str not in itinerary:
                itinerary[d_str] = {
                    "day_number": day_number,
                    "city": stop.destination.city if stop.destination else "Unknown",
                    "activities": []
                }
                day_costs[d_str] = 0
                day_number += 1
                
            cost = act.custom_cost if act.custom_cost is not None else (act.activity.estimated_cost if act.activity and act.activity.estimated_cost else 0.0)
            
            itinerary[d_str]["activities"].append({
                "id": act.id,
                "activity_id": act.activity_id,
                "name": act.activity.name if act.activity else "Unknown",
                "start_time": act.start_time.isoformat() if act.start_time else None,
                "end_time": act.end_time.isoformat() if act.end_time else None,
                "cost": float(cost),
                "notes": act.notes
            })
            day_costs[d_str] += float(cost)
            
    return {
        "itinerary": itinerary,
        "day_costs": day_costs
    }

def add_itinerary_activity(db: Session, trip_stop_id: int, activity_id: int, date_val: date, start_time: Optional[time] = None, end_time: Optional[time] = None, custom_cost: Optional[float] = None, notes: Optional[str] = None) -> ItineraryActivity:
    max_order = db.query(func.max(ItineraryActivity.activity_order)).filter(ItineraryActivity.trip_stop_id == trip_stop_id, ItineraryActivity.date == date_val).scalar()
    next_order = 1 if max_order is None else max_order + 1
    
    it_act = ItineraryActivity(
        trip_stop_id=trip_stop_id,
        activity_id=activity_id,
        date=date_val,
        start_time=start_time,
        end_time=end_time,
        custom_cost=custom_cost,
        activity_order=next_order,
        notes=notes
    )
    
    db.add(it_act)
    db.commit()
    db.refresh(it_act)
    return it_act

def remove_itinerary_activity(db: Session, activity_id: int) -> bool:
    act = db.query(ItineraryActivity).filter(ItineraryActivity.id == activity_id).first()
    if not act:
        return False
        
    ts_id = act.trip_stop_id
    d = act.date
    db.delete(act)
    
    remaining = db.query(ItineraryActivity).filter(ItineraryActivity.trip_stop_id == ts_id, ItineraryActivity.date == d).order_by(ItineraryActivity.activity_order).all()
    for idx, a in enumerate(remaining):
        a.activity_order = idx + 1
        
    db.commit()
    return True

def reorder_itinerary_activities(db: Session, trip_id: int, activity_ids: List[int]) -> bool:
    # Find all activities from the list
    activities = db.query(ItineraryActivity).filter(ItineraryActivity.id.in_(activity_ids)).all()
    act_map = {a.id: a for a in activities}
    
    for idx, a_id in enumerate(activity_ids):
        if a_id in act_map:
            act_map[a_id].activity_order = idx + 1
            
    db.commit()
    return True

def get_day_activities(db: Session, trip_stop_id: int, date_val: date) -> List[ItineraryActivity]:
    return db.query(ItineraryActivity).filter(ItineraryActivity.trip_stop_id == trip_stop_id, ItineraryActivity.date == date_val).order_by(ItineraryActivity.activity_order).all()
