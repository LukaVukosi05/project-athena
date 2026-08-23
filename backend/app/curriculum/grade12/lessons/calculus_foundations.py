"""Teacher-review-required calculus foundation lessons."""

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    StepExplanation, TeachingStep, WhiteboardBlock,
)
from app.services.graphing import function_graph


def explain(what: str, why: str, purpose: str, remember: str) -> StepExplanation:
    return StepExplanation(what=what, why=why, purpose=purpose, remember=remember)


AVERAGE_RATE = Lesson(
    id="g12-calculus-average-rate",
    order=1,
    title="Average rate of change in an exam question",
    objective="Calculate an average rate of change and interpret its units in context.",
    why_it_matters="Average rate of change prepares you for gradients, first principles and derivative applications in Paper 1.",
    intuition="Rate of change compares how much an output changes with how much the input changes. On a graph, it is the gradient of a secant line joining two points.",
    prerequisites=["g12-readiness-linear-equations", "function notation", "gradient of a straight line"],
    estimated_minutes=25, difficulty="foundation", access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED, mastery_threshold=0.8,
    blocks=[
        LessonBlock(type="concept", title="How this appears in an exam", content="Questions normally give a function and two input values, ask for the average rate of change, and may ask you to interpret the answer using units."),
        LessonBlock(type="checkpoint", title="Prerequisite check", content="For f(x)=x²+1, calculate f(2).", data={"options": ["3", "5", "6"], "correct_index": 1, "feedback": "Substitute 2 for every x: 2²+1=5."}),
        WhiteboardBlock(id="tank-average-rate",
            problem="EXAM-STYLE QUESTION: The volume of water in a tank is V(t)=t²+4t+10 litres, where t is measured in minutes. Calculate the average rate at which the volume changes from t=2 to t=5. Interpret your answer.",
            initial_expression="V(t)=t²+4t+10; t₁=2; t₂=5",
            graph_spec=function_graph(range(7), [10, 15, 22, 31, 42, 55, 70], title="V(t) = t² + 4t + 10", x_label="time (minutes)", y_label="volume (litres)", points=[(2, 22, "start"), (5, 55, "end")]),
            steps=[
                TeachingStep(step_number=0, title="Identify what the question gives",
                    before_expression="V(t)=t²+4t+10; t₁=2; t₂=5", operation=MathematicalOperation(type="identify_interval", value="2 to 5"), after_expression="V(t)=t²+4t+10; t₁=2; t₂=5",
                    explanation=explain("Identify the function and the two times.", "Average change needs a starting point and an ending point.", "This tells us which two function values to calculate.", "Underline the function, both inputs, and the units before calculating."),
                    common_mistake="Using 5−2 as the numerator. Input change belongs in the denominator.", animation_template="rate_change_setup", screen_reader_description="The volume function and the interval from 2 to 5 minutes are identified."),
                TeachingStep(step_number=1, title="Calculate the starting volume",
                    before_expression="V(t)=t²+4t+10; t₁=2; t₂=5", operation=MathematicalOperation(type="substitute_function_value", value=2), after_expression="V(2)=2²+4(2)+10=22 litres",
                    explanation=explain("Substitute t=2 into the function.", "We need the output at the beginning of the interval.", "This gives the starting volume for the change calculation.", "Use brackets when substituting a value into every occurrence of the variable."),
                    common_mistake="Substituting 2 into only one t-term.", animation_template="function_substitution", screen_reader_description="At 2 minutes the volume is 22 litres."),
                TeachingStep(step_number=2, title="Calculate the ending volume",
                    before_expression="V(2)=2²+4(2)+10=22 litres", operation=MathematicalOperation(type="substitute_function_value", value=5), after_expression="V(5)=5²+4(5)+10=55 litres; V(2)=22 litres",
                    explanation=explain("Substitute t=5 into the same function.", "We also need the output at the end of the interval.", "This gives the ending volume.", "Keep the two function values clearly labelled so they are not reversed."),
                    common_mistake="Writing V(5)=5²+4+10 and forgetting to multiply 4 by 5.", animation_template="function_substitution", screen_reader_description="At 5 minutes the volume is 55 litres."),
                TeachingStep(step_number=3, title="Form the average-rate quotient",
                    before_expression="V(5)=5²+4(5)+10=55 litres; V(2)=22 litres", operation=MathematicalOperation(type="calculate_average_rate", value="[V(5)−V(2)]/[5−2]"), after_expression="Average rate = (55−22)/(5−2)=33/3=11 litres per minute",
                    explanation=explain("Divide the change in volume by the change in time.", "A rate compares output change with input change.", "The quotient gives the secant gradient over the interval.", "Average rate = change in output over change in input; keep the subtraction order consistent."),
                    common_mistake="Reversing only one subtraction gives the wrong sign.", animation_template="average_rate_quotient", screen_reader_description="The change of 33 litres divided by 3 minutes gives 11 litres per minute."),
                TeachingStep(step_number=4, title="Interpret the answer",
                    before_expression="Average rate = (55−22)/(5−2)=33/3=11 litres per minute", operation=MathematicalOperation(type="interpret_rate", value="litres per minute"), after_expression="From 2 to 5 minutes, the tank's volume increased by an average of 11 litres each minute.",
                    explanation=explain("State what 11 means in the situation.", "An unexplained number does not fully answer an interpretation question.", "This connects the calculation to the physical context and earns interpretation marks.", "An average rate describes the whole interval, not necessarily the rate at every instant."),
                    common_mistake="Saying the tank contains 11 litres. Eleven is a rate, not a volume.", animation_template="rate_interpretation", screen_reader_description="The result is interpreted as an average increase of 11 litres per minute."),
            ]),
        LessonBlock(type="practice", title="Guided practice", content="The distance travelled is s(t)=3t²+2 metres. Find the average velocity from t=1 to t=4.", data={"mode": "guided", "hints": ["Calculate s(1) and s(4).", "Use [s(4)−s(1)]/[4−1].", "Include metres per second."], "worked_answer": ["s(1)=5", "s(4)=50", "(50−5)/3=15 m/s"]}),
        LessonBlock(type="practice", title="Independent and exam practice", content="Write all substitutions and include units where supplied.", data={"questions": [
            {"difficulty": "Foundation", "question": "For f(x)=x²−3x, calculate the average rate of change from x=1 to x=4.", "answer": "2"},
            {"difficulty": "Standard", "question": "For g(x)=2x²+5, find the gradient of the secant joining x=−1 and x=3.", "answer": "4"},
            {"difficulty": "Exam", "question": "A particle's displacement is s(t)=t³−6t²+9t metres. Calculate and interpret its average velocity during the first 3 seconds.", "answer": "0 m/s; its net displacement over the interval is zero."},
            {"difficulty": "Challenge", "question": "For f(x)=x², show that the average rate from x=a to x=a+h is 2a+h.", "answer": "[(a+h)²−a²]/h=2a+h, h≠0."}
        ]}),
        LessonBlock(type="mistake", title="Common exam mistakes", content="Do not confuse average rate with f(5)−f(2), omit the denominator, reverse only one subtraction, drop units, or describe an average as an instantaneous rate."),
        LessonBlock(type="memory_tip", title="Memory tool", content="Output change over input change: Δy/Δx. Same order on top and bottom."),
        LessonBlock(type="summary", title="Lesson summary", content="Find both outputs, subtract consistently, divide by the input change, simplify, attach compound units, and interpret the result over the stated interval."),
    ])


