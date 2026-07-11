# NAVIGATION_ENGINE_ARCHITECTURE.md

## Chapter 7 — Backend Architecture

### Services

```text
Auth

Navigation

Digital Twin

Simulation

AI

Analytics
```

---

## APIs

GET

/stadium

GET

/nodes

GET

/graph

POST

/navigate

POST

/reroute

POST

/reason

GET

/crowd

GET

/parking

GET

/facilities

---

## Backend Owns

* Graph
* Metadata
* Occupancy
* Parking
* AI
* Simulation
* Auth

Never Frontend.

---

## Response Rules

* JSON only
* Typed
* Versioned
* Validated

---

## Done

Every frontend screen uses backend APIs only.
