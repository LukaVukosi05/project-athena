"""Validated self-guided banks for the complete approved lesson schedule."""
from fractions import Fraction
from app.curriculum.grade12.lessons.sequences_practice import LESSON_ONE_PRACTICE
from app.curriculum.grade12.lessons.sequences_runtime import GENERATORS
from app.practice.schemas import PracticeQuestion, WorkedSolutionStep


def is_numeric(value:str)->bool:
    try: Fraction(value);return True
    except (ValueError,ZeroDivisionError): return False


def bank_for(number:int)->list[PracticeQuestion]:
    lesson_id=f"g12-sequences-series-{number:02}"
    result=[]
    for index,spec in enumerate(GENERATORS[number](),1):
        steps=[WorkedSolutionStep(expression=spec.prompt,explanation="Identify the given information and required result.",why="A correct model must be selected before calculation.",focus=["problem"]),WorkedSolutionStep(expression=spec.method,explanation="Select the sequence or series method.",why="This method matches the mathematical structure in the prompt.",focus=["method"])]
        steps.extend(WorkedSolutionStep(expression=line,explanation="Carry out the next mathematical transformation.",why="This follows from the selected formula and the stated values.",focus=["working"]) for line in spec.working)
        steps.append(WorkedSolutionStep(expression=f"Answer: {spec.answer}",explanation="State the requested result.",why="The result follows from the completed working.",focus=["answer"]))
        steps.append(WorkedSolutionStep(expression=spec.verification,explanation="Check the answer against the original information.",why="Verification detects formula, sign and indexing errors.",focus=["verification"]))
        result.append(PracticeQuestion(id=f"g12-seq-l{number:02}-p{index:02}",lesson_id=lesson_id,question_number=index,difficulty="foundation" if index<=2 else "easy" if index<=4 else "standard" if index<=7 else "intermediate" if index<=9 else "exam" if index<=11 else "advanced",cognitive_level="routine" if index<=6 else "complex" if index<=10 else "problem_solving",marks=2 if index<=6 else 4,type="numeric" if is_numeric(spec.answer) else "short_text",prompt=spec.prompt,accepted_answers=[spec.answer],hints=["First decide which sequence or series structure applies.",spec.method,f"Set up the calculation as: {spec.working[0]}"],worked_solution=steps,misconception_tags=[spec.misconception],verification={"check":spec.verification},correct_feedback=f"Correct. {spec.verification}"))
    return result


PRACTICE_BANKS={"g12-sequences-series-01":LESSON_ONE_PRACTICE}
PRACTICE_BANKS.update({f"g12-sequences-series-{number:02}":bank_for(number) for number in range(2,19)})
PRACTICE_BY_ID={question.id:question for bank in PRACTICE_BANKS.values() for question in bank}

assert all(len(bank)==12 for bank in PRACTICE_BANKS.values())
assert len(PRACTICE_BY_ID)==18*12
