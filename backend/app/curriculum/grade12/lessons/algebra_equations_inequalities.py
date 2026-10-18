"""Approved Topic 5 runtime, generated from the canonical pack data."""
from __future__ import annotations
import json, re
from pathlib import Path

from app.curriculum.schemas import (
 AccessLevel, ContentStatus, FormulaUnderstanding, Lesson, LessonBlock,
 MathematicalOperation, SemanticObject, StepExplanation, TeachingStep,
 TimelineEvent, VisualizationInstruction, VisualizationState, WhiteboardBlock,
 WhiteboardQuestion,
)

SOURCE="Project_Athena_Grade12_Topic5_Algebra_Equations_and_Inequalities_Approved_Lesson_Pack.docx"
DATA=json.loads((Path(__file__).with_name("algebra_pack_data.json")).read_text(encoding="utf-8"))["lessons"]
MODES=("balance","factorisation","zero_product","quadratic_formula","method_selection","surd","quadratic_form","exponential","linear_simultaneous","nonlinear_simultaneous","inequality","discriminant","parameter_roots","rational_restrictions","proof","modelling","integrated","mastery")

def explanation(title,why):
 return StepExplanation(what=title,why=why,purpose="Make the mathematical cause visible before the changed expression.",remember="A valid algebraic method preserves the intended solution set and ends with verification.")

def formula_understanding(item,mode):
 return FormulaUnderstanding(
  meaning=item["objective"],origin=item["teaching"],formula=item["anchor"],
  symbol_anatomy=["target: the object or condition to find","given terms: the current equation or inequality","operation: the legal transformation","candidate: a possible solution","restriction: a value excluded by the original form","verification: evidence in the original task"],
  why_it_works=item["teaching"],validity_conditions=["Use the method only after identifying its structure","Apply equivalence-preserving operations to complete sides or expressions","Retain domain restrictions and check candidates"],
  selection_reason=f"The {mode.replace('_',' ')} structure matches the authored task.",
  wrong_use_cases=["Do not transpose without showing the same inverse operation on both sides","Do not cancel terms across addition or subtraction","Do not accept candidates without the required original-equation, interval or restriction check"],
  visual_model={"focus":"addressable algebra tokens","operation":"cause shown before result","validity":"restriction, branch or interval evidence","check":"original task verification"},
  verification={"equation":"substitute every candidate","inequality":"test a value in each interval","restriction":"compare against excluded values","formula":"check discriminant, roots and rounding"})

def special_event(number):
 return {2:"factor",3:"branch_zero_product",4:"highlight_discriminant",6:"mark_restriction",7:"back_substitute",9:"back_substitute",10:"back_substitute",11:"draw_number_line",12:"highlight_discriminant",13:"highlight_discriminant",14:"mark_restriction"}.get(number,"write")

