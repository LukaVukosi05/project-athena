"""Reviewed Batch 1 runtime lessons for Grade 12 Sequences and Series."""
from fractions import Fraction

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, TeachingStep, TimelineEvent,
    VisualizationInstruction, VisualizationState, WhiteboardBlock,
    WhiteboardQuestion,
)


def explanation(what: str, why: str, purpose: str, remember: str) -> StepExplanation:
    return StepExplanation(what=what, why=why, purpose=purpose, remember=remember)


def differences(values: list[int | float]) -> list[int | float]:
    return [values[index + 1] - values[index] for index in range(len(values) - 1)]


def sequence_kind(values: list[int | float]) -> tuple[str, str]:
    first = differences(values)
    if len(set(first)) == 1:
        return "arithmetic", f"constant first difference {first[0]:g}"
    if all(value != 0 for value in values[:-1]):
        ratios = [Fraction(values[index + 1]).limit_denominator() / Fraction(values[index]).limit_denominator() for index in range(len(values) - 1)]
        if len(set(ratios)) == 1:
            return "geometric", f"constant ratio {ratios[0]}"
    second = differences(first)
    if second and len(set(second)) == 1:
        return "quadratic", f"constant second difference {second[0]:g}"
    return "neither", "no constant first difference, ratio, or second difference"


def objects_for(values: list[int | float], kind: str) -> list[SemanticObject]:
    result = []
    for index, value in enumerate(values):
        result.extend([
            SemanticObject(id=f"position-{index + 1}", type="position", value=str(index + 1), group="positions"),
            SemanticObject(id=f"term-{index + 1}", type="term", value=f"{value:g}", group="terms"),
        ])
    first = differences(values)
    ratios = [Fraction(values[index + 1]).limit_denominator() / Fraction(values[index]).limit_denominator() for index in range(len(values)-1)] if kind == "geometric" else []
    for index, value in enumerate(ratios if ratios else first):
        result.append(SemanticObject(id=f"difference-{index + 1}", type="ratio" if ratios else "difference", value=f"×{value}" if ratios else f"{value:+g}", group="ratios" if ratios else "first-differences"))
    for index, value in enumerate(differences(differences(values))):
        result.append(SemanticObject(id=f"second-difference-{index + 1}", type="difference", value=f"{value:+g}", group="second-differences"))
    result.extend([
        SemanticObject(id="goal", type="label", value="Classify the sequence", group="instruction"),
        SemanticObject(id="classification", type="result", value="classification", group="result"),
        SemanticObject(id="verification", type="verification", value="verified", group="verification"),
        SemanticObject(id="predicted-change", type="operation", value="next change", group="prediction"),
        SemanticObject(id="next-term", type="term", value="next term", group="prediction"),
    ])
    return result


def paired_speech(at_ms: int, text: str) -> list[TimelineEvent]:
    return [TimelineEvent(at_ms=at_ms, type="narration", text=text), TimelineEvent(at_ms=at_ms, type="caption", text=text)]


