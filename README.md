# 🌍 GlobeTrotter

### Personalized Multi-City Travel Planning & Budget Management Platform

GlobeTrotter is a full-stack web application designed to help travelers discover incredible destinations, organize complex multi-city journeys, track their travel budget, and share their itineraries with the world. Built with a robust Python backend and a dynamic, server-rendered frontend, it provides a cinematic and highly interactive trip-planning experience.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg?logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57.svg?logo=sqlite&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-Templates-B41717.svg?logo=jinja&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Vanilla-F7DF1E.svg?logo=javascript&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4+-38B2AC.svg?logo=tailwind-css&logoColor=white)

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [User Roles](#user-roles)
- [Feature Matrix](#feature-matrix)
- [Screen / Page Overview](#screen--page-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)

---

## Project Overview

Planning a trip with multiple stops, keeping track of daily activities, and managing the budget across different currencies and categories can quickly become overwhelming. GlobeTrotter solves this by unifying the entire travel lifecycle into one platform.

The core traveler workflow is:
**DISCOVER** ➔ **PLAN** ➔ **BUILD ITINERARY** ➔ **TRACK BUDGET** ➔ **SHARE JOURNEY**

From discovering curated destinations to generating a shareable link for friends and family, GlobeTrotter acts as a centralized travel companion.

---

## Key Features

### Authentication
- **Registration & Login**: Secure user authentication with JWT cookies.
- **Logout**: Session termination and cookie clearing.
- **Password Hashing**: Secure storage using `bcrypt`.
- **Session Management**: HTTP-only JWT cookies for security.
- **Role-based Access**: Hard separation between Travelers and Administrators.

### Traveler Features
- **Dashboard**: High-level overview of upcoming trips and recommended destinations.
- **Trip Management**: Create, edit, and delete travel plans.
- **Multi-city Trips**: Add, remove, and drag-and-drop reorder stops via the visual builder.
- **Destination Discovery**: Browse a global catalog of destinations.
- **Activity Discovery**: Explore activities linked to specific destinations.
- **Calendar & Timeline**: View trips sequentially or mapped on a calendar.
- **Budget Tracking**: Log expenses by category, compare against estimated budget, and view Chart.js breakdowns.
- **Saved Destinations**: Bookmark favorite locations for future trips.
- **Public Trip Sharing**: Generate a unique secure token to share read-only trips with guests.
- **Copy Shared Trip**: Clone a public trip into your own account as a template.
- **Profile Management**: Update user details and preferences.

### Admin Features
- **Admin Dashboard**: System-wide overview.
- **User Management**: View, activate/deactivate, and change roles of users.
- **Trip Monitoring**: Read-only access to all platform trips.
- **Destination Management**: Create, update, and delete global destinations.
- **Activity Management**: Create, update, and delete global activities.
- **Analytics**: Platform statistics and usage growth metrics.

### Partially Implemented
- **Activity Planning in Itinerary Builder**: The backend REST APIs for adding/reordering specific activities on specific days (`ItineraryActivity`) are fully implemented and functional, but the frontend UI inside the Itinerary Builder is currently mocked (awaiting frontend integration).

### Future Enhancements
- Real-time collaborative trip editing.
- Email verification and robust password reset flow.
- Maps integration for walking/driving directions between itinerary stops.
- Multi-currency budget conversion.

---

## User Roles

### Traveler
The primary authenticated user. Travelers can browse the catalog, create private trips, add destinations, log budget expenses, bookmark favorite locations, and generate public sharing links for their friends.

### Administrator
System administrators manage the platform. They populate and edit the global catalog of Destinations and Activities, monitor overall platform usage and analytics, and have the power to suspend or elevate other user accounts. 

### Guest / Public Viewer
Unauthenticated visitors landing on the platform. Guests can explore the public landing page, browse the catalog of global destinations and activities, and view specific shared trips if provided with a valid `share_token` link by a Traveler. They must create an account to start planning or copying trips.

---

## Feature Matrix

| Feature | Traveler | Admin | Guest |
|---------|----------|-------|-------|
| **Authentication** | ✅ | ✅ | ❌ |
| **Trip Management** | ✅ | ❌ (View Only) | ❌ |
| **Destination Discovery** | ✅ | ✅ | ✅ |
| **Activity Discovery** | ✅ | ✅ | ✅ |
| **Itinerary Building** | ✅ | ❌ | ❌ (View Only) |
| **Budget Tracking** | ✅ | ❌ | ❌ |
| **Sharing (Create Token)** | ✅ | ❌ | ❌ |
| **Copy Shared Trip** | ✅ | ✅ | ❌ |
| **Profile Management** | ✅ | ✅ | ❌ |
| **Admin Dashboard** | ❌ | ✅ | ❌ |
| **User Management** | ❌ | ✅ | ❌ |
| **Destination Management** | ❌ | ✅ | ❌ |
| **Activity Management** | ❌ | ✅ | ❌ |
| **Platform Analytics** | ❌ | ✅ | ❌ |

---

## Screen / Page Overview

The platform is built using Jinja2 templates served by FastAPI. Here is a breakdown of the major routes and views:

| Page | Route | Access | Purpose |
|------|-------|--------|---------|
| **Landing Page** | `/` | Public | Marketing landing page. |
| **Login** | `/login` | Public | User authentication. |
| **Signup** | `/signup` | Public | Account creation. |
| **Forgot Password** | `/forgot-password` | Public | Account recovery view. |
| **Shared Trip** | `/share/{token}` | Public | Read-only view of a public trip. |
| **Explore** | `/destinations` | Traveler/Guest | Global destination grid. |
| **Discover** | `/activities` | Traveler/Guest | Global activity grid. |
| **Dashboard** | `/dashboard` | Traveler | User's main hub and recent trips. |
| **My Trips** | `/trips` | Traveler | List of all user trips. |
| **Create Trip** | `/trips/create` | Traveler | Form to initialize a new journey. |
| **Trip Detail** | `/trips/{id}` | Traveler | Trip overview and high-level stats. |
| **Itinerary Builder** | `/trips/{id}/itinerary` | Traveler | Interactive map and routing interface. |
| **Timeline View** | `/trips/{id}/view` | Traveler | Vertical timeline of the trip. |
| **Calendar View** | `/trips/{id}/calendar` | Traveler | Month-view calendar of the trip. |
| **Budget Overview** | `/trips/{id}/budget` | Traveler | Expense logging and visual charts. |
| **Profile** | `/profile` | Traveler | User settings. |
| **Admin Panel** | `/admin` | Admin | Main administrative dashboard. |
| **Admin Users** | `/admin/users` | Admin | User management interface. |
| **Admin Trips** | `/admin/trips` | Admin | Platform trip monitoring. |
| **Admin Catalog** | `/admin/destinations` | Admin | Destination CRUD interface. |
| **Admin Analytics** | `/admin/analytics` | Admin | Data and growth metrics. |

---

## Tech Stack

- **Backend Architecture**: FastAPI (Python 3.11+)
- **Database**: SQLite with SQLAlchemy 2.0 ORM and Alembic migrations.
- **Frontend Views**: Jinja2 Templating Engine.
- **Styling**: Tailwind CSS (via CDN) with a custom design system palette.
- **Frontend Interactivity**: Vanilla JavaScript, SortableJS (drag-and-drop), Leaflet.js (mapping), Chart.js (budget visualizations).
- **Security**: JWT tokens in HttpOnly cookies, Passlib with bcrypt hashing.

---

## Project Structure

```text
├── app/
│   ├── core/           # Security, dependencies, config
│   ├── database/       # Models, session maker, DB setup
│   ├── routers/        # API and Page route controllers
│   ├── schemas/        # Pydantic validation models
│   └── services/       # Business logic (trips, users, budget)
├── static/
│   ├── css/            # Custom stylesheets
│   ├── js/             # Global scripts
│   └── images/         # Assets
├── templates/          # Jinja2 HTML templates
│   ├── admin/
│   ├── auth/
│   ├── budget/
│   ├── components/
│   ├── itinerary/
│   └── trips/
├── globetrotter.db     # SQLite Database
└── requirements.txt    # Python Dependencies
```
