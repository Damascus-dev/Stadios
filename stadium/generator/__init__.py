# StadiumOS AI — Procedural Stadium Generator
# See docs/NAVIGATION_ENGINE_ARCHITECTURE/ for spec

from .levels import generate_levels
from .seating import generate_sections
from .facilities import generate_facilities
from .parking import generate_parking
from .graph import build_navigation_graph

from ..metadata.schemas import StadiumData, StadiumConfig, LevelConfig, Position
from ..blueprint.loader import load_config


def generate_stadium(config_path: str | None = None) -> StadiumData:
    cfg = load_config(config_path)

    stadium_cfg = StadiumConfig(
        name=cfg["stadium"]["name"],
        origin=Position(*cfg["stadium"]["origin"]),
        levels=[LevelConfig(lvl, elev, cfg["stadium"]["levels"]["labels"].get(str(lvl), ""))
                for lvl, elev in cfg["stadium"]["levels"]["elevation"].items()],
        quadrants=cfg["stadium"]["quadrants"]["names"],
        sections_per_level=cfg["stadium"]["sections"]["per_level"],
        rows_per_section=cfg["stadium"]["rows"]["per_section"],
        seats_per_row=cfg["stadium"]["seats"]["per_row"],
        parking_zones=cfg["stadium"]["parking"]["zones"],
        gates_primary=cfg["stadium"]["gates"]["primary"],
        gates_emergency=cfg["stadium"]["gates"]["emergency"],
    )

    levels_cfg = cfg["stadium"]["levels"]
    sections_cfg = cfg["stadium"]["sections"]
    rows_cfg = cfg["stadium"]["rows"]
    seats_cfg = cfg["stadium"]["seats"]
    quad_names = cfg["stadium"]["quadrants"]["names"]

    seats_list = []
    facilities_list = []
    graph_nodes = {}
    graph_edges = []

    for lvl, elev in levels_cfg["elevation"].items():
        lvl = int(lvl)
        sections = generate_sections(lvl, elev, sections_cfg, rows_cfg, seats_cfg, quad_names)
        seats_list.extend(sections["seats"])
        facilities_list.extend(sections["facilities"])

        # Level concourse nodes
        concourse_node = {
            "id": f"concourse_l{lvl}",
            "type": "concourse",
            "name": f"Level {lvl} Concourse",
            "position": (0, elev, 0),
            "level": lvl,
            "quadrant": "",
            "accessible": True,
        }
        graph_nodes[concourse_node["id"]] = concourse_node

    facs = generate_facilities(cfg["stadium"]["facilities"], levels_cfg, quad_names)
    for f in facs:
        facilities_list.append(f)
        fn = {
            "id": f.id,
            "type": f.type.value,
            "name": f.type.value.title(),
            "position": (f.position.x, f.position.y, f.position.z),
            "level": f.level,
            "quadrant": f.quadrant,
            "accessible": True,
        }
        graph_nodes[fn["id"]] = fn

    parking_zones = generate_parking(cfg["stadium"]["parking"], quad_names)

    graph = build_navigation_graph(graph_nodes, graph_edges, cfg["stadium"])

    from datetime import datetime
    return StadiumData(
        config=stadium_cfg,
        seats=seats_list,
        facilities=facilities_list,
        graph=graph,
        parking=parking_zones,
        total_seats=len(seats_list),
        generated_at=datetime.utcnow().isoformat(),
    )
