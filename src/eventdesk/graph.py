"""Initial closeout pipeline. LangGraph/Claude orchestration is a future milestone."""

from collections.abc import Iterable

from eventdesk.state import CheckIn, CloseoutResult, Event, Member
from eventdesk.tools import reconcile_attendance


def close_out_event(
    event: Event, members: Iterable[Member], check_ins: Iterable[CheckIn]
) -> CloseoutResult:
    report = reconcile_attendance(event.id, members, check_ins)
    draft = (
        f"Thanks for joining {event.title}! "
        "We appreciate everyone who participated. Watch this space for our next event."
    )
    # No send capability: a draft is not authorization to contact members.
    return CloseoutResult(report=report, draft=draft)
