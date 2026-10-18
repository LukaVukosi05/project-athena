"""Deterministic runtime factories for approved Sequences and Series Lessons 2–18."""
from dataclasses import dataclass
from fractions import Fraction
from math import isclose
import re

from app.curriculum.schemas import AccessLevel, ContentStatus, Lesson, LessonBlock, MathematicalOperation, SemanticObject, StepExplanation, TeachingStep, TimelineEvent, VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion


@dataclass(frozen=True)
class Example:
    prompt: str
    method: str
    working: tuple[str, ...]
    answer: str
    verification: str
    misconception: str


def fmt(value):
    value=Fraction(value)
    return str(value.numerator) if value.denominator==1 else f"{value.numerator}/{value.denominator}"


def arithmetic_term_examples():
    configs=[(7,4,25),(3,7,10),(14,-5,12),(5,4,30),(12,-3,40),(-5,4,20),(100,-8,15),(0,7,50),(21,-5,30),(4,0,100),(2,6,34),(11,7,50)]
    return [Example(f"For an arithmetic sequence with a={a} and d={d}, find T_{n}.","Use T_n=a+(n−1)d.",(f"T_{n}={a}+({n}−1)({d})",f"T_{n}={a+(n-1)*d}"),str(a+(n-1)*d),f"T_1={a}; one adds {d} exactly {n-1} times.","using-n-instead-of-n-minus-one") for a,d,n in configs]


def arithmetic_parameter_examples():
    configs=[(5,18,12,46,30),(4,17,10,47,20),(8,-6,20,-42,25),(2,9,7,34,15),(6,23,15,59,12),(3,-4,9,20,18),(10,100,25,250,40),(5,0,12,21,30),(7,50,19,-10,25),(12,7,30,61,50),(9,-12,17,28,22),(20,3,35,48,60)]
    result=[]
    for p,tp,q,tq,n in configs:
        d=Fraction(tq-tp,q-p);a=Fraction(tp)-(p-1)*d;answer=a+(n-1)*d
        result.append(Example(f"Given T_{p}={tp} and T_{q}={tq} in an arithmetic sequence, find T_{n}.","Write two equations in a and d, then subtract.",(f"a+{p-1}d={tp}; a+{q-1}d={tq}",f"d={fmt(d)}; a={fmt(a)}",f"T_{n}={fmt(a)}+{n-1}({fmt(d)})={fmt(answer)}"),fmt(answer),f"Substitution gives T_{p}={tp} and T_{q}={tq}.","term-number-coefficient") )
    return result


def arithmetic_context_examples():
    configs=[("seats in row",18,3,25,"90 seats"),("training distance",3,Fraction(2,5),15,"8.6 km"),("tank volume",500,-12,18,"296 L"),("phone value",8000,-150,18,"R5 450"),("weekly saving",200,80,12,"R1 080"),("stack width",45,-2,16,"15 cm"),("temperature reading",24,-3,9,"0 °C"),("tile count",12,5,20,"107 tiles"),("page target",30,4,14,"82 pages"),("row length",6,Fraction(3,2),11,"21 m"),("membership",150,25,13,"450 members"),("machine output",900,-35,21,"200 units")]
    result=[]
    for label,a,d,n,answer_label in configs:
        exact=Fraction(a)+(n-1)*Fraction(d)
        result.append(Example(f"A {label} follows an arithmetic pattern with first value {a} and change {fmt(d)} per interval. Find value {n}.","Define interval 1, then use T_n=a+(n−1)d.",(f"T_{n}={a}+({n}−1)({fmt(d)})",f"T_{n}={fmt(exact)}"),fmt(exact),f"The value changes by {fmt(d)} for each of the {n-1} intervals.","context-indexing"))
    return result


def geometric_term_examples():
    configs=[(3,-2,9),(625,Fraction(1,5),6),(2,3,8),(-4,-2,7),(160,Fraction(1,2),10),(5,2,12),(81,Fraction(1,3),7),(7,-1,20),(Fraction(1,2),2,9),(100,Fraction(9,10),6),(6,-3,6),(1024,Fraction(1,2),11)]
    result=[]
    for a,r,n in configs:
        answer=Fraction(a)*Fraction(r)**(n-1)
        result.append(Example(f"For a geometric sequence with a={fmt(a)} and r={fmt(r)}, find T_{n}.","Use T_n=ar^(n−1).",(f"T_{n}={fmt(a)}({fmt(r)})^({n}−1)",f"T_{n}={fmt(answer)}"),fmt(answer),f"The exponent {n-1} counts multiplications from term 1.","geometric-exponent"))
    return result


