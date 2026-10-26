"""Original Grade 8 rule-finding source: progressively authored table investigations."""
import hashlib
import json
from pathlib import Path

from docx import Document
from docx.shared import Pt

ROOT=Path(__file__).resolve().parents[1]
SOURCE='Project_Athena_Grade8_Functions_Relationships_Lesson3_Source_Pack_v1.docx'
OUT=ROOT/'docs/curriculum/grade8/functions-relationships'/SOURCE
JSON=ROOT/'backend/app/curriculum/grade8/generated/functions_relationships_03.json'
SOURCES=[('DBE CAPS Mathematics Grades 7–9','https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf'),
 ('DBE Grade 8 Mathematics 2026 ATP','https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208')]

def ex(n,level,marks,skill,q,answer,family,rows,given,derived,states,moves,verify,mistake,repair):
    assert len(states)==len(moves)+1 and len(set(states))==len(states),(n,states)
    assert 2<=len(given)<=5 and 1<=len(derived)<=4
    assert 2<=len(rows)<=5 and all(len(r)==2 and isinstance(r[0],int) and (r[1] is None or isinstance(r[1],int)) for r in rows)
    return dict(id=f'g8-fr-l03-w{n:02}',number=n,level=level,marks=marks,skill=skill,q=q,answer=answer,
        model={'family':family,'inputs':given,'outputs':derived,'rows':rows,'description':skill},
        states=states,steps=[dict(title=t,action=a,narration=v) for t,a,v in moves],
        verify=verify,misconception=mistake,repair=repair)

