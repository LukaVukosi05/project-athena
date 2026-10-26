"""Author original Grade 8 equivalent-representation questions and a reviewable pack."""
import hashlib
import json
from pathlib import Path

from docx import Document
from docx.shared import Pt

ROOT=Path(__file__).resolve().parents[1]
SOURCE='Project_Athena_Grade8_Functions_Relationships_Lesson2_Source_Pack_v1.docx'
OUT=ROOT/'docs/curriculum/grade8/functions-relationships'/SOURCE
JSON=ROOT/'backend/app/curriculum/grade8/generated/functions_relationships_02.json'
SOURCES=[
 ('DBE CAPS Mathematics Grades 7–9','https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf'),
 ('DBE Grade 8 Mathematics 2026 ATP','https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208'),
]

def ex(n,level,marks,skill,prompt,answer,family,given,derived,states,moves,verify,mistake,repair):
    assert len(states)==len(moves)+1 and len(set(states))==len(states),(n,states)
    assert 2<=len(given)<=5 and 1<=len(derived)<=4
    return dict(id=f'g8-fr-l02-w{n:02}',number=n,level=level,marks=marks,skill=skill,
        q=prompt,answer=answer,model={'family':family,'inputs':given,'outputs':derived,'description':skill},
        states=states,steps=[dict(title=t,action=a,narration=v) for t,a,v in moves],
        verify=verify,misconception=mistake,repair=repair)

