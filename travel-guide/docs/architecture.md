# Architecture — Travel Guide

## Overview

A web application that lets users discover places in Poznań and plan trips, with filtering by interest (culture, sport, family, etc.). The stack follows a standard 3-tier model: frontend, backend, and database.

---

## Stack

```
Browser (HTML/JS)
    ↓  REST API over HTTP
FastAPI (Python)
    ↓  SQL
PostgreSQL
```

---

## Frontend

Plain HTML/CSS/JavaScript. No frameworks to keep it simple and focus on core concepts.

**Features:**
- Place listing
- Category filters
- Itinerary view and map display (in future)

Communicates with the backend exclusively through `fetch()` calls to the REST API.

---

## Backend

Built with Python and FastAPI.

Handles request routing, business logic, and all database interactions. Returns JSON responses to the frontend.

**Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/places` | List all places |
| GET | `/places?category=art` | Filter by category |
| GET | `/itinerary` | Generate an itinerary |

---

## Database

PostgreSQL. Main entities: `Place`, `Category`, `Itinerary`.

**`places` table:**

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| name | TEXT | Place name |
| category | TEXT | art, sport, family… |
| latitude | FLOAT | Coordinates |
| longitude | FLOAT | Coordinates |
| description | TEXT | Short description |
| image_url | TEXT | URL to an image |
| opening_hours | TEXT | e.g., "9am-5pm" |
| price_range | TEXT | e.g., "$", "$$" |
| rating | INTEGER | tour guide rating (1-5) |

---

## Request Flow

1. User selects a city or applies a filter
2. Frontend sends a GET request to the API
3. Backend queries the database
4. Results are returned as JSON
5. Frontend renders the data

---

## Project Structure

```
travel-guide/
├── frontend/
│   ├── public/
│   └── src/
│       ├── assets/        # images, icons
│       ├── components/    # reusable UI components
│       ├── pages/
│       ├── services/      # API calls
│       └── main.js
│
├── backend/
│   └── app/
│       ├── main.py        # entry point
│       ├── routes/        # places.py, itinerary.py
│       ├── models/        # ORM models
│       ├── schemas/       # request/response validation
│       ├── services/      # business logic
│       ├── db/            # session.py
│       └── core/          # config, settings
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── docs/
│   ├── user-stories.md
│   ├── architecture.md
│   └── api-spec.md
│
└── README.md
```

---

## Running Locally

Each part starts independently:

```bash
# Frontend
npm run dev

# Backend
uvicorn app.main:app --reload

# Database
# PostgreSQL running locally
```

---

