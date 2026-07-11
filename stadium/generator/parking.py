"""StadiumOS AI — Parking Zone Generation

Generates parking zones around the stadium perimeter.
Each quadrant gets zones with rows and spaces.
"""

from __future__ import annotations

import math

from ..metadata.schemas import ParkingZone, Position


def generate_parking(parking_cfg: dict, quad_names: list[str]) -> list[ParkingZone]:
    zones = []
    total_zones = parking_cfg["zones"]
    zones_per_quad = total_zones // len(quad_names)
    outer_ring_r = 200

    for qi, quad in enumerate(quad_names):
        base_angle = qi * (2 * math.pi / len(quad_names))
        for zi in range(zones_per_quad):
            zone_idx = qi * zones_per_quad + zi
            angle = base_angle + (zi - zones_per_quad / 2) * 0.15
            zone_id = f"P{chr(65 + zone_idx)}" if zone_idx < 26 else f"P{zone_idx}"

            x = outer_ring_r * math.cos(angle)
            z = outer_ring_r * math.sin(angle)

            zones.append(ParkingZone(
                zone_id=zone_id,
                capacity=400,
                occupied=0,
                nearest_gate_id=f"gate_primary_{qi}",
            ))

    return zones