E=[
 ex(1,'foundation',2,'Words into a rule','Double an input, then add 3. Write the rule and find the output at x=4.',
  'y=2x+3; at x=4, y=11.','equivalence_translation',['input x','double','add 3'],['rule 2x+3','4→11'],
  ['The input is doubled then three is added','Doubling x gives 2x','Add three to get y=2x+3','At x=4: 8+3=11'],
  [('Trace the first verb','Attach times two to the input x.','Double the input before adding anything.'),('Trace the second verb','Attach plus three to the doubled input.','The full output is two x plus three.'),('Test the rule','Substitute four and evaluate.','Four becomes eight then eleven.')],
  'Flow 4→8→11 and formula 2(4)+3=11.','Writing 2(x+3) changes the operation order.','Place a value between the double and add arrows.'),
 ex(2,'easy',3,'Table and flow','A table has 0→5, 1→6, 2→7. State a rule that fits and show its flow for input 2.',
  'A fitting rule is y=x+5; 2→add 5→7.','equivalence_flow_table',['0→5','1→6','2→7'],['rule x+5','flow 2→7'],
  ['Three given rows rise by one per input step','At zero the output is five','A fitting rule is y=x+5','Input two plus five gives seven'],
  [('Compare equal input steps','Each input increase of one matches an output increase of one.','A simple add-five rule is a candidate.'),('Use input zero','Five is the output when input is zero.','This is the fixed part of the candidate rule.'),('Draw a flow','Send two through plus five to get seven.','The flow reproduces the stated row.')],
  'The candidate gives 5,6,7 on all stated inputs; other rules may fit only these rows.','Claiming the three rows uniquely prove a rule for every input.','Call it a fitting rule and check every given row.'),
 ex(3,'easy',3,'Brackets in a flow','The flow adds 2 then triples. Write its formula and output at x=1.',
  'y=3(x+2)=3x+6; at x=1, y=9.','equivalence_algebra',['input x','add 2','triple'],['3(x+2)','3x+6','1→9'],
  ['Flow x→add 2→times 3','The intermediate value is x+2','Triple the complete bracket: 3(x+2)','Distribute to 3x+6','At one: 3(1+2)=9'],
  [('Preserve the intermediate','Write x plus two in a single bracket.','The second arrow acts on the complete result.'),('Build formula','Multiply the complete bracket by three.','The flow is three times the quantity x plus two.'),('Show equivalent expression','Multiply each term inside the bracket by three.','This gives three x plus six.'),('Check with an input','At one the bracket is three, then triples to nine.','Both formula forms agree.')],
  '3(1+2)=9 and 3(1)+6=9.','Writing 3x+2 applies the triple to x alone.','Keep the entire intermediate result inside brackets.'),
 ex(4,'standard',4,'Distinguish operation order','Rule A doubles x then adds 3. Rule B adds 3 then doubles. Are they equivalent? Use x=2.',
  'No. A(2)=7 while B(2)=10.','equivalence_counterexample',['A: ×2 then +3','B: +3 then ×2','input 2'],['A=7','B=10','not equivalent'],
  ['Two flows start at the same input two','A: 2→4→7','B: 2→5→10','Seven differs from ten, so the rules differ'],
  [('Follow A in order','Double two then add three to get seven.','Keep A in its own lane.'),('Follow B in order','Add three then double to get ten.','Do not use A’s intermediate value.'),('Compare shared input','Seven is different from ten.','One counterexample proves that the rules are not equivalent.')],
  'A(2)=2(2)+3=7; B(2)=2(2+3)=10.','Treating addition and multiplication as interchangeable in a flow.','Use one common input in two separate lanes.'),
 ex(5,'standard',4,'Choose a formula from a table','The rows are 0→4,1→6,2→8. Which fits: A: y=2x+4 or B: y=4x+2? Check all rows.',
  'A fits every row; B fails already at x=0.','equivalence_flow_table',['0→4','1→6','2→8','A=2x+4','B=4x+2'],['A: 4,6,8','B(0)=2','A fits'],
  ['Given outputs are 4,6,8','A predicts 4,6,8','B predicts 2 at input zero','A fits; B does not'],
  [('Evaluate A row by row','Compute two x plus four at zero, one and two.','Each calculated output matches the stated row.'),('Find B’s first mismatch','At zero, four times zero plus two is two.','The table says four, so B is ruled out.'),('State the conclusion','A matches every supplied row while B fails one.','The comparison concerns these two candidates on the given rows.')],
  'A(0,1,2)=(4,6,8); B(0)=2≠4.','Comparing only the multiplier without testing the fixed value.','Test the input-zero row first.'),
 ex(6,'standard',4,'Subtraction in words and formula','“Start at 5 and subtract twice the input.” Write a formula and find its output at x=−1.',
  'y=5−2x; when x=−1, y=7.','equivalence_translation',['start 5','subtract twice x','input −1'],['5−2x','output 7'],
  ['The start is five; twice x is subtracted','Twice the input is 2x','The rule is y=5−2x','At −1: 5−2(−1)=7'],
  [('Name the repeated quantity','Twice x means two multiplied by x.','Keep the factor with the variable.'),('Write the full rule','Subtract the whole two x from five.','The order is five minus two x.'),('Substitute with brackets','Twice negative one is negative two; subtracting it gives seven.','Check the sign before simplifying.')],
  '5−2(−1)=5+2=7.','Reading the words as 2(5−x).','Place the five before the subtraction arrow.'),
 ex(7,'intermediate',5,'Prove algebraic equivalence','A flow gives y=3(x−2). A classmate writes y=3x−6. Show why these are the same rule for every x.',
  '3(x−2)=3x−6 by distribution, so they agree for every x.','equivalence_algebra',['3(x−2)','3x−6','any input x'],['3x−6','same rule for all x'],
  ['Compare the two symbolic descriptions','Distribute 3 to x: 3×x=3x','Distribute 3 to −2: 3×(−2)=−6','Both descriptions equal 3x−6'],
  [('Mark the first product','Three multiplies x to produce three x.','The outside factor applies to every bracket term.'),('Mark the signed product','Three times negative two is negative six.','Keep the negative sign in the second product.'),('Compare expressions','The expanded form is exactly the second expression.','An identity proves equivalence for all inputs in the common domain.')],
  'At any x, distribution gives 3x−6; both have the same domain.','Expanding only the first bracket term.','Draw a multiplication arrow from three to each term.'),
 ex(8,'intermediate',5,'Locate the half','Compare “half the input then add 4” with “add 4 then halve”. Are they equivalent? Use x=8.',
  'No. First: 8; second: 6 at x=8.','equivalence_counterexample',['A: x÷2 then +4','B: x+4 then ÷2','input 8'],['A=8','B=6','not equivalent'],
  ['Use input eight in both flows','A: 8÷2=4, then 4+4=8','B: 8+4=12, then 12÷2=6','Different outputs disprove equivalence'],
  [('Trace the first wording','Half eight to four and then add four.','A gives eight.'),('Trace the second wording','Add four to eight first and halve twelve.','B gives six.'),('Compare the outputs','Eight and six are different.','The bracket placement changes which total is halved.')],
  '8÷2+4=8; (8+4)÷2=6.','Assuming both descriptions halve only x.','Draw each operation order and bracket the intermediate total.'),
 ex(9,'intermediate',5,'Money story, table and domain','An activity charges R15 once plus R4 per ticket. Give C(n), a table at n=0,1,3, and sensible inputs.',
  'C(n)=15+4n rand; 0→R15,1→R19,3→R27; n a whole number ≥0.','equivalence_context',['fixed R15','R4 per ticket','n=0,1,3'],['C(n)=15+4n','15,19,27','n whole ≥0'],
  ['Fixed fifteen plus four per ticket','The repeated charge is 4n','Formula C(n)=15+4n','Table: 15,19,27 rand','Ticket counts are nonnegative whole numbers'],
  [('Build the repeated part','Count four rand once for each ticket.','Four n changes when n changes.'),('Add the once-only charge','Keep fifteen outside the repeated amount.','The formula is fifteen plus four n.'),('Fill each row','Evaluate zero, one and three tickets.','Each table output follows the same rule.'),('Check the context domain','A ticket count cannot be fractional or negative.','Domain affects which symbolic inputs make sense.')],
  'C(0)=15, C(1)=19, C(3)=27 with n∈{0,1,2,…}.','Charging R15 per ticket or allowing negative ticket counts.','Separate once-only and per-ticket tiles.'),
 ex(10,'exam',6,'Area as flow and expanded formula','A rectangle has width 3 cm and length (x+2) cm. Write area as a flow and two equivalent formulas. Find area at x=5.',
  'A=3(x+2)=3x+6 cm²; when x=5, A=21 cm².','equivalence_algebra',['length x+2','width 3','area length × width'],['3(x+2)','3x+6','21 cm²'],
  ['Length x+2 and width 3','Flow: add 2 to x, then multiply by 3','Area A=3(x+2)','Distribute: A=3x+6','At five: 3(7)=21 square centimetres'],
  [('Follow the length first','Add two to x to obtain the whole length.','The width does not add to the length.'),('Build area product','Multiply the whole length by width three.','Area is width times length.'),('Split the area','Three multiplies x and two, giving three x plus six.','The two forms represent the same rectangle.'),('Check dimension','At five, length is seven and width three.','Area twenty one has square centimetre units.')],
  '3(5+2)=21 and 3×5+6=21 cm².','Adding 3 and x+2 rather than multiplying side lengths.','Show the full rectangle as two adjoining regions.'),
 ex(11,'exam',6,'Limits of a short table','A table contains 0→0 and 2→4. Both y=2x and y=x² fit. Show they are not the same rule.',
  'At x=1, 2x=2 but x²=1, so they are not equivalent.','equivalence_counterexample',['0→0','2→4','A=2x','B=x²'],['A(1)=2','B(1)=1','not equivalent'],
  ['Two rows agree with both proposed rules','At x=1, A gives 2','At x=1, B gives 1','One differs from the other'],
  [('Choose a fresh input','Test one, which the table does not show.','Agreement at finitely many rows alone cannot prove equivalence.'),('Evaluate both rules','Twice one is two; one squared is one.','The candidates differ on the same input.'),('Use the counterexample','Two differs from one.','The rules are not identical, even though both fit the displayed rows.')],
  'Both fit x=0,2; at x=1 outputs 2 and 1 differ.','Claiming a few matched table rows prove two formulas identical.','Look for a fresh input or prove an identity.'),
 ex(12,'exam',6,'Units and restricted inputs','A complete carton contains 6 eggs. Are “six times the number of cartons” and E(c)=6c equivalent for c=0,1,2,…? Could c=−1 describe the situation?',
  'Yes on nonnegative whole-number c; c=−1 is outside the context.','equivalence_domain',['6 eggs/carton','c complete cartons','c whole ≥0'],['E(c)=6c eggs','same rule on domain','−1 excluded'],
  ['Each complete carton contributes six eggs','Words translate to E(c)=6c','At zero, one, two: 0,6,12 eggs','The descriptions agree for every valid whole c','A negative carton count is invalid here'],
  [('Build the equal groups','Multiply the number of cartons by six eggs each.','This translates the words into a formula.'),('Test sample rows','At zero, one and two cartons count zero, six and twelve eggs.','The samples illustrate the translation.'),('State the identity','For each valid carton count, both descriptions mean six c.','The same operation, not just the samples, justifies equivalence.'),('Restrict the domain','A negative complete-carton count is not a situation in this question.','Keep the context with the algebra.')],
  'Both descriptions are 6c eggs for c∈{0,1,2,…}; −1 is not a valid count.','Declaring every algebraic input a possible physical count.','Mark the allowed carton inputs on a number line.'),
 ex(13,'advanced',7,'Reject a misleading fare formula','A plan charges R8 once and R3 per visit. Compare A(n)=8+3n with B(n)=3(n+8) using n=0 and n=4. Which represents the plan?',
  'A represents it: A(0)=R8,A(4)=R20. B(0)=R24,B(4)=R36, so B does not.','equivalence_context',['fixed R8','R3 per visit','n=0,4','B=3(n+8)'],['A(0)=8,B(0)=24','A(4)=20,B(4)=36','choose A'],
  ['A once-only eight-rand charge plus three per visit','At zero visits, actual cost is eight','A(0)=8 while B(0)=24','At four visits, A(4)=20','B(4)=36; only A models this plan'],
  [('Read the starting amount','With no visits, the only cost is eight rand.','Zero is a powerful test for a fixed fee.'),('Test zero in both formulas','A gives eight while B incorrectly gives twenty four.','The bracket multiplies the fixed charge.'),('Check the first candidate again','At four visits, eight plus twelve is twenty rand.','A repeats only the per-visit charge.'),('Check the other candidate','B makes three times twelve equal thirty six.','The extra amount confirms that B models a different arrangement.')],
  'The words imply 8+3n; at n=0 and n=4 A gives 8,20, while B gives 24,36.','Multiplying a once-only fee by the number of visits.','Put the fixed fee outside the multiplication bracket.'),
 ex(14,'advanced',7,'Reject a plausible table rule','Outputs 3,5,7 correspond to inputs 0,1,2. Compare A(x)=2x+3 and B(x)=3x+2; give the matching candidate and explain.',
  'A matches all three rows; B(0)=2≠3 and B(2)=8≠7.','equivalence_flow_table',['0→3','1→5','2→7','A=2x+3','B=3x+2'],['A: 3,5,7','B: 2,5,8','A fits'],
  ['Given pairs (0,3),(1,5),(2,7)','A at 0,1,2 gives 3,5,7','B at zero gives two','B at two gives eight','Only A matches every stated row'],
  [('Evaluate A at each input','Calculate two x plus three at zero, one and two.','All outputs agree with the table.'),('Test B at zero','Three times zero plus two is two, not three.','One mismatch rules B out.'),('Test B at two','Three times two plus two is eight, not seven.','The middle row alone was misleading.'),('Conclude precisely','A is the matching candidate among the two proposed rules.','A short table does not establish uniqueness among all possible formulas.')],
  'A(0,1,2)=(3,5,7); B(0,1,2)=(2,5,8).','Trusting one matching row instead of checking every row.','Highlight the first and third mismatches.'),
 ex(15,'advanced',8,'Identity versus counterexample in one scene','Compare A(x)=2(x+5), B(x)=2x+10, C(x)=2x+5. Which are equivalent for every x? Show outputs at x=0 and x=3.',
  'A and B are equivalent for every x; C differs. At x=0: 10,10,5; x=3: 16,16,11.','equivalence_algebra',['A=2(x+5)','B=2x+10','C=2x+5','x=0,3'],['A=B for all x','C differs','10,10,5','16,16,11'],
  ['Three proposed rules A,B,C','Expand A: 2×x+2×5','A=2x+10, identical to B','At zero: A=10,B=10,C=5','At three: A=16,B=16,C=11','A and B agree for all x; C fails'],
  [('Expand both bracket parts','Distribute two to x and five.','The whole bracket is doubled.'),('Compare symbolic forms','Expanded A is exactly B.','An identity proves these two agree for all x.'),('Test a counterexample','At zero A and B give ten; C gives five.','One input disproves equivalence with C.'),('Check another input','At three A and B give sixteen; C gives eleven.','The two results stay distinct.'),('State the exact conclusion','A and B are equivalent, while C is not.','Sample checks illustrate the algebraic identity and counterexample.')],
  '2(x+5)=2x+10 identically; at zero and three C differs.','Assuming 2(x+5)=2x+5 by distributing to only x.','Draw one distribution arrow to each bracket term.'),
]

