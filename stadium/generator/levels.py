"""StadiumOS AI — Level Generation

Generates concentric ring geometry for each stadium level.
Each level is a flat ring (torus) at a specific elevation.
"""

from __future__ import annotations

from ..metadata.schemas import Position


def generate_level_ring(
    level: int,
    elevation: float,
    inner_radius: float,
    outer_radius: float,
    quadrants: int = 4,
) -> dict:
    return {
        "level": level,
        "elevation": elevation,
        "inner_radius": inner_radius,
        "outer_radius": outer_radius,
        "quadrants": quadrants,
        "center": Position(0, elevation, 0),
    }


def generate_levels(config: dict, quad_names: list[str]) -> list[dict]:
    levels = []
    for lvl_str, elev in config["elevation"].items():
        lvl = int(lvl_str)
        ring = generate_level_ring(
            level=lvl,
            elevation=elev,
            inner_radius=60,
            outer_radius=80,
            quadrants=len(quad_names),
        )
        levels.append(ring)
    return levels
