"""
GlobeTrotter Database Seed Script
Run: python -m app.database.seed
Creates demo data: destinations, activities, demo user, sample trip
"""
from datetime import date, time, timedelta
from app.database.database import SessionLocal, engine, Base
from app.database.models import (
    User, Trip, Destination, TripStop, Activity,
    ItineraryActivity, BudgetExpense, SavedDestination
)
from app.core.security import get_password_hash, generate_share_token

def seed_destinations(db):
    """Seed 15 destinations with realistic data."""
    destinations = [
        Destination(
            city="Tokyo", country="Japan", region="East Asia",
            description="A mesmerizing blend of ultramodern and traditional, from neon-lit skyscrapers to historic temples. Tokyo offers an unparalleled cultural experience.",
            image="/static/images/destinations/tokyo.jpg",
            cost_index=4, popularity=92, latitude=35.6762, longitude=139.6503
        ),
        Destination(
            city="Kyoto", country="Japan", region="East Asia",
            description="The cultural heart of Japan, home to countless temples, shrines, and traditional gardens. A city where ancient traditions thrive.",
            image="/static/images/destinations/kyoto.jpg",
            cost_index=3, popularity=88, latitude=35.0116, longitude=135.7681
        ),
        Destination(
            city="Osaka", country="Japan", region="East Asia",
            description="Japan's kitchen and entertainment capital. Known for street food, vibrant nightlife, and the iconic Osaka Castle.",
            image="/static/images/destinations/osaka.jpg",
            cost_index=3, popularity=80, latitude=34.6937, longitude=135.5023
        ),
        Destination(
            city="Paris", country="France", region="Europe",
            description="The City of Light captivates with its iconic landmarks, world-class cuisine, and romantic atmosphere along the Seine.",
            image="/static/images/destinations/paris.jpg",
            cost_index=4, popularity=95, latitude=48.8566, longitude=2.3522
        ),
        Destination(
            city="Rome", country="Italy", region="Europe",
            description="The Eternal City where ancient ruins, Renaissance art, and vibrant Italian culture create an unforgettable experience.",
            image="/static/images/destinations/rome.jpg",
            cost_index=3, popularity=90, latitude=41.9028, longitude=12.4964
        ),
        Destination(
            city="Barcelona", country="Spain", region="Europe",
            description="A vibrant Mediterranean city famous for Gaudi's architecture, beautiful beaches, and incredible food scene.",
            image="/static/images/destinations/barcelona.jpg",
            cost_index=3, popularity=88, latitude=41.3874, longitude=2.1686
        ),
        Destination(
            city="London", country="United Kingdom", region="Europe",
            description="A global city of culture, history, and innovation. From Buckingham Palace to Camden Market, London never disappoints.",
            image="/static/images/destinations/london.jpg",
            cost_index=5, popularity=93, latitude=51.5074, longitude=-0.1278
        ),
        Destination(
            city="Dubai", country="UAE", region="Middle East",
            description="A futuristic city of superlatives — the tallest buildings, largest malls, and most luxurious experiences in the desert.",
            image="/static/images/destinations/dubai.jpg",
            cost_index=5, popularity=85, latitude=25.2048, longitude=55.2708
        ),
        Destination(
            city="New York", country="USA", region="North America",
            description="The city that never sleeps. From Times Square to Central Park, NYC is the ultimate urban adventure.",
            image="/static/images/destinations/newyork.jpg",
            cost_index=5, popularity=94, latitude=40.7128, longitude=-74.0060
        ),
        Destination(
            city="Bali", country="Indonesia", region="Southeast Asia",
            description="An island paradise of lush rice terraces, ancient temples, stunning beaches, and spiritual retreats.",
            image="/static/images/destinations/bali.jpg",
            cost_index=2, popularity=89, latitude=-8.3405, longitude=115.0920
        ),
        Destination(
            city="Goa", country="India", region="South Asia",
            description="India's beach paradise with golden shores, Portuguese heritage, vibrant nightlife, and laid-back charm.",
            image="/static/images/destinations/goa.jpg",
            cost_index=1, popularity=78, latitude=15.2993, longitude=74.1240
        ),
        Destination(
            city="Manali", country="India", region="South Asia",
            description="A Himalayan jewel nestled in the mountains, perfect for adventure seekers and nature lovers.",
            image="/static/images/destinations/manali.jpg",
            cost_index=1, popularity=72, latitude=32.2396, longitude=77.1887
        ),
        Destination(
            city="Leh", country="India", region="South Asia",
            description="The land of high passes. Dramatic landscapes, Buddhist monasteries, and some of the most stunning roads on Earth.",
            image="/static/images/destinations/leh.jpg",
            cost_index=2, popularity=75, latitude=34.1526, longitude=77.5771
        ),
        Destination(
            city="Singapore", country="Singapore", region="Southeast Asia",
            description="A gleaming city-state where futuristic gardens, hawker food, and multicultural heritage create a unique destination.",
            image="/static/images/destinations/singapore.jpg",
            cost_index=4, popularity=86, latitude=1.3521, longitude=103.8198
        ),
        Destination(
            city="Istanbul", country="Turkey", region="Middle East",
            description="Where East meets West. A city spanning two continents with bazaars, mosques, and millennia of history.",
            image="/static/images/destinations/istanbul.jpg",
            cost_index=2, popularity=82, latitude=41.0082, longitude=28.9784
        ),
    ]
    for d in destinations:
        existing = db.query(Destination).filter(Destination.city == d.city).first()
        if not existing:
            db.add(d)
    db.commit()
    print(f"  ✓ Seeded {len(destinations)} destinations")
    return db.query(Destination).all()


