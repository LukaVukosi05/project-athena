"""Shared mastery and topic-check answer scoring."""

from fastapi import HTTPException


def _normalise_assessment(value: str) -> str:
    return "".join(str(value).casefold().replace("−", "-").replace("–", "-").split())


def _score_assessment(bank, answers: dict[str, str]) -> tuple[int, list, list[str]]:
    expected = {item.id for item in bank}
    if set(answers) != expected:
        raise HTTPException(
            422, f"Answers must contain exactly: {', '.join(sorted(expected))}"
        )
    reviewed = []
    tags = []
    correct = 0
    for item in bank:
        # This item explicitly tests the fixed fee model AND verification.
        # Its pack's short answer is a memo, not sufficient submission evidence.
        accepted = (
            [*getattr(item, "accepted_answers", [])]
            if item.id in {"g8-ae-l10-m05", "g8-ae-l10-r03"}
            else [item.answer, *getattr(item, "accepted_answers", [])]
        )
        passed = any(
            _normalise_assessment(answers[item.id]).rstrip(".")
            == _normalise_assessment(option).rstrip(".")
            for option in accepted
        )
        correct += int(passed)
        if not passed:
            tags.extend(item.misconception_tags)
        reviewed.append(
            {
                "id": item.id,
                "correct": passed,
                "answer": item.answer,
                "solution": item.solution,
                "verification": item.verification,
            }
        )
    return correct, reviewed, list(dict.fromkeys(tags))
