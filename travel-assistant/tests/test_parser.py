from datetime import datetime
from pathlib import Path

from src.gmail.parser import parse_itinerary_email
from src.models import StopType

FIXTURES = Path(__file__).parent / "fixtures"


def test_parses_outbound_legs():
    text = (FIXTURES / "honolulu_outbound_confirmation.txt").read_text()
    itinerary = parse_itinerary_email(text, trip_name="Honolulu")

    assert len(itinerary.legs) == 2

    leg1, leg2 = itinerary.legs
    assert leg1.flight_number == "UA2126"
    assert leg1.origin == "RDM"
    assert leg1.destination == "LAX"
    assert leg1.departure_time == datetime(2026, 8, 13, 9, 37)
    assert leg1.arrival_time == datetime(2026, 8, 13, 11, 48)
    assert leg1.confirmation_number == "AB12CD"

    assert leg2.flight_number == "UA1170"
    assert leg2.origin == "LAX"
    assert leg2.destination == "HNL"
    assert leg2.departure_time == datetime(2026, 8, 13, 17, 5)
    assert leg2.arrival_time == datetime(2026, 8, 13, 19, 48)


def test_outbound_stops_classification():
    text = (FIXTURES / "honolulu_outbound_confirmation.txt").read_text()
    itinerary = parse_itinerary_email(text, trip_name="Honolulu")

    stops = itinerary.stops
    assert [s.airport for s in stops] == ["RDM", "LAX", "HNL"]
    assert [s.stop_type for s in stops] == [
        StopType.ORIGIN, StopType.LAYOVER, StopType.FINAL_DESTINATION,
    ]

    lax_stop = stops[1]
    assert lax_stop.arrival_time == datetime(2026, 8, 13, 11, 48)
    assert lax_stop.departure_time == datetime(2026, 8, 13, 17, 5)


def test_parses_return_leg():
    text = (FIXTURES / "honolulu_return_confirmation.txt").read_text()
    itinerary = parse_itinerary_email(text, trip_name="Honolulu Return")

    assert len(itinerary.legs) == 1
    leg = itinerary.legs[0]
    assert leg.flight_number == "UA1437"
    assert leg.origin == "LAX"
    assert leg.destination == "RDM"
    assert leg.departure_time == datetime(2026, 8, 20, 11, 50)
    assert leg.arrival_time == datetime(2026, 8, 20, 13, 55)
    assert leg.confirmation_number == "EF34GH"
