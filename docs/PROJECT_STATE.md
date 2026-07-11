# StadiumOS AI — Project State

> Single source of truth. Read this before any other document.

---

## Current Phase

**Phase 11 — Explainable AI Navigation ✓**

---

## Completed

| Phase | Summary |
|---|---|
| Phase 1 — Research & Architecture Lock | Antigravity compatibility, 6 personas, 5 prompt templates, simulation engine (12 phases, 14 zones, 3 scenarios), v2/v3/v4 plans |
| Phase 2 — Frontend Shell | 5 pages (Landing, Dashboard, Navigation, Chat, Alerts), glassmorphism dark-mode UI, PWA manifest + service worker, mobile layout fix |
| Phase 3 — Backend Skeleton | FastAPI with 7 endpoints, 22 Pydantic schemas, realistic FIFA mock data, CORS configured |
| Phase 4 — AI Orchestrator | Intent classifier, provider abstraction (DeepSeek + Gemini), cache/fallback layer, orchestrator pipeline, frontend wired to API |
| Phase 5 — Navigation Agent | Deterministic route engine (Dijkstra, congestion-aware, accessibility-aware), 3-tier routing, shared simulation state |
| Phase 6 — Operations Agent | Deterministic operations engine (zone analysis, predictions, volunteer allocation, transportation/sustainability signals), dashboard fully wired |
| Phase 7 — Foundation Stabilization | Repository audit, dependency cleanup, directory skeleton, auto-compaction protocol, documentation update |
| Phase 8 — Authentication & RBAC | OTP service (demo `123456`), JWT sign/verify, role middleware (fan/volunteer/operations), auth routes, Zustand authStore, login+OTP+role-selector screens, ProtectedRoute, role-based redirects |
| Phase 9 — Procedural Digital Twin | Stadium generator (levels, 57,600 seats, 116 facilities, 12 parking zones, 120-node/525-edge graph), backend APIs (`GET /api/stadium`, `/graph`, `/facilities`), R3F StadiumCanvas with rings/InstancedMesh seats/facility markers, DestinationPicker, Zustand stadiumStore, sidebar nav item |
| Phase 10 — Navigation Engine | Physical/Operational/Semantic graph services, Graph Composer (<100ms runtime), extended Dijkstra navigator, `POST /api/navigation/route` returns path spline data, `/api/navigation/zones` serves physical graph nodes, frontend RoutePath tube rendering, "Navigate Here" wired end-to-end |
| Phase 11 — Explainable AI | AI prompt `navigation_explain_v1.md`, backend route alternatives (find_alternatives), AICard component on stadium+navigation pages, dynamic reroute (useAutoReroute hook, POST /api/navigation/reroute), intent transitions (NextIntent component, POST /api/navigation/next-intent), frontend API types synced (NavigationResponse + RouteAlternative) |

---

## Project Vision (Navigation-First Pivot)

**Before**: "A Smart Stadium Operating System solving every stadium problem."

**After**: **"An Explainable AI Navigation Platform for Smart Stadiums."**

- **Public Name**: StadiumOS Navigator
- **Navigation is the product** — everything else supports navigation
- **Primary Persona**: Fan (80% of presentation)
- **Secondary**: Volunteer (10%), Operations (10%)
- **3D Digital Twin** is the primary interface
- **AI explains** — deterministic engine computes
- See `docs/PROJECT_SHIFT/` for full vision

---

## Current Provider

**DeepSeek** (`deepseek-chat` via OpenAI-compatible API at `api.deepseek.com`)

Secondary: Gemini (`gemini-2.0-flash`) — quota exhausted, fallback to DeepSeek.

---

## Known Issues

- Gemini API free tier quota exhausted (429 RESOURCE_EXHAUSTED) — DeepSeek configured as default

---

## Active Branch

`main` — always demo-ready

---

## Deployment Status

- **Frontend**: Local dev only (`http://localhost:3000`)
- **Backend**: Local dev only (`http://localhost:8000`)
- **Production**: Not deployed

---

## Current Blockers

None

---

## Next Phases

1. Phase 11 — Explainable AI (CURRENT)
2. Phase 12 — Deployment Hardening

---

## Resume Context

> 2026-07-11 (Session 10 — Phase 11 completion)

**Changes this session**:
- Phase 11 — Explainable AI Navigation completed
- `frontend/lib/api.ts`: Fixed NavigationResponse type — added path, reason, benefit, tradeoff, confidence, alternatives, RouteAlternative
- `frontend/app/navigation/page.tsx`: Added AICard + NextIntent components below route details; saves route to zustand store
- `backend/app/graph/navigator.py`: Refactored with _dijkstra() helper, find_alternatives() for K-shortest paths
- `backend/app/routes/navigation.py`: Added POST /api/navigation/reroute, POST /api/navigation/next-intent with INTENT_CHAINS, alternatives in _build_deterministic_route
- `frontend/hooks/useAutoReroute.ts`: New — polls every 30s and recalculates route
- `frontend/features/navigation/NextIntent.tsx`: New — suggests next logical destination based on intent chain + match phase
- `frontend/app/stadium/page.tsx`: Integrated useAutoReroute + NextIntent
- `docs/TODO.md`, `docs/PROJECT_STATE.md`: Updated for Phase 11 completion

**Blockers**: None

**Next**: Phase 12 — Deployment Hardening (Vercel, Render, PWA, bundle optimization, error boundaries, competition deliverables)

---

> Last updated: 2026-07-11
