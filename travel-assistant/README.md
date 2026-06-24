# Travel Assistant

A personal travel assistant that texts you a single, friend-style SMS when you land —
itinerary-aware recommendations for layovers and final destinations, researched ahead of time.

## Status

Built incrementally, with a check-in after each phase:

1. [x] Gmail itinerary parser + live client
2. [x] Calendar cross-reference
3. [x] Recommendation engine (layovers + destinations)
4. [x] SMS delivery (Twilio)
5. [x] Scheduling / polling runner (cadence + idempotent notification tracking)
6. [x] Wire it all together in `main.py`'s `check` command
7. [ ] Live flight-status checks closer to departure/arrival

Run tests with `python -m pytest` from this directory.

## Project layout

- `src/models.py` — core data types (itinerary, flight legs, stops)
- `src/` — gmail, calendar, recommendations, and sms modules (added phase by phase)
- `tests/fixtures/` — sample data used to validate parsing logic
- `main.py` — CLI entry point
- `.env` — local credentials (never committed; copy from `.env.example`)

## Setup

1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and fill in credentials as each phase requires them.
4. **Google OAuth (Gmail + Calendar):**
   - In Google Cloud Console, enable the Gmail API and Calendar API on a project, then create an
     OAuth client ID (type: Desktop app) and download its JSON as `credentials/client_secret.json`
     (path configurable via `GOOGLE_CLIENT_SECRET_FILE`).
   - Run `python scripts/setup_google_auth.py` -- it opens a browser for the Google consent screen
     and saves the resulting token to `GOOGLE_TOKEN_FILE` (`credentials/token.json` by default).
   - This is an interactive, browser-based flow, so it has to be run on a machine with a browser
     you're signed into -- not from a headless/remote session.
5. **Twilio:** create a (free trial is fine) account at twilio.com, grab the Account SID and Auth
   Token from the console, buy/verify a from-number, and set all four `TWILIO_*` vars in `.env`.
   Run `python main.py test-sms` to confirm credentials work.
