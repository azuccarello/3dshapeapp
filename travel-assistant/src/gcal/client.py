"""Google Calendar API client for fetching trip-relevant calendar events.

Requires GOOGLE_CLIENT_SECRET_FILE / GOOGLE_TOKEN_FILE (see .env.example) and
the Calendar API enabled on the associated Google Cloud project. The Google
API libraries are imported lazily inside get_events() so that parse_event()
stays usable (and testable) without those credentials or packages in place.
"""

from datetime import datetime

from src.gcal.models import CalendarEvent


def parse_event(raw: dict) -> CalendarEvent:
    """Convert a raw Calendar API event resource into a CalendarEvent."""
    start_raw = raw["start"]
    end_raw = raw["end"]
    all_day = "date" in start_raw

    if all_day:
        start = datetime.fromisoformat(start_raw["date"])
        end = datetime.fromisoformat(end_raw["date"])
    else:
        start = datetime.fromisoformat(start_raw["dateTime"])
        end = datetime.fromisoformat(end_raw["dateTime"])

    return CalendarEvent(
        summary=raw.get("summary", ""),
        start=start,
        end=end,
        all_day=all_day,
        location=raw.get("location"),
        description=raw.get("description"),
    )


def get_events(start: datetime, end: datetime) -> list[CalendarEvent]:
    """Fetch the user's personal calendar events (excluding flight bookings) in [start, end)."""
    import os

    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(os.environ["GOOGLE_TOKEN_FILE"])
    service = build("calendar", "v3", credentials=creds)

    response = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        eventTypes=["default"],
        singleEvents=True,
    ).execute()

    return [parse_event(e) for e in response.get("items", [])]
