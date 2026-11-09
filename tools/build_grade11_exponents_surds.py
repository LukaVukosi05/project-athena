"""Build original, deterministic Grade 11 Exponents and Surds source banks."""
from __future__ import annotations

import json
from hashlib import sha256
from math import gcd
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/curriculum/grade11/exponents-surds"
OUT = ROOT / "backend/app/curriculum/grade11/generated"
ATP = "https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2023%20ATPs/FET%20Content%20Subjects/Grade%2011/1.590%20ATP%202023-24%20Gr%2011%20Maths%20final.pdf"
TITLES = {
    1: "Rational exponents and positive roots",
    2: "Exponent laws with rational powers",
    3: "Simplifying surds by square factors",
    4: "Combining like surds after simplification",
    5: "Dividing and rationalising surds",
    6: "Surd equations and extraneous roots",
}
DIFFICULTIES = ["foundation"] * 2 + ["easy"] * 3 + ["standard"] * 4 + ["intermediate"] * 3 + ["exam"] * 3


def case(n: int, i: int, variant: int = 0) -> dict:
    s = i + variant * 19
    d = (2, 3, 5, 6, 7, 10, 11)[s % 7]
    k = 2 + s % 8
    if n == 1:
        q = 2 + s % 2
        p = 1 + (s // 2) % 3
        base = k ** q
        value = k ** p
        ordinal = {2:"second",3:"third"}[q]
        problem = f"Evaluate {base}^({p}/{q}) using the positive {ordinal} root."
        answer = str(value)
        steps = [f"Identify the base {base} and rational exponent {p}/{q}.",
                 f"The denominator {q} means take the positive {ordinal} root of {base}.",
                 f"Because {k}^{q} = {base}, that root is {k}.",
                 f"Raise {k} to the numerator {p}: {k}^{p} = {value}.",
                 f"Answer: {value}. Check: {value}^{q} = {base}^{p}."]
        wrong = [str(k * p + 1), str(base ** p), str(value + q)]
        visual = {"family": "root_power", "base": base, "index": q, "power": p, "root": k}
    elif n == 2:
        denominator = 2 + s % 3
        a = 2 + s % 5
        b = 1 + (s // 2) % 4
        c = 1 + (s // 3) % 2
        result_num = a + b - c
        problem = f"Simplify x^({a}/{denominator}) × x^({b}/{denominator}) ÷ x^({c}/{denominator}), for x > 0."
        exponent = Fraction(result_num, denominator)
        answer = f"x^{exponent.numerator}" if exponent.denominator == 1 else f"x^({exponent.numerator}/{exponent.denominator})"
        steps = [f"Keep the common positive base x and denominators {denominator}.",
                 f"Multiplication adds numerator exponents: {a} + {b} = {a+b}.",
                 f"Division subtracts numerator exponent {c}: {a+b} − {c} = {result_num}.",
                 f"Reduce {result_num}/{denominator} where possible: write {answer}; retain x > 0.",
                 f"Answer: {answer}, x > 0. Substitute x = {denominator**denominator} into both forms to check."]
        wrong = [f"x^({a+b+c}/{denominator})", f"x^({a*b-c}/{denominator})", f"x^({result_num+denominator}/{denominator})"]
        visual = {"family": "exponent_laws", "a": a, "b": b, "c": c, "denominator": denominator}
    elif n == 3:
        radicand = k * k * d
        problem = f"Simplify √{radicand} exactly."
        answer = f"{k}√{d}"
        steps = [f"Find a square factor of {radicand}: {k*k} × {d}.",
                 f"Split the radical: √{radicand} = √{k*k} × √{d}.",
                 f"The principal square root of {k*k} is {k}, not a negative number.",
                 f"Keep the nonsquare factor {d} inside the radical.",
                 f"Answer: {answer}. Check by squaring: ({k}√{d})² = {radicand}."]
        wrong = [f"{k*d}√{d}", f"{k}√{k*d}", str(radicand)]
        visual = {"family": "surd_pairs", "radicand": radicand, "square": k*k, "remainder": d, "outside": k}
    elif n == 4:
        a = 2 + s % 6
        b = 1 + (s // 2) % 4
        m = 2 + (s // 3) % 4
        # Alternate addition and subtraction, preserving a nonzero result.
        minus = s % 3 == 0
        coefficient = a*m - b if minus else a*m + b
        operator = "−" if minus else "+"
        problem = f"Simplify {a}√{m*m*d} {operator} {b}√{d}."
        answer = f"{coefficient}√{d}"
        steps = [f"Find the square factor {m*m} in {m*m*d}.",
                 f"Rewrite √{m*m*d} = {m}√{d}.",
                 f"Multiply the first coefficient: {a} × {m} = {a*m}.",
                 f"Combine like surds: {a*m}√{d} {operator} {b}√{d} = {coefficient}√{d}.",
                 f"Answer: {answer}. Both terms share √{d}; estimate to check the sign."]
        wrong = [f"{a*m+b if minus else a*m-b}√{d}", f"{coefficient}√{2*d}", f"{a+b}√{d}"]
        visual = {"family": "like_surds", "a": a, "b": b, "factor": m, "radicand": d, "subtract": minus}
    elif n == 5:
        numerator = 2 + s % 8
        problem = f"Rationalise the denominator of {numerator}/√{d} and simplify."
        divisor = gcd(numerator, d)
        answer = f"{numerator//divisor}√{d}/{d//divisor}" if d//divisor != 1 else f"{numerator//divisor}√{d}"
        steps = [f"Start with {numerator}/√{d}; √{d} is nonzero.",
                 f"Multiply numerator and denominator by √{d}/√{d}, which equals one.",
                 f"The numerator becomes {numerator}√{d}.",
                 f"The denominator becomes (√{d})² = {d}.",
                 f"Answer: {answer}. Divide numerator and denominator by {divisor}; both forms have the same value."]
        wrong = [f"{numerator}/{d}", f"{numerator}√{d}", f"√{numerator*d}/{d}"]
        visual = {"family": "rationalise", "numerator": numerator, "radicand": d}
    else:
        b = 1 + s % 5
        t = 4 + (s // 5) % 9
        a = t*t - b - t
        valid = b+t
        rejected = b+1-t
        problem = f"Solve √(x + {a}) = x − {b} in real numbers."
        answer = f"x = {valid}"
        steps = [f"The principal root is nonnegative, so x − {b} ≥ 0 and x ≥ {b}.",
                 f"Square both sides: x + {a} = (x − {b})².",
                 f"Solve the resulting quadratic to get candidates {valid} and {rejected}.",
                 f"Substitute into the ORIGINAL equation: x = {rejected} fails because its right side is negative.",
                 f"Answer: {answer}. At x = {valid}, √({valid}+{a}) = {t} and {valid} − {b} = {t}."]
        wrong = [f"x = {rejected}", f"x = {valid} or x = {rejected}", f"x = {valid+1}"]
        visual = {"family": "surd_equation", "offset": a, "rhs_offset": b, "valid": valid, "rejected": rejected}
    wrong = list(dict.fromkeys(option for option in wrong if option != answer))
    offset = 1
    while len(wrong) < 3:
        if n == 1:
            alternative = str(value + offset + q)
        elif n == 2:
            alternative = f"x^({result_num + denominator + offset}/{denominator})"
        elif n in (3, 4):
            alternative = f"{(k if n == 3 else coefficient) + offset}√{d}"
        elif n == 5:
            alternative = f"{numerator + offset}√{d}/{d}"
        else:
            alternative = f"x = {valid + offset}"
        if alternative not in wrong:
            wrong.append(alternative)
        offset += 1
    wrong = wrong[:3]
    assert len(steps) == 5 and len({answer, *wrong}) == 4, (n, i, answer, wrong)
    return {"id": f"g11-es-l{n:02}-w{i:02}", "lesson": n, "problem": problem,
            "answer": answer, "actions": steps, "check": steps[-1],
            "visual": {"family": "grade11_exponents_surds", "values": {**visual, "lesson": n}},
            "wrong": wrong, "misconception": "Apply a root, exponent or surd rule to every factor and check in the original.",
            "difficulty": DIFFICULTIES[min(i-1, 14)]}


def item(n: int, i: int, variant: int, prefix: str) -> dict:
    q = case(n, i, variant)
    # Keep the answer index explicit after rotation, including the last question.
    options = [q["answer"], *q["wrong"]]
    shift = i % 4
    options = options[-shift:] + options[:-shift] if shift else options
    return {"id": f"g11-es-l{n:02}-{prefix}{i:02}", "prompt": q["problem"],
            "options": options, "answer_index": options.index(q["answer"]),
            "memo": " ".join(q["actions"]), "actions": q["actions"]}


def build() -> None:
    DOC.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for n, title in TITLES.items():
        worked = [{k: v for k, v in case(n, i).items() if k != "wrong"} for i in range(1, 16)]
        data = {"source": f"grade11-es-lesson-{n:02}.md", "worked": worked,
                "practice": [item(n, i, 1, "p") for i in range(1, 16)],
                "mastery": [item(n, i+15, 2, "m") for i in range(1, 6)],
                "reassessment": [item(n, i+20, 3, "r") for i in range(1, 4)]}
        assert len({q["problem"] for q in worked}) == 15
        lines = [f"# Grade 11 Topic 1, Lesson {n}: {title}", f"Source: [DBE Grade 11 ATP]({ATP}), Term 1. Original Athena questions.",
                 "Status: teacher review and browser acceptance required. Work every question in a book before choosing."]
        for q in worked:
            lines += [f"## {q['id']}: {q['problem']}", f"Visual contract: `{json.dumps(q['visual'], ensure_ascii=False)}`",
                      *[f"{j}. {action}" for j, action in enumerate(q["actions"], 1)],
                      f"**Answer:** {q['answer']}. **Check:** {q['check']}"]
        for title2, key in (("Practice", "practice"), ("Mastery", "mastery"), ("Parallel reassessment", "reassessment")):
            lines.append(f"## {title2} answer key")
            for q in data[key]:
                lines.append(f"- {q['id']}: {q['prompt']} Options: {' | '.join(q['options'])}. Correct: {q['options'][q['answer_index']]}. {q['memo']}")
        source = DOC / data["source"]
        source.write_text("\n\n".join(lines) + "\n", encoding="utf-8")
        (OUT / f"exponents_surds_{n:02}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        manifest.append({"lesson_id": f"g11-es-{n:02}", "source": source.name,
                         "source_sha256": sha256(source.read_bytes()).hexdigest(),
                         "worked": 15, "practice": 15, "mastery": 5, "reassessment": 3,
                         "status": "teacher_review_required", "teacher_approved": False, "browser_accepted": False})
    (DOC / "topic1-acceptance-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
