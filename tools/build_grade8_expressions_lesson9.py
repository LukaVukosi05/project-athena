"""Original representations and contexts pack; the DOCX is the authored source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson9_Source_Pack_v1.docx'
JSON = ROOT/'backend/app/curriculum/grade8/generated/algebraic_expressions_09.json'
SOURCES = [
 ('DBE Grade 8 Mathematics 2026 Annual Teaching Plan','https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208'),
 ('DBE CAPS Mathematics Grades 7–9','https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf'),
]

def ex(n,level,marks,skill,q,answer,family,tokens,states,moves,verify,mistake,repair,inputs=2):
    assert len(states)==len(moves)+1 and len(states)>=3 and len(set(states))==len(states)
    assert 1<=inputs<len(tokens)<=8
    return dict(id=f'g8-ex-l09-w{n:02}',number=n,level=level,marks=marks,skill=skill,q=q,
      answer=answer,model={'family':family,'tokens':tokens,'description':skill,'scene':{'input_count':inputs}},
      states=states,steps=[dict(title=a,action=b,narration=c) for a,b,c in moves],
      verify=verify,misconception=mistake,repair=repair)

E=[
 ex(1,'foundation',2,'Turn words into a rule','A library charges R4 per printed page. Write the cost for n pages.','C=4n rand.','unit_receipt',['n pages','R4 each','C=4n'],
    ['n pages at R4 each','n equal groups of R4','C=4n rand'],[('Count equal groups','Place one four-rand tile under each page.','The number of pages tells us how many copies of four rand to use.'),('Name the cost','Multiply four by n.','The answer is a cost in rand, not a page count.')],
    'For n=3, three pages cost R12; 4(3)=12.','Writing 4+n instead of four per page.','Draw one price tile for every page.'),
 ex(2,'easy',3,'Add a fixed charge once','A delivery costs R10 plus R3 per kilometre. Write the cost for k kilometres.','C=10+3k rand.','fixed_variable_receipt',['fixed R10','k km','R3 each km','C=10+3k'],
    ['Fixed R10; R3 for each of k km','Variable part is 3k','C=10+3k rand'],[('Build the distance part','Give every kilometre its three-rand tile.','Three times k varies with distance.'),('Attach the one fixed charge','Add ten rand once to the variable total.','The starting fee does not repeat for every kilometre.')],
    'For k=2, R10+R6=R16 and 10+3(2)=16.','Multiplying the fixed R10 by k.','Place the fixed tile outside the repeated kilometres.',3),
 ex(3,'easy',3,'Read a two-operation flow diagram','A flow machine doubles x, then adds 5. Write its output rule and find the output for x=3.','y=2x+5; at x=3, y=11.','flow_rule',['input x','×2','+5','y=2x+5','x=3 → 11'],
    ['x → double → add 5','x → 2x → 2x+5','y=2x+5','At x=3: y=11'],[('Follow the first arrow','Doubling x gives two x.','The first action is multiplication.'),('Follow the second arrow','Add five after doubling.','Operation order matters; add five only at the end.'),('Try a concrete input','Three doubles to six, then plus five is eleven.','The rule and diagram agree for this input.')],
    'x=3: 3→6→11; 2(3)+5=11.','Writing 2(x+5) despite add being second.','Trace the arrows in their stated order.',3),
 ex(4,'standard',4,'Infer a rule from a table','A table pairs x=1,2,3 with y=5,8,11. Write a linear rule and test x=4.','y=3x+2; y=14 at x=4.','input_table',['1 → 5','2 → 8','3 → 11','increase +3','y=3x+2','4 → 14'],
    ['(1,5), (2,8), (3,11)','Each input +1 raises output by 3','At x=1: 3(1)+2=5','y=3x+2','At x=4: y=14'],[('Compare successive rows','Each next output rises by three when x rises by one.','The variable contribution is three per input unit.'),('Find the fixed offset','At x one, three plus two makes five.','The offset is two, not five.'),('Write the complete rule','Combine three x with the two-unit start.','Check all three given rows.'),('Extend one row','At four the output is twelve plus two.','The new row tests the proposed rule.')],
    'x=1,2,3,4 gives 5,8,11,14 under y=3x+2.','Taking 5 as the starting amount at x=0.','Run the three-times part backward to zero.',3),
 ex(5,'standard',4,'Match words to a table','Tickets cost R6 each plus one booking fee of R4. Write C(t), then fill costs for t=1,2,3.','C(t)=6t+4; costs R10, R16, R22.','fare_table',['R6 per ticket','booking fee R4','t=1','t=2','t=3','C=6t+4; 10,16,22'],
    ['t tickets; R6 each plus R4 once','Variable ticket cost: 6t','C(t)=6t+4','C(1)=10; C(2)=16','C(3)=22'],[('Model each ticket','Six times t gives the changing ticket total.','The number of tickets controls only this part.'),('Attach the booking fee','Add four once after ticket cost.','It is charged for the whole booking.'),('Fill first two table rows','At one ticket pay ten; at two pay sixteen.','Each additional ticket raises the bill by six.'),('Fill the third row','Eighteen plus four is twenty two.','Check the six-rand increase continues.')],
    'For t=3, three R6 tickets cost R18 plus R4 fee = R22.','Adding R4 to every ticket.','Keep the fee tile separate from ticket columns.',5),
 ex(6,'standard',4,'Describe a decreasing rule','A tank starts with 30 L and loses 2 L each minute. Write V(m) and find V(5). State a sensible domain.','V=30-2m litres; V(5)=20 L; 0≤m≤15.','decrease_timeline',['start 30 L','lose 2 L per min','m minutes','V=30-2m','m=5 → 20 L','0≤m≤15'],
    ['Tank 30 L; lose 2 L/min','Total loss after m minutes is 2m L','V(m)=30-2m L','At m=5: V=20 L','Empty at m=15; 0≤m≤15'],[('Accumulate the loss','Two litres leave in each minute, for m minutes.','The loss is two m litres.'),('Subtract loss from the start','Thirty minus two m is the remaining volume.','A loss lowers the total.'),('Substitute five minutes','Thirty minus ten leaves twenty litres.','Units remain litres.'),('Bound the time','After fifteen minutes the model reaches zero.','Negative time or negative physical volume is outside this scenario.')],
    'Five losses of 2 L give 30−10=20 L; 15 losses give 0 L.','Adding a loss or accepting a negative tank volume.','Animate each two-litre loss from the starting bar.',3),
 ex(7,'intermediate',5,'Model repeated groups with an extra','A school buys p packs of 6 pencils and 4 loose pencils. Write the total and find it for p=3.','N=6p+4 pencils; N(3)=22 pencils.','packs_plus_loose',['p packs','6 in each','4 loose','N=6p+4','p=3 → 22'],
    ['p groups of 6 and four loose','Pack count gives 6p pencils','N=6p+4 pencils','At p=3: N=22 pencils'],[('Count pack pencils','Each of p packs contains six pencils.','Multiply six by the pack count.'),('Add loose pencils once','The four loose pencils are outside the packs.','They are not four in each pack.'),('Try three packs','Eighteen packed plus four loose is twenty two.','Count the diagram independently.')],
    '3 packs ×6=18; 18+4=22 pencils.','Multiplying the four loose pencils by p.','Keep loose pencils visually outside the pack boundaries.',3),
 ex(8,'intermediate',5,'Build a perimeter expression','A rectangle has length (x+3) cm and width x cm. Write a simplified perimeter rule and find P at x=4.','P=4x+6 cm; P(4)=22 cm.','context_perimeter',['top x+3 cm','right x cm','bottom x+3 cm','left x cm','P=4x+6 cm','x=4 → 22 cm'],
    ['Rectangle sides x+3, x, x+3, x','P=(x+3)+x+(x+3)+x','P=4x+6 cm','At x=4: P=22 cm'],[('Trace each side','Two sides are x plus three and two sides are x.','Perimeter follows the whole boundary.'),('Collect like terms','Four x pieces and two threes give four x plus six.','Do not leave out the opposite side.'),('Measure at four','Two sevens and two fours total twenty two centimetres.','Check the simplified rule gives the same length.')],
    'At x=4 sides are 7,4,7,4 cm; total 22 cm; 4(4)+6=22.','Using area or only two sides.','Trace four edges with distinct markers.',4),
 ex(9,'intermediate',5,'Compare two prices without solving','Plan A costs R20 plus R5 per visit; Plan B costs R8 per visit. Write both rules and compare for 4 visits.','A(v)=20+5v, B(v)=8v; at v=4, A=R40 and B=R32, so B costs R8 less.','plan_comparison',['A fixed R20','A R5 per visit','B R8 per visit','v=4','A=20+5v; B=8v','A R40; B R32'],
    ['Plan A fixed 20 + 5v; B=8v','A(v)=20+5v; B(v)=8v','At v=4: A=20+20=40','At v=4: B=32; B costs R8 less'],[('Build each plan separately','A has a start fee plus visit fees; B has only visit fees.','Do not mix charges from different plans.'),('Calculate A for four','Four visits add twenty rand to the twenty-rand fee.','Plan A is forty rand.'),('Calculate B and compare','Four times eight is thirty two; the difference is eight rand.','This comparison is for four visits only.')],
    'At 4 visits, A=20+4×5=40 and B=4×8=32; 40−32=8.','Claiming one plan is always cheaper from one input.','Keep parallel plan lanes and label the input.',4),
 ex(10,'exam',5,'Diagnose a repeated fee','A taxi charges R12 once and R4 per kilometre. A learner writes T(d)=16d. Find the first mistake and write the correct rule.','The learner repeated the R12 fixed fee; T(d)=12+4d.','fee_error',['once R12','R4 per km','claim T=16d','T=12+4d'],
    ['Taxi R12 once + R4/km; claim 16d','R12 is one fixed tile, not d tiles','Distance part is 4d','Correct T(d)=12+4d'],[('Inspect the learner rule','Sixteen d multiplies both fee and distance by d.','The R12 start charge does not repeat.'),('Rebuild the changing part','Only four rand per kilometre becomes four d.','Distance controls the variable part.'),('Place the one-off fee','Attach twelve once to four d.','The corrected expression is twelve plus four d.')],
    'At d=2, taxi costs R12+R8=R20; claim 16(2)=R32.','Combining fixed and per-unit prices before multiplying.','Move the fixed tile outside the distance row.',3),
 ex(11,'exam',5,'Compare equivalent verbal and formula rules','A savings rule says “start with R7 and add R5 each week”. Another says S(w)=5(w+1)+2. Are the rules equivalent for every w?','Yes; both give S(w)=5w+7.','equivalence_models',['start R7','R5 per week','5(w+1)+2','5w+7'],
    ['Words: start 7, add 5 weekly; formula 5(w+1)+2','Verbal path: 7+5w; formula: 5(w+1)+2','Distribute formula: 5w+5+2','Both simplify to 5w+7'],[('Build the verbal path','The start is seven and each week adds five.','Seven is a fixed amount.'),('Expand the formula path','Five multiplies w and one, then two remains.','Five multiplies both w and one, so the formula becomes five w plus five plus two.'),('Compare general expressions','Five w plus seven appears in both paths.','The rules agree for every permitted week count.')],
    'At w=2 both give R17; distribution proves equality for every w.','Treating one matching week as proof for all weeks.','Show the symbolic expansion before a numerical check.',3),
 ex(12,'exam',6,'Translate a table with a missing input','A shop charges R9 once plus R3 per item. Complete the total for 2, 4 and n items, then find the total for n=7.','2 items R15; 4 items R21; n items R(9+3n); 7 items R30.','general_table',['R9 once','R3 each','2 items','4 items','n items','15,21,9+3n,30'],
    ['Start 9; add 3 for each item','T(n)=9+3n','T(2)=15; T(4)=21','T(7)=30'],[('Make the general rule','The one-off nine stays outside the three-per-item term.','A letter can stand for any item count.'),('Fill two concrete rows','Two items add six, four items add twelve.','Each row applies the same rule.'),('Test seven items','Nine plus twenty one equals thirty.','Check the three-rand steps from the table.')],
    'T(2)=9+6=15; T(4)=9+12=21; T(7)=9+21=30.','Mistaking the R9 for a per-item price.','Keep the fixed-fee column separate.',5),
 ex(13,'exam',6,'Model area without confusing units','A rectangular garden has length (x+2) m and width 3 m. Write and simplify its area; find area when x=4.','A=3(x+2)=3x+6 m²; A(4)=18 m².','split_area_context',['length x+2 m','width 3 m','3×x region','3×2 region','A=3x+6 m²','x=4 → 18 m²'],
    ['Length x+2 m, width 3 m','Split area into 3×x and 3×2','A=3x+6 m²','At x=4: A=18 m²'],[('Split the length','Partition the rectangle into x metres and two metres.','Both regions share the three-metre width.'),('Calculate both regions','Areas are three x and six square metres.','Area units are square metres, not metres.'),('Test at four','Length is six metres, so three times six is eighteen square metres.','The split regions give twelve plus six.')],
    'At x=4, full rectangle 6×3=18 m²; split 12+6=18 m².','Using perimeter or writing 3x+2.','Shade both 3×x and 3×2 regions.',2),
 ex(14,'advanced',7,'Distinguish two flows with the same inputs','Machine A adds 4 then doubles; Machine B doubles then adds 4. Write both rules and compare outputs at x=5.','A(x)=2(x+4)=2x+8, B(x)=2x+4; A(5)=18, B(5)=14.','parallel_flows',['A +4 then ×2','B ×2 then +4','input x=5','A=2x+8','B=2x+4','18 vs 14'],
    ['A: x→+4→×2; B: x→×2→+4','A(x)=2(x+4); B(x)=2x+4','A(x)=2x+8; B(x)=2x+4','At x=5: A=18 and B=14'],[('Trace each arrow order','A doubles the whole x plus four; B adds four after doubling.','Operations in different orders give different rules.'),('Expand A only','Two multiplies x and four, producing two x plus eight.','B stays two x plus four.'),('Compare at five','A: five plus four, doubled, is eighteen; B: ten plus four is fourteen.','The outputs differ by four for this input.')],
    'At x=5 A=2(9)=18; B=2(5)+4=14.','Assuming addition and doubling commute.','Keep two labelled machines side by side.',3),
 ex(15,'advanced',8,'Integrate table, context and representation','A fundraiser sells b booklets at R6 each, plus one R15 donation. Give F(b), fill totals for b=0,2,5, and check the claim F(b)=6(b+15).','F(b)=6b+15; table totals R15, R27, R45; claim invalid.','fundraiser_audit',['booklets b at R6','one donation R15','b=0,2,5','claim 6(b+15)','F=6b+15','15,27,45'],
    ['R6 per booklet plus one R15 gift','F(b)=6b+15','F(0)=15; F(2)=27; F(5)=45','Claim 6(b+15)=6b+90','Claim invalid; fixed gift is R15 once'],[('Separate variable and fixed parts','Six times the booklet count changes; the fifteen-rand donation stays once.','The donation is not in every booklet.'),('Fill the three input rows','Zero booklets still leaves fifteen rand; two yield twenty seven, five yield forty five.','Use the same rule each time.'),('Inspect the proposed bracket','Six times fifteen would count ninety rand of donation.','This is the first mismatch with the context.'),('State the corrected conclusion','Six b plus fifteen fits all three rows and the original story.','A contextual reason and table both reject the claim.')],
    'At b=0 true total R15 while claim gives R90; at b=5 true total R45.','Multiplying the one donation by every booklet.','Place the gift as one separate tile before forming the rule.',4),
]
P=[
 ('p01','R7 per badge: write cost for n badges.','7n rand','Repeat the R7 unit price.','n badges at R7 each cost R7n.'),
 ('p02','A van costs R15 to start and R2 per kilometre. Write C(k).','15+2k rand','Keep the start fee once.','C(k)=15+2k rand.'),
 ('p03','A machine triples x then adds 2. Give the rule and output for x=4.','3x+2; output 14','Trace arrows in order.','x→3x→3x+2; at x=4, y=14.'),
 ('p04','A table has (1,6),(2,10),(3,14). Give y(x) and y(4).','y=4x+2; y(4)=18','Outputs rise by four.','At x=1, 4+2=6; y=4x+2 and y(4)=18.'),
 ('p05','R5 per snack plus a single R3 bag fee. Give C(s) and C(2).','C=5s+3; C(2)=R13','Bag fee stays outside repetitions.','C(s)=5s+3; C(2)=10+3=13.'),
 ('p06','A bottle starts with 24 L and loses 3 L each hour. Give V(h), V(2), and sensible h-domain.','V=24-3h L; V(2)=18 L; 0≤h≤8','Find when it reaches zero.','24-3(2)=18; 24-3(8)=0.'),
 ('p07','There are q packs of 4 pens and 3 loose pens. Give N(q), N(5).','N=4q+3; N(5)=23','Count loose pens once.','4(5)+3=23.'),
 ('p08','A rectangle length x+2 cm, width x cm. Give perimeter P(x), P(3).','P=4x+4 cm; P(3)=16 cm','Trace all four sides.','(x+2)+x+(x+2)+x=4x+4; at x=3, 16 cm.'),
 ('p09','Plan A is R12+R4 per visit; B is R7 per visit. Give both costs at 3 visits.','A=R24; B=R21','Keep plans in separate lanes.','A(3)=12+4(3)=24; B(3)=7(3)=21.'),
 ('p10','R9 once and R5 per km; learner writes 14d. Correct the rule.','9+5d rand','Only the per-km cost repeats.','R9 once plus R5d; at d=2 correct R19, claim R28.'),
 ('p11','Compare “R8 start and R3 a week” with 3(w+2)+2. Equivalent?','Yes; both equal 3w+8','Expand both paths.','3(w+2)+2=3w+6+2=3w+8.'),
 ('p12','R6 once plus R4 per item. Find totals for 1,3,n,5 items.','R10, R18, R(6+4n), R26','Keep one fixed fee.','T(n)=6+4n; T(1)=10,T(3)=18,T(5)=26.'),
 ('p13','Rectangle length x+3 m and width 2 m. Give area and value at x=5.','A=2x+6 m²; at x=5, 16 m²','Split into two regions.','2(x+3)=2x+6; at 5, 2(8)=16 m².'),
 ('p14','A adds 3 then triples; B triples then adds 3. Give A(2),B(2).','A(2)=15; B(2)=9','Keep operation order.','A=3(x+3)=3x+9, B=3x+3; at 2, 15 and 9.'),
 ('p15','Fundraiser sells n cards at R8 each plus one R10 gift. Give totals at n=0,2,4; reject 8(n+10).','R10,R26,R42; claim invalid','Separate the gift from cards.','F(n)=8n+10; at 0,2,4 totals 10,26,42; 8(n+10) gives 80 at n=0.'),
]
M=[
 ('m01',2,'R5 per item: write price for n items.','5n rand','Cost is five repeated n times.'),
 ('m02',3,'A flow doubles x then subtracts 3. Give rule and y at x=5.','y=2x-3; y(5)=7','x→2x→2x−3; at five, ten minus three equals seven.'),
 ('m03',4,'Table inputs 1,2,3 give outputs 7,11,15. Give rule and output at 4.','y=4x+3; y(4)=19','Difference four; at x=1 offset three; outputs 7,11,15,19.'),
 ('m04',5,'A rectangle has length x+4 cm and width 2 cm. Give simplified area and perimeter at x=3.','A=2x+8 cm²; P=2x+12 cm; at x=3, A=14 cm² and P=18 cm','A=2(x+4)=2x+8; P=2[(x+4)+2]=2x+12; at x=3, length 7, area 14 and perimeter 18.'),
 ('m05',6,'Plan A charges R18 once plus R3 per visit. Plan B charges R6 per visit. Write both rules and compare at 4 visits. Explain why one input does not show the cheaper plan for every visit count.','A(v)=18+3v; B(v)=6v; at 4, A=R30, B=R24, B is R6 cheaper; one input is not a universal comparison.','At 4: A=18+12=30, B=24; at 10: A=48, B=60, so the relative price changes.'),
]
R=[
 ('r01','R4 per pencil and one R2 fee: give cost for n pencils and for n=3.','4n+2 rand; R14 at n=3','Each pencil costs four; add the single fee two: 4(3)+2=14.'),
 ('r02','Flow subtracts 2 from x then triples. Give rule and output at x=6.','3(x-2)=3x-6; output 12','x→x−2→3(x−2); at six, 3(4)=12.'),
 ('r03','R7 per booklet and one R9 gift: fill fundraiser totals for b=0,2,4; reject 7(b+9).','R9,R23,R37; claim invalid','F(b)=7b+9; at 0,2,4 gives 9,23,37; wrong claim gives R63 at b=0.'),
]


def build():
    doc=Document();sec=doc.sections[0];sec.top_margin=sec.bottom_margin=Inches(.7);sec.left_margin=sec.right_margin=Inches(.75)
    style=doc.styles['Normal'];style.font.name='Arial';style.font.size=Pt(10);style.paragraph_format.space_after=Pt(5)
    doc.add_heading('Grade 8 Algebraic Expressions | Lesson 9',0)
    doc.add_paragraph('Representing rules across words, tables, flow diagrams and contexts. Original Athena teaching source v1; teacher review required.')
    doc.add_paragraph('Fifteen worked examples, fifteen independent questions, five mastery questions (20 marks), and three parallel reassessments are authored here. The runtime loads these records; it does not generate questions with AI.')
    doc.add_heading('Curriculum and lesson method',1)
    for title,url in SOURCES: doc.add_paragraph(f'{title}: {url}')
    doc.add_paragraph('Prerequisites: lessons 1–8 on expressions, products, division and substitution. The 2026 Grade 8 ATP asks learners to compare verbal rules, flow diagrams, tables, formulae and number sentences. All examples below are original, modelled on the curriculum scope rather than copied from source questions.')
    doc.add_paragraph('Modelling routine: name the varying quantity and its unit; mark each fixed amount once; show each operation in the order the story applies it; build a formula and use input-output pairs to check it. Compare equivalent forms generally. Keep every completed state visible and conceal derived outputs until their mathematical operation is taught. Do not confuse an expression with an equation to solve.')
    doc.add_heading('Progression matrix and authored whiteboards',1)
    for item in E:
        doc.add_heading(f"Example {item['number']}: {item['skill']}",2)
        doc.add_paragraph(f"Level {item['level']} | Cognitive progression | {item['marks']} marks | Scene {item['model']['family']}")
        doc.add_paragraph('Question: '+item['q'])
        doc.add_paragraph('Given visual objects: '+'; '.join(f"token-{i+1} = {token}" for i,token in enumerate(item['model']['tokens'][:item['model']['scene']['input_count']]))+'. Output objects are concealed at first.')
        doc.add_paragraph('Initial state: '+item['states'][0])
        for index,step in enumerate(item['steps']):
            doc.add_paragraph(f"Board step {index+1} — {step['title']}. Operation shown first: {step['action']} Result revealed after the operation: {item['states'][index+1]}. Caption and narration: {step['narration']}")
        doc.add_paragraph('Final answer: '+item['answer']+' Check in original: '+item['verify'])
        doc.add_paragraph('First-error diagnosis: '+item['misconception']+' Targeted repair: '+item['repair'])
    doc.add_heading('Independent questions: answer only after submission',1)
    for pid,q,a,hint,memo in P:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Hint: '+hint);doc.add_paragraph('Worked memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Mastery check | 20 marks',1)
    for pid,marks,q,a,memo in M:
        doc.add_heading(f'{pid.upper()} | {marks} marks',2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Worked memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Parallel reassessment',1)
    for pid,q,a,memo in R:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Worked memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Release gates',1)
    doc.add_paragraph('Teacher must review each rule, unit, input-output pair, diagram label, target, narration, independent-attempt gate, desktop and mobile presentation. Equivalent expressions and short-text answers need robust scoring before release approval.')
    OUT.parent.mkdir(parents=True,exist_ok=True);doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-09','title':'Representations and contextual expressions','source_document':OUT.name,'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'worked_examples':E,'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True);JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(OUT,JSON,payload['source_sha256'],sep='\n')

if __name__=='__main__':build()
