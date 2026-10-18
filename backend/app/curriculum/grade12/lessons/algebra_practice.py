"""Approved Topic 5 self-guided practice (12 source-authored items per lesson)."""
from __future__ import annotations
import json
from pathlib import Path

from app.practice.schemas import ALGEBRA_SOURCE, AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

DATA=json.loads(Path(__file__).with_name("algebra_pack_data.json").read_text(encoding="utf-8"))["lessons"]
LEVELS={"Foundation":"foundation","Routine":"standard","Complex":"intermediate","Exam-level":"exam"}

def concise_answer(memo: str) -> str:
    parts=[part.strip().rstrip(".") for part in memo.split(";") if part.strip()]
    return parts[-1] if parts else memo

def make(item,spec,number):
    answer=spec["answer"]; concise=concise_answer(answer)
    return PracticeQuestion(
      id=spec["id"],lesson_id=item["id"],question_number=number,difficulty=LEVELS[spec["level"]],
      cognitive_level="knowledge" if number<=2 else "routine" if number<=6 else "complex" if number<=10 else "problem_solving",
      marks=2 if number<=2 else 3 if number<=10 else 4,type="short_text",prompt=spec["prompt"],
      accepted_answers=list(dict.fromkeys([answer,concise])),answer_normalisation=AnswerNormalisation(),
      hints=["Name the target and identify the algebraic structure without calculating.",f"Use this structure anchor: {item['anchor']}","Show the first valid transformation, retain every condition, then verify in the original task."],
      worked_solution=[
       WorkedSolutionStep(expression=spec["prompt"],explanation="Orient on the complete task and its conditions.",why="The target and original domain determine what counts as a valid answer.",focus=["problem","target"],verification="No condition has been omitted."),
       WorkedSolutionStep(expression=item["anchor"],explanation="Select the method from the visible structure.",why=item["teaching"],focus=["structure","method"],verification="The method matches the requested object."),
       WorkedSolutionStep(expression=answer,explanation="Carry out the source-authored marks-bearing route one legal change at a time.",why="Each equality transformation is applied to complete sides; inequality, surd and rational steps retain their conditions.",focus=["operation","candidate"],verification="Signs, brackets, factors and restrictions remain visible."),
       WorkedSolutionStep(expression=concise,explanation="State every candidate, interval, ordered pair or parameter condition.",why="A partial branch or missing endpoint changes the solution set.",focus=["result"],verification="Compare with every branch of the solution."),
       WorkedSolutionStep(expression="Verify in the original task",explanation="Substitute roots or ordered pairs, test inequality regions, expand factors, or check restrictions and the discriminant.",why="An algebraically generated candidate is not automatically valid in the original task.",focus=["verification"],verification="The final result satisfies the original conditions and excludes invalid values."),
      ],misconception_tags=[item["misconception"]],verification={"original_task":"required","critical_misconception":item["misconception"]},correct_feedback="Correct. The selected method, validity conditions and original-task verification agree.",source=ALGEBRA_SOURCE)

PRACTICE_BANKS={item["id"]:[make(item,spec,n) for n,spec in enumerate(item["practice"],1)] for item in DATA}
PRACTICE_BY_ID={q.id:q for bank in PRACTICE_BANKS.values() for q in bank}
