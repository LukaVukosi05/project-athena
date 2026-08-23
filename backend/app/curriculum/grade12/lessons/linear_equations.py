"""Teacher-reviewable algebra-readiness vertical slice: linear equations."""
from app.curriculum.schemas import (AccessLevel, ContentStatus, Lesson, LessonBlock,
    MathematicalOperation, StepExplanation, TeachingStep, WhiteboardBlock, WhiteboardQuestion)
from app.whiteboard.linear_equations import solve_linear_equation

def explain(what, why, purpose, remember="Keep both sides balanced."):
    return StepExplanation(what=what, why=why, purpose=purpose, remember=remember)

def board(identifier, problem, changes):
    solution = solve_linear_equation(problem)
    if solution is None: raise ValueError(f"Unverified equation: {problem}")
    answer = str(solution.numerator) if solution.denominator == 1 else str(solution)
    steps = [TeachingStep(step_number=0, title="Plan the solution", before_expression=problem,
        working_expression=problem, operation=MathematicalOperation(type="identify_objective", value="x"),
        after_expression=problem, explanation=explain("Identify the operations around x.",
        "A plan prevents sign and order mistakes.", "Choose a valid first transformation."),
        animation_template="identify_unknown", screen_reader_description=f"The equation is {problem}. The unknown is identified.")]
    before = problem
    for title, working, after in changes:
        steps.append(TeachingStep(step_number=len(steps), title=title, before_expression=before,
            working_expression=working, operation=MathematicalOperation(type="equivalent_transform"),
            after_expression=after, explanation=explain(title,
            "This transformation preserves the solution while simplifying the equation.", "Move closer to isolating x."),
            common_mistake="Check signs, brackets and denominators before simplifying.",
            animation_template="equation_transformation", screen_reader_description=f"{working}, which simplifies to {after}."))
        before = after
    steps.append(TeachingStep(step_number=len(steps), title="Verify the solution", before_expression=before,
        working_expression=f"Substitute x = {answer} into {problem}",
        operation=MathematicalOperation(type="substitute_value", value=answer),
        after_expression=f"x = {answer}; substitute in the original equation; left side = right side ✓",
        explanation=explain("Substitute the answer into the original equation.",
        "A true statement confirms the solution.", "Catch arithmetic or sign errors.", "Check the original equation."),
        animation_template="substitution_verification", screen_reader_description=f"Substitution verifies x equals {answer}."))
    return WhiteboardBlock(id=identifier, problem=f"Solve {problem}", initial_expression=problem, steps=steps)

SPECS = [
 ("wbq-001","foundation","2x + 5 = 15",[("Subtract 5","2x + 5 - 5 = 15 - 5","2x = 10"),("Divide by 2","2x / 2 = 10 / 2","x = 5")]),
 ("wbq-002","foundation","3x - 4 = 17",[("Add 4","3x - 4 + 4 = 17 + 4","3x = 21"),("Divide by 3","3x / 3 = 21 / 3","x = 7")]),
 ("wbq-003","easy","-2x + 3 = 11",[("Subtract 3","-2x + 3 - 3 = 11 - 3","-2x = 8"),("Divide by negative 2","-2x / -2 = 8 / -2","x = -4")]),
 ("wbq-004","easy","7 - 3x = 22",[("Subtract 7","7 - 3x - 7 = 22 - 7","-3x = 15"),("Divide by negative 3","-3x / -3 = 15 / -3","x = -5")]),
 ("wbq-005","standard","3(x + 2) = 21",[("Expand the bracket","3x + 6 = 21","3x + 6 = 21"),("Subtract 6","3x = 15","3x = 15"),("Divide by 3","3x / 3 = 15 / 3","x = 5")]),
 ("wbq-006","standard","2(x - 4) + 3 = 15",[("Expand and simplify","2x - 8 + 3 = 15","2x - 5 = 15"),("Add 5","2x = 20","2x = 20"),("Divide by 2","2x / 2 = 20 / 2","x = 10")]),
 ("wbq-007","intermediate","5x + 3 = 2x + 18",[("Collect x terms","5x - 2x + 3 = 18","3x + 3 = 18"),("Subtract 3","3x = 15","3x = 15"),("Divide by 3","3x / 3 = 15 / 3","x = 5")]),
 ("wbq-008","intermediate","4(x - 2) = 2x + 10",[("Expand","4x - 8 = 2x + 10","4x - 8 = 2x + 10"),("Collect x terms","2x - 8 = 10","2x - 8 = 10"),("Add 8","2x = 18","2x = 18"),("Divide by 2","2x / 2 = 18 / 2","x = 9")]),
 ("wbq-009","exam","(x + 3) / 4 = 5",[("Multiply by 4","x + 3 = 20","x + 3 = 20"),("Subtract 3","x = 17","x = 17")]),
 ("wbq-010","exam","(2x - 5) / 3 + 2 = 7",[("Subtract 2","(2x - 5) / 3 = 5","(2x - 5) / 3 = 5"),("Multiply by 3","2x - 5 = 15","2x - 5 = 15"),("Add 5 and divide","2x = 20; x = 10","x = 10")]),
 ("wbq-011","advanced","3(2x - 1) - 2(x + 4) = 9",[("Expand","6x - 3 - 2x - 8 = 9","4x - 11 = 9"),("Add 11","4x = 20","4x = 20"),("Divide by 4","4x / 4 = 20 / 4","x = 5")]),
 ("wbq-012","expert","(x - 2) / 3 + (x + 1) / 2 = 5",[("Clear denominators","2(x - 2) + 3(x + 1) = 30","2(x - 2) + 3(x + 1) = 30"),("Expand","2x - 4 + 3x + 3 = 30","5x - 1 = 30"),("Add 1","5x = 31","5x = 31"),("Divide by 5","5x / 5 = 31 / 5","x = 31 / 5")]),
]
GUIDANCE = ["high"]*3 + ["moderate"]*4 + ["reduced"]*3 + ["minimal"]*2
QUESTIONS = [WhiteboardQuestion(id=i, order=n+1, difficulty=d, estimated_minutes=3,
    is_core_example=n == 0, guidance_level=GUIDANCE[n], whiteboard=board(i,p,s))
    for n,(i,d,p,s) in enumerate(SPECS)]

