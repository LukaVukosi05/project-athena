"""Private Grade 11 Probability MCQ banks."""
from app.curriculum.grade11.probability import LESSONS
from app.curriculum.grade9.assessment_whole_numbers import AssessmentQuestion
from app.practice.schemas import PracticeQuestion, WorkedSolutionStep

def banks(number):
    lesson, data = LESSONS[number]
    tag = "grade11-probability"
    practice = []
    for index, item in enumerate(data["practice"], 1):
        answer = item["options"][item["answer_index"]]
        practice.append(PracticeQuestion(
            id=item["id"], lesson_id=lesson.id, question_number=index,
            difficulty=lesson.whiteboard_questions[index - 1].difficulty,
            cognitive_level=lesson.whiteboard_questions[index - 1].cognitive_level,
            marks=2 if index <= 5 else 4, type="multiple_choice",
            prompt=item["prompt"], options=item["options"], accepted_answers=[answer],
            hints=["Copy the sample space and identify favourable outcomes before choosing a rule.",
                   "Calculate in your book; check overlap, replacement and the correct denominator."],
            worked_solution=[WorkedSolutionStep(expression=line, explanation=line,
                 why="Show the disjoint regions or tree branches using the given counts.")
                 for line in item["actions"]],
            misconception_tags=[tag],
            verification={"original_question_check":item["memo"][-650:]},
            correct_feedback="Correct. Compare your written method with the worked review.",
            source=data["source"], answer_hidden_before_submission=True))
    def assessment(item, index, mastery):
        answer = item["options"][item["answer_index"]]
        return AssessmentQuestion(id=item["id"], number=index, prompt=item["prompt"],
            options=item["options"], marks=4 if mastery else None, answer=answer,
            solution=[item["memo"]], verification=item["memo"][-650:],
            misconception_tags=[tag], accepted_answers=[answer])
    mastery = [assessment(item, i, True) for i, item in enumerate(data["mastery"], 1)]
    reassessment = [assessment(item, i, False) for i, item in enumerate(data["reassessment"], 1)]
    repairs = {tag:{"diagnosis":"Find the first double-counted overlap, incorrect denominator or unchanged branch after a draw.",
                    "repair":"Correct the first event-counting error and retry with a different sample space."}}
    rules = {tag:"Check each numerator and denominator against the original event conditions."}
    return practice, mastery, reassessment, repairs, rules

BANKS = {number:banks(number) for number in range(1, 8)}
