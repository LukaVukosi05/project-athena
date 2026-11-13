# Grade 11 Topic 10, Lesson 6: Integrated growth, decay and finance diagnosis

Curriculum: [DBE Grade 11 ATP](https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf) and [Mathematics CAPS](https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20FET%20_%20MATHEMATICS%20_%20GR%2010-12%20_%20Web_1133.pdf).

Original Athena questions, not past-paper transcriptions. Teacher review and live browser acceptance required.

Calculation convention: use Decimal arithmetic; retain full precision until the last rounding to cents, two-decimal rates or whole people. Exchange quote is rand per foreign unit; fees excluded.

## g11-fin-l06-w01: R3,165.00 earns 6.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "compare_methods", "principal": "3165", "rate": "0.06", "years": 3}}`

1. Simple interest gives Aₛ = 3,165.00 × (1 + 0.06 × 3) = R3,734.70.

2. Compound interest gives A꜀ = 3,165.00 × (1 + 0.06)^3.

3. Evaluate the compound power before rounding: A꜀ = R3,769.57.

4. Compare R3,769.57 with R3,734.70; compound growth is larger for this positive rate and multiple years.

5. Answer: Compound amount = R3,769.57 compound amount. The difference is R34.87.

Answer: Compound amount = R3,769.57. Check: Answer: Compound amount = R3,769.57 compound amount. The difference is R34.87.

## g11-fin-l06-w02: A bank advertises 7.00% nominal interest compounded quarterly. A learner calls 7.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "rate_diagnosis", "principal": "3330", "rate": "0.07", "periods": 4, "years": 1}}`

1. The quoted 7.00% is nominal, with 4 compounding periods per year.

2. The learner ignored compounding: first divide the nominal rate by 4 to get 0.017500 per quarter.

3. Then compound four periods: (1 + 0.07/4)^4 − 1.

4. The effective annual rate is 7.19%; it differs from the advertised nominal rate.

5. Answer: Effective annual rate = 7.19% effective annually. The first error was equating nominal and effective rates.

Answer: Effective annual rate = 7.19%. Check: Answer: Effective annual rate = 7.19% effective annually. The first error was equating nominal and effective rates.

## g11-fin-l06-w03: A price of R3,495.00 rises 8.00% each year for 2 years, then falls 6.00% once. Find its final price; explain why the percentages cannot simply be subtracted.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "growth_then_decay", "principal": "3495", "rate": "0.08", "decline": "0.06", "years": 2}}`

1. The first growth applies 2 times to the changing balance: R3,495.00 × (1 + 0.08)^2.

2. The price after growth is approximately R4,076.57; retain the unrounded balance.

3. The final fall applies to the unrounded new price: 3,495.00 × (1 + 0.08)^2 × (1 − 0.06).

4. This gives R3,831.97. The two percentage changes use different bases.

5. Answer: Final price = R3,831.97. Check by multiplying the two factors, not subtracting their percentages.

Answer: Final price = R3,831.97. Check: Answer: Final price = R3,831.97. Check by multiplying the two factors, not subtracting their percentages.

## g11-fin-l06-w04: R3,660.00 earns 9.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "compare_methods", "principal": "3660", "rate": "0.09", "years": 3}}`

1. Simple interest gives Aₛ = 3,660.00 × (1 + 0.09 × 3) = R4,648.20.

2. Compound interest gives A꜀ = 3,660.00 × (1 + 0.09)^3.

3. Evaluate the compound power before rounding: A꜀ = R4,739.81.

4. Compare R4,739.81 with R4,648.20; compound growth is larger for this positive rate and multiple years.

5. Answer: Compound amount = R4,739.81 compound amount. The difference is R91.61.

Answer: Compound amount = R4,739.81. Check: Answer: Compound amount = R4,739.81 compound amount. The difference is R91.61.

## g11-fin-l06-w05: A bank advertises 10.0% nominal interest compounded quarterly. A learner calls 10.0% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "rate_diagnosis", "principal": "3825", "rate": "0.1", "periods": 4, "years": 1}}`

1. The quoted 10.0% is nominal, with 4 compounding periods per year.

2. The learner ignored compounding: first divide the nominal rate by 4 to get 0.025000 per quarter.

