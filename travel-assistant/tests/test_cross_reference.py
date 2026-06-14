import json
from datetime import date
from pathlib import Path

from src.gcal.client import parse_event
from src.gcal.cross_reference import events_during_trip, trip_window
from src.gmail.parser import parse_itinerary_email

FIXTURES = Path(__file__).parent / "fixtures"


def _load_calendar_events():
    raw = json.loads((FIXTURES / "calendar_events_honolulu_window.json").read_text())
    return [parse_event(e) for e in raw]


def _load_itineraries():
    outbound = parse_itinerary_email(
        (FIXTURES / "honolulu_outbound_confirmation.txt").read_text(), trip_name="Honolulu"
    )
    return_trip = parse_itinerary_email(
        (FIXTURES / "honolulu_return_confirmation.txt").read_text(), trip_name="Honolulu Return"
    )
    return outbound, return_trip


def test_trip_window_spans_outbound_and_return():
    outbound, return_trip = _load_itineraries()
    assert trip_window(outbound, return_trip) == (date(2026, 8, 13), date(2026, 8, 20))


def test_events_during_trip_includes_relevant_events():
    outbound, return_trip = _load_itineraries()
    start, end = trip_window(outbound, return_trip)
    events = _load_calendar_events()

    relevant = events_during_trip(events, start, end)
    summaries = [e.summary for e in relevant]

    assert "Hawaii Spartan Sprint 5K - Saturday, August 15th 2026" in summaries
    assert "Bingo at Midtown Yacht Club (Bend, OR)" in summaries
    assert summaries.count("Gym") == 5
    assert "PAYDAY" not in summaries
    assert len(relevant) == 7
