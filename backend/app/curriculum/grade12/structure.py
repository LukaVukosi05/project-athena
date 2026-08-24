"""Active curriculum catalogue: approved Grade 12 Sequences and Series pack only."""

from app.curriculum.grade12.lessons.sequences_series import SEQUENCES_SERIES
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


GRADE_12 = GradeCurriculum(
    id="grade-12",
    grade=12,
    status=ContentStatus.DRAFT,
    topics=[SEQUENCES_TOPIC],
)