def geometric_parameter_examples():
    configs=[(500,Fraction(28,25),8),(1000,Fraction(9,10),6),(5,2,10),(80,Fraction(3,2),5),(240,Fraction(3,4),7),(12,-2,6),(64,Fraction(1,2),9),(300,Fraction(21,20),12),(20,3,7),(729,Fraction(1,3),8),(4,-3,5),(200,Fraction(17,20),10)]
    result=[]
    for a,r,periods in configs:
        answer=Fraction(a)*Fraction(r)**periods
        result.append(Example(f"A quantity starts at {fmt(a)} and is multiplied by {fmt(r)} for {periods} completed periods. Find the new amount.","Repeated percentage or ratio change is geometric.",(f"A={fmt(a)}({fmt(r)})^{periods}",f"A={fmt(answer)}"),fmt(answer),f"Dividing the result by {fmt(r)} reverses the final period.","percentage-multiplier"))
    return result


def quadratic_examples():
    configs=[(1,2,0,20),(2,1,-1,20),(1,3,-2,15),(2,-1,3,12),(3,0,-2,10),(1,-4,8,16),(2,3,1,18),(3,-2,4,14),(1,5,5,25),(2,-5,7,11),(4,1,-3,9),(1,-1,1,30)]
    result=[]
    for a,b,c,n in configs:
        terms=[a*k*k+b*k+c for k in range(1,5)];answer=a*n*n+b*n+c
        result.append(Example(f"Find T_{n} for the quadratic pattern {', '.join(map(str,terms))}, …","Use constant second difference 2a, then determine b and c.",(f"First differences: {terms[1]-terms[0]}, {terms[2]-terms[1]}, {terms[3]-terms[2]}",f"Second differences: {2*a}, {2*a}; therefore a={a}",f"T_n={a}n²+{b}n+{c}; T_{n}={answer}"),str(answer),f"Substituting n=1,2,3,4 reproduces {terms}.","quadratic-coefficients"))
    return result


def sigma_examples():
    configs=[(1,6,3,-2),(2,5,1,0),(1,5,0,2),(1,4,2,1),(3,7,2,-1),(1,8,4,0),(2,6,3,1),(1,10,1,-1),(4,9,2,3),(1,7,5,-4),(3,8,1,2),(1,12,2,0)]
    result=[]
    for start,end,m,c in configs:
        terms=[m*k+c for k in range(start,end+1)];answer=sum(terms)
        result.append(Example(f"Evaluate Σ from k={start} to {end} of ({m}k{c:+d}).","Substitute every integer index from the lower to upper limit.",(f"Terms: {' + '.join(map(str,terms))}",f"Sum={answer}"),str(answer),f"There are {end-start+1} terms and their direct total is {answer}.","sigma-limits"))
    return result


def arithmetic_sum_examples():
    configs=[(7,4,40),(5,3,33),(12,3,25),(100,-5,20),(3,4,16),(8,6,18),(50,-2,22),(1,1,100),(20,5,15),(-10,4,30),(6,-3,12),(14,7,25)]
    result=[]
    for a,d,n in configs:
        last=a+(n-1)*d;answer=Fraction(n,2)*(a+last)
        result.append(Example(f"Find S_{n} for the arithmetic series with a={a} and d={d}.","Find the last term, then pair first and last terms.",(f"T_{n}={a}+({n}−1)({d})={last}",f"S_{n}={n}/2({a}+{last})={fmt(answer)}"),fmt(answer),f"The average term is {fmt(Fraction(a+last,2))}; multiplying by {n} gives {fmt(answer)}.","term-versus-sum"))
    return result


def arithmetic_sum_context_examples():
    configs=[("theatre seats",24,2,20),("training kilometres",2,Fraction(1,2),14),("stacked cans",30,-1,16),("monthly deposits",300,40,10),("auditorium rows",18,3,25),("daily pages",12,2,21),("production units",100,15,12),("shrinking rows",80,-4,15),("weekly distance",5,1,20),("saving contributions",150,25,18),("tile bands",10,6,14),("garden plants",45,-2,19)]
    result=[]
    for label,a,d,n in configs:
        last=Fraction(a)+(n-1)*Fraction(d);answer=Fraction(n,2)*(Fraction(a)+last)
        result.append(Example(f"A {label} total has {n} arithmetic contributions, starting at {a} and changing by {fmt(d)}. Find the total.","The question asks for a cumulative total, so use an arithmetic series.",(f"T_{n}={fmt(last)}",f"S_{n}={n}/2({a}+{fmt(last)})={fmt(answer)}"),fmt(answer),f"Adding {n} contributions with average {fmt((Fraction(a)+last)/2)} gives {fmt(answer)}.","context-term-or-total"))
    return result


