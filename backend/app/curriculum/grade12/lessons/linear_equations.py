"""Algebra readiness vertical slice: linear equations."""

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    StepExplanation, TeachingStep, WhiteboardBlock,
)


def explanation(what: str, why: str, purpose: str, remember: str) -> StepExplanation:
    return StepExplanation(what=what, why=why, purpose=purpose, remember=remember)


LINEAR_EQUATIONS = Lesson(
    id="g12-readiness-linear-equations",
    order=1,
    title="Solving linear equations by keeping the balance",
    objective="Solve a linear equation and explain why each operation is valid.",
    why_it_matters="Equation skills are used throughout functions, finance, trigonometry, calculus and both final examination papers.",
    intuition="An equation is a balanced statement. We undo operations around x in reverse order while applying the same valid operation to both sides.",
    prerequisites=["g12-readiness-algebraic-manipulation"],
    estimated_minutes=20,
    difficulty="foundation",
    access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    mastery_threshold=0.8,
    blocks=[
        LessonBlock(type="concept", title="Intuition first", content="Think of the equals sign as a balance: both expressions have the same value."),
        WhiteboardBlock(
            id="solve-3x-plus-7",
            problem="Solve 3x + 7 = 22",
            initial_expression="3x + 7 = 22",
            steps=[
                TeachingStep(step_number=0, title="Identify the objective",
                    before_expression="3x + 7 = 22",
                    working_expression="3x + 7 = 22",
                    operation=MathematicalOperation(type="identify_objective", value="x"),
                    after_expression="3x + 7 = 22",
                    explanation=explanation("Find the value of x.", "x is combined with multiplication by 3 and addition of 7.", "Plan to undo those operations in reverse order.", "Undo operations from the outside in."),
                    animation_template="identify_unknown",
                    screen_reader_description="The original equation is 3 x plus 7 equals 22. The x term is highlighted as the unknown."),
                TeachingStep(step_number=1, title="Remove the plus seven",
                    before_expression="3x + 7 = 22",
                    working_expression="3x + 7 - 7 = 22 - 7",
                    operation=MathematicalOperation(type="subtract_both_sides", value=7),
                    after_expression="3x = 15",
                    explanation=explanation("Subtract 7 from both sides.", "The plus 7 prevents the term containing x from being isolated.", "Cancellation leaves only 3x on the left.", "An equation is a balance: use the same operation on both sides."),
                    common_mistake="It may look as though 7 moved and changed sign. Mathematically, 7 was subtracted from both sides.",
                    animation_template="equation_balance_subtraction",
                    screen_reader_description="Minus 7 appears under both sides. Plus 7 and minus 7 cancel on the left; 22 minus 7 becomes 15."),
                TeachingStep(step_number=2, title="Leave one x",
                    before_expression="3x = 15",
                    working_expression="3x / 3 = 15 / 3",
                    operation=MathematicalOperation(type="divide_both_sides", value=3),
                    after_expression="x = 5",
                    explanation=explanation("Divide both sides by 3.", "3x means 3 multiplied by x.", "Dividing by 3 leaves one x.", "Undo multiplication with division."),
                    common_mistake="Divide the complete expression on each side, not only a convenient term.",
                    animation_template="equation_balance_division",
                    screen_reader_description="Both sides are divided by 3. The threes cancel on the left and 15 divided by 3 is 5."),
                TeachingStep(step_number=3, title="Verify the solution",
                    before_expression="x = 5",
                    working_expression="3(5) + 7 = 22; 15 + 7 = 22; 22 = 22 ✓",
                    operation=MathematicalOperation(type="substitute_value", value=5),
                    after_expression="3(5) + 7 = 22; 15 + 7 = 22; 22 = 22 ✓",
                    explanation=explanation("Substitute x equals 5 into the original equation.", "A proposed solution is correct only if it makes the original equation true.", "The true statement verifies the answer.", "Always check in the original equation, not a rearranged line."),
                    animation_template="substitution_verification",
                    screen_reader_description="Substitution gives 3 times 5 plus 7 equals 22, then 22 equals 22, verified."),
            ],
        ),
        LessonBlock(type="checkpoint", title="What should happen next?", content="Choose the same valid operation for both sides.", data={"options": ["Subtract 7 from both sides", "Add 7 to the right only", "Divide only x by 3"], "correct_index": 0}),
        LessonBlock(type="practice", title="Guided practice", content="Solve 4x + 6 = 26.", data={"hint": "Undo +6 before ×4.", "answer": "x = 5", "mode": "guided"}),
        LessonBlock(type="practice", title="Independent practice", content="Show every balancing operation.", data={"questions": ["2x + 9 = 19", "5x - 4 = 31", "7 - 3x = 22"], "difficulty": ["foundation", "standard", "exam"]}),
        LessonBlock(type="mistake", title="Watch out", content="3x + 7 = 22 therefore 3x = 29 is wrong: adding 7 does not undo +7, and changing one side breaks equality."),
        LessonBlock(type="memory_tip", title="Memory tool", content="Same operation, both sides; undo from the outside in."),
        LessonBlock(type="summary", title="Key takeaways", content="Preserve equality, isolate the x-term, isolate x, then verify in the original equation."),
    ],
)