def seed_activities(db, destinations):
    """Seed activities for each destination."""
    activities_data = {
        "Tokyo": [
            ("Meiji Shrine Visit", "Sightseeing", "Explore the serene Meiji Shrine surrounded by ancient forest in the heart of Tokyo.", 2.0, 0, 4.7),
            ("Tsukiji Outer Market Food Tour", "Food", "Sample the freshest sushi, wagyu beef, and Japanese street food at the famous market.", 3.0, 2500, 4.8),
            ("Shibuya Crossing Experience", "Sightseeing", "Stand at the world's busiest intersection and experience the energy of Tokyo.", 1.0, 0, 4.5),
            ("Akihabara Electronics District", "Shopping", "Explore the electric town of anime, manga, and cutting-edge electronics.", 2.5, 1000, 4.3),
            ("TeamLab Borderless", "Culture", "Immerse yourself in a world of interactive digital art installations.", 2.0, 3200, 4.9),
            ("Ramen Alley Exploration", "Food", "Discover Tokyo's best ramen shops hidden in narrow alleyways.", 1.5, 1200, 4.6),
        ],
        "Kyoto": [
            ("Fushimi Inari Shrine", "Sightseeing", "Walk through thousands of vermillion torii gates on the mountainside.", 3.0, 0, 4.9),
            ("Bamboo Grove Walk", "Sightseeing", "Stroll through the enchanting Arashiyama Bamboo Grove.", 1.5, 0, 4.7),
            ("Tea Ceremony Experience", "Culture", "Participate in a traditional Japanese tea ceremony with a tea master.", 1.5, 3000, 4.8),
            ("Geisha District Walk", "Culture", "Explore the historic Gion district and spot geisha at dusk.", 2.0, 0, 4.5),
            ("Kinkaku-ji Golden Pavilion", "Sightseeing", "Visit the stunning gold-leaf covered temple reflected in a mirror pond.", 1.5, 500, 4.8),
        ],
        "Paris": [
            ("Eiffel Tower Visit", "Sightseeing", "Ascend the iconic iron lattice tower for panoramic views of the City of Light.", 2.5, 2600, 4.8),
            ("Louvre Museum", "Culture", "Explore the world's largest art museum, home to the Mona Lisa and Venus de Milo.", 4.0, 1700, 4.9),
            ("Seine River Cruise", "Sightseeing", "Glide along the Seine and see Paris's landmarks illuminated at night.", 1.5, 1500, 4.7),
            ("Montmartre Walking Tour", "Culture", "Discover the artistic heart of Paris, from Sacré-Cœur to charming cafés.", 2.5, 0, 4.6),
            ("French Pastry Cooking Class", "Food", "Learn to make croissants and macarons from a Parisian pastry chef.", 3.0, 8500, 4.9),
            ("Palace of Versailles Day Trip", "Sightseeing", "Visit the opulent palace and its magnificent gardens outside Paris.", 5.0, 2000, 4.7),
        ],
        "Rome": [
            ("Colosseum Tour", "Sightseeing", "Step inside the ancient amphitheater where gladiators once fought.", 2.5, 1600, 4.8),
            ("Italian Food Tour", "Food", "Taste authentic Roman cuisine from pasta to gelato on a guided food walk.", 3.0, 6500, 4.9),
            ("Trevi Fountain", "Sightseeing", "Throw a coin into the most famous fountain in the world.", 0.5, 0, 4.6),
            ("Vatican Museums & Sistine Chapel", "Culture", "Marvel at Michelangelo's ceiling and centuries of papal art collections.", 3.5, 1700, 4.9),
            ("Trastevere Evening Walk", "Culture", "Wander through Rome's most charming neighborhood as the sun sets.", 2.0, 0, 4.5),
        ],
        "Barcelona": [
            ("Sagrada Familia", "Sightseeing", "Gaudi's unfinished masterpiece, a basilica unlike anything in the world.", 2.0, 2600, 4.9),
            ("La Rambla Walk", "Culture", "Stroll down Barcelona's most famous boulevard filled with street performers.", 1.5, 0, 4.3),
            ("Park Güell", "Sightseeing", "Explore Gaudi's whimsical public park with mosaic sculptures and city views.", 2.0, 1000, 4.7),
            ("Tapas Tour in Born", "Food", "Hop between traditional tapas bars in the trendy El Born neighborhood.", 3.0, 4500, 4.8),
            ("Barceloneta Beach", "Adventure", "Relax on the golden Mediterranean beach and enjoy seafood paella.", 3.0, 500, 4.4),
        ],
        "London": [
            ("Tower of London", "Sightseeing", "Explore the historic castle, home to the Crown Jewels and centuries of royal history.", 3.0, 3000, 4.7),
            ("British Museum", "Culture", "Discover world history through millions of artifacts, from the Rosetta Stone to Egyptian mummies.", 3.0, 0, 4.8),
            ("Borough Market Food Tour", "Food", "Sample artisan foods from one of London's oldest and most diverse food markets.", 2.0, 2000, 4.6),
            ("West End Theatre Show", "Culture", "Watch a world-class performance in London's legendary theatre district.", 3.0, 7000, 4.8),
            ("Hyde Park & Kensington Walk", "Sightseeing", "Stroll through London's royal parks and elegant neighborhoods.", 2.0, 0, 4.5),
        ],
        "Dubai": [
            ("Burj Khalifa Observation Deck", "Sightseeing", "See the world from the top of the tallest building on Earth.", 1.5, 3500, 4.8),
            ("Desert Safari", "Adventure", "Experience dune bashing, camel riding, and a Bedouin camp dinner under the stars.", 6.0, 5000, 4.7),
            ("Dubai Mall & Aquarium", "Shopping", "Explore the world's largest mall and its mesmerizing underwater aquarium.", 3.0, 1500, 4.5),
            ("Old Dubai Creek Abra Ride", "Culture", "Cross the historic creek on a traditional wooden boat through the old souks.", 1.0, 100, 4.4),
            ("Dubai Marina Night Walk", "Sightseeing", "Stroll along the illuminated marina surrounded by futuristic skyscrapers.", 1.5, 0, 4.3),
        ],
        "New York": [
            ("Statue of Liberty & Ellis Island", "Sightseeing", "Visit America's most iconic symbol of freedom and immigration history.", 4.0, 2400, 4.7),
            ("Central Park Walk", "Sightseeing", "Explore the 843-acre urban oasis in the heart of Manhattan.", 2.0, 0, 4.8),
            ("Broadway Show", "Culture", "Experience the magic of a Broadway musical in the Theater District.", 3.0, 12000, 4.9),
            ("Times Square", "Sightseeing", "Stand in the neon glow of the crossroads of the world.", 1.0, 0, 4.4),
            ("Brooklyn Bridge Walk", "Adventure", "Walk across the iconic bridge for stunning views of Manhattan skyline.", 1.5, 0, 4.7),
        ],
        "Bali": [
            ("Ubud Rice Terrace Trek", "Adventure", "Hike through the stunning Tegallalang rice terraces carved into the hillside.", 3.0, 500, 4.8),
            ("Uluwatu Temple Sunset", "Sightseeing", "Watch a traditional Kecak fire dance at the clifftop temple during sunset.", 2.5, 700, 4.9),
            ("Balinese Cooking Class", "Food", "Learn to cook traditional Balinese dishes at a local family compound.", 4.0, 2000, 4.7),
            ("Snorkeling in Nusa Penida", "Adventure", "Swim with manta rays and explore coral reefs off Bali's sister island.", 6.0, 3500, 4.8),
            ("Tirta Empul Water Temple", "Culture", "Participate in a traditional purification ritual at the sacred spring temple.", 2.0, 300, 4.6),
        ],
        "Goa": [
            ("Baga Beach Day", "Adventure", "Enjoy the sun, sand, and water sports at Goa's most popular beach.", 5.0, 500, 4.3),
            ("Old Goa Churches Walk", "Culture", "Explore the UNESCO World Heritage Portuguese churches and cathedrals.", 2.5, 0, 4.5),
            ("Spice Plantation Tour", "Food", "Walk through fragrant spice gardens and enjoy an authentic Goan lunch.", 3.0, 800, 4.4),
            ("Dudhsagar Falls Trek", "Adventure", "Trek through the jungle to one of India's tallest and most spectacular waterfalls.", 6.0, 1500, 4.7),
            ("Saturday Night Market", "Shopping", "Browse handicrafts, live music, and street food at Arpora's famous night bazaar.", 3.0, 500, 4.3),
        ],
        "Manali": [
            ("Solang Valley Adventure", "Adventure", "Experience paragliding, zorbing, and skiing in the stunning Himalayan valley.", 5.0, 2000, 4.6),
            ("Hadimba Temple Visit", "Culture", "Visit the ancient wooden temple nestled among towering cedar trees.", 1.5, 0, 4.5),
            ("Old Manali Walk", "Sightseeing", "Explore the charming old village with its cafés, bakeries, and mountain views.", 2.0, 0, 4.4),
            ("Jogini Waterfall Trek", "Adventure", "Hike through pine forests to a beautiful waterfall above Old Manali.", 3.0, 0, 4.5),
            ("Rohtang Pass Day Trip", "Adventure", "Drive to the high mountain pass for snow activities and breathtaking panoramas.", 6.0, 1500, 4.7),
        ],
        "Leh": [
            ("Pangong Lake Day Trip", "Sightseeing", "Visit the surreal blue lake at 14,270 feet, crossing the world's highest motorable pass.", 10.0, 3000, 4.9),
            ("Thiksey Monastery", "Culture", "Explore the magnificent 12-story monastery resembling the Potala Palace.", 2.0, 300, 4.7),
            ("Magnetic Hill", "Sightseeing", "Experience the optical illusion where vehicles appear to roll uphill on their own.", 1.0, 0, 4.2),
            ("Nubra Valley Camel Safari", "Adventure", "Ride double-humped Bactrian camels through the cold desert sand dunes.", 5.0, 2000, 4.6),
            ("Leh Palace", "Culture", "Visit the 17th-century royal palace overlooking the town of Leh.", 1.5, 200, 4.4),
        ],
        "Singapore": [
            ("Gardens by the Bay", "Sightseeing", "Walk among the futuristic Supertrees and explore the Cloud Forest dome.", 3.0, 2800, 4.8),
            ("Hawker Centre Food Tour", "Food", "Taste Michelin-starred hawker food from Singapore's legendary street kitchens.", 2.5, 800, 4.9),
            ("Marina Bay Sands Skypark", "Sightseeing", "Take in panoramic city views from the iconic rooftop observation deck.", 1.5, 2300, 4.6),
            ("Sentosa Island Day", "Adventure", "Enjoy beaches, Universal Studios, and adventure activities on the resort island.", 6.0, 5000, 4.5),
            ("Chinatown Heritage Walk", "Culture", "Explore the historic streets, temples, and markets of Singapore's Chinatown.", 2.0, 0, 4.4),
        ],
        "Istanbul": [
            ("Hagia Sophia", "Culture", "Marvel at the architectural masterpiece that served as cathedral, mosque, and museum.", 2.0, 2500, 4.9),
            ("Grand Bazaar Shopping", "Shopping", "Get lost in one of the world's oldest and largest covered markets.", 3.0, 1000, 4.6),
            ("Bosphorus Cruise", "Sightseeing", "Sail between Europe and Asia on the stunning strait connecting two seas.", 2.0, 1500, 4.7),
            ("Turkish Bath Experience", "Culture", "Indulge in a traditional hammam ritual at a centuries-old bathhouse.", 2.0, 3000, 4.5),
            ("Street Food in Kadikoy", "Food", "Cross to the Asian side for the best street food Istanbul has to offer.", 2.5, 800, 4.7),
        ],
    }

    count = 0
    for dest in destinations:
        city_activities = activities_data.get(dest.city, [])
        for act_data in city_activities:
            name, category, description, duration, cost, rating = act_data
            existing = db.query(Activity).filter(
                Activity.destination_id == dest.id,
                Activity.name == name
            ).first()
            if not existing:
                activity = Activity(
                    destination_id=dest.id,
                    name=name,
                    description=description,
                    category=category,
                    duration_hours=duration,
                    estimated_cost=cost,
                    rating=rating
                )
                db.add(activity)
                count += 1
    db.commit()
    print(f"  ✓ Seeded {count} activities")