def geometric_sum_examples():
    configs=[(3,2,10),(160,Fraction(1,2),8),(5,3,7),(96,Fraction(1,2),6),(2,4,6),(81,Fraction(1,3),5),(7,-2,6),(10,Fraction(3,2),5),(1,2,12),(64,Fraction(-1,2),7),(6,3,8),(100,Fraction(4,5),10)]
    result=[]
    for a,r,n in configs:
        answer=Fraction(a)*((Fraction(r)**n)-1)/(Fraction(r)-1) if r!=1 else Fraction(a)*n
        result.append(Example(f"Find S_{n} for the geometric series with a={fmt(a)} and r={fmt(r)}.","Use the finite geometric sum after identifying a, r and n.",(f"S_{n}={fmt(a)}[({fmt(r)})^{n}−1]/({fmt(r)}−1)",f"S_{n}={fmt(answer)}"),fmt(answer),f"Direct expansion of the {n} terms has the same total.","geometric-sum-sign"))
    return result


def finite_geometric_context_examples():
    configs=[("prize payments",1000,2,8),("fractal lengths",81,Fraction(1,3),4),("sharing rounds",2,3,7),("bounce heights",10,Fraction(3,5),6),("staged savings",200,Fraction(3,2),5),("shrinking strips",128,Fraction(1,2),8),("cell groups",4,2,10),("discounted payments",500,Fraction(9,10),12),("branch lengths",243,Fraction(1,3),6),("reward rounds",50,2,9),("echo strengths",100,Fraction(2,5),7),("alternating adjustments",64,Fraction(-1,2),6)]
    result=[]
    for label,a,r,n in configs:
        answer=Fraction(a)*((Fraction(r)**n)-1)/(Fraction(r)-1)
        result.append(Example(f"A {label} model has {n} contributions, first {fmt(a)}, ratio {fmt(r)}. Find the finite total.","Count the contributions and use the finite geometric-series formula.",(f"S_{n}={fmt(a)}[({fmt(r)})^{n}−1]/({fmt(r)}−1)",f"S_{n}={fmt(answer)}"),fmt(answer),f"The direct {n}-term expansion agrees with {fmt(answer)}.","context-first-term"))
    return result


def infinite_examples():
    configs=[(12,Fraction(1,2)),(5,-2),(9,Fraction(1,3)),(4,Fraction(-1,2)),(20,Fraction(3,4)),(7,Fraction(-2,3)),(3,1),(10,Fraction(6,5)),(1,Fraction(1,10)),(16,Fraction(-1,4)),(6,Fraction(5,6)),(8,-1)]
    result=[]
    for a,r in configs:
        converges=abs(r)<1
        answer=fmt(Fraction(a)/(1-Fraction(r))) if converges else "diverges"
        result.append(Example(f"Determine convergence and, if possible, find S∞ for a={a}, r={fmt(r)}.","Check |r|<1 before using an infinite-sum formula.",(f"|r|={fmt(abs(Fraction(r)))}",f"S∞={a}/(1−{fmt(r)})={answer}" if converges else "|r|≥1, so no finite sum exists"),answer,f"The terms {'approach zero' if converges else 'do not approach zero sufficiently'}, confirming the decision.","convergence-condition"))
    return result


def infinite_application_examples():
    configs=[("recurring decimal 0.363636…",Fraction(36,100),Fraction(1,100)),("ball rebound after a 10 m drop",6,Fraction(3,5)),("recurring decimal 0.777…",Fraction(7,10),Fraction(1,10)),("retained amount",100,Fraction(17,20)),("echo distance",20,Fraction(1,2)),("recurring decimal 0.121212…",Fraction(12,100),Fraction(1,100)),("shrinking area",64,Fraction(1,4)),("rebound height",8,Fraction(3,4)),("recurring decimal 0.454545…",Fraction(45,100),Fraction(1,100)),("repeated dose",5,Fraction(4,5)),("nested length",12,Fraction(2,3)),("recurring decimal 0.090909…",Fraction(9,100),Fraction(1,100))]
    result=[]
    for label,a,r in configs:
        answer=Fraction(a)/(1-Fraction(r))
        result.append(Example(f"Model {label} as an infinite geometric series with first repeated contribution {fmt(a)} and ratio {fmt(r)}. Find its limit.","Confirm |r|<1, then use S∞=a/(1−r).",(f"|{fmt(r)}|<1",f"S∞={fmt(a)}/(1−{fmt(r)})={fmt(answer)}"),fmt(answer),"Partial sums approach the stated limit because the remaining tail tends to zero.","physical-versus-mathematical-infinity"))
    return result


