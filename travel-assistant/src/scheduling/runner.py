"""Single-check orchestration: has a landing just happened, and has it already been notified?"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.models import Itinerary, Stop
from src.scheduling.landing import stop_at_landing
from src.scheduling.state import DEFAULT_STATE_PATH, has_been_notified


@dataclass
class CheckResult:
    stop: Stop | None
    should_notify: bool


def check_for_landing(
    itinerary: Itinerary, now: datetime, state_path: Path = DEFAULT_STATE_PATH
) -> CheckResult:
    """Determine if a stop just landed and hasn't already triggered a notification.

    Callers should send the SMS when `should_notify` is True, then call
    `state.mark_notified` only once the send succeeds -- so a failed send
    can be retried on the next poll instead of being silently skipped.
    """
    stop = stop_at_landing(itinerary, now)
    if stop is None:
        return CheckResult(stop=None, should_notify=False)

    if has_been_notified(itinerary, stop, state_path):
        return CheckResult(stop=stop, should_notify=False)

    return CheckResult(stop=stop, should_notify=True)
