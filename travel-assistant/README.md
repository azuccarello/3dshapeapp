# Travel Assistant

A personal travel assistant that texts you a single, friend-style SMS when you land —
itinerary-aware recommendations for layovers and final destinations, researched ahead of time.

## Status

Built incrementally, with a check-in after each phase:

1. [x] Gmail itinerary parser
2. [x] Calendar cross-reference
3. [ ] Recommendation engine (layovers + destinations)
4. [ ] SMS delivery (Twilio)
5. [ ] Scheduling / polling runner

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
   Google OAuth and Twilio setup walkthroughs will be added here as those phases are built.
