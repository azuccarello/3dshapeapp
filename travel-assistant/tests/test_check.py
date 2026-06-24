from datetime import datetime

from src.models import Stop, StopType
from src.scheduling.check import build_landing_sms


def test_layover_stop_builds_single_sms():
    # Real Honolulu-trip layover: UA2126 arrives 11:48, UA1170 departs 17:05.
    stop = Stop(
        airport="LAX",
        arrival_time=datetime(2026, 8, 13, 11, 48),
        departure_time=datetime(2026, 8, 13, 17, 5),
        stop_type=StopType.LAYOVER,
    )

    messages = build_landing_sms(stop)

    assert messages is not None
    assert len(messages) == 1
    assert "LAX" in messages[0]
    assert "LAX Art Program" in messages[0]


def test_final_destination_stop_builds_two_sms():
    stop = Stop(
        airport="HNL",
        arrival_time=datetime(2026, 8, 13, 19, 48),
        departure_time=None,
        stop_type=StopType.FINAL_DESTINATION,
    )

    messages = build_landing_sms(stop)

    assert messages is not None
    assert len(messages) == 2
    assert all(len(m) <= 1600 for m in messages)


def test_unresearched_layover_airport_returns_none():
    stop = Stop(
        airport="ZZZ",
        arrival_time=datetime(2026, 8, 13, 11, 48),
        departure_time=datetime(2026, 8, 13, 13, 0),
        stop_type=StopType.LAYOVER,
    )

    assert build_landing_sms(stop) is None


def test_unresearched_destination_airport_returns_none():
    stop = Stop(
        airport="ZZZ",
        arrival_time=datetime(2026, 8, 13, 19, 48),
        departure_time=None,
        stop_type=StopType.FINAL_DESTINATION,
    )

    assert build_landing_sms(stop) is None
