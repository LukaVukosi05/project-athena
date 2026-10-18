"""Active curriculum catalogue: approved Grade 12 Sequences and Series pack only."""

from app.curriculum.grade12.lessons.sequences_series import SEQUENCES_SERIES
from app.curriculum.grade12.lessons.functions_graphs import FUNCTIONS_GRAPH_LESSONS
from app.curriculum.grade12.lessons.finance_growth_decay import FINANCE_GROWTH_DECAY_LESSONS
from app.curriculum.grade12.lessons.differential_calculus import DIFFERENTIAL_CALCULUS_LESSONS
from app.curriculum.grade12.lessons.algebra_equations_inequalities import ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS
from app.curriculum.grade12.lessons.paper2_topics import (
    ANALYTICAL_GEOMETRY_LESSONS, STATISTICS_REGRESSION_LESSONS,
)
from app.curriculum.schemas import ContentStatus, GradeCurriculum, Subtopic, Topic


SEQUENCES_TOPIC = Topic(
    id="sequences-series",
    product_order=1,
    title="Sequences and Series",
    official_caps_topic="Patterns, Sequences and Series",
    caps_sequence=1,
    term=1,
    expected_duration="18 lessons",
    paper="Paper 1",
    caps_reference="CAPS Grade 12 Mathematics — Patterns, Sequences and Series",
    curriculum="CAPS",
    ieb_relevant=True,
    ieb_notes="CAPS-aligned with additional proof-of-understanding and unfamiliar-problem preparation.",
    ieb_assessment_tags=["sequences", "series", "algebraic reasoning"],
    exam_relevance="Grade 12 Paper 1",
    status=ContentStatus.DRAFT,
    subtopics=[Subtopic(
        id="sequences-series-learning-path",
        order=1,
        title="Approved 18-lesson learning path",
        prerequisites=[],
        lessons=SEQUENCES_SERIES,
    )],
)

FUNCTIONS_GRAPHS_TOPIC = Topic(
    id="functions-graphs",
    product_order=2,
    title="Functions and Graphs",
    official_caps_topic="Functions and Graphs",
    caps_sequence=2,
    term=1,
    expected_duration="18 lessons",
    paper="Paper 1",
    caps_reference="CAPS Grade 12 Mathematics — Functions and Graphs",
    curriculum="CAPS",
    ieb_relevant=True,
    ieb_notes="Scheduled for source conversion and teacher review.",
    ieb_assessment_tags=["functions", "graphs", "inverse functions"],
    exam_relevance="Grade 12 Paper 1 — approximately 35 marks",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(
        id="functions-graphs-learning-path",
        order=1,
        title="Approved 18-lesson learning path",
        prerequisites=["sequences-series"],
        lessons=FUNCTIONS_GRAPH_LESSONS,
    )],
)

FINANCE_GROWTH_DECAY_TOPIC = Topic(
    id="finance-growth-decay",
    product_order=3,
    title="Finance, Growth and Decay",
    official_caps_topic="Finance, Growth and Decay",
    caps_sequence=3,
    term=1,
    expected_duration="16 lessons",
    paper="Paper 1",
    caps_reference="CAPS Grade 12 Mathematics — Finance, Growth and Decay",
    curriculum="CAPS",
    ieb_relevant=True,
    ieb_notes="Approved pack converted in controlled batches; Lessons 1–3 await teacher review.",
    ieb_assessment_tags=["financial mathematics", "growth and decay", "annuities"],
    exam_relevance="Grade 12 Paper 1 — approximately 15 marks",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(
        id="finance-growth-decay-learning-path",
        order=1,
        title="Approved 16-lesson learning path",
        prerequisites=["functions-graphs"],
        lessons=FINANCE_GROWTH_DECAY_LESSONS,
    )],
)

