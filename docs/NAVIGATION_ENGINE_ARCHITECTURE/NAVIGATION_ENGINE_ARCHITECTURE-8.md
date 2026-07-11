# NAVIGATION_ENGINE_ARCHURE.md

## Chapter 8 — Agent Responsibilities

### Chief Orchestrator

Owns

* Architecture
* Phase Planning
* Reviews
* Merge Approval

Never codes directly.

---

### Backend Agent

Owns

* APIs
* Graph
* Auth
* AI
* Simulation

Never edits UI.

---

### Frontend Agent

Owns

* UI
* R3F
* Camera
* Animation
* Mobile UX

Never edits backend.

---

### AI Agent

Owns

* Prompts
* Reasoning
* Structured Output
* Evaluation

Never edits routing logic.

---

### Documentation Agent

Owns

* PROJECT_STATE
* TODO
* BUILD_HISTORY
* ARCHITECTURE
* DECISIONS

Updated after EVERY phase.

---

### QA Agent

Checks

* Build
* Mobile
* APIs
* Deployment
* Runtime Errors
* Console Errors

---

## Stop Conditions

Agent MUST ask user if

* New library needed
* Breaking API
* Folder restructure
* > 10 files affected
* New architecture proposed

No assumptions.

---

## Phase Completion

✔ Build passes

✔ Tests pass

✔ Mobile works

✔ Docs updated

✔ Deploy succeeds

Only then begin next phase.
