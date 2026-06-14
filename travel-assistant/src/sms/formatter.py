"""Formats recommendation picks into SMS-ready message text.

Layovers produce a single short message. Final destinations produce two
messages: one covering food/drink near the stay, one covering things to do.
"""

from src.recommendations.engine import CategoryPick, DestinationRecommendation, LayoverRecommendation
from src.recommendations.layover import LayoverTier

CATEGORY_EMOJI = {
    "coffee": "☕",
    "food": "🍴",
    "bars": "🍸",
    "activity": "🎯",
    "free": "✨",
}

TIER_PHRASES = {
    LayoverTier.QUICK: "short connection",
    LayoverTier.SHORT: "decent window",
    LayoverTier.EXTENDED: "good chunk of time",
}


def format_layover_sms(recommendation: LayoverRecommendation) -> list[str]:
    """Build the (single) SMS for a layover stop."""
    window = recommendation.window
    intro = (
        f"Landed at {window.airport} -- {TIER_PHRASES[window.tier]}, "
        f"{_format_duration(window.effective_minutes)} before you need to head to your gate."
    )

    lines = [intro, ""]
    for category_pick in recommendation.picks:
        lines.append(_format_pick(category_pick))
        lines.append("")

    return [_join(lines)]


def format_destination_sms(recommendation: DestinationRecommendation) -> list[str]:
    """Build the (up to two) SMS messages for a final-destination stop."""
    by_category: dict[str, list[CategoryPick]] = {}
    for category_pick in recommendation.picks:
        by_category.setdefault(category_pick.category, []).append(category_pick)

    food_drink = _build_message(
        f"Welcome to {recommendation.destination}! Food & drink near you:",
        by_category,
        ["coffee", "food", "bars"],
    )
    things_to_do = _build_message(
        "And for things to do while you're here:",
        by_category,
        ["activity", "free"],
    )

    return [food_drink, things_to_do]


def _build_message(intro: str, by_category: dict[str, list[CategoryPick]], categories: list[str]) -> str:
    lines = [intro, ""]
    for category in categories:
        for category_pick in by_category.get(category, []):
            lines.append(_format_pick(category_pick))
            lines.append("")
    return _join(lines)


def _format_pick(category_pick: CategoryPick) -> str:
    pick = category_pick.pick
    emoji = CATEGORY_EMOJI.get(category_pick.category, "")
    parts = [f"{emoji} {pick.name} ({pick.location})", _first_sentence(pick.why)]
    if pick.link:
        parts.append(pick.link)
    return "\n".join(parts)


def _first_sentence(text: str) -> str:
    sentence = text.split(". ")[0].rstrip(".")
    return f"{sentence}."


def _format_duration(minutes: int) -> str:
    if minutes < 60:
        return f"~{minutes}min"
    return f"~{minutes / 60:.1f}hr"


def _join(lines: list[str]) -> str:
    return "\n".join(lines).strip()
