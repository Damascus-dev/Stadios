# StadiumOS AI — Architecture Decision Records

> Every significant technical decision is documented here.
> See `docs/planning/appendix_c.md` §DECISIONS.md for the ADR format spec.

---

## ADR-001

**Date**: 2026-07-07

**Decision**: Confirmed v2 provisional stack (Next.js + TailwindCSS + FastAPI + Gemini + SQLite) as final stack.

**Reason**: Antigravity is a build tool (agentic coding assistant), not a runtime constraint — it orchestrates against existing repos and is stack-agnostic.

**Alternatives considered**: Waiting for deeper Antigravity investigation, switching to a Google-native stack (Firebase/Cloud Run).

**Status**: Accepted

---

## ADR-002

**Date**: 2026-07-07

**Decision**: Use dataclass simulation state instead of a database.

**Reason**: Simplicity per v3 constitution §8 — no DB schema, migrations, or connection management needed for a hackathon.

**Alternatives considered**: SQLite with SQLAlchemy, in-memory dict with no typing.

**Status**: Accepted

---

## ADR-003

**Date**: 2026-07-07

**Decision**: Build as a mobile-first PWA rather than a native app.

**Reason**: FIFA World Cup operations context — fans scan a QR code at the stadium gate. No app store friction, no install barrier, works offline via service worker cache.

**Alternatives considered**: React Native, Flutter, native iOS/Android.

**Status**: Accepted

---

## ADR-004

**Date**: 2026-07-07

**Decision**: Introduced provider abstraction layer for LLMs.

**Reason**: Support multiple runtime LLMs without orchestrator changes. Enables fallback when one provider is unavailable.

**Alternatives considered**: Hardcoded Gemini integration only.

**Status**: Accepted

---

## ADR-005

**Date**: 2026-07-07

**Decision**: Three-tier fallback architecture — Live AI → Cache → Rule Engine.

**Reason**: The rehearsed demo must never depend on a live API call succeeding. Each tier degrades gracefully.

**Alternatives considered**: Single-tier live AI only, live AI with hardcoded fallback.

**Status**: Accepted

---

## ADR-006

**Date**: 2026-07-07

**Decision**: LLM is an implementation detail — orchestration is the product.

**Reason**: The orchestrator pipeline (classify → build context → select prompt → validate → fallback) is the core engineering value. Provider SDK calls are isolated behind an abstract interface.

**Alternatives considered**: Direct provider SDK calls throughout the codebase.

**Status**: Accepted

---

## ADR-007

**Date**: 2026-07-07

**Decision**: Repository is the project's persistent memory — never conversation memory.

**Reason**: AI coding sessions have finite context windows. Every important engineering decision should exist as a document or code artifact, not only in conversation history.

**Alternatives considered**: Relying on agent context compaction, manual session notes only.

**Status**: Accepted

---

## ADR-008

**Date**: 2026-07-07

**Decision**: 5 canonical documents replace ad-hoc documentation.

**Reason**: Single source of truth reduces confusion and ensures new agents can onboard in minutes.

**Documents**:
- `PROJECT_STATE.md` — current phase, blockers, resume context
- `BUILD_HISTORY.md` — append-only chronological log
- `DECISIONS.md` — architecture decision records (this file)
- `TODO.md` — active work tracking
- `ARCHITECTURE.md` — system architecture reference

**Status**: Accepted

## ADR-009

**Date**: 2026-07-11

**Decision**: Navigation-First pivot: Project shifts from multi-agent stadium OS to Explainable AI Navigation Platform (StadiumOS Navigator). Navigation becomes the flagship product. 3D Digital Twin (React Three Fiber) becomes primary interface. Multi-layer navigation graph architecture (Physical + Operational + Semantic + Intent). New phased roadmap: Foundation → Auth → Digital Twin → Navigation Engine → Explainable AI → Deployment.

**Status**: Accepted

---