def balance_prototype(item, spec, order):
 prompt=spec["prompt"]
 objects=[SemanticObject(id=name,type="token",value=name.replace("-"," ")) for name in (
  "variable-term","constant-term","left-side","right-side","subtract-left","subtract-right",
  "cancel-pair","coefficient","divide-left","divide-right","answer","verification",
 )]
 rows=[
  ("Identify the goal","balance_focus_goal","equation_focus","3x + 7 = 22","3x + 7 = 22",None,[TimelineEvent(at_ms=0,type="caption",text="We need to isolate x while keeping both sides equal."),TimelineEvent(at_ms=250,type="focus",targets=["variable-term"])]),
  ("Identify the first obstacle","balance_focus_constant","equation_focus","3x + 7 = 22","3x + 7 = 22",None,[TimelineEvent(at_ms=0,type="caption",text="Seven is being added to 3x. We undo this by subtracting 7."),TimelineEvent(at_ms=250,type="dim",targets=["variable-term","right-side"]),TimelineEvent(at_ms=350,type="focus",targets=["constant-term"])]),
  ("Subtract 7 from both sides","apply_both_sides_display","equation_balance_display","3x + 7 = 22","3x + 7 - 7 = 22 - 7",None,[TimelineEvent(at_ms=0,type="caption",text="We subtract 7 from both sides so that the equation remains balanced."),TimelineEvent(at_ms=250,type="apply_both_sides",targets=["subtract-left","subtract-right"],label="-7")]),
  ("Simplify the balanced equation","simplify_equation","equation_simplification","3x + 7 - 7 = 22 - 7","3x = 15",None,[TimelineEvent(at_ms=0,type="caption",text="Positive 7 and negative 7 cancel. Twenty-two minus 7 is 15."),TimelineEvent(at_ms=150,type="apply_both_sides",targets=["subtract-left","subtract-right"],label="-7 is already on both sides"),TimelineEvent(at_ms=300,type="cancel",targets=["subtract-left","subtract-right"]),TimelineEvent(at_ms=500,type="simplify",targets=["cancel-pair"])]),
  ("Divide both sides by 3","divide_both_sides_display","equation_division_display","3x = 15","3x / 3 = 15 / 3",None,[TimelineEvent(at_ms=0,type="caption",text="We divide both sides by 3 because x is multiplied by 3."),TimelineEvent(at_ms=200,type="focus",targets=["coefficient"]),TimelineEvent(at_ms=350,type="apply_both_sides",targets=["divide-left","divide-right"],label="divide by 3")]),
  ("Simplify to reveal x","simplify_equation","equation_simplification","3x / 3 = 15 / 3","x = 5",None,[TimelineEvent(at_ms=0,type="caption",text="Both sides simplify, giving x equals 5."),TimelineEvent(at_ms=300,type="simplify",targets=["answer"])]),
  ("Substitute into the original equation","verification_line","equation_verification","x = 5","3(5) + 7 = 22",None,[TimelineEvent(at_ms=0,type="caption",text="Substitute 5 into the original equation to check the answer."),TimelineEvent(at_ms=300,type="substitute",targets=["verification"])]),
  ("Evaluate the left side","verification_line","equation_verification","3(5) + 7 = 22","15 + 7 = 22",None,[TimelineEvent(at_ms=0,type="caption",text="Three times 5 is 15, so we continue simplifying the original left side."),TimelineEvent(at_ms=300,type="simplify",targets=["verification"])]),
  ("Verify equality","verification_line","equation_verification","15 + 7 = 22","22 = 22 \u2713",None,[TimelineEvent(at_ms=0,type="caption",text="Substituting 5 into the original equation makes both sides equal, so the answer is correct."),TimelineEvent(at_ms=300,type="verify",targets=["verification"],style="verification")]),
 ]
 steps=[]
 for index,(title,operation,template,before,after,working,events) in enumerate(rows):
  caption=events[0].text
  steps.append(TeachingStep(id=f"step-{index}",step_number=index,title=title,before_expression=before,working_expression=working or after,operation=MathematicalOperation(type=operation,value=7 if operation=="apply_both_sides_display" else 3 if operation=="divide_both_sides_display" else None),after_expression=after,explanation=explanation(title,caption),common_mistake="Never move a term across the equals sign and change its sign without showing the balancing operation.",animation_template=template,screen_reader_description=caption,visualization_state=VisualizationState(objects=[obj.id for obj in objects],highlights=[],annotations=["semantic-equation",f"visual-stage:{index}"]),instructional_goal=title,duration_ms=900,events=[TimelineEvent(at_ms=0,type="narration",text=caption),*events],narration=caption,state_after={"expression":after}))
 params={"mode":"balance","prompt":prompt,"answer":spec["answer"],"method":"Apply the same inverse operation to both sides."}
 return WhiteboardBlock(id=f"g12-algebra-01-board-{order:02}",representation="visual",problem=prompt,initial_expression="3x + 7 = 22",steps=steps,visualization=VisualizationInstruction(type="algebra",template="algebra_reasoning",parameters=params),semantic_objects=objects,formula_understanding=formula_understanding(item,"balance"))

