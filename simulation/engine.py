# StadiumOS AI — Simulation Engine

"""
Simulation engine for StadiumOS AI.

The simulation drives all application state (v3 §7: Simulation → Backend → Frontend).
LLMs interpret this state — they never own or invent it.

Primary Scenario: Match begins → crowd increases → goal scored → rush to food court →
  density spike → Operations AI predicts congestion → Navigation reroutes →
  volunteers redirected → dashboard updates

Backup Scenario A: Wheelchair accessibility request during active congestion
Backup Scenario B: Transportation/shuttle bottleneck at exit gates post-match
"""

import json
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class ScenarioType(str, Enum):
    PRIMARY = "primary"
    BACKUP_A = "backup_a_accessibility"
    BACKUP_B = "backup_b_transportation"


class SimulationPhase(str, Enum):
    PRE_MATCH = "pre_match"
    MATCH_START = "match_start"
    FIRST_HALF = "first_half"
    GOAL_EVENT = "goal_event"
    CROWD_RUSH = "crowd_rush"
    CONGESTION_PEAK = "congestion_peak"
    REROUTING = "rerouting"
    STABILIZED = "stabilized"
    HALF_TIME = "half_time"
    SECOND_HALF = "second_half"
    MATCH_END = "match_end"
    EXIT_RUSH = "exit_rush"


@dataclass
class ZoneState:
    zone_id: str
    name: str
    capacity: int
    current_occupancy: int
    density_pct: float = 0.0
    risk_level: str = "low"
    trend: str = "stable"

    def update_density(self):
        self.density_pct = round((self.current_occupancy / self.capacity) * 100, 1) if self.capacity > 0 else 0.0
        if self.density_pct >= 90:
            self.risk_level = "critical"
        elif self.density_pct >= 75:
            self.risk_level = "high"
        elif self.density_pct >= 50:
            self.risk_level = "medium"
        else:
            self.risk_level = "low"


@dataclass
class IncidentState:
    incident_id: str
    type: str
    severity: str
    zone_id: str
    description: str
    active: bool = True
    timestamp: float = 0.0


@dataclass
class SimulationState:
    """The single source of truth for all application state."""
    phase: SimulationPhase = SimulationPhase.PRE_MATCH
    scenario: ScenarioType = ScenarioType.PRIMARY
    timestamp: float = 0.0
    match_minute: int = 0
    total_attendance: int = 0
    stadium_capacity: int = 82500  # MetLife Stadium
    zones: list[ZoneState] = field(default_factory=list)
    incidents: list[IncidentState] = field(default_factory=list)
    shuttle_load_pct: float = 0.0
    parking_capacity_pct: float = 0.0
    energy_load_kwh: float = 0.0
    waste_generation_kg: float = 0.0
    water_usage_liters: float = 0.0
    stadium_health_score: float = 100.0

    def to_dict(self) -> dict:
        return asdict(self)


# Default stadium zones for MetLife Stadium
DEFAULT_ZONES = [
    ZoneState("north_stand", "North Stand", 18000, 0),
    ZoneState("south_stand", "South Stand", 18000, 0),
    ZoneState("east_wing", "East Wing", 15000, 0),
    ZoneState("west_wing", "West Wing", 15000, 0),
    ZoneState("vip_lounge", "VIP Lounge West", 2500, 0),
    ZoneState("food_court_north", "North Food Court", 3000, 0),
    ZoneState("food_court_east", "East Wing Food Court", 3000, 0),
    ZoneState("main_concourse", "Main Concourse", 5000, 0),
    ZoneState("gate_a", "Gate A Entrance", 2000, 0),
    ZoneState("gate_b", "Gate B Entrance", 2000, 0),
    ZoneState("gate_c", "Gate C Entrance", 2000, 0),
    ZoneState("gate_d", "Gate D Entrance", 2000, 0),
    ZoneState("medical_station", "Medical Station Alpha", 200, 0),
    ZoneState("media_center", "Press & Media Center", 1500, 0),
]