SECANT_TO_TANGENT = Lesson(
    id="g12-calculus-secant-to-tangent", order=1,
    title="From a secant line to a tangent", objective="Explain how secant gradients approach an instantaneous gradient.",
    why_it_matters="This visual idea is the foundation of first-principles differentiation and derivative notation.",
    intuition="A secant uses two points. Move the second point closer to the first: the secant turns toward the tangent and its gradient approaches the instantaneous gradient.",
    prerequisites=["g12-calculus-average-rate"], estimated_minutes=25,
    difficulty="foundation", access_level=AccessLevel.FREE,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED, mastery_threshold=0.8,
    blocks=[
        LessonBlock(type="concept", title="Exam language", content="An exam may ask for a gradient from first principles, the gradient at a point, or the equation of a tangent. All three depend on this secant-to-tangent idea."),
        WhiteboardBlock(id="secant-to-tangent-x-squared", problem="CONCEPT-TO-EXAM QUESTION: For f(x)=x², explain why the gradient at x=2 is 4 by considering a second point at x=2+h.", initial_expression="P(2,4) and Q(2+h,(2+h)²)", graph_spec=function_graph([-2,-1,0,1,2,3,4], [4,1,0,1,4,9,16], title="f(x) = x²", points=[(2,4,"P"),(3,9,"Q")]), steps=[
            TeachingStep(step_number=0, title="Place two points on the curve", before_expression="P(2,4) and Q(2+h,(2+h)²)", operation=MathematicalOperation(type="draw_secant", value="P to Q"), after_expression="P(2,4) and Q(2+h,(2+h)²)", explanation=explain("Join P and Q with a secant.", "Two distinct points determine an average gradient.", "This creates a measurable gradient near x=2.", "Secant means two points; tangent touches at the target point."), animation_template="secant_line", screen_reader_description="A secant joins P at x equals 2 to Q at x equals 2 plus h."),
            TeachingStep(step_number=1, title="Calculate the secant gradient", before_expression="P(2,4) and Q(2+h,(2+h)²)", operation=MathematicalOperation(type="calculate_secant_gradient", value="h"), after_expression="mₛ=[(2+h)²−4]/h=4+h, h≠0", explanation=explain("Use change in y over change in x.", "The secant gradient is the average rate between P and Q.", "Simplifying exposes what happens as h gets smaller.", "Expand first, factor h, then cancel; never substitute h=0 before cancelling."), common_mistake="Putting h=0 into the original quotient causes division by zero.", animation_template="secant_gradient", screen_reader_description="The secant gradient simplifies to 4 plus h for non-zero h."),
            TeachingStep(step_number=2, title="Move Q toward P", before_expression="mₛ=[(2+h)²−4]/h=4+h, h≠0", operation=MathematicalOperation(type="approach_limit", value="h→0"), after_expression="As h→0, mₛ=4+h→4", explanation=explain("Let h approach zero.", "Q moves closer to P while remaining distinct during the calculation.", "The secant gradients approach the tangent gradient.", "A limit approaches zero; it does not divide by zero."), animation_template="secant_approaches_tangent", screen_reader_description="Point Q approaches P and the secant gradient approaches 4."),
            TeachingStep(step_number=3, title="State the instantaneous gradient", before_expression="As h→0, mₛ=4+h→4", operation=MathematicalOperation(type="draw_tangent", value=4), after_expression="f′(2)=4", explanation=explain("Draw the tangent at P and state its gradient.", "The tangent is the limiting position of the secant.", "This gives the instantaneous rate at x=2.", "The derivative at a point is the tangent gradient there."), animation_template="tangent_at_point", screen_reader_description="The tangent at x equals 2 has gradient 4, so f prime of 2 equals 4."),
        ]),
        LessonBlock(type="practice", title="Practice", content="Answer in words and algebra.", data={"questions": [
            {"difficulty": "Foundation", "question": "What is the difference between a secant and a tangent?", "answer": "A secant uses two curve points; a tangent gives the limiting gradient at one point."},
            {"difficulty": "Standard", "question": "For f(x)=x², simplify [f(3+h)−f(3)]/h.", "answer": "6+h, h≠0."},
            {"difficulty": "Exam", "question": "Hence determine f′(3) and explain the limiting step.", "answer": "f′(3)=6 because 6+h approaches 6 as h approaches zero."}
        ]}),
        LessonBlock(type="summary", title="Lesson summary", content="A secant measures average change. As its second point approaches the first, its gradient approaches the tangent gradient—the derivative at that point."),
    ])

from app.curriculum.grade12.lessons.calculus_question_sets import rate_questions, tangent_questions
AVERAGE_RATE = AVERAGE_RATE.model_copy(update={"whiteboard_questions": rate_questions()})
SECANT_TO_TANGENT = SECANT_TO_TANGENT.model_copy(update={"whiteboard_questions": tangent_questions()})