3. Then compound four periods: (1 + 0.1/4)^4 − 1.

4. The effective annual rate is 10.38%; it differs from the advertised nominal rate.

5. Answer: Effective annual rate = 10.38% effective annually. The first error was equating nominal and effective rates.

Answer: Effective annual rate = 10.38%. Check: Answer: Effective annual rate = 10.38% effective annually. The first error was equating nominal and effective rates.

## g11-fin-l06-w06: A price of R3,990.00 rises 11.00% each year for 2 years, then falls 3.00% once. Find its final price; explain why the percentages cannot simply be subtracted.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "growth_then_decay", "principal": "3990", "rate": "0.11", "decline": "0.03", "years": 2}}`

1. The first growth applies 2 times to the changing balance: R3,990.00 × (1 + 0.11)^2.

2. The price after growth is approximately R4,916.08; retain the unrounded balance.

3. The final fall applies to the unrounded new price: 3,990.00 × (1 + 0.11)^2 × (1 − 0.03).

4. This gives R4,768.60. The two percentage changes use different bases.

5. Answer: Final price = R4,768.60. Check by multiplying the two factors, not subtracting their percentages.

Answer: Final price = R4,768.60. Check: Answer: Final price = R4,768.60. Check by multiplying the two factors, not subtracting their percentages.

## g11-fin-l06-w07: R4,155.00 earns 12.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "compare_methods", "principal": "4155", "rate": "0.12", "years": 3}}`

1. Simple interest gives Aₛ = 4,155.00 × (1 + 0.12 × 3) = R5,650.80.

2. Compound interest gives A꜀ = 4,155.00 × (1 + 0.12)^3.

3. Evaluate the compound power before rounding: A꜀ = R5,837.48.

4. Compare R5,837.48 with R5,650.80; compound growth is larger for this positive rate and multiple years.

5. Answer: Compound amount = R5,837.48 compound amount. The difference is R186.68.

Answer: Compound amount = R5,837.48. Check: Answer: Compound amount = R5,837.48 compound amount. The difference is R186.68.

## g11-fin-l06-w08: A bank advertises 5.00% nominal interest compounded quarterly. A learner calls 5.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "rate_diagnosis", "principal": "4320", "rate": "0.05", "periods": 4, "years": 1}}`

1. The quoted 5.00% is nominal, with 4 compounding periods per year.

2. The learner ignored compounding: first divide the nominal rate by 4 to get 0.012500 per quarter.

3. Then compound four periods: (1 + 0.05/4)^4 − 1.

4. The effective annual rate is 5.09%; it differs from the advertised nominal rate.

5. Answer: Effective annual rate = 5.09% effective annually. The first error was equating nominal and effective rates.

Answer: Effective annual rate = 5.09%. Check: Answer: Effective annual rate = 5.09% effective annually. The first error was equating nominal and effective rates.

## g11-fin-l06-w09: A price of R4,485.00 rises 6.00% each year for 2 years, then falls 6.00% once. Find its final price; explain why the percentages cannot simply be subtracted.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "growth_then_decay", "principal": "4485", "rate": "0.06", "decline": "0.06", "years": 2}}`

1. The first growth applies 2 times to the changing balance: R4,485.00 × (1 + 0.06)^2.

2. The price after growth is approximately R5,039.35; retain the unrounded balance.

3. The final fall applies to the unrounded new price: 4,485.00 × (1 + 0.06)^2 × (1 − 0.06).

4. This gives R4,736.99. The two percentage changes use different bases.

5. Answer: Final price = R4,736.99. Check by multiplying the two factors, not subtracting their percentages.

Answer: Final price = R4,736.99. Check: Answer: Final price = R4,736.99. Check by multiplying the two factors, not subtracting their percentages.

## g11-fin-l06-w10: R4,650.00 earns 7.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "compare_methods", "principal": "4650", "rate": "0.07", "years": 3}}`

1. Simple interest gives Aₛ = 4,650.00 × (1 + 0.07 × 3) = R5,626.50.

2. Compound interest gives A꜀ = 4,650.00 × (1 + 0.07)^3.

3. Evaluate the compound power before rounding: A꜀ = R5,696.45.

4. Compare R5,696.45 with R5,626.50; compound growth is larger for this positive rate and multiple years.

