"""Private practice and assessment for Lesson 6 variables on both sides."""
from __future__ import annotations

import re
from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson6_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

HINTS = [
 ("Which x term is smaller?", "Subtract x from both complete sides, then remove the constant and divide."),
 ("How many y tiles remain after removing three?", "Subtract 3y from both sides, then add five and divide by four."),
 ("Which first move keeps a positive coefficient?", "Subtract 2a from both sides, then add one."),
 ("Keep the negative m tiles intact.", "Add 3m to both complete sides before moving the constant."),
 ("Which side has a negative p term?", "Add 2p to both sides, then add six."),
 ("Compare the q coefficients in tenths.", "Subtract 0.2q from both sides, then remove one."),
 ("Compare the r coefficients in quarters.", "Subtract one quarter of r, then remove two."),
 ("What remains when 7s leaves both sides?", "The constants are identical, so every permitted s works."),
 ("What remains when 3t leaves both sides?", "Eight cannot equal one; no choice of t repairs this."),
 ("How did eight x become three x?", "Subtract 5x from both original sides before solving."),
 ("Write both plan costs in one variable.", "Set 40 + 9u equal to 70 + 6u at the break-even point."),
 ("Track each person's starting money and weekly saving.", "Set 80 + 30w equal to 200 + 10w."),
 ("Why can the side labels be set equal?", "They mark equal sides: 4x + 1 = 6x - 9."),
 ("Keep the negative quarter attached to n.", "Add 0.25n to both sides and solve the remaining 0.75n."),
 ("What happens when a equals c?", "Compare b with d to decide identity or contradiction; then solve the numerical example."),
]

def _practice(item):
    n = item["number"]
    accepted = [item["answer"]]
    if (match := re.fullmatch(r"[a-z] = (-?\d+(?:\.\d+)?)", item["answer"])):
        accepted.append(match.group(1))
    if n == 8: accepted.extend(["all real numbers", "all values of s", "identity"])
    if n == 9: accepted.extend(["none", "no solutions", "contradiction"])
    if n == 10: accepted.append("subtract 5x from both sides; x = 5")
    if n == 13: accepted.append("x = 5; 21 cm")
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
    id: str = Field(pattern=r"^g8-ae-l06-[mr]\d{2}$")
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
    "m01": "variable-one-side-only",
    "m02": "coefficient-subtraction-error",
    "m03": "identity-as-one-solution",
    "m04": "contradiction-as-zero",
    "m05": "context-equality-missed",
    "r01": "coefficient-subtraction-error",
    "r02": "contradiction-as-zero",
    "r03": "context-equality-missed",
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