def balance_second_example(item, spec, order):
 prompt=spec["prompt"]
 objects=[SemanticObject(id=name,type="token",value=name.replace("-"," ")) for name in (
  "variable-term","constant-term","left-side","right-side","add-left","add-right",
  "cancel-pair","coefficient","divide-left","divide-right","answer","verification",
 )]
 rows=[
  ("Identify the goal","balance_focus_goal","equation_focus","5x - 4 = 11","5x - 4 = 11","We need to isolate x while preserving equality.",[TimelineEvent(at_ms=250,type="focus",targets=["variable-term"])]),
  ("Identify the first obstacle","balance_focus_constant","equation_focus","5x - 4 = 11","5x - 4 = 11","Four is subtracted from 5x, so addition by 4 is the inverse operation.",[TimelineEvent(at_ms=250,type="dim",targets=["variable-term","right-side"]),TimelineEvent(at_ms=350,type="focus",targets=["constant-term"])]),
  ("Add 4 to both sides","apply_both_sides_display","equation_balance_display","5x - 4 = 11","5x - 4 + 4 = 11 + 4","We add 4 to both sides so the equation remains balanced.",[TimelineEvent(at_ms=250,type="apply_both_sides",targets=["add-left","add-right"],label="+4")]),
  ("Simplify the balanced equation","simplify_equation","equation_simplification","5x - 4 + 4 = 11 + 4","5x = 15","Negative 4 and positive 4 cancel, while 11 plus 4 is 15.",[TimelineEvent(at_ms=150,type="apply_both_sides",targets=["add-left","add-right"],label="+4 is on both sides"),TimelineEvent(at_ms=300,type="cancel",targets=["add-left","add-right"]),TimelineEvent(at_ms=500,type="simplify",targets=["cancel-pair"])]),
  ("Divide both sides by 5","divide_both_sides_display","equation_division_display","5x = 15","5x / 5 = 15 / 5","We divide both sides by 5 because x is multiplied by 5.",[TimelineEvent(at_ms=200,type="focus",targets=["coefficient"]),TimelineEvent(at_ms=350,type="apply_both_sides",targets=["divide-left","divide-right"],label="divide by 5")]),
  ("Simplify to reveal x","simplify_equation","equation_simplification","5x / 5 = 15 / 5","x = 3","Both sides simplify, giving x equals 3.",[TimelineEvent(at_ms=300,type="simplify",targets=["answer"])]),
  ("Substitute into the original equation","verification_line","equation_verification","x = 3","5(3) - 4 = 11","Substitute 3 into the original equation to check the answer.",[TimelineEvent(at_ms=300,type="substitute",targets=["verification"])]),
  ("Evaluate the left side","verification_line","equation_verification","5(3) - 4 = 11","15 - 4 = 11","Five times 3 is 15, so simplify the original left side.",[TimelineEvent(at_ms=300,type="simplify",targets=["verification"])]),
  ("Verify equality","verification_line","equation_verification","15 - 4 = 11","11 = 11 ✓","Both sides equal 11, so x equals 3 is verified.",[TimelineEvent(at_ms=300,type="verify",targets=["verification"],style="verification")]),
 ]
 steps=[]
 for index,(title,operation,template,before,after,caption,actions) in enumerate(rows):
  events=[TimelineEvent(at_ms=0,type="narration",text=caption),TimelineEvent(at_ms=0,type="caption",text=caption),*actions]
  steps.append(TeachingStep(id=f"step-{index}",step_number=index,title=title,before_expression=before,working_expression=after,operation=MathematicalOperation(type=operation,value=4 if operation=="apply_both_sides_display" else 5 if operation=="divide_both_sides_display" else None),after_expression=after,explanation=explanation(title,caption),common_mistake="Apply the same inverse operation to both complete sides.",animation_template=template,screen_reader_description=caption,visualization_state=VisualizationState(objects=[obj.id for obj in objects],highlights=[],annotations=["semantic-equation",f"visual-stage:{index}"]),instructional_goal=title,duration_ms=900,events=events,narration=caption,state_after={"expression":after}))
 params={"mode":"balance","prompt":prompt,"answer":spec["answer"],"method":"Apply the same inverse operation to both sides."}
 return WhiteboardBlock(id=f"g12-algebra-01-board-{order:02}",representation="visual",problem=prompt,initial_expression="5x - 4 = 11",steps=steps,visualization=VisualizationInstruction(type="algebra",template="algebra_reasoning",parameters=params),semantic_objects=objects,formula_understanding=formula_understanding(item,"balance"))

