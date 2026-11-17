"""One server-owned offer; amounts are integer ZAR cents."""

from app.curriculum.repository import curriculum_repository
from app.curriculum.content_manifest import is_usable
from app.practice.catalog import PRACTICE_BANKS

PRICE_CENTS = 14900
TRIAL_DAYS = 14
TERMS_VERSION = "athena-trial-149-v1"


def plan_summary():
    grades = curriculum_repository.list_grades()
    return {
        "name": "Athena Mathematics",
        "price_cents": PRICE_CENTS,
        "currency": "ZAR",
        "interval": "month",
        "trial_days": TRIAL_DAYS,
        "terms_version": TERMS_VERSION,
        "interactive_lessons": sum(
            is_usable(l)
            for g in grades
            for t in g.topics
            for s in t.subtopics
            for l in s.lessons
        ),
        "topics": sum(len(g.topics) for g in grades),
        "practice_questions": sum(len(bank) for bank in PRACTICE_BANKS.values()),
    }
