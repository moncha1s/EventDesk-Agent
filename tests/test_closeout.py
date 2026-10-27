import unittest

from eventdesk.graph import close_out_event
from eventdesk.state import CheckIn, Event, Member
from eventdesk.tools import reconcile_attendance


class AttendanceTests(unittest.TestCase):
    def setUp(self):
        self.members = [Member("a", "Alex", "alex@example.com")]

    def test_duplicates_do_not_inflate_attendance(self):
        rows = [CheckIn("event", "a", True)] * 2
        report = reconcile_attendance("event", self.members, rows)
        self.assertEqual(report.member_ids, ("a",))
        self.assertEqual(report.duplicates, 1)
        self.assertEqual(report.submissions, 2)

    def test_unknown_and_unverified_are_unresolved(self):
        rows = [CheckIn("event", "unknown", True), CheckIn("event", "a")]
        report = reconcile_attendance("event", self.members, rows)
        self.assertEqual(report.unresolved, 2)
        self.assertEqual(report.member_ids, ())

    def test_events_are_isolated(self):
        rows = [CheckIn("other", "a", True)]
        self.assertEqual(reconcile_attendance("event", self.members, rows).submissions, 0)

    def test_member_can_attend_multiple_events(self):
        rows = [CheckIn("one", "a", True), CheckIn("two", "a", True)]
        for event_id in ("one", "two"):
            self.assertEqual(
                reconcile_attendance(event_id, self.members, rows).member_ids, ("a",)
            )

    def test_draft_requires_review_and_excludes_member_details(self):
        result = close_out_event(Event("event", "Workshop"), self.members, [])
        self.assertEqual(result.status, "pending_review")
        self.assertNotIn("alex@example.com", result.draft)
        self.assertEqual(result.report.member_ids, ())

    def test_blank_event_id_is_rejected(self):
        with self.assertRaises(ValueError):
            reconcile_attendance(" ", self.members, [])


if __name__ == "__main__":
    unittest.main()
