"""Short topic check across the three authored Functions and Relationships lessons.

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
)

LABELS = {
    "g8-functions-relationships-01": "Input and output rules",
    "g8-functions-relationships-02": "Equivalent forms and operation order",
    "g8-functions-relationships-03": "Finding rules from tables",
}


def public_items():
    return [{"id": item.id, "prompt": item.prompt} for item in ITEMS]


def score(answers: dict[str, str]):
    if set(answers) != {item.id for item in ITEMS}:
        raise ValueError("Submit one answer for each of the nine questions")
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
