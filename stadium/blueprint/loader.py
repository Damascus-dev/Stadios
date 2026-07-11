"""StadiumOS AI — Blueprint Config Loader"""

from __future__ import annotations

import yaml
from pathlib import Path


def load_config(config_path: str | None = None) -> dict:
    if config_path:
        p = Path(config_path)
    else:
        p = Path(__file__).resolve().parent / "config.yaml"

    if not p.exists():
        raise FileNotFoundError(f"Blueprint config not found: {p}")

    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)
