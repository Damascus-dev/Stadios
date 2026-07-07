"""StadiumOS AI — Alerts Routes (mock data)"""

from __future__ import annotations

import sys, pathlib
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from schemas.alerts import Alert, AlertsResponse

router = APIRouter()

# ── Mutable mock store (in‑memory only) ──────────────────────────────
_NOW = datetime(2026, 7, 7, 19, 45, 0, tzinfo=timezone.utc)

_ALERTS: dict[str, Alert] = {
    a.id: a
    for a in [
        Alert(
            id="ALT-001",
            type="crowd",
            severity="critical",
            title="Gate A Overcrowding",
            message="North Stand Gate A at 92 % capacity. Crowd pressure building on turnstile bank 3. Immediate action recommended.",
            zone="North Stand Gate A",
            timestamp=_NOW - timedelta(minutes=4),
            acknowledged=False,
            recommended_action="Open auxiliary Gate A2 and deploy 6 additional crowd-management volunteers.",
        ),
        Alert(
            id="ALT-002",
            type="medical",
            severity="high",
            title="Heat Exhaustion Case",
            message="Fan in Section E-08, Row 22 showing signs of heat exhaustion. On-site paramedic responding. Ambient temp 34 °C.",
            zone="East Stand Lower Tier",
            timestamp=_NOW - timedelta(minutes=11),
            acknowledged=False,
            recommended_action="Ensure cooling station at East Concourse is fully stocked. Notify Medical Bay 1 for potential transfer.",
        ),
        Alert(
            id="ALT-003",
            type="infrastructure",
            severity="medium",
            title="Elevator B3 Offline",
            message="Elevator B3 on West Concourse non-operational — door sensor fault. Maintenance ETA 15 min.",
            zone="West Concourse",
            timestamp=_NOW - timedelta(minutes=22),
            acknowledged=True,
            recommended_action="Deploy portable ramp at Section W-12 for wheelchair access to Level 2.",
        ),
        Alert(
            id="ALT-004",
            type="security",
            severity="high",
            title="Unattended Bag Detected",
            message="Unattended backpack reported near Food Court North, Table 7. Security team dispatched for inspection.",
            zone="Food Court North",
            timestamp=_NOW - timedelta(minutes=8),
            acknowledged=False,
            recommended_action="Establish 15 m perimeter. Re-route foot traffic through South Concourse until cleared.",
        ),
        Alert(
            id="ALT-005",
            type="weather",
            severity="low",
            title="Light Rain Forecast",
            message="20 % chance of light rain starting at 21:30 local time. Retractable roof sections 4-6 on standby.",
            zone="Stadium-wide",
            timestamp=_NOW - timedelta(minutes=35),
            acknowledged=False,
            recommended_action="Pre-position roof closure sequence. Alert fans in open seating via PA system at T-15 min.",
        ),
    ]
}


def _build_response() -> AlertsResponse:
    alerts = sorted(_ALERTS.values(), key=lambda a: a.timestamp, reverse=True)
    return AlertsResponse(
        alerts=alerts,
        total=len(alerts),
        unacknowledged_count=sum(1 for a in alerts if not a.acknowledged),
    )


# ── Routes ───────────────────────────────────────────────────────────
@router.get("/", response_model=AlertsResponse)
async def get_alerts():
    """Return all active alerts sorted by most recent."""
    return _build_response()


@router.post("/{alert_id}/acknowledge", response_model=Alert)
async def acknowledge_alert(alert_id: str):
    """Mark an alert as acknowledged."""
    alert = _ALERTS.get(alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    alert.acknowledged = True
    return alert
