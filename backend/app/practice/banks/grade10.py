"""Grade 10 lesson banks: practice, mastery, reassessment, repairs and rules."""

from app.curriculum.grade10.assessment import (
    ALGEBRA_BANKS as GRADE10_ALGEBRA_BANKS,
    EEI_BANKS as GRADE10_EEI_BANKS,
    TRIG_BANKS as GRADE10_TRIG_BANKS,
    EUC_BANKS as GRADE10_EUC_BANKS,
    AG_BANKS as GRADE10_AG_BANKS,
    FN_BANKS as GRADE10_FN_BANKS,
    STAT_BANKS as GRADE10_STAT_BANKS,
    PROB_BANKS as GRADE10_PROB_BANKS,
    FIN_BANKS as GRADE10_FIN_BANKS,
    MEAS_BANKS as GRADE10_MEAS_BANKS,
)

LESSON_BANKS = {
    **{f"g10-fn-{number:02}": GRADE10_FN_BANKS[number] for number in range(1, 8)},
    **{f"g10-stat-{number:02}": GRADE10_STAT_BANKS[number] for number in range(1, 7)},
    **{f"g10-meas-{number:02}": GRADE10_MEAS_BANKS[number] for number in range(1, 7)},
    **{f"g10-fin-{number:02}": GRADE10_FIN_BANKS[number] for number in range(1, 7)},
    **{f"g10-prob-{number:02}": GRADE10_PROB_BANKS[number] for number in range(1, 6)},
    **{f"g10-ag-{number:02}": GRADE10_AG_BANKS[number] for number in range(1, 7)},
    **{f"g10-euc-{number:02}": GRADE10_EUC_BANKS[number] for number in range(1, 7)},
    **{f"g10-trig-{number:02}": GRADE10_TRIG_BANKS[number] for number in range(1, 8)},
    **{f"g10-eei-{number:02}": GRADE10_EEI_BANKS[number] for number in range(1, 10)},
    **{
        f"g10-algebra-{number:02}": GRADE10_ALGEBRA_BANKS[number]
        for number in range(1, 7)
    },
}
