from datetime import datetime

from src.recommendations.airport_profile import AirportProfile, Pick, load_airport_profile
from src.recommendations.destination_profile import load_destination_profile
from src.recommendations.engine import build_destination_recommendation, build_layover_recommendation
from src.recommendations.layover import LayoverWindow
from src.sms.formatter import format_destination_sms, format_layover_sms

DEN_PROFILE = AirportProfile(
    code="DEN",
    name="Denver International Airport",
    timezone="America/Denver",
    transfer_minutes=15,
    activities=[Pick(name="Yoga Room", location="Concourse B", why="Free, quiet, mats provided.")],
    coffee=[Pick(name="Corvus Coffee", location="Concourse B", why="Local Denver roaster. Small batch.")],
    food=[Pick(name="Smashburger", location="Concourse B", why="Decent burger, fast.")],
)


def test_extended_layover_sms_includes_all_picks():
    # Real Honolulu-trip layover: UA2126 arrives 11:48, UA1170 departs 17:05.
    profile = load_airport_profile("LAX")
    window = LayoverWindow(
        airport="LAX",
        arrival_time=datetime(2026, 8, 13, 11, 48),
        departure_time=datetime(2026, 8, 13, 17, 5),
        transfer_minutes=profile.transfer_minutes,
    )
    recommendation = build_layover_recommendation(window, profile)

    messages = format_layover_sms(recommendation)

    assert len(messages) == 1
    message = messages[0]
    assert "LAX" in message
    assert "~4.7hr" in message
    assert "LAX Art Program" in message
    assert "Ashland Hill" in message
    assert "Klatch Coffee" in message
    assert "https://www.laxshopdine.com/directory/klatch-coffee-terminal-7-t7/" in message

    # Long "why" text gets trimmed to its first sentence for the SMS.
    assert "World Barista Championship" in message
    assert "Globally-sourced beans" not in message


def test_quick_layover_sms_is_coffee_only():
    window = LayoverWindow(
        airport="DEN",
        arrival_time=datetime(2026, 1, 1, 10, 0),
        departure_time=datetime(2026, 1, 1, 11, 30),
        transfer_minutes=15,
    )
    recommendation = build_layover_recommendation(window, DEN_PROFILE)

    messages = format_layover_sms(recommendation)

    assert len(messages) == 1
    message = messages[0]
    assert "~55min" in message
    assert "Corvus Coffee" in message
    assert "Smashburger" not in message
    assert "Yoga Room" not in message


def test_destination_sms_splits_food_and_activities():
    profile = load_destination_profile("waikiki")
    recommendation = build_destination_recommendation(profile)

    messages = format_destination_sms(recommendation)

    assert len(messages) == 2
    food_drink, things_to_do = messages

    assert "Welcome to Waikiki, Honolulu!" in food_drink
    assert "Knots Coffee Roasters" in food_drink
    assert "Da Cove Health Bar" in food_drink
    assert "Green Lady Cocktail Room" in food_drink
    assert "Diamond Head Summit Trail" not in food_drink

    assert "Diamond Head Summit Trail" in things_to_do
    assert "Kuhio Beach Hula Show" in things_to_do
    assert "Knots Coffee Roasters" not in things_to_do
