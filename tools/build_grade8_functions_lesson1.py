"""Original Grade 8 functions and relationships input-output lesson source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/curriculum/grade8/functions-relationships/Project_Athena_Grade8_Functions_Relationships_Lesson1_Source_Pack_v1.docx'
JSON=ROOT/'backend/app/curriculum/grade8/generated/functions_relationships_01.json'
SOURCES=[
 ('DBE CAPS Mathematics Grades 7–9','https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf'),
 ('DBE Grade 8 Mathematics 2026 ATP','https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208'),
]


def ex(n,level,marks,skill,prompt,answer,family,inputs,outputs,states,moves,verify,misconception,repair):
    assert len(states)==len(moves)+1 and len(set(states))==len(states)
    assert 1<len(inputs)<=5 and 0<len(outputs)<=4
    return dict(id=f'g8-fr-l01-w{n:02}',number=n,level=level,marks=marks,skill=skill,
        q=prompt,answer=answer,model={'family':family,'inputs':inputs,'outputs':outputs,'description':skill},
        states=states,steps=[dict(title=t,action=a,narration=v) for t,a,v in moves],
        verify=verify,misconception=misconception,repair=repair)


E=[
 ex(1,'foundation',2,'Read a one-step flow','A flow machine multiplies each input by 3. Find the output for input 4.',
    '12.','function_flow',['input 4','multiply by 3'],['output 12'],
    ['4 enters a times-three machine','4×3=12','The output is 12'],
    [('Track the input','Move the four tile into the multiplication box.','The given input is four.'),('Multiply','Four groups of three give twelve.','The output is twelve, not seven.')],
    'Using the original rule, 4×3=12.','Adding three instead of multiplying.','Read the operation printed inside the flow box.'),
 ex(2,'easy',3,'Follow a two-step flow','The flow is add 5, then double. Find the output when the input is 2.',
    '14.','function_flow',['input 2','add 5','then double'],['intermediate 7','output 14'],
    ['2→add 5→double','2+5=7','7×2=14'],
    [('First arrow','Two plus five gives seven.','Do the operation beside the first arrow first.'),('Second arrow','Double seven to fourteen.','The doubling applies to seven, not two.')],
    '2→7→14 under the stated flow.','Doubling two before adding five.','Place the intermediate result between the two arrows.'),
 ex(3,'easy',3,'Find a missing output from a table','A rule is y=x+4. A table contains input 1→5 and 3→7. Find the missing output for input 6.',
    '10.','function_table',['rule y=x+4','1→5','3→7','input 6'],['6→10'],
    ['Rule x+4 with missing row x=6','Replace x by 6','6+4=10'],
    [('Choose the missing row','Move input six into the rule.','The other rows show how the rule behaves.'),('Evaluate','Add four to six to get ten.','Check the same add-four pattern holds for all rows.')],
    '1+4=5; 3+4=7; 6+4=10.','Copying the previous output rather than applying the rule.','Trace the input row through the rule.'),
 ex(4,'standard',4,'Reverse a one-step flow','A multiply-by-4 machine produces output 28. What input did it receive?',
    '7.','function_reverse',['unknown input','multiply by 4','output 28'],['input 7'],
    ['?×4=28','Reverse with 28÷4','Input is 7'],
    [('Read the output backward','Start at twenty eight and undo multiplication by four.','The reverse action is division.'),('Recover the input','Twenty eight shared into four groups gives seven.','Send seven forward to check.')],
    '7×4=28, the original output.','Multiplying twenty eight by four.','Use an inverse arrow from output to input.'),
 ex(5,'standard',4,'Reverse a two-step flow','A machine triples a number then adds 2. Its output is 20. Find the input.',
    '6.','function_reverse',['unknown input','multiply by 3','then add 2','output 20'],['before add 18','input 6'],
    ['3x+2=20','Undo +2: 20−2=18','Undo ×3: 18÷3=6'],
    [('Undo the last action','Subtract two from twenty.','Reverse the operations in the opposite order.'),('Undo the first action','Divide eighteen by three.','Six is the original input.')],
    '6×3+2=20.','Dividing twenty by three before removing the two.','Walk back through the flow boxes from right to left.'),
 ex(6,'standard',4,'Read a rule from constant differences','A table shows input 0,1,2,3 and output 5,8,11,14. Give the rule.',
    'y=3x+5.','function_table',['0→5','1→8','2→11','3→14'],['change +3','rule y=3x+5'],
    ['Outputs 5,8,11,14 for inputs 0,1,2,3','Each input +1 adds 3 to output','At input zero, output is 5','Rule y=3x+5'],
    [('Compare two adjacent rows','The output rises by three whenever the input rises by one.','Three is the multiplier of x.'),('Find the start','The row at input zero gives five.','Five is the fixed part.'),('Join rule parts','Multiply input by three, then add five.','Check all four rows.')],
    'At x=0,1,2,3 the rule gives 5,8,11,14.','Calling five the multiplier because it is the first output.','Use the input-zero row for the fixed term.'),
 ex(7,'intermediate',5,'Use a negative input','The rule y=2x−3 maps x=−2 to an output. Find it and show the signed substitution.',
    '−7.','function_flow',['rule 2x−3','input −2','multiply by 2','subtract 3'],['intermediate −4','output −7'],
    ['y=2x−3, x=−2','2(−2)=−4','−4−3=−7'],
    [('Keep negative input grouped','Two times negative two is negative four.','Brackets protect the sign of the input.'),('Subtract three','Move three more units left from negative four.','The output is negative seven.')],
    '2(−2)−3=−4−3=−7.','Treating negative two as positive two.','Place a signed tile into the input slot.'),
 ex(8,'intermediate',5,'Compare two flow orders','Flow A doubles x then adds 3. Flow B adds 3 then doubles. Find both outputs at x=4.',
    'A=11; B=14.','function_compare',['A: ×2 then +3','B: +3 then ×2','input 4'],['A 4→8→11','B 4→7→14'],
    ['One input four; two different flows','A: 4→8→11','B: 4→7→14'],
    [('Trace flow A','Double four to eight, then add three to eleven.','Keep the order stated for A.'),('Trace flow B','Add three to four to make seven, then double to fourteen.','Do not reuse A’s intermediate value.')],
    'A(4)=2(4)+3=11; B(4)=2(4+3)=14.','Assuming the same numbers imply the same rule.','Put each flow in a separate lane and compare outputs.'),
 ex(9,'intermediate',5,'Check equivalent table and formula','A table pairs x=1,2,3 with y=4,7,10. A learner proposes y=3x+1. Does the rule match every row?',
    'Yes; all three rows match.','function_table',['1→4','2→7','3→10','proposed y=3x+1'],['check 4,7,10'],
    ['Table (1,4),(2,7),(3,10); proposed 3x+1','At one: 3+1=4; at two: 6+1=7','At three: 9+1=10; all rows match'],
    [('Check the first two rows','Substitute one and two into the proposed formula.','Matching one row alone is insufficient.'),('Check the remaining row','Substitute three to get ten.','Every provided row must agree.')],
    '3(1)+1=4; 3(2)+1=7; 3(3)+1=10.','Declaring equivalence from a single matched row.','Highlight each tested row separately.'),
 ex(10,'exam',6,'Model a taxi fare table','A taxi charges R7 when you board and R5 per kilometre. Build a rule and give fares for 0,2,4 km.',
    'C(d)=7+5d rand; C(0)=R7, C(2)=R17, C(4)=R27.','function_context',
    ['boarding R7','R5 per km','d=0,2,4 km'],['C(d)=7+5d','R7,R17,R27'],
    ['One boarding fee plus five per kilometre','Variable amount 5d plus fixed 7','C(d)=7+5d','At 0,2,4 km: 7,17,27 rand'],
    [('Count kilometre tiles','Five rand repeats for each kilometre.','The boarding fee does not repeat.'),('Add the start fee','Keep seven rand once outside the repeated row.','This gives the rule seven plus five d.'),('Complete table','Evaluate the rule at zero, two and four kilometres.','Each two kilometres raises the fare by ten rand.')],
    'At 4 km, 7+4×5=27 rand; zero-distance fare is R7.','Multiplying the once-only boarding fee by distance.','Show fixed and variable charges in different rows.'),
 ex(11,'exam',6,'Reverse a fee relationship','A photo booth charges R6 once plus R4 per print. The total was R30. Find the number of prints.',
    '6 prints.','function_reverse',['fixed R6','R4 per print','total R30'],['print cost R24','6 prints'],
    ['6+4p=30','30−6=24 spent on prints','24÷4=6 prints'],
    [('Remove the fixed charge','Subtract the one six-rand fee from thirty.','Twenty four rand belongs to prints.'),('Count print groups','Divide twenty four by four rand per print.','The quotient is six prints.')],
    '6+4(6)=30 rand.','Dividing the full total by the print price.','Separate the fixed fee before reversing the flow.'),
 ex(12,'exam',6,'Distinguish a nonlinear table','A table pairs x=0,1,2,3 with y=0,1,4,9. Is y=2x a rule? Find a matching rule and output at x=4.',
    'y=x²; at x=4 output 16.','function_table',['0→0','1→1','2→4','3→9','claim y=2x'],['rule y=x²','4→16'],
    ['Outputs 0,1,4,9; learner claims 2x','At input one, 2x predicts 2, not 1','Squares match all rows: x²','At x=4, x²=16'],
    [('Test the claim','At one, the proposed double rule gives two.','The table actually shows one, so this rule fails.'),('Test square rule','Zero, one, four and nine are squares of the inputs.','Every given row agrees.'),('Extend to four','Four squared is sixteen.','This relationship is not a constant three-step increase.')],
    '0²=0, 1²=1, 2²=4, 3²=9, 4²=16.','Assuming any growing table is linear.','Show square tiles growing by unequal amounts.'),
 ex(13,'advanced',7,'Compare rules at two inputs','Plan A costs R12 plus R3 per visit; Plan B costs R6 per visit. Compare at 2 and 5 visits.',
    'At 2: A=R18, B=R12; at 5: A=R27, B=R30.','function_compare',
    ['A=12+3v','B=6v','v=2 and v=5'],['at 2: 18 vs 12','at 5: 27 vs 30'],
    ['Two plans at visits 2 and 5','At 2: A=12+6=18; B=12','At 5: A=12+15=27; B=30'],
    [('Compare at two','Calculate both plans for the same two visits.','B costs less at two.'),('Compare at five','Recalculate both plans for five visits.','A costs less at five; comparisons depend on input.')],
    'A(2)=18, B(2)=12; A(5)=27, B(5)=30.','Assuming one plan is always cheaper.','Keep both rules and both shared inputs visible.'),
 ex(14,'advanced',7,'Specify a discrete domain','A carton holds 6 eggs. Write E(c) and state sensible inputs for c cartons. How many eggs in 7 cartons?',
    'E(c)=6c eggs for whole-number c≥0; E(7)=42 eggs.','function_context',
    ['6 eggs per carton','c complete cartons','c whole number ≥0'],['E(c)=6c','E(7)=42'],
    ['Six eggs per complete carton','E(c)=6c eggs','Only whole c≥0 describes complete cartons','Seven cartons hold 42 eggs'],
    [('Build equal groups','Place six eggs in every carton group.','The count follows six times c.'),('Restrict input','A complete carton count is a nonnegative whole number.','Half a carton is not a complete carton in this model.'),('Evaluate seven','Seven groups of six contain forty two eggs.','The output is an egg count.')],
    '7×6=42 eggs; c=0 yields 0 eggs.','Allowing arbitrary negative carton counts.','Show physical whole cartons, then name the domain.'),
 ex(15,'advanced',8,'Integrate flow table and inverse','A rule triples the input then subtracts 4. Fill outputs at x=−1,0,3, then recover the input whose output is 17.',
    'y=3x−4; outputs −7,−4,5; input 7 gives output 17.','function_reverse',
    ['input x','×3 then −4','test −1,0,3','target output 17'],['rule 3x−4','outputs −7,−4,5','inverse input 7'],
    ['Flow triples x then subtracts four','Rule: y=3x−4','At −1: −3−4=−7; at 0: −4','At 3: 9−4=5','Reverse output 17: 17+4=21','Undo triple: 21÷3=7'],
    [('Write the rule','Place multiplication by three before subtraction of four.','The order is stated in the flow.'),('Fill two rows','At negative one output negative seven; at zero output negative four.','Keep the signed input when multiplying.'),('Fill third row','Three triples to nine then minus four leaves five.','Each row follows the same rule.'),('Reverse the last arrow','Add four to seventeen to recover twenty one.','Undo subtraction before multiplication.'),('Reverse multiplication','Divide twenty one by three to recover seven.','Run seven forward to verify.')],
    '3(7)−4=17; the other outputs follow 3x−4.','Dividing 17 by 3 before reversing subtraction.','Preserve intermediate values in forward and reverse lanes.'),
]

P=[
 ('p01','Double an input of 6.','12.','Use multiplication.','2×6=12.'),
 ('p02','Add 4 then double, starting at 3.','14.','Keep the intermediate value.','3+4=7 then 7×2=14.'),
 ('p03','For y=x+7, find the output at x=5.','12.','Substitute the input.','5+7=12.'),
 ('p04','A machine multiplies by 5 and outputs 35. Find the input.','7.','Reverse multiplication.','35÷5=7; 7×5=35.'),
 ('p05','Double then add 3 gives 19. Find the input.','8.','Undo plus three first.','19−3=16, then 16÷2=8.'),
 ('p06','Table 0→2,1→6,2→10. Write a rule.','y=4x+2.','Use difference then zero row.','Outputs rise by 4 for each input +1; at zero output is 2.'),
 ('p07','For y=3x+1, find output at x=−2.','−5.','Keep negative input bracketed.','3(−2)+1=−6+1=−5.'),
 ('p08','A doubles x then subtracts 1; B subtracts 1 then doubles. Give outputs at x=3.','A=5; B=4.','Follow each lane in order.','A: 3→6→5; B: 3→2→4.'),
 ('p09','Does y=2x+1 match table 1→3,2→5,3→7?','Yes; all three rows match.','Check every row.','At inputs 1,2,3 outputs are 3,5,7.'),
 ('p10','A club costs R9 once and R4 per session. Give C(s) and C(3).','C(s)=9+4s; C(3)=R21.','Fixed nine is added once.','9+4(3)=21 rand.'),
 ('p11','R5 once plus R3 per item totals R20. Find items.','5 items.','Remove the fixed fee first.','(20−5)÷3=5 items.'),
 ('p12','Table x=0,1,2 gives y=0,1,4. Find rule and y at x=3.','y=x²; at x=3, y=9.','Test squares.','0²,1²,2² are 0,1,4; 3²=9.'),
 ('p13','A=R8+R2 per visit; B=R5 per visit. Compare 2 and 4 visits.','At 2: A=R12, B=R10; at 4: A=R16, B=R20.','Use shared inputs.','At two B is cheaper; at four A is cheaper.'),
 ('p14','Five buttons per completed card. Write B(c), sensible c and B(8).','B(c)=5c for whole c≥0; B(8)=40.','Card count is discrete.','Eight groups of five give forty buttons.'),
 ('p15','Flow multiply by 4 then minus 3. Give outputs at −1 and 2, and input for output 17.','Outputs −7 and 5; input 5.','Reverse minus three first.','At −1: −4−3=−7; at 2: 8−3=5; (17+3)÷4=5.'),
]
M=[
 ('m01',2,'Machine adds 6. What input gives output 13?','7.','13−6=7; 7+6=13.'),
 ('m02',3,'Table 0→4,1→7,2→10. Give rule.','y=3x+4.','Difference is 3; input zero gives starting value 4.'),
 ('m03',4,'Flow doubles then subtracts 5. Find output for x=−2 and input for output 11.','At x=−2 output −9; input 8 gives 11.','2(−2)−5=−9; reverse (11+5)÷2=8.'),
 ('m04',5,'A delivery charges R10 once plus R6 per km. Give C(d), costs at 0 and 3 km, and sensible d.','C(d)=10+6d; C(0)=R10; C(3)=R28; d≥0.','The fixed charge is R10; 3 km adds R18; distance cannot be negative.'),
 ('m05',6,'Plan A is R8+R4 per visit and Plan B is R6 per visit. Compare at 2 and 5 visits, with both formulas.','A(v)=8+4v, B(v)=6v; at 2 A=R16,B=R12; at 5 A=R28,B=R30.','For two visits B costs R4 less. For five A costs R2 less; both calculations use the same input.'),
]
R=[
 ('r01','Add 7 then triple gives 30. Find the input.','3.','Undo triple: 30÷3=10; undo plus seven: 10−7=3.'),
 ('r02','Table 0→6,1→10,2→14. Write the rule and output for 4.','y=4x+6; output 22.','The output rises by 4 per input step and starts at 6.'),
 ('r03','A printer costs R5 once plus R2 per page. Write C(p), find C(6), and state a sensible domain.','C(p)=5+2p; C(6)=R17; p a whole number ≥0.','Six pages cost R12 plus one R5 fee; page count is nonnegative whole.'),
]


def build():
    assert len(E)==len(P)==15 and len(M)==5 and sum(x[1] for x in M)==20 and len(R)==3
    d=Document(); d.sections[0].top_margin=d.sections[0].bottom_margin=914400
    d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(11)
    for key in ('Title','Heading 1','Heading 2'):
        d.styles[key].font.name='Arial';d.styles[key].font.color.rgb=RGBColor(0,0,0)
    border=d.styles['Title'].element.find('.//'+qn('w:pBdr'))
    if border is not None:border.getparent().remove(border)
    d.add_paragraph('Grade 8 Functions and Relationships Lesson 1',style='Title')
    d.add_heading('Input Output Values and Rules',1)
    d.add_paragraph('Original authoring draft for teacher review and learner browser acceptance. The DOCX and runtime data come from the same checked-in authored records. This lesson teaches a learner to follow a rule, reverse it, compare representations and check results in the original situation.')
    d.add_heading('Curriculum scope and references',1)
    for title,url in SOURCES:d.add_paragraph(f'{title}: {url}')
    d.add_paragraph('Grade 8 CAPS and its 2026 ATP specify finding input values, output values and rules using flow diagrams, tables, formulae and equations. This first lesson teaches the input-output foundation; graphs and later topic lessons remain separate.')
    d.add_heading('Objectives and teaching design',1)
    d.add_paragraph('Prerequisites: integer operations, substitution and simple equations. Estimated 90 minutes. Identify the given input or output, label the mathematical rule, show intermediate values in their flow order, reverse operations in opposite order when finding an input, verify a rule against every given table row, and label units and sensible domains in contexts.')
    d.add_paragraph('The whiteboard begins with given values only. It uses current question data for arrows, input-output tables, reverse pathways, contextual receipts and parallel rules. One operation appears before its mathematical result. Earlier states remain visible. Answers for independent practice, mastery and reassessment remain gated until submission.')
    d.add_heading('Fifteen progressive worked examples and visual steps',1)
    for item in E:
        d.add_heading(f"Example {item['number']} {item['skill']}",2)
        d.add_paragraph(f"{item['level']} · {item['marks']} marks · {item['model']['family']}")
        d.add_paragraph('Question: '+item['q'])
        d.add_paragraph('Given objects: '+'; '.join(f'given-{i+1}: {v}' for i,v in enumerate(item['model']['inputs']))+'. Derived objects initially hidden: '+str(len(item['model']['outputs'])))
        d.add_paragraph('Initial board state: '+item['states'][0])
        for i,step in enumerate(item['steps']):
            d.add_paragraph(f"Step {i+1} {step['title']}. Show operation: {step['action']} Reveal result: {item['states'][i+1]}. Caption and narration: {step['narration']}")
        d.add_paragraph('Answer: '+item['answer']+' Check original: '+item['verify'])
        d.add_paragraph('Misconception: '+item['misconception']+' Repair: '+item['repair'])
    d.add_heading('Fifteen independent practice questions',1)
    for pid,q,a,hint,memo in P:
        d.add_heading(pid.upper(),2);d.add_paragraph('Question: '+q);d.add_paragraph('Hint: '+hint);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Five mastery questions 20 marks',1)
    for pid,marks,q,a,memo in M:
        d.add_heading(f'{pid.upper()} {marks} marks',2);d.add_paragraph('Question: '+q);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Three parallel reassessments',1)
    for pid,q,a,memo in R:
        d.add_heading(pid.upper(),2);d.add_paragraph('Question: '+q);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Release checks',1)
    d.add_paragraph('Teacher verification of mathematical explanations and answers, equivalence-aware scoring, accessibility, responsive layout, and a complete learner browser journey are still required. This pack alone does not approve release.')
    OUT.parent.mkdir(parents=True,exist_ok=True);d.save(OUT)
    payload={'id':'g8-functions-relationships-01','title':'Input output values and rules','source_document':OUT.name,'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'worked_examples':E,'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True);JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print(OUT,JSON,payload['source_sha256'],sep='\n')

if __name__=='__main__':build()
