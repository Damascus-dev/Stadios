"""StadiumOS AI — Stadium Data Routes

Serves the procedurally generated Digital Twin data:
- GET /api/stadium — Full stadium metadata (config, seats, facilities, parking)
- GET /api/graph — Navigation graph (nodes + edges)
- GET /api/facilities/{type} — Filter facilities by type
"""

from __future__ import annotations

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from stadium.generator import generate_stadium
from stadium.metadata.schemas import FacilityType

router = APIRouter()

_stadium_data = None


def _get_stadium():
    global _stadium_data
    if _stadium_data is None:
        _stadium_data = generate_stadium()
    return _stadium_data


class FacilityFilter(BaseModel):
    type: str


@router.get("/api/stadium")
async def get_stadium():
    data = _get_stadium()
    return {
        "config": {
            "name": data.config.name,
            "origin": {"x": data.config.origin.x, "y": data.config.origin.y, "z": data.config.origin.z},
            "levels": [{"level": l.level, "elevation": l.elevation, "label": l.label} for l in data.config.levels],
            "quadrants": data.config.quadrants,
            "sections_per_level": data.config.sections_per_level,
            "rows_per_section": data.config.rows_per_section,
            "seats_per_row": data.config.seats_per_row,
            "total_seats": data.total_seats,
        },
        "seats": len(data.seats),
        "facilities": len(data.facilities),
        "parking_zones": len(data.parking),
        "generated_at": data.generated_at,
    }


@router.get("/api/graph")
async def get_graph():
    data = _get_stadium()
    g = data.graph
    return {
        "nodes": [
            {
                "id": n.id,
                "type": n.type.value,
                "name": n.name,
                "position": {"x": n.position.x, "y": n.position.y, "z": n.position.z},
                "level": n.level,
                "quadrant": n.quadrant,
                "accessible": n.accessible,
            }
            for n in g.nodes.values()
        ],
        "edges": [
            {
                "start_id": e.start_id,
                "end_id": e.end_id,
                "distance_m": e.distance_m,
                "travel_time_s": e.travel_time_s,
                "accessible": e.accessible,
            }
            for e in g.edges
        ],
    }


@router.get("/api/facilities/{facility_type}")
async def get_facilities(facility_type: str):
    data = _get_stadium()
    try:
        ftype = FacilityType(facility_type)
    except ValueError:
        valid = [e.value for e in FacilityType]
        raise HTTPException(status_code=404, detail=f"Unknown facility type '{facility_type}'. Valid: {valid}")

    matched = [f for f in data.facilities if f.type == ftype]
    return {
        "type": facility_type,
        "count": len(matched),
        "facilities": [
            {
                "id": f.id,
                "type": f.type.value,
                "position": {"x": f.position.x, "y": f.position.y, "z": f.position.z},
                "level": f.level,
                "quadrant": f.quadrant,
                "capacity": f.capacity,
                "status": f.status,
            }
            for f in matched
        ],
    }
