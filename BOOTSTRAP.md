# StadiumOS AI — Agent Bootstrap

> **READ THIS FILE FIRST.** This is the single-file entry point for any agent session working on this project.
> After reading this, read the phase tracker, then the latest build log, then start working.

---

## Project Identity

**StadiumOS AI** — An AI Operating System for managing FIFA World Cup 2026 stadium operations.
Built for **PromptWars Virtual Challenge 4** hackathon (12-day build + Day 13 submission).

---

## Read Order (mandatory)

1. **This file** — you're here
2. **Phase tracker** → `f:\stadios\docs\phase_tracker.md` — current phase, what's done, what's next
3. **Latest build log** → `f:\stadios\docs\build_logs\` — most recent session's work and decisions
4. **If you need deeper context** on architecture/rules/tasks:
   - `f:\stadios\docs\planning\stadiumos-ai-revised-plan-v2.md` — WHAT to build, architecture, timeline
   - `f:\stadios\docs\planning\stadiumos-v3.md` — HOW to make decisions, constraints, constitution
   - `f:\stadios\docs\planning\stadiumos-ai-implementation-spec-v4.md` — EXACT tasks with pass/fail criteria

---

## Architecture (memorize this)

```
User → Intent Detection → Planner → Agent Selection → Context Retrieval
     → Prompt Construction → Gemini (structured output) → Cache/Fallback → Frontend
```

- **3 Agents**: Navigation, Operations, Accessibility
- **2 Thin Tiles** (outputs of Operations Agent, NOT separate agents): Transportation, Sustainability
- **Source of Truth**: Simulation → Backend → Frontend. LLMs interpret state, never own it.
- **Structured output only** — Gemini via function calling / JSON schema. Never free-text parsing.
- **Cache/fallback layer** — demo paths always have pre-computed responses.

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js 15 (App Router), TypeScript, TailwindCSS, Framer Motion |
| Backend | FastAPI, Python, Pydantic |
| AI | Gemini, structured outputs, function calling |
| Storage | In-memory simulation state, JSON files (no DB) |
| Deploy | Vercel (frontend), Render (backend) |

---

## Repo Structure

```
f:\stadios\
├── frontend/          # Next.js 15 app
├── backend/           # FastAPI app
│   └── app/
│       ├── main.py    # Entry point
│       └── routes/    # API route handlers
├── simulation/        # Simulation engine (source of truth)
├── agents/            # AI agent logic
├── prompts/           # Versioned prompt templates (*_v1.md)
├── schemas/           # Pydantic models + TS types
├── docs/
│   ├── planning/      # v2, v3, v4 implementation plans
│   ├── build_logs/    # Per-session build logs
│   ├── phase_tracker.md  # ← CURRENT STATUS LIVES HERE
│   ├── personas.md
│   ├── decision_log.md
│   ├── deferred_ideas.md
│   └── judge_questions.md
├── assets/
├── blog/
├── presentation/
├── tests/
└── BOOTSTRAP.md       # ← YOU ARE HERE
```

---

## Key Rules (from v3 Constitution — never violate these)

1. **Demo first.** Working > ambitious.
2. **LLMs interpret state, never own it.** Simulation → Backend → Frontend.
3. **Structured output only.** No free-text parsing from Gemini.
4. **No scope creep.** If it's not in the current phase's Result Parameters, don't build it. Write it in `deferred_ideas.md`.
5. **Main branch = demo-ready.** No broken pages, no TODO comments, no placeholder buttons.
6. **3 agents only.** Navigation, Operations, Accessibility. Transportation + Sustainability are Operations outputs.
7. **Cache/fallback for demo paths.** The rehearsed demo must never depend on a live API call succeeding.

---

## Demo Scenarios (the product story)

**Primary**: Match begins → crowd ↑ → goal scored → rush to food court → density spike → Operations AI predicts congestion → Navigation reroutes → volunteers redirected → dashboard updates

**Backup A**: Wheelchair user needs accessible route during active congestion → Accessibility Agent

**Backup B**: Transportation/shuttle bottleneck at exit gates post-match → Operations Agent (Transportation signal)

---

## Session Protocol

### Starting a session:
1. Read this file
2. Read `docs/phase_tracker.md` to know current phase
3. Read the latest file in `docs/build_logs/` to know what happened last
4. Pick up where the last session left off

### During a session:
- Work on tasks for the active phase from v4 spec
- Follow the Result Parameters as pass/fail gates
- Log decisions in `docs/decision_log.md`
- Log deferred ideas in `docs/deferred_ideas.md`

### Ending a session:
1. **Create a build log** → `docs/build_logs/session_NNN.md` using this template:

```markdown
# Session NNN — [Brief Title]

| Field | Value |
|---|---|
| **Date** | YYYY-MM-DD |
| **Duration** | ~X min |
| **Phase** | Phase N — [Name] |

## What Was Done
- bullet list of completed work

## Decisions Made
- any architectural or design decisions

## What's In Progress
- unfinished work that should be continued

## Blockers
- anything blocking progress (or "None")
```

2. **Update phase tracker** → `docs/phase_tracker.md`:
   - Update the "Current Status" table (Active Phase, Day, Last Updated, Last Session, Build Health, Blockers)
   - Update the "Phase Completion Status" table (mark phases as ✅ DONE / 🔵 IN PROGRESS / ⬜ NOT STARTED)
   - Update "What's Been Built So Far" with new deliverables
   - Update "What Needs To Happen Next"

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
