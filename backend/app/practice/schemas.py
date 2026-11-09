"""Validated contracts for self-guided practice, separate from whiteboards."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator

GRADE9_1_SOURCE = "lesson-01-number-systems.md"
GRADE9_2_SOURCE = "lesson-02-prime-factors-hcf-lcm.md"
GRADE9_3_SOURCE = "lesson-03-ratio-and-rate.md"
GRADE9_4_SOURCE = "lesson-04-direct-and-inverse-proportion.md"
GRADE9_5_SOURCE = "lesson-05-percentages-and-transactions.md"
GRADE9_6_SOURCE = "lesson-06-budgets-and-accounts.md"
GRADE9_7_SOURCE = "lesson-07-loans-and-interest.md"
GRADE9_8_SOURCE = "lesson-08-exchange-commission-and-rentals.md"
GRADE9_LINE_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,6))
GRADE9_SHAPE_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,9))
GRADE9_AREA_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,6))
GRADE9_DATA_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,9))
GRADE10_ALGEBRA_SOURCES = tuple(f"grade10-algebra-lesson-{n:02}.md" for n in range(1,7))
GRADE10_EEI_SOURCES = tuple(f"grade10-eei-lesson-{n:02}.md" for n in range(1,10))
GRADE10_FN_SOURCES = tuple(f"grade10-fn-lesson-{n:02}.md" for n in range(1,8))
GRADE10_STAT_SOURCES = tuple(f"grade10-stat-lesson-{n:02}.md" for n in range(1,7))
GRADE10_FIN_SOURCES = tuple(f"grade10-fin-lesson-{n:02}.md" for n in range(1,7))
GRADE10_PROB_SOURCES = tuple(f"grade10-prob-lesson-{n:02}.md" for n in range(1,6))
GRADE10_AG_SOURCES = tuple(f"grade10-ag-lesson-{n:02}.md" for n in range(1,7))
GRADE10_EUC_SOURCES = tuple(f"grade10-euc-lesson-{n:02}.md" for n in range(1,7))
GRADE10_TRIG_SOURCES = tuple(f"grade10-trig-lesson-{n:02}.md" for n in range(1,8))
GRADE9_TRANSFORM_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,8))
GRADE9_SURFACE_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,7))
GRADE9_SOLID_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,5))
GRADE9_PROB_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,6))
GRADE9_GRAPH_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,8))
GRADE9_EQUATION_SOURCES = tuple(f"lesson-{number:02}.md" for number in range(1,7))
GRADE9_EXPONENT_SOURCES = ("lesson-01-powers-and-exponent-laws.md", "lesson-02-zero-and-negative-exponents.md",
    "lesson-03-scientific-notation-and-small-numbers.md", "lesson-04-combined-operations-and-parentheses.md",
    "lesson-05-scientific-notation-in-contexts.md", "lesson-06-exponent-error-diagnosis-and-reassessment.md")
GRADE9_FUNCTION_SOURCES = ("lesson-01-flow-diagrams-and-output-values.md", "lesson-02-input-output-tables-and-inverse-lookup.md",
    "lesson-03-formulae-and-equations.md", "lesson-04-equivalent-words-tables-formulae-and-graphs.md",
    "lesson-05-mixed-representations-and-first-error-repair.md")
GRADE9_EXPRESSION_SOURCES = ("lesson-01-algebraic-language-and-term-classification.md",
    "lesson-02-collecting-like-terms-with-fractions-and-decimals.md",
    "lesson-03-distributing-monomials-across-polynomials.md", "lesson-04-products-and-squares-of-binomials.md",
    "lesson-05-polynomial-division-and-substitution.md", "lesson-06-common-factor-factorisation.md",
    "lesson-07-difference-of-two-squares.md", "lesson-08-trinomials-and-algebraic-fractions.md",
    "lesson-09-mixed-expressions-and-first-error-repair.md")
GRADE9_PATTERN_SOURCES = ("lesson-01-visual-and-numeric-patterns.md", "lesson-02-tables-and-position-rules.md",
    "lesson-03-changing-differences-and-ratios.md", "lesson-04-general-rules-and-unknown-terms.md",
    "lesson-05-justifying-and-diagnosing-pattern-rules.md")
GRADE9_INTEGER_SOURCES = ("lesson-01-ordering-and-four-operations.md", "lesson-02-sign-rules-and-integer-properties.md",
    "lesson-03-squares-cubes-and-integer-roots.md", "lesson-04-multi-operation-integer-contexts.md",
    "lesson-05-first-error-diagnosis-and-reassessment.md")
SEQUENCES_SOURCE = "Project_Athena_Grade12_Topic1_Sequences_and_Series_Lesson_Pack.docx"
FUNCTIONS_SOURCE = "Project_Athena_Grade12_Topic2_Functions_and_Graphs_Approved_Lesson_Pack.docx"
FINANCE_SOURCE = "Project_Athena_Grade12_Topic3_Finance_Growth_and_Decay_Approved_Lesson_Pack.docx"
CALCULUS_SOURCE = "Project_Athena_Grade12_Topic4_Differential_Calculus_Approved_Lesson_Pack.docx"
ALGEBRA_SOURCE = "Project_Athena_Grade12_Topic5_Algebra_Equations_and_Inequalities_Approved_Lesson_Pack.docx"
STATISTICS_SOURCE = "Project_Athena_Grade12_Topic8_Statistics_and_Regression_Paper2_Approved_Lesson_Pack.docx"
ANALYTICAL_GEOMETRY_SOURCE = "Project_Athena_Grade12_Topic9_Analytical_Geometry_Paper2_Approved_Lesson_Pack.docx"
GRADE8_ALGEBRA_SOURCE = "Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"
GRADE8_EXPRESSIONS_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson1_Source_Pack_v1.docx"
GRADE8_EXPRESSIONS_2_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson2_Source_Pack_v1.docx"
GRADE8_EXPRESSIONS_3_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson3_Source_Pack_v1.docx"
GRADE8_EXPRESSIONS_4_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson4_Source_Pack_v1.docx"
GRADE8_EXPRESSIONS_5_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson5_Source_Pack_v1.docx"
GRADE8_EXPRESSIONS_6_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson6_Source_Pack_v1.docx"
GRADE8_EXPRESSIONS_9_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson9_Source_Pack_v1.docx"
GRADE8_EXPRESSIONS_10_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson10_Source_Pack_v1.docx"
GRADE8_FUNCTIONS_1_SOURCE = "Project_Athena_Grade8_Functions_Relationships_Lesson1_Source_Pack_v1.docx"
GRADE8_FUNCTIONS_2_SOURCE = "Project_Athena_Grade8_Functions_Relationships_Lesson2_Source_Pack_v1.docx"
GRADE8_FUNCTIONS_3_SOURCE = "Project_Athena_Grade8_Functions_Relationships_Lesson3_Source_Pack_v1.docx"
GRADE8_FUNCTIONS_4_SOURCE = "lesson-04-formulas-in-context.md"
GRADE8_FUNCTIONS_5_SOURCE = "lesson-05-matching-representations.md"
GRADE8_FUNCTIONS_6_SOURCE = "lesson-06-relationship-repair.md"
GRADE8_GRAPHS_1_SOURCE = "lesson-01-cartesian-plane-draft.md"
GRADE8_GRAPHS_2_SOURCE = "lesson-02-tables-to-graphs.md"
GRADE8_GRAPHS_3_SOURCE = "lesson-03-reading-global-graphs.md"
GRADE8_GRAPHS_4_SOURCE = "lesson-04-drawing-global-graphs.md"
GRADE8_GRAPHS_5_SOURCE = "lesson-05-comparing-global-graphs.md"
GRADE8_GRAPHS_6_SOURCE = "lesson-06-diagnosing-graph-claims.md"
GRADE8_PATTERNS_1_SOURCE = "lesson-01-numeric-rules.md"
GRADE8_PATTERNS_2_SOURCE = "lesson-02-geometric-models.md"
GRADE8_PATTERNS_3_SOURCE = "lesson-03-algebraic-rules.md"
GRADE8_PATTERNS_4_SOURCE = "lesson-04-missing-values.md"
GRADE8_PATTERNS_5_SOURCE = "lesson-05-competing-rules.md"
GRADE8_PATTERNS_6_SOURCE = "lesson-06-repair-pattern-claims.md"
GRADE8_WHOLE_1_SOURCE = "lesson-01-properties.md"
GRADE8_WHOLE_2_SOURCE = "lesson-02-factors.md"
GRADE8_INTEGER_1_SOURCE = "lesson-01-order-and-compare.md"
GRADE8_INTEGER_2_SOURCE = "lesson-02-addition-and-subtraction.md"
GRADE8_INTEGER_3_SOURCE = "lesson-03-multiplication-division.md"
GRADE8_INTEGER_4_SOURCE = "lesson-04-powers-roots.md"
GRADE8_INTEGER_5_SOURCE = "lesson-05-integer-properties.md"
GRADE8_INTEGER_6_SOURCE = "lesson-06-integer-contexts.md"
GRADE8_FRACTIONS_1_SOURCE = "lesson-01-equivalent-and-comparing.md"
GRADE8_FRACTIONS_2_SOURCE = "lesson-02-adding-and-subtracting.md"
GRADE8_FRACTIONS_3_SOURCE = "lesson-03-multiplying-fractions.md"
GRADE8_FRACTIONS_4_SOURCE = "lesson-04-dividing-fractions.md"
GRADE8_FRACTIONS_5_SOURCE = "lesson-05-powers-and-roots.md"
GRADE8_FRACTIONS_6_SOURCE = "lesson-06-fraction-contexts.md"
GRADE8_FRACTIONS_7_SOURCE = "lesson-07-percentage-of-a-whole.md"
GRADE8_FRACTIONS_8_SOURCE = "lesson-08-percentage-change.md"
GRADE8_DECIMALS_1_SOURCE = "lesson-01-place-value-comparison.md"
GRADE8_DECIMALS_2_SOURCE = "lesson-02-rounding-estimating.md"
GRADE8_DECIMALS_3_SOURCE = "lesson-03-multiplying-decimals.md"
GRADE8_DECIMALS_4_SOURCE = "lesson-04-dividing-decimals.md"
GRADE8_DECIMALS_5_SOURCE = "lesson-05-powers-of-decimals.md"
GRADE8_DECIMALS_6_SOURCE = "lesson-06-roots-of-decimals.md"
GRADE8_EXPONENTS_1_SOURCE = "lesson-01-representing-and-comparing-powers.md"
GRADE8_EXPONENTS_2_SOURCE = "lesson-02-laws-of-exponents.md"
GRADE8_EXPONENTS_3_SOURCE = "lesson-03-square-and-cube-roots.md"
GRADE8_EXPONENTS_4_SOURCE = "lesson-04-powers-and-roots-in-context.md"
GRADE8_EXPONENTS_5_SOURCE = "lesson-05-diagnosing-exponent-errors.md"
GRADE8_EXPONENTS_6_SOURCE = "lesson-06-integrated-exponents-readiness.md"
GRADE8_LINES_1_SOURCE = "geometry-of-straight-lines/lesson-01.md"
GRADE8_LINES_2_SOURCE = "geometry-of-straight-lines/lesson-02.md"
GRADE8_LINES_3_SOURCE = "geometry-of-straight-lines/lesson-03.md"
GRADE8_LINES_4_SOURCE = "geometry-of-straight-lines/lesson-04.md"
GRADE8_LINES_5_SOURCE = "geometry-of-straight-lines/lesson-05.md"
GRADE8_SHAPES_1_SOURCE = "geometry-of-2d-shapes/lesson-01.md"
GRADE8_SHAPES_2_SOURCE = "geometry-of-2d-shapes/lesson-02.md"
GRADE8_SHAPES_3_SOURCE = "geometry-of-2d-shapes/lesson-03.md"
GRADE8_SHAPES_4_SOURCE = "geometry-of-2d-shapes/lesson-04.md"
GRADE8_SHAPES_5_SOURCE = "geometry-of-2d-shapes/lesson-05.md"
GRADE8_PYTHAGORAS_1_SOURCE = "pythagoras/lesson-01.md"
GRADE8_PYTHAGORAS_2_SOURCE = "pythagoras/lesson-02.md"
GRADE8_PYTHAGORAS_3_SOURCE = "pythagoras/lesson-03.md"
GRADE8_PYTHAGORAS_4_SOURCE = "pythagoras/lesson-04.md"
GRADE8_PYTHAGORAS_5_SOURCE = "pythagoras/lesson-05.md"
GRADE8_EXPRESSIONS_8_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson8_Source_Pack_v1.docx"
GRADE8_EXPRESSIONS_7_SOURCE = "Project_Athena_Grade8_Algebraic_Expressions_Lesson7_Source_Pack_v1.docx"
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
    id: str = Field(pattern=r"^(?:g10-(?:aex|eei|trig|euc|ag|fn|stat|prob|fin)-l\d{2}-p\d{2}|g8-(?:ae|ex|fr|graphs|patterns|whole|int|frac|dec|exp|lines|shapes|pythagoras)-l\d{2}-p\d{2}|g9-(?:whole|int|exp|pat|fn|aex|eq|gr|lines|shapes|area|data|prob|solid|sv|tg)-l\d{2}-p\d{2}|g12-(?:seq|functions|finance|calculus)-l\d{2}-p\d{2}|G12-(?:ALG|STAT|AG)-L\d{2}-P\d{2})$")
    lesson_id: str = Field(pattern=r"^(?:g10-(?:algebra|eei|trig|euc|ag|fn|stat|prob|fin)|g8-(?:algebraic-(?:equations|expressions)|functions-relationships|graphs|patterns|whole-numbers|integers|common-fractions|decimal-fractions|exponents|straight-lines|shapes|pythagoras)|g9-(?:whole-numbers|integers|exponents|patterns|functions|expressions|equations|graphs|straight-lines|shapes|area|data|prob|solid|sv|tg)|g12-(?:sequences-series|functions|finance|calculus|algebra|statistics|analytical-geometry))-\d{2}$")
    question_number: int = Field(ge=1, le=15)
    difficulty: Literal["foundation", "easy", "standard", "intermediate", "exam", "advanced", "source_unspecified"]
    cognitive_level: Literal["knowledge", "routine", "complex", "problem_solving", "source_unspecified"]
    marks: int = Field(ge=1, le=10)
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
    source: Literal[*GRADE10_FN_SOURCES, *GRADE10_STAT_SOURCES, *GRADE10_PROB_SOURCES, *GRADE10_FIN_SOURCES, *GRADE10_AG_SOURCES, *GRADE10_EUC_SOURCES, *GRADE10_TRIG_SOURCES, *GRADE10_EEI_SOURCES, *GRADE10_ALGEBRA_SOURCES, *GRADE9_TRANSFORM_SOURCES, *GRADE9_SURFACE_SOURCES, *GRADE9_SOLID_SOURCES, *GRADE9_PROB_SOURCES, *GRADE9_DATA_SOURCES, *GRADE9_AREA_SOURCES, *GRADE9_SHAPE_SOURCES, *GRADE9_LINE_SOURCES, *GRADE9_GRAPH_SOURCES, *GRADE9_EQUATION_SOURCES, *GRADE9_EXPRESSION_SOURCES, *GRADE9_FUNCTION_SOURCES, *GRADE9_PATTERN_SOURCES, *GRADE9_EXPONENT_SOURCES, *GRADE9_INTEGER_SOURCES, GRADE9_1_SOURCE, GRADE9_2_SOURCE, GRADE9_3_SOURCE, GRADE9_4_SOURCE, GRADE9_5_SOURCE, GRADE9_6_SOURCE, GRADE9_7_SOURCE, GRADE9_8_SOURCE, SEQUENCES_SOURCE, FUNCTIONS_SOURCE, FINANCE_SOURCE, CALCULUS_SOURCE, ALGEBRA_SOURCE, STATISTICS_SOURCE, ANALYTICAL_GEOMETRY_SOURCE, GRADE8_ALGEBRA_SOURCE, GRADE8_EXPRESSIONS_SOURCE, GRADE8_EXPRESSIONS_2_SOURCE, GRADE8_EXPRESSIONS_3_SOURCE, GRADE8_EXPRESSIONS_4_SOURCE, GRADE8_EXPRESSIONS_5_SOURCE, GRADE8_EXPRESSIONS_6_SOURCE, GRADE8_EXPRESSIONS_7_SOURCE, GRADE8_EXPRESSIONS_8_SOURCE, GRADE8_EXPRESSIONS_9_SOURCE, GRADE8_EXPRESSIONS_10_SOURCE, GRADE8_FUNCTIONS_1_SOURCE, GRADE8_FUNCTIONS_2_SOURCE, GRADE8_FUNCTIONS_3_SOURCE, GRADE8_FUNCTIONS_4_SOURCE, GRADE8_FUNCTIONS_5_SOURCE, GRADE8_FUNCTIONS_6_SOURCE, GRADE8_GRAPHS_1_SOURCE, GRADE8_GRAPHS_2_SOURCE, GRADE8_GRAPHS_3_SOURCE, GRADE8_GRAPHS_4_SOURCE, GRADE8_GRAPHS_5_SOURCE, GRADE8_GRAPHS_6_SOURCE, GRADE8_PATTERNS_1_SOURCE, GRADE8_PATTERNS_2_SOURCE, GRADE8_PATTERNS_3_SOURCE, GRADE8_PATTERNS_4_SOURCE, GRADE8_PATTERNS_5_SOURCE, GRADE8_PATTERNS_6_SOURCE, GRADE8_WHOLE_1_SOURCE, GRADE8_WHOLE_2_SOURCE, GRADE8_INTEGER_1_SOURCE, GRADE8_INTEGER_2_SOURCE, GRADE8_INTEGER_3_SOURCE, GRADE8_INTEGER_4_SOURCE, GRADE8_INTEGER_5_SOURCE, GRADE8_INTEGER_6_SOURCE, GRADE8_FRACTIONS_1_SOURCE, GRADE8_FRACTIONS_2_SOURCE, GRADE8_FRACTIONS_3_SOURCE, GRADE8_FRACTIONS_4_SOURCE, GRADE8_FRACTIONS_5_SOURCE, GRADE8_FRACTIONS_6_SOURCE, GRADE8_FRACTIONS_7_SOURCE, GRADE8_FRACTIONS_8_SOURCE, GRADE8_DECIMALS_1_SOURCE, GRADE8_DECIMALS_2_SOURCE, GRADE8_DECIMALS_3_SOURCE, GRADE8_DECIMALS_4_SOURCE, GRADE8_DECIMALS_5_SOURCE, GRADE8_DECIMALS_6_SOURCE, GRADE8_EXPONENTS_1_SOURCE, GRADE8_EXPONENTS_2_SOURCE, GRADE8_EXPONENTS_3_SOURCE, GRADE8_EXPONENTS_4_SOURCE, GRADE8_EXPONENTS_5_SOURCE, GRADE8_EXPONENTS_6_SOURCE, GRADE8_LINES_1_SOURCE, GRADE8_LINES_2_SOURCE, GRADE8_LINES_3_SOURCE, GRADE8_LINES_4_SOURCE, GRADE8_LINES_5_SOURCE, GRADE8_SHAPES_1_SOURCE, GRADE8_SHAPES_2_SOURCE, GRADE8_SHAPES_3_SOURCE, GRADE8_SHAPES_4_SOURCE, GRADE8_SHAPES_5_SOURCE, GRADE8_PYTHAGORAS_1_SOURCE, GRADE8_PYTHAGORAS_2_SOURCE, GRADE8_PYTHAGORAS_3_SOURCE, GRADE8_PYTHAGORAS_4_SOURCE, GRADE8_PYTHAGORAS_5_SOURCE] = SEQUENCES_SOURCE
    expected_evidence: str | None = None
    feedback_route: str | None = None
    operation_signature: list[str] = Field(default_factory=list)
    reasoning_demands: list[str] = Field(default_factory=list)
    answer_tolerance: float | None = Field(default=None, ge=0)
    approximate_answer: bool = False
    answer_hidden_before_submission: bool = True

    @model_validator(mode="after")
    def validate_control(self):
        if self.lesson_id.startswith("g12-") and len(self.worked_solution) < 4:
            raise ValueError("Grade 12 practice requires at least four worked-solution steps")
        if self.lesson_id.startswith(("g9-","g10-")) and (self.type != "multiple_choice" or len(self.options) != 4 or len(set(self.options)) != 4 or len(self.accepted_answers) != 1 or self.accepted_answers[0] not in self.options):
            raise ValueError("Grade 9 practice requires four distinct options and one matching correct answer")
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