5. Answer: Compound amount = R5,696.45 compound amount. The difference is R69.95.

Answer: Compound amount = R5,696.45. Check: Answer: Compound amount = R5,696.45 compound amount. The difference is R69.95.

## g11-fin-l06-w11: A bank advertises 8.00% nominal interest compounded quarterly. A learner calls 8.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "rate_diagnosis", "principal": "4815", "rate": "0.08", "periods": 4, "years": 1}}`

1. The quoted 8.00% is nominal, with 4 compounding periods per year.

2. The learner ignored compounding: first divide the nominal rate by 4 to get 0.020000 per quarter.

3. Then compound four periods: (1 + 0.08/4)^4 − 1.

4. The effective annual rate is 8.24%; it differs from the advertised nominal rate.

5. Answer: Effective annual rate = 8.24% effective annually. The first error was equating nominal and effective rates.

Answer: Effective annual rate = 8.24%. Check: Answer: Effective annual rate = 8.24% effective annually. The first error was equating nominal and effective rates.

## g11-fin-l06-w12: A price of R4,980.00 rises 9.00% each year for 2 years, then falls 3.00% once. Find its final price; explain why the percentages cannot simply be subtracted.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "growth_then_decay", "principal": "4980", "rate": "0.09", "decline": "0.03", "years": 2}}`

1. The first growth applies 2 times to the changing balance: R4,980.00 × (1 + 0.09)^2.

2. The price after growth is approximately R5,916.74; retain the unrounded balance.

3. The final fall applies to the unrounded new price: 4,980.00 × (1 + 0.09)^2 × (1 − 0.03).

4. This gives R5,739.24. The two percentage changes use different bases.

5. Answer: Final price = R5,739.24. Check by multiplying the two factors, not subtracting their percentages.

Answer: Final price = R5,739.24. Check: Answer: Final price = R5,739.24. Check by multiplying the two factors, not subtracting their percentages.

## g11-fin-l06-w13: R5,145.00 earns 10.0% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "compare_methods", "principal": "5145", "rate": "0.1", "years": 3}}`

1. Simple interest gives Aₛ = 5,145.00 × (1 + 0.1 × 3) = R6,688.50.

2. Compound interest gives A꜀ = 5,145.00 × (1 + 0.1)^3.

3. Evaluate the compound power before rounding: A꜀ = R6,848.00.

4. Compare R6,848.00 with R6,688.50; compound growth is larger for this positive rate and multiple years.

5. Answer: Compound amount = R6,848.00 compound amount. The difference is R159.50.

Answer: Compound amount = R6,848.00. Check: Answer: Compound amount = R6,848.00 compound amount. The difference is R159.50.

## g11-fin-l06-w14: A bank advertises 11.00% nominal interest compounded quarterly. A learner calls 11.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "rate_diagnosis", "principal": "5310", "rate": "0.11", "periods": 4, "years": 1}}`

1. The quoted 11.00% is nominal, with 4 compounding periods per year.

2. The learner ignored compounding: first divide the nominal rate by 4 to get 0.027500 per quarter.

3. Then compound four periods: (1 + 0.11/4)^4 − 1.

4. The effective annual rate is 11.46%; it differs from the advertised nominal rate.

5. Answer: Effective annual rate = 11.46% effective annually. The first error was equating nominal and effective rates.

Answer: Effective annual rate = 11.46%. Check: Answer: Effective annual rate = 11.46% effective annually. The first error was equating nominal and effective rates.

## g11-fin-l06-w15: A price of R5,475.00 rises 12.00% each year for 2 years, then falls 6.00% once. Find its final price; explain why the percentages cannot simply be subtracted.

Question-specific visual values: `{"family": "grade11_finance", "values": {"mode": "growth_then_decay", "principal": "5475", "rate": "0.12", "decline": "0.06", "years": 2}}`

1. The first growth applies 2 times to the changing balance: R5,475.00 × (1 + 0.12)^2.

2. The price after growth is approximately R6,867.84; retain the unrounded balance.

3. The final fall applies to the unrounded new price: 5,475.00 × (1 + 0.12)^2 × (1 − 0.06).

4. This gives R6,455.77. The two percentage changes use different bases.

5. Answer: Final price = R6,455.77. Check by multiplying the two factors, not subtracting their percentages.

