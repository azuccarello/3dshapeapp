"""Gmail API client for fetching airline trip-confirmation emails.

Requires GOOGLE_CLIENT_SECRET_FILE / GOOGLE_TOKEN_FILE (see .env.example) and
the Gmail API enabled on the associated Google Cloud project, authorized for
the gmail.readonly scope. The Google API libraries are imported lazily inside
fetch_confirmation_bodies() so extract_plain_text() stays usable (and
testable) without those credentials or packages in place.
"""

import base64


def extract_plain_text(message: dict) -> str:
    """Pull the text/plain body out of a raw Gmail API message resource."""
    data = _find_plain_text_data(message.get("payload", {}))
    if data is None:
        return ""
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")


def _find_plain_text_data(part: dict) -> str | None:
    if part.get("mimeType") == "text/plain":
        data = part.get("body", {}).get("data")
        if data:
            return data

    for subpart in part.get("parts", []):
        found = _find_plain_text_data(subpart)
        if found is not None:
            return found

    return None


def fetch_confirmation_bodies(query: str) -> list[str]:
    """Search Gmail for messages matching `query`, returning each one's plain-text body."""
    import os

    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(os.environ["GOOGLE_TOKEN_FILE"])
    service = build("gmail", "v1", credentials=creds)

    response = service.users().messages().list(userId="me", q=query).execute()
    message_ids = [m["id"] for m in response.get("messages", [])]

    bodies = []
    for message_id in message_ids:
        message = service.users().messages().get(userId="me", id=message_id, format="full").execute()
        bodies.append(extract_plain_text(message))

    return bodies
