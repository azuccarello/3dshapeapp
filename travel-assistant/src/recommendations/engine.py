"""Assembles ranked recommendation picks for a layover or final-destination stop.

Layover picks are filtered by tier (see ``layover.LayoverTier``):
QUICK gets a coffee pick only, SHORT adds a food pick, and EXTENDED leads
with an activity before food and coffee. Final-destination picks aren't
tier-filtered -- narrowing by day, weather, or events happens later in the
pipeline.
"""

from dataclasses import dataclass

from src.recommendations.airport_profile import AirportProfile, Pick
from src.recommendations.destination_profile import DestinationProfile
from src.recommendations.layover import LayoverTier, LayoverWindow


@dataclass
class CategoryPick:
    category: str
    pick: Pick


@dataclass
class LayoverRecommendation:
    window: LayoverWindow
    picks: list[CategoryPick]


@dataclass
class DestinationRecommendation:
    destination: str
    picks: list[CategoryPick]


def build_layover_recommendation(window: LayoverWindow, profile: AirportProfile) -> LayoverRecommendation:
    """Select picks for a layover based on its effective-time tier."""
    picks: list[CategoryPick] = []

    if window.tier == LayoverTier.EXTENDED:
        picks += _take(profile.activities, "activity", 1)
        picks += _take(profile.food, "food", 1)
        picks += _take(profile.coffee, "coffee", 1)
    elif window.tier == LayoverTier.SHORT:
        picks += _take(profile.food, "food", 1)
        picks += _take(profile.coffee, "coffee", 1)
    else:  # QUICK
        picks += _take(profile.coffee, "coffee", 1)

    return LayoverRecommendation(window=window, picks=picks)


def build_destination_recommendation(profile: DestinationProfile) -> DestinationRecommendation:
    """Return all curated picks for a final destination, grouped by category."""
    picks: list[CategoryPick] = []
    for category, category_picks in (
        ("coffee", profile.coffee),
        ("food", profile.food),
        ("bars", profile.bars),
        ("activity", profile.activities),
        ("free", profile.free),
    ):
        picks += _take(category_picks, category, len(category_picks))

    return DestinationRecommendation(destination=profile.name, picks=picks)


def _take(picks: list[Pick], category: str, count: int) -> list[CategoryPick]:
    return [CategoryPick(category=category, pick=p) for p in picks[:count]]
