"""StadiumOS AI — Unified Data Models for Stadium Generation

Canonical data structures shared across Blueprint, Generator, Backend, and AI layers.
Every entity has exactly one owner. No duplicated state. Single source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class NodeType(str, Enum):
    PARKING = "parking"
    GATE = "gate"
    SECURITY = "security"
    LIFT = "lift"
    ESCALATOR = "escalator"
    STAIR = "stair"
    CONCOURSE = "concourse"
    FOOD = "food"
    RESTROOM = "restroom"
    MEDICAL = "medical"
    PRAYER = "prayer"
    CHARGING = "charging"
    MERCHANDISE = "merchandise"
    VOLUNTEER = "volunteer"
    EXIT = "exit"
    SEAT = "seat"
    SECTION = "section"
    ROW = "row"


class FacilityType(str, Enum):
    FOOD = "food"
    RESTROOM = "restroom"
    MEDICAL = "medical"
    CHARGING = "charging"
    PRAYER = "prayer"
    MERCHANDISE = "merchandise"
    VOLUNTEER = "volunteer"
    INFORMATION = "information"


class IntentType(str, Enum):
    REACH_SEAT = "reach_seat"
    EXIT_STADIUM = "exit_stadium"
    RETURN_PARKING = "return_parking"
    FOOD = "food"
    RESTROOM = "restroom"
    MEDICAL = "medical"
    MERCHANDISE = "merchandise"
    CHARGING = "charging"
    PRAYER = "prayer"
    INFORMATION = "information"
    EVACUATION = "evacuation"
    EMERGENCY = "emergency"


@dataclass
class Position:
    x: float
    y: float
    z: float


@dataclass
class StadiumConfig:
    name: str
    origin: Position
    levels: list[LevelConfig]
    quadrants: list[str]
    sections_per_level: int
    rows_per_section: int
    seats_per_row: int
    parking_zones: int
    gates_primary: int
    gates_emergency: int


@dataclass
class LevelConfig:
    level: int
    elevation: float
    label: str


@dataclass
class Seat:
    id: str
    section: int
    row: int
    number: int
    position: Position
    accessible: bool
    reserved: bool = False
    occupied: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Facility:
    id: str
    type: FacilityType
    position: Position
    level: int
    quadrant: str
    capacity: int = 0
    occupancy: int = 0
    status: str = "open"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NavigationNode:
    id: str
    type: NodeType
    name: str
    position: Position
    level: int
    quadrant: str
    accessible: bool = True
    capacity: int = 0
    current_occupancy: int = 0
    estimated_delay: float = 0.0
    services: list[str] = field(default_factory=list)
    status: str = "open"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NavigationEdge:
    start_id: str
    end_id: str
    distance_m: float
    travel_time_s: float
    capacity: int = 100
    current_density: float = 0.0
    accessible: bool = True
    width_m: float = 2.0
    slope: float = 0.0
    emergency_route: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NavigationGraph:
    nodes: dict[str, NavigationNode] = field(default_factory=dict)
    edges: list[NavigationEdge] = field(default_factory=list)


@dataclass
class Route:
    route_id: str
    start_node_id: str
    destination_node_id: str
    waypoints: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    total_distance_m: float = 0.0
    total_duration_s: float = 0.0
    reason: str = ""
    confidence: float = 0.0
    alternatives: list[str] = field(default_factory=list)


@dataclass
class Intent:
    intent_type: IntentType
    priority: int
    status: str = "idle"  # idle | navigating | paused | completed
    destination_node_id: str = ""
    parent_intent: str | None = None


@dataclass
class CrowdState:
    zone_id: str
    density_pct: float
    prediction: str = ""
    confidence: float = 0.0


@dataclass
class ParkingZone:
    zone_id: str
    capacity: int
    occupied: int
    nearest_gate_id: str = ""

    @property
    def available(self) -> int:
        return self.capacity - self.occupied


@dataclass
class UserSession:
    user_id: str
    role: str  # fan | volunteer | operations
    current_node_id: str = ""
    intent: Intent | None = None
    route: Route | None = None
    preferences: dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    recommendation: str
    reason: str
    alternatives: list[str] = field(default_factory=list)
    confidence: float = 0.0
    warnings: list[str] = field(default_factory=list)
    eta: str = ""


@dataclass
class StadiumData:
    """Complete output of the procedural generator."""
    config: StadiumConfig | None = None
    seats: list[Seat] = field(default_factory=list)
    facilities: list[Facility] = field(default_factory=list)
    graph: NavigationGraph | None = None
    parking: list[ParkingZone] = field(default_factory=list)
    total_seats: int = 0
    generated_at: str = ""
