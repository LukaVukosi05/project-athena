"""Private four-choice banks and diagnostic repair for Grade 10 Algebraic Expressions."""
from app.curriculum.grade9.assessment_whole_numbers import banks
ALGEBRA_BANKS={n:banks(n,'grade10') for n in range(1,7)}
EEI_BANKS={n:banks(n,'grade10_eei') for n in range(1,10)}
