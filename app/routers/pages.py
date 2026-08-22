from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.database.models import User, Trip, Destination
from app.services import trip_service, budget_service
import random

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory="templates")

def get_user_or_redirect(user: User):
    if not user:
        raise HTTPException(status_code=status.HTTP_302_FOUND, headers={"Location": "/login"})
    return user

def get_admin_or_redirect(user: User):
    if not user or not getattr(user, 'is_admin', False):
        raise HTTPException(status_code=status.HTTP_302_FOUND, headers={"Location": "/"})
    return user

@router.get("/", response_class=HTMLResponse)
def landing(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("landing.html", {"request": request, "user": user})

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user: User = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request, user: User = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse("auth/signup.html", {"request": request})

@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_password(request: Request):
    return templates.TemplateResponse("auth/forgot_password.html", {"request": request})

@router.get("/logout")
def logout_page():
    res = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    res.delete_cookie(key="access_token")
    return res

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    recent_trips = db.query(Trip).filter(Trip.user_id == user.id).order_by(Trip.created_at.desc()).limit(5).all()
    all_destinations = db.query(Destination).all()
    recommendations = random.sample(all_destinations, min(6, len(all_destinations))) if all_destinations else []
    stats = {"total_trips": len(recent_trips)}
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "recent_trips": recent_trips, "recommendations": recommendations, "stats": stats})