def mixed_examples():
    sources=[arithmetic_term_examples(),geometric_term_examples(),arithmetic_sum_examples(),geometric_sum_examples(),infinite_examples()]
    result=[]
    for index in range(12):
        base=sources[index%len(sources)][index]
        result.append(Example("Choose the correct sequence or series model, then solve: "+base.prompt, "Decision first: term or total; additive or multiplicative; finite or infinite. "+base.method,base.working,base.answer,base.verification,"formula-selection"))
    return result


def error_examples():
    errors=[("For 3,12,48,… use r=12−3.","r=12÷3=4","A ratio uses division, not subtraction."),("For S_8 use the last power r^7 in the sum formula.","Use r^8 in S_8","The finite-sum formula contains r^n."),("Since r=−0.5, the infinite series diverges.","It converges because |−0.5|<1","Convergence uses the absolute value."),("T_n=a+nd.","T_n=a+(n−1)d","There are n−1 jumps from term 1."),("0.777…=7/10.","0.777…=(7/10)/(1−1/10)=7/9","A recurring decimal is an infinite sum."),("Every increasing pattern is arithmetic.","Test first differences","Direction is not classification evidence."),("S_n finds one term.","T_n finds one term; S_n finds a total","Term and sum notation have different roles."),("A non-integer term position is valid.","A term position must be a positive integer","Sequence positions are discrete."),("Use S∞ without checking r.","Check |r|<1 first","The infinite formula has a convergence condition."),("Second difference equals a.","Second difference equals 2a","For an²+bn+c, the second difference is 2a."),("Σ from 2 to 5 has five terms.","It has 5−2+1=4 terms","Both limits are inclusive."),("Move a term and change its sign.","Apply the same inverse operation to both sides","Equivalent equations require balanced operations.")]
    return [Example(f"Find and repair the first error: {wrong}","Identify the first violated mathematical condition.",(f"Incorrect: {wrong}",f"Correction: {repair}"),repair,why,"error-diagnosis") for wrong,repair,why in errors]


GENERATORS={2:arithmetic_term_examples,3:arithmetic_parameter_examples,4:arithmetic_context_examples,5:geometric_term_examples,6:geometric_parameter_examples,7:quadratic_examples,8:sigma_examples,9:arithmetic_sum_examples,10:arithmetic_sum_context_examples,11:geometric_sum_examples,12:finite_geometric_context_examples,13:infinite_examples,14:infinite_application_examples,15:mixed_examples,16:mixed_examples,17:error_examples,18:mixed_examples}

SEQUENCE_TEMPLATES={
    2:"term_rows",3:"term_rows",4:"term_rows",5:"term_rows",6:"term_rows",
    7:"difference_table",8:"sigma_expansion",9:"partial_sum",10:"partial_sum",
    11:"partial_sum",12:"partial_sum",13:"convergence_diagram",14:"convergence_diagram",
    15:"formula_decision",16:"formula_decision",17:"error_diagnosis",18:"formula_decision",
}

def _number(token:str)->Fraction:
    return Fraction(token.replace("−","-").replace("âˆ’","-"))

