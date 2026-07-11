# StadiumOS AI — Agent Execution Contract

> Every AI coding agent working on this repository MUST follow this contract.
> Violations introduce architectural drift, inconsistent implementations, and deployment instability.

---

## Worker Agent Cycle

Every coding session follows this sequence. No steps may be skipped.

```
1. Read BOOTSTRAP.md
2. Read SESSION_CONTEXT.md
3. Read PROJECT_STATE.md
4. Read TODO.md
5. Understand current phase goal
6. Implement
7. Self-test (build, lint, start)
8. Fix errors
9. Update docs (via checkpoint.py)
10. Compact context (python docs/checkpoint.py --action compact)
11. Report completion
12. Wait for next instruction
```

Never continue automatically. Always report completion and wait.

---

## Forbidden Actions

| Action | Reason |
|---|---|
| ❌ Refactor unrelated files | Scope creep — stick to current phase |
| ❌ Add libraries without approval | Technology consistency |
| ❌ Break the build | Main branch = demo-ready |
| ❌ Leave TODO placeholders | No unfinished work in main |
| ❌ Fake implementations | Every visible feature must function |
| ❌ Change architecture silently | Must ask user first |
| ❌ Skip compaction | Context loss is not acceptable |

---

## Must Ask User Before

| Situation | Why |
|---|---|
| New npm/Python package needed | Avoid dependency bloat |
| API redesign / breaking changes | Contracts must stay stable |
| Folder restructure | Could break imports across files |
| >10 files affected by a change | Scope has expanded unexpectedly |
| New architecture introduced | Must be approved |
| Removing existing features | Could break demo paths |
| Deployment provider change | Vercel + Render confirmed |

---

## Required Completion Report

Every completed task MUST end with:

```markdown
### Completed
- ...

### Files Changed
- ...

### Tests
- Build: pass/fail
- Backend start: pass/fail
- Mobile verified: pass/fail

### Remaining
- ...

### Risks
- ...

### Next Suggested Task
- ...
```

---

## Phase Completion Checklist

A phase is complete ONLY when all of these pass:

1. Phase acceptance criteria satisfied
2. `npm run build` passes
3. Backend starts without errors
4. No console errors on any page
5. Mobile layout verified (portrait)
6. `PROJECT_STATE.md` updated
7. `BUILD_HISTORY.md` updated
8. `TODO.md` updated (completed items marked)
9. `DECISIONS.md` updated (if architecture changed)
10. `SESSION_CONTEXT.md` regenerated (`--action compact`)

Only then may the next phase begin.

---

## Success Metric

> The repository should always remain in a state where another AI agent can immediately continue development without reverse engineering previous work.

That is the primary objective of this architecture.
