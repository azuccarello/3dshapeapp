from datetime import datetime

from src.recommendations.airport_profile import AirportProfile, Pick, load_airport_profile
from src.recommendations.destination_profile import load_destination_profile
from src.recommendations.engine import (
    build_destination_recommendation,
    build_layover_recommendation,
)
from src.recommendations.layover import LayoverTier, LayoverWindow

DEN_PROFILE = AirportProfile(
    code="DEN",
    name="Denver International Airport",
    timezone="America/Denver",
    transfer_minutes=15,
    activities=[Pick(name="Yoga Room", location="Concourse B", why="Free, quiet, mats provided.")],
    coffee=[Pick(name="Corvus Coffee", location="Concourse B", why="Local Denver roaster.")],
    food=[Pick(name="Smashburger", location="Concourse B", why="Decent burger, fast.")],
)


def test_extended_layover_leads_with_activity():
    # Real Honolulu-trip layover: UA2126 arrives 11:48, UA1170 departs 17:05.
    profile = load_airport_profile("LAX")
    window = LayoverWindow(
        airport="LAX",
        arrival_time=datetime(2026, 8, 13, 11, 48),
        departure_time=datetime(2026, 8, 13, 17, 5),
        transfer_minutes=profile.transfer_minutes,
    )
    assert window.tier == LayoverTier.EXTENDED

    recommendation = build_layover_recommendation(window, profile)

    categories = [p.category for p in recommendation.picks]
    assert categories == ["activity", "food", "coffee"]
    assert "LAX Art Program" in recommendation.picks[0].pick.name
    assert "Ashland Hill" in recommendation.picks[1].pick.name
    assert "Klatch" in recommendation.picks[2].pick.name


def test_short_layover_skips_activity():
    window = LayoverWindow(
        airport="DEN",
        arrival_time=datetime(2026, 1, 1, 10, 0),
        departure_time=datetime(2026, 1, 1, 12, 0),
        transfer_minutes=15,
    )
    assert window.tier == LayoverTier.SHORT

    recommendation = build_layover_recommendation(window, DEN_PROFILE)

    categories = [p.category for p in recommendation.picks]
    assert categories == ["food", "coffee"]


def test_quick_layover_is_coffee_only():
    window = LayoverWindow(
        airport="DEN",
        arrival_time=datetime(2026, 1, 1, 10, 0),
        departure_time=datetime(2026, 1, 1, 11, 30),
        transfer_minutes=15,
    )
    assert window.tier == LayoverTier.QUICK

    recommendation = build_layover_recommendation(window, DEN_PROFILE)

    categories = [p.category for p in recommendation.picks]
    assert categories == ["coffee"]
    assert "Corvus" in recommendation.picks[0].pick.name


def test_destination_recommendation_includes_all_categories():
    profile = load_destination_profile("waikiki")

    recommendation = build_destination_recommendation(profile)

    categories = {p.category for p in recommendation.picks}
    assert categories == {"coffee", "food", "bars", "activity", "free"}
    assert len(recommendation.picks) == (
        len(profile.coffee) + len(profile.food) + len(profile.bars)
        + len(profile.activities) + len(profile.free)
    )
