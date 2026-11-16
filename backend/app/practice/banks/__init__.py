"""Single registration point for practice and assessment content in Grades 8–11."""

from app.practice.banks.grade8 import LESSON_BANKS as GRADE8_BANKS
from app.practice.banks.grade9 import LESSON_BANKS as GRADE9_BANKS
from app.practice.banks.grade10 import LESSON_BANKS as GRADE10_BANKS
from app.practice.banks.grade11 import LESSON_BANKS as GRADE11_BANKS

LESSON_BANKS = {**GRADE8_BANKS, **GRADE9_BANKS, **GRADE10_BANKS, **GRADE11_BANKS}
