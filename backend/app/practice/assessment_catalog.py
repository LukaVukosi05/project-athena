"""Private assessment banks derived from the same registrations as practice."""

from app.practice.banks import LESSON_BANKS

ASSESSMENT_BANKS = {lesson_id: bank[1:] for lesson_id, bank in LESSON_BANKS.items()}
