"""Validated contracts for self-guided practice, separate from whiteboards."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator

SOURCE_DOCUMENT = "Project_Athena_Grade12_Topic1_Sequences_and_Series_Lesson_Pack.docx"


class PracticeState(StrEnum):
    UNANSWERED = "unanswered"
    ANSWER_ENTERED = "answer_entered"
    CHECKING = "checking"
    INCORRECT_FIRST_ATTEMPT = "incorrect_first_attempt"
    INCORRECT_RETRY = "incorrect_retry"
    CORRECT = "correct"
    SOLUTION_AVAILABLE = "solution_available"
    SOLUTION_VIEWED = "solution_viewed"
    COMPLETE = "complete"


class AnswerNormalisation(BaseModel):
    trim: bool = True
    casefold: bool = True
    collapse_whitespace: bool = True
    accept_fraction_decimal_equivalence: bool = False


class WorkedSolutionStep(BaseModel):
    expression: str = Field(min_length=1, max_length=500)
    explanation: str = Field(min_length=1, max_length=700)
    why: str = Field(min_length=1, max_length=700)
    focus: list[str] = Field(default_factory=list, max_length=12)


class PracticeQuestion(BaseModel):
    id: str = Field(pattern=r"^g12-seq-l01-p\d{2}$")
    lesson_id: Literal["g12-sequences-series-01"]
    question_number: int = Field(ge=1, le=12)
    difficulty: Literal["foundation", "easy", "standard", "intermediate", "exam", "advanced"]
    cognitive_level: Literal["knowledge", "routine", "complex", "problem_solving"]
    marks: int = Field(ge=1, le=6)
    type: Literal["numeric", "short_text", "multiple_choice", "classification", "missing_term", "error_analysis"]
    prompt: str = Field(min_length=1, max_length=500)
    options: list[str] = Field(default_factory=list, max_length=8)
    accepted_answers: list[str] = Field(min_length=1, max_length=12)
    answer_normalisation: AnswerNormalisation = Field(default_factory=AnswerNormalisation)
    hints: list[str] = Field(min_length=2, max_length=3)
    worked_solution: list[WorkedSolutionStep] = Field(min_length=4, max_length=12)
    misconception_tags: list[str] = Field(default_factory=list, max_length=8)
    verification: dict[str, str] = Field(min_length=1, max_length=4)
    correct_feedback: str = Field(min_length=1, max_length=500)
    source: Literal[SOURCE_DOCUMENT] = SOURCE_DOCUMENT

    @model_validator(mode="after")
    def validate_control(self):
        if self.type in {"classification", "multiple_choice", "error_analysis"} and len(self.options) < 2:
            raise ValueError(f"{self.type} requires selectable options")
        return self


class PracticeAnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=500)


class PracticePublicQuestion(BaseModel):
    id: str
    question_number: int
    difficulty: str
    cognitive_level: str
    marks: int
    type: str
    prompt: str
    options: list[str]


class PracticeBankResponse(BaseModel):
    lesson_id: str
    title: str
    supporting_text: str
    mastery_threshold: float
    questions: list[PracticePublicQuestion]

