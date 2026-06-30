import json
from pathlib import Path

from src.gmail.client import extract_plain_text
from src.gmail.parser import parse_itinerary_email

FIXTURES = Path(__file__).parent / "fixtures"


def _load_message():
    return json.loads((FIXTURES / "gmail_message_honolulu_outbound.json").read_text())


def test_extract_plain_text_picks_the_text_plain_part():
    body = extract_plain_text(_load_message())

    assert "Confirmation Number: AB12CD" in body
    assert "Flight 2126" in body
    assert "HTML version" not in body


def test_extract_plain_text_returns_empty_string_when_no_plain_part():
    message = {"payload": {"mimeType": "text/html", "body": {"data": "PGgxPkhpPC9oMT4"}}}

    assert extract_plain_text(message) == ""


def test_extracted_body_parses_into_a_valid_itinerary():
    body = extract_plain_text(_load_message())

    itinerary = parse_itinerary_email(body, trip_name="Honolulu")

    assert len(itinerary.legs) == 2
    assert itinerary.legs[0].flight_number == "UA2126"
    assert itinerary.legs[1].destination == "HNL"
