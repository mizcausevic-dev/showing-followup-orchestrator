from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.followup_service import build_service


class ShowingFollowupServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = build_service(ROOT)

    def test_summary_shape(self) -> None:
        summary = self.service.summary()
        self.assertEqual(summary["brokerage"], "Northstar Residential Group")
        self.assertGreater(summary["showingCount"], 0)

    def test_top_lead_is_newton_or_cambridge(self) -> None:
        queue = self.service.queue()
        self.assertIn(queue[0]["showingId"], {"shw-7001", "shw-7004"})

    def test_lookup(self) -> None:
        item = self.service.showing("shw-7002")
        self.assertIsNotNone(item)
        self.assertIn(item["status"], {"hot", "warm", "cool"})


if __name__ == "__main__":
    unittest.main()
