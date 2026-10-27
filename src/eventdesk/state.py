"""Typed records shared by deterministic tools and the future agent graph."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Member:
    id: str
    name: str
    email: str


@dataclass(frozen=True)
class Event:
    id: str
    title: str


@dataclass(frozen=True)
class CheckIn:
    event_id: str
    member_id: str
    # Set by trusted authentication code, never a public form field.
    verified: bool = False


@dataclass(frozen=True)
class AttendanceReport:
    event_id: str
    submissions: int
    member_ids: tuple[str, ...]
    duplicates: int
    unresolved: int


@dataclass(frozen=True)
class CloseoutResult:
    report: AttendanceReport
    draft: str
    status: Literal["pending_review"] = "pending_review"
