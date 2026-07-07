"""StadiumOS AI — Shared Pydantic Schema Models"""

# Dashboard
from .dashboard import (
    StadiumHealth,
    CrowdZone,
    CrowdHeat,
    VolunteerAssignment,
    VolunteerStatus,
    SeverityBreakdown,
    IncidentCount,
    AlertSummary,
    ActiveAlerts,
    AIRecommendation,
    ExitCongestion,
    TransportationStatus,
    SustainabilityMetrics,
    DashboardResponse,
)

# Navigation
from .navigation import (
    NavigationRequest,
    RouteStep,
    StadiumZone,
    NavigationResponse,
)

# Alerts
from .alerts import Alert, AlertsResponse

# Agents
from .agents import AgentQuery, AgentResponse

__all__ = [
    # Dashboard
    "StadiumHealth",
    "CrowdZone",
    "CrowdHeat",
    "VolunteerAssignment",
    "VolunteerStatus",
    "SeverityBreakdown",
    "IncidentCount",
    "AlertSummary",
    "ActiveAlerts",
    "AIRecommendation",
    "ExitCongestion",
    "TransportationStatus",
    "SustainabilityMetrics",
    "DashboardResponse",
    # Navigation
    "NavigationRequest",
    "RouteStep",
    "StadiumZone",
    "NavigationResponse",
    # Alerts
    "Alert",
    "AlertsResponse",
    # Agents
    "AgentQuery",
    "AgentResponse",
]