DIFFERENTIAL_CALCULUS_TOPIC = Topic(
    id="differential-calculus", product_order=4, title="Differential Calculus",
    official_caps_topic="Differential Calculus", caps_sequence=4, term=2,
    expected_duration="24 lessons", paper="Paper 1",
    caps_reference="CAPS Grade 12 Mathematics — Differential Calculus",
    curriculum="CAPS", ieb_relevant=True,
    ieb_notes="Approved pack converted in controlled batches; Lessons 1–6 await teacher review.",
    ieb_assessment_tags=["calculus", "derivatives", "optimisation"],
    exam_relevance="Grade 12 Paper 1 — approximately 35 marks",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="differential-calculus-learning-path", order=1,
        title="Approved 24-lesson learning path", prerequisites=["finance-growth-decay"],
        lessons=DIFFERENTIAL_CALCULUS_LESSONS)],
)

ALGEBRA_EQUATIONS_INEQUALITIES_TOPIC = Topic(
    id="algebra-equations-inequalities", product_order=5,
    title="Algebra, Equations and Inequalities",
    official_caps_topic="Algebra, Equations and Inequalities", caps_sequence=5, term=2,
    expected_duration="18 lessons", paper="Paper 1",
    caps_reference="CAPS Grade 12 Mathematics — Algebra, Equations and Inequalities",
    curriculum="CAPS", ieb_relevant=True,
    ieb_notes="Approved integration source with 10 whiteboards and 12 practice items per lesson.",
    ieb_assessment_tags=["algebra", "equations", "inequalities"],
    exam_relevance="Grade 12 Paper 1 — approximately 25 marks",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="algebra-equations-inequalities-learning-path",order=1,
        title="Approved 18-lesson learning path",prerequisites=["differential-calculus"],
        lessons=ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS)],
)

STATISTICS_REGRESSION_TOPIC = Topic(
    id="statistics-regression", product_order=8, title="Statistics and Regression",
    official_caps_topic="Statistics and Regression", caps_sequence=8, term=3,
    expected_duration="18 lessons", paper="Paper 2", paper_number=2, grade=12,
    subject="Mathematics", official_weighting=20,
    caps_reference="CAPS Grade 12 Mathematics — Statistics and Regression",
    curriculum="CAPS", ieb_relevant=True,
    ieb_notes="Approved Paper 2 pack with 10 guided examples and 12 independent items per lesson.",
    ieb_assessment_tags=["statistics", "regression", "data interpretation"],
    exam_relevance="Grade 12 Paper 2 — 20 marks",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="statistics-regression-learning-path", order=1,
        title="Approved 18-lesson Paper 2 learning path", prerequisites=[],
        lessons=STATISTICS_REGRESSION_LESSONS)],
)

ANALYTICAL_GEOMETRY_TOPIC = Topic(
    id="analytical-geometry", product_order=9, title="Analytical Geometry",
    official_caps_topic="Analytical Geometry", caps_sequence=9, term=3,
    expected_duration="16 lessons", paper="Paper 2", paper_number=2, grade=12,
    subject="Mathematics", official_weighting=40,
    caps_reference="CAPS Grade 12 Mathematics — Analytical Geometry",
    curriculum="CAPS", ieb_relevant=True,
    ieb_notes="Approved Paper 2 pack with 10 guided examples and 12 independent items per lesson.",
    ieb_assessment_tags=["analytical geometry", "circles", "coordinate proof"],
    exam_relevance="Grade 12 Paper 2 — 40 marks",
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    subtopics=[Subtopic(id="analytical-geometry-learning-path", order=1,
        title="Approved 16-lesson Paper 2 learning path", prerequisites=["statistics-regression"],
        lessons=ANALYTICAL_GEOMETRY_LESSONS)],
)


GRADE_12 = GradeCurriculum(
    id="grade-12",
    grade=12,
    status=ContentStatus.DRAFT,
    topics=[SEQUENCES_TOPIC, FUNCTIONS_GRAPHS_TOPIC, FINANCE_GROWTH_DECAY_TOPIC,
            DIFFERENTIAL_CALCULUS_TOPIC, ALGEBRA_EQUATIONS_INEQUALITIES_TOPIC,
            STATISTICS_REGRESSION_TOPIC, ANALYTICAL_GEOMETRY_TOPIC],
)