class SimulationEngine:
    """
    Drives the simulation through phases, updating state at each tick.
    This is the ONLY source of truth — backend reads from here, LLMs interpret it.
    """

    def __init__(self):
        self.state = SimulationState(
            zones=[ZoneState(z.zone_id, z.name, z.capacity, z.current_occupancy) for z in DEFAULT_ZONES],
            timestamp=time.time(),
        )

    def reset(self, scenario: ScenarioType = ScenarioType.PRIMARY):
        """Reset simulation to initial state for a given scenario."""
        self.state = SimulationState(
            scenario=scenario,
            zones=[ZoneState(z.zone_id, z.name, z.capacity, 0) for z in DEFAULT_ZONES],
            timestamp=time.time(),
        )

    def advance_to_phase(self, phase: SimulationPhase):
        """Jump to a specific simulation phase (for demo triggering)."""
        self.state.phase = phase
        self._apply_phase_state(phase)

    def tick(self):
        """Advance simulation by one step."""
        phases = list(SimulationPhase)
        current_idx = phases.index(self.state.phase)
        if current_idx < len(phases) - 1:
            next_phase = phases[current_idx + 1]
            self.state.phase = next_phase
            self._apply_phase_state(next_phase)
        self.state.timestamp = time.time()

    def _apply_phase_state(self, phase: SimulationPhase):
        """Apply state changes for a given phase."""
        zones = {z.zone_id: z for z in self.state.zones}

        if phase == SimulationPhase.PRE_MATCH:
            self.state.total_attendance = 12000
            self.state.match_minute = 0
            self._distribute_crowd(zones, 0.15)
            self.state.shuttle_load_pct = 85.0
            self.state.parking_capacity_pct = 30.0
            self.state.energy_load_kwh = 1200.0
            self.state.waste_generation_kg = 150.0
            self.state.water_usage_liters = 4500.0

        elif phase == SimulationPhase.MATCH_START:
            self.state.total_attendance = 68000
            self.state.match_minute = 1
            self._distribute_crowd(zones, 0.80)
            self.state.energy_load_kwh = 2100.0

        elif phase == SimulationPhase.FIRST_HALF:
            self.state.total_attendance = 78000
            self.state.match_minute = 25
            self._distribute_crowd(zones, 0.90)
            self.state.energy_load_kwh = 2450.0
            self.state.waste_generation_kg = 580.0
            self.state.water_usage_liters = 9800.0

        elif phase == SimulationPhase.GOAL_EVENT:
            self.state.total_attendance = 78000
            self.state.match_minute = 34
            self.state.stadium_health_score = 88.0

        elif phase == SimulationPhase.CROWD_RUSH:
            self.state.match_minute = 35
            # Rush to food courts after goal
            zones["food_court_north"].current_occupancy = 2800
            zones["food_court_east"].current_occupancy = 2900
            zones["main_concourse"].current_occupancy = 4500
            for z in zones.values():
                z.update_density()
            self.state.stadium_health_score = 76.0
            self.state.waste_generation_kg = 780.0
            # Add congestion incident
            self.state.incidents.append(IncidentState(
                incident_id="INC-001",
                type="congestion",
                severity="high",
                zone_id="food_court_east",
                description="Critical density spike at East Wing Food Court — 96.7% capacity",
                timestamp=time.time(),
            ))

        elif phase == SimulationPhase.CONGESTION_PEAK:
            self.state.match_minute = 37
            zones["food_court_east"].current_occupancy = 2950
            zones["food_court_east"].update_density()
            self.state.stadium_health_score = 72.0

        elif phase == SimulationPhase.REROUTING:
            self.state.match_minute = 39
            # After AI intervention — redirect crowd
            zones["food_court_east"].current_occupancy = 2200
            zones["food_court_north"].current_occupancy = 2400
            zones["main_concourse"].current_occupancy = 3800
            for z in zones.values():
                z.update_density()
            self.state.stadium_health_score = 85.0
            # Resolve the incident
            for inc in self.state.incidents:
                if inc.incident_id == "INC-001":
                    inc.active = False

        elif phase == SimulationPhase.STABILIZED:
            self.state.match_minute = 42
            self._distribute_crowd(zones, 0.85)
            self.state.stadium_health_score = 92.0

        elif phase == SimulationPhase.MATCH_END:
            self.state.match_minute = 90
            self.state.total_attendance = 78000

        elif phase == SimulationPhase.EXIT_RUSH:
            self.state.match_minute = 95
            # Transportation bottleneck for Backup Scenario B
            zones["gate_a"].current_occupancy = 1900
            zones["gate_b"].current_occupancy = 1850
            zones["gate_c"].current_occupancy = 1800
            zones["gate_d"].current_occupancy = 1950
            for z in zones.values():
                z.update_density()
            self.state.shuttle_load_pct = 98.0
            self.state.parking_capacity_pct = 95.0
            self.state.stadium_health_score = 68.0
            self.state.incidents.append(IncidentState(
                incident_id="INC-002",
                type="transportation",
                severity="high",
                zone_id="gate_d",
                description="Exit bottleneck at Gate D — shuttle queue exceeding 45 minutes",
                timestamp=time.time(),
            ))

    def _distribute_crowd(self, zones: dict[str, ZoneState], fill_ratio: float):
        """Distribute crowd across seating zones based on fill ratio."""
        seating_zones = ["north_stand", "south_stand", "east_wing", "west_wing"]
        for zone_id in seating_zones:
            z = zones[zone_id]
            z.current_occupancy = int(z.capacity * fill_ratio)
            z.update_density()
        # Some flow to concourse and food
        zones["main_concourse"].current_occupancy = int(zones["main_concourse"].capacity * fill_ratio * 0.4)
        zones["food_court_north"].current_occupancy = int(zones["food_court_north"].capacity * fill_ratio * 0.3)
        zones["food_court_east"].current_occupancy = int(zones["food_court_east"].capacity * fill_ratio * 0.3)
        zones["vip_lounge"].current_occupancy = int(zones["vip_lounge"].capacity * fill_ratio * 0.7)
        for z in zones.values():
            z.update_density()

    def get_state(self) -> SimulationState:
        return self.state

    def get_state_dict(self) -> dict:
        return self.state.to_dict()
