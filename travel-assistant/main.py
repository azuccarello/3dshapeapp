import argparse

from dotenv import load_dotenv


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Personal travel assistant")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("check", help="Run the itinerary/landing check (not yet implemented)")
    test_sms_parser = subparsers.add_parser("test-sms", help="Send a test SMS via Twilio to confirm credentials work")
    test_sms_parser.add_argument(
        "message", nargs="?", default="Test message from your travel assistant."
    )

    args = parser.parse_args()

    if args.command == "check":
        print("Not implemented yet.")
    elif args.command == "test-sms":
        from src.sms.client import send_messages

        sids = send_messages([args.message])
        print(f"Sent {len(sids)} message(s): {', '.join(sids)}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
