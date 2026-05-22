# Product Backlog — Poznań Travel Guide

> **Source:** GitHub Project board [`aymericz3/projects/2`](https://github.com/users/aymericz3/projects/2/views/1)
> **Last updated:** 2026-05-16
> **Last synced:** 2026-05-15
> **Note:** This backlog is a living document and may evolve as the project progresses. It reflects the current state of identified work items, their status, and how they map to user stories and features.
> **Related documents:** [Product Goal](product-goal.md), [Definition of Done](definition-of-done.md), [User Stories](user-stories.md), [Architecture](architecture.md)


---

## Sprint & Iteration Timeline

| | Iteration 1 Start | Iteration 1 to 2 | Iteration 2 to 3 | Iteration 3 to 4 | Iteration 4 End |
|---|---|---|---|---|---|
| **Sprint 1** | Fri 24 Apr | Wed 29 Apr | Wed 6 May | Fri 15 May | Fri 22 May |
| **Sprint 2** | Fri 22 May | Fri 29 May | Fri 5 Jun | Fri 12 Jun | Fri 19 Jun |

Sprint boundaries = physical meetings with teachers. Iteration boundaries = online meetings.

---

## Board Overview

Items are grouped by feature area. Each item shows its status and the sprint/iteration it was completed in or is planned for.

| Icon | Status | Meaning |
|---|---|---|
| ✅ | Completed | Implemented and merged |
| 🔄 | In Progress | Active work in current iteration |
| 📋 | TODO | Committed to current sprint, not yet started |
| 📌 | Product Backlog | Identified but not yet scheduled |

---

## User Stories

The backlog is driven by the 7 user stories defined in [user-stories.md](user-stories.md):

| ID | Profile | Core Need |
|---|---|---|
| US#01 | The explorer | Visit all must-see landmarks |
| US#02 | The sports enthusiast | Find sports venues and sport-related attractions |
| US#03 | The short-stay traveler | Generate an efficient itinerary for a short trip |
| US#04 | The culture & history lover | Discover historical sites at a relaxed pace |
| US#05 | The art lover | Browse museums, galleries, and hidden artistic gems |
| US#06 | The cyclist | Plan bike-friendly routes through the city |
| US#07 | The family traveler | Locate kid-friendly, educational, and outdoor activities |

---

### Feature 1 — Team & Project Setup

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| — | Team introductions and role assignment (Product Owner, Scrum Master) | ✅ Completed | S1 · I1 |
| — | Create shared GitHub repository and project page, and a WhatsApp group | ✅ Completed | S1 · I1 |
| [#3](https://github.com/aymericz3/erasmus-sds-2026/issues/3) | Create project initial structure (frontend / backend / database folders) | ✅ Completed | S1 · I1 |
| [#34](https://github.com/aymericz3/erasmus-sds-2026/issues/34) | Create backend project structure (routes, services, models, config) | ✅ Completed | S1 · I1 |
| [#33](https://github.com/aymericz3/erasmus-sds-2026/issues/33) | Connect backend to PostgreSQL | ✅ Completed | S1 · I2 |

---

### Feature 2 — Attractions Data Layer

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#9](https://github.com/aymericz3/erasmus-sds-2026/issues/9) | Create Poznań attractions dataset (min 15–20 entries with name, category, description, opening hours) | ✅ Completed | S1 · I2 |
| [#10](https://github.com/aymericz3/erasmus-sds-2026/issues/10) | Define final categories list (landmark, sport, culture, art, outdoor, family, hotel, food) | ✅ Completed | S1 · I2 |
| [#28](https://github.com/aymericz3/erasmus-sds-2026/issues/28) | Add estimated visit duration to each attraction (e.g. Museum: 90 min, Park: 45 min) | ✅ Completed | S1 · I3 |
| [#35](https://github.com/aymericz3/erasmus-sds-2026/issues/35) | Create `GET /places` endpoint — returns all attractions as JSON | ✅ Completed | S1 · I3 |
| [#36](https://github.com/aymericz3/erasmus-sds-2026/issues/36) | Create `GET /places?categories=...` endpoint — filtered by one or more categories | ✅ Completed | S1 · I3 |

---

### Feature 3 — Home Page & Category Selection

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#4](https://github.com/aymericz3/erasmus-sds-2026/issues/4) | Create Home Page (landing page with greeting, category section) | ✅ Completed | S1 · I3 |
| [#5](https://github.com/aymericz3/erasmus-sds-2026/issues/5) | Build category selector UI (multi-selectable checkboxes or cards) | ✅ Completed | S1 · I3 |
| [#6](https://github.com/aymericz3/erasmus-sds-2026/issues/6) | Add "Select All" option — clicking selects every category | ✅ Completed | S1 · I3 |
| [#7](https://github.com/aymericz3/erasmus-sds-2026/issues/7) | Add Explore button — submits selected categories, navigates to Results page | ✅ Completed | S1 · I3 |
| [#8](https://github.com/aymericz3/erasmus-sds-2026/issues/8) | Store selected categories and pass them to Results page | ✅ Completed | S1 · I3 |

---

### Feature 4 — Results Page & Attraction Browsing

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#11](https://github.com/aymericz3/erasmus-sds-2026/issues/11) | Create Results Page layout (grid container) | ✅ Completed | S1 · I2 |
| [#12](https://github.com/aymericz3/erasmus-sds-2026/issues/12) | Build attraction cards (name, category, description — responsive layout) | ✅ Completed | S1 · I2 |
| [#29](https://github.com/aymericz3/erasmus-sds-2026/issues/29) | Show estimated duration on attraction cards | ✅ Completed | S1 · I2 |
| [#16](https://github.com/aymericz3/erasmus-sds-2026/issues/16) | Add select/deselect toggle per attraction card (clearly visible state) | ✅ Completed | S1 · I2 |
| [#17](https://github.com/aymericz3/erasmus-sds-2026/issues/17) | Highlight selected attraction cards visually | ✅ Completed | S1 · I2 |
| [#18](https://github.com/aymericz3/erasmus-sds-2026/issues/18) | Display selection count in header (e.g. "3 selected") | ✅ Completed | S1 · I3 |
| [#19](https://github.com/aymericz3/erasmus-sds-2026/issues/19) | Show Plan Trip button once at least one attraction is selected | ✅ Completed | S1 · I2 |
| [#13](https://github.com/aymericz3/erasmus-sds-2026/issues/13) | Implement category filtering logic (show only matching categories, multi-category support) | ✅ Completed | S1 · I2 |
| [#14](https://github.com/aymericz3/erasmus-sds-2026/issues/14) | Show all attractions when no filter is selected (safe fallback) | ✅ Completed | S1 · I2 |
| [#15](https://github.com/aymericz3/erasmus-sds-2026/issues/15) | Allow filter refinement directly from Results page (without returning home) | 📋 TODO | S1 · I4 |

---

### Feature 5 — Itinerary Generation

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#22](https://github.com/aymericz3/erasmus-sds-2026/issues/22) | Define itinerary generation rules (fit within time, sort by priority/category/proximity) | 🔄 In Progress | S1 · I4 |
| [#20](https://github.com/aymericz3/erasmus-sds-2026/issues/20) | Add trip duration input field (number of days or hours for a single-day trip) | 📋 TODO | S1 · I4 |
| [#21](https://github.com/aymericz3/erasmus-sds-2026/issues/21) | Save duration input in state and pass it to the itinerary generator | 📋 TODO | S1 · I4 |
| [#23](https://github.com/aymericz3/erasmus-sds-2026/issues/23) | Create backend endpoint or planner function (receives selected attractions + duration) | 📋 TODO | S1 · I4 |
| [#24](https://github.com/aymericz3/erasmus-sds-2026/issues/24) | Implement basic planning algorithm (add attractions until time limit reached, return ordered list) | 📋 TODO | S1 · I4 |
| [#25](https://github.com/aymericz3/erasmus-sds-2026/issues/25) | Create itinerary results page/section (display generated plan cleanly) | 📋 TODO | S1 · I4 |
| [#26](https://github.com/aymericz3/erasmus-sds-2026/issues/26) | Handle insufficient time case (warn user when attractions cannot fit in available time) | 📋 TODO | S1 · I4 |
| [#27](https://github.com/aymericz3/erasmus-sds-2026/issues/27) | Add regenerate button (re-run planner without re-entering data) | 🔄 In Progress | S1 · I4 |

---

### Feature 6 — Duration & Time Display

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#30](https://github.com/aymericz3/erasmus-sds-2026/issues/30) | Show estimated duration in itinerary view (each stop shows time needed) | ✅ Completed | S1 · I2 |
| [#31](https://github.com/aymericz3/erasmus-sds-2026/issues/31) | Calculate total time from all selected itinerary items | ✅ Completed | S1 · I2 |
| [#32](https://github.com/aymericz3/erasmus-sds-2026/issues/32) | Display total duration prominently (e.g. "Total: 5h 30m") | ✅ Completed | S1 · I2 |

---

### Feature 7 — Itinerary Intensity Levels

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#51](https://github.com/aymericz3/erasmus-sds-2026/issues/51) | Define intensity level specifications (≥3 levels: attractions/day, walking distance, active hours, break frequency) | 📋 TODO | S1 · I4 |
| [#52](https://github.com/aymericz3/erasmus-sds-2026/issues/52) | Create UI for selecting itinerary intensity (description per option, visual highlight, mobile-friendly) | 📋 TODO | S1 · I4 |
| [#53](https://github.com/aymericz3/erasmus-sds-2026/issues/53) | Add intensity field to itinerary generation request (frontend → backend, default: Balanced) | 📋 TODO | S1 · I4 |
| [#54](https://github.com/aymericz3/erasmus-sds-2026/issues/54) | Adapt itinerary generation based on intensity (Relaxed = fewer attractions, Explorer = more) | 📋 TODO | S1 · I4 |
| [#55](https://github.com/aymericz3/erasmus-sds-2026/issues/55) | Insert free-time/downtime blocks in relaxed itineraries | 📋 TODO | S1 · I4 |
| [#56](https://github.com/aymericz3/erasmus-sds-2026/issues/56) | Allow users to switch intensity after itinerary is generated (regenerate, optionally restore previous) | 📋 TODO | S1 · I4 |

---

### Feature 8 — Itinerary Management (User Control)

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| — | User can remove attractions from itinerary | 📌 Product Backlog | — |
| — | User can reorder attractions in the itinerary | 📌 Product Backlog | — |

---

### Feature 9 — Map Integration

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| — | User can see attractions on the map | 📌 Product Backlog | — |
| — | User can see the route of the itinerary on the map | 📌 Product Backlog | — |