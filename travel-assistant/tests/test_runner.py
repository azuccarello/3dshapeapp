from datetime import datetime

from src.models import FlightLeg, Itinerary
from src.scheduling.runner import check_for_landing
from src.scheduling.state import mark_notified


def _honolulu_itinerary() -> Itinerary:
    return Itinerary(
        trip_name="Honolulu",
        legs=[
            FlightLeg(
                flight_number="UA2126", airline="United", origin="RDM", destination="LAX",
                departure_time=datetime(2026, 8, 13, 8, 30),
                arrival_time=datetime(2026, 8, 13, 11, 48),
            ),
            FlightLeg(
                flight_number="UA1170", airline="United", origin="LAX", destination="HNL",
                departure_time=datetime(2026, 8, 13, 17, 5),
                arrival_time=datetime(2026, 8, 13, 19, 32),
            ),
        ],
    )


def test_no_stop_when_not_near_any_arrival(tmp_path):
    state_path = tmp_path / "notified_stops.json"
    itinerary = _honolulu_itinerary()

    result = check_for_landing(itinerary, datetime(2026, 8, 13, 10, 0), state_path)

    assert result.stop is None
    assert result.should_notify is False


def test_should_notify_on_first_check_within_landing_window(tmp_path):
    state_path = tmp_path / "notified_stops.json"
    itinerary = _honolulu_itinerary()

    result = check_for_landing(itinerary, datetime(2026, 8, 13, 11, 55), state_path)

    assert result.stop is not None
    assert result.stop.airport == "LAX"
    assert result.should_notify is True


def test_does_not_notify_twice_for_the_same_landing(tmp_path):
    state_path = tmp_path / "notified_stops.json"
    itinerary = _honolulu_itinerary()
    now = datetime(2026, 8, 13, 11, 55)

    first = check_for_landing(itinerary, now, state_path)
    mark_notified(itinerary, first.stop, state_path)

    second_check = check_for_landing(itinerary, datetime(2026, 8, 13, 12, 0), state_path)

    assert second_check.stop is not None
    assert second_check.should_notify is False
