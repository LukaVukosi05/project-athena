"""Short topic check across the six authored Functions and Relationships lessons.

Fresh values and compact responses make automatic scoring fairer than using
the multi-part lesson mastery memos as literal answer strings.
"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Item:
    id: str
    lesson_id: str
    prompt: str
    answers: tuple[str, ...]
    explanation: str


ITEMS = (
    Item("fr-t01", "g8-functions-relationships-01", "A machine multiplies an input by 4 then adds 3. What is the output for input 2?", ("11",), "4 × 2 + 3 = 11."),
    Item("fr-t02", "g8-functions-relationships-01", "A machine triples an input and adds 2. Its output is 17. What was the input?", ("5",), "Undo the addition, then divide: (17 − 2) ÷ 3 = 5."),
    Item("fr-t03", "g8-functions-relationships-01", "A delivery charge is R9 once plus R4 per km. What is the cost for 3 km, in rand?", ("21", "r21", "r21.00"), "The fixed R9 is charged once: 9 + 4 × 3 = R21."),
    Item("fr-t04", "g8-functions-relationships-02", "'Double x, then add 3.' What is the output for x = 2?", ("7",), "Doubling first gives 4; adding 3 gives 7."),
    Item("fr-t05", "g8-functions-relationships-02", "'Add 3, then double.' What is the output for x = 2?", ("10",), "Add first: 2 + 3 = 5; doubling gives 10. Order matters."),
    Item("fr-t06", "g8-functions-relationships-02", "Are 4(x + 2) and 4x + 8 equivalent for every x? Answer yes or no.", ("yes", "y"), "Yes. Distribution gives 4(x + 2) = 4x + 8 for every x."),
    Item("fr-t07", "g8-functions-relationships-03", "A table pairs x = 0, 1, 2 with y = 3, 6, 9. What output fits x = 3 using the simplest linear rule?", ("12",), "Each step of one in x adds three in y; the next output is 12."),
    Item("fr-t08", "g8-functions-relationships-03", "A table pairs x = 0, 2, 4 with y = 5, 11, 17. What output fits x = 3 using a linear rule?", ("14",), "Two input units add six output units, so one input adds three; 5 + 3 × 3 = 14."),
    Item("fr-t09", "g8-functions-relationships-03", "The table 0→1, 1→2, 2→5 follows y = x² + 1. What is the output for x = 3?", ("10",), "3² + 1 = 10; check the formula against every given row."),
    Item("fr-t10", "g8-functions-relationships-04", "A rectangle has area 42 cm² and width 6 cm. What is its length in centimetres?", ("7",), "Area divided by width gives length: 42 ÷ 6 = 7 cm."),
    Item("fr-t11", "g8-functions-relationships-04", "A rectangle is 8 cm long and 3 cm wide. What is its perimeter in centimetres?", ("22",), "Add two lengths and two widths: 2(8 + 3) = 22 cm."),
    Item("fr-t12", "g8-functions-relationships-04", "A rectangle has area 30 m². Tiles cost R40 per m². What is the total cost in rand?", ("1200", "r1200"), "Multiply the square-metre area by the price per square metre: 30 × 40 = R1200."),
    Item("fr-t13", "g8-functions-relationships-05", "Double x then add 4: what is the output at x = 3?", ("10",), "2×3 + 4 = 10; operation order matters."),
    Item("fr-t14", "g8-functions-relationships-05", "A R7 fixed fee plus R2 per item gives what cost for five items, in rand?", ("17", "r17"), "7 + 2×5 = R17."),
    Item("fr-t15", "g8-functions-relationships-05", "Are 3(x + 2) and 3x + 6 equivalent for all inputs? Answer yes or no.", ("yes", "y"), "Distribute three to both terms."),
    Item("fr-t16", "g8-functions-relationships-06", "A learner expands 2(x + 4) as 2x + 4. What is the correct constant term?", ("8",), "Two multiplies both x and four."),
    Item("fr-t17", "g8-functions-relationships-06", "From 0→5 and 2→11 a learner calls the rate six per input. What is the correct rate?", ("3",), "The output changes by six over two input units."),
    Item("fr-t18", "g8-functions-relationships-06", "A learner claims a square of side 4 has area 4×4 boundary edges. What is its area in unit squares?", ("16",), "Four rows of four unit squares give area 16."),
)

LABELS = {
    "g8-functions-relationships-01": "Input and output rules",
    "g8-functions-relationships-02": "Equivalent forms and operation order",
    "g8-functions-relationships-03": "Finding rules from tables",
    "g8-functions-relationships-04": "Formula contexts and missing dimensions",
    "g8-functions-relationships-05": "Matching relationship representations",
    "g8-functions-relationships-06": "First-error relationship repair",
}


def public_items():
    return [{"id": item.id, "prompt": item.prompt} for item in ITEMS]


def score(answers: dict[str, str]):
    if set(answers) != {item.id for item in ITEMS}:
        raise ValueError("Submit one answer for each of the eighteen questions")
    groups = {lesson_id: {"lesson_id": lesson_id, "title": title, "correct": 0, "total": 3}
              for lesson_id, title in LABELS.items()}
    review = []
    for item in ITEMS:
        answer = answers[item.id]
        if not isinstance(answer, str) or not 0 < len(answer.strip()) <= 100:
            raise ValueError(f"Answer {item.id} must contain 1 to 100 characters")
        normal = re.sub(r"\s+", "", answer.casefold().replace("−", "-"))
        correct = normal in item.answers
        groups[item.lesson_id]["correct"] += int(correct)
        review.append({"id": item.id, "correct": correct, "answer": item.answers[0],
                       "explanation": item.explanation, "lesson_id": item.lesson_id})
    areas = list(groups.values())
    for area in areas:
        area["needs_review"] = area["correct"] < 3
    total = sum(area["correct"] for area in areas)
    return {"score": total, "total": len(ITEMS), "areas": areas,
            "recommended_lesson_id": next((area["lesson_id"] for area in areas if area["needs_review"]), None),
            "review": review, "note": "This short check directs revision; it does not replace lesson mastery or teacher review."}