def balanced_equation_timeline(item, spec, order):
 match=re.search(r"Solve\s+([+-]?\d+)x\s*\+\s*\(([+-]?\d+)\)\s*=\s*([+-]?\d+)",spec["prompt"])
 solution=re.search(r"x\s*=\s*([+-]?\d+(?:\.\d+)?)",spec["answer"])
 if not match or not solution:
  raise ValueError(f"Unsupported balanced-equation authoring input: {spec['id']}")
 coefficient,constant,right=map(int,match.groups()); x_value=float(solution.group(1));x_text=f"{x_value:g}"
 signed_constant=f"+ {constant}" if constant>=0 else f"- {abs(constant)}"
 inverse=-constant; inverse_text=f"+ {inverse}" if inverse>=0 else f"- {abs(inverse)}"
 equation=f"{coefficient}x {signed_constant} = {right}"
 balanced=f"{coefficient}x {signed_constant} {inverse_text} = {right} {inverse_text}"
 simplified_right=right+inverse
 simplified=f"{coefficient}x = {simplified_right}"
 division=f"{coefficient}x / {coefficient} = {simplified_right} / {coefficient}"
 solved=f"x = {x_text}"
 substituted=f"{coefficient}({x_text}) {signed_constant} = {right}"
 multiplied=f"{coefficient*x_value:g} {signed_constant} = {right}"
 verified=f"{right} = {right} ✓"
 operation_id=("add" if inverse>=0 else "subtract")
 objects=[SemanticObject(id=name,type="token",value=name.replace("-"," ")) for name in ("variable-term","constant-term","left-side","right-side",f"{operation_id}-left",f"{operation_id}-right","cancel-pair","coefficient","divide-left","divide-right","answer","verification")]
 captions=[
  "Identify x as the value to isolate while keeping both sides equal.",
  f"The constant {constant:g} is attached to the variable term. Use its inverse operation next.",
  f"Apply {inverse_text} to both sides so equality is preserved.",
  f"The constant and {inverse_text} cancel on the left, and the right side becomes {simplified_right}.",
  f"Divide both sides by {coefficient} because x is multiplied by {coefficient}.",
  f"Both sides simplify, giving x equals {x_text}.",
  f"Substitute {x_text} into the original equation.",
  "Evaluate the multiplication before combining the constant.",
  f"Both sides equal {right}, so the solution is verified.",
 ]
 states=[equation,equation,equation,balanced,simplified,division,solved,substituted,multiplied,verified]
 operations=["balance_focus_goal","balance_focus_constant","apply_both_sides_display","simplify_equation","divide_both_sides_display","simplify_equation","verification_line","verification_line","verification_line"]
 templates=["equation_focus","equation_focus","equation_balance_display","equation_simplification","equation_division_display","equation_simplification","equation_verification","equation_verification","equation_verification"]
 actions=[
  [TimelineEvent(at_ms=250,type="focus",targets=["variable-term"])],
  [TimelineEvent(at_ms=250,type="dim",targets=["variable-term","right-side"]),TimelineEvent(at_ms=350,type="focus",targets=["constant-term"])],
  [TimelineEvent(at_ms=250,type="apply_both_sides",targets=[f"{operation_id}-left",f"{operation_id}-right"],label=inverse_text)],
  [TimelineEvent(at_ms=150,type="apply_both_sides",targets=[f"{operation_id}-left",f"{operation_id}-right"],label=inverse_text),TimelineEvent(at_ms=300,type="cancel",targets=[f"{operation_id}-left",f"{operation_id}-right"]),TimelineEvent(at_ms=500,type="simplify",targets=["cancel-pair"])],
  [TimelineEvent(at_ms=200,type="focus",targets=["coefficient"]),TimelineEvent(at_ms=350,type="apply_both_sides",targets=["divide-left","divide-right"],label=f"divide by {coefficient}")],
  [TimelineEvent(at_ms=300,type="simplify",targets=["answer"])],
  [TimelineEvent(at_ms=300,type="substitute",targets=["verification"])],
  [TimelineEvent(at_ms=300,type="simplify",targets=["verification"])],
  [TimelineEvent(at_ms=300,type="verify",targets=["verification"],style="verification")],
 ]
 steps=[]
 for index,(before,after,operation,template,caption,event_actions) in enumerate(zip(states,states[1:],operations,templates,captions,actions)):
  events=[TimelineEvent(at_ms=0,type="narration",text=caption),TimelineEvent(at_ms=0,type="caption",text=caption),*event_actions]
  value=abs(inverse) if operation=="apply_both_sides_display" else coefficient if operation=="divide_both_sides_display" else None
  steps.append(TeachingStep(id=f"step-{index}",step_number=index,title=("Identify the goal","Identify the first obstacle",f"Apply {inverse_text} to both sides","Simplify the balanced equation",f"Divide both sides by {coefficient}","Reveal x","Substitute in the original","Evaluate the left side","Verify equality")[index],before_expression=before,working_expression=after,operation=MathematicalOperation(type=operation,value=value),after_expression=after,explanation=explanation("Work one legal operation at a time",caption),common_mistake="Never move a term across the equals sign without showing the same inverse operation on both sides.",animation_template=template,screen_reader_description=caption,visualization_state=VisualizationState(objects=[obj.id for obj in objects],annotations=["semantic-equation",f"visual-stage:{index}"]),instructional_goal=caption,duration_ms=900,events=events,narration=caption,state_after={"expression":after}))
 params={"mode":"balance","prompt":spec["prompt"],"answer":spec["answer"],"method":"Apply the same inverse operation to both sides."}
 return WhiteboardBlock(id=f"g12-algebra-01-board-{order:02}",representation="visual",problem=spec["prompt"],initial_expression=equation,steps=steps,visualization=VisualizationInstruction(type="algebra",template="algebra_reasoning",parameters=params),semantic_objects=objects,formula_understanding=formula_understanding(item,"balance"))