def seed_demo_user(db):
    """Create demo user account."""
    existing = db.query(User).filter(User.email == "demo@globetrotter.local").first()
    if existing:
        print("  ✓ Demo user already exists")
        return existing

    demo_user = User(
        name="Explorer",
        email="demo@globetrotter.local",
        password_hash=get_password_hash("Demo@123"),
        language="en",
        is_active=True,
        is_admin=True
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    print(f"  ✓ Created demo user: demo@globetrotter.local / Demo@123")
    return demo_user


def seed_demo_trip(db, user):
    """Create a sample Europe Explorer trip for the demo user."""
    existing = db.query(Trip).filter(Trip.user_id == user.id, Trip.name == "Europe Explorer").first()
    if existing:
        print("  ✓ Demo trip already exists")
        return existing

    # Get destinations
    paris = db.query(Destination).filter(Destination.city == "Paris").first()
    rome = db.query(Destination).filter(Destination.city == "Rome").first()
    barcelona = db.query(Destination).filter(Destination.city == "Barcelona").first()

    if not all([paris, rome, barcelona]):
        print("  ✗ Required destinations not found, skipping demo trip")
        return None

    # Create trip
    start = date.today() + timedelta(days=30)
    trip = Trip(
        user_id=user.id,
        name="Europe Explorer",
        description="A 12-day journey through the cultural capitals of Europe. From the romantic streets of Paris to the ancient ruins of Rome and the vibrant energy of Barcelona.",
        start_date=start,
        end_date=start + timedelta(days=11),
        estimated_budget=84500,
        is_public=True,
        share_token=generate_share_token()
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)

    # Add stops
    stops = []
    stop_data = [
        (paris, start, start + timedelta(days=3), 0),
        (rome, start + timedelta(days=4), start + timedelta(days=7), 1),
        (barcelona, start + timedelta(days=8), start + timedelta(days=11), 2),
    ]
    for dest, s_date, e_date, order in stop_data:
        stop = TripStop(
            trip_id=trip.id,
            destination_id=dest.id,
            start_date=s_date,
            end_date=e_date,
            stop_order=order
        )
        db.add(stop)
        stops.append(stop)
    db.commit()
    for s in stops:
        db.refresh(s)

    # Add itinerary activities
    paris_stop = stops[0]
    rome_stop = stops[1]
    barcelona_stop = stops[2]

    # Paris activities
    paris_activities = db.query(Activity).filter(Activity.destination_id == paris.id).all()
    for i, act in enumerate(paris_activities[:4]):
        ia = ItineraryActivity(
            trip_stop_id=paris_stop.id,
            activity_id=act.id,
            date=start + timedelta(days=i // 2),
            start_time=time(9 + (i % 2) * 4, 0),
            end_time=time(9 + (i % 2) * 4 + int(act.duration_hours), 0),
            activity_order=i
        )
        db.add(ia)

    # Rome activities
    rome_activities = db.query(Activity).filter(Activity.destination_id == rome.id).all()
    for i, act in enumerate(rome_activities[:4]):
        ia = ItineraryActivity(
            trip_stop_id=rome_stop.id,
            activity_id=act.id,
            date=start + timedelta(days=4 + i // 2),
            start_time=time(9 + (i % 2) * 4, 0 if i % 2 == 0 else 30),
            end_time=time(9 + (i % 2) * 4 + int(act.duration_hours), 0),
            activity_order=i
        )
        db.add(ia)

    # Barcelona activities
    bcn_activities = db.query(Activity).filter(Activity.destination_id == barcelona.id).all()
    for i, act in enumerate(bcn_activities[:3]):
        ia = ItineraryActivity(
            trip_stop_id=barcelona_stop.id,
            activity_id=act.id,
            date=start + timedelta(days=8 + i),
            start_time=time(10, 0),
            end_time=time(10 + int(act.duration_hours), 0),
            activity_order=i
        )
        db.add(ia)

    db.commit()

    # Add budget expenses
    expenses = [
        BudgetExpense(trip_id=trip.id, category="transport", description="Flight: Home to Paris", amount=15000, date=start),
        BudgetExpense(trip_id=trip.id, category="transport", description="Train: Paris to Rome", amount=8000, date=start + timedelta(days=4)),
        BudgetExpense(trip_id=trip.id, category="transport", description="Flight: Rome to Barcelona", amount=6000, date=start + timedelta(days=8)),
        BudgetExpense(trip_id=trip.id, category="transport", description="Flight: Barcelona to Home", amount=14000, date=start + timedelta(days=11)),
        BudgetExpense(trip_id=trip.id, category="accommodation", description="Hotel in Paris (4 nights)", amount=16000, date=start),
        BudgetExpense(trip_id=trip.id, category="accommodation", description="Hotel in Rome (4 nights)", amount=12000, date=start + timedelta(days=4)),
        BudgetExpense(trip_id=trip.id, category="accommodation", description="Hotel in Barcelona (4 nights)", amount=10000, date=start + timedelta(days=8)),
        BudgetExpense(trip_id=trip.id, category="activities", description="Eiffel Tower + Louvre", amount=4300, date=start),
        BudgetExpense(trip_id=trip.id, category="activities", description="Colosseum + Vatican", amount=3300, date=start + timedelta(days=4)),
        BudgetExpense(trip_id=trip.id, category="activities", description="Sagrada Familia + Park Güell", amount=3600, date=start + timedelta(days=8)),
        BudgetExpense(trip_id=trip.id, category="meals", description="Daily meals in Paris", amount=4000, date=start),
        BudgetExpense(trip_id=trip.id, category="meals", description="Daily meals in Rome", amount=3500, date=start + timedelta(days=4)),
        BudgetExpense(trip_id=trip.id, category="meals", description="Daily meals in Barcelona", amount=3000, date=start + timedelta(days=8)),
        BudgetExpense(trip_id=trip.id, category="other", description="Travel insurance", amount=2000, date=start),
        BudgetExpense(trip_id=trip.id, category="other", description="Miscellaneous", amount=1500, date=start),
    ]
    for exp in expenses:
        db.add(exp)
    db.commit()

    print(f"  ✓ Created demo trip: Europe Explorer (3 cities, {len(expenses)} expenses)")

    # Save some destinations for demo user
    for dest in [paris, rome, barcelona]:
        existing = db.query(SavedDestination).filter(
            SavedDestination.user_id == user.id,
            SavedDestination.destination_id == dest.id
        ).first()
        if not existing:
            db.add(SavedDestination(user_id=user.id, destination_id=dest.id))
    db.commit()
    print("  ✓ Saved favorite destinations for demo user")

    return trip


def run_seed():
    """Run all seed functions."""
    print("\nGlobeTrotter Database Seeding")
    print("=" * 40)

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("  Seed: Database tables created")

    db = SessionLocal()
    try:
        destinations = seed_destinations(db)
        seed_activities(db, destinations)
        demo_user = seed_demo_user(db)
        seed_demo_trip(db, demo_user)

        print("=" * 40)
        print("Seeding complete!")
        print(f"   Destinations: {db.query(Destination).count()}")
        print(f"   Activities: {db.query(Activity).count()}")
        print(f"   Users: {db.query(User).count()}")
        print(f"   Trips: {db.query(Trip).count()}")
        print(f"\n   Demo login: demo@globetrotter.local / Demo@123")
        print()
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
