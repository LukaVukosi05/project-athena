"""Grade 11 lesson banks: practice, mastery, reassessment, repairs and rules."""

from app.curriculum.grade11.assessment import BANKS as GRADE11_ES_BANKS
from app.curriculum.grade11.assessment_equations import BANKS as GRADE11_EI_BANKS
from app.curriculum.grade11.assessment_trigonometry import BANKS as GRADE11_TR_BANKS
from app.curriculum.grade11.assessment_euclidean import BANKS as GRADE11_EUC_BANKS
from app.curriculum.grade11.assessment_analytical import BANKS as GRADE11_AG_BANKS
from app.curriculum.grade11.assessment_functions import BANKS as GRADE11_FN_BANKS
from app.curriculum.grade11.assessment_triangle_rules import (
    BANKS as GRADE11_RULES_BANKS,
)
from app.curriculum.grade11.assessment_statistics import BANKS as GRADE11_STAT_BANKS
from app.curriculum.grade11.assessment_probability import BANKS as GRADE11_PROB_BANKS
from app.curriculum.grade11.assessment_finance import BANKS as GRADE11_FIN_BANKS
from app.curriculum.grade11.assessment_patterns import BANKS as GRADE11_PAT_BANKS
from app.curriculum.grade11.assessment_measurement_review import (
    BANKS as GRADE11_MEAS_BANKS,
)

LESSON_BANKS = {
    **{f"g11-fn-{number:02}": GRADE11_FN_BANKS[number] for number in range(1, 9)},
    **{f"g11-rules-{number:02}": GRADE11_RULES_BANKS[number] for number in range(1, 6)},
    **{f"g11-stat-{number:02}": GRADE11_STAT_BANKS[number] for number in range(1, 8)},
    **{f"g11-prob-{number:02}": GRADE11_PROB_BANKS[number] for number in range(1, 8)},
    **{f"g11-fin-{number:02}": GRADE11_FIN_BANKS[number] for number in range(1, 7)},
    **{f"g11-pat-{number:02}": GRADE11_PAT_BANKS[number] for number in range(1, 6)},
    **{f"g11-meas-{number:02}": GRADE11_MEAS_BANKS[number] for number in range(1, 5)},
    **{f"g11-ag-{number:02}": GRADE11_AG_BANKS[number] for number in range(1, 7)},
    **{f"g11-euc-{number:02}": GRADE11_EUC_BANKS[number] for number in range(1, 9)},
    **{f"g11-tr-{number:02}": GRADE11_TR_BANKS[number] for number in range(1, 8)},
    **{f"g11-ei-{number:02}": GRADE11_EI_BANKS[number] for number in range(1, 8)},
    **{f"g11-es-{number:02}": GRADE11_ES_BANKS[number] for number in range(1, 7)},
}
