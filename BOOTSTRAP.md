# StadiumOS AI — Agent Bootstrap

> **READ THIS FILE FIRST.** This is the single-file entry point for any agent session working on this project.

---

## Project Identity

**StadiumOS AI** (public name: **StadiumOS Navigator**) — An Explainable AI Navigation Platform for large football stadiums.
Built for **PromptWars Virtual Challenge 4** hackathon.

**Navigation is the product.** Everything else (operations, accessibility, volunteer tools) supports navigation.

---

## Read Order (mandatory — do not skip)

1. **This file** — you're here
2. **Session Context** → `f:\stadios\docs\SESSION_CONTEXT.md` — compacted agent handoff, resume context, current state. Read this IMMEDIATELY after BOOTSTRAP.md
3. **Project State** → `f:\stadios\docs\PROJECT_STATE.md` — single source of truth, current phase, blockers, resume context
4. **Architecture** → `f:\stadios\docs\ARCHITECTURE.md` — system architecture reference (read the PROJECT_SHIFT and NAVIGATION_ENGINE_ARCHITECTURE folders for the new vision)
5. **TODO** → `f:\stadios\docs\TODO.md` — active tasks
6. **Build History** → `f:\stadios\docs\BUILD_HISTORY.md` — append-only chronological log
7. **If you need deeper context** on rules/decisions/plans:
   - `f:\stadios\docs\DECISIONS.md` — Architecture Decision Records
   - `f:\stadios\docs\PROJECT_SHIFT\` — Full project pivot documentation (read all parts)
   - `f:\stadios\docs\NAVIGATION_ENGINE_ARCHITECTURE\` — Complete implementation blueprint (read all chapters)
   - `f:\stadios\docs\checkpoint.py` — **Persistence engine** (run this, don't edit docs by hand)

---

## Architecture (memorize this)

```
User → Frontend (Next.js + R3F Digital Twin) → API (FastAPI) → Orchestrator
                                                                  │
                                                       ┌──────────┼──────────┐
                                                       ▼          ▼          ▼
                                                 Intent      Provider     Cache/
                                                 Classifier  Factory      Fallback
                                                       │          │          │
                                                       ▼          ▼          ▼
                                                 Prompt     DeepSeek    Pre-computed
                                                 Templates  / Gemini    Responses
                                                                  │
                                                                  ▼
                                                            Validated
                                                            Response
