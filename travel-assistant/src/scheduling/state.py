"""Tracks which itinerary stops have already triggered a landing SMS, so reruns don't double-send."""

import json
from pathlib import Path

from src.models import Itinerary, Stop

DEFAULT_STATE_PATH = Path(__file__).resolve().parents[2] / "data" / "state" / "notified_stops.json"


def stop_key(itinerary: Itinerary, stop: Stop) -> str:
    """A stable identifier for a stop within an itinerary, used to dedupe notifications."""
    return f"{itinerary.trip_name}:{stop.airport}:{stop.arrival_time.isoformat()}"


def load_notified(path: Path = DEFAULT_STATE_PATH) -> set[str]:
    if not path.exists():
        return set()
    return set(json.loads(path.read_text()))


def save_notified(notified: set[str], path: Path = DEFAULT_STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(notified)))


def has_been_notified(itinerary: Itinerary, stop: Stop, path: Path = DEFAULT_STATE_PATH) -> bool:
    return stop_key(itinerary, stop) in load_notified(path)


def mark_notified(itinerary: Itinerary, stop: Stop, path: Path = DEFAULT_STATE_PATH) -> None:
    notified = load_notified(path)
    notified.add(stop_key(itinerary, stop))
    save_notified(notified, path)
