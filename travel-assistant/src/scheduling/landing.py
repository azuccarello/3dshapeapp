"""Determines which stop (if any) just became relevant -- i.e., should trigger a recommendation."""

from datetime import datetime, timedelta

from src.models import Itinerary, Stop

LANDING_WINDOW_MINUTES = 15  # how close to "now" an arrival must be to count as "just landed"


def stop_at_landing(itinerary: Itinerary, now: datetime) -> Stop | None:
    """Return the stop the traveler has just landed at, if `now` is within the landing window."""
    for stop in itinerary.stops:
        if stop.arrival_time is None:
            continue
        if stop.arrival_time <= now <= stop.arrival_time + timedelta(minutes=LANDING_WINDOW_MINUTES):
            return stop
    return None
