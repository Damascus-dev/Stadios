# NAVIGATION_ENGINE_ARCHITECTURE.md

## Chapter 14 — Agent Execution Contract

### Orchestrator (MASTER)

Responsible for

* Assigning phases
* Reviewing architecture
* Preventing scope creep
* Approving merges
* Updating roadmap

Never implements code.

---

## Worker Agent Cycle

```
Read Docs

↓

Read Current Phase

↓

Understand Goal

↓

Implement

↓

Self Test

↓

Fix Errors

↓

Update Docs

↓

Report Done

↓

Wait
```

Never continue automatically.

---

## Required Report

Every completed task MUST end with

### Completed

* ...

### Files Changed

* ...

### Tests

* ...

### Remaining

* ...

### Risks

* ...

### Next Suggested Task

* ...

---

## Forbidden

❌ Refactor unrelated files

❌ Add libraries without approval

❌ Break build

❌ Leave TODO placeholders

❌ Fake implementations

❌ Change architecture silently

---

## Ask User Before

* New package
* API redesign
* Folder restructure
* Breaking changes
* Removing features
* Deployment changes

---

## Success Metric

The repository should always remain in a state where another AI agent can immediately continue development without reverse engineering previous work.

That is the primary objective of this architecture.
