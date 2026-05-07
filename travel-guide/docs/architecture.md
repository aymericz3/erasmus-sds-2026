# Architecture — Travel Guide

## Overview

A web application that lets users discover places in Poznań and plan trips, with filtering by interest (culture, sport, family, etc.). The stack follows a standard 3-tier model: frontend, backend, and database.

---

## Stack

```
Browser (React + Vite)
    ↓  REST API over HTTP
FastAPI (Python)
    ↓  SQL
PostgreSQL
```

---

## Frontend

React 19 with Vite as the build tool and dev server. Component-based UI, no routing library — page navigation is handled via `useState`.

**Features:**
- Category filter selection
- Place listing with select/deselect
- Itinerary generation (planned)

Will communicate with the backend through `fetch()` calls to the REST API.

---

## Backend

Built with Python and FastAPI.

Handles request routing, business logic, and all database interactions. Returns JSON responses to the frontend.

**Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/places` | List all places |
| GET | `/places?categories=art` | Filter by one category |
| GET | `/places?categories=art,sport` | Filter by multiple categories |
| GET | `/categories` | List available categories |

---

## Database

PostgreSQL. Main entity: `Place`.

**`places` table:**

| Field | Type | Description |
|-------|------|-------------|
| id | INTEGER | Primary key |
| name_en | TEXT | Place name in English (nullable) |
| name_pl | TEXT | Place name in Polish (nullable) |
| category | TEXT | landmark, sport, culture, art, outdoor, family, hotel, food |
| description | TEXT | Short description |
| opening_hours | TEXT | e.g., "9am-5pm" |

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
│   ├── index.html         # Vite entry point
│   ├── vite.config.js
│   ├── package.json
│   ├── eslint.config.js
│   ├── public/            # static assets (favicon, icons)
│   └── src/
│       ├── App.jsx        # root component, page routing via useState
│       ├── main.jsx       # React DOM entry point
│       ├── index.css
│       ├── assets/
│       ├── components/
│       ├── pages/
│       └── services/      # API calls (future)
│
├── backend/
│   └── app/
│       ├── main.py        # entry point
│       ├── routes/        # places.py, categories.py
│       ├── models/        # ORM models
│       ├── schemas/       # request/response validation
│       ├── services/      # business logic
│       ├── db/            # session.py
│       └── core/          # config, constants
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── docs/
│   ├── user-stories.md
│   └── architecture.md
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

