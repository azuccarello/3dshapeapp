import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Personal travel assistant")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("check", help="Run the itinerary/landing check (not yet implemented)")

    args = parser.parse_args()

    if args.command == "check":
        print("Not implemented yet.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