def classification_board(identifier: str, values: list[int | float]) -> tuple[WhiteboardBlock, str, list[str]]:
    kind, evidence = sequence_kind(values)
    prompt = f"Classify {', '.join(f'{value:g}' for value in values)}, …"
    first = differences(values); second = differences(first)
    object_ids = [f"term-{index + 1}" for index in range(len(values))]
    position_ids = [f"position-{index + 1}" for index in range(len(values))]
    ratios = [Fraction(values[index + 1]).limit_denominator() / Fraction(values[index]).limit_denominator() for index in range(len(values)-1)] if kind == "geometric" else []
    operation_events=[]
    for index in range(len(first)):
        start=450+index*850
        operation=f"{values[index+1]:g} ÷ {values[index]:g} = {ratios[index]}" if ratios else f"{values[index+1]:g} − {values[index]:g} = {first[index]:g}"
        operation_events.extend([TimelineEvent(at_ms=start,type="focus",targets=object_ids[index:index+2],style="operation"),TimelineEvent(at_ms=start+220,type="calculate_ratio" if ratios else "calculate_difference",targets=[f"difference-{index+1}"],label=operation),TimelineEvent(at_ms=start+520,type="draw_arrow",from_target=object_ids[index],to_target=object_ids[index+1],label=f"×{ratios[index]}" if ratios else f"{first[index]:+g}",targets=[f"difference-{index+1}"])])
    inspect_text = "Compare each consecutive change before choosing a sequence type."
    classify_text = f"The evidence is {evidence}, so this sequence is {kind}."
    states = [prompt, f"First differences: {', '.join(f'{x:+g}' for x in first)}", f"{kind}: {evidence}", f"Verified: {evidence}", f"Final answer: {kind}"]
    comparison_ids = [f"second-difference-{i+1}" for i in range(len(second))] if kind == "quadratic" else [f"difference-{i+1}" for i in range(len(first))]
    select_events = [TimelineEvent(at_ms=0,type="align",targets=[f"difference-{i+1}" for i in range(len(first))])]
    if kind == "quadratic":
        for i in range(len(second)):
            start=400+i*650
            select_events.extend([TimelineEvent(at_ms=start,type="focus",targets=[f"difference-{i+1}",f"difference-{i+2}"],style="operation"),TimelineEvent(at_ms=start+180,type="calculate_difference",targets=[f"second-difference-{i+1}"],label=f"{first[i+1]:g} − {first[i]:g} = {second[i]:g}"),TimelineEvent(at_ms=start+430,type="draw_arrow",from_target=f"difference-{i+1}",to_target=f"difference-{i+2}",label=f"{second[i]:+g}",targets=[f"second-difference-{i+1}"])])
    select_events.extend([TimelineEvent(at_ms=1800,type="compare",targets=comparison_ids,style="matching_pattern"),TimelineEvent(at_ms=2300,type="reveal",targets=["classification"],style="result"),*paired_speech(2500,classify_text)])
    steps = [
        TeachingStep(id="orient", step_number=0, title="Orient", instructional_goal="Identify the given terms and classification goal", duration_ms=3200,
            before_expression=states[0], working_expression=states[0], operation=MathematicalOperation(type="timeline_orient"), after_expression=states[0],
            explanation=explanation("Read the full sequence.", "We need evidence before selecting a formula.", "Separate what is given from what must be found.", "Increasing values alone do not prove an arithmetic sequence."),
            animation_template="semantic_timeline", screen_reader_description=f"Term positions are aligned above sequence values {values}; the goal is to classify the sequence.", visualization_state=VisualizationState(objects=position_ids+object_ids, highlights=["goal"]),
            events=[TimelineEvent(at_ms=0,type="reveal",targets=position_ids+object_ids),TimelineEvent(at_ms=400,type="focus",targets=object_ids,style="given"),TimelineEvent(at_ms=900,type="reveal",targets=["goal"],style="target"),*paired_speech(1200,"We are given a sequence and need to determine its type. We will compare consecutive terms before choosing a formula.")], narration="We are given a sequence and need to determine its type. We will compare consecutive terms before choosing a formula."),
        TeachingStep(id="inspect", step_number=1, title="Inspect consecutive terms", instructional_goal="Make each first difference visible", duration_ms=4200,
            before_expression=states[0], working_expression=states[1], operation=MathematicalOperation(type="timeline_inspect"), after_expression=states[1],
            explanation=explanation("Subtract consecutive terms.", "A constant first difference is the arithmetic test.", "Make the changes visible before classifying.", "Use ratios only when differences are not constant."), common_mistake="Do not classify from appearance alone.",
            animation_template="semantic_timeline", screen_reader_description=f"First differences are {first}.", visualization_state=VisualizationState(objects=object_ids+[f"difference-{i+1}" for i in range(len(first))],highlights=["first-differences"]),
            events=[TimelineEvent(at_ms=0,type="dim",targets=object_ids[2:]),*operation_events,*paired_speech(3300,inspect_text)], narration=inspect_text),
        TeachingStep(id="select", step_number=2, title="Select the classification", instructional_goal="Compare the calculated changes", duration_ms=3600,
            before_expression=states[1], working_expression=states[2], operation=MathematicalOperation(type="timeline_select"), after_expression=states[2],
            explanation=explanation("Compare the difference rows.", "The first valid constant pattern determines the classification.", "Connect visual evidence to mathematical language.", "Quadratic means constant second differences, not merely curved growth."),
            animation_template="semantic_timeline", screen_reader_description=classify_text, visualization_state=VisualizationState(objects=["classification"],highlights=["classification"]), state_after={"classification":kind,"evidence":evidence},
            events=select_events, narration=classify_text),
        TeachingStep(id="verify", step_number=3, title="Verify the pattern", instructional_goal="Confirm the classification against every displayed term", duration_ms=3000,
            before_expression=states[2], working_expression=states[3], operation=MathematicalOperation(type="timeline_verify"), after_expression=states[3],
            explanation=explanation("Check every consecutive relationship.", "One matching pair is not enough evidence.", "Confirm the rule across the displayed sequence.", "Verification must use the original terms."),
            animation_template="semantic_timeline", screen_reader_description=f"Verification confirms {evidence}.", visualization_state=VisualizationState(objects=["verification"],highlights=["verification"]),
            events=[TimelineEvent(at_ms=0,type="verify",targets=["verification"],style="verification"),*paired_speech(700,f"Checking every displayed term confirms the {evidence}.")], narration=f"Checking every displayed term confirms the {evidence}."),
        TeachingStep(id="summarize", step_number=4, title="Summarise", instructional_goal="State the conclusion and misconception to avoid", duration_ms=3000,
            before_expression=states[3], working_expression=states[4], operation=MathematicalOperation(type="timeline_summarize"), after_expression=states[4],
            explanation=explanation(f"The sequence is {kind}.", f"It has {evidence}.", "Retain the test used to justify the answer.", "Do not name a pattern from direction or size alone."), common_mistake="Classification requires a calculated difference or ratio test.",
            animation_template="semantic_timeline", screen_reader_description=f"Final classification: {kind} because it has {evidence}.", visualization_state=VisualizationState(objects=["classification","verification"],highlights=["classification"]),
            events=[TimelineEvent(at_ms=0,type="focus",targets=["classification"],style="result"),*paired_speech(500,f"The sequence is {kind} because it has {evidence}. Classify from evidence, not appearance.")], narration=f"The sequence is {kind} because it has {evidence}. Classify from evidence, not appearance."),
    ]
    if kind == "arithmetic": next_change=first[-1]; next_term=values[-1]+next_change
    elif kind == "geometric": next_change=f"×{ratios[-1]}"; next_term=Fraction(values[-1]).limit_denominator()*ratios[-1]
    elif kind == "quadratic": next_change=first[-1]+second[-1]; next_term=values[-1]+next_change
    else: next_change="retest"; next_term="unknown"
    verification_text=f"The predicted next change is {next_change}; the next term is {next_term}. This extends the same calculated structure."
    steps[3].duration_ms=3600;steps[3].working_expression=f"Predict the next term after {values[-1]:g}";steps[3].after_expression=f"Verified next term: {next_term}"
    steps[3].events=[TimelineEvent(at_ms=0,type="checkpoint",checkpoint_type="calculate_value",text="What should the next change and next term be?"),TimelineEvent(at_ms=700,type="reveal",targets=["predicted-change"],label=str(next_change),style="operation"),TimelineEvent(at_ms=1300,type="reveal",targets=["next-term"],label=str(next_term),style="result"),TimelineEvent(at_ms=1900,type="verify",targets=["verification"],style="verification"),*paired_speech(2200,verification_text)];steps[3].narration=verification_text;steps[3].state_after={"next_change":str(next_change),"next_term":str(next_term),"verified":True}
    steps[4].before_expression=steps[3].after_expression
    params={"terms":values,"positions":list(range(1,len(values)+1)),"mode":"classification","title":prompt,"differences":first,"next_term":str(next_term),"next_change":str(next_change)}
    if ratios: params["ratios"]=[str(value) for value in ratios]
    if second: params["second_differences"]=second
    board=WhiteboardBlock(id=identifier,representation="visual",problem=prompt,initial_expression=states[0],semantic_objects=objects_for(values,kind),visualization=VisualizationInstruction(type="sequences",template="sequence_timeline",parameters=params),steps=steps)
    memo=[f"First differences: {first}.", f"Conclusion: {kind}; {evidence}.", "Verification: the relationship holds for every displayed consecutive pair."]
    return board, kind, memo


