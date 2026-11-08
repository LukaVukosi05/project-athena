"""Grade 10 Term 1 Topic 1, authored lessons awaiting teacher review."""
from app.curriculum.schemas import ContentStatus,GradeCurriculum,Topic,Subtopic
from app.curriculum.grade9.whole_numbers_runtime import build_lesson
LESSONS={n:build_lesson(n,'grade10-algebraic-expressions') for n in range(1,7)}
EEI_LESSONS={n:build_lesson(n,'grade10-exponents-equations-inequalities') for n in range(1,10)}
GRADE_10=GradeCurriculum(id='grade-10',grade=10,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 topics=[Topic(id='algebraic-expressions',product_order=1,title='Algebraic Expressions',official_caps_topic='Algebraic expressions',
 caps_sequence=1,term=1,expected_duration='Six authored lessons awaiting teacher and browser review',
 caps_reference='DBE Grade 10 Mathematics ATP, Term 1',paper='Paper 1',
 exam_relevance='Grade 10 Paper 1 algebra and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='algebra-learning-path',order=1,title='Real numbers, expansion, factorisation and algebraic fractions',
 prerequisites=[],lessons=[LESSONS[n][0] for n in range(1,7)])]),
 Topic(id='exponents-equations-inequalities',product_order=2,title='Exponents, Equations and Inequalities',
 official_caps_topic='Exponents, equations and inequalities',caps_sequence=2,term=1,
 expected_duration='Nine authored lessons awaiting teacher and browser review',
 caps_reference='DBE Grade 10 Mathematics ATP, Term 1',paper='Paper 1',
 exam_relevance='Grade 10 Paper 1 algebra and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='eei-learning-path',order=1,title='Exponent laws, equations, word problems and inequalities',
 prerequisites=[],lessons=[EEI_LESSONS[n][0] for n in range(1,10)])])])