P=[
 ('p01','“Triple x then subtract 1.” Write a formula.','y=3x−1.','Triple first, then subtract.','Three times x less one is 3x−1.'),
 ('p02','Table 0→2,1→3,2→4. Give one fitting simple rule.','y=x+2.','Use input zero.','x+2 agrees with every listed row; it is a fitting candidate.'),
 ('p03','Flow adds 4 then doubles. Give a formula.','y=2(x+4).','Keep the intermediate value bracketed.','Double the whole x+4.'),
 ('p04','Is 2(x+3) equivalent to 2x+6?','Yes, for all x.','Distribute to both terms.','2×x+2×3=2x+6.'),
 ('p05','At x=2 compare 3x+1 with 3(x+1). Are they equivalent?','No; at x=2 they give 7 and 9.','Try the same input in both.','3(2)+1=7; 3(2+1)=9.'),
 ('p06','Table 0→6,1→8,2→10. Which fits: 2x+6 or 6x+2?','2x+6 fits; 6x+2 fails.','Test zero first.','At zero the expected output is six, not two.'),
 ('p07','“Start at 7 and subtract twice x.” Formula and output at x=−1?','y=7−2x; output 9.','Protect the negative input.','7−2(−1)=9.'),
 ('p08','Are 4(x−3) and 4x−12 equivalent for all x?','Yes, for all x.','Distribute four to both terms.','4×x+4×(−3)=4x−12.'),
 ('p09','Half x then add 3 versus add 3 then halve. Compare at x=6.','First gives 6; second gives 4.5; not equivalent.','Draw two operation orders.','6÷2+3=6, while (6+3)÷2=4.5.'),
 ('p10','R12 once plus R5 per ticket. Give C(n), C(0), C(2), and sensible n.','C(n)=12+5n; C(0)=R12; C(2)=R22; n a whole number ≥0.','Fixed fee is added once.','12+5(2)=22 rand; n counts tickets.'),
 ('p11','The table 0→0,2→8 fits y=4x and y=2x². Find an input where they disagree.','At x=1, outputs are 4 and 2.','Choose an input not in the table.','4(1)=4 but 2(1²)=2, so the rules differ.'),
 ('p12','Rectangle width 4, length x+3. Give equivalent area formulas and area at x=2.','A=4(x+3)=4x+12; at x=2, A=20 square units.','Multiply the complete length.','4(2+3)=20 and 4(2)+12=20.'),
 ('p13','A=R5+R4 per visit; B=R4(n+5). Which reflects the stated fixed R5 at zero visits?','A(n)=5+4n; A(0)=R5; B(0)=R20 does not.','Test zero visits.','The once-only five is not multiplied by four.'),
 ('p14','Table 0→2,1→5,2→8. Compare 3x+2 and 2x+3 on all rows.','3x+2 matches; 2x+3 does not.','Test zero and two.','3x+2 gives 2,5,8; 2x+3 gives 3,5,7.'),
 ('p15','Compare 3(x+2), 3x+6 and 3x+2 for all x; give outputs at x=0.','First two equivalent for all x; at zero they give 6 and 6, while third gives 2.','Distribute to both terms.','3(x+2)=3x+6 identically; 3x+2 fails at zero.'),
]
M=[
 ('m01',2,'“Double x, then subtract five.” Give a formula and output at x=4.','y=2x−5; output 3.','Two times four minus five equals three.'),
 ('m02',3,'Table 0→3,1→7,2→11. Compare y=4x+3 and y=3x+4. Which fits?','y=4x+3 fits; y=3x+4 fails at x=0 and x=2.','First gives 3,7,11; second gives 4,7,10.'),
 ('m03',4,'Are 5(x−2) and 5x−10 equivalent for every x? Explain and evaluate both at x=3.','Yes; 5(x−2)=5x−10, and both give 5 at x=3.','Distribute five to x and negative two; x=3 gives five.'),
 ('m04',5,'A workshop charges R20 once plus R3 per item. Give C(n), costs at zero and four, sensible n, and reject 3(n+20).','C(n)=20+3n; C(0)=R20; C(4)=R32; n whole ≥0; 3(n+20) gives R60 at zero, so it is wrong.','The fixed fee occurs once and the per-item fee repeats.'),
 ('m05',6,'A=2(x+4), B=2x+8 and C=2x+4. Identify the equivalent pair for all x, use x=0 to reject the third, and give outputs at x=3.','A and B equivalent for all x; at x=0 A=B=8 but C=4; at x=3 A=B=14 and C=10.','Distribute two to x and four to prove A=B. The counterexample at zero rejects C.'),
]
R=[
 ('r01','“Triple x then add five” and “add five then triple”. At x=2 compare outputs.','First 11; second 21; not equivalent.','3(2)+5=11, while 3(2+5)=21.'),
 ('r02','Are 4(x−2) and 4x−8 equivalent for every x? Give a reason.','Yes; 4(x−2)=4x−8 by distribution.','Four multiplies both x and negative two.'),
 ('r03','A booking costs R9 once plus R2 per seat. Give the formula, table for zero and three seats, and sensible seat counts.','C(n)=9+2n; C(0)=R9; C(3)=R15; n whole ≥0.','Count the fixed R9 once; three seats add R6.'),
]

