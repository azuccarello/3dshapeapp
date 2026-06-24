"""Builds the SMS body/bodies for a stop that just triggered a landing notification."""

from src.models import Stop, StopType
from src.recommendations.airport_profile import load_airport_profile
from src.recommendations.destination_profile import load_destination_profile
from src.recommendations.engine import build_destination_recommendation, build_layover_recommendation
from src.recommendations.layover import LayoverWindow
from src.sms.formatter import format_destination_sms, format_layover_sms

# Final-destination airport codes we've pre-researched a neighborhood profile for.
DESTINATION_SLUGS = {
    "HNL": "waikiki",
}


def build_landing_sms(stop: Stop) -> list[str] | None:
    """Return the SMS body/bodies for a landed stop, or None if we have no profile data for it yet."""
    if stop.stop_type == StopType.LAYOVER:
        return _build_layover_sms(stop)
    return _build_destination_sms(stop)


def _build_layover_sms(stop: Stop) -> list[str] | None:
    profile = load_airport_profile(stop.airport)
    if profile is None:
        return None

    window = LayoverWindow(
        airport=stop.airport,
        arrival_time=stop.arrival_time,
        departure_time=stop.departure_time,
        transfer_minutes=profile.transfer_minutes,
    )
    recommendation = build_layover_recommendation(window, profile)
    return format_layover_sms(recommendation)


def _build_destination_sms(stop: Stop) -> list[str] | None:
    slug = DESTINATION_SLUGS.get(stop.airport)
    if slug is None:
        return None

    profile = load_destination_profile(slug)
    if profile is None:
        return None

    recommendation = build_destination_recommendation(profile)
    return format_destination_sms(recommendation)
