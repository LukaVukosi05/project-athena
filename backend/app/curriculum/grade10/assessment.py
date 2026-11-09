"""Private four-choice banks and diagnostic repair for Grade 10 Algebraic Expressions."""
from app.curriculum.grade9.assessment_whole_numbers import banks
ALGEBRA_BANKS={n:banks(n,'grade10') for n in range(1,7)}
EEI_BANKS={n:banks(n,'grade10_eei') for n in range(1,10)}
TRIG_BANKS={n:banks(n,'grade10_trig') for n in range(1,8)}
EUC_BANKS={n:banks(n,'grade10_euc') for n in range(1,7)}
AG_BANKS={n:banks(n,'grade10_ag') for n in range(1,7)}
FN_BANKS={n:banks(n,'grade10_fn') for n in range(1,8)}
STAT_BANKS={n:banks(n,'grade10_stat') for n in range(1,7)}
MEAS_BANKS={n:banks(n,'grade10_meas') for n in range(1,7)}
FIN_BANKS={n:banks(n,'grade10_fin') for n in range(1,7)}
PROB_BANKS={n:banks(n,'grade10_prob') for n in range(1,6)}
