"""StadiumOS AI — Facility Generation

Generates facilities procedurally based on blueprint rules:
- Food every Nth section
- Restroom every Nth section
- Medical per quadrant
- Prayer per level
- Charging every Nth section
- Merchandise near gates
- Volunteer desk per quadrant
- Elevators per quadrant
"""

from __future__ import annotations

import math

from ..metadata.schemas import Facility, FacilityType, Position


def generate_facilities(facilities_cfg: dict, levels_cfg: dict, quad_names: list[str]) -> list[Facility]:
    facilities = []
    num_levels = len(levels_cfg["elevation"])
    sections_per = 12
    angular_span = 2 * math.pi / sections_per
    inner_r = 55
    fid = 0

    for lvl_str in levels_cfg["elevation"]:
        lvl = int(lvl_str)
        elev = levels_cfg["elevation"][lvl_str]
        quad_sections = sections_per // len(quad_names)

        # Food courts every N sections
        food_every = facilities_cfg.get("food", {}).get("every_n_sections", 2)
        for sec in range(0, sections_per, food_every):
            theta = sec * angular_span + angular_span / 2
            quad_idx = sec // quad_sections
            fid += 1
            facilities.append(Facility(
                id=f"food_{fid}", type=FacilityType.FOOD,
                position=Position(x=inner_r * math.cos(theta), y=elev, z=inner_r * math.sin(theta)),
                level=lvl, quadrant=quad_names[min(quad_idx, len(quad_names) - 1)],
                capacity=50, status="open",
            ))

        # Restrooms every N sections
        rr_every = facilities_cfg.get("restroom", {}).get("every_n_sections", 3)
        for sec in range(0, sections_per, rr_every):
            theta = sec * angular_span + angular_span / 2
            quad_idx = sec // quad_sections
            fid += 1
            facilities.append(Facility(
                id=f"restroom_{fid}", type=FacilityType.RESTROOM,
                position=Position(x=inner_r * math.cos(theta), y=elev, z=inner_r * math.sin(theta)),
                level=lvl, quadrant=quad_names[min(quad_idx, len(quad_names) - 1)],
                capacity=20, status="open",
            ))

        # Medical per quadrant
        med_per = facilities_cfg.get("medical", {}).get("per_quadrant", 1)
        for q in range(len(quad_names)):
            for _ in range(med_per):
                theta = q * (2 * math.pi / len(quad_names))
                fid += 1
                facilities.append(Facility(
                    id=f"medical_{fid}", type=FacilityType.MEDICAL,
                    position=Position(x=inner_r * math.cos(theta), y=elev, z=inner_r * math.sin(theta)),
                    level=lvl, quadrant=quad_names[q],
                    capacity=5, status="open",
                ))

        # Prayer per level
        prayer_per = facilities_cfg.get("prayer", {}).get("per_level", 1)
        for _ in range(prayer_per):
            theta = (lvl * 90 + 45) * math.pi / 180
            fid += 1
            facilities.append(Facility(
                id=f"prayer_{fid}", type=FacilityType.PRAYER,
                position=Position(x=inner_r * math.cos(theta), y=elev, z=inner_r * math.sin(theta)),
                level=lvl, quadrant=quad_names[lvl % len(quad_names)],
                capacity=10, status="open",
            ))

        # Charging stations every N sections
        chg_every = facilities_cfg.get("charging", {}).get("every_n_sections", 2)
        for sec in range(0, sections_per, chg_every):
            theta = sec * angular_span + angular_span / 2
            quad_idx = sec // quad_sections
            fid += 1
            facilities.append(Facility(
                id=f"charging_{fid}", type=FacilityType.CHARGING,
                position=Position(x=inner_r * math.cos(theta), y=elev, z=inner_r * math.sin(theta)),
                level=lvl, quadrant=quad_names[min(quad_idx, len(quad_names) - 1)],
                capacity=8, status="open",
            ))

        # Volunteer desks per quadrant
        vol_per = facilities_cfg.get("volunteer_desk", {}).get("per_quadrant", 1)
        for q in range(len(quad_names)):
            for _ in range(vol_per):
                theta = q * (2 * math.pi / len(quad_names)) + angular_span / 2
                fid += 1
                facilities.append(Facility(
                    id=f"volunteer_{fid}", type=FacilityType.VOLUNTEER,
                    position=Position(x=inner_r * math.cos(theta), y=elev, z=inner_r * math.sin(theta)),
                    level=lvl, quadrant=quad_names[q],
                    capacity=3, status="open",
                ))

        # Merchandise near each quadrant gate
        if facilities_cfg.get("merchandise", {}).get("near_gates", False):
            for q in range(len(quad_names)):
                theta = q * (2 * math.pi / len(quad_names))
                fid += 1
                facilities.append(Facility(
                    id=f"merch_{fid}", type=FacilityType.MERCHANDISE,
                    position=Position(x=(inner_r + 5) * math.cos(theta), y=elev, z=(inner_r + 5) * math.sin(theta)),
                    level=lvl, quadrant=quad_names[q],
                    capacity=15, status="open",
                ))

    return facilities