# Preserve the original public block contract for older clients. New clients use
# ``whiteboard_questions`` and start with the 2x + 5 canonical example above.
LEGACY_BOARD = board("solve-3x-plus-7", "3x + 7 = 22", [
    ("Remove the plus seven", "3x + 7 - 7 = 22 - 7", "3x = 15"),
    ("Leave one x", "3x / 3 = 15 / 3", "x = 5"),
])
LEGACY_BOARD.steps[1] = LEGACY_BOARD.steps[1].model_copy(update={
    "operation": MathematicalOperation(type="subtract_both_sides", value=7),
    "animation_template": "equation_balance_subtraction",
})
LEGACY_BOARD.steps[2] = LEGACY_BOARD.steps[2].model_copy(update={
    "operation": MathematicalOperation(type="divide_both_sides", value=3),
    "animation_template": "equation_balance_division",
})
LEGACY_BOARD.steps[3] = LEGACY_BOARD.steps[3].model_copy(update={
    "working_expression": "3(5) + 7 = 22; 15 + 7 = 22; 22 = 22 ✓",
    "after_expression": "3(5) + 7 = 22; 15 + 7 = 22; 22 = 22 ✓",
})

LINEAR_EQUATIONS = Lesson(id="g12-readiness-linear-equations", order=1,
 title="Solving linear equations by keeping the balance",
 objective="Solve a linear equation and explain why each operation is valid.",
 why_it_matters="Equation skills support functions, finance, trigonometry, calculus and both final examination papers.",
 intuition="An equation is balanced. Undo operations around x while applying the same operation to both sides.",
 prerequisites=["g12-readiness-algebraic-manipulation"], estimated_minutes=35, difficulty="foundation",
 access_level=AccessLevel.FREE, status=ContentStatus.TEACHER_REVIEW_REQUIRED, mastery_threshold=.8,
 whiteboard_questions=QUESTIONS, blocks=[
  LessonBlock(type="concept",title="Intuition first",content="Think of the equals sign as a balance: both expressions have the same value."),
  LEGACY_BOARD,
  LessonBlock(type="practice",title="Self-guided practice",content="Solve, submit, then compare your method.",data={"assessment_mode":"self_guided","questions":[{
   "question":"Solve 5x - 8 = 27","difficulty":"foundation","input_type":"math","accepted_answers":["x = 7","x=7","7"],"answer":"x = 7","explanation":"x = 7 makes the original equation true.",
   "hints":["Undo subtraction before multiplication.","Add 8 to both sides."],
   "solution_steps":["5x - 8 = 27","5x - 8 + 8 = 27 + 8","5x = 35","5x / 5 = 35 / 5","x = 7","Check: 5(7) - 8 = 27","35 - 8 = 27","27 = 27 ✓"],
   "why_explanations":[None,"Add 8 to both sides to preserve equality.","Simplify both sides.","Divide both sides by 5 to leave one x.","State the solution.","Substitute into the original equation.","Simplify the left side.","Both sides agree, so the solution is verified."]}]}),
  LessonBlock(type="checkpoint",title="What should happen next?",content="Choose the same valid operation for both sides.",data={"options":["Subtract 7 from both sides","Add 7 to the right only","Divide only x by 3"],"correct_index":0}),
  LessonBlock(type="practice",title="Guided practice",content="Solve 4x + 6 = 26.",data={"hint":"Undo +6 before ×4.","answer":"x = 5","mode":"guided"}),
  LessonBlock(type="practice",title="Independent practice",content="Show every balancing operation.",data={"questions":["2x + 9 = 19","5x - 4 = 31","7 - 3x = 22"],"difficulty":["foundation","standard","exam"]}),
  LessonBlock(type="mistake",title="Watch out",content="Changing only one side breaks equality. Apply every balancing operation to both sides."),
  LessonBlock(type="memory_tip",title="Memory tool",content="Same operation, both sides; undo from the outside in."),
  LessonBlock(type="summary",title="Key takeaways",content="Preserve equality, isolate x, then verify in the original equation.")])
