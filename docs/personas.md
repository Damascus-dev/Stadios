# StadiumOS AI — Personas & Requirements

> Frozen per v4 Task 1.2. No new personas beyond these 6.

---

## 1. Fan
**Needs:**
- Navigate to seats, food courts, restrooms, exits efficiently → **Navigation Agent**
- Get real-time crowd-aware route alternatives → **Navigation Agent**
- Receive multilingual assistance → **Accessibility Agent**
- Understand transportation/shuttle options → **Operations Agent (Transportation signal)**
- Accessible routing for wheelchair/vision/hearing needs → **Accessibility Agent**

## 2. Volunteer
**Needs:**
- Know where to deploy based on crowd conditions → **Operations Agent**
- Receive reallocation recommendations during incidents → **Operations Agent**
- Navigate to assigned zones quickly → **Navigation Agent**
- Communicate with non-English-speaking attendees → **Accessibility Agent**

## 3. Security Staff
**Needs:**
- Monitor crowd density in real-time → **Operations Agent**
- Receive incident predictions before they happen → **Operations Agent**
- Access rapid response routing during emergencies → **Navigation Agent**
- Coordinate with operations dashboard → **Operations Agent (Dashboard)**

## 4. Medical Staff
**Needs:**
- Find fastest accessible routes to incidents → **Navigation Agent + Accessibility Agent**
- Receive emergency routing during active incidents → **Accessibility Agent (Emergency Routing)**
- View real-time crowd conditions that affect response times → **Operations Agent**

## 5. Operations Manager
**Needs:**
- Executive dashboard with stadium health overview → **Operations Agent (Dashboard)**
- Crowd density predictions and alerts → **Operations Agent**
- Volunteer allocation recommendations → **Operations Agent**
- Transportation congestion status → **Operations Agent (Transportation signal)**
- Sustainability/energy load monitoring → **Operations Agent (Sustainability signal)**
- AI-driven operational recommendations → **Operations Agent**

## 6. Executive
**Needs:**
- High-level metrics and KPIs → **Operations Agent (Dashboard)**
- Decision support recommendations → **Operations Agent (Real-time Decision Support)**
- Cross-domain operational visibility → **Operations Agent (Dashboard)**

---

## Capability Area Coverage Map

| Capability Area | Mapped Persona(s) | Agent/Module |
|---|---|---|
| Navigation | Fan, Volunteer, Security, Medical | Navigation Agent |
| Crowd Management | Security, Operations Manager | Operations Agent |
| Accessibility | Fan, Medical | Accessibility Agent |
| Transportation | Fan, Operations Manager | Operations Agent (Transportation signal) |
| Sustainability | Operations Manager, Executive | Operations Agent (Sustainability signal) |
| Multilingual Assistance | Fan, Volunteer | Accessibility Agent |
| Operational Intelligence | Operations Manager, Executive | Operations Agent |
| Real-time Decision Support | Security, Operations Manager, Executive | Operations Agent |

All 8 capability areas are mapped. All 6 personas have at least one traced need.
