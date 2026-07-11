# PROJECT_SHIFT.md (Part 4)

---

# 27. AI Agent Operating Constitution

This repository is designed to be developed primarily through AI-assisted engineering.

Every AI coding agent is expected to follow this operating constitution before modifying any source code.

Failure to comply with these rules introduces architectural drift, inconsistent implementations, and deployment instability.

These rules are mandatory.

---

# Rule 1

## Never Assume

If required information is unavailable,

the agent must stop.

Do not invent.

Do not guess.

Do not silently change architecture.

Instead,

produce a concise clarification request.

Examples

Acceptable

"I need clarification regarding the parking layout before implementing routing."

Unacceptable

"I assumed the parking lot has six entrances."

---

# Rule 2

## One Phase at a Time

Every coding session belongs to exactly one implementation phase.

An agent may complete multiple tasks inside that phase,

but may never begin work belonging to a later milestone.

Example

Current Phase

Digital Twin Foundation

Allowed

Geometry

Navigation graph

Seat metadata

Camera

Lighting

Not Allowed

Authentication redesign

Dashboard redesign

Operations AI

Deployment optimization

Maintain strict phase boundaries.

---

# Rule 3

## Never Leave a Broken Repository

Before ending a session the repository must satisfy:

Frontend builds.

Backend builds.

No failing imports.

No runtime crashes.

No intentionally disabled components.

No placeholder implementations.

If a build breaks,

repair it before ending.

---

# Rule 4

## Every Task Must Have a Finish Line

Tasks such as

"Improve navigation"

are prohibited.

Instead,

tasks must have measurable completion.

Example

Create seat metadata schema.

Generate parking graph.

Implement camera controls.

Connect routing endpoint.

Each task should be objectively verifiable.

---

# Rule 5

## Preserve Existing Architecture

Unless explicitly instructed,

the following systems must remain untouched.

Provider abstraction

AI orchestrator

Backend contracts

Folder hierarchy

Documentation framework

Shared routing engine

Existing APIs

Never replace existing architecture to solve a local problem.

---

# Rule 6

## Never Refactor Outside Scope

If assigned

Seat highlighting

Only modify

Seat rendering

Selection

Highlighting

Avoid

Authentication

Provider abstraction

Dashboard

Operations

Navigation graph

Refactoring unrelated code is prohibited.

---

# Rule 7

## Stop Before Large Refactors

If implementation unexpectedly requires

more than

10 files

or

more than

3 architectural layers,

stop.

Produce a report explaining

why

the change expanded.

Request approval.

---

# Rule 8

## Backend Owns Truth

Frontend may never fabricate

occupancy

parking

crowd

navigation

recommendations

Every displayed state must originate from backend services.

Mock data is acceptable,

provided it originates from backend APIs.

---

# Rule 9

## AI Owns Reasoning

Deterministic systems own calculations.

AI owns interpretation.

Correct

Routing Engine

↓

Shortest Path

↓

AI

↓

Explain why

Incorrect

AI

↓

Invent geometry

↓

Guess path

↓

Frontend displays

---

# Rule 10

## Every Phase Ends Deployable

At the completion of every milestone,

the application must be deployable.

No milestone may knowingly introduce

broken builds

disabled routes

temporary hacks

unfinished pages

placeholder buttons

Every visible feature must function.

---

# Rule 11

## Mobile First

Every interface must be tested conceptually for

mobile portrait.

Desktop enhancements are optional.

Mobile usability is mandatory.

Navigation should remain usable with one hand.

Touch interactions always take priority over mouse interactions.

---

# Rule 12

## Performance Budget

The application targets Progressive Web App deployment.

Agents must continually optimize.

Avoid

Large textures

Massive geometry

Uncompressed assets

Heavy animations

Unnecessary dependencies

Performance is a feature.

---

# Rule 13

## Documentation Is Part of Development

A feature is incomplete until documentation is updated.

Mandatory updates include

PROJECT_STATE

BUILD_HISTORY

TODO

ARCHITECTURE

DECISIONS

Documentation should be committed alongside implementation.

Never postpone documentation.

---

# Rule 14

## Validate Before Completion

Every completed milestone requires validation.

Minimum checklist

Backend starts.

Frontend starts.

No console errors.

No runtime crashes.

Build succeeds.

Navigation functions.

Mobile layout verified.

API responses validated.

Only then may the milestone be marked complete.

---

# Rule 15

## Every New Capability Requires Acceptance Criteria

Agents should never consider work complete until explicit acceptance criteria are satisfied.

Example

Seat Navigation

Acceptance

Seat selectable.

Path rendered.

ETA displayed.

AI explanation visible.

Mobile interaction works.

Documentation updated.

---

# Rule 16

## Fail Gracefully

Unexpected situations should produce useful behavior.

Examples

Provider unavailable

↓

Fallback provider.

No route available

↓

Nearest reachable point.

Simulation unavailable

↓

Cached dataset.

Never expose stack traces to users.

---

# Rule 17

## Do Not Over-Engineer

Every implementation must justify its existence.

Questions every agent should ask

Does this improve the user experience?

Does this improve navigation?

Does this improve reliability?

Does this improve explainability?

If all answers are "No",

the feature should not be implemented.

---

# Rule 18

## Ask Before Introducing New Technology

Do not introduce

new rendering engines

new authentication systems

new databases

new mapping libraries

new deployment providers

without approval.

Technology consistency reduces maintenance complexity.

---

# Rule 19

## Keep Mock Data Replaceable

All synthetic datasets must be isolated.

Future real-world datasets should replace them without modifying business logic.

Never scatter mock data across components.

---

# Rule 20

## Preserve Demo Stability

The PromptWars demonstration takes priority over experimental features.

If a choice exists between

an impressive prototype

or

a reliable demonstration,

choose reliability.

Every demo interaction should work repeatedly under identical conditions.

---

# 28. Mandatory Agent Workflow

Every coding session shall follow this sequence.

1.

Read documentation.

↓

2.

Review current implementation phase.

↓

3.

Review previous build status.

↓

4.

Review assigned objective.

↓

5.

Implement.

↓

6.

Run validation.

↓

7.

Update documentation.

↓

8.

Verify deployment.

↓

9.

Commit.

↓

10.

Report completion.

No steps may be skipped.

---

# 29. Completion Standard

An implementation is considered complete only when all of the following are true.

The feature works.

The build succeeds.

The application deploys.

The documentation reflects reality.

No known regressions remain.

Acceptance criteria are satisfied.

The repository is ready for the next implementation phase.

Anything less remains "In Progress."

---

# 30. Final Directive

Every engineering decision should move StadiumOS Navigator toward one objective:

Deliver the most intuitive, explainable, production-quality AI navigation experience for a football stadium while preserving a clean architecture, predictable repository, and stable deployment pipeline.

Future development should optimize for depth, clarity, maintainability, and reliability rather than feature count.

This document is the governing constitution for all future development unless superseded by a newer approved revision.

**End of Part 4**
