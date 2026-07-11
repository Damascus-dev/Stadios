# NAVIGATION_ENGINE_ARCHITECTURE.md

## Chapter 6 — AI Navigation Engine

### AI Responsibility

AI NEVER computes paths.

Routing Engine computes.

AI reasons.

---

## AI Input

* User Position
* Destination
* Graph
* Crowd Density
* Parking State
* Match Phase
* Accessibility
* User Preferences

---

## AI Output

```json
{
  "recommended_route":"...",
  "reason":"...",
  "alternative":"...",
  "eta":"...",
  "confidence":0.96,
  "warnings":[],
  "next_stop":"..."
}
```

---

## AI Responsibilities

✓ Explain

✓ Predict

✓ Compare

✓ Suggest

✓ Re-route

✗ Graph Search

✗ Geometry

✗ Seat Generation

✗ Physics

---

## Explainability Format

Recommendation

↓

Reason

↓

Benefit

↓

Tradeoff

↓

Confidence

---

## Done

Every route contains reasoning.

No unexplained AI output.
