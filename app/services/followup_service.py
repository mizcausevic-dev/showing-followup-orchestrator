from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any


def _clamp(value: float, low: int = 0, high: int = 100) -> int:
    return max(low, min(high, round(value)))


@dataclass(slots=True)
class ShowingFollowupService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return json.loads(self.source_path.read_text(encoding="utf-8"))

    def score(self, item: dict[str, Any]) -> dict[str, Any]:
        freshness = max(0, 36 - min(item["hours_since_showing"], 36)) * 1.2
        disclosure_bonus = 12 if item["asked_for_disclosures"] else 0
        second_showing_bonus = 16 if item["asked_for_second_showing"] else 0
        financing_bonus = 8 if item["financing_ready"] else -6
        objection_penalty = item["objection_count"] * 6.5

        intent_score = _clamp(
            item["interest_signal"] * 0.34
            + item["price_fit"] * 0.22
            + freshness
            + disclosure_bonus * 0.8
            + second_showing_bonus * 0.9
            + financing_bonus
            - objection_penalty
        )
        urgency_score = _clamp(
            item["interest_signal"] * 0.34
            + max(0, 30 - item["hours_since_showing"]) * 1.1
            + (10 if item["asked_for_second_showing"] else 0)
            - item["objection_count"] * 4.2
        )

        status = "hot" if intent_score >= 84 else "warm" if intent_score >= 64 else "cool"
        cadence = (
            "send same-day follow-up with disclosures and offer path"
            if status == "hot"
            else "follow up within 24 hours with objection handling"
            if status == "warm"
            else "place in nurture lane and revisit interest next week"
        )
        next_action = (
            f"Use {item['preferred_channel']} now, attach disclosures, and offer a second showing window."
            if status == "hot"
            else f"Use {item['preferred_channel']} within 24 hours and address pricing or fit objections directly."
            if status == "warm"
            else f"Use {item['preferred_channel']} for a lighter nurture touch and keep the lead in the long-tail pipeline."
        )

        return {
            "showingId": item["showing_id"],
            "buyerName": item["buyer_name"],
            "listingTitle": item["listing_title"],
            "city": item["city"],
            "agentName": item["agent_name"],
            "hoursSinceShowing": item["hours_since_showing"],
            "intentScore": intent_score,
            "urgencyScore": urgency_score,
            "status": status,
            "preferredChannel": item["preferred_channel"],
            "cadence": cadence,
            "nextAction": next_action,
            "askedForDisclosures": item["asked_for_disclosures"],
            "askedForSecondShowing": item["asked_for_second_showing"],
            "financingReady": item["financing_ready"],
            "objectionCount": item["objection_count"],
        }

    def queue(self) -> list[dict[str, Any]]:
        return sorted(
            [self.score(item) for item in self.load()["showings"]],
            key=lambda item: (-item["urgencyScore"], -item["intentScore"], item["buyerName"]),
        )

    def showing(self, showing_id: str) -> dict[str, Any] | None:
        for item in self.queue():
            if item["showingId"] == showing_id:
                return item
        return None

    def summary(self) -> dict[str, Any]:
        data = self.load()
        queue = self.queue()
        hot = [item for item in queue if item["status"] == "hot"]
        warm = [item for item in queue if item["status"] == "warm"]
        avg_intent = mean(item["intentScore"] for item in queue)
        avg_urgency = mean(item["urgencyScore"] for item in queue)
        return {
            "brokerage": data["brokerage"],
            "market": data["market"],
            "showingCount": len(queue),
            "hotLeadCount": len(hot),
            "warmLeadCount": len(warm),
            "averageIntentScore": round(avg_intent, 1),
            "averageUrgencyScore": round(avg_urgency, 1),
            "leadRecommendation": (
                "Work the Newton and Cambridge second-showing buyers same day, then move the Boston multifamily lead into a tighter objection-handling sequence before momentum cools."
            ),
        }

    def sample_payload(self) -> dict[str, Any]:
        queue = self.queue()
        return {
            "dashboard": self.summary(),
            "followups": [
                {
                    "showingId": item["showingId"],
                    "buyerName": item["buyerName"],
                    "intentScore": item["intentScore"],
                    "urgencyScore": item["urgencyScore"],
                    "status": item["status"],
                    "nextAction": item["nextAction"],
                }
                for item in queue[:3]
            ],
        }


def build_service(root: Path | None = None) -> ShowingFollowupService:
    base = root or Path(__file__).resolve().parents[2]
    return ShowingFollowupService(base / "app" / "data" / "sample_showings.json")
