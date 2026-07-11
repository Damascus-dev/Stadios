# NAVIGATION_ENGINE_ARCHITECTURE.md

## Chapter 5.7 — Unified Data Model

---

# Objective

Every backend service, frontend component, AI provider, and navigation algorithm SHALL use the same canonical data structures.

No duplicate models.

No frontend-only models.

No backend-only models.

One entity.

One definition.

---

# Core Entities

## Stadium

Contains

* Levels
* Quadrants
* Graph
* Metadata

Owner

Blueprint Generator

---

## Level

Contains

* Sections
* Facilities
* Vertical Connections

---

## Section

Contains

* Rows
* Facilities
* Navigation Nodes

---

## Row

Contains

* Seats

---

## Seat

Fields

```text
id
section
row
number
position
occupied
reserved
accessible
metadata
```

---

## Facility

Types

* Food
* Restroom
* Medical
* Charging
* Prayer
* Volunteer
* Merchandise
* Information

Fields

```text
id

type

position

capacity

occupancy

status
```

---

## Navigation Node

Fields

```text
id

type

position

level

connections

metadata
```

---

## Navigation Edge

Fields

```text
start

end

distance

travel_time

capacity

crowd_weight

accessible
```

---

## Route

Fields

```text
route_id

start

destination

waypoints

eta

distance

reason

confidence
```

---

## Intent

Fields

```text
intent

priority

status

destination

parent

timestamp
```

---

## Crowd State

Fields

```text
zone

density

prediction

confidence

last_updated
```

---

## Parking Zone

Fields

```text
zone

capacity

occupied

available

nearest_gate
```

---

## User Session

Fields

```text
user

role

current_node

intent

route

preferences
```

---

## AI Response

Fields

```text
reason

recommendation

alternatives

confidence

warnings

eta
```

Always structured JSON.

Never free text.

---

# Ownership Matrix

Blueprint

↓

Geometry

Simulation

↓

Operational Data

Graph Engine

↓

Routing

AI

↓

Reasoning

Frontend

↓

Visualization

---

# Rule

Every entity has exactly ONE owner.

No duplicated state.

Single source of truth.

---

# Done

✓ Shared models

✓ Typed

✓ Serializable

✓ Backend + Frontend compatible

✓ AI compatible

This chapter becomes the canonical schema reference for the entire project.
