"""Curated graph-first reinforcement sets for calculus foundations."""
from app.curriculum.schemas import MathematicalOperation, StepExplanation, TeachingStep, WhiteboardBlock, WhiteboardQuestion
from app.services.graphing import function_graph

def e(what, why, purpose, remember):
    return StepExplanation(what=what, why=why, purpose=purpose, remember=remember)

RATE_SPECS = [
 ("f(x)=x²",1,3,1,9,"4",[-2,-1,0,1,2,3,4],[4,1,0,1,4,9,16]),
 ("f(x)=2x+1",0,4,1,9,"2",[-1,0,1,2,3,4,5],[-1,1,3,5,7,9,11]),
 ("f(x)=x²-3x",1,4,-2,4,"2",[-1,0,1,2,3,4,5],[4,0,-2,-2,0,4,10]),
 ("g(x)=2x²+5",-1,3,7,23,"4",[-2,-1,0,1,2,3,4],[13,7,5,7,13,23,37]),
 ("s(t)=3t²+2",1,4,5,50,"15",[0,1,2,3,4,5],[2,5,14,29,50,77]),
 ("h(x)=x²+2x",-2,2,0,8,"2",[-3,-2,-1,0,1,2,3],[3,0,-1,0,3,8,15]),
 ("p(t)=t³",1,3,1,27,"13",[0,1,2,3,4],[0,1,8,27,64]),
 ("q(x)=-x²+6x",1,5,5,5,"0",[0,1,2,3,4,5,6],[0,5,8,9,8,5,0]),
]

def rate_board(index, spec):
    formula,a,b,fa,fb,rate,xs,ys=spec; initial=f"{formula}; x₁={a}; x₂={b}"
    formula_line=f"average rate = [f({b}) - f({a})] / ({b} - {a})"
    working=f"({fb} - {fa}) / ({b} - {a}) = {rate}"
    return WhiteboardBlock(id=f"average-rate-{index:02}",problem=f"Find the average rate of change of {formula} from {a} to {b}.",initial_expression=initial,
      graph_spec=function_graph(xs,ys,title=formula,points=[(a,fa,"start"),(b,fb,"end")]),steps=[
       TeachingStep(step_number=0,title="Mark the interval",before_expression=initial,working_expression=initial,operation=MathematicalOperation(type="read_problem"),after_expression=initial,explanation=e("Locate both endpoints on the graph.","Average rate uses two distinct points.","The endpoints define the secant line.","Read x-values and matching y-values together."),animation_template="problem_annotation",screen_reader_description=f"The interval is from {a} to {b}."),
       TeachingStep(step_number=1,title="Write the rate formula",before_expression=initial,working_expression=formula_line,operation=MathematicalOperation(type="select_method"),after_expression=formula_line,explanation=e("Use change in output over change in input.","This is the gradient between the two graph points.","It connects the algebra to the secant line.","Keep subtraction order consistent."),animation_template="method_selection",screen_reader_description=formula_line),
       TeachingStep(step_number=2,title="Substitute and simplify",before_expression=formula_line,working_expression=working,operation=MathematicalOperation(type="show_working"),after_expression=f"{working}; ∴ {rate}",explanation=e("Substitute both function values.","The quotient measures vertical change per horizontal unit.","This calculates the secant gradient.","Do not omit the denominator."),animation_template="progressive_working",screen_reader_description=f"The average rate is {rate}."),
       TeachingStep(step_number=3,title="Read the graph",before_expression=f"{working}; ∴ {rate}",working_expression=f"secant gradient = {rate}",operation=MathematicalOperation(type="verify_result"),after_expression=f"secant gradient = {rate} ✓",explanation=e("Compare the sign and steepness with the graph.","The visual direction should agree with the calculated gradient.","This checks the result geometrically.","Horizontal endpoints can produce an average rate of zero."),animation_template="result_verification",screen_reader_description=f"The graph confirms a secant gradient of {rate}.")])

TANGENT_SPECS=[("x²",0,"0"),("x²",1,"2"),("x²",2,"4"),("x²",3,"6"),("x²",-1,"-2"),("2x²",1,"4"),("x³",1,"3"),("x³",2,"12")]
def tangent_board(index,spec):
    formula,a,gradient=spec; ys=([4,1,0,1,4,9,16] if formula=="x²" else [8,2,0,2,8,18,32]) if "²" in formula else [-8,-1,0,1,8,27,64]; xs=[-2,-1,0,1,2,3,4]; y=(a*a if formula=="x²" else 2*a*a if formula=="2x²" else a**3); initial=f"f(x)={formula}; P({a},{y})"
    secant=f"m_secant = [f({a}+h)-f({a})] / h, h≠0"
    approach=f"as h→0, m_secant→{gradient}"
    return WhiteboardBlock(id=f"tangent-{index:02}",problem=f"Use secants to find the tangent gradient of f(x)={formula} at x={a}.",initial_expression=initial,graph_spec=function_graph(xs,ys,title=f"f(x) = {formula}",points=[(a,y,"P")]),steps=[
      TeachingStep(step_number=0,title="Draw a secant",before_expression=initial,working_expression=initial,operation=MathematicalOperation(type="draw_secant"),after_expression=initial,explanation=e("Join P to a nearby point Q.","Two points give an average gradient.","The secant provides gradients near P.","Q remains distinct while h is non-zero."),animation_template="secant_line",screen_reader_description="A secant is drawn through P and Q."),
      TeachingStep(step_number=1,title="Form the secant gradient",before_expression=initial,working_expression=secant,operation=MathematicalOperation(type="calculate_secant_gradient",value="h"),after_expression=secant,explanation=e("Calculate change in y over change in x.","This gives the nearby average gradient.","Its simplified form reveals the limit.","Cancel h before taking the limit."),animation_template="secant_gradient",screen_reader_description=secant),
      TeachingStep(step_number=2,title="Move Q towards P",before_expression=secant,working_expression=approach,operation=MathematicalOperation(type="approach_limit",value="h→0"),after_expression=approach,explanation=e("Let h approach zero.","The secant turns toward the tangent.","Its gradient approaches the instantaneous gradient.","Approaching zero is not dividing by zero."),animation_template="secant_approaches_tangent",screen_reader_description=approach),
      TeachingStep(step_number=3,title="State the tangent gradient",before_expression=approach,working_expression=f"f′({a})={gradient}",operation=MathematicalOperation(type="draw_tangent",value=gradient),after_expression=f"f′({a})={gradient}",explanation=e("Draw the limiting tangent.","Its gradient is the derivative at P.","This connects the graph to derivative notation.","f′(a) is a gradient, not a coordinate."),animation_template="tangent_at_point",screen_reader_description=f"The tangent gradient is {gradient}.")])

def rate_questions(): return [WhiteboardQuestion(id=b.id,order=i,difficulty=("foundation" if i<3 else "standard" if i<6 else "exam"),is_core_example=i==1,guidance_level=("high" if i<4 else "moderate" if i<7 else "reduced"),whiteboard=b) for i,b in enumerate((rate_board(n,s) for n,s in enumerate(RATE_SPECS,1)),1)]
def tangent_questions(): return [WhiteboardQuestion(id=b.id,order=i,difficulty=("foundation" if i<3 else "standard" if i<6 else "exam"),is_core_example=i==1,guidance_level=("high" if i<4 else "moderate" if i<7 else "reduced"),whiteboard=b) for i,b in enumerate((tangent_board(n,s) for n,s in enumerate(TANGENT_SPECS,1)),1)]
