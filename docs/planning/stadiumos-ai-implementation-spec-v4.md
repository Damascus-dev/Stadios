# StadiumOS AI — Implementation Specification (v4)
**Agent Task-Loop Spec: Goal / Result Parameters per Phase**

> Read order: v2 (Build Plan) → v3 (Implementation Constitution) → **this document**.
> This is the "Implementation Specification (v4)" referenced at the end of v3, scoped specifically to give an executing agent an unambiguous **Goal** and a binary-checkable **Result** for every task, so progress can be self-validated without human judgment calls mid-loop.

---

## 0. How the Agent Uses This Document

Every task below has exactly three fields:

- **Goal** — one sentence: the intent. Not instructions, not a how-to.
- **Result Parameters** — a checklist. Every item must be objectively true (pass/fail, not "looks good"). A task is not done until every box passes.
- **Non-Goals** — explicit adjacent things NOT to build in this task, even if they seem like a natural extension. This is the scope-creep guardrail, applied at the moment of temptation rather than after the fact.

### Agent-in-Loop Iteration Protocol (applies to every task in this document)

1. Read the task's Goal and Result Parameters before writing anything.
2. Implement the smallest version that could satisfy the Result Parameters.
3. Self-validate: check every Result Parameter individually. Partial pass = fail. There is no "mostly done."
4. If any parameter fails: fix only what failed. Do not touch unrelated code, do not add anything from Non-Goals, do not "improve while you're in there."
5. **Iteration cap: 3 attempts per task.** If Result Parameters still don't fully pass after 3 attempts, STOP. Do not ship a hacky pass. Log the blocker (see Decision Log template) and flag for human/change-control review per v3 §16 rather than silently expanding scope or lowering the bar.
6. If satisfying a Result Parameter would require touching an Architecture Invariant (v3 §3) or adding a dependency/feature not listed in this task — that is a change-control event, not an implementation detail. Stop and flag it; do not resolve it unilaterally.
7. Before moving to the next task in the same phase, re-check the Result Parameters of the *previous* task in that phase still pass (regression check — see Cross-Phase Regression Gate below). A new task must never silently break a prior one.
8. Mark the task complete only when it also satisfies v3 §4 (Definition of Done) in full: backend implemented, frontend integrated, error handling exists, manually tested, included in demo flow if applicable, documented, reviewed, no known regressions.
9. Any deviation, blocker, or dropped idea gets one line in the Decision Log — this becomes blog/README material later (v3 §13), so write it in plain language, not just a commit hash.

### Bug Budget Rule
Zero known regressions may persist across a phase boundary. If a fix in one task breaks something validated in an earlier task, that is not acceptable collateral — it must be resolved before the phase is marked complete.

### No-Extra-Features Rule
If, while implementing, an addition suggests itself that isn't in this task's Result Parameters — do not build it. Write it in `/docs/deferred_ideas.md` with one line of context and move on. Every unplanned feature is a complexity-budget violation (v3 §6) until explicitly scored and approved.

---

## Phase 1 — Day 1: Research & Architecture Lock (No Code)

**Phase Goal:** Every downstream decision has a written, agreed answer before a single line of implementation code is written.

**1.1 — Antigravity Workflow Verification** *(blocking — do this first)*
- **Goal:** Determine exactly how Google Antigravity expects to be used, and whether the v2 provisional stack (Next.js/FastAPI/Gemini/SQLite/Vercel-Render) is compatible with it.
- **Result Parameters:**
  - ✓ A written answer exists (in `/docs/antigravity_compatibility.md`) stating: how Antigravity ingests prompts, what artifacts it produces, and whether it orchestrates against an existing repo or generates one itself
  - ✓ An explicit compatibility verdict is recorded: COMPATIBLE / COMPATIBLE WITH CHANGES / INCOMPATIBLE
  - ✓ If not fully compatible, the specific stack changes required are listed with an effort estimate
