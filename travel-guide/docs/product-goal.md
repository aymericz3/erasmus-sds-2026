# Product Goal — Poznań Travel Guide

## Vision

Help travelers discover and plan their visit to Poznań by providing a personalized, interest-driven guide that surfaces the right places for every type of visitor.

---

## Problem Statement

Travelers arriving in an unfamiliar city face an overwhelming amount of information spread across multiple sources. Deciding which places to visit, how to organize a trip around personal interests, and how to make the most of limited time is genuinely hard — especially for short stays.

Existing generic travel sites do not tailor recommendations to individual profiles (sports enthusiasts, families, art lovers, cyclists, culture seekers, etc.) and rarely offer structured, time-aware itineraries.

---

## Product Goal

**Build a web application that enables any visitor of Poznań to quickly discover places of interest filtered by their personal profile, and to generate a coherent visit plan adapted to their available time and interests.**

---

## Target Users

Based on the identified user stories, the product serves the following traveler profiles:

| Profile | Core Need |
|---|---|
| The explorer | See all must-visit landmarks in the city |
| The sports enthusiast | Find sports facilities and sport-related attractions |
| The short-stay traveler | Generate an efficient itinerary for 1–2 day trips |
| The culture & history lover | Discover historical sites at a relaxed pace |
| The art lover | Browse museums, galleries, and hidden artistic gems |
| The cyclist | Plan bike-friendly routes through the city |
| The family traveler | Locate kid-friendly, educational, and outdoor activities |

---

## Core Features

The product delivers value through the following capabilities, derived directly from user needs:

1. **Place catalog** — A curated database of Poznań attractions covering categories: landmarks, culture, sport, art, outdoor, family, food, and accommodation.
2. **Interest-based filtering** — Users select one or more interest categories to narrow the place listing to what matters to them.
3. **Itinerary generator** — Users receive a suggested visit plan based on selected places, adaptable to trip duration.
4. **Interactive map** — Key locations are shown on a map to support spatial planning.
5. **Hidden gems** — Lesser-known spots are surfaced alongside well-known attractions to reward curious visitors.

---

## Out of Scope (for current scope)

- Support for cities other than Poznań
- User accounts and saved itineraries
- Real-time data (live opening hours, pricing)
- Booking or reservation integration
- Native mobile application

---

## Success Criteria

The product is considered successful when:

- A user can browse places in Poznań filtered by at least one interest category within a few clicks.
- A user can generate a basic itinerary covering their selected places.
- The interface is usable by someone with no prior knowledge of the city.
- All seven traveler profiles from the user stories are served by the filtering and recommendation system.

---

## Team

This product is developed by a team of 5 Erasmus students at Politechnika Poznańska as part of the Software Development Studio course (2026 Summer Semester).

| Developer Name | Special Role |
|---|---|
| Matija Faukovic | Product Owner |
| Miguel Morales | Scrum Master |
| David Alonso |  |
| Aymeric Zaluski |  |
| Furkan Toprak |  |

---

## Technical Alignment

The product is built as a 3-tier web application:

- **Frontend**: React 19 + Vite — component-based UI with category filtering and place listing.
- **Backend**: Python + FastAPI — REST API serving place and category data.
- **Database**: PostgreSQL — stores the place catalog with categories and descriptions.

Full architecture details are in [architecture.md](architecture.md).
