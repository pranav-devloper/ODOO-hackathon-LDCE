import random
from datetime import date, timedelta, time
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.database.models import User, Trip, Destination, TripStop, Activity, ItineraryActivity, BudgetExpense, Base
import string

def generate_share_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def add_more_demo_trips():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == "demo@globetrotter.local").first()
        if not user:
            print("Demo user not found.")
            return

        destinations = db.query(Destination).all()
        if not destinations:
            print("No destinations found.")
            return

        trip_templates = [
            {"name": "Asian Adventure", "desc": "Exploring the heart of Asia.", "cities": ["Tokyo", "Kyoto", "Bangkok", "Bali"]},
            {"name": "North American Roadtrip", "desc": "Coast to coast.", "cities": ["New York", "Los Angeles"]},
            {"name": "South American Wonders", "desc": "Nature and culture.", "cities": ["Rio de Janeiro", "Buenos Aires"]},
            {"name": "Middle East Explorer", "desc": "History and modernity.", "cities": ["Dubai", "Istanbul"]},
            {"name": "Island Hopping", "desc": "Beaches and sun.", "cities": ["Bali", "Maldives"]},
            {"name": "European Summer", "desc": "Classic Euro trip.", "cities": ["Rome", "Paris", "London", "Amsterdam"]},
            {"name": "Winter Getaway", "desc": "Snowy mountains.", "cities": ["Kyoto", "London"]},
            {"name": "Desert Safari", "desc": "Dunes and camels.", "cities": ["Dubai", "Cairo"]},
            {"name": "Tropical Paradise", "desc": "Relaxation.", "cities": ["Maldives", "Bali"]},
            {"name": "Historical Journey", "desc": "Ancient ruins.", "cities": ["Rome", "Cairo", "Istanbul"]},
            {"name": "Foodie Tour", "desc": "Tasting the world.", "cities": ["Tokyo", "Paris", "Bangkok"]},
            {"name": "City Lights", "desc": "Metropolitan vibes.", "cities": ["New York", "Tokyo", "Dubai"]},
            {"name": "Romantic Escape", "desc": "Just for two.", "cities": ["Paris", "Venice", "Maldives"]},
            {"name": "Backpacking Asia", "desc": "Budget friendly.", "cities": ["Bangkok", "Bali"]},
            {"name": "Art & Culture", "desc": "Museums and galleries.", "cities": ["London", "Paris", "Rome", "Florence"]}
        ]

        # Generate 14 additional trips
        num_new_trips = 14
        trips_to_create = trip_templates[:num_new_trips]

        print(f"Creating {len(trips_to_create)} additional trips...")

        for t_info in trips_to_create:
            start = date.today() + timedelta(days=random.randint(-100, 100))
            days = random.randint(5, 20)
            
            trip = Trip(
                user_id=user.id,
                name=t_info["name"],
                description=t_info["desc"],
                start_date=start,
                end_date=start + timedelta(days=days),
                estimated_budget=random.randint(20000, 150000),
                is_public=random.choice([True, False]),
                share_token=generate_share_token()
            )
            db.add(trip)
            db.commit()
            db.refresh(trip)

            # Pick 2-4 destinations based on the template cities or random
            trip_dest_names = t_info.get("cities", [])
            trip_dests = []
            for name in trip_dest_names:
                d = next((d for d in destinations if d.city == name), None)
                if d:
                    trip_dests.append(d)
            
            if len(trip_dests) < 2:
                # fill with random
                extra = random.sample(destinations, min(3, len(destinations)))
                for e in extra:
                    if e not in trip_dests:
                        trip_dests.append(e)

            # Add stops
            current_date = start
            for idx, dest in enumerate(trip_dests):
                stop_days = max(1, days // len(trip_dests))
                end_date = current_date + timedelta(days=stop_days)
                if idx == len(trip_dests) - 1:
                    end_date = start + timedelta(days=days) # Adjust last stop

                stop = TripStop(
                    trip_id=trip.id,
                    destination_id=dest.id,
                    start_date=current_date,
                    end_date=end_date,
                    stop_order=idx
                )
                db.add(stop)
                db.commit()
                db.refresh(stop)

                # Add some activities
                acts = db.query(Activity).filter(Activity.destination_id == dest.id).all()
                if acts:
                    sample_acts = random.sample(acts, min(3, len(acts)))
                    for a_idx, act in enumerate(sample_acts):
                        ia = ItineraryActivity(
                            trip_stop_id=stop.id,
                            activity_id=act.id,
                            date=current_date + timedelta(days=random.randint(0, max(0, stop_days-1))),
                            start_time=time(random.randint(9, 16), 0),
                            end_time=time(random.randint(17, 20), 0),
                            activity_order=a_idx
                        )
                        db.add(ia)
                
                # Add an expense
                db.add(BudgetExpense(
                    trip_id=trip.id, category="accommodation", description=f"Hotel in {dest.city}", 
                    amount=random.randint(2000, 10000), date=current_date
                ))
                current_date = end_date

            db.commit()
            print(f"Created trip: {trip.name}")

    finally:
        db.close()

if __name__ == "__main__":
    add_more_demo_trips()
