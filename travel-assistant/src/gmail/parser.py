"""Parses airline trip-confirmation emails into Itinerary objects.

Operates on the plain-text body of a confirmation email (the text/plain
part of a Gmail message). Times are kept exactly as printed -- the local
time at each respective airport -- with no timezone conversion. That keeps
layover math simple (arrival and departure at the same airport are already
in the same clock), and timezone-awareness gets added later, once we need
to compare itinerary times against "now".
"""

import re
from datetime import datetime, time, timedelta

from src.models import FlightLeg, Itinerary

AIRLINE_CODES = {"United": "UA"}

FLIGHT_PATTERN = re.compile(
    r"Flight (?P<flight_number>\d+)\s*\n"
    r"(?P<date>[A-Za-z]+, [A-Za-z]+ \d{1,2}, \d{4})\s*\n"
    r"Depart .*?\((?P<origin>[A-Z]{3})\)\s+(?P<dep_time>\d{1,2}:\d{2}\s*[AP]M)\s*\n"
    r"Arrive .*?\((?P<dest>[A-Z]{3})\)\s+(?P<arr_time>\d{1,2}:\d{2}\s*[AP]M)"
)

CONFIRMATION_PATTERN = re.compile(r"Confirmation Number:\s*([A-Z0-9]{4,8})", re.IGNORECASE)


def parse_itinerary_email(text: str, trip_name: str, airline: str = "United") -> Itinerary:
    """Extract flight legs and the confirmation number from a trip confirmation email."""
    confirmation_match = CONFIRMATION_PATTERN.search(text)
    confirmation_number = confirmation_match.group(1) if confirmation_match else None

    flight_prefix = AIRLINE_CODES.get(airline, "")
    legs = []
    for match in FLIGHT_PATTERN.finditer(text):
        date = datetime.strptime(match["date"], "%a, %b %d, %Y")
        departure = datetime.combine(date, _parse_time(match["dep_time"]))
        arrival = datetime.combine(date, _parse_time(match["arr_time"]))
        if arrival < departure:
            arrival += timedelta(days=1)

        legs.append(FlightLeg(
            flight_number=f"{flight_prefix}{match['flight_number']}",
            airline=airline,
            origin=match["origin"],
            destination=match["dest"],
            departure_time=departure,
            arrival_time=arrival,
            confirmation_number=confirmation_number,
        ))

    return Itinerary(trip_name=trip_name, legs=legs)


def _parse_time(raw: str) -> time:
    return datetime.strptime(raw.replace(" ", ""), "%I:%M%p").time()
