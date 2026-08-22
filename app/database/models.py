from sqlalchemy import Column, Integer, String, Text, Float, Boolean, Date, Time, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    profile_image = Column(String(500), nullable=True)
    language = Column(String(10), default='en')
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    trips = relationship("Trip", back_populates="user")
    saved_destinations = relationship("SavedDestination", back_populates="user")

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    cover_image = Column(String(500), nullable=True)
    estimated_budget = Column(Float, default=0)
    is_public = Column(Boolean, default=False)
    share_token = Column(String(64), unique=True, nullable=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", back_populates="trips")
    stops = relationship("TripStop", back_populates="trip", cascade="all, delete-orphan")
    expenses = relationship("BudgetExpense", back_populates="trip", cascade="all, delete-orphan")

class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    region = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    image = Column(String(500), nullable=True)
    cost_index = Column(Integer, default=3)
    popularity = Column(Integer, default=50)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    activities = relationship("Activity", back_populates="destination")
    trip_stops = relationship("TripStop", back_populates="destination")
    saved_by_users = relationship("SavedDestination", back_populates="destination")

class TripStop(Base):
    __tablename__ = "trip_stops"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    stop_order = Column(Integer, nullable=False, default=0)
    notes = Column(Text, nullable=True)

    trip = relationship("Trip", back_populates="stops")
    destination = relationship("Destination", back_populates="trip_stops")
    itinerary_activities = relationship("ItineraryActivity", back_populates="trip_stop", cascade="all, delete-orphan")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)
    duration_hours = Column(Float, default=2.0)
    estimated_cost = Column(Float, default=0)
    image = Column(String(500), nullable=True)
    rating = Column(Float, default=4.0)

    destination = relationship("Destination", back_populates="activities")
    itinerary_activities = relationship("ItineraryActivity", back_populates="activity")

class ItineraryActivity(Base):
    __tablename__ = "itinerary_activities"
    id = Column(Integer, primary_key=True, index=True)
    trip_stop_id = Column(Integer, ForeignKey("trip_stops.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    custom_cost = Column(Float, nullable=True)
    activity_order = Column(Integer, default=0)
    notes = Column(Text, nullable=True)

    trip_stop = relationship("TripStop", back_populates="itinerary_activities")
    activity = relationship("Activity", back_populates="itinerary_activities")

class BudgetExpense(Base):
    __tablename__ = "budget_expenses"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    trip = relationship("Trip", back_populates="expenses")

class SavedDestination(Base):
    __tablename__ = "saved_destinations"
    __table_args__ = (UniqueConstraint('user_id', 'destination_id', name='uq_user_destination'),)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="saved_destinations")
    destination = relationship("Destination", back_populates="saved_by_users")
