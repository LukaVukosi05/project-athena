"""Validated contracts for self-guided practice, separate from whiteboards."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator

SEQUENCES_SOURCE = "Project_Athena_Grade12_Topic1_Sequences_and_Series_Lesson_Pack.docx"
FUNCTIONS_SOURCE = "Project_Athena_Grade12_Topic2_Functions_and_Graphs_Approved_Lesson_Pack.docx"
FINANCE_SOURCE = "Project_Athena_Grade12_Topic3_Finance_Growth_and_Decay_Approved_Lesson_Pack.docx"
CALCULUS_SOURCE = "Project_Athena_Grade12_Topic4_Differential_Calculus_Approved_Lesson_Pack.docx"
ALGEBRA_SOURCE = "Project_Athena_Grade12_Topic5_Algebra_Equations_and_Inequalities_Approved_Lesson_Pack.docx"
STATISTICS_SOURCE = "Project_Athena_Grade12_Topic8_Statistics_and_Regression_Paper2_Approved_Lesson_Pack.docx"
ANALYTICAL_GEOMETRY_SOURCE = "Project_Athena_Grade12_Topic9_Analytical_Geometry_Paper2_Approved_Lesson_Pack.docx"
GRADE8_ALGEBRA_SOURCE = "Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"
SOURCE_DOCUMENT = SEQUENCES_SOURCE


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
    verification: str = Field(default="", max_length=700)


class PracticeQuestion(BaseModel):
    id: str = Field(pattern=r"^(?:g8-ae-l\d{2}-p\d{2}|g12-(?:seq|functions|finance|calculus)-l\d{2}-p\d{2}|G12-(?:ALG|STAT|AG)-L\d{2}-P\d{2})$")
    lesson_id: str = Field(pattern=r"^(?:g8-algebraic-equations|g12-(?:sequences-series|functions|finance|calculus|algebra|statistics|analytical-geometry))-\d{2}$")
    question_number: int = Field(ge=1, le=15)
    difficulty: Literal["foundation", "easy", "standard", "intermediate", "exam", "advanced", "source_unspecified"]
    cognitive_level: Literal["knowledge", "routine", "complex", "problem_solving", "source_unspecified"]
    marks: int = Field(ge=1, le=6)
    type: Literal["numeric", "short_text", "multiple_choice", "classification", "missing_term", "error_analysis"]
    prompt: str = Field(min_length=1, max_length=500)
    options: list[str] = Field(default_factory=list, max_length=8)
    accepted_answers: list[str] = Field(min_length=1, max_length=12)
    answer_normalisation: AnswerNormalisation = Field(default_factory=AnswerNormalisation)
    hints: list[str] = Field(min_length=2, max_length=3)
    worked_solution: list[WorkedSolutionStep] = Field(min_length=2, max_length=12)
    misconception_tags: list[str] = Field(default_factory=list, max_length=8)
    verification: dict[str, str] = Field(min_length=1, max_length=4)
    correct_feedback: str = Field(min_length=1, max_length=500)
    source: Literal[SEQUENCES_SOURCE, FUNCTIONS_SOURCE, FINANCE_SOURCE, CALCULUS_SOURCE, ALGEBRA_SOURCE, STATISTICS_SOURCE, ANALYTICAL_GEOMETRY_SOURCE, GRADE8_ALGEBRA_SOURCE] = SEQUENCES_SOURCE
    expected_evidence: str | None = None
    feedback_route: str | None = None
    operation_signature: list[str] = Field(default_factory=list)
    reasoning_demands: list[str] = Field(default_factory=list)
    answer_tolerance: float | None = Field(default=None, ge=0)
    approximate_answer: bool = False
    answer_hidden_before_submission: bool = True

    @model_validator(mode="after")
    def validate_control(self):
        if not self.lesson_id.startswith("g8-") and len(self.worked_solution) < 4:
            raise ValueError("Grade 12 practice requires at least four worked-solution steps")
        if self.type in {"classification", "multiple_choice", "error_analysis"} and len(self.options) < 2:
            raise ValueError(f"{self.type} requires selectable options")
        return self


class PracticeAnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=500)


class AssessmentSubmission(BaseModel):
    answers: dict[str, str] = Field(min_length=1, max_length=15)


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
