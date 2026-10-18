"""Server-private Grade 8 Lesson 1 assessment banks."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.curriculum.grade8.lesson1_runtime import SOURCE, SOURCE_DATA
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep


QUESTION_VERIFICATIONS = {
    "g8-ae-l01-p01": "The original expressions both evaluate to 13, so 13 = 13.",
    "g8-ae-l01-p02": "Substitute 9: 11 + 2 = 9 + 4, so 13 = 13.",
    "g8-ae-l01-p03": "Substitute 13: 13 - 4 = 9, so 9 = 9.",
    "g8-ae-l01-p04": "Evaluate both transformed sides: 15 - 6 = 15 - 6, so 9 = 9.",
    "g8-ae-l01-p05": "Substitute 3: 3 + 8 = 11, so 11 = 11.",
    "g8-ae-l01-p06": "Substitute 8: 8 + 9 = 17, so 17 = 17.",
    "g8-ae-l01-p07": "Substitute 7: 6(7) = 42, so 42 = 42.",
    "g8-ae-l01-p08": "Substitute 7: 3(7) + 4 = 25, so 25 = 25.",
    "g8-ae-l01-p09": "Substitute 7: 5(7) - 8 = 27, so 27 = 27.",
    "g8-ae-l01-p10": "Substitute 7: 4(7) + 1 = 2(7) + 15, so 29 = 29.",
    "g8-ae-l01-p11": "Substitute 10 into the original equation: 2(10) + 10 = 30, so 30 = 30.",
    "g8-ae-l01-p12": "Substitute -2: 3(-2) + 4 = -2, so -2 = -2.",
    "g8-ae-l01-p13": "Substitute R70: 4(R70) + R20 = R300, so R300 = R300.",
    "g8-ae-l01-p14": "Substitute 4.2: 5(4.2) - 3 = 18, so 18 = 18.",
    "g8-ae-l01-p15": "Substitute 10: 3(10 - 2) = 24, so 24 = 24.",
    "g8-ae-l01-m01": "Substitute 8: 14 + 3 = 8 + 9, so 17 = 17.",
    "g8-ae-l01-m02": "Substitute 19: 19 - 7 = 12, so 12 = 12.",
    "g8-ae-l01-m03": "Substitute 6: 7(6) + 5 = 47, so 47 = 47.",
    "g8-ae-l01-m04": "Continue the repaired method to x = 7, then 4(7) - 8 = 20, so 20 = 20.",
    "g8-ae-l01-m05": "Substitute R120: 2(R120) + R35 = R275, so R275 = R275.",
    "g8-ae-l01-r01": "Substitute 11: 12 + 6 = 11 + 7, so 18 = 18.",
    "g8-ae-l01-r02": "Substitute 15: 15 + 8 = 23, so 23 = 23.",
    "g8-ae-l01-r03": "Substitute R55: 3(R55) + R15 = R180, so R180 = R180.",
}


PRACTICE_HINTS = {
    "g8-ae-l01-p01": ["Evaluate the left-hand expression first.", "Now evaluate the right-hand expression and compare the two values."],
    "g8-ae-l01-p02": ["Evaluate 11 + 2 before finding the box.", "Undo the added 4 from the required right-hand total."],
    "g8-ae-l01-p03": ["Use the inverse of subtracting 4.", "Apply the same operation to both sides before simplifying."],
    "g8-ae-l01-p04": ["Write subtraction of 6 on both complete sides.", "Evaluate the two sides separately and compare them."],
    "g8-ae-l01-p05": ["Replace x with the proposed value in the original equation.", "Evaluate the left side and compare it with 11."],
    "g8-ae-l01-p06": ["Undo the added 9 with its inverse.", "Subtract 9 from both sides, then simplify."],
    "g8-ae-l01-p07": ["The coefficient tells you how many equal x-groups there are.", "Divide both complete sides by 6."],
    "g8-ae-l01-p08": ["Undo the added 4 before dealing with the coefficient.", "After isolating 3x, divide both sides by 3."],
    "g8-ae-l01-p09": ["Undo subtracting 8 by adding 8 to both sides.", "Then divide both complete sides by the coefficient of x."],
    "g8-ae-l01-p10": ["Collect the variable terms on one side first.", "After removing 2x from both sides, isolate the remaining x-term."],
    "g8-ae-l01-p11": ["Check whether every term on the complete left side was divided.", "Restart from the original equation and remove 10 from both sides first."],
    "g8-ae-l01-p12": ["Substitute the claimed value into x.", "Follow multiplication before addition, then compare with the right side."],
    "g8-ae-l01-p13": ["Let x represent one ticket and form an equation for four tickets plus the fee.", "Remove the booking fee from both sides before dividing by four."],
    "g8-ae-l01-p14": ["Test the learner's claim in the original equation first.", "If it fails, undo subtracting 3 and then divide by 5."],
    "g8-ae-l01-p15": ["Treat x - 2 as one complete group.", "Divide both sides by 3, then use an inverse operation to isolate x."],
}


def _solution_steps(lines: list[str], verification: str) -> list[WorkedSolutionStep]:
    # The Gold Pack supplies one complete line per step but no separate prose
    # fields. Repeating that exact source line avoids inventing an explanation.
    return [
        WorkedSolutionStep(
            expression=line,
            explanation=line,
            why=line,
            verification=verification if index == len(lines) - 1 else "",
        )
        for index, line in enumerate(lines)
    ]


def _practice_question(item: dict) -> PracticeQuestion:
    return PracticeQuestion(
        id=item["id"],
        lesson_id=SOURCE_DATA["id"],
        question_number=item["number"],
        difficulty="source_unspecified",
        cognitive_level="source_unspecified",
        marks=item["marks"],
        type="short_text",
        prompt=item["prompt"],
        accepted_answers=[item["answer"]],
        answer_normalisation=AnswerNormalisation(),
        hints=PRACTICE_HINTS[item["id"]],
        worked_solution=_solution_steps(item["solution"], QUESTION_VERIFICATIONS[item["id"]]),
        misconception_tags=item["misconception_tags"],
        verification={"original_question_check": QUESTION_VERIFICATIONS[item["id"]]},
        correct_feedback="Correct.",
        source=SOURCE,
        answer_hidden_before_submission=True,
    )


PRACTICE_BANK = [_practice_question(item) for item in SOURCE_DATA["practice_questions"]]


class AssessmentQuestion(BaseModel):
    id: str = Field(pattern=r"^g8-ae-l01-[mr]\d{2}$")
    number: int = Field(ge=1, le=5)
    prompt: str
    marks: int | None = Field(default=None, ge=1, le=10)
    answer: str
    solution: list[str] = Field(min_length=1)
    verification: str = Field(min_length=1)
    misconception_tags: list[str] = Field(default_factory=list)

    def public(self) -> dict:
        return self.model_dump(include={"id", "number", "prompt", "marks"})


ASSESSMENT_TAGS = {
    "g8-ae-l01-m01": ["equals-means-answer"],
    "g8-ae-l01-m02": ["change-side-change-sign"],
    "g8-ae-l01-m03": ["divide-one-term"],
    "g8-ae-l01-m04": ["change-side-change-sign"],
    "g8-ae-l01-m05": ["context-to-equation"],
    "g8-ae-l01-r01": ["equals-means-answer"],
    "g8-ae-l01-r02": ["change-side-change-sign"],
    "g8-ae-l01-r03": ["context-to-equation"],
}


def _assessment(item: dict) -> AssessmentQuestion:
    return AssessmentQuestion(**{
        **item,
        "misconception_tags": ASSESSMENT_TAGS[item["id"]],
        "verification": QUESTION_VERIFICATIONS[item["id"]],
    })


MASTERY_BANK = [_assessment(item) for item in SOURCE_DATA["mastery_questions"]]
REASSESSMENT_BANK = [_assessment(item) for item in SOURCE_DATA["reassessment_questions"]]
MISCONCEPTION_REPAIRS = {
    item["tag"]: {"diagnosis": item["diagnosis"], "repair": item["repair"]}
    for item in SOURCE_DATA["misconceptions"]
}
REPAIR_RULES = SOURCE_DATA["repair_rules"]
MISCONCEPTION_REPAIRS["context-to-equation"] = {
    "diagnosis": REPAIR_RULES[5],
    "repair": REPAIR_RULES[5],
}