E=[
 ex(1,'foundation',2,'Follow a constant difference','Table: x=0,1,2; y=2,3,4. Give a simple matching rule and output at x=3.',
  'A matching rule is y=x+2; at x=3, y=5.','rule_difference',[(0,2),(1,3),(2,4),(3,None)],['0→2','1→3','2→4'],['change +1','rule x+2','3→5'],
  ['Each input step is one','Output rises by one each row','At input zero, output is two','Use y=x+2 to get five at x=3'],
  [('Compare adjacent rows','Mark plus one between both adjacent input and output rows.','The input and output change at the same rate.'),('Find the starting value','Circle the row at input zero.','Two is the constant amount added.'),('Extend the rule','Send three through add two.','The next output is five.')],
  'x+2 gives 2,3,4,5 on inputs 0,1,2,3.','Copying an output without relating it to input.','Highlight changes between successive rows.'),
 ex(2,'easy',3,'Recognise a decreasing rule','Table: x=0,1,2,3; y=10,7,4,1. Give a simple matching rule.',
  'A matching rule is y=10−3x.','rule_difference',[(0,10),(1,7),(2,4),(3,1)],['0→10','1→7','2→4','3→1'],['change −3','rule 10−3x'],
  ['Outputs 10,7,4,1','Every input plus one changes output by minus three','At zero, output is ten','Rule y=10−3x'],
  [('Follow down the table','Record a decrease of three for each unit input increase.','The rate is negative three.'),('Mark input zero','Ten is the output before any input steps.','This is the starting value.'),('Write and test','Start at ten and subtract three x.','At x=3 the result is one.')],
  'At x=0,1,2,3 the proposed rule gives 10,7,4,1.','Writing 10+3x even though outputs decrease.','Use directed minus-three arrows.'),
 ex(3,'easy',3,'Handle a negative input','Rule y=2x+5 has x=−2,0,2. Complete its table.',
  'Outputs are 1,5,9 respectively.','rule_signed',[(-2,None),(0,None),(2,None)],['x=−2','x=0','x=2','y=2x+5'],['−2→1','0→5','2→9'],
  ['Evaluate y=2x+5 on three inputs','At negative two: 2(−2)+5=1','At zero: 0+5=5','At two: 4+5=9'],
  [('Keep the sign','Insert negative two inside brackets.','Twice negative two is negative four.'),('Use zero','The multiplier term becomes zero.','This reveals the starting value five.'),('Use positive two','Twice two is four, then add five.','Nine completes the third row.')],
  '2(−2)+5=1; 2(0)+5=5; 2(2)+5=9.','Treating negative input as positive.','Keep the signed input in a visible substitution slot.'),
 ex(4,'standard',4,'Recover the zero row','A table shows x=1→7, 2→10, 3→13. Find a simple linear rule and its output at x=0.',
  'A matching linear rule is y=3x+4; at zero y=4.','rule_zero',[(0,None),(1,7),(2,10),(3,13)],['1→7','2→10','3→13'],['per step +3','zero row 4','rule 3x+4'],
  ['Each input plus one gives output plus three','Undo one step from x=1: 7−3=4 at x=0','A matching linear rule is y=3x+4','The zero output is four'],
  [('Measure the step','Compare seven and ten, then ten and thirteen.','Both gaps are plus three.'),('Step backwards','Subtract three from seven for the previous input zero.','The fixed part is four.'),('Check the rule','At x=1,2,3 formula gives 7,10,13.','All stated rows agree.')],
  '3(0)+4=4 and x=1,2,3 produce 7,10,13.','Assuming the first shown output is the intercept.','Insert the missing zero row explicitly.'),
 ex(5,'standard',4,'Account for unequal input spacing','Table: 0→3, 2→11, 4→19. Find a simple linear rule and output at x=3.',
  'A matching linear rule is y=4x+3; at x=3, y=15.','rule_difference',[(0,3),(2,11),(3,None),(4,19)],['0→3','2→11','4→19'],['2 input steps→8 output','per step +4','rule 4x+3','3→15'],
  ['Inputs jump by two; outputs jump by eight','One input step changes output by four','At zero the output is three','A matching rule is y=4x+3','At x=3 output is fifteen'],
  [('Compare both intervals','Each two-input gap adds eight output units.','Do not mistake eight for the per-one rate.'),('Divide by step width','Eight over two gives four per one input.','That is the rate.'),('Read the starting row','At zero output is three.','Add three after four times x.'),('Fill the missing row','At three, twelve plus three is fifteen.','It lies between outputs eleven and nineteen.')],
  'At x=0,2,3,4 the rule gives 3,11,15,19.','Treating an eight-output jump over two input units as slope eight.','Label both Δx and Δy arrows.'),
 ex(6,'standard',4,'Distinguish a proportional rule','Table: x=0,1,2,3; y=0,4,8,12. Give a simple rule and explain the zero row.',
  'A matching rule is y=4x; zero input gives zero output.','rule_zero',[(0,0),(1,4),(2,8),(3,12)],['0→0','1→4','2→8','3→12'],['per step +4','zero part 0','rule 4x'],
  ['Output grows by four for every unit input','At zero output is zero','A matching rule is y=4x','At three, four times three is twelve'],
  [('Find unit groups','One input adds four output units.','Each input contributes one group of four.'),('Check zero','No input groups give zero output.','There is no fixed extra amount.'),('Name the rule','Multiply any input by four.','Check all supplied rows.')],
  '4(0)=0,4(1)=4,4(2)=8,4(3)=12.','Adding four to every input instead of multiplying by four.','Represent input as a count of four-blocks.'),
 ex(7,'intermediate',5,'Identify square outputs','Table: x=0,1,2,3; y=0,1,4,9. Find a matching square rule and output at x=4.',
  'A matching rule is y=x²; at x=4 output 16.','rule_nonlinear',[(0,0),(1,1),(2,4),(3,9),(4,None)],['0→0','1→1','2→4','3→9'],['square blocks 0,1,4,9','rule x²','4→16'],
  ['Outputs are 0,1,4,9','These are square arrays of side x','A matching rule is y=x²','Four-by-four array has sixteen cells'],
  [('Build square arrays','Place a square array for each shown nonnegative x.','The counted cells are zero, one, four and nine.'),('Read the pattern','Each output is x multiplied by itself.','That gives a candidate square rule.'),('Extend to four','Count four rows of four cells.','The next output is sixteen.')],
  'x² at x=0,1,2,3,4 gives 0,1,4,9,16.','Assuming every table grows by a constant output step.','Compare square arrays and unequal differences.'),
 ex(8,'intermediate',5,'Identify a shifted square','Table: x=0,1,2,3; y=1,2,5,10. Suggest a simple rule and output at x=4.',
  'A matching rule is y=x²+1; at x=4 output 17.','rule_nonlinear',[(0,1),(1,2),(2,5),(3,10),(4,None)],['0→1','1→2','2→5','3→10'],['square counts 0,1,4,9','add one','rule x²+1','4→17'],
  ['Given outputs 1,2,5,10','Subtract one from each output: 0,1,4,9','These are square counts','Add one back: y=x²+1','At four: 16+1=17'],
  [('Peel off one','Remove a single fixed tile from each displayed output.','The remainders are zero, one, four and nine.'),('Recognise the squares','The remainders are input squared.','This is not a constant-step linear rule.'),('Restore the fixed tile','Add one to each square count.','The candidate rule is x squared plus one.'),('Extend','Four squared plus one is seventeen.','Verify the given rows too.')],
  'At x=0,1,2,3,4, x²+1 gives 1,2,5,10,17.','Taking the changing differences as a constant rate.','Show square blocks plus one separate fixed tile.'),
 ex(9,'intermediate',5,'Recognise underdetermination','Only 0→0 and 2→4 are shown. Both y=2x and y=x² fit. Are they necessarily the same rule?',
  'No; at x=1, 2x=2 while x²=1.','rule_choice',[(0,0),(2,4),(1,None)],['0→0','2→4','A=2x','B=x²'],['A(1)=2','B(1)=1','not the same'],
  ['Two shown rows agree with two candidates','At x=1, A gives two','At x=1, B gives one','The rules differ on an unshown input'],
  [('Choose a fresh input','Use one between the displayed zero and two.','Rows alone do not establish a unique general rule.'),('Test first candidate','Twice one is two.','Keep the same input for both candidates.'),('Test second candidate','One squared is one.','Different outputs are a counterexample.')],
  'At x=0,2 both agree; at x=1, 2≠1.','Claiming a short table uniquely proves a general formula.','Test another input or use the actual rule statement.'),
 ex(10,'exam',6,'Model a fixed fee table','A plan charges R12 once plus R3 per visit. Make a table for 0,2,5 visits and give C(n).',
  'C(n)=12+3n rand; costs R12,R18,R27.','rule_context',[(0,None),(2,None),(5,None)],['fixed R12','R3 per visit','n=0,2,5'],['C=12+3n','0→12','2→18','5→27'],
  ['One fee of twelve plus three per visit','C(n)=12+3n','At zero cost twelve','At two cost eighteen','At five cost twenty seven'],
  [('Separate the charges','Show twelve once and three for each visit.','The fixed charge does not repeat.'),('Write the formula','Add three n to twelve.','n counts visits.'),('Fill zero row','With no visits only the fixed fee remains.','Cost is twelve rand.'),('Fill two and five','Add six or fifteen rand to the fixed fee.','Costs are eighteen and twenty seven.')],
  '12+3(0)=12; 12+3(2)=18; 12+3(5)=27 rand.','Multiplying the fixed fee by visit count.','Keep fixed and repeated charges in separate lanes.'),
 ex(11,'exam',6,'Interpret a negative rate','The rule y=9−2x gives outputs at x=0,1,3. Fill the table and find y at x=5.',
  'Outputs at 0,1,3 are 9,7,3; at x=5, y=−1.','rule_signed',[(0,None),(1,None),(3,None),(5,None)],['rule 9−2x','x=0,1,3,5'],['outputs 9,7,3','5→−1'],
  ['The given formula is y=9−2x','Start nine; subtract two per unit input','At zero and one: 9 and 7','At three: 9−6=3','At five: 9−10=−1'],
  [('Show starting value','At zero the two x term is zero.','The output begins at nine.'),('Use one input step','Subtract two for x=1.','Output seven is lower than nine.'),('Jump three units','Three input units remove six from nine.','At three output is three.'),('Evaluate five','Five steps remove ten.','The mathematical output is negative one; no physical restriction was stated.')],
  'y(0)=9,y(1)=7,y(3)=3,y(5)=−1.','Rejecting a negative output despite no restricted context.','Follow the signed number line through zero.'),
 ex(12,'exam',6,'Reverse a formula row','For y=4x−3, what input produces output 17? Fill rows at x=0,2 and this input.',
  'x=5; rows 0→−3,2→5,5→17.','rule_zero',[(0,None),(2,None),(5,17)],['rule 4x−3','0→?','2→?','?→17'],['0→−3','2→5','17+3=20','x=5'],
  ['Given y=4x−3 with output seventeen','Reverse equation 4x−3=17','At zero output minus three','At two output five','Undo minus three: twenty','Undo multiply four: x=5'],
  [('Set up backward row','Write four x minus three equals seventeen.','The unknown is the input, not the output.'),('Fill zero','Four times zero minus three is negative three.','This reveals the starting row.'),('Fill two','Eight minus three is five.','The row is separate from the inverse task.'),('Undo subtraction','Add three to seventeen to get twenty.','Reverse the final flow arrow first.'),('Undo multiplication','Twenty divided by four is five.','Five is the input because four times five minus three equals seventeen.')],
  '4(5)−3=17; 4(0)−3=−3; 4(2)−3=5.','Dividing seventeen by four before undoing minus three.','Reverse the operation boxes right to left.'),
 ex(13,'advanced',7,'Reject a linear claim','Table: x=0,1,2,3; y=0,1,4,9. A learner says y=3x. Find the first mismatch and a better matching rule.',
  'At x=1 the claim predicts 3 but table says 1; a matching rule is y=x².','rule_nonlinear',[(0,0),(1,1),(2,4),(3,9)],['table 0,1,4,9','claim 3x'],['claim fails x=1','differences 1,3,5','rule x²'],
  ['Given outputs zero, one, four, nine; claim 3x','At zero, both candidate and table give zero','At one, proposed 3x gives three, table gives one','Output gaps are one, three, five','Squares of inputs match each shown row'],
  [('Do not trust the first row alone','Zero makes many different rules appear to agree.','Test the next row.'),('Find first mismatch','At x=1, three x equals three, not one.','The proposed rule is false.'),('Inspect changing gaps','Output differences are one, then three, then five.','A constant rate does not fit this table.'),('Test squares','Zero, one, four, nine are the displayed squares.','State a matching rule without claiming uniqueness from only four rows.')],
  '3(1)=3≠1; x² at 0,1,2,3 gives 0,1,4,9.','Accepting a rule because it matches at zero.','Check each row and name the first mismatch.'),
 ex(14,'advanced',7,'Find rate with nonunit gaps','Table: 0→2, 3→11, 5→17. Assuming a linear rule, find it and fill x=2.',
  'The linear rule is y=3x+2; at x=2 output 8.','rule_difference',[(0,2),(2,None),(3,11),(5,17)],['0→2','3→11','5→17'],['Δx=3,Δy=9','rate 3','zero value 2','2→8'],
  ['From zero to three, output rises nine','Nine divided by three is three per input','From three to five, six over two also gives three','At zero fixed part is two','At x=2, output is eight'],
  [('Compare first gap','Mark three input steps and nine output steps.','The per-input rate is not nine.'),('Confirm with another gap','Six output units over two input units again give three.','Both gaps support a linear rule.'),('Use zero row','At x=0, output two is the fixed part.','Rule is three x plus two.'),('Fill x=2','Three times two plus two is eight.','Check it lies between two and eleven.')],
  '3(0)+2=2; 3(3)+2=11; 3(5)+2=17; 3(2)+2=8.','Dividing only one output jump by no input width.','Draw matching input and output jump arrows.'),
 ex(15,'advanced',8,'Integrate signed and inverse rows','Assume a linear rule. Table 0→4,2→10,4→16. Find the rule, output at x=−1 and input for output 22.',
  'The linear rule is y=3x+4; −1→1; input 6 gives 22.','rule_choice',[(-1,None),(0,4),(2,10),(4,16)],['0→4','2→10','4→16','missing x=−1'],['rate 3','rule 3x+4','−1→1','22→6'],
  ['Given rows 0→4, 2→10, 4→16','From zero to two, output changes by six','Six over two gives rate three','At zero fixed part is four','At negative one: minus three plus four is one','For output 22: 22−4=18, divide by three gives six'],
  [('Measure both jumps','Every two-input step adds six output units.','Rate is three per unit input.'),('Read the zero row','Four is the value at input zero.','The linear rule is three x plus four.'),('Use signed substitution','Three times negative one plus four is one.','Protect the negative input in brackets.'),('Reverse the output','Subtract four from twenty two to get eighteen.','Undo the final addition first.'),('Recover input','Eighteen divided by three gives six.','Run six forward and get twenty two.')],
  '3(−1)+4=1; 3(6)+4=22; given rows also fit.','Using the output jump six as the per-one rate.','Label step width before calculating and verify both requested rows.'),
]

