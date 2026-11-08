"""Grade 10 Term 1 Topic 1, authored lessons awaiting teacher review."""
from app.curriculum.schemas import ContentStatus,GradeCurriculum,Topic,Subtopic
from app.curriculum.grade9.whole_numbers_runtime import build_lesson
LESSONS={n:build_lesson(n,'grade10-algebraic-expressions') for n in range(1,7)}
GRADE_10=GradeCurriculum(id='grade-10',grade=10,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 topics=[Topic(id='algebraic-expressions',product_order=1,title='Algebraic Expressions',official_caps_topic='Algebraic expressions',
 caps_sequence=1,term=1,expected_duration='Six authored lessons awaiting teacher and browser review',
 caps_reference='DBE Grade 10 Mathematics ATP, Term 1',paper='Paper 1',
 exam_relevance='Grade 10 Paper 1 algebra and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='algebra-learning-path',order=1,title='Real numbers, expansion, factorisation and algebraic fractions',
 prerequisites=[],lessons=[LESSONS[n][0] for n in range(1,7)])])])
