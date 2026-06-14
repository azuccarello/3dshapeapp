"""Cross-references calendar events against an itinerary's trip window."""

from datetime import date

from src.gcal.models import CalendarEvent
from src.models import Itinerary


def trip_window(*itineraries: Itinerary) -> tuple[date, date]:
    """Return the (start, end) dates spanning all legs across the given itineraries."""
    all_times = [
        t
        for itinerary in itineraries
        for leg in itinerary.legs
        for t in (leg.departure_time, leg.arrival_time)
    ]
    return min(all_times).date(), max(all_times).date()


def events_during_trip(events: list[CalendarEvent], trip_start: date, trip_end: date) -> list[CalendarEvent]:
    """Return calendar events that fall on any day within [trip_start, trip_end] (inclusive)."""
    return [
        e for e in events
        if e.start.date() <= trip_end and e.end.date() >= trip_start
    ]
