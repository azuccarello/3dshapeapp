"""Sends SMS messages via Twilio."""

import os


def send_messages(bodies: list[str]) -> list[str]:
    """Send each message body as a separate SMS, returning the Twilio message SIDs."""
    from twilio.rest import Client

    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
    from_number = os.environ["TWILIO_FROM_NUMBER"]
    to_number = os.environ["TWILIO_TO_NUMBER"]

    return [
        client.messages.create(body=body, from_=from_number, to=to_number).sid
        for body in bodies
    ]