CLASSIFICATION_EXAMPLES = [
    # The first three reproduce the primary teaching sequence in the approved pack.
    ([5,9,13,17],"foundation","arithmetic"),
    ([3,6,12,24],"foundation","geometric"),
    ([2,6,12,20],"foundation","quadratic"),
    # Further examples are all taken from examples or practice in the same pack.
    ([18,13,8,3],"easy","arithmetic"),
    ([7,12,17,22],"easy","arithmetic"),
    ([81,27,9,3],"standard","geometric"),
    ([2,8,32,128],"standard","geometric"),
    ([1,5,11,19],"standard","quadratic"),
    ([3,8,15,24],"intermediate","quadratic"),
    ([4,10,18,28],"intermediate","mixed"),
    ([64,32,16,8],"exam","mixed"),
    ([1,6,15,28],"advanced","misconception"),
]

def question(identifier: str, order: int, difficulty: str, built, misconception: str) -> WhiteboardQuestion:
    board,answer,memo=built
    return WhiteboardQuestion(id=identifier,order=order,difficulty=difficulty,estimated_minutes=5,is_core_example=order==1,guidance_level="high" if order<=3 else "moderate" if order<=7 else "reduced" if order<=10 else "minimal",whiteboard=board,cognitive_level="knowledge" if order<=2 else "routine" if order<=7 else "complex" if order<=10 else "problem_solving",marks=2 if order<=7 else 4,answer=answer,full_memo=memo,misconception_tags=[misconception])


