# StadiumOS AI — TODO

> Active tasks only. Remove completed items.

---

## Phase 9 — Procedural Digital Twin ✓

- [x] Create `stadium/blueprint/config.yaml` with full stadium parameters
- [x] Create `stadium/metadata/schemas.py` — unified data models
- [x] Create `stadium/generator/` — levels, seating, facilities, parking, graph
- [x] Validate generator output (all nodes reachable, no isolated nodes)
- [x] Backend APIs: GET /api/stadium, GET /api/graph, GET /api/facilities/{type}
- [x] Frontend: R3F Scene, Stadium mesh, InstancedMesh seats, OrbitControls
- [x] Zustand stadiumStore

## Phase 10 — Navigation Engine ✓

- [x] Physical Graph service (immutable)
- [x] Operational Graph service (reads simulation state)
- [x] Semantic Graph service (facility index)
- [x] Graph Composer — runtime weighted graph <100ms
- [x] Extended Dijkstra with congestion/queue/accessibility weights
- [x] POST /api/navigation/route, GET /api/navigation/zones
- [x] Frontend: RoutePath (spline glow), DestinationPicker, "Navigate Here" button

**Deferred** (not required for MVP):
- [ ] Intent Graph service (state machine) — can be handled by existing intent classifier
- [ ] POST /api/reroute — current route recalculates on new navigate call

## Phase 11 — Explainable AI ✓

- [x] AI prompt: `navigation_explain_v1.md` — reason + benefit + tradeoff + confidence
- [x] AI output schema: route + reason + benefit + tradeoff + confidence
- [x] Frontend: AICard component showing AI reasoning below route display (stadium + navigation pages)
- [x] Route alternatives: show top 2-3 options with AI comparison (backend + AICard)
- [x] Dynamic reroute: auto-recalculate when simulation state changes (useAutoReroute hook)
- [x] Intent transitions: parking → gate → seat → facility → exit (NextIntent component + /api/navigation/next-intent)
- [x] Frontend API types: NavigationResponse updated with reason/benefit/tradeoff/confidence/alternatives/path

## Phase 12 — Deployment Hardening ✓

- [x] Vercel configuration (`vercel.json`, `next.config.ts`)
- [x] Render configuration (`render.yaml`, `requirements.txt`, `runtime.txt`)
- [x] Bundle optimization — static assets ~1.7MB (<5MB)
- [x] Error boundaries — graceful fallbacks
- [x] Project README (`README.md`)
- [ ] Deploy to Vercel (user action required)
- [ ] Deploy to Render (user action required)
- [ ] PWA verification, Lighthouse 90+
- [ ] Competition deliverables (blog post, LinkedIn, demo video, presentation)
