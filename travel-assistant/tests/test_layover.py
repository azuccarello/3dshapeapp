from datetime import datetime

from src.recommendations.layover import LayoverTier, LayoverWindow


def test_lax_layover_is_extended():
    # Real Honolulu-trip layover: UA2126 arrives 11:48, UA1170 departs 17:05.
    window = LayoverWindow(
        airport="LAX",
        arrival_time=datetime(2026, 8, 13, 11, 48),
        departure_time=datetime(2026, 8, 13, 17, 5),
        transfer_minutes=20,
    )
    assert window.connection_minutes == 317
    assert window.effective_minutes == 277
    assert window.tier == LayoverTier.EXTENDED


def test_short_connection_is_quick_tier():
    window = LayoverWindow(
        airport="DEN",
        arrival_time=datetime(2026, 1, 1, 10, 0),
        departure_time=datetime(2026, 1, 1, 11, 30),
        transfer_minutes=15,
    )
    assert window.effective_minutes == 55
    assert window.tier == LayoverTier.QUICK


def test_medium_connection_is_short_tier():
    window = LayoverWindow(
        airport="DEN",
        arrival_time=datetime(2026, 1, 1, 10, 0),
        departure_time=datetime(2026, 1, 1, 12, 0),
        transfer_minutes=15,
    )
    assert window.effective_minutes == 85
    assert window.tier == LayoverTier.SHORT