def _question_terms(lesson_number:int,spec:Example)->list[Fraction]:
    prompt=spec.prompt.replace("âˆ’","-")
    if lesson_number==3:
        known=[(int(position),_number(value)) for position,value in re.findall(r"T_(\d+)=(-?\d+(?:/\d+)?)",prompt)]
        target=re.search(r"find T_(\d+)",prompt,re.I)
        if known and target:return [value for _,value in known]+[_number(spec.answer)]
    if lesson_number==7:
        match=re.search(r"pattern\s+(.+?),\s*(?:â€¦|\.\.\.)",spec.prompt)
        if match:return [_number(value) for value in re.findall(r"-?\d+(?:/\d+)?",match.group(1))]
    if lesson_number==8:
        return [_number(value) for value in re.findall(r"-?\d+(?:/\d+)?",spec.working[0].split(":",1)[-1])]
    a_match=re.search(r"(?:a=|first(?: value| repeated contribution)?\s+)(-?\d+(?:/\d+)?)",prompt,re.I)
    d_match=re.search(r"(?:d=|change(?: by)?\s+)(-?\d+(?:/\d+)?)",prompt,re.I)
    r_match=re.search(r"(?:r=|ratio\s+|multiplied by\s+)(-?\d+(?:/\d+)?)",prompt,re.I)
    if not a_match and "starts at" in prompt.lower():a_match=re.search(r"starts at\s+(-?\d+(?:/\d+)?)",prompt,re.I)
    if a_match and (d_match or r_match):
        a=_number(a_match.group(1));change=_number((d_match or r_match).group(1));geometric=bool(r_match)
        return [a*(change**index) if geometric else a+index*change for index in range(6)]
    values=[_number(value) for value in re.findall(r"(?<![A-Za-z_])-?\d+(?:/\d+)?",prompt)]
    return values[:8] if len(values)>=2 else [Fraction(0),Fraction(1)]

def _sequence_visualization(lesson_number:int,spec:Example,object_ids:tuple[str,...])->VisualizationInstruction:
    terms=_question_terms(lesson_number,spec)
    first=[terms[index+1]-terms[index] for index in range(len(terms)-1)]
    second=[first[index+1]-first[index] for index in range(len(first)-1)]
    ratios=[terms[index+1]/terms[index] for index in range(len(terms)-1)] if all(term for term in terms[:-1]) else []
    partial=[];running=Fraction(0)
    for term in terms:running+=term;partial.append(running)
    parameters={
        "title":spec.prompt,"method":spec.method,"working_lines":list(spec.working),"answer":spec.answer,
        "objects":list(object_ids),"positions":list(range(1,len(terms)+1)),"terms":[float(term) for term in terms],
        "differences":[float(value) for value in first],"second_differences":[float(value) for value in second],
        "partial_sums":[float(value) for value in partial],
    }
    if ratios:parameters["ratios"]=[float(value) for value in ratios]
    return VisualizationInstruction(type="sequences",template=SEQUENCE_TEMPLATES[lesson_number],parameters=parameters)


def legacy_board_for(lesson_number:int,order:int,spec:Example)->WhiteboardBlock:
    method=f"Method: {spec.method}";worked="; ".join(spec.working);result=f"∴ {spec.answer}";verified=f"{spec.verification} ✓"
    explain=lambda what,why,purpose,remember:StepExplanation(what=what,why=why,purpose=purpose,remember=remember)
    steps=[
        TeachingStep(step_number=0,title="Orient",before_expression=spec.prompt,working_expression=spec.prompt,operation=MathematicalOperation(type="read_problem"),after_expression=spec.prompt,explanation=explain("Read the complete problem.","The givens determine the model.","Identify what must be found.","Choose a formula only after identifying the structure."),animation_template="problem_annotation",screen_reader_description=spec.prompt),
        TeachingStep(step_number=1,title="Select the method",before_expression=spec.prompt,working_expression=method,operation=MathematicalOperation(type="select_method"),after_expression=method,explanation=explain("Select the relevant sequence or series structure.",spec.method,"Connect the given information to a valid method.",spec.misconception),animation_template="method_selection",screen_reader_description=method),
        TeachingStep(step_number=2,title="Apply the method",before_expression=method,working_expression=worked,operation=MathematicalOperation(type="show_working"),after_expression=result,explanation=explain("Substitute and simplify one line at a time.","Each line follows from the selected formula.","Keep the calculation traceable.","Retain exact values until the final answer."),animation_template="progressive_working",screen_reader_description=worked),
        TeachingStep(step_number=3,title="Verify and conclude",before_expression=result,working_expression=spec.verification,operation=MathematicalOperation(type="verify_result"),after_expression=verified,explanation=explain("Check the result against the original information.",spec.verification,"Confirm the answer is valid in context.",spec.misconception),animation_template="result_verification",screen_reader_description=verified),
    ]
    return WhiteboardBlock(id=f"g12-seq-l{lesson_number:02}-board-{order:02}",representation="symbolic",problem=spec.prompt,initial_expression=spec.prompt,steps=steps)