- **Non-Goals:** Do not start writing application code until this task passes. Do not guess and proceed silently.

**1.2 — Persona & Requirements Lock**
- **Goal:** Freeze the 6 personas and their needs so no persona work shifts mid-build.
- **Result Parameters:**
  - ✓ `/docs/personas.md` lists Fan, Volunteer, Security, Medical Staff, Operations Manager, Executive with needs, each need traced to a specific agent/module from v2
  - ✓ Every capability area (Navigation, Crowd Mgmt, Accessibility, Transportation, Sustainability, Multilingual, Operational Intelligence, Real-time Decision Support) is mapped to at least one persona need
- **Non-Goals:** No new personas beyond the 6 already defined in v2.

**1.3 — Architecture Diagram Lock**
- **Goal:** Freeze the architecture flow from v2 as the single source-of-truth diagram.
- **Result Parameters:**
  - ✓ `/docs/architecture.png` (or `.svg`) exists showing: Intent Detection → Planner → Agent Selection → Context Retrieval → Prompt Construction → Gemini (structured output) → Cache/Fallback Layer → Structured Output → Frontend
  - ✓ Diagram explicitly marks which layer is the Source of Truth (per v3 §7: Simulation → Backend → Frontend; LLMs interpret, never own state)
- **Non-Goals:** No new orchestrators, no additional layers beyond what v2/v3 specify.

**1.4 — Wireframes**
- **Goal:** Lock the screen inventory so Day 2 has no open design questions.
- **Result Parameters:**
  - ✓ Wireframe exists for: Landing, Dashboard (with Transportation + Sustainability tiles), Navigation page, Chat/interaction UI, Alerts panel
  - ✓ Every wireframed screen maps to something that will actually appear in the Demo Flow — no orphan screens
- **Non-Goals:** No settings pages, no auth/login screens, no admin panels (v3 §17 Kill List).

---

## Phase 2 — Day 2: Frontend Shell (Mocked Data Only)

**Phase Goal:** Every screen from Day 1's wireframes exists and renders with mock data. No backend, no AI.

**2.1 — Landing + Dashboard Shell**
- **Goal:** Dashboard renders with all required cards using hardcoded mock data.
- **Result Parameters:**
  - ✓ Dashboard shows: stadium health, crowd heat, volunteer usage, incident count, active alerts, AI recommendations, Transportation tile, Sustainability tile — all 8 elements present
  - ✓ Page loads with zero console errors
  - ✓ Responsive at demo-relevant viewport (laptop screen-share resolution)
- **Non-Goals:** No live data wiring yet. No animations beyond basic transitions.

**2.2 — Navigation Page Shell**
- **Goal:** Navigation UI renders a map with a mock route.
- **Result Parameters:**
  - ✓ Map component (Leaflet/Google Maps) renders with a hardcoded start/end pin and a drawn route line
  - ✓ ETA and "suggested alternative" UI elements are present (static text is fine at this stage)
- **Non-Goals:** No real routing logic yet.

**2.3 — Chat/Interaction UI + Alerts Panel**
- **Goal:** Chat interface and alerts panel render and accept input, with mocked responses.
- **Result Parameters:**
  - ✓ Chat UI accepts text input and displays a hardcoded response on submit
  - ✓ Alerts panel renders a static list of 3+ mock alerts with severity styling
- **Non-Goals:** No LLM wiring yet.

---

## Phase 3 — Day 3: Backend Skeleton (Fake Data, No AI)

**Phase Goal:** API routes exist and return structured fake data; frontend can be pointed at them instead of hardcoded mocks.

**3.1 — API Route Scaffolding**
- **Goal:** FastAPI app exposes routes for dashboard, navigation, agents, and alerts, each returning static JSON.
- **Result Parameters:**
  - ✓ `/api/dashboard`, `/api/navigation`, `/api/alerts`, `/api/agents/{navigation|operations|accessibility}` all return HTTP 200 with valid JSON matching the schemas defined in `/schemas`
  - ✓ Frontend from Phase 2 successfully fetches from these routes instead of hardcoded data, with no visual regression
