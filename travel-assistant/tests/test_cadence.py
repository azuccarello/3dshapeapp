from datetime import datetime, timedelta

from src.models import FlightLeg, Itinerary
from src.scheduling.cadence import (
    CHECK_INTERVAL_NEAR_LANDING,
    CHECK_INTERVAL_NO_ITINERARY,
    next_check_interval,
)


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


def test_no_itinerary_checks_every_other_day():
    assert next_check_interval(None, datetime(2026, 8, 1, 9, 0)) == CHECK_INTERVAL_NO_ITINERARY


def test_far_from_any_arrival_checks_every_other_day():
    itinerary = _honolulu_itinerary()
    assert next_check_interval(itinerary, datetime(2026, 8, 1, 9, 0)) == CHECK_INTERVAL_NO_ITINERARY


def test_within_two_hours_of_arrival_checks_every_15_minutes():
    itinerary = _honolulu_itinerary()
    near_lax_arrival = datetime(2026, 8, 13, 11, 48) - timedelta(hours=1)
    assert next_check_interval(itinerary, near_lax_arrival) == CHECK_INTERVAL_NEAR_LANDING


def test_no_upcoming_arrivals_left_checks_every_other_day():
    itinerary = _honolulu_itinerary()
    after_final_arrival = datetime(2026, 8, 13, 20, 0)
    assert next_check_interval(itinerary, after_final_arrival) == CHECK_INTERVAL_NO_ITINERARY
