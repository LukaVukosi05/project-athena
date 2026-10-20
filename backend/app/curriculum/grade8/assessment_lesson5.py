"""Private practice and assessment for Lesson 5 two step equations."""
from __future__ import annotations

import re
from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson5_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

HINTS = [
 ("Which operation acts on x last?", "Subtract three on both sides before dividing by two."),
 ("What does the minus five do after multiplying y?", "Add five on both sides, then divide by three."),
 ("Follow x through the forward machine.", "Undo adding two, then undo dividing by four."),
 ("Rewrite the variable term with its sign.", "After removing twenty, divide by negative three."),
 ("The outside seven is the last operation.", "Subtract seven first; then divide by the signed coefficient."),
 ("Treat the variable term as negative n thirds.", "Remove the starting five while keeping the minus attached to n."),
 ("Remove the fixed decimal first.", "Subtract one and a half, then double the remaining half of p."),
 ("What is done after taking two thirds?", "Add four first, then multiply by the reciprocal three halves."),
 ("Check the learner's first division on the whole side.", "If dividing the whole left by four, the six must also be divided; subtract six first instead."),
 ("Keep both negatives visible.", "Subtract seven on both sides, then divide by negative two."),
 ("Count both known sides of the rectangle.", "Subtract their total from the perimeter, then divide the remaining two lengths equally."),
 ("Separate fixed fare and distance fare.", "Remove eighteen rand before dividing by six rand per kilometre."),
 ("Subtract the starting temperature.", "Divide the total increase by three degrees per hour."),
 ("Work in tenths to remove the outside constant.", "Add two point four, then multiply the one-fifth expression by five."),
 ("What must be true to divide by a?", "Remove b first, keep a non-zero, then divide by the signed example coefficient."),
]

def _practice(item):
    n = item["number"]
    accepted = [item["answer"]]
    if (match := re.fullmatch(r"[a-z] = (-?\d+(?:\.\d+)?)", item["answer"])):
        accepted.append(match.group(1))
    if n == 9:
        accepted.extend(["x = 5", "subtract 10 first; x = 5"])
    if n == 11:
        accepted.append("16 cm")
    if n == 15:
        accepted.extend(["a ≠ 0; x = -8", "a != 0; x = -8"])
    return PracticeQuestion(
        id=item["id"], lesson_id=SOURCE_DATA["id"], question_number=n,
        difficulty="source_unspecified", cognitive_level="source_unspecified", marks=item["marks"],
        type="short_text", prompt=item["prompt"], accepted_answers=accepted,
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
    id: str = Field(pattern=r"^g8-ae-l05-[mr]\d{2}$")
    number: int = Field(ge=1, le=5)
    prompt: str
    marks: int | None = Field(default=None, ge=1, le=10)
    answer: str
    solution: list[str] = Field(min_length=1)
    verification: str = Field(min_length=1)
    misconception_tags: list[str] = Field(default_factory=list)

    def public(self):
        return self.model_dump(include={"id","number","prompt","marks"})

ASSESSMENT_TAGS = {
    "m01": "wrong-operation-order",
    "m02": "variable-subtracted-error",
    "m03": "fraction-decimal-error",
    "m04": "one-side-operation",
    "m05": "verification-omitted",
    "r01": "coefficient-sign-error",
    "r02": "fraction-decimal-error",
    "r03": "wrong-operation-order",
}

def _assessment(item):
    suffix = item["id"].split("-")[-1]
    return AssessmentQuestion(**{**item, "verification":item["solution"][-1],
                                 "misconception_tags":[ASSESSMENT_TAGS[suffix]]})

MASTERY_BANK = [_assessment(item) for item in SOURCE_DATA["mastery_questions"]]
REASSESSMENT_BANK = [_assessment(item) for item in SOURCE_DATA["reassessment_questions"]]
MISCONCEPTION_REPAIRS = {item["tag"]:{"diagnosis":item["diagnosis"],"repair":item["repair"]}
                         for item in SOURCE_DATA["misconceptions"]}
REPAIR_RULES = SOURCE_DATA["repair_rules"]