Answer: Final price = R6,455.77. Check: Answer: Final price = R6,455.77. Check by multiplying the two factors, not subtracting their percentages.

## Practice key

- g11-fin-l06-p01: R5,640.00 earns 5.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger. Options: Compound amount = R6,333.13 | Compound amount = R6,920.75 | Compound amount = R6,529.01 | Compound amount = R6,724.88. Correct: Compound amount = R6,529.01. Simple interest gives Aₛ = 5,640.00 × (1 + 0.05 × 3) = R6,486.00. Compound interest gives A꜀ = 5,640.00 × (1 + 0.05)^3. Evaluate the compound power before rounding: A꜀ = R6,529.01. Compare R6,529.01 with R6,486.00; compound growth is larger for this positive rate and multiple years. Answer: Compound amount = R6,529.01 compound amount. The difference is R43.01.

- g11-fin-l06-p02: A bank advertises 6.00% nominal interest compounded quarterly. A learner calls 6.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places. Options: Effective annual rate = 6.64% | Effective annual rate = 6.14% | Effective annual rate = 6.39% | Effective annual rate = 5.89%. Correct: Effective annual rate = 6.14%. The quoted 6.00% is nominal, with 4 compounding periods per year. The learner ignored compounding: first divide the nominal rate by 4 to get 0.015000 per quarter. Then compound four periods: (1 + 0.06/4)^4 − 1. The effective annual rate is 6.14%; it differs from the advertised nominal rate. Answer: Effective annual rate = 6.14% effective annually. The first error was equating nominal and effective rates.

- g11-fin-l06-p03: A price of R5,970.00 rises 7.00% each year for 2 years, then falls 3.00% once. Find its final price; explain why the percentages cannot simply be subtracted. Options: Final price = R6,630.00 | Final price = R6,828.90 | Final price = R6,431.10 | Final price = R7,027.80. Correct: Final price = R6,630.00. The first growth applies 2 times to the changing balance: R5,970.00 × (1 + 0.07)^2. The price after growth is approximately R6,835.05; retain the unrounded balance. The final fall applies to the unrounded new price: 5,970.00 × (1 + 0.07)^2 × (1 − 0.03). This gives R6,630.00. The two percentage changes use different bases. Answer: Final price = R6,630.00. Check by multiplying the two factors, not subtracting their percentages.

- g11-fin-l06-p04: R6,135.00 earns 8.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger. Options: Compound amount = R7,960.18 | Compound amount = R7,496.48 | Compound amount = R8,192.03 | Compound amount = R7,728.33. Correct: Compound amount = R7,728.33. Simple interest gives Aₛ = 6,135.00 × (1 + 0.08 × 3) = R7,607.40. Compound interest gives A꜀ = 6,135.00 × (1 + 0.08)^3. Evaluate the compound power before rounding: A꜀ = R7,728.33. Compare R7,728.33 with R7,607.40; compound growth is larger for this positive rate and multiple years. Answer: Compound amount = R7,728.33 compound amount. The difference is R120.93.

- g11-fin-l06-p05: A bank advertises 9.00% nominal interest compounded quarterly. A learner calls 9.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places. Options: Effective annual rate = 9.06% | Effective annual rate = 9.81% | Effective annual rate = 9.31% | Effective annual rate = 9.56%. Correct: Effective annual rate = 9.31%. The quoted 9.00% is nominal, with 4 compounding periods per year. The learner ignored compounding: first divide the nominal rate by 4 to get 0.022500 per quarter. Then compound four periods: (1 + 0.09/4)^4 − 1. The effective annual rate is 9.31%; it differs from the advertised nominal rate. Answer: Effective annual rate = 9.31% effective annually. The first error was equating nominal and effective rates.

- g11-fin-l06-p06: A price of R6,465.00 rises 10.0% each year for 2 years, then falls 6.00% once. Find its final price; explain why the percentages cannot simply be subtracted. Options: Final price = R7,794.49 | Final price = R7,353.29 | Final price = R7,573.89 | Final price = R7,132.69. Correct: Final price = R7,353.29. The first growth applies 2 times to the changing balance: R6,465.00 × (1 + 0.1)^2. The price after growth is approximately R7,822.65; retain the unrounded balance. The final fall applies to the unrounded new price: 6,465.00 × (1 + 0.1)^2 × (1 − 0.06). This gives R7,353.29. The two percentage changes use different bases. Answer: Final price = R7,353.29. Check by multiplying the two factors, not subtracting their percentages.

