"""StadiumOS AI — Seating Generation

Generates sections, rows, and seats procedurally.
Uses InstancedMesh-compatible output (position + quaternion per seat).
"""

from __future__ import annotations

import math

from ..metadata.schemas import Seat, Position, Facility, FacilityType


def generate_sections(
    level: int,
    elevation: float,
    sections_cfg: dict,
    rows_cfg: dict,
    seats_cfg: dict,
    quad_names: list[str],
) -> dict:
    num_sections = sections_cfg["per_level"]
    angular_span = math.radians(sections_cfg["angular_span"])
    rows_per = rows_cfg["per_section"]
    radial_spacing = rows_cfg["radial_spacing"]
    seats_per = seats_cfg["per_row"]
    seat_width = seats_cfg["width"]
    inner_r = 40

    seats_list = []
    facilities_list = []
    quad_sections = num_sections // len(quad_names)

    for sec in range(num_sections):
        quad_idx = sec // quad_sections
        quad_name = quad_names[quad_idx]
        section_angle_start = sec * angular_span
        section_mid_angle = section_angle_start + angular_span / 2

        for row in range(rows_per):
            row_radius = inner_r + (row * radial_spacing)
            arc_length = 2 * row_radius * math.sin(angular_span / 2)
            seats_in_row = min(seats_per, max(1, int(arc_length / seat_width)))
            seat_spacing = arc_length / max(seats_in_row, 1)

            row_start_angle = section_angle_start + (angular_span - (seats_in_row * seat_spacing / row_radius)) / 2

            for s in range(seats_in_row):
                theta = row_start_angle + (s * seat_spacing / row_radius)
                x = row_radius * math.cos(theta)
                z = row_radius * math.sin(theta)
                sid = f"s{level}_{sec}_{row}_{s}"

                seats_list.append(Seat(
                    id=sid,
                    section=sec,
                    row=row,
                    number=s,
                    position=Position(x=x, y=elevation, z=z),
                    accessible=(row == 0 and s < seats_cfg.get("wheelchair_spaces_per_section", 4)),
                ))

    return {"seats": seats_list, "facilities": facilities_list}
