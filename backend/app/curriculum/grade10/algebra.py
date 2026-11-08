"""Grade 10 Term 1 Topic 1, authored lessons awaiting teacher review."""
from app.curriculum.schemas import ContentStatus,GradeCurriculum,Topic,Subtopic
from app.curriculum.grade9.whole_numbers_runtime import build_lesson
LESSONS={n:build_lesson(n,'grade10-algebraic-expressions') for n in range(1,7)}
EEI_LESSONS={n:build_lesson(n,'grade10-exponents-equations-inequalities') for n in range(1,10)}
TRIG_LESSONS={n:build_lesson(n,'grade10-trigonometry') for n in range(1,8)}
EUC_LESSONS={n:build_lesson(n,'grade10-euclidean-geometry') for n in range(1,7)}
AG_LESSONS={n:build_lesson(n,'grade10-analytical-geometry') for n in range(1,7)}
FN_LESSONS={n:build_lesson(n,'grade10-functions-and-graphs') for n in range(1,8)}
STAT_LESSONS={n:build_lesson(n,'grade10-statistics') for n in range(1,7)}
PROB_LESSONS={n:build_lesson(n,'grade10-probability') for n in range(1,6)}
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
 prerequisites=[],lessons=[EEI_LESSONS[n][0] for n in range(1,10)])]),
 Topic(id='trigonometry',product_order=3,title='Trigonometry',official_caps_topic='Trigonometry',
 caps_sequence=3,term=1,expected_duration='Seven authored lessons awaiting teacher and browser review',
 caps_reference='DBE Grade 10 Mathematics ATP, Term 1',paper='Paper 2',
 exam_relevance='Grade 10 Paper 2 trigonometry and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='trigonometry-learning-path',order=1,title='Right triangles, unit circle, exact ratios and applications',
 prerequisites=[],lessons=[TRIG_LESSONS[n][0] for n in range(1,8)])]),
 Topic(id='euclidean-geometry',product_order=4,title='Euclidean Geometry',official_caps_topic='Euclidean geometry',
 caps_sequence=4,term=2,expected_duration='Six authored lessons awaiting teacher and browser review',
 caps_reference='DBE Grade 10 Mathematics ATP, Term 2',paper='Paper 2',
 exam_relevance='Grade 10 Paper 2 geometry and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='euclidean-learning-path',order=1,title='Angles, congruence, similarity, quadrilaterals, midpoint theorem and riders',
 prerequisites=[],lessons=[EUC_LESSONS[n][0] for n in range(1,7)])]),
 Topic(id='analytical-geometry',product_order=5,title='Analytical Geometry',official_caps_topic='Analytical Geometry',
 caps_sequence=5,term=2,expected_duration='Six authored lessons awaiting teacher and browser review',
 caps_reference='DBE Grade 10 Mathematics ATP, Term 2',paper='Paper 2',
 exam_relevance='Grade 10 Paper 2 coordinate geometry and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='analytical-learning-path',order=1,title='Distance, gradient, midpoint, line relationships and quadrilateral proof',
 prerequisites=[],lessons=[AG_LESSONS[n][0] for n in range(1,7)])]),
 Topic(id='functions-and-graphs',product_order=6,title='Functions and Graphs',official_caps_topic='Functions and graphs including trigonometric functions',
 caps_sequence=6,term=2,expected_duration='Seven authored lessons awaiting teacher and browser review',
 caps_reference='DBE Grade 10 Mathematics ATP, Term 2',paper='Paper 1',
 exam_relevance='Grade 10 Paper 1 functions and graphs and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='functions-learning-path',order=1,title='Representations, parent curves, transformations, trigonometric graphs and equation inference',
 prerequisites=[],lessons=[FN_LESSONS[n][0] for n in range(1,8)])]),
 Topic(id='statistics',product_order=7,title='Statistics',official_caps_topic='Statistics',caps_sequence=7,term=3,
 expected_duration='Six authored lessons awaiting teacher and browser review',caps_reference='DBE Grade 10 Mathematics ATP, Term 3',paper='Paper 2',
 exam_relevance='Grade 10 Paper 2 statistics and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='statistics-learning-path',order=1,title='Raw and grouped data, quartiles, box plots, histograms and comparison',
 prerequisites=[],lessons=[STAT_LESSONS[n][0] for n in range(1,7)])]),
 Topic(id='probability',product_order=8,title='Probability',official_caps_topic='Probability',caps_sequence=8,term=3,
 expected_duration='Five authored lessons awaiting teacher and browser review',caps_reference='DBE Grade 10 Mathematics ATP, Term 3',paper='Paper 1',
 exam_relevance='Grade 10 Paper 1 probability and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
 subtopics=[Subtopic(id='probability-learning-path',order=1,title='Relative frequency, Venn regions, unions, mutually exclusive and complementary events',
 prerequisites=[],lessons=[PROB_LESSONS[n][0] for n in range(1,6)])])])
