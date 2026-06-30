"""Loads pre-researched destination profiles (coffee, food, bars, activities, free stuff)."""

import json
from dataclasses import dataclass
from pathlib import Path

from src.recommendations.airport_profile import Pick

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "destinations"


@dataclass
class DestinationProfile:
    code: str
    name: str
    timezone: str
    coffee: list[Pick]
    food: list[Pick]
    bars: list[Pick]
    activities: list[Pick]
    free: list[Pick]


def load_destination_profile(slug: str) -> DestinationProfile | None:
    """Load the pre-researched profile for a destination slug, or None if not yet researched."""
    path = DATA_DIR / f"{slug.lower()}.json"
    if not path.exists():
        return None

    data = json.loads(path.read_text())
    return DestinationProfile(
        code=data["code"],
        name=data["name"],
        timezone=data["timezone"],
        coffee=[Pick(**p) for p in data.get("coffee", [])],
        food=[Pick(**p) for p in data.get("food", [])],
        bars=[Pick(**p) for p in data.get("bars", [])],
        activities=[Pick(**p) for p in data.get("activities", [])],
        free=[Pick(**p) for p in data.get("free", [])],
    )
