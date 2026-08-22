"""
GlobeTrotter - Plan Your Journey. Explore Your World.
Main FastAPI Application
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.config import settings
from app.database.database import engine, Base

# Create all tables on startup (for hackathon/development)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GlobeTrotter",
    description="Plan Your Journey. Explore Your World.",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))

# Import and include routers
from app.routers import auth, pages, trips, destinations, activities, itinerary, budget, public, profile, admin

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(trips.router)
app.include_router(destinations.router)
app.include_router(activities.router)
app.include_router(itinerary.router)
app.include_router(budget.router)
app.include_router(public.router)
app.include_router(profile.router)
app.include_router(admin.router)


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=404,
            content={"success": False, "error": {"code": "NOT_FOUND", "message": "Resource not found"}}
        )
    return templates.TemplateResponse("errors/404.html", {"request": request}, status_code=404)

@app.exception_handler(403)
async def forbidden_handler(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=403,
            content={"success": False, "error": {"code": "FORBIDDEN", "message": "Access denied"}}
        )
    return templates.TemplateResponse("errors/403.html", {"request": request}, status_code=403)

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": {"code": "SERVER_ERROR", "message": "Internal server error"}}
        )
    return templates.TemplateResponse("errors/500.html", {"request": request}, status_code=500)


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    print("=" * 60)
    print("  GlobeTrotter - Plan Your Journey. Explore Your World.")
    print("=" * 60)
    print(f"  Environment: {settings.APP_ENV}")
    print(f"  Database: {settings.DATABASE_URL}")
    print(f"  Docs: http://localhost:8000/docs")
    print("=" * 60)
