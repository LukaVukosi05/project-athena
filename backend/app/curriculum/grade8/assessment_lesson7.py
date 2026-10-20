"""Private practice and assessment for Lesson 7 bracket equations."""
from __future__ import annotations

import re
from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson7_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

HINTS = [
 ("How many identical groups are there?", "Divide both sides by two, then subtract five."),
 ("Which operation undoes four groups?", "Divide by four first, then add three."),
 ("Keep the outside negative sign.", "Divide both sides by negative three before solving the bracket."),
 ("The whole group repeats seven times.", "Divide by seven, then solve 2p minus one."),
 ("Do not lose the outside ten.", "Subtract ten first, then divide by negative two and subtract one."),
 ("Four tenths multiplies the entire bracket.", "Distribute to both terms: 2q plus four equals twelve."),
 ("Half multiplies every internal term.", "Half of 6r is 3r and half of negative four is negative two."),
 ("The right side also contains x.", "Expand the left bracket, then subtract x from both sides."),
 ("Expand both complete sides.", "Compare 10n minus five with 3n plus twelve."),
 ("What remains after expansion?", "Both complete expressions are identical: every s works."),
 ("Compare the constants after expanding.", "Negative eight cannot equal positive one: no solution."),
 ("Perimeter includes both lengths and both widths.", "Write 2[(x+3)+(x+1)]=32 before simplifying."),
 ("Each ticket contains both charges.", "Write 3(x+20)=210; divide before subtracting twenty."),
 ("A negative half affects both terms.", "Expand to negative 2k plus three equals seven."),
 ("When is division by a legal?", "Require a nonzero; for the example divide by negative four, then subtract 1.5."),
]

def _practice(item):
    n = item["number"]
    accepted = [item["answer"]]
    if (match := re.fullmatch(r"[a-z] = (-?\d+(?:\.\d+)?)", item["answer"])):
        accepted.append(match.group(1))
    if n == 10: accepted.extend(["all real numbers", "all values of s", "identity"])
    if n == 11: accepted.extend(["none", "no solutions", "contradiction"])
    if n == 13: accepted.extend(["R50", "50"])
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
    id: str = Field(pattern=r"^g8-ae-l07-[mr]\d{2}$")
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
    "m01": "distributes-first-term-only", "m02": "negative-distribution-error",
    "m03": "bracket-operation-order", "m04": "context-bracket-missed",
    "m05": "false-cancellation", "r01": "negative-distribution-error",
    "r02": "one-side-operation", "r03": "context-bracket-missed",
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
