# StadiumOS Navigator — Explainable AI Navigation for Smart Stadiums

**PromptWars Virtual Challenge 4** — An AI-powered interactive stadium navigation platform with a 3D Digital Twin, real-time simulation, and explainable routing.

## Demo

[Live Frontend](https://stadiumos-navigator.vercel.app) | [API](https://stadiumos-api.onrender.com/api/health)

Demo login: use any email, OTP code `123456`, select role "Fan".

## Architecture

```
User → Frontend (Next.js + R3F Digital Twin) → API (FastAPI) → Orchestrator
                                                                   │
                                                        ┌──────────┼──────────┐
                                                        ▼          ▼          ▼
                                                  Intent      Provider     Cache/
                                                  Classifier  Factory      Fallback
                                                        │          │          │
                                                        ▼          ▼          ▼
                                                  Prompt     DeepSeek    Pre-computed
                                                  Templates  / Gemini    Responses
                                                                   │
                                                                   ▼
                                                             Validated
                                                             Response
```

### 5 Independent Systems

| System | Responsibility |
|---|---|
| **Digital Twin** | 3D visualization (React Three Fiber) — never computes routes |
| **Navigation Graph** | Multi-layer (Physical + Operational + Semantic + Intent) |
| **Simulation Engine** | Live state — congestion, queues, parking, match phases |
| **AI Orchestrator** | Reasoning, explanation, prediction — never computes paths |
| **Frontend** | Rendering, animation, touch, camera — no business logic |

### Tech Stack

- **Frontend**: Next.js 16, TypeScript, TailwindCSS v4, Three.js, React Three Fiber, Zustand
- **Backend**: FastAPI, Python 3.11+, Pydantic v2, JWT auth
- **AI**: DeepSeek (default), Gemini (secondary) via provider abstraction
- **Stadium**: Procedural Python generator from YAML blueprint (57,600 seats, 116 facilities, 525 graph edges)
- **Storage**: In-memory simulation state, JSON files
- **Auth**: Mock OTP (`123456`), JWT, RBAC (Fan/Volunteer/Operations)
- **Deploy**: Vercel (frontend), Render (backend)

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv && .venv\Scripts\activate
pip install -r ..\requirements.txt
copy ..\.env.example .env
# Set your API keys in .env
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

## Deployment

### Frontend (Vercel)

```bash
npx vercel --prod
```

Set environment variable: `NEXT_PUBLIC_API_URL=https://stadiumos-api.onrender.com`

### Backend (Render)

1. Create a **New Web Service** → connect your GitHub repo
2. **Root Directory**: leave **empty** (repo root) — the code imports from `agents/`, `schemas/`, etc. which are siblings of `backend/`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

Required env vars: `PYTHONPATH=.`, `JWT_SECRET`, `DEEPSEEK_API_KEY` or `GEMINI_API_KEY`.

## What's Stubbed vs Real

| Feature | Status |
|---|---|
| 3D Digital Twin (R3F) | Real — procedurally generated stadium |
| Navigation Graph (Dijkstra) | Real — congestion-aware multi-layer routing |
| AI Orchestrator (DeepSeek/Gemini) | Real — provider abstraction with fallback |
| Simulation Engine | Real — 12 match phases, 14 zones |
| Auth (OTP + JWT) | Real — demo OTP `123456` |
| Dashboard + Alerts | Real — live data from simulation |
| Real FIFA World Cup APIs | Stubbed — simulation generates match state |
| Real weather/traffic data | Stubbed — handled by simulation scenarios |

## Competition Deliverables

- [x] Live deployed application
- [x] GitHub repository
- [ ] Architecture diagram
- [ ] Technical blog post
- [ ] LinkedIn post
- [ ] Demo video
- [ ] Presentation

## License

MIT
