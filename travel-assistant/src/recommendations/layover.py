"""Effective layover time and the recommendation tier it falls into.

Effective time = connection window - boarding buffer - realistic transfer
time for that specific airport. Transfer time is airport-specific (varies
by terminal layout) and is supplied by the caller, typically from an
airport profile.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

BOARDING_BUFFER_MINUTES = 20


class LayoverTier(Enum):
    QUICK = "quick"  # < 1hr effective: smoothie/coffee only, terminal options
    SHORT = "short"  # 1-2hrs effective: food recommendation, sit-down if close to gate
    EXTENDED = "extended"  # 2hrs+ effective: activity first, then food


@dataclass
class LayoverWindow:
    airport: str
    arrival_time: datetime
    departure_time: datetime
    transfer_minutes: int

    @property
    def connection_minutes(self) -> int:
        delta = self.departure_time - self.arrival_time
        return int(delta.total_seconds() // 60)

    @property
    def effective_minutes(self) -> int:
        return self.connection_minutes - BOARDING_BUFFER_MINUTES - self.transfer_minutes

    @property
    def tier(self) -> LayoverTier:
        if self.effective_minutes < 60:
            return LayoverTier.QUICK
        if self.effective_minutes < 120:
            return LayoverTier.SHORT
        return LayoverTier.EXTENDED