- g11-fin-l06-p07: R6,630.00 earns 11.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger. Options: Compound amount = R9,067.39 | Compound amount = R9,339.42 | Compound amount = R8,795.37 | Compound amount = R9,611.44. Correct: Compound amount = R9,067.39. Simple interest gives Aₛ = 6,630.00 × (1 + 0.11 × 3) = R8,817.90. Compound interest gives A꜀ = 6,630.00 × (1 + 0.11)^3. Evaluate the compound power before rounding: A꜀ = R9,067.39. Compare R9,067.39 with R8,817.90; compound growth is larger for this positive rate and multiple years. Answer: Compound amount = R9,067.39 compound amount. The difference is R249.49.

- g11-fin-l06-p08: A bank advertises 12.00% nominal interest compounded quarterly. A learner calls 12.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places. Options: Effective annual rate = 12.80% | Effective annual rate = 12.30% | Effective annual rate = 13.05% | Effective annual rate = 12.55%. Correct: Effective annual rate = 12.55%. The quoted 12.00% is nominal, with 4 compounding periods per year. The learner ignored compounding: first divide the nominal rate by 4 to get 0.030000 per quarter. Then compound four periods: (1 + 0.12/4)^4 − 1. The effective annual rate is 12.55%; it differs from the advertised nominal rate. Answer: Effective annual rate = 12.55% effective annually. The first error was equating nominal and effective rates.

- g11-fin-l06-p09: A price of R6,960.00 rises 5.00% each year for 2 years, then falls 3.00% once. Find its final price; explain why the percentages cannot simply be subtracted. Options: Final price = R7,219.90 | Final price = R7,889.79 | Final price = R7,443.20 | Final price = R7,666.49. Correct: Final price = R7,443.20. The first growth applies 2 times to the changing balance: R6,960.00 × (1 + 0.05)^2. The price after growth is approximately R7,673.40; retain the unrounded balance. The final fall applies to the unrounded new price: 6,960.00 × (1 + 0.05)^2 × (1 − 0.03). This gives R7,443.20. The two percentage changes use different bases. Answer: Final price = R7,443.20. Check by multiplying the two factors, not subtracting their percentages.

- g11-fin-l06-p10: R7,125.00 earns 6.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger. Options: Compound amount = R8,995.15 | Compound amount = R8,485.99 | Compound amount = R8,740.57 | Compound amount = R8,231.41. Correct: Compound amount = R8,485.99. Simple interest gives Aₛ = 7,125.00 × (1 + 0.06 × 3) = R8,407.50. Compound interest gives A꜀ = 7,125.00 × (1 + 0.06)^3. Evaluate the compound power before rounding: A꜀ = R8,485.99. Compare R8,485.99 with R8,407.50; compound growth is larger for this positive rate and multiple years. Answer: Compound amount = R8,485.99 compound amount. The difference is R78.49.

- g11-fin-l06-p11: A bank advertises 7.00% nominal interest compounded quarterly. A learner calls 7.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places. Options: Effective annual rate = 7.19% | Effective annual rate = 7.44% | Effective annual rate = 6.94% | Effective annual rate = 7.69%. Correct: Effective annual rate = 7.19%. The quoted 7.00% is nominal, with 4 compounding periods per year. The learner ignored compounding: first divide the nominal rate by 4 to get 0.017500 per quarter. Then compound four periods: (1 + 0.07/4)^4 − 1. The effective annual rate is 7.19%; it differs from the advertised nominal rate. Answer: Effective annual rate = 7.19% effective annually. The first error was equating nominal and effective rates.

- g11-fin-l06-p12: A price of R7,455.00 rises 8.00% each year for 2 years, then falls 6.00% once. Find its final price; explain why the percentages cannot simply be subtracted. Options: Final price = R8,418.99 | Final price = R7,928.57 | Final price = R8,664.21 | Final price = R8,173.78. Correct: Final price = R8,173.78. The first growth applies 2 times to the changing balance: R7,455.00 × (1 + 0.08)^2. The price after growth is approximately R8,695.51; retain the unrounded balance. The final fall applies to the unrounded new price: 7,455.00 × (1 + 0.08)^2 × (1 − 0.06). This gives R8,173.78. The two percentage changes use different bases. Answer: Final price = R8,173.78. Check by multiplying the two factors, not subtracting their percentages.

