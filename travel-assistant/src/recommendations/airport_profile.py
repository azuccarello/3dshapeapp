"""Loads pre-researched airport profiles (transfer times, activities, coffee, food)."""

import json
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "airports"


@dataclass
class Pick:
    name: str
    location: str
    why: str
    link: str | None = None
    book_ahead: str | None = None


@dataclass
class AirportProfile:
    code: str
    name: str
    timezone: str
    transfer_minutes: int
    activities: list[Pick]
    coffee: list[Pick]
    food: list[Pick]


def load_airport_profile(code: str) -> AirportProfile | None:
    """Load the pre-researched profile for an airport code, or None if not yet researched."""
    path = DATA_DIR / f"{code.lower()}.json"
    if not path.exists():
        return None

    data = json.loads(path.read_text())
    return AirportProfile(
        code=data["code"],
        name=data["name"],
        timezone=data["timezone"],
        transfer_minutes=data["transfer_minutes"],
        activities=[Pick(**p) for p in data.get("activities", [])],
        coffee=[Pick(**p) for p in data.get("coffee", [])],
        food=[Pick(**p) for p in data.get("food", [])],
    )
