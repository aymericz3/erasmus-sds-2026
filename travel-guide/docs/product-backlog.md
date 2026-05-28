# Product Backlog — Poznań Travel Guide

> **Source:** GitHub Project board [`aymericz3/projects/2`](https://github.com/users/aymericz3/projects/2/views/1)
> **Last updated:** 2026-05-28
> **Last synced:** 2026-05-28
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
| [#48](https://github.com/aymericz3/erasmus-sds-2026/issues/48) | Connect frontend to backend | ✅ Completed | S1 · I3 |
| [#49](https://github.com/aymericz3/erasmus-sds-2026/issues/49) | Fetch places from database | ✅ Completed | S1 · I3 |

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
| [#15](https://github.com/aymericz3/erasmus-sds-2026/issues/15) | Allow filter refinement directly from Results page (without returning home) | ✅ Completed | S1 · I3 |

---

### Feature 5 — Itinerary Generation

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#22](https://github.com/aymericz3/erasmus-sds-2026/issues/22) | Define itinerary generation rules (fit within time, sort by priority/category/proximity) | ✅ Completed | S1 · I4 |
| [#20](https://github.com/aymericz3/erasmus-sds-2026/issues/20) | Add trip duration input field (number of days or hours for a single-day trip) | ✅ Completed | S1 · I4 |
| [#21](https://github.com/aymericz3/erasmus-sds-2026/issues/21) | Save duration input in state and pass it to the itinerary generator ✅ Completed | S1 · I4 |
| [#23](https://github.com/aymericz3/erasmus-sds-2026/issues/23) | Create backend endpoint or planner function (receives selected attractions + duration) | ✅ Completed | S1 · I4 |
| [#24](https://github.com/aymericz3/erasmus-sds-2026/issues/24) | Implement basic planning algorithm (add attractions until time limit reached, return ordered list) | ✅ Completed | S1 · I4 |
| [#25](https://github.com/aymericz3/erasmus-sds-2026/issues/25) | Create itinerary results page/section (display generated plan cleanly) | ✅ Completed | S1 · I4 |
| [#26](https://github.com/aymericz3/erasmus-sds-2026/issues/26) | Handle insufficient time case (warn user when attractions cannot fit in available time) | ✅ Completed | S1 · I4 |
| [#27](https://github.com/aymericz3/erasmus-sds-2026/issues/27) | Add regenerate button (re-run planner without re-entering data) | ✅ Completed | S1 · I4 |
| [#57](https://github.com/aymericz3/erasmus-sds-2026/issues/57) | Implement itinerary planner service and endpoint | ✅ Completed | S1 · I4 |

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
| [#51](https://github.com/aymericz3/erasmus-sds-2026/issues/51) | Define intensity level specifications (≥3 levels: attractions/day, walking distance, active hours, break frequency) | ✅ Completed | S1 · I4 |
| [#52](https://github.com/aymericz3/erasmus-sds-2026/issues/52) | Create UI for selecting itinerary intensity (description per option, visual highlight, mobile-friendly) | ✅ Completed | S1 · I4 |
| [#53](https://github.com/aymericz3/erasmus-sds-2026/issues/53) | Add intensity field to itinerary generation request (frontend → backend, default: Balanced) | ✅ Completed | S1 · I4 |
| [#54](https://github.com/aymericz3/erasmus-sds-2026/issues/54) | Adapt itinerary generation based on intensity (Relaxed = fewer attractions, Explorer = more) | ✅ Completed | S1 · I4 |
| [#55](https://github.com/aymericz3/erasmus-sds-2026/issues/55) | Insert free-time/downtime blocks in relaxed itineraries | ✅ Completed | S1 · I4 |
| [#56](https://github.com/aymericz3/erasmus-sds-2026/issues/56) | Allow users to switch intensity after itinerary is generated (regenerate, optionally restore previous) | ✅ Completed | S1 · I4 |

---

### Feature 8 — Itinerary Management (User Control)

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| — | User can remove attractions from itinerary | ✅ Completed | S1 · I4 |
| — | User can reorder attractions in the itinerary | ✅ Completed | S1 · I4 |

---

### Feature 9 — Map Integration

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| — | User can see attractions on the map | ✅ Completed | S1 · I4 |
| — | User can see the route of the itinerary on the map | ✅ Completed | S1 · I4 |

---

### Feature 10 — Itinerary Scheduling & Time Management

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#66](https://github.com/aymericz3/erasmus-sds-2026/issues/66) | Add configurable daily itinerary start time | 📋 TODO | S2 · I1 |
| [#74](https://github.com/aymericz3/erasmus-sds-2026/issues/74) | Define attraction duration logic | 📋 TODO | S2 · I1 |
| [#75](https://github.com/aymericz3/erasmus-sds-2026/issues/75) | Calculate itinerary schedule | 📋 TODO | S2 · I1 |
| [#76](https://github.com/aymericz3/erasmus-sds-2026/issues/76) | Display attraction schedule in UI | 📋 TODO | S2 · I1 |
| [#77](https://github.com/aymericz3/erasmus-sds-2026/issues/77) | Recalculate times after itinerary changes | 📋 TODO | S2 · I1 |
| [#78](https://github.com/aymericz3/erasmus-sds-2026/issues/78) | Prevent scheduling conflicts | 📋 TODO | S2 · I1 |
| [#103](https://github.com/aymericz3/erasmus-sds-2026/issues/103) | Design start time selection UI | 📋 TODO | S2 · I1 |
| [#104](https://github.com/aymericz3/erasmus-sds-2026/issues/104) | Store daily start time | 📋 TODO | S2 · I1 |
| [#105](https://github.com/aymericz3/erasmus-sds-2026/issues/105) | Update itinerary schedule | 📋 TODO | S2 · I1 |
| [#106](https://github.com/aymericz3/erasmus-sds-2026/issues/106) | Validate realistic schedules | 📋 TODO | S2 · I1 |
| [#67](https://github.com/aymericz3/erasmus-sds-2026/issues/67) | Implement itinerary recalculation engine | 📋 TODO | S2 · I2 |
| [#68](https://github.com/aymericz3/erasmus-sds-2026/issues/68) | Validate itinerary feasibility | 📋 TODO | S2 · I2 |

---

### Feature 11 — Break Management

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#63](https://github.com/aymericz3/erasmus-sds-2026/issues/63) | Implement break insertion into itinerary | 📋 TODO | S2 · I1 |
| [#92](https://github.com/aymericz3/erasmus-sds-2026/issues/92) | Design break feature UI | 📋 TODO | S2 · I1 |
| [#93](https://github.com/aymericz3/erasmus-sds-2026/issues/93) | Insert breaks into schedule | 📋 TODO | S2 · I1 |
| [#94](https://github.com/aymericz3/erasmus-sds-2026/issues/94) | Edit and remove breaks | 📋 TODO | S2 · I2 |
| [#95](https://github.com/aymericz3/erasmus-sds-2026/issues/95) | Validate schedule after breaks | 📋 TODO | S2 · I2 |

---

### Feature 12 — Transport & Distance

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#62](https://github.com/aymericz3/erasmus-sds-2026/issues/62) | Add travel time estimation between itinerary locations | 📋 TODO | S2 · I1 |
| [#64](https://github.com/aymericz3/erasmus-sds-2026/issues/64) | Add transportation preference selection | 📋 TODO | S2 · I1 |
| [#65](https://github.com/aymericz3/erasmus-sds-2026/issues/65) | Display distance between itinerary locations | 📋 TODO | S2 · I1 |
| [#89](https://github.com/aymericz3/erasmus-sds-2026/issues/89) | Calculate travel time | 📋 TODO | S2 · I1 |
| [#90](https://github.com/aymericz3/erasmus-sds-2026/issues/90) | Display travel time in UI | 📋 TODO | S2 · I1 |
| [#91](https://github.com/aymericz3/erasmus-sds-2026/issues/91) | Recalculate travel time | 📋 TODO | S2 · I2 |
| [#96](https://github.com/aymericz3/erasmus-sds-2026/issues/96) | Design transport selection UI | 📋 TODO | S2 · I1 |
| [#97](https://github.com/aymericz3/erasmus-sds-2026/issues/97) | Implement transport preference logic | 📋 TODO | S2 · I1 |
| [#98](https://github.com/aymericz3/erasmus-sds-2026/issues/98) | Update itinerary calculations | 📋 TODO | S2 · I2 |
| [#99](https://github.com/aymericz3/erasmus-sds-2026/issues/99) | Save transport preference | 📋 TODO | S2 · I2 |
| [#100](https://github.com/aymericz3/erasmus-sds-2026/issues/100) | Calculate attraction distances | 📋 TODO | S2 · I1 |
| [#101](https://github.com/aymericz3/erasmus-sds-2026/issues/101) | Display distances in UI | 📋 TODO | S2 · I2 |
| [#102](https://github.com/aymericz3/erasmus-sds-2026/issues/102) | Update distances dynamically | 📋 TODO | S2 · I2 |

---

### Feature 13 — External API Integration

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#61](https://github.com/aymericz3/erasmus-sds-2026/issues/61) | Integrate ZPM API | 📋 TODO | S2 · I2 |
| [#84](https://github.com/aymericz3/erasmus-sds-2026/issues/84) | Select attractions API | 📋 TODO | S2 · I2 |
| [#85](https://github.com/aymericz3/erasmus-sds-2026/issues/85) | Integrate API connection | 📋 TODO | S2 · I2 |
| [#86](https://github.com/aymericz3/erasmus-sds-2026/issues/86) | Fetch attraction details | 📋 TODO | S2 · I2 |
| [#87](https://github.com/aymericz3/erasmus-sds-2026/issues/87) | Handle API failures | 📋 TODO | S2 · I2 |
| [#88](https://github.com/aymericz3/erasmus-sds-2026/issues/88) | Integrate routing service | 📋 TODO | S2 · I2 |

---

### Feature 14 — Personalized Itinerary Generation

| # | Title | Status | Sprint · Iter |
|---|---|---|---|
| [#60](https://github.com/aymericz3/erasmus-sds-2026/issues/60) | Implement personalized itinerary generation | 📋 TODO | S2 · I2 |
| [#69](https://github.com/aymericz3/erasmus-sds-2026/issues/69) | Create preference data model | 📋 TODO | S2 · I1 |
| [#70](https://github.com/aymericz3/erasmus-sds-2026/issues/70) | Create preference settings UI | 📋 TODO | S2 · I2 |
| [#71](https://github.com/aymericz3/erasmus-sds-2026/issues/71) | Save user preferences | 📋 TODO | S2 · I2 |
| [#72](https://github.com/aymericz3/erasmus-sds-2026/issues/72) | Load saved preferences | 📋 TODO | S2 · I2 |
| [#73](https://github.com/aymericz3/erasmus-sds-2026/issues/73) | Edit saved preferences | 📋 TODO | S2 · I2 |
| [#79](https://github.com/aymericz3/erasmus-sds-2026/issues/79) | Define personalization factors | 📋 TODO | S2 · I1 |
| [#80](https://github.com/aymericz3/erasmus-sds-2026/issues/80) | Collect user preferences | 📋 TODO | S2 · I2 |
| [#81](https://github.com/aymericz3/erasmus-sds-2026/issues/81) | Implement recommendation weighting logic | 📋 TODO | S2 · I2 |
| [#82](https://github.com/aymericz3/erasmus-sds-2026/issues/82) | Generate personalized itinerary | 📋 TODO | S2 · I2 |
| [#83](https://github.com/aymericz3/erasmus-sds-2026/issues/83) | Test personalization quality | 📋 TODO | S2 · I3 |