def board_for(lesson_number:int,order:int,spec:Example)->WhiteboardBlock:
    """Build a question-first semantic timeline from the authored working lines."""
    explain=lambda title,caption:StepExplanation(what=title,why=caption,purpose="Keep the operation visible before its result.",remember=spec.misconception)
    object_ids=("left-side","equals","right-side","operation","result","verification")
    objects=[SemanticObject(id=name,type="token",value=name.replace("-"," ")) for name in object_ids]
    steps=[]
    def add(title,before,working,after,operation,caption,event_type,targets):
        index=len(steps)
        events=[TimelineEvent(at_ms=0,type="narration",text=caption),TimelineEvent(at_ms=0,type="caption",text=caption),TimelineEvent(at_ms=180,type="focus",targets=targets),TimelineEvent(at_ms=420,type=event_type,targets=targets)]
        steps.append(TeachingStep(id=f"step-{index}",step_number=index,title=title,before_expression=before,working_expression=working,operation=MathematicalOperation(type=operation),after_expression=after,explanation=explain(title,caption),animation_template="semantic_timeline",screen_reader_description=caption,visualization_state=VisualizationState(objects=list(object_ids),annotations=[f"lesson:{lesson_number}",f"visual-stage:{index}"]),instructional_goal=title,duration_ms=900,events=events,narration=caption,state_after={"expression":after}))
    add("Choose the model",spec.prompt,f"Inspect the evidence: {spec.method}",spec.method,"timeline_select","Select the operation that matches the evidence in the question.","show_operation",["operation"])
    previous=spec.method
    for line in spec.working:
        event="calculate_ratio" if "ratio" in spec.method.lower() or "geometric" in spec.method.lower() else "calculate_difference" if "difference" in line.lower() else "write"
        add("Apply one mathematical step",previous,f"{previous}  ->  {line}",line,"timeline_inspect","Carry out this calculation before using its result in the next line.",event,["left-side","right-side"] if "=" in line else ["operation"])
        previous=line
    result=f"Therefore {spec.answer}"
    add("State the result",previous,f"Therefore: {spec.answer}",result,"timeline_summarize","State the answer only after the calculation has established it.","reveal",["result"])
    verified=f"{spec.verification} ✓"
    add("Verify",result,f"Check: {spec.verification}",verified,"timeline_verify",spec.verification,"verify",["verification"])
    return WhiteboardBlock(
        id=f"g12-seq-l{lesson_number:02}-board-{order:02}", representation="visual",
        problem=spec.prompt, initial_expression=spec.prompt, steps=steps,
        semantic_objects=objects,
        visualization=_sequence_visualization(lesson_number,spec,object_ids),
    )


def build_questions(lesson_number:int)->list[WhiteboardQuestion]:
    examples=GENERATORS[lesson_number]()
    assert len(examples)==12
    levels=["foundation","foundation","easy","easy","standard","standard","standard","intermediate","intermediate","exam","advanced","expert"]
    return [WhiteboardQuestion(id=f"g12-seq-l{lesson_number:02}-wbq-{i:02}",order=i,difficulty=levels[i-1],estimated_minutes=5,is_core_example=i==1,guidance_level="high" if i<=3 else "moderate" if i<=7 else "reduced" if i<=10 else "minimal",whiteboard=board_for(lesson_number,i,spec),cognitive_level="routine" if i<=6 else "complex" if i<=10 else "problem_solving",marks=2 if i<=6 else 4,answer=spec.answer,full_memo=[*spec.working,spec.verification],misconception_tags=[spec.misconception]) for i,spec in enumerate(examples,1)]


def build_lesson(metadata:tuple)->Lesson:
    number,title,objective,teaching=metadata;questions=build_questions(number)
    return Lesson(id=f"g12-sequences-series-{number:02}",order=number,title=title,objective=objective,why_it_matters="This lesson is part of the approved CAPS Paper 1 Sequences and Series learning path.",intuition=teaching,prerequisites=[f"g12-sequences-series-{number-1:02}"],estimated_minutes=55,difficulty="standard" if number<15 else "exam",access_level=AccessLevel.PREMIUM,status=ContentStatus.DRAFT,mastery_threshold=.8,whiteboard_questions=questions,blocks=[LessonBlock(type="concept",title="Teach the idea",content=teaching),questions[0].whiteboard,LessonBlock(type="mistake",title="Misconception diagnosis and repair",content=f"Watch for: {questions[-1].misconception_tags[0].replace('-', ' ')}."),LessonBlock(type="practice",title="Self-guided practice",content="Solve, submit, then compare your method.",data={"practice_bank_id":f"g12-sequences-series-{number:02}"}),LessonBlock(type="summary",title="Key takeaway",content=objective)])