P=[
 ('p01','Table x=0,1,2 gives y=1,2,3. Give a simple fitting rule.','y=x+1.','Compare adjacent rows.','Each input step adds one; at zero output is one.'),
 ('p02','Table x=0,1,2 gives y=9,7,5. Give a simple fitting rule.','y=9−2x.','Outputs decrease by two.','At zero output nine; one step subtracts two.'),
 ('p03','For y=3x+2, give outputs at x=−1,0,1.','−1,2,5.','Substitute each signed input.','3(−1)+2=−1; 3(0)+2=2; 3(1)+2=5.'),
 ('p04','Table 1→8,2→11,3→14. Assuming linear, find the rule and zero row.','y=3x+5; zero→5.','Step backward once.','The output rises three per input and at zero is five.'),
 ('p05','Table 0→1,2→11,4→21. Assuming linear, find the rule.','y=5x+1.','Divide output gap by input gap.','Ten over two gives five per input; at zero output one.'),
 ('p06','Table 0→0,1→6,2→12. Give a simple proportional rule.','y=6x.','Read group size.','Each input contributes six, and zero contributes zero.'),
 ('p07','Table 0→0,1→1,2→4,3→9. Give a matching square rule and output at four.','y=x²; output 16.','Visualise square arrays.','Four groups of four give sixteen.'),
 ('p08','Table 0→2,1→3,2→6,3→11. Give a simple matching rule.','y=x²+2.','Remove the fixed two.','The remaining outputs 0,1,4,9 are squares.'),
 ('p09','The rows 0→0,3→9 fit y=3x and y=x². Show these are not the same rule.','At x=1, outputs 3 and 1 differ.','Use a new shared input.','3(1)=3 but 1²=1.'),
 ('p10','Club fee R5 once plus R4 per visit. Give C(n) and table at n=0,2,4.','C(n)=5+4n; 5,13,21 rand.','Separate fixed and repeated charges.','5+4(0)=5,5+4(2)=13,5+4(4)=21.'),
 ('p11','For y=6−3x, fill outputs at 0,2,3.','6,0,−3.','The output may be negative.','At x=0,2,3 the rule yields six, zero, minus three.'),
 ('p12','For y=5x−2, what input produces output 18?','x=4.','Undo minus two first.','18+2=20; 20÷5=4; 5(4)−2=18.'),
 ('p13','Table 0→1,1→2,2→5,3→10. Reject y=2x+1 using the first mismatch and suggest a better matching rule.','At x=2, claim gives 5 (matches); at x=1, claim gives 3 but table says 2; y=x²+1 fits.','Check the first nonzero row.','At one claim three differs from two; squares plus one match all rows.'),
 ('p14','Table 0→5,3→11,5→15. Assuming linear, find rule and output at x=2.','y=2x+5; output 9.','Use both jump widths.','Six over three and four over two both give rate two.'),
 ('p15','Assume linear: 0→3,2→9,4→15. Find rule, output at x=−2, and input for output 24.','y=3x+3; −2→−3; output 24 comes from input 7.','Divide six by two, then reverse.','3(−2)+3=−3; (24−3)÷3=7.'),
]
M=[
 ('m01',2,'Table 0→4,1→6,2→8. Give a simple matching rule.','y=2x+4.','Two output units per one input; starting output four.'),
 ('m02',3,'Table 1→9,2→13,3→17. Assuming linear, find rule and zero row.','y=4x+5; zero→5.','Four per input; step back from nine to five.'),
 ('m03',4,'Table 0→2,2→10,4→18. Assuming linear, give rule and output at x=3.','y=4x+2; at x=3 output 14.','Eight output units over two input units gives four per input.'),
 ('m04',5,'Table 0→1,1→2,2→5,3→10. Find a square-based rule, give output at x=4 and reject y=3x+1 at the first mismatch.','y=x²+1; at x=4 output 17; y=3x+1 fails at x=1, predicting 4 rather than 2.','Subtract one and recognise squares; test first positive input.'),
 ('m05',6,'Assuming linear, table 0→6,2→12,4→18. Find rule, output at −1, input for output 27, and check all given rows.','y=3x+6; −1→3; output 27 comes from input 7; rows 6,12,18 agree.','Rate six over two is three; subtract six and divide three to reverse 27.'),
]
R=[
 ('r01','Table 0→7,1→9,2→11. Give a simple fitting rule.','y=2x+7.','Two per input and starting value seven.'),
 ('r02','Assuming linear: table 0→1,3→10,5→16. Find rule and output at x=2.','y=3x+1; at x=2 output 7.','Nine over three and six over two give rate three.'),
 ('r03','For y=4x−5, find output at x=−1 and input for output 15.','−9 and input 5.','4(−1)−5=−9; undo minus five then multiply four: (15+5)÷4=5.'),
]

