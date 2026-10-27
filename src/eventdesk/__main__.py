"""Run a synthetic closeout example: python -m eventdesk."""

import json
from dataclasses import asdict

from eventdesk.graph import close_out_event
from eventdesk.state import CheckIn, Event, Member


def main() -> None:
    event = Event("demo-workshop", "Demo Python Workshop")
    members = [
        Member("member-1", "Alex Example", "alex@example.com"),
        Member("member-2", "Sam Example", "sam@example.com"),
    ]
    check_ins = [
        CheckIn(event.id, "member-1", verified=True),
        CheckIn(event.id, "member-1", verified=True),
        CheckIn(event.id, "member-2", verified=True),
        CheckIn(event.id, "unknown", verified=True),
    ]
    print(json.dumps(asdict(close_out_event(event, members, check_ins)), indent=2))


if __name__ == "__main__":
    main()
