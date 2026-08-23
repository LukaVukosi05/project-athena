"""Typed curriculum, lesson-block and whiteboard contracts."""

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator


class ContentStatus(StrEnum):
    DRAFT = "draft"
    AI_ASSISTED = "ai_assisted"
    TEACHER_REVIEW_REQUIRED = "teacher_review_required"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class AccessLevel(StrEnum):
    FREE = "free"
    PREMIUM = "premium"


class StepExplanation(BaseModel):
    what: str = Field(min_length=1)
    why: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    remember: str = Field(min_length=1)


class MathematicalOperation(BaseModel):
    type: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    value: int | float | str | None = None


class TeachingStep(BaseModel):
    step_number: int = Field(ge=0)
    title: str
    before_expression: str
    working_expression: str | None = None
    operation: MathematicalOperation
    after_expression: str
    explanation: StepExplanation
    common_mistake: str | None = None
    animation_template: str
    screen_reader_description: str


class WhiteboardBlock(BaseModel):
    type: Literal["whiteboard"] = "whiteboard"
    id: str
    problem: str
    initial_expression: str
    steps: list[TeachingStep] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_state_chain(self):
        expected = list(range(len(self.steps)))
        if [step.step_number for step in self.steps] != expected:
            raise ValueError("Whiteboard step numbers must be contiguous from zero")
        if self.steps[0].before_expression != self.initial_expression:
            raise ValueError("First step must begin at the initial expression")
        for previous, current in zip(self.steps, self.steps[1:]):
            if previous.after_expression != current.before_expression:
                raise ValueError("Whiteboard states must form a deterministic chain")
        return self


class WhiteboardQuestion(BaseModel):
    id: str
    order: int = Field(ge=1)
    difficulty: Literal["foundation", "easy", "standard", "intermediate", "exam", "advanced", "expert"]
    estimated_minutes: int = Field(default=4, ge=1, le=20)
    is_core_example: bool = False
    guidance_level: Literal["high", "moderate", "reduced", "minimal"] = "high"
    whiteboard: WhiteboardBlock


class LessonBlock(BaseModel):
    type: Literal["concept", "checkpoint", "practice", "mistake", "memory_tip", "summary", "past_paper_question"]
    title: str
    content: str
    data: dict[str, Any] = Field(default_factory=dict)


class Lesson(BaseModel):
    id: str
    order: int = Field(ge=1)
    title: str
    objective: str
    why_it_matters: str
    intuition: str
    prerequisites: list[str] = Field(default_factory=list)
    estimated_minutes: int | None = Field(default=None, ge=1)
    difficulty: Literal["foundation", "standard", "exam", "challenge"]
    access_level: AccessLevel
    status: ContentStatus
    blocks: list[LessonBlock | WhiteboardBlock]
    whiteboard_questions: list[WhiteboardQuestion] = Field(default_factory=list, max_length=15)
    mastery_threshold: float = Field(default=0.7, ge=0, le=1)

    @model_validator(mode="after")
    def validate_whiteboard_question_set(self):
        if self.whiteboard_questions:
            orders = [question.order for question in self.whiteboard_questions]
            if orders != list(range(1, len(orders) + 1)):
                raise ValueError("Whiteboard question order must be contiguous from one")
            if sum(question.is_core_example for question in self.whiteboard_questions) != 1:
                raise ValueError("A whiteboard question set must have exactly one core example")
        return self


class Subtopic(BaseModel):
    id: str
    order: int = Field(ge=1)
    title: str
    prerequisites: list[str] = Field(default_factory=list)
    lessons: list[Lesson] = Field(default_factory=list)


class Topic(BaseModel):
    id: str
    product_order: int = Field(ge=0)
    title: str
    official_caps_topic: str | None = None
    caps_sequence: int | None = None
    term: int | None = Field(default=None, ge=1, le=4)
    expected_duration: str | None = None
    paper: Literal["Paper 1", "Paper 2", "Both", "Readiness"]
    caps_reference: str | None = None
    curriculum: Literal["CAPS"] = "CAPS"
    ieb_relevant: bool = True
    ieb_notes: str | None = None
    ieb_assessment_tags: list[str] = Field(default_factory=list)
    exam_relevance: str | None = None
    status: ContentStatus
    subtopics: list[Subtopic]


class GradeCurriculum(BaseModel):
    id: str
    grade: int = Field(ge=8, le=12)
    subject: Literal["Mathematics"] = "Mathematics"
    status: ContentStatus
    topics: list[Topic]