def board(item, spec, order):
 if spec["id"] == "G12-ALG-L01-W01":
  return balance_prototype(item,spec,order)
 if spec["id"] == "G12-ALG-L01-W02":
  return balance_second_example(item,spec,order)
 if item["number"] == 1:
  return balanced_equation_timeline(item,spec,order)
 number=item["number"]; mode=MODES[number-1]; prompt=spec["prompt"]; answer=spec["answer"]
 fragments=[part.strip() for part in answer.split(";") if part.strip()]
 method=item["anchor"].strip()
 if method == prompt: method=f"Use {mode.replace('_',' ')} on the displayed structure."
 states=[prompt,*fragments]
 if len(states)==2:
  states.insert(1,method)
 names=("left-side","equals","right-side","operation","candidate","restriction","discriminant","branch-a","branch-b","number-line","endpoint-a","endpoint-b","result","verification")
 objects=[SemanticObject(id=name,type="token",value=name.replace("-"," ")) for name in names]
 family_actions={
  "factorisation":"factor_expression","zero_product":"split_zero_product",
  "quadratic_formula":"calculate_discriminant","method_selection":"show_operation",
  "surd":"preserve_restriction","quadratic_form":"back_substitute",
  "exponential":"replace","linear_simultaneous":"align",
  "nonlinear_simultaneous":"pair_solutions","inequality":"mark_number_line",
  "discriminant":"calculate_discriminant","parameter_roots":"calculate_discriminant",
  "rational_restrictions":"preserve_restriction","proof":"replace",
  "modelling":"substitute","integrated":"show_operation","mastery":"show_operation",
 }
 action=family_actions[mode]
 steps=[]
 for i,(before,after) in enumerate(zip(states,states[1:])):
  title="Select the method" if i==0 else "Perform the next mathematical step"
  operation_expression=method if i==0 else f"{before}  →  {after}"
  narration=(f"First identify why {mode.replace('_',' ')} applies before changing the expression."
             if i==0 else f"Apply one {mode.replace('_',' ')} step. This produces {after}.")
  targets=["left-side","right-side"] if "=" in before else ["operation"]
  events=[TimelineEvent(at_ms=0,type="narration",text=narration),TimelineEvent(at_ms=0,type="caption",text=narration),TimelineEvent(at_ms=180,type="focus",targets=targets),TimelineEvent(at_ms=420,type=action,targets=targets)]
  steps.append(TeachingStep(id=f"step-{i}",step_number=i,title=title,before_expression=before,working_expression=operation_expression,operation=MathematicalOperation(type="algebra_select" if i==0 else "algebra_transform"),after_expression=after,explanation=explanation(title,narration),common_mistake=item["misconception"],animation_template="algebra_timeline_reasoning",screen_reader_description=narration,visualization_state=VisualizationState(objects=list(names),highlights=targets,annotations=[mode,f"stage:{i}"]),instructional_goal=title,duration_ms=900,events=events,narration=narration,state_after={"expression":after,"mode":mode}))
 verify_before=states[-1]
 verify_working=f"Check in the original task: {prompt}"
 verify_after=f"Verified: {answer}"
 verify_caption="Check the result against the original task, including every restriction, branch, interval or ordered pair."
 verify_events=[TimelineEvent(at_ms=0,type="narration",text=verify_caption),TimelineEvent(at_ms=0,type="caption",text=verify_caption),TimelineEvent(at_ms=250,type="verify_original",targets=["verification"])]
 steps.append(TeachingStep(id=f"step-{len(steps)}",step_number=len(steps),title="Verify in the original task",before_expression=verify_before,working_expression=verify_working,operation=MathematicalOperation(type="algebra_verify"),after_expression=verify_after,explanation=explanation("Verify",verify_caption),common_mistake=item["misconception"],animation_template="algebra_timeline_reasoning",screen_reader_description=verify_caption,visualization_state=VisualizationState(objects=list(names),highlights=["verification"],annotations=[mode,f"stage:{len(steps)}"]),instructional_goal="Verify the result",duration_ms=900,events=verify_events,narration=verify_caption,state_after={"expression":verify_after,"mode":mode}))
 params={"mode":mode,"prompt":prompt,"answer":answer,"method":item["anchor"]}
 numbers=[float(value) for value in re.findall(r"(?<![A-Za-z^])[-+]?\d+(?:\.\d+)?",answer)[:6]]
 if numbers: params["values"]=numbers
 return WhiteboardBlock(id=f"g12-algebra-{number:02}-board-{order:02}",representation="visual",problem=prompt,initial_expression=prompt,steps=steps,visualization=VisualizationInstruction(type="algebra",template="algebra_reasoning",parameters=params),semantic_objects=objects,formula_understanding=formula_understanding(item,mode))