def build():
    assert len(E)==len(P)==15 and len(M)==5 and sum(row[1] for row in M)==20 and len(R)==3
    d=Document(); d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(11)
    d.add_heading('Grade 8 Functions and Relationships — Lesson 2',0)
    d.add_heading('Equivalent Forms of a Relationship',1)
    d.add_paragraph('Original question bank for teacher review. Learners translate a relationship among words, flows, tables and formulas; prove an identity by legal algebra and reject a proposed equivalence using one counterexample. Matching a few table rows establishes agreement on those rows, not uniqueness for all inputs.')
    d.add_heading('CAPS scope and source references',1)
    for label,url in SOURCES:d.add_paragraph(f'{label}: {url}')
    d.add_heading('Pedagogical contract',1)
    d.add_paragraph('Prerequisite: Lesson 1 input-output rules and Grade 8 distribution. A whiteboard opens with the complete question and only given objects. It constructs one representation at a time, showing the legal operation before the new mathematical state. Earlier states remain visible. Derived objects appear only at their corresponding result step. Final verification returns to the given words, flow, table or situation. Context inputs keep their domain and units.')
    d.add_heading('Fifteen progressive whiteboard examples',1)
    for item in E:
        d.add_heading(f"Example {item['number']}: {item['skill']}",2)
        d.add_paragraph(f"{item['level']} · {item['marks']} marks · {item['model']['family']}")
        d.add_paragraph('Question: '+item['q'])
        d.add_paragraph('Given objects: '+'; '.join(item['model']['inputs']))
        d.add_paragraph('Derived objects, initially hidden: '+'; '.join(item['model']['outputs']))
        d.add_paragraph('Initial state: '+item['states'][0])
        for i,step in enumerate(item['steps']):
            d.add_paragraph(f"Step {i+1}: {step['title']}. Operation: {step['action']} Result: {item['states'][i+1]}. Narration and caption: {step['narration']}")
        d.add_paragraph('Answer: '+item['answer']+' Verify: '+item['verify'])
        d.add_paragraph('Misconception: '+item['misconception']+' Reteach: '+item['repair'])
    d.add_heading('Independent practice: fifteen fresh questions',1)
    for pid,q,a,h,memo in P:
        d.add_heading(pid.upper(),2);d.add_paragraph('Question: '+q);d.add_paragraph('Hint: '+h);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Mastery: five questions, twenty marks',1)
    for pid,marks,q,a,memo in M:
        d.add_heading(f'{pid.upper()} — {marks} marks',2);d.add_paragraph('Question: '+q);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Parallel reassessment',1)
    for pid,q,a,memo in R:
        d.add_heading(pid.upper(),2);d.add_paragraph('Question: '+q);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Release gate',1)
    d.add_paragraph('Teacher verification, accessible desktop and mobile browser acceptance, and mathematically equivalent answer scoring remain required before publication.')
    OUT.parent.mkdir(parents=True,exist_ok=True);d.save(OUT)
    payload=dict(id='g8-functions-relationships-02',title='Equivalent forms of a relationship',source_document=SOURCE,
        source_sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),worked_examples=E,practice_questions=P,
        mastery_questions=M,reassessment_questions=R)
    JSON.parent.mkdir(parents=True,exist_ok=True)
    JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{OUT}: sha256 {payload["source_sha256"]}, {len(E)} worked, {len(P)} practice')

if __name__=='__main__':build()
