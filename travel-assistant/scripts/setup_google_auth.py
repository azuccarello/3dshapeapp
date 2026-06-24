"""One-time interactive OAuth flow for Gmail + Calendar access.

Run this locally (it opens a browser for Google's consent screen) to
generate the token file at GOOGLE_TOKEN_FILE. Requires GOOGLE_CLIENT_SECRET_FILE
(see .env.example) -- download this from Google Cloud Console after enabling
the Gmail API and Calendar API and creating an OAuth client ID for a Desktop app.

Usage: python scripts/setup_google_auth.py
"""

import os

from dotenv import load_dotenv

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]


def main() -> None:
    load_dotenv()
    from google_auth_oauthlib.flow import InstalledAppFlow

    client_secret_file = os.environ["GOOGLE_CLIENT_SECRET_FILE"]
    token_file = os.environ["GOOGLE_TOKEN_FILE"]

    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
    creds = flow.run_local_server(port=0)

    os.makedirs(os.path.dirname(token_file) or ".", exist_ok=True)
    with open(token_file, "w") as f:
        f.write(creds.to_json())

    print(f"Saved credentials to {token_file}")


if __name__ == "__main__":
    main()