def questions(item):
 levels={"Foundation":"foundation","Routine":"standard","Complex":"intermediate","Exam-level":"exam"}
 return [WhiteboardQuestion(id=spec["id"],order=i,difficulty=levels[spec["level"]],estimated_minutes=5,is_core_example=i==1,guidance_level="high" if i<=2 else "moderate" if i<=6 else "reduced" if i<=8 else "minimal",whiteboard=board(item,spec,i),cognitive_level="knowledge" if i<=2 else "routine" if i<=6 else "complex" if i<=8 else "problem_solving",marks=2 if i<=2 else 3 if i<=8 else 4,answer=spec["answer"],full_memo=[item["anchor"],spec["answer"],"Verify in the original task."],misconception_tags=[item["misconception"]]) for i,spec in enumerate(item["whiteboards"],1)]

def lesson(item):
 qs=questions(item); number=item["number"]
 mastery={"minimum_correct":10,"required_exam_question_numbers":[11,12],"explain_back_required":True,"critical_misconception":item["misconception"],"worked_solution_view_is_independent_mastery":False}
 if number==18: mastery.update({"timed_marks":25,"minimum_marks":20,"initial_hints_allowed":False,"parallel_reassessment_required_after_reteach":True})
 return Lesson(id=item["id"],order=number,title=item["title"],objective=item["objective"],why_it_matters="Algebra, Equations and Inequalities contributes approximately 25 marks to CAPS Mathematics Paper 1.",intuition=item["teaching"],prerequisites=[] if number==1 else [f"g12-algebra-{number-1:02}"],estimated_minutes=65,difficulty="foundation" if number<=2 else "standard" if number<17 else "exam",access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,status=ContentStatus.TEACHER_REVIEW_REQUIRED,blocks=[LessonBlock(type="concept",title="Teach the idea before the procedure",content=item["teaching"],data={"source":SOURCE,"structure_anchor":item["anchor"]}),qs[0].whiteboard,LessonBlock(type="mistake",title="Misconception diagnosis and repair",content=f"Detect and repair {item['misconception']} at its first invalid step."),LessonBlock(type="practice",title="Self-guided practice",content="Attempt, submit, use progressive support if needed, explain back, then continue.",data={"practice_bank_id":item["id"],"mastery":mastery}),LessonBlock(type="checkpoint",title="Explain-back exit checkpoint",content="Explain why the selected method applies, how validity was preserved and how the result was verified.",data={"options":["I can justify and verify the method","I need targeted repair"],"correct_index":0,"feedback":"Independent mastery also requires 10 of 12, including both exam items."}),LessonBlock(type="summary",title="Key takeaway",content=item["objective"])],whiteboard_questions=qs,mastery_threshold=.8)

ALGEBRA_EQUATIONS_INEQUALITIES_LESSONS=[lesson(item) for item in DATA]
