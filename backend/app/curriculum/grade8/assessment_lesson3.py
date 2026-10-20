"""Private practice, mastery, and parallel checks for additive inverses."""
from __future__ import annotations

from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson3_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

HINTS = [
 ("What cancels a positive eight?", "Apply the inverse on both complete sides."),
 ("What cancels negative six?", "Add the same amount to each side."),
 ("Remove positive fourteen equally.", "Count back from five on a signed number line."),
 ("Undo subtracting nine.", "Jump right from negative three."),
 ("Cancel positive twenty-one.", "Combine the negative counters on the right."),
 ("Cancel negative eighteen.", "Pair eighteen positive counters with negative counters."),
 ("Test the learner's claimed value first.", "Negative twelve needs positive twelve to make zero."),
 ("Reorder five plus p as p plus five.", "Subtract five equally from both sides."),
 ("Express both decimals in tenths.", "Subtract forty-eight tenths from ninety-three tenths."),
 ("Add two thirds to both complete sides.", "Convert the right-hand fractions into sixths."),
 ("Keep the minus attached to x.", "Find the opposite of the resulting positive quantity."),
 ("Represent the temperature fall with subtraction.", "Reverse the fall by adding seventeen."),
 ("Write a bill plus service fee equation.", "Remove the fee equally from both sides."),
 ("Subtracting negative nine means adding nine.", "Undo that addition equally on both sides."),
 ("Show the same subtraction of c on each side.", "Substituting negative c means subtracting a negative."),
]

VERIFICATIONS = {
 1:"11 + 8 = 19",2:"23 - 6 = 17",3:"-9 + 14 = 5",4:"6 - 9 = -3",5:"-29 + 21 = -8",
 6:"-7 - 18 = -25",7:"32 - 12 = 20",8:"5 + (-17) = -12",9:"4.5 + 4.8 = 9.3",
 10:"1 5/6 - 2/3 = 1 1/6",11:"-(-7) + 9 = 16",12:"11 - 17 = -6",
 13:"R277 + R49 = R326",14:"-13 - (-9) = -4",15:"19 + (-12) = 7",
}


def _practice(item):
    n=item["number"]
    return PracticeQuestion(
        id=item["id"],lesson_id=SOURCE_DATA["id"],question_number=n,
        difficulty="source_unspecified",cognitive_level="source_unspecified",marks=item["marks"],
        type="short_text",prompt=item["prompt"],accepted_answers=[item["answer"]],
        answer_normalisation=AnswerNormalisation(),hints=list(HINTS[n-1]),
        worked_solution=[WorkedSolutionStep(expression=line,explanation=line,why=line,
                         verification=VERIFICATIONS[n] if index==len(item["solution"])-1 else "")
                         for index,line in enumerate(item["solution"])],
        misconception_tags=item["misconception_tags"],
        verification={"original_question_check":VERIFICATIONS[n]},
        correct_feedback="Correct.",source=SOURCE,answer_hidden_before_submission=True,
    )


PRACTICE_BANK=[_practice(item) for item in SOURCE_DATA["practice_questions"]]


class AssessmentQuestion(BaseModel):
    id: str = Field(pattern=r"^g8-ae-l03-[mr]\d{2}$")
    number: int = Field(ge=1,le=5)
    prompt: str
    marks: int | None = Field(default=None,ge=1,le=10)
    answer: str
    solution: list[str] = Field(min_length=1)
    verification: str = Field(min_length=1)
    misconception_tags: list[str] = Field(default_factory=list)

    def public(self):
        return self.model_dump(include={"id","number","prompt","marks"})


ASSESSMENT_VERIFICATION={
 "m01":"8 + 13 = 21","m02":"11 - 16 = -5","m03":"-23 + 9 = -14","m04":"23 - 8 = 15","m05":"R118 + R27 = R145",
 "r01":"4 - 11 = -7","r02":"-19 + 17 = -2","r03":"R178 + R32 = R210",
}
ASSESSMENT_TAGS={
 "m01":"change-side-change-sign","m02":"wrong-inverse","m03":"integer-sign-error",
 "m04":"wrong-inverse","m05":"verification-omitted","r01":"wrong-inverse",
 "r02":"integer-sign-error","r03":"verification-omitted",
}


def _assessment(item):
    suffix=item["id"].split("-")[-1]
    return AssessmentQuestion(**{**item,"verification":ASSESSMENT_VERIFICATION[suffix],
                                 "misconception_tags":[ASSESSMENT_TAGS[suffix]]})


MASTERY_BANK=[_assessment(item) for item in SOURCE_DATA["mastery_questions"]]
REASSESSMENT_BANK=[_assessment(item) for item in SOURCE_DATA["reassessment_questions"]]
MISCONCEPTION_REPAIRS={item["tag"]:{"diagnosis":item["diagnosis"],"repair":item["repair"]}
                       for item in SOURCE_DATA["misconceptions"]}
REPAIR_RULES=SOURCE_DATA["repair_rules"]
