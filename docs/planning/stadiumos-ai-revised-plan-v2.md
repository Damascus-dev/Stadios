# StadiumOS AI — Revised Build Plan (v2)
**PromptWars Virtual — Challenge 4: Smart Stadiums & Tournament Operations**

> This is a revision of the original 12-day context doc ("og version" / v1). Every section carries `⚠️ v1 issue` marks where the original plan was wrong, incomplete, or based on an unverified assumption, followed by the fix applied here. Sections with no mark were fine as-is and are carried over largely unchanged.

---

## 0. Competition Reality Check (new — not in v1 at all)

v1 was written as if this were a generic "bring your own stack" hackathon. It isn't. Verified from PromptWars' own site/FAQ:

- **Google Antigravity is mandatory.** All submissions must be built using Google Antigravity (Google's agentic, prompt-driven dev platform) — this is stated as a fairness requirement, not a suggestion.
- **Submission has two required parts:** (1) Technical — code + a live preview link, (2) Narrative — a technical blog post + a LinkedIn "Build-in-Public" post.
- **Timeline is fixed by the platform, not by us:** challenge drops Monday → 12-day build phase → Day 13 submission (code + live preview + blog/LinkedIn) → Day 14 evaluation.
- **Scoring is two-stage:** an automated AI evaluation engine drives the leaderboard for everyone; reaching the top 50 additionally requires manual expert review of functionality **and** blog depth **and** the LinkedIn post together.

> **⚠️ v1 issue:** The original doc's "Reverse Engineered Judge Priorities" section was a guess (generic hackathon heuristics — working product, AI integration, production thinking, live demo). It never accounted for the narrative/blog scoring track or the Antigravity requirement at all.
> **Fix:** Judging model below replaces the guessed one.

### Actual Judging Model (v2)
| Stage | What's scored | Weight in practice |
|---|---|---|
| AI evaluation (leaderboard) | Functionality of submission, presumably parsed from repo/live app | Everyone |
| Manual review (top 50 only) | App functionality + blog depth + LinkedIn post, together | Gatekeeps real prizes/credits |

**Open question to resolve before Day 1:** exactly how Antigravity expects you to work (agent orchestration model, what artifacts it produces, whether our planned stack — Next.js/FastAPI/Gemini — is even compatible with it). Flagging this as unverified rather than guessing — worth a short research pass before committing engineering time.

---

## 1. Objective (revised)

Build a hackathon-winning MVP for PromptWars Virtual Challenge 4 in the 12-day build window, **using Google Antigravity as the primary build tool**, optimizing for:

- Demo quality & live-preview stability
- AI usefulness (shown through structured, reliable outputs — not just a chat wrapper)
- Narrative depth (blog + LinkedIn, not an afterthought)
- Practicality / production framing
- Coverage of **all 8** stated capability areas, not just the convenient ones

> **⚠️ v1 issue:** Objective section only mentioned demo/AI/practicality/production/problem-solving/presentation — no mention of the narrative track, which is formally scored.
> **Fix:** Added narrative depth as a first-class objective.

---

## 2. Challenge & Context — unchanged

Same as v1: Smart Stadiums & Tournament Operations, FIFA World Cup 2026 context, must improve Navigation, Crowd Management, Accessibility, Transportation, Sustainability, Multilingual Assistance, Operational Intelligence, Real-time Decision Support.

---

## 3. Primary Users — unchanged

Fan, Volunteer, Security, Medical Staff, Operations Manager, Executives — v1's persona breakdown was solid and is kept as-is.

---

## 4. MVP Scope (revised)

**v1 scope:** Navigation AI, Operations AI, Accessibility AI.

> **⚠️ v1 issue:** The challenge explicitly names 8 required capability areas. v1's three modules cover Navigation, Crowd Management (via Operations), Accessibility, Multilingual (folded into Accessibility), Operational Intelligence, and Real-time Decision Support — but **Transportation** and **Sustainability** are never addressed anywhere in the doc. That's two of eight explicit judging-criteria items silently dropped, not consolidated.
> **Fix:** Add two *thin* modules — not new products, just tiles/agents that plug into the same three core agents so scope doesn't balloon.

**v2 scope — still ONE platform, five thin surfaces:**

1. **Navigation AI** *(unchanged from v1)*
2. **Operations AI** *(unchanged from v1)*
3. **Accessibility AI** *(unchanged from v1, multilingual stays folded in here)*
4. **Transportation tile (new, thin)** — shuttle/parking congestion prediction feeding into the same Operations Agent; reuses the crowd simulation data, no new backend.
5. **Sustainability tile (new, thin)** — a single dashboard card showing predicted waste/energy load correlated with crowd density, generated from the same simulation feed.

Neither new tile needs its own agent, database, or UI page — they're additional outputs of the existing Operations Agent and additional cards on the existing dashboard. This closes the coverage gap without adding new architecture.

---

## 5. High-Level Architecture (revised)

v1's flow was:
`Frontend → API Gateway → AI Orchestrator → Intent Classifier → Specialized Agent → Knowledge Layer → Simulation Layer → Response`

> **⚠️ v1 issue:** No fallback/failure path anywhere in the architecture. A live judged demo making live Gemini calls with no cache and no fallback is a single point of failure — LLM latency, rate limits, or malformed JSON output live on stage is the single most common way "impressive AI demos" die in front of judges. v1 also never states how structured output is enforced.
> **Fix:** Add a caching/fallback layer and mandate structured output enforcement (function calling / JSON schema), not free-text parsing.

**v2 flow:**

```
User
 → Intent Detection
 → Planner
 → Agent Selection
 → Context Retrieval
 → Prompt Construction
 → Gemini (structured output via function calling / JSON schema — never free-text parsing)
 → [Cache/Fallback Layer: pre-computed responses for the rehearsed demo path]
 → Structured Output
 → Frontend
```

The cache/fallback layer is invisible in normal operation (live calls succeed most of the time) but guarantees the rehearsed demo script never stalls on a live API hiccup in front of judges.

---

## 6. Agent Architecture — unchanged (Navigation, Operations, Accessibility)

v1's per-agent responsibilities/inputs/outputs were reasonable and are kept. Only addition: Operations Agent's output set now includes Transportation and Sustainability signals (see Section 4).

---

## 7. Simulation Layer (revised)

> **⚠️ v1 issue:** Only one scripted scenario (goal scored → crowd rushes → reroute). Fine as the primary demo spine, but fragile if a judge asks an off-script question live — there's no fallback interaction path.
> **Fix:** Keep the primary scenario as-is (it's a good demo beat), but script 2 backup scenarios so an off-script judge question doesn't break the demo.

**Primary scenario** *(unchanged from v1):* Match begins → crowd increases → goal scored → rush to food court → density spike → Operations AI predicts congestion → Navigation reroutes → volunteers redirected → dashboard updates.

**Backup scenario A (new):** Accessibility request mid-match (wheelchair user needs an alternate route around the congestion) — exercises the Accessibility Agent live.

**Backup scenario B (new):** A transportation/shuttle bottleneck at exit gates post-match — exercises the new Transportation tile.

---

## 8. Dashboard — unchanged, plus 2 new cards (Transportation, Sustainability) per Section 4.

---

## 9. Tech Stack (revised — flagged as pending verification)

> **⚠️ v1 issue:** v1 specified Next.js/TailwindCSS/shadcn/Framer Motion + FastAPI/Python + Gemini + SQLite/JSON + Vercel/Render, with zero mention of Google Antigravity, despite Antigravity being a mandatory build tool for the competition.
> **Fix:** Do not finalize this stack until we've confirmed how Antigravity expects to be used (does it generate the app from prompts inside its own environment, or does it orchestrate against an existing repo?). Everything below is provisional.

**Provisional stack (unchanged from v1, pending Antigravity compatibility check):**
- Frontend: Next.js, TailwindCSS, shadcn/ui, Framer Motion, Leaflet/Google Maps
- Backend: FastAPI, Python
- AI: Gemini, structured outputs, function calling
- Storage: SQLite, JSON
- Deployment: Vercel, Render

---

## 10. What NOT to Build — unchanged from v1

Auth, payments, notifications, role management, DB optimization, Kubernetes, Redis, RabbitMQ, custom ML training, vector DB, distributed systems. Still correct triage for 12 days.

---

## 11. Build Timeline (revised — 13 days, narrative baked in, not bolted on)

> **⚠️ v1 issue:** v1's 12-day plan allocated **zero days** to the blog/LinkedIn narrative, despite it being a formally scored part of submission (manual review weighs functionality + blog depth + LinkedIn post together). Worse, a "build in public" narrative can't be convincingly reconstructed on the last day — it needs to look like it happened *during* the build.
> **Fix:** Bake lightweight narrative checkpoints into the timeline itself, and correct the day count to match the platform's actual Day 13 submission deadline.

| Day | Build focus (mostly unchanged from v1) | Narrative checkpoint (new) |
|---|---|---|
| 1 | Research, personas, architecture, wireframes — no coding | — |
| 2 | Frontend: landing, dashboard, nav page, chat UI, alerts (mocked) | Blog post draft #1: "Why this problem" |
| 3 | Backend: API routes, fake data, no AI | — |
| 4 | AI Orchestrator: intent detection, agent routing, prompt builder, output formatter | LinkedIn post #1: early build-in-public screenshot |
| 5 | Navigation Agent: crowd-aware routing, accessibility routing, ETA | — |
| 6 | Operations Agent: crowd prediction, incident simulation, volunteer recs, **+ Transportation/Sustainability signals** | Blog post draft #2: architecture decisions |
| 7 | Accessibility Agent: wheelchair, translation, visual assistance, emergency routing | — |
| 8 | Executive Dashboard: charts, metrics, live updates, recommendations, **+ 2 new tiles** | LinkedIn post #2: mid-build demo clip |
| 9 | Simulation Engine: primary + 2 backup scenarios, cache/fallback layer for live demo | — |
| 10 | Pitch prep: architecture diagram, product story, demo flow, README | Blog post draft #3 (near-final) |
| 11 | Polish: animations, performance, bug fixes | — |
| 12 | Deployment, demo recording, final QA | Finalize blog post + LinkedIn "build-in-public" post |
| 13 | **Submission day (platform deadline):** code + live preview + blog + LinkedIn | Submit |

---

## 12. Demo Flow (revised)

v1's 10-beat flow is kept as the primary path. Addition: presenter should have Backup Scenario A and B (Section 7) ready to trigger on request, so an off-script judge question doesn't expose a single-path demo.

---

## 13. Success Criteria — unchanged from v1

"This could realistically assist operations during FIFA World Cup 2026" — still the right bar.

---

## 14. Deliverables (revised)

> **⚠️ v1 issue:** v1 listed deployment, GitHub repo, architecture diagram, README, presentation, demo video, live application — but never explicitly listed the blog post or LinkedIn post as deliverables, even though they're a required submission component.
> **Fix:** Added explicitly below.

- Live deployed application (Vercel/Render or Antigravity-native hosting, TBD)
- GitHub repository
- Architecture diagram
- README (explicitly framing what's stubbed for demo vs. what a real deployment would need — don't let judges infer this, state it)
- Technical blog post ("Build-in-Public" narrative — **required for scoring**)
- LinkedIn post ("Build-in-Public" — **required for scoring**)
- Demo video
- Presentation

---

## 15. Future Features (Not MVP) — unchanged from v1

Computer vision crowd estimation, drone integration, IoT sensor fusion, predictive maintenance, digital twin, emergency evacuation optimizer, ticket fraud detection, energy optimization (now partially pulled forward as the thin Sustainability tile), parking optimization (partially pulled forward as the thin Transportation tile), wearable integration, AR navigation.

---

## Summary of All Changes from v1

1. Added Antigravity as a mandatory build constraint (was entirely absent).
2. Added the real submission/scoring model (code + live preview + blog + LinkedIn, two-stage AI + manual review) — replaces guessed judge priorities.
3. Closed the Transportation + Sustainability coverage gap with two thin tiles, no new architecture.
4. Added a cache/fallback layer to the AI architecture to protect the live demo from LLM latency/failure.
5. Added two backup demo scenarios so the demo isn't a single fragile scripted path.
6. Rebuilt the timeline around baked-in narrative checkpoints instead of a Day-10 bolt-on, and corrected it to match the platform's actual Day 13 submission deadline.
7. Flagged the tech stack as provisional pending confirmation of how Antigravity actually expects to be used.