- **Non-Goals:** No database yet if not needed for fake data — flat JSON files are sufficient. No auth headers, no rate limiting.

**3.2 — Schema Definitions**
- **Goal:** Every API contract has a validated schema before any real logic is built against it.
- **Result Parameters:**
  - ✓ `/schemas` contains a schema file per route (Pydantic models backend-side; matching TypeScript types frontend-side)
  - ✓ A schema validation test exists and passes for each route's fake response
- **Non-Goals:** No schema for features not in MVP scope.

---

## Phase 4 — Day 4: AI Orchestrator

**Phase Goal:** The intent → planner → agent-selection → prompt-construction → structured-output pipeline works end-to-end on at least one trivial query, with real Gemini calls.

**4.1 — Intent Detection**
- **Goal:** Given a user query, correctly classify which agent (Navigation/Operations/Accessibility) should handle it.
- **Result Parameters:**
  - ✓ 10 test queries (at least 3 per agent type) are classified correctly by the intent detector
  - ✓ Ambiguous/out-of-scope queries return a defined fallback (not a crash, not a guess dressed as confidence)
- **Non-Goals:** No multi-intent handling (one query → one agent) in this phase.

**4.2 — Prompt Construction + Structured Output Contract**
- **Goal:** Every agent call goes through a versioned prompt template and returns schema-validated structured output — never free-text parsing.
- **Result Parameters:**
  - ✓ `/prompts/navigation_v1.md`, `/prompts/operations_v1.md`, `/prompts/accessibility_v1.md`, `/prompts/planner_v1.md`, `/prompts/formatter_v1.md` exist and are the only files referenced by code (no inline prompt strings)
  - ✓ Gemini is called with function calling / JSON schema enforcement, not asked to "return JSON" in free text
  - ✓ A schema validation step rejects and retries on malformed output (max 1 retry, then falls back — see 4.3)
- **Non-Goals:** No prompt A/B testing infrastructure. No prompt admin UI.

**4.3 — Cache/Fallback Layer**
- **Goal:** The demo's rehearsed query path never depends on a live Gemini call succeeding.
- **Result Parameters:**
  - ✓ Pre-computed responses exist for the exact queries used in the Demo Flow's primary scenario and both backup scenarios
  - ✓ A forced-failure test (mock a Gemini timeout) confirms the app falls back to a cached response without a visible error to the user
- **Non-Goals:** No general-purpose caching layer for arbitrary queries — only the rehearsed demo paths need this guarantee.

---

## Phase 5 — Day 5: Navigation Agent

**Phase Goal:** Navigation Agent meets its full acceptance criteria from v3 §5.

**5.1 — Route Generation**
- **Goal:** Given start/destination, agent returns a route.
- **Result Parameters:**
  - ✓ Destination selection triggers a real (not hardcoded) route generation call
  - ✓ Route generated and rendered on the map component from Phase 2
- **Non-Goals:** No turn-by-turn walking directions beyond what a route line + ETA requires.

**5.2 — Congestion & Accessibility-Aware Routing**
- **Goal:** Route changes based on simulated congestion and accessibility preference.
- **Result Parameters:**
  - ✓ Feeding a high-congestion simulation state into the agent changes the suggested route (verified by comparing two runs with different congestion inputs)
  - ✓ Toggling an accessibility preference (e.g., wheelchair) changes the route or explicitly confirms the same route is accessible
  - ✓ ETA is displayed and updates when the route changes
  - ✓ Cached fallback (from 4.3) is available for this agent specifically
- **Non-Goals:** No real-world traffic API integration — simulation-driven only.

---

## Phase 6 — Day 6: Operations Agent (+ Transportation/Sustainability Signals)

**Phase Goal:** Operations Agent predicts issues and produces Transportation/Sustainability outputs as line items, not new modules.

