"""Server-private assessment and practice for Grade 8 equations by inspection."""
from __future__ import annotations

from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson2_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

# Hints stop before the candidate; the authored memo stays gated by submission.
HINTS = [
 ("What number added to eight gives thirteen?", "Use the related subtraction fact to test a candidate."),
 ("Think of a starting point that becomes four after removing nine.", "Check by subtracting nine in the original equation."),
 ("Recall a multiplication fact for eight groups and fifty-six.", "Test how many objects each of eight groups needs."),
 ("Work backwards from nine objects in each of six groups.", "Test the total by dividing it into six groups."),
 ("Find the value before adding five.", "Now consider which input doubled makes that value."),
 ("Find the value before subtracting three.", "Recall the four-times fact for that intermediate value."),
 ("Three equal bracket groups total twenty-one; find one group's value.", "Then find n by undoing the plus two inside each group."),
 ("Measure the distance between twenty and twelve.", "The variable is the amount subtracted, so test a backward jump."),
 ("A negative times which sign gives a positive?", "Try a negative candidate in the original product."),
 ("Before adding two, the quotient must be five.", "Find the total which gives five when divided by three."),
 ("Test the claimed five in the original expression.", "If it misses the target, find the pre-subtraction value."),
 ("Evaluate each side for a small candidate in a two-column table.", "Look for the row where the left and right totals agree."),
 ("Area equals length times width.", "Find the length that makes seven times length equal eighty-four."),
 ("Consecutive numbers differ by one.", "Place candidates on either side of half of thirty-five."),
 ("Find the quantity before adding two.", "One quarter of the unknown must match that quantity."),
]

VERIFICATIONS = {
 1:"5 + 8 = 13",2:"13 - 9 = 4",3:"8(7) = 56",4:"54 ÷ 6 = 9",5:"2(6) + 5 = 17",
 6:"4(5) - 3 = 17",7:"3(5 + 2) = 21",8:"20 - 8 = 12",9:"(-4)(-7) = 28",
 10:"15 ÷ 3 + 2 = 7",11:"4(19/4) - 1 = 18",12:"3(5) + 1 = 5 + 11 = 16",
 13:"12 cm × 7 cm = 84 cm²",14:"17 + 18 = 35",15:"0.25(12) + 2 = 5",
}


def _practice(item: dict) -> PracticeQuestion:
    n=item["number"]
    return PracticeQuestion(
        id=item["id"], lesson_id=SOURCE_DATA["id"], question_number=n,
        difficulty="source_unspecified", cognitive_level="source_unspecified", marks=item["marks"],
        type="short_text", prompt=item["prompt"], accepted_answers=[item["answer"]],
        answer_normalisation=AnswerNormalisation(), hints=list(HINTS[n-1]),
        worked_solution=[WorkedSolutionStep(expression=line, explanation=line, why=line,
                         verification=VERIFICATIONS[n] if i==len(item["solution"])-1 else "")
                         for i,line in enumerate(item["solution"])],
        misconception_tags=item["misconception_tags"],
        verification={"original_question_check":VERIFICATIONS[n]},
        correct_feedback="Correct.", source=SOURCE, answer_hidden_before_submission=True,
    )


PRACTICE_BANK=[_practice(item) for item in SOURCE_DATA["practice_questions"]]


class AssessmentQuestion(BaseModel):
    id: str = Field(pattern=r"^g8-ae-l02-[mr]\d{2}$")
    number: int = Field(ge=1, le=5)
    prompt: str
    marks: int | None = Field(default=None, ge=1, le=10)
    answer: str
    solution: list[str] = Field(min_length=1)
    verification: str = Field(min_length=1)
    misconception_tags: list[str] = Field(default_factory=list)
    def public(self): return self.model_dump(include={"id","number","prompt","marks"})

ASSESSMENT_VERIFICATION={
    "m01":"19 - 12 = 7", "m02":"5(6) + 2 = 32", "m03":"16 - 7 = 9", "m04":"(-5)(-4) = 20", "m05":"3(R60) = R180",
    "r01":"19 - 6 = 13", "r02":"(-6)(-5) = 30", "r03":"4(R24) = R96",
}
ASSESSMENT_TAGS={
    "m01":"subtracts-variable-backwards", "m02":"ignores-operation-order", "m03":"subtracts-variable-backwards",
    "m04":"missing-negative-sign", "m05":"unit-omitted", "r01":"subtracts-variable-backwards",
    "r02":"missing-negative-sign", "r03":"unit-omitted",
}

def _assessment(item):
    suffix=item["id"].split("-")[-1]
    return AssessmentQuestion(**{**item,"verification":ASSESSMENT_VERIFICATION[suffix],"misconception_tags":[ASSESSMENT_TAGS[suffix]]})
MASTERY_BANK=[_assessment(item) for item in SOURCE_DATA["mastery_questions"]]
REASSESSMENT_BANK=[_assessment(item) for item in SOURCE_DATA["reassessment_questions"]]
MISCONCEPTION_REPAIRS={item["tag"]:{"diagnosis":item["diagnosis"],"repair":item["repair"]} for item in SOURCE_DATA["misconceptions"]}
REPAIR_RULES=SOURCE_DATA["repair_rules"]
