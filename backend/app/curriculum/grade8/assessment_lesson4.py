"""Private practice and assessment for Lesson 4 multiplicative inverses."""
from __future__ import annotations

from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson4_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

HINTS = [
 ("How many equal groups are shown?", "Share the total over those groups; divide both sides."),
 ("How many shares make the whole?", "Multiply both complete sides by the divisor."),
 ("What sign is attached to the coefficient?", "Divide by the whole signed coefficient on both sides."),
 ("What undoes dividing by a negative number?", "Multiply both complete sides by that negative divisor."),
 ("What fraction of the whole is given?", "Two halves restore a whole; double both sides."),
 ("Which fraction makes two thirds equal one?", "Multiply both sides by three halves."),
 ("What is the coefficient of a negative variable?", "Negative one times x is negative x; divide by negative one."),
 ("Share the signed total across four groups.", "Keep the negative sign and simplify the fraction before converting to decimal."),
 ("How many quarters are in one whole?", "Multiply both sides by one quarter to undo division by a quarter."),
 ("Substitute the learner's claim in the original.", "The coefficient of x must become one by division on both sides."),
 ("Which dimension is unknown?", "Width times length is area; divide both sides by the width."),
 ("What does one bundle cost?", "Share the total price across seven identical bundles."),
 ("Write an equation for three equal stages.", "Divide the full route by three and include kilometres."),
 ("What fraction of the tank is known?", "Four equal quarters make one tank; multiply both sides by four."),
 ("When is division by a allowed?", "Keep the non-zero condition visible, then divide by the signed coefficient."),
]

def _practice(item):
    n = item["number"]
    return PracticeQuestion(
        id=item["id"], lesson_id=SOURCE_DATA["id"], question_number=n,
        difficulty="source_unspecified", cognitive_level="source_unspecified", marks=item["marks"],
        type="short_text", prompt=item["prompt"], accepted_answers=[item["answer"]],
        answer_normalisation=AnswerNormalisation(), hints=list(HINTS[n-1]),
        worked_solution=[WorkedSolutionStep(expression=line, explanation=line, why=line,
                          verification=item["solution"][-1] if index==len(item["solution"])-1 else "")
                         for index,line in enumerate(item["solution"])],
        misconception_tags=item["misconception_tags"],
        verification={"original_question_check":item["solution"][-1]},
        correct_feedback="Correct.", source=SOURCE, answer_hidden_before_submission=True,
    )

PRACTICE_BANK = [_practice(item) for item in SOURCE_DATA["practice_questions"]]

class AssessmentQuestion(BaseModel):
    id: str = Field(pattern=r"^g8-ae-l04-[mr]\d{2}$")
    number: int = Field(ge=1, le=5)
    prompt: str
    marks: int | None = Field(default=None, ge=1, le=10)
    answer: str
    solution: list[str] = Field(min_length=1)
    verification: str = Field(min_length=1)
    misconception_tags: list[str] = Field(default_factory=list)

    def public(self):
        return self.model_dump(include={"id","number","prompt","marks"})

def _assessment(item):
    return AssessmentQuestion(**{**item, "verification":item["solution"][-1]})

MASTERY_BANK = [_assessment(item) for item in SOURCE_DATA["mastery_questions"]]
REASSESSMENT_BANK = [_assessment(item) for item in SOURCE_DATA["reassessment_questions"]]
MISCONCEPTION_REPAIRS = {item["tag"]:{"diagnosis":item["diagnosis"],"repair":item["repair"]}
                         for item in SOURCE_DATA["misconceptions"]}
REPAIR_RULES = SOURCE_DATA["repair_rules"]