**6.1 — Crowd Density Prediction**
- **Goal:** Agent predicts congestion risk from simulation feed.
- **Result Parameters:**
  - ✓ Feeding a simulated crowd-density spike produces an alert/prediction output within the expected schema
  - ✓ Prediction includes a plain-language explanation (AI reasoning surface, per v3 §8) alongside any numeric output
- **Non-Goals:** No custom ML model training — reasoning over simulated data via Gemini only.

**6.2 — Incident Simulation + Volunteer Recommendations**
- **Goal:** Agent recommends volunteer reallocation given a simulated incident.
- **Result Parameters:**
  - ✓ A simulated incident event produces a volunteer-reallocation recommendation with a stated reason
- **Non-Goals:** No real volunteer scheduling system — recommendation text/UI only.

**6.3 — Transportation Signal (thin, reuses Operations Agent — no new agent)**
- **Goal:** Operations Agent additionally surfaces a shuttle/parking congestion signal from the same simulation feed.
- **Result Parameters:**
  - ✓ Transportation dashboard tile (from Phase 2) is wired to a real field in the Operations Agent's output schema
  - ✓ No new backend service, no new agent class was created to satisfy this — confirmed by code review against v3 §3 (architecture invariants)
- **Non-Goals:** No live transit API integration, no new orchestrator.

**6.4 — Sustainability Signal (thin, same pattern as 6.3)**
- **Goal:** Operations Agent surfaces a waste/energy-load signal correlated with crowd density.
- **Result Parameters:**
  - ✓ Sustainability dashboard tile is wired to a real field in the Operations Agent's output schema
  - ✓ No new agent/service created
- **Non-Goals:** Same as 6.3.

---

## Phase 7 — Day 7: Accessibility Agent

**Phase Goal:** Accessibility Agent meets full acceptance criteria including multilingual support.

**7.1 — Wheelchair & Visual/Hearing Support Routing**
- **Goal:** Agent produces accessible routing and instructions for stated accessibility needs.
- **Result Parameters:**
  - ✓ Selecting a wheelchair/vision/hearing preference produces a route or instruction set tailored to that need, visibly different from the default
- **Non-Goals:** No new UI pages beyond what's in the wireframe lock (Phase 1).

**7.2 — Multilingual Translation**
- **Goal:** Agent responses can be returned in at least 2 non-English languages relevant to World Cup attendees.
- **Result Parameters:**
  - ✓ A language toggle produces correctly schema'd output in the selected language for at least 2 languages beyond English
- **Non-Goals:** No full i18n of the entire UI chrome — translation applies to agent-generated content, not static UI labels.

**7.3 — Emergency Accessibility Routing**
- **Goal:** Agent handles an emergency accessibility request (e.g., accessible route during an active incident).
- **Result Parameters:**
  - ✓ Backup Demo Scenario A runs end-to-end using this agent and produces a valid, schema-conformant, cached-fallback-available response
- **Non-Goals:** None beyond what's already scoped.

---

## Phase 8 — Day 8: Executive Dashboard — *Feature Freeze on new UI begins per v3 §15*

**Phase Goal:** Dashboard is feature-complete and wired to real agent outputs. No new UI may be proposed after this day.

**8.1 — Live Dashboard Wiring**
- **Goal:** All 8 dashboard elements reflect real backend/agent state, not mock data.
- **Result Parameters:**
  - ✓ Every dashboard element from Task 2.1 now reads from a live API route (Phase 3) that reflects actual agent/simulation output
  - ✓ Dashboard refreshes on simulation state change without a manual page reload
- **Non-Goals:** No new dashboard elements beyond the 8 already locked. Any new-UI proposal from this point forward is rejected per v3 §15 (Day 8 = no new UI) unless it passes Change Control (v3 §16).