@router.get("/trips", response_class=HTMLResponse)
def list_trips(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    trips = db.query(Trip).filter(Trip.user_id == user.id).all()
    return templates.TemplateResponse("trips/list.html", {"request": request, "user": user, "trips": trips})

@router.get("/trips/create", response_class=HTMLResponse)
def create_trip(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    destinations = db.query(Destination).all()
    return templates.TemplateResponse("trips/create.html", {"request": request, "user": user, "destinations": destinations})

@router.get("/trips/{trip_id}", response_class=HTMLResponse)
def trip_detail(request: Request, trip_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    trip = trip_service.get_trip(db, trip_id)
    if not trip or str(trip.user_id) != str(user.id):
        return RedirectResponse(url="/trips")
    budget = budget_service.get_budget_summary(db, trip_id)
    return templates.TemplateResponse("trips/detail.html", {"request": request, "user": user, "trip": trip, "budget": budget})

@router.get("/trips/{trip_id}/edit", response_class=HTMLResponse)
def edit_trip(request: Request, trip_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    trip = trip_service.get_trip(db, trip_id)
    if not trip or str(trip.user_id) != str(user.id):
        return RedirectResponse(url="/trips")
    return templates.TemplateResponse("trips/edit.html", {"request": request, "user": user, "trip": trip})

@router.get("/trips/{trip_id}/itinerary", response_class=HTMLResponse)
def trip_itinerary_builder(request: Request, trip_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    trip = trip_service.get_trip(db, trip_id)
    destinations = db.query(Destination).all()
    return templates.TemplateResponse("itinerary/builder.html", {"request": request, "user": user, "trip": trip, "destinations": destinations})

@router.get("/trips/{trip_id}/view", response_class=HTMLResponse)
def trip_itinerary_view(request: Request, trip_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    trip = trip_service.get_trip(db, trip_id)
    return templates.TemplateResponse("itinerary/timeline.html", {"request": request, "user": user, "trip": trip})

@router.get("/trips/{trip_id}/calendar", response_class=HTMLResponse)
def trip_calendar(request: Request, trip_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    trip = trip_service.get_trip(db, trip_id)
    return templates.TemplateResponse("itinerary/calendar.html", {"request": request, "user": user, "trip": trip})

@router.get("/trips/{trip_id}/budget", response_class=HTMLResponse)
def trip_budget(request: Request, trip_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    trip = trip_service.get_trip(db, trip_id)
    budget = budget_service.get_budget_summary(db, trip_id)
    return templates.TemplateResponse("budget/overview.html", {"request": request, "user": user, "trip": trip, "budget": budget})

@router.get("/destinations", response_class=HTMLResponse)
def explore_destinations(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("destinations/explore.html", {"request": request, "user": user})

@router.get("/activities", response_class=HTMLResponse)
def discover_activities(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse("activities/discover.html", {"request": request, "user": user})

@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_user_or_redirect(user)
    
    # Fetch user's trips
    from app.database.models import Trip, Destination, TripStop
    trips = db.query(Trip).filter(Trip.user_id == user.id).all()
    
    # Calculate basic stats
    stats = {
        "trips": len(trips),
        "cities": 0,
        "countries": 0
    }
    
    return templates.TemplateResponse("profile/profile.html", {
        "request": request, 
        "user": user,
        "trips": trips,
        "stats": stats
    })

@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_admin_or_redirect(user)
    
    from app.database.models import User as DBUser, Trip, Destination, Activity, TripStop, ItineraryActivity
    from sqlalchemy import func
    
    # Calculate real stats
    total_users = db.query(DBUser).count()
    active_users = db.query(DBUser).filter(DBUser.is_active == True).count()
    total_trips = db.query(Trip).count()
    total_public_trips = db.query(Trip).filter(Trip.is_public == True).count()
    total_destinations = db.query(Destination).count()
    total_activities = db.query(Activity).count()
    
    stats = {
        "total_users": total_users, 
        "active_users": active_users,
        "total_trips": total_trips, 
        "total_public_trips": total_public_trips, 
        "total_destinations": total_destinations,
        "total_activities": total_activities
    }
    
    # Real popular destinations (based on trip stops)
    pop_dests = db.query(
        Destination.id, Destination.city, Destination.country, func.count(TripStop.id).label('count')
    ).join(TripStop).group_by(Destination.id).order_by(func.count(TripStop.id).desc()).limit(5).all()
    popular_destinations = [{"id": d[0], "city": d[1], "country": d[2], "trip_count": d[3]} for d in pop_dests]
    
    # Real popular activities (based on itinerary activities)
    pop_acts = db.query(
        Activity.id, Activity.name, Activity.category, func.count(ItineraryActivity.id).label('count')
    ).join(ItineraryActivity).group_by(Activity.id).order_by(func.count(ItineraryActivity.id).desc()).limit(5).all()
    popular_activities = [{"id": a[0], "name": a[1], "category": a[2], "added_count": a[3]} for a in pop_acts]
    
    # Recent users
    users = db.query(DBUser).order_by(DBUser.created_at.desc()).limit(10).all()
    recent_users_list = []
    for u in users:
        trips_count = db.query(Trip).filter(Trip.user_id == u.id).count()
        recent_users_list.append({
            "name": u.name, "email": u.email, "trips_count": trips_count, 
            "joined_date": u.created_at.strftime("%Y-%m-%d") if u.created_at else "N/A"
        })
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request, 
        "user": user,
        "stats": stats,
        "popular_destinations": popular_destinations,
        "popular_activities": popular_activities,
        "users": recent_users_list
    })

@router.get("/admin/users", response_class=HTMLResponse)
def admin_users_page(request: Request, user: User = Depends(get_current_user)):
    user = get_admin_or_redirect(user)
    return templates.TemplateResponse("admin/users.html", {"request": request, "user": user})

@router.get("/admin/trips", response_class=HTMLResponse)
def admin_trips_page(request: Request, user: User = Depends(get_current_user)):
    user = get_admin_or_redirect(user)
    return templates.TemplateResponse("admin/trips.html", {"request": request, "user": user})

@router.get("/admin/destinations", response_class=HTMLResponse)
def admin_destinations_page(request: Request, user: User = Depends(get_current_user)):
    user = get_admin_or_redirect(user)
    return templates.TemplateResponse("admin/destinations.html", {"request": request, "user": user})

@router.get("/admin/activities", response_class=HTMLResponse)
def admin_activities_page(request: Request, user: User = Depends(get_current_user)):
    user = get_admin_or_redirect(user)
    return templates.TemplateResponse("admin/activities.html", {"request": request, "user": user})

@router.get("/admin/analytics", response_class=HTMLResponse)
def admin_analytics_page(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    user = get_admin_or_redirect(user)
    from app.database.models import User as DBUser, Trip, Destination, Activity, TripStop, ItineraryActivity
    import datetime
    
    # User analytics
    total_users = db.query(DBUser).count()
    active_users = db.query(DBUser).filter(DBUser.is_active == True).count()
    
    # Trip analytics
    total_trips = db.query(Trip).count()
    public_trips = db.query(Trip).filter(Trip.is_public == True).count()
    
    # Destination analytics
    from sqlalchemy import func
    pop_dests = db.query(
        Destination.city, func.count(TripStop.id).label('count')
    ).join(TripStop).group_by(Destination.id).order_by(func.count(TripStop.id).desc()).limit(10).all()
    dest_labels = [d[0] for d in pop_dests]
    dest_data = [d[1] for d in pop_dests]
    
    # Activity analytics
    pop_cats = db.query(
        Activity.category, func.count(ItineraryActivity.id).label('count')
    ).join(ItineraryActivity).group_by(Activity.category).order_by(func.count(ItineraryActivity.id).desc()).limit(6).all()
    cat_labels = [c[0] for c in pop_cats]
    cat_data = [c[1] for c in pop_cats]
    
    analytics = {
        "users": {"total": total_users, "active": active_users},
        "trips": {"total": total_trips, "public": public_trips},
        "destinations": {"labels": dest_labels, "data": dest_data},
        "categories": {"labels": cat_labels, "data": cat_data}
    }
    
    return templates.TemplateResponse("admin/analytics.html", {"request": request, "user": user, "analytics": analytics})

@router.get("/admin/settings", response_class=HTMLResponse)
def admin_settings_page(request: Request, user: User = Depends(get_current_user)):
    user = get_admin_or_redirect(user)
    import os
    app_version = os.environ.get("APP_VERSION", "1.0.0")
    return templates.TemplateResponse("admin/settings.html", {"request": request, "user": user, "app_version": app_version})

@router.get("/share/{share_token}", response_class=HTMLResponse)
def shared_trip(request: Request, share_token: str, db: Session = Depends(get_db)):
    from app.database.models import Trip
    trip = db.query(Trip).filter(Trip.share_token == share_token).first()
    
    if not trip:
        return templates.TemplateResponse("errors/404.html", {"request": request})
        
    budget_summary = {"total": 0, "categories": {}}
    itinerary = {}
    
    return templates.TemplateResponse("public/shared_trip.html", {
        "request": request, 
        "trip": trip,
        "budget_summary": budget_summary,
        "itinerary": itinerary
    })
