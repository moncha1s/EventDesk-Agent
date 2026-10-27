"""Deterministic domain tools. These functions perform no network calls."""

from collections.abc import Iterable

from eventdesk.state import AttendanceReport, CheckIn, Member


def reconcile_attendance(
    event_id: str, members: Iterable[Member], check_ins: Iterable[CheckIn]
) -> AttendanceReport:
    """Count verified, known member IDs once per event; flag all unresolved rows."""
    if not event_id.strip():
        raise ValueError("An explicit event ID is required")
    known_ids = {member.id for member in members if member.id.strip()}
    seen: set[str] = set()
    submissions = duplicates = unresolved = 0
    for check_in in check_ins:
        if check_in.event_id != event_id:
            continue
        submissions += 1
        if not check_in.verified or check_in.member_id not in known_ids:
            unresolved += 1
        elif check_in.member_id in seen:
            duplicates += 1
        else:
            seen.add(check_in.member_id)
    return AttendanceReport(
        event_id, submissions, tuple(sorted(seen)), duplicates, unresolved
    )