**8.2 — Recommendations Surface**
- **Goal:** AI recommendations from the Operations Agent appear in the dashboard's recommendation card.
- **Result Parameters:**
  - ✓ At least 3 distinct recommendation types can appear (crowd, volunteer, transportation/sustainability) depending on simulation state

---

## Phase 9 — Day 9: Simulation Engine — *Feature Freeze on new features begins per v3 §15*

**Phase Goal:** Primary scenario + 2 backup scenarios run reliably; cache/fallback layer is complete for all three.

**9.1 — Primary Scenario End-to-End**
- **Goal:** The full primary scenario (match begins → crowd increase → goal → rush → density spike → prediction → reroute → volunteer redirect → dashboard update) runs without manual intervention once triggered.
- **Result Parameters:**
  - ✓ Triggering the scenario produces, in order: crowd metric increase, Operations Agent alert, Navigation Agent reroute, dashboard update — all observable in the UI within the demo's expected time window
  - ✓ Runs successfully 3 times in a row with no manual fixes between runs

**9.2 — Backup Scenarios A & B**
- **Goal:** Both backup scenarios (accessibility request; transportation/exit bottleneck) run independently of the primary scenario.
- **Result Parameters:**
  - ✓ Scenario A triggers Accessibility Agent output correctly
  - ✓ Scenario B triggers Transportation signal (Task 6.3) correctly
  - ✓ Neither backup scenario depends on the primary scenario having run first

**9.3 — Offline/API-Failure Demo Mode**
- **Goal:** The full demo (primary + backups) can run with no internet/API access, using only cached responses.
- **Result Parameters:**
  - ✓ With network access disabled, all three scenarios still complete using the cache/fallback layer (Task 4.3) with no visible errors
- **Non-Goals:** This is not a general offline mode for arbitrary queries — demo paths only.

---

## Phase 10 — Day 10: Pitch Prep — *Polishing/documentation only, no features*

**Phase Goal:** All submission narrative materials have a complete draft.

**10.1 — Architecture Diagram + README**
- **Goal:** README and architecture diagram accurately reflect what was actually built (not the original plan).
- **Result Parameters:**
  - ✓ README explicitly states what's stubbed for demo vs. what a real deployment would need — don't let judges infer this
  - ✓ Architecture diagram matches the as-built system, not the Day 1 draft, if they diverged

**10.2 — Demo Flow Script**
- **Goal:** A written, timed script exists for the live demo including backup-scenario triggers.
- **Result Parameters:**
  - ✓ Script covers all 10 beats from the Demo Flow plus explicit cues for triggering Backup Scenarios A/B if asked
  - ✓ Full run-through completes in under 5 minutes (v3 §18)

**10.3 — Blog Post Draft #3 (near-final)**
- **Goal:** Blog post reflects the actual build journey, pulling from the Decision Log.
- **Result Parameters:**
  - ✓ Blog draft references at least 3 real entries from the Decision Log (architecture choices, tradeoffs, a blocker that was hit)
  - ✓ Draft is substantively different from Blog Draft #1/#2 — shows progression, not a copy-paste update

**10.4 — Judge Q&A Prep**
- **Goal:** Answers exist in advance for expected judge questions.
- **Result Parameters:**
  - ✓ `/docs/judge_questions.md` has a written answer for each of: Why Gemini? Why simulation? How scalable? How secure? Production deployment path? Estimated cost? Future roadmap? Limitations?

---

## Phase 11 — Day 11: Polish — *Bug fixes only, per v3 §15*

**Phase Goal:** Zero known regressions; performance and visual polish only.

**11.1 — Full Regression Pass**
- **Goal:** Every task's Result Parameters from Phases 1–10 are re-verified in one pass.
- **Result Parameters:**
  - ✓ A checklist run confirms all prior phases' Result Parameters still pass on the current build
  - ✓ Any failure found is fixed and re-verified before end of day — no fix is deferred past Day 11

