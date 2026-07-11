# StadiumOS AI — Architecture

> System architecture reference. Updated for the Navigation-First pivot.
> See `docs/PROJECT_SHIFT/` for the full project vision.
> See `docs/NAVIGATION_ENGINE_ARCHITECTURE/` for the implementation blueprint.

---

## Project Identity

- **Public Name**: StadiumOS Navigator
- **Internal Name**: StadiumOS AI
- **Vision**: Explainable AI Navigation Platform for large football stadiums
- **Navigation is the product.** Everything else (operations, accessibility, volunteer) supports navigation.

---

## System Architecture

```
User → Frontend (Next.js + R3F Digital Twin)
         → API (FastAPI)
           → Auth Middleware (JWT, RBAC)
             → Orchestrator Pipeline
               → Graph Composer (Physical + Operational + Semantic + Intent)
               → Deterministic Router (Dijkstra on weighted graph)
               → AI Evaluator (explain, predict, compare, suggest)
               → Response
         ← Frontend Rendering (3D path animation, AI card, bottom sheet)
```

### 5 Independent Systems

| System | Responsibility | Never Does |
|---|---|---|
| **Digital Twin** | Visualization, interaction, camera | Routing, reasoning, business logic |
| **Navigation Graph** | Nodes, edges, weights, multi-layer composition | AI reasoning, rendering |
| **Simulation Engine** | Live state (congestion, queues, parking, phase) | Modifying geometry |
| **AI Orchestrator** | Reasoning, explanation, prediction | Path computation |
| **Frontend** | Rendering, animation, touch, camera | Routing calculations |

---

## Principle: AI Owns Reasoning

AI receives a composed graph + user intent + top candidate routes.

AI outputs: recommendation + reason + benefit + tradeoff + confidence.

The **Deterministic Routing Engine** computes shortest paths. AI never does.

---

## Three-Tier Fallback

| Tier | Mechanism | Latency |
|---|---|---|
| 1 — Live AI | Provider factory → API call | ~2-5s |
| 2 — Cache | Pre-computed scenario responses | ~10ms |
| 3 — Rule Engine | Deterministic logic | ~1ms |

The app never depends entirely on a live LLM response. The rehearsed demo works offline.

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js 16, TypeScript, TailwindCSS v4, Three.js, React Three Fiber, @react-three/drei, Zustand |
| Backend | FastAPI, Python 3.11+, Pydantic v2, python-jose (JWT), passlib (OTP) |
| AI | DeepSeek (default), Gemini (secondary) via provider abstraction |
| Stadium | Procedural Python generator from YAML blueprint |
| Storage | In-memory simulation state, JSON files (no DB) |
| Auth | Mock OTP (demo: `123456`), JWT, RBAC (Fan/Volunteer/Operations) |
| Deploy | Vercel (frontend), Render (backend) |

---

## Layer Details

### Frontend (`frontend/`)
- **Framework**: Next.js 16 (App Router) + TypeScript + TailwindCSS v4
- **3D Engine**: React Three Fiber + Three.js + @react-three/drei
- **State**: Zustand stores (auth, navigation, stadium, simulation, ui)
- **Pages**: Landing, Login, Digital Twin (primary), Navigation (route overlay), Dashboard (ops), Alerts
- **Features**: `features/digital-twin/`, `features/navigation/`, `features/auth/`, `features/ai-card/`
- **PWA**: `manifest.json` (standalone), `sw.js` (network-first, offline demo cache)

### Backend (`backend/`)
- **Framework**: FastAPI + Pydantic v2
- **Services**: Auth (OTP + JWT), Graph (multi-layer navigation), Navigation (routing), Simulation, AI
- **Graph Layers**: Physical (immutable), Operational (live state), Semantic (facilities), Intent (user goal)
- **Endpoints**: Health, Auth, Stadium, Graph, Navigation, Dashboard, Alerts, Agents
- **CORS**: localhost:3000, 3001; configured for deployment

### AI Layer (`agents/`)
- **Providers**: Abstract `LLMProvider` interface + factory (`get_provider()`)
  - `deepseek.py`: OpenAI-compatible API, model `deepseek-chat`
  - `gemini.py`: Google Generative AI, model `gemini-2.0-flash`
  - Default: DeepSeek (fallback when Gemini unavailable)
- **Orchestrator**: classifies intent → builds context → selects prompt → LLM call → validates → formats
- **Cache**: Pre-computed demo responses (fallback tier 2)

### Simulation (`simulation/`)
- **Engine**: 12-phase match lifecycle, 14 zones, 3 scenarios
- **State**: Dataclass-based, in-memory
- **Use**: Feeds the Operational Graph with live density/queue/incident data

### Stadium Generator (`stadium/`) — NEW
- **Blueprint**: YAML config (levels, sections, rows, seats, parking, gates, facilities)
- **Generator**: Procedural Python generation of geometry + metadata + navigation graph
- **Metadata**: Unified data models shared across all layers

---

## Multi-Layer Navigation Graph

```
Physical Graph (immutable — roads, gates, corridors, stairs, seats)
         +
Operational Graph (live — crowd density, queue length, match phase)
         +
Semantic Graph (meaning — food, restroom, medical, services)
         +
Intent Graph (user goal — seat, food, exit, emergency)
         ↓
Weighted Navigation Graph (runtime composed per request)
         ↓
Dijkstra Shortest Path
         ↓
AI Explanation
```

---

## Directory Structure

```
f:\stadios\
├── frontend/          # Next.js 16 app
│   └── features/
│       ├── digital-twin/  # R3F 3D stadium
│       ├── navigation/    # Route display, path animation
│       ├── auth/          # Login, OTP
│       └── ai-card/       # Explainability UI
├── backend/
│   └── app/
│       ├── auth/          # OTP + JWT service
│       ├── graph/         # Multi-layer navigation graph
│       └── routes/        # API route handlers
├── stadium/           # Procedural stadium generation
│   ├── blueprint/         # YAML config
│   ├── generator/         # Geometry + metadata generator
│   └── metadata/          # Unified data models
├── agents/            # AI agent logic + providers
├── prompts/           # Prompt templates
├── schemas/           # Pydantic + TS types
├── packages/          # Project-local dep cache
├── docs/
│   ├── SESSION_CONTEXT.md  # ← READ 2nd (after BOOTSTRAP)
│   ├── PROJECT_STATE.md
│   ├── ARCHITECTURE.md     # ← YOU ARE HERE
│   ├── BUILD_HISTORY.md
│   ├── DECISIONS.md
│   ├── TODO.md
│   ├── PROJECT_SHIFT/      # Pivot documentation
│   ├── NAVIGATION_ENGINE_ARCHITECTURE/  # Blueprint spec
│   └── planning/
└── BOOTSTRAP.md       # ← START HERE
```

---

## Demo Flow

Visitor arrives → AI recommends parking → AI recommends gate → AI explains why → conditions change → AI reroutes → visitor reaches seat → diverts to food/restroom → route recalculates → match ends → AI predicts optimal exit → visitor leaves

Every step includes: **reasoning + context + recommendation**.

---

## Prompt Templates (`prompts/`)

| Template | Version | Purpose |
|---|---|---|
| `planner_v1.md` | v1 | Intent classification |
| `navigation_v1.md` | v1 | Route planning |
| `operations_v1.md` | v1 | Operations recommendations |
| `accessibility_v1.md` | v1 | Accessibility routing |
| `formatter_v1.md` | v1 | Response formatting |