```

### 5 Independent Systems

| System | Responsibility |
|---|---|
| **Digital Twin** | Visualization only — never computes routes or reasoning |
| **Navigation Graph** | Mathematical representation (physical + operational + semantic + intent layers) |
| **Simulation Engine** | Live operational state (congestion, queues, parking, event phase) |
| **AI Orchestrator** | Reasoning only — explains, predicts, compares; never computes shortest paths |
| **Frontend Experience** | Interaction, animation, camera, rendering; never performs routing |

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js 16, TypeScript, TailwindCSS v4, Three.js, React Three Fiber, Zustand |
| Backend | FastAPI, Python 3.11+, Pydantic v2, python-jose (JWT) |
| AI | DeepSeek (default), Gemini (secondary) via provider abstraction |
| Stadium | Procedural Python generator from YAML blueprint |
| Storage | In-memory simulation state, JSON files (no DB) |
| Auth | Mock OTP (demo code: `123456`), JWT, RBAC (Fan/Volunteer/Operations) |
| Deploy | Vercel (frontend), Render (backend) |

---

## Repo Structure

```
f:\stadios\
├── frontend/          # Next.js 16 app with R3F Digital Twin
│   └── features/
│       ├── digital-twin/  # 3D stadium components
│       ├── navigation/    # Route display, path animation
│       ├── auth/          # Login, OTP, protected routes
│       └── ai-card/       # Explainability UI
├── backend/           # FastAPI app
│   └── app/
│       ├── auth/          # OTP + JWT service
│       ├── graph/         # Multi-layer navigation graph engine
│       └── routes/        # API route handlers
├── stadium/           # Stadium generation (NEW)
│   ├── blueprint/         # YAML stadium config
│   ├── generator/         # Procedural geometry generator
│   └── metadata/          # Unified data models
├── simulation/        # Simulation engine
├── agents/            # AI agent logic + providers
├── prompts/           # Versioned prompt templates
├── schemas/           # Pydantic models + TS types
├── packages/          # Project-local dependency cache
├── docs/
│   ├── SESSION_CONTEXT.md  # ← READ IMMEDIATELY after BOOTSTRAP
│   ├── PROJECT_STATE.md    # Single source of truth
│   ├── BUILD_HISTORY.md    # Append-only chronological log
│   ├── DECISIONS.md        # Architecture Decision Records
│   ├── TODO.md             # Active tasks
│   ├── ARCHITECTURE.md     # System architecture
│   ├── checkpoint.py       # Persistence engine (run this)
│   ├── PROJECT_SHIFT/      # Full project pivot docs
│   ├── NAVIGATION_ENGINE_ARCHITECTURE/  # Implementation blueprint
│   └── planning/           # Legacy plans
└── BOOTSTRAP.md       # ← YOU ARE HERE
```

---

## Key Rules (never violate these)

1. **Navigation is the Product.** Everything else supports navigation.
2. **LLMs interpret state, never own it.** Simulation → Backend → Frontend.
3. **Structured output only.** No free-text parsing from LLMs.
4. **No scope creep.** If not in current phase's acceptance criteria, defer it.
5. **Main branch = demo-ready.** No broken pages, no TODO comments, no placeholder buttons.
6. **Backend owns truth.** Frontend never fabricates operational state.
7. **AI owns reasoning.** Deterministic systems compute; AI explains.
8. **Mobile first.** Every feature works on mobile portrait, one-handed.
9. **Cache/fallback for demo paths.** The rehearsed demo never depends on a live API call succeeding.
10. **Every phase ends deployable.** No broken builds, no placeholder pages.

---

## Demo Scenario (the product story)

Visitor arrives → AI recommends parking → AI recommends gate → AI explains why → conditions change → AI reroutes → visitor reaches seat → visitor diverts to food/restroom → route recalculates → match ends → AI predicts optimal exit → visitor leaves

Every step must include: **reasoning + context + recommendation**.

---

## Auto-Compaction Protocol (MANDATORY)

> **Context preservation is critical.** AI sessions have finite context windows. This protocol ensures no knowledge is lost.

### What is compaction?
Compaction generates `docs/SESSION_CONTEXT.md` — a single-file snapshot containing current phase, active tasks, blockers, architecture state, key files, and handoff notes. A new agent reads this first (after BOOTSTRAP.md) to resume in under 5 minutes.

### When to compact (automatic triggers)
The agent MUST run compaction in ALL of these scenarios:

- **Context reaches ~85-90% utilization** — compact immediately, continue working
- **Before ending any coding session** — this is non-optional
- **Before any major architecture change** — save state before modifying
- **Before switching implementation phases** — phase boundaries require a fresh context
- **At the end of every completed phase** — final handoff for the next phase

### How to compact

```powershell
python docs/checkpoint.py --action compact
```

This auto-detects session number, phase, scans the repository, and regenerates `docs/SESSION_CONTEXT.md`. No flags needed for basic usage.

For a richer snapshot (with change descriptions):

```powershell
python docs/checkpoint.py --action compact `
    --changes "Feature A implemented; Bug B fixed; Folder C created" `
    --blockers "None" --next "Start next task"
```

---

## Session Protocol

### Starting a session:
1. Read this file (BOOTSTRAP.md)
2. Read `docs/SESSION_CONTEXT.md` — compacted resume context (may contain stale info, verify against PROJECT_STATE)
3. Read `docs/PROJECT_STATE.md` — single source of truth
4. Read `docs/TODO.md` — active tasks
5. Read `docs/ARCHITECTURE.md` — system architecture
6. Read `docs/BUILD_HISTORY.md` — latest activity
7. Pick up where the last session left off

### During a session:
- Work on tasks for the active phase
- Follow acceptance criteria as pass/fail gates
- Log decisions in `docs/DECISIONS.md` (ADR format)
- **Auto-compact at ~85% context, before architecture changes, before phase switches**
- Run `python docs/checkpoint.py --action compact` to save state

### Ending a session (MANDATORY):
1. Run full milestone checkpoint:
   ```powershell
   python docs/checkpoint.py --action milestone `
       --session NNN --phase "Phase X — Name" `
       --changes "Feature A implemented; Bug B fixed" `
       --decisions "Decision description" `
       --blockers "None" --next "Next task" `
       --completed-todo "Task 1; Task 2" `
       --added-todo "New task"
   ```
2. **Run compaction** (non-optional):
   ```powershell
   python docs/checkpoint.py --action compact
   ```
3. The next agent will read SESSION_CONTEXT.md and resume seamlessly.

### Phase completion protocol:
1. Update `docs/PROJECT_STATE.md` (via checkpoint.py)
2. Update `docs/BUILD_HISTORY.md` (via checkpoint.py)
3. Update `docs/TODO.md` — mark all completed tasks
4. Update `docs/DECISIONS.md` if architecture changed
5. **Regenerate `docs/SESSION_CONTEXT.md`** — `python docs/checkpoint.py --action compact`
6. Only then consider the phase complete

---

## Competition Deliverables (don't forget these)

- [ ] Live deployed application (Vercel + Render)
- [ ] GitHub repository (public)
- [ ] Architecture diagram
- [ ] README (explicitly states what's stubbed vs real)
- [ ] Technical blog post (Build-in-Public narrative — **scored**)
- [ ] LinkedIn post (Build-in-Public — **scored**)
- [ ] Demo video
- [ ] Presentation