**11.2 — Performance Pass**
- **Goal:** Dashboard refresh, routing response, and agent response times are acceptable for a live demo.
- **Result Parameters:**
  - ✓ Success metrics from v3 §19 (routing latency, incident response latency, prediction generation time, simulation update rate, volunteer allocation time, dashboard refresh time) are measured and logged, even if simulated

**Non-Goals for this entire phase:** No new features, no new UI, no new agents — enforced by v3 §15 Feature Freeze Policy without exception.

---

## Phase 12 — Day 12: Deployment — *Deployment and submission only, per v3 §15*

**Phase Goal:** Live deployment is stable and demo is recorded.

**12.1 — Live Deployment**
- **Goal:** Application is deployed and publicly reachable via a live preview link.
- **Result Parameters:**
  - ✓ Live URL loads the full app with no build errors
  - ✓ All 3 demo scenarios (primary + 2 backups) run successfully against the deployed instance, not just localhost

**12.2 — Demo Recording**
- **Goal:** A recorded demo video exists as submission backup in case the live demo has issues.
- **Result Parameters:**
  - ✓ Video covers the full scripted flow from Task 10.2, under the required length

**12.3 — Final QA**
- **Goal:** Nothing is broken at submission time.
- **Result Parameters:**
  - ✓ Every item in v3 §18 Demo Readiness checklist is individually confirmed true (30-second comprehension, under-5-minute demo, offline fallback, API failure handling, AI failure handling, README complete, architecture documented, blog complete, LinkedIn complete, live deployment working)

---

## Phase 13 — Day 13: Submission

**Phase Goal:** All required submission components are delivered before the platform deadline.

**13.1 — Submission Package**
- **Goal:** Submit code, live preview, blog post, and LinkedIn post together.
- **Result Parameters:**
  - ✓ GitHub repo is public and matches the deployed code
  - ✓ Live preview link works from a fresh browser session (not just the dev's own logged-in state)
  - ✓ Blog post is published (not just drafted) and linked in the submission
  - ✓ LinkedIn "Build-in-Public" post is published and linked in the submission
- **Non-Goals:** No last-minute feature additions — Day 13 is submission only, per v3 §15.

---

## Cross-Phase Regression Gate (run at the end of every phase, before starting the next)

- ✓ All Result Parameters from every task in the current phase still pass together (not just individually re-tested in isolation)
- ✓ No task in the current phase broke a Result Parameter from a previous phase
- ✓ No item from `/docs/deferred_ideas.md` was silently implemented without Change Control approval (v3 §16)
- ✓ Decision Log has at least one entry for the phase (even "no notable deviations" counts, but say so explicitly)

---

## Kill List Enforcement Checkpoints

At the end of Phase 8 (Day 8) and again at Phase 11 (Day 11): if any phase's Result Parameters are not passing and time is short, cut in this order (v3 §17), never touching Navigation, Operations, Accessibility, Simulation, Dashboard, or Demo Story:

1. Authentication (should not exist anyway per v2)
2. Notifications
3. Analytics
4. Settings
5. Admin Panels
6. Profile Pages
7. Fancy Animations
8. Secondary Dashboards

---

## Appendix A — Prompt Contract Template

```
/prompts/{agent}_v{n}.md

## Purpose
[one sentence]

## Input Schema
[reference to /schemas file]

## Output Schema
[reference to /schemas file — must match Gemini function-calling schema exactly]

## Constraints
- Never invent state not present in input context (v3 §7)
- Always return via structured output, never free text
- Fallback behavior if schema validation fails: [cached response ID / retry count]
```

## Appendix B — Repository Structure (per v3 §11)

```
/frontend
/backend
/simulation
/agents
/prompts
/schemas
/docs
  personas.md
  architecture.png
  antigravity_compatibility.md
  judge_questions.md
  deferred_ideas.md
  decision_log.md
/assets
/blog
/presentation
/tests
```

## Appendix C — Decision Log Entry Template

```
Date:
Decision:
Reason:
Alternatives considered:
Impact:
```
