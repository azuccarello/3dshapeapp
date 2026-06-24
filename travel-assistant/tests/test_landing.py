from datetime import datetime

from src.models import FlightLeg, Itinerary, StopType
from src.scheduling.landing import stop_at_landing


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


def test_no_landing_before_first_arrival():
    itinerary = _honolulu_itinerary()
    assert stop_at_landing(itinerary, datetime(2026, 8, 13, 10, 0)) is None


def test_detects_layover_landing_within_window():
    itinerary = _honolulu_itinerary()
    stop = stop_at_landing(itinerary, datetime(2026, 8, 13, 11, 55))
    assert stop is not None
    assert stop.airport == "LAX"
    assert stop.stop_type == StopType.LAYOVER


def test_detects_final_destination_landing_within_window():
    itinerary = _honolulu_itinerary()
    stop = stop_at_landing(itinerary, datetime(2026, 8, 13, 19, 40))
    assert stop is not None
    assert stop.airport == "HNL"
    assert stop.stop_type == StopType.FINAL_DESTINATION


def test_outside_landing_window_returns_none():
    itinerary = _honolulu_itinerary()
    # 20 minutes after LAX arrival, past the 15-minute window.
    assert stop_at_landing(itinerary, datetime(2026, 8, 13, 12, 8)) is None
