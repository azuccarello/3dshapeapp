"""Data types for Google Calendar events used as trip context."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class CalendarEvent:
    summary: str
    start: datetime
    end: datetime
    all_day: bool = False
    location: str | None = None
    description: str | None = None
