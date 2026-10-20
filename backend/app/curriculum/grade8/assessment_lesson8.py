"""Private practice and assessment for Lesson 8 fraction equations."""
from __future__ import annotations

import re
from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson8_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

HINTS = [
 ("What is one fifth of the whole?", "Multiply both sides by five and check thirty-five divided by five."),
 ("Remove the whole-number tiles first.", "Subtract three from both sides, then multiply by four."),
 ("The bar covers the whole numerator.", "Multiply the complete fraction by three, then subtract two."),
 ("The numerator contains two m bars.", "Clear denominator three, then divide both sides by two."),
 ("What is divisible by both two and three?", "Choose six; multiply every term, then collect 3x plus 2x."),
 ("Keep the minus with the second fraction.", "Choose twelve; apply it to all three terms, keeping the subtraction sign."),
 ("Group 3q minus one as a single numerator.", "Multiply by five, add one, then divide by three."),
 ("What does the fraction bar divide?", "Multiply by four to recover all of 3(r-2); then divide by three."),
 ("There are four terms across both sides.", "Multiply ALL four by six before collecting x."),
 ("Which term did the learner fail to multiply?", "Apply four to x/2, 3/4 and 5; solve 2x+3=20."),
 ("Define the entire unknown number.", "Write 3n/4+5=26, then undo five and solve."),
 ("Define the whole fare before taking fractions.", "Use f/3+12=f/2 and multiply every term by six."),
 ("The minus sign belongs to the whole second numerator.", "Use LCD twelve and distribute negative three to both k and negative two."),
 ("Choose a denominator shared by all three fractions.", "Multiply every complete numerator by ten; check t=0 in the original."),
 ("Let c be the total capacity.", "Write 2c/5+18=7c/10; use LCD ten and check in litres."),
]

def _practice(item):
    n = item["number"]
    accepted = [item["answer"]]
    if (match := re.fullmatch(r"[a-z] = (-?\d+(?:\.\d+)?)", item["answer"])):
        accepted.append(match.group(1))
    if n == 7: accepted.extend(["a = 11.5", "11.5", "23/2"])
    if n == 15: accepted.extend(["v = 6.7", "6.7", "67/10"])
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
    id: str = Field(pattern=r"^g8-ae-l08-[mr]\d{2}$")
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
    "m01":"multiplies-one-term-only", "m02":"wrong-lcd", "m03":"sign-lost",
    "m04":"whole-term-omitted", "m05":"verification-omitted",
    "r01":"multiplies-one-term-only", "r02":"wrong-lcd", "r03":"whole-term-omitted",
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
