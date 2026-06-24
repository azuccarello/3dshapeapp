from datetime import datetime

from src.models import FlightLeg, Itinerary, Stop, StopType
from src.scheduling.state import has_been_notified, load_notified, mark_notified, save_notified, stop_key


def _honolulu_itinerary() -> Itinerary:
    return Itinerary(
        trip_name="Honolulu",
        legs=[
            FlightLeg(
                flight_number="UA1170", airline="United", origin="LAX", destination="HNL",
                departure_time=datetime(2026, 8, 13, 17, 5),
                arrival_time=datetime(2026, 8, 13, 19, 32),
            ),
        ],
    )


def _hnl_stop() -> Stop:
    return Stop(
        airport="HNL",
        arrival_time=datetime(2026, 8, 13, 19, 32),
        departure_time=None,
        stop_type=StopType.FINAL_DESTINATION,
    )


def test_load_notified_returns_empty_set_when_file_missing(tmp_path):
    path = tmp_path / "notified_stops.json"
    assert load_notified(path) == set()


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "notified_stops.json"
    save_notified({"a", "b"}, path)
    assert load_notified(path) == {"a", "b"}


def test_has_been_notified_false_before_marking(tmp_path):
    path = tmp_path / "notified_stops.json"
    itinerary = _honolulu_itinerary()
    stop = _hnl_stop()

    assert has_been_notified(itinerary, stop, path) is False


def test_mark_notified_makes_has_been_notified_true(tmp_path):
    path = tmp_path / "notified_stops.json"
    itinerary = _honolulu_itinerary()
    stop = _hnl_stop()

    mark_notified(itinerary, stop, path)

    assert has_been_notified(itinerary, stop, path) is True


def test_stop_key_is_stable_for_same_itinerary_and_stop():
    itinerary = _honolulu_itinerary()
    stop = _hnl_stop()

    assert stop_key(itinerary, stop) == stop_key(itinerary, stop)
