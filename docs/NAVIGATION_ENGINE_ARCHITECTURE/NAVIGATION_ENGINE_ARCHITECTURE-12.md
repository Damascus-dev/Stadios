# NAVIGATION_ENGINE_ARCHITECTURE.md

## Chapter 12 — Repository Structure

### Goal

Strict separation of responsibilities.

```
stadiumos-ai/

├── frontend/
│   ├── app/
│   ├── components/
│   ├── features/
│   │   ├── navigation/
│   │   ├── digital-twin/
│   │   ├── auth/
│   │   ├── ai/
│   │   └── dashboard/
│   ├── hooks/
│   ├── stores/
│   └── lib/
│
├── backend/
│   ├── api/
│   ├── auth/
│   ├── graph/
│   ├── navigation/
│   ├── simulation/
│   ├── ai/
│   └── providers/
│
├── stadium/
│   ├── blueprint/
│   ├── generator/
│   ├── metadata/
│   └── assets/
│
├── docs/
└── tests/
```

---

## Rules

Never mix

* Rendering
* Graph
* AI
* Simulation

Each owns its own folder.