def lesson_one_questions():
    return [question(f"sequence-structure-{i:02}",i,difficulty,classification_board(f"sequence-structure-board-{i:02}",values),"classify-by-appearance" if category == "misconception" else f"{category}-classification") for i,(values,difficulty,category) in enumerate(CLASSIFICATION_EXAMPLES,1)]


LESSON_PACK_METADATA = [
    (1,"Recognising sequence structure","Classify arithmetic, geometric and quadratic patterns using evidence, not appearance.","A sequence is an ordered list. The position is n and the value at that position is T_n. Arithmetic sequences have a constant first difference. Geometric sequences have a constant non-zero ratio. Quadratic patterns have constant second differences. A pattern must be tested before a rule is chosen."),
    (2,"Arithmetic sequences and the nth term","Derive and use T_n = a + (n−1)d.","The first term is a. To reach term n from term 1, exactly n−1 equal jumps are made. Each jump is d, therefore T_n = a + (n−1)d. The n−1 is structural, not a formula trick."),
    (3,"Solving arithmetic sequence problems","Determine unknown terms, positions and parameters from arithmetic information.","Translate every statement into T_n = a+(n−1)d. Two known terms produce two linear equations in a and d. Solve the equations, then return to the question and check the term position is a positive integer."),
    (4,"Arithmetic sequences in context","Model constant additive change and interpret variables with units.","An arithmetic model is appropriate when the quantity changes by the same amount per equal interval. Define what n=1 represents. Units and starting position determine a; careless indexing changes the whole model."),
    (5,"Geometric sequences and the nth term","Derive and use T_n = ar^(n−1), including negative and fractional ratios.","A geometric sequence multiplies by the same ratio r. From the first term to term n there are n−1 multiplications, so T_n = ar^(n−1). A negative ratio alternates signs; |r|<1 produces decreasing magnitudes."),
    (6,"Geometric parameters and applications","Solve for unknown geometric parameters and model repeated percentage change.","Use T_p=ar^(p−1) and T_q=ar^(q−1). Dividing the equations removes a and gives r^(q−p)=T_q/T_p. In context, repeated percentage growth uses r=1+p/100; decay uses r=1−p/100."),
    (7,"Quadratic number patterns","Find T_n=an²+bn+c from constant second differences.","For T_n=an²+bn+c, the constant second difference equals 2a. After finding a, substitute known terms to find b and c. The method links a difference table to the algebraic rule."),
    (8,"Sigma notation","Expand, interpret and evaluate finite sums written with Σ.","Σ compresses repeated addition. The index starts at the lower limit and ends at the upper limit. Substitute each integer index into the general term. The number of terms from m to n inclusive is n−m+1."),
    (9,"Deriving the arithmetic-series formula","Understand and apply S_n=n/2[2a+(n−1)d]=n/2(a+l).","A series is the sum of sequence terms. Pairing the first and last, second and second-last, produces equal pair sums a+l. The formula is derived from structure and remains valid whether n is odd or even."),
    (10,"Arithmetic-series applications","Model totals where contributions change by a constant amount.","First determine whether the question asks for one term or a cumulative total. Translate units and indexing, find any missing n, then apply the series formula. Interpret negative or non-integer solutions against the context."),
    (11,"Deriving the finite geometric-series formula","Understand and apply S_n=a(r^n−1)/(r−1), r≠1.","Multiplying a geometric series by r shifts every term by one power. Subtracting the aligned expressions cancels the middle terms. Equivalent sign forms are valid; choose one and substitute carefully. If r=1, S_n=na."),
    (12,"Finite geometric-series applications","Use finite sums for repeated multiplicative contributions.","Finite geometric models appear when each contribution is a constant multiple of the previous one: bounces, staged payments, viral sharing and shrinking lengths. Define whether the initial quantity is term 1 and count exactly how many contributions occur."),
    (13,"Infinite geometric series and convergence","Explain convergence and use S_infinity=a/(1−r) only when |r|<1.","An infinite series can have a finite sum when its terms shrink rapidly enough. For |r|<1, r^n approaches 0, so the finite formula approaches a/(1−r). If |r|≥1, terms do not shrink to zero and the geometric series diverges."),
    (14,"Infinite-series applications","Model limits, recurring decimals and endless repeated motion.","An infinite model is justified only when the process repeats indefinitely with a constant ratio whose magnitude is below one. The mathematical limit may describe an idealised total even when the physical process eventually stops."),
    (15,"Mixed sequence and series decisions","Choose the correct model and formula in unfamiliar questions.","The difficult part is often model selection. Ask: one term or total? additive or multiplicative change? finite or infinite? known first/last term or known ratio? Write a short evidence statement before using any formula."),
    (16,"Algebraic and integrated exam problems","Solve multi-step problems combining terms, sums, equations and constraints.","Integrated questions require a chain: translate conditions, solve parameters, construct a rule, then calculate or prove the requested result. Keep exact values until the final line and test all candidate solutions against sequence restrictions."),
    (17,"Error clinic and proof of understanding","Diagnose, explain and repair common Grade 12 sequence errors.","Error analysis develops stronger transfer than repeating correct procedures. A complete correction names the first wrong step, explains the violated idea and supplies a valid replacement."),
    (18,"Paper 1 mastery assessment","Demonstrate independent mastery across routine, complex and problem-solving questions.","This lesson is assessment-led. Learners first work without hints, then use the whiteboard memo to compare reasoning line by line. A score alone is insufficient; error tags determine the required reteach lesson."),
]


