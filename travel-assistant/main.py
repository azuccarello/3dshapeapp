import argparse
from datetime import datetime

from dotenv import load_dotenv

# Gmail search query for United trip-confirmation emails. Adjust as more airlines are supported.
CONFIRMATION_EMAIL_QUERY = 'subject:"Trip Confirmation"'


def run_check() -> None:
    """Fetch confirmation emails, check each itinerary for a fresh landing, and text picks."""
    from src.gmail.client import fetch_confirmation_bodies
    from src.gmail.parser import parse_itinerary_email
    from src.scheduling.check import build_landing_sms
    from src.scheduling.runner import check_for_landing
    from src.scheduling.state import mark_notified
    from src.sms.client import send_messages

    bodies = fetch_confirmation_bodies(CONFIRMATION_EMAIL_QUERY)
    if not bodies:
        print("No confirmation emails found.")
        return

    itineraries = [parse_itinerary_email(body, trip_name="Trip") for body in bodies]

    now = datetime.now()
    sent_any = False
    for itinerary in itineraries:
        result = check_for_landing(itinerary, now)
        if not result.should_notify:
            continue

        sms_bodies = build_landing_sms(result.stop)
        if sms_bodies is None:
            print(f"Landed at {result.stop.airport}, but no profile data yet -- skipping SMS.")
            continue

        send_messages(sms_bodies)
        mark_notified(itinerary, result.stop)
        sent_any = True
        print(f"Sent landing SMS for {result.stop.airport}.")

    if not sent_any:
        print("No new landing detected this check.")


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Personal travel assistant")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("check", help="Check Gmail for itineraries and text picks if you've just landed")
    test_sms_parser = subparsers.add_parser("test-sms", help="Send a test SMS via Twilio to confirm credentials work")
    test_sms_parser.add_argument(
        "message", nargs="?", default="Test message from your travel assistant."
    )

    args = parser.parse_args()

    if args.command == "check":
        run_check()
    elif args.command == "test-sms":
        from src.sms.client import send_messages

        sids = send_messages([args.message])
        print(f"Sent {len(sids)} message(s): {', '.join(sids)}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