- g11-fin-l06-p13: R7,620.00 earns 9.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger. Options: Compound amount = R9,572.08 | Compound amount = R10,460.21 | Compound amount = R9,868.12 | Compound amount = R10,164.16. Correct: Compound amount = R9,868.12. Simple interest gives Aₛ = 7,620.00 × (1 + 0.09 × 3) = R9,677.40. Compound interest gives A꜀ = 7,620.00 × (1 + 0.09)^3. Evaluate the compound power before rounding: A꜀ = R9,868.12. Compare R9,868.12 with R9,677.40; compound growth is larger for this positive rate and multiple years. Answer: Compound amount = R9,868.12 compound amount. The difference is R190.72.

- g11-fin-l06-p14: A bank advertises 10.0% nominal interest compounded quarterly. A learner calls 10.0% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places. Options: Effective annual rate = 10.88% | Effective annual rate = 10.38% | Effective annual rate = 10.63% | Effective annual rate = 10.13%. Correct: Effective annual rate = 10.38%. The quoted 10.0% is nominal, with 4 compounding periods per year. The learner ignored compounding: first divide the nominal rate by 4 to get 0.025000 per quarter. Then compound four periods: (1 + 0.1/4)^4 − 1. The effective annual rate is 10.38%; it differs from the advertised nominal rate. Answer: Effective annual rate = 10.38% effective annually. The first error was equating nominal and effective rates.

- g11-fin-l06-p15: A price of R7,950.00 rises 11.00% each year for 2 years, then falls 3.00% once. Find its final price; explain why the percentages cannot simply be subtracted. Options: Final price = R9,501.34 | Final price = R9,786.38 | Final price = R9,216.30 | Final price = R10,071.42. Correct: Final price = R9,501.34. The first growth applies 2 times to the changing balance: R7,950.00 × (1 + 0.11)^2. The price after growth is approximately R9,795.20; retain the unrounded balance. The final fall applies to the unrounded new price: 7,950.00 × (1 + 0.11)^2 × (1 − 0.03). This gives R9,501.34. The two percentage changes use different bases. Answer: Final price = R9,501.34. Check by multiplying the two factors, not subtracting their percentages.

## Mastery key

- g11-fin-l06-m01: R8,115.00 earns 12.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger. Options: Compound amount = R12,085.05 | Compound amount = R11,400.99 | Compound amount = R11,743.02 | Compound amount = R11,058.96. Correct: Compound amount = R11,400.99. Simple interest gives Aₛ = 8,115.00 × (1 + 0.12 × 3) = R11,036.40. Compound interest gives A꜀ = 8,115.00 × (1 + 0.12)^3. Evaluate the compound power before rounding: A꜀ = R11,400.99. Compare R11,400.99 with R11,036.40; compound growth is larger for this positive rate and multiple years. Answer: Compound amount = R11,400.99 compound amount. The difference is R364.59.

- g11-fin-l06-m02: A bank advertises 5.00% nominal interest compounded quarterly. A learner calls 5.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places. Options: Effective annual rate = 5.09% | Effective annual rate = 5.34% | Effective annual rate = 4.84% | Effective annual rate = 5.59%. Correct: Effective annual rate = 5.09%. The quoted 5.00% is nominal, with 4 compounding periods per year. The learner ignored compounding: first divide the nominal rate by 4 to get 0.012500 per quarter. Then compound four periods: (1 + 0.05/4)^4 − 1. The effective annual rate is 5.09%; it differs from the advertised nominal rate. Answer: Effective annual rate = 5.09% effective annually. The first error was equating nominal and effective rates.

