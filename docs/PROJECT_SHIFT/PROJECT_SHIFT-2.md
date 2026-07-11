# PROJECT_SHIFT.md (Part 2)

---

# 14. Engineering Constitution

This section defines how StadiumOS AI shall be engineered from this point forward.

Every implementation decision must satisfy the following principles.

If a future implementation violates these principles, it should be reconsidered before being merged into the repository.

---

## Principle 1

### Navigation is the Product.

Everything else supports navigation.

The project is no longer presented as an all-in-one stadium operating system.

Instead,

Navigation becomes the flagship experience.

Supporting systems exist only to make navigation more intelligent.

Examples

Crowd Analysis

↓

Improves route selection.

Parking Analytics

↓

Improves arrival planning.

Accessibility

↓

Improves inclusive routing.

Operations

↓

Produces navigation intelligence.

Volunteer Systems

↓

Improve assistance for lost visitors.

Every subsystem should ultimately answer:

> How does this improve navigation?

---

## Principle 2

### AI must reason.

AI should never produce unexplained recommendations.

Every AI response should include:

* Recommendation
* Reasoning
* Supporting evidence
* Alternative options
* Confidence
* Expected outcome

Example

Instead of

> Gate A

Return

Recommended Gate

Gate D

Reason

Current congestion at Gate A exceeds projected thresholds.

Expected Benefit

Reduce waiting time by approximately 5 minutes.

Confidence

94%

---

## Principle 3

### The Digital Twin becomes the application's core interface.

The 3D stadium is no longer an optional visualization.

It becomes the primary interaction model.

Every major navigation task begins inside the Digital Twin.

Examples

Select Parking

↓

Navigate to Gate

↓

Navigate to Seat

↓

Find Restroom

↓

Find Food

↓

Emergency Exit

↓

Return Route

↓

Exit Stadium

The map becomes the application's "home screen."

---

## Principle 4

### The backend owns reality.

The frontend visualizes reality.

No frontend component may invent operational state.

All crowd information,

gate occupancy,

parking availability,

facility status,

recommended routes,

must originate from backend services.

---

## Principle 5

### Every feature must remain mobile-first.

The primary experience is expected to work as a Progressive Web Application.

Desktop enhancements are welcome.

Desktop-only functionality is prohibited.

Every UI decision should first consider

portrait mobile usage.

---

# 15. Revised System Architecture

The architecture becomes:

User

↓

Authentication

↓

Role Verification

↓

Permission Middleware

↓

Navigation Experience

↓

Digital Twin

↓

Interaction Layer

↓

Navigation Engine

↓

AI Orchestrator

↓

Simulation Engine

↓

Provider Layer

↓

Response

↓

Frontend Rendering

---

Each layer owns one responsibility.

No layer should bypass another.

---

# 16. Revised Repository Direction

The repository remains modular.

Recommended ownership:

Frontend

Responsible for

* rendering
* interaction
* animations
* state visualization
* mobile responsiveness

Never performs routing calculations.

---

Backend

Responsible for

* simulation
* routing
* occupancy
* parking
* crowd prediction
* AI orchestration
* authentication
* authorization

Never performs visualization.

---

AI

Responsible only for reasoning.

AI should never calculate deterministic shortest paths.

Deterministic routing belongs to routing services.

AI explains,

prioritizes,

and adapts.

---

# 17. Authentication Strategy

The application is expected to be publicly deployed.

Unauthenticated access to protected dashboards is unacceptable.

The application shall implement Role-Based Access Control (RBAC).

Required roles

* Fan
* Volunteer
* Operations

Authentication Flow

Landing

↓

Choose Login

↓

OTP Verification

↓

JWT Issued

↓

Permission Middleware

↓

Role Dashboard

Authentication must be handled before dashboard access.

Frontend route hiding alone is insufficient.

Backend authorization remains the final authority.

---

# 18. Persona Strategy

Although the platform supports multiple personas,

the public demonstration prioritizes one.

Priority

Fan

Secondary

Volunteer

Tertiary

Operations

Presentation time should approximately follow:

Fan

80%

Volunteer

10%

Operations

10%

The backend remains shared.

---

# 19. Existing Components

The following completed work should be preserved.

Do NOT rebuild without explicit approval.

* AI Orchestrator
* Provider Abstraction
* Backend APIs
* Dashboard APIs
* Navigation Services
* Deterministic Routing
* Simulation Engine
* Operations Engine
* Documentation Framework

Future work extends these systems.

It does not replace them.

---

# 20. Current Project Review

Completed

✔ Backend foundation

✔ Frontend foundation

✔ AI orchestration

✔ Provider abstraction

✔ Navigation prototype

✔ Operations prototype

✔ Documentation framework

✔ Multi-agent architecture

Incomplete

✘ Digital Twin

✘ Interactive Stadium

✘ Seat Navigation

✘ Parking Navigation

✘ Indoor Multi-level Navigation

✘ Authentication

✘ RBAC

✘ Mobile Optimization

✘ Deployment Hardening

✘ Production Testing

These become the remaining milestones.

---

# 21. Development Philosophy

Every phase must satisfy four conditions before proceeding.

Functional

The feature works.

Reliable

No known breaking bugs remain.

Documented

Documentation updated.

Deployable

Application can still be deployed after the phase.

No phase may intentionally leave the repository in a broken state.

---

# 22. Definition of Done (Engineering)

A feature is complete only if:

Backend implemented.

Frontend implemented.

Mobile verified.

API documented.

Edge cases tested.

Errors handled.

Documentation updated.

Build passes.

Deployment succeeds.

If any requirement is missing,

the feature remains "In Progress."

---

# 23. Agent-Oriented Development

Every future coding session should work toward one finite milestone.

An implementation phase must never contain unrelated work.

Each phase must have:

Objective

Deliverables

Acceptance Criteria

Validation Steps

Documentation Updates

Rollback Strategy

If an implementation task grows beyond its original scope,

the responsible agent must stop and request clarification instead of making architectural assumptions.

This rule is mandatory.

---

# 24. Transition to Phase Roadmap

The following chapters define the new implementation roadmap.

Unlike previous iterations,

future phases are no longer organized by isolated AI agents.

Instead,

they are organized by complete vertical slices of the product.

Every phase ends with a fully deployable application.

Every phase leaves the repository in a releasable state.

No phase may introduce unfinished placeholder functionality.

The roadmap begins with foundational infrastructure,

then progresses toward the complete Digital Twin navigation experience.

**End of Part 2**