def build():
    assert len(E)==len(P)==15 and len(M)==5 and sum(row[1] for row in M)==20 and len(R)==3
    d=Document();d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(11)
    d.add_heading('Grade 8 Functions and Relationships — Lesson 3',0)
    d.add_heading('Finding and Testing Rules from Tables',1)
    d.add_paragraph('Original authoring draft for teacher review. This lesson advances beyond following or translating a supplied rule: learners construct a candidate from table evidence, attend to input step width, distinguish decreasing and square patterns, test proposed rules, and reverse a rule to recover an input. A finite table does not uniquely determine a formula unless a rule family is specified.')
    d.add_heading('Curriculum scope and references',1)
    for title,url in SOURCES:d.add_paragraph(f'{title}: {url}')
    d.add_heading('Teaching sequence and whiteboard contract',1)
    d.add_paragraph('Prerequisites: Lessons 1 and 2, signed number operations and square numbers. Align input and output rows. Display both Δx and Δy before calculating change per one input. Mark the zero row, preserve signed substitutions and units, construct actual question-specific table and difference arrows, conceal new rows and answers until their operation, then verify against every supplied row. Explain when data support a candidate rather than proving uniqueness.')
    d.add_heading('Fifteen worked examples with individual visual actions',1)
    for item in E:
        d.add_heading(f"Example {item['number']}: {item['skill']}",2)
        d.add_paragraph(f"{item['level']} · {item['marks']} marks · {item['model']['family']}")
        d.add_paragraph('Problem: '+item['q'])
        d.add_paragraph('Input-output cells: '+'; '.join(f'{x}→{y if y is not None else "hidden"}' for x,y in item['model']['rows']))
        d.add_paragraph('Given semantic objects: '+'; '.join(item['model']['inputs']))
        d.add_paragraph('Derived objects hidden initially: '+'; '.join(item['model']['outputs']))
        d.add_paragraph('Initial state: '+item['states'][0])
        for i,step in enumerate(item['steps']):
            d.add_paragraph(f"Step {i+1}: {step['title']}. Show operation: {step['action']} Reveal result: {item['states'][i+1]}. Narration and caption: {step['narration']}")
        d.add_paragraph('Answer: '+item['answer']+' Check all original rows: '+item['verify'])
        d.add_paragraph('Misconception: '+item['misconception']+' Repair: '+item['repair'])
    d.add_heading('Fifteen independent practice questions',1)
    for pid,q,a,h,memo in P:
        d.add_heading(pid.upper(),2);d.add_paragraph('Problem: '+q);d.add_paragraph('Hint: '+h);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Five mastery questions, twenty marks',1)
    for pid,marks,q,a,memo in M:
        d.add_heading(f'{pid.upper()} — {marks} marks',2);d.add_paragraph('Problem: '+q);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Three parallel reassessments',1)
    for pid,q,a,memo in R:
        d.add_heading(pid.upper(),2);d.add_paragraph('Problem: '+q);d.add_paragraph('Answer: '+a);d.add_paragraph('Memo: '+memo)
    d.add_heading('Release checks',1)
    d.add_paragraph('Teacher verification, equivalent-answer scoring, desktop and mobile browser acceptance and caption inspection remain before publication.')
    OUT.parent.mkdir(parents=True,exist_ok=True);d.save(OUT)
    payload=dict(id='g8-functions-relationships-03',title='Finding and testing rules from tables',source_document=SOURCE,
        source_sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),worked_examples=E,practice_questions=P,
        mastery_questions=M,reassessment_questions=R)
    JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{len(E)} worked, {len(P)} practice, source {payload["source_sha256"]}')

if __name__=='__main__':build()