- g11-fin-l06-m03: A price of R8,445.00 rises 6.00% each year for 2 years, then falls 6.00% once. Find its final price; explain why the percentages cannot simply be subtracted. Options: Final price = R9,187.06 | Final price = R8,651.89 | Final price = R9,454.64 | Final price = R8,919.47. Correct: Final price = R8,919.47. The first growth applies 2 times to the changing balance: R8,445.00 × (1 + 0.06)^2. The price after growth is approximately R9,488.80; retain the unrounded balance. The final fall applies to the unrounded new price: 8,445.00 × (1 + 0.06)^2 × (1 − 0.06). This gives R8,919.47. The two percentage changes use different bases. Answer: Final price = R8,919.47. Check by multiplying the two factors, not subtracting their percentages.

- g11-fin-l06-m04: R8,610.00 earns 7.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger. Options: Compound amount = R10,231.19 | Compound amount = R11,180.48 | Compound amount = R10,547.62 | Compound amount = R10,864.05. Correct: Compound amount = R10,547.62. Simple interest gives Aₛ = 8,610.00 × (1 + 0.07 × 3) = R10,418.10. Compound interest gives A꜀ = 8,610.00 × (1 + 0.07)^3. Evaluate the compound power before rounding: A꜀ = R10,547.62. Compare R10,547.62 with R10,418.10; compound growth is larger for this positive rate and multiple years. Answer: Compound amount = R10,547.62 compound amount. The difference is R129.52.

- g11-fin-l06-m05: A bank advertises 8.00% nominal interest compounded quarterly. A learner calls 8.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places. Options: Effective annual rate = 8.74% | Effective annual rate = 8.24% | Effective annual rate = 8.49% | Effective annual rate = 7.99%. Correct: Effective annual rate = 8.24%. The quoted 8.00% is nominal, with 4 compounding periods per year. The learner ignored compounding: first divide the nominal rate by 4 to get 0.020000 per quarter. Then compound four periods: (1 + 0.08/4)^4 − 1. The effective annual rate is 8.24%; it differs from the advertised nominal rate. Answer: Effective annual rate = 8.24% effective annually. The first error was equating nominal and effective rates.

## Reassessment key

- g11-fin-l06-r01: R10,590.00 earns 11.00% annually for 3 years. Compare simple interest with annual compound interest; find the compound amount and identify which is larger. Options: Compound amount = R14,483.21 | Compound amount = R14,917.71 | Compound amount = R14,048.72 | Compound amount = R15,352.21. Correct: Compound amount = R14,483.21. Simple interest gives Aₛ = 10,590.00 × (1 + 0.11 × 3) = R14,084.70. Compound interest gives A꜀ = 10,590.00 × (1 + 0.11)^3. Evaluate the compound power before rounding: A꜀ = R14,483.21. Compare R14,483.21 with R14,084.70; compound growth is larger for this positive rate and multiple years. Answer: Compound amount = R14,483.21 compound amount. The difference is R398.51.

- g11-fin-l06-r02: A bank advertises 12.00% nominal interest compounded quarterly. A learner calls 12.00% the effective annual rate. Locate the first error and give the effective annual rate to two decimal places. Options: Effective annual rate = 12.80% | Effective annual rate = 12.30% | Effective annual rate = 13.05% | Effective annual rate = 12.55%. Correct: Effective annual rate = 12.55%. The quoted 12.00% is nominal, with 4 compounding periods per year. The learner ignored compounding: first divide the nominal rate by 4 to get 0.030000 per quarter. Then compound four periods: (1 + 0.12/4)^4 − 1. The effective annual rate is 12.55%; it differs from the advertised nominal rate. Answer: Effective annual rate = 12.55% effective annually. The first error was equating nominal and effective rates.

- g11-fin-l06-r03: A price of R10,920.00 rises 5.00% each year for 2 years, then falls 3.00% once. Find its final price; explain why the percentages cannot simply be subtracted. Options: Final price = R11,327.78 | Final price = R12,378.81 | Final price = R11,678.12 | Final price = R12,028.46. Correct: Final price = R11,678.12. The first growth applies 2 times to the changing balance: R10,920.00 × (1 + 0.05)^2. The price after growth is approximately R12,039.30; retain the unrounded balance. The final fall applies to the unrounded new price: 10,920.00 × (1 + 0.05)^2 × (1 − 0.03). This gives R11,678.12. The two percentage changes use different bases. Answer: Final price = R11,678.12. Check by multiplying the two factors, not subtracting their percentages.
