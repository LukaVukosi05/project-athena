"""Private practice and assessment for Lesson 9 contextual equations."""
from __future__ import annotations

import re
from pydantic import BaseModel, Field
from app.curriculum.grade8.lesson9_runtime import SOURCE_DATA, SOURCE
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

HINTS = [
 ("What number was increased?", "Let n be that number; match n + 9 to the stated total."),
 ("Start with three times the number.", "Subtract four FROM 3x; then match the result to twenty."),
 ("Which charge happens only once?", "Put R25 outside the repeated R8 per parcel blocks."),
 ("How many physical edges does a rectangle have?", "Trace two lengths and two widths; substitute x only after solving."),
 ("Draw equal base shares first.", "Remove the extra R18, then divide the remainder into two equal shares."),
 ("How do consecutive integers change?", "Represent them by n, n+1 and n+2; their total is seventy-two."),
 ("Define the child's age first.", "The aunt is 2c+6; add their ages before solving."),
 ("Separate the rental fee from hourly costs.", "Write 40+15h=115; remove forty before counting hours."),
 ("What quantity does six less modify?", "Start with 4y, subtract six, then match the result to thirty."),
 ("Build each plan's total separately.", "Equate 100+3u and 40+6u; compare the fixed and per-use gaps."),
 ("Trace all three triangle sides.", "Add x, x+2 and 2x-1, then check all three lengths total twenty-nine."),
 ("What amount was already saved?", "Keep R90 once; multiply R30 by the number of weeks."),
 ("Which route section is longer?", "Let the first be d; the second is d+24 and both add to 164."),
 ("Name the learner count l.", "Adults are l+2; multiply both ticket prices by their respective counts."),
 ("What is the shared base pack price?", "Keep the additions INSIDE each bracket, multiply by five and two, and check the invoice."),
]

# Concise answers remain acceptable, but multipart questions require every
# requested quantity. These are authored alternatives, never AI generated.
ALTERNATIVE_ANSWERS = {
  1:["n=16","16"], 2:["x=8","8"], 3:["7","7 parcels"],
  4:["x=6; 10cm by 6cm","10cm by 6cm"],
  5:["R39 and R57","39 and 57"], 6:["23,24,25"],
  7:["child=12; aunt=30","12 and 30"], 8:["5 hours","5"],
  9:["4y-6=30; y=9"], 10:["20 uses","20"],
  11:["7cm, 9cm, 13cm"], 12:["7 weeks","7"],
  13:["70km and 94km"],
  14:["5 learner tickets and 7 adult tickets","learners=5; adults=7"],
  15:["x=R50; learner=R58; premium=R78"],
}

def _practice(item):
    n = item["number"]
    accepted = [item["answer"], item["answer"].rstrip("."), *ALTERNATIVE_ANSWERS[n]]
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
    id: str = Field(pattern=r"^g8-ae-l09-[mr]\d{2}$")
    number: int = Field(ge=1, le=5)
    prompt: str
    marks: int | None = Field(default=None, ge=1, le=10)
    answer: str
    solution: list[str] = Field(min_length=1)
    verification: str = Field(min_length=1)
    misconception_tags: list[str] = Field(default_factory=list)
    accepted_answers: list[str] = Field(default_factory=list)

    def public(self):
        return self.model_dump(include={"id","number","prompt","marks"})

ASSESSMENT_TAGS = {
    "m01":"reversed-subtraction", "m02":"fixed-fee-multiplied", "m03":"comparison-direction",
    "m04":"perimeter-pair-missed", "m05":"equation-without-equality",
    "r01":"comparison-direction", "r02":"perimeter-pair-missed", "r03":"equation-without-equality",
}
ASSESSMENT_ALTERNATIVES = {
    "m01":["13"], "m02":["7", "7 uses"],
    "m03":["R45 and R65", "45 and 65"],
    "m04":["12cm by 7cm"], "m05":["20", "20 sessions"],
    "r01":["R32 and R42", "32 and 42"],
    "r02":["8cm by 6cm"], "r03":["20", "20 visits"],
}

def _assessment(item):
    suffix = item["id"].split("-")[-1]
    return AssessmentQuestion(**{**item, "verification":item["solution"][-1],
                                 "accepted_answers":ASSESSMENT_ALTERNATIVES[suffix],
                                 "misconception_tags":[ASSESSMENT_TAGS[suffix]]})

MASTERY_BANK = [_assessment(item) for item in SOURCE_DATA["mastery_questions"]]
REASSESSMENT_BANK = [_assessment(item) for item in SOURCE_DATA["reassessment_questions"]]
MISCONCEPTION_REPAIRS = {item["tag"]:{"diagnosis":item["diagnosis"],"repair":item["repair"]}
                         for item in SOURCE_DATA["misconceptions"]}
REPAIR_RULES = SOURCE_DATA["repair_rules"]