def lesson_pack_shell(number: int, title: str, objective: str, teaching: str) -> Lesson:
    return Lesson(id=f"g12-sequences-series-{number:02}",order=number,title=title,objective=objective,
        why_it_matters="This lesson is part of the approved CAPS Paper 1 Sequences and Series learning path.",
        intuition=teaching,prerequisites=[] if number == 1 else [f"g12-sequences-series-{number-1:02}"],
        estimated_minutes=55,difficulty="foundation" if number == 1 else "standard",access_level=AccessLevel.PREMIUM,
        status=ContentStatus.DRAFT,mastery_threshold=.8,blocks=[
            LessonBlock(type="concept",title="Teach the idea",content=teaching),
            LessonBlock(type="summary",title="Authoring status",content="This DOCX-authored lesson is listed in sequence but its interactive whiteboard bank is awaiting the Lesson 1 experience review."),
        ])


_lesson_one_questions = lesson_one_questions()
LESSON_ONE = Lesson(id="g12-sequences-series-01",order=1,title=LESSON_PACK_METADATA[0][1],
    objective=LESSON_PACK_METADATA[0][2],why_it_matters="A pattern must be tested before selecting a formula.",
    intuition=LESSON_PACK_METADATA[0][3],prerequisites=[],estimated_minutes=50,difficulty="foundation",
    access_level=AccessLevel.FREE,status=ContentStatus.DRAFT,mastery_threshold=.8,
    whiteboard_questions=_lesson_one_questions,blocks=[
        LessonBlock(type="concept",title="Teach the idea",content=LESSON_PACK_METADATA[0][3]),
        _lesson_one_questions[0].whiteboard,
        LessonBlock(type="mistake",title="Misconception diagnosis and repair",content="Increasing only describes direction; constant difference proves arithmetic. Test differences, ratios and then second differences before naming the pattern."),
        LessonBlock(type="practice",title="Independent practice",content="Classify each pattern using calculated evidence.",data={"questions":[
            {"question":"Classify 7, 12, 17, 22, …","answer":"Arithmetic, d=5","solution_steps":["12−7=5","17−12=5","22−17=5","The constant first difference proves the sequence is arithmetic."],"difficulty":"foundation"},
            {"question":"Classify 2, 8, 32, 128, …","answer":"Geometric, r=4","solution_steps":["8÷2=4","32÷8=4","128÷32=4","The constant non-zero ratio proves the sequence is geometric."],"difficulty":"standard"},
            {"question":"Classify 1, 5, 11, 19, …","answer":"Quadratic, second difference 2","solution_steps":["First differences: 4, 6, 8","Second differences: 2, 2","The constant second difference proves the pattern is quadratic."],"difficulty":"standard"},
        ]}),
        LessonBlock(type="checkpoint",title="Mastery quiz",content="Use evidence rather than appearance.",data={"assessment_mode":"scored_multiple_choice","pass_mark":.8,"questions":[
            {"question":"Which evidence proves 5, 9, 13, 17, … is arithmetic?","options":["It increases","Its terms are positive","Its first differences are all 4","It has four shown terms"],"correct_index":2,"explanation":"A constant first difference is the arithmetic test."},
            {"question":"Which calculation tests whether 3, 6, 12, 24, … is geometric?","options":["6−3","6÷3","6+3","6×3"],"correct_index":1,"explanation":"A geometric sequence is tested using consecutive non-zero ratios."},
            {"question":"Why is 2, 6, 12, 20, … quadratic?","options":["It increases","Its first differences are constant","Its second differences are constant","Every term is even"],"correct_index":2,"explanation":"The first differences 4, 6, 8 have constant second differences 2, 2."},
        ]}),
        LessonBlock(type="summary",title="Key takeaway",content="Arithmetic means constant first difference; geometric means constant non-zero ratio; quadratic means constant second difference. Test before choosing a formula."),
    ])

SEQUENCES_SERIES = [LESSON_ONE] + [lesson_pack_shell(*metadata) for metadata in LESSON_PACK_METADATA[1:]]
