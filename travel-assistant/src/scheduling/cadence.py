"""Decides how often the assistant should re-check for itinerary/landing updates."""

from datetime import datetime, timedelta

from src.models import Itinerary

CHECK_INTERVAL_NO_ITINERARY = timedelta(days=2)
CHECK_INTERVAL_NEAR_LANDING = timedelta(minutes=15)
NEAR_LANDING_WINDOW = timedelta(hours=2)  # how far ahead of an arrival to start polling every 15 min


def next_check_interval(itinerary: Itinerary | None, now: datetime) -> timedelta:
    """How long to wait before the next check.

    No itinerary yet, or no upcoming arrivals: check every other day. Within
    NEAR_LANDING_WINDOW of the next upcoming arrival: check every 15 minutes.
    """
    if itinerary is None:
        return CHECK_INTERVAL_NO_ITINERARY

    upcoming_arrivals = [
        stop.arrival_time
        for stop in itinerary.stops
        if stop.arrival_time is not None and stop.arrival_time >= now
    ]
    if not upcoming_arrivals:
        return CHECK_INTERVAL_NO_ITINERARY

    if min(upcoming_arrivals) - now <= NEAR_LANDING_WINDOW:
        return CHECK_INTERVAL_NEAR_LANDING

    return CHECK_INTERVAL_NO_ITINERARY
