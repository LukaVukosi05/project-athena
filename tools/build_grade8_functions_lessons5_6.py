"""Original, question-specific Grade 8 functions lessons 5 and 6."""
import ast
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'backend/app/curriculum/grade8'
DOCS=ROOT/'docs/curriculum/grade8/functions-relationships'
CAPS='https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf'
# level, marks, question, given representations, x, candidate rules (name, a, b, c),
# correct rule, answer, misconception, repair. Rule means ax²+bx+c.
FIVE=[
('foundation',2,'Words say double an input then add 1. Does y=2x+1 or y=2(x+1) match? Test x=2.',['double, then add 1','y=2x+1','y=2(x+1)'],2,[('2x+1',0,2,1),('2(x+1)',0,2,2)],'2x+1','2x+1; at x=2, y=5','Grouping the +1 inside the doubling.','Perform the operations in the spoken order.'),
('easy',2,'A flow adds 3 then doubles. Which rule, 2(x+3) or 2x+3, fits input 1?',['x → +3 → ×2','2(x+3)','2x+3'],1,[('2(x+3)',0,2,6),('2x+3',0,2,3)],'2(x+3)','2(x+3); at x=1, y=8','Reversing the flow order.','Record the intermediate value four before doubling.'),
('easy',3,'The pairs are (0,4),(1,7),(2,10). Match y=3x+4 or y=4x+3; test x=2.',['0→4; 1→7; 2→10','y=3x+4','y=4x+3'],2,[('3x+4',0,3,4),('4x+3',0,4,3)],'3x+4','y=3x+4; at x=2, y=10','Mistaking the zero output for the rate.','At x=0 the fixed amount is four.'),
('standard',3,'A table gives 0→2, 2→8, 4→14. Which rule fits, y=3x+2 or y=2x+3? Check x=4.',['0→2; 2→8; 4→14','y=3x+2','y=2x+3'],4,[('3x+2',0,3,2),('2x+3',0,2,3)],'3x+2','y=3x+2; at x=4, y=14','Counting a two-unit input step as one.','Divide output change six by input change two.'),
('standard',3,'A taxi costs R12 once plus R5 per kilometre. Choose C=12+5k or C=5+12k and find C at k=3.',['R12 once','R5 per km','C=12+5k or 5+12k'],3,[('12+5k',0,5,12),('5+12k',0,12,5)],'12+5k','C=12+5k; C(3)=R27','Charging the fixed amount for each kilometre.','Label fixed and repeated costs separately.'),
('standard',4,'The number of tiles for a square of side n is n². Does y=n² or y=2n fit n=3?',['square with side n','y=n²','y=2n'],3,[('n²',1,0,0),('2n',0,2,0)],'n²','y=n²; at n=3, y=9','Confusing area with doubling a side.','Build three rows of three tiles.'),
('intermediate',4,'A machine subtracts 4 and then triples. Which expression, 3(x−4) or 3x−4, matches input 7?',['x → −4 → ×3','3(x−4)','3x−4'],7,[('3(x−4)',0,3,-12),('3x−4',0,3,-4)],'3(x−4)','3(x−4); at x=7, y=9','Multiplying only x.','The whole result of subtracting four is tripled.'),
('intermediate',4,'A subscription costs R20 plus R6 for each class. For 5 classes, choose 20+6n or 20n+6.',['R20 fixed','R6 per class','n=5'],5,[('20+6n',0,6,20),('20n+6',0,20,6)],'20+6n','20+6n; for 5 classes, R50','Multiplying the once-off amount.','Pay twenty once, then add five groups of six.'),
('intermediate',4,'The rows −1→1, 0→2, 1→3 are given. Does y=x+2 or y=x²+2 fit every row?',['−1→1; 0→2; 1→3','y=x+2','y=x²+2'],-1,[('x+2',0,1,2),('x²+2',1,0,2)],'x+2','y=x+2; at x=−1, y=1','Checking positive inputs only.','Test a signed input to separate the candidates.'),
('exam',5,'The pairs 0→5, 1→8, 3→14 represent a fixed fee and a rate. Which is correct: 5+3x or 3+5x? Find y(4).',['0→5; 1→8; 3→14','5+3x','3+5x'],4,[('5+3x',0,3,5),('3+5x',0,5,3)],'5+3x','5+3x; y(4)=17','Using the larger number as the rate.','The zero row determines the fixed fee.'),
('exam',5,'A rule outputs −2,1,4 for inputs −1,0,1. Choose 3x+1 or x+3; predict input 2.',['−1→−2; 0→1; 1→4','3x+1','x+3'],2,[('3x+1',0,3,1),('x+3',0,1,3)],'3x+1','3x+1; input 2 gives 7','Ignoring the negative pair.','Check every original row before predicting.'),
('exam',5,'A square border has 4n unit edges. A square area has n² unit squares. For n=5, which rule gives area?',['side n','border 4n','area n²'],5,[('n²',1,0,0),('4n',0,4,0)],'n²','n²; area at n=5 is 25 square units','Mixing boundary length with area.','Shade the 5-by-5 interior, not the 20 edges.'),
('advanced',6,'The flow doubles then adds 6; a table gives 0→6, 2→10. Does y=2(x+3) agree with both? Test x=−3.',['×2 → +6','0→6; 2→10','y=2(x+3)'],-3,[('2(x+3)',0,2,6),('2x+3',0,2,3)],'2(x+3)','Yes: 2(x+3)=2x+6; at x=−3, y=0','Assuming equivalent expressions look identical.','Distribute, then compare two table rows and a signed value.'),
('advanced',6,'Two descriptions are 4(x−2) and 4x−8. Which is equivalent to “subtract 2 then quadruple”? Evaluate x=−1.',['subtract 2, then quadruple','4(x−2)','4x−8'],-1,[('4(x−2)',0,4,-8),('4x−2',0,4,-2)],'4(x−2)','4(x−2)=4x−8; at x=−1, y=−12','Failing to multiply the negative constant.','Show four copies of x−2 before collecting.'),
('advanced',7,'A delivery company offers A=10+4d or B=4+10d. The bill for 0 km is R10 and for 2 km R18. Identify the rule and give the bill for 5 km.',['0 km→R10; 2 km→R18','A=10+4d','B=4+10d'],5,[('10+4d',0,4,10),('4+10d',0,10,4)],'10+4d','A=10+4d; at 5 km, R30','Swapping the fixed fee and per-kilometre rate.','Use zero kilometres for fixed fee and divide the change by two.'),
]
# Lesson 6 starts with a stated learner claim. The two rule paths expose a first
# wrong operation before the correct repair, with a parallel check at test input.
SIX=[
('foundation',2,'A learner claims double x then add 3 is 2(x+3). Find the first error and repair for x=2.',['double x → add 3','learner 2(x+3)'],2,[('learner',0,2,6),('correct',0,2,3)],'correct','Correct: 2x+3, so x=2 gives 7; learner gives 10','The learner grouped the addition inside doubling.','Double x first; add three once afterwards.'),
('easy',2,'A learner claims the table 0→4,1→7 follows y=4x+3. Diagnose with x=0.',['0→4; 1→7','learner 4x+3'],0,[('learner',0,4,3),('correct',0,3,4)],'correct','Correct: 3x+4; x=0 must output 4','The zero input output was used as the coefficient.','Set x to zero to locate the constant.'),
('easy',3,'A learner writes add 2 then triple as 3x+2. Find the first missed operation and test x=1.',['x → +2 → ×3','learner 3x+2'],1,[('learner',0,3,2),('correct',0,3,6)],'correct','Correct: 3(x+2); at x=1 the output is 9','The triple did not act on the entire previous result.','Keep x+2 together when tripling.'),
('standard',3,'From pairs 0→6,2→12 a learner writes y=6x+6. Identify the wrong rate and predict y at x=4.',['0→6; 2→12','learner y=6x+6'],4,[('learner',0,6,6),('correct',0,3,6)],'correct','Correct: y=3x+6; at x=4, y=18','Six output units were counted per one input unit.','Divide Δy=6 by Δx=2.'),
('standard',3,'For a R8 joining fee plus R5 per visit, a learner writes C=8v+5. Correct the swapped fee and find cost at v=3.',['R8 once','R5 each visit','learner 8v+5'],3,[('learner',0,8,5),('correct',0,5,8)],'correct','Correct: C=8+5v, C(3)=R23','The once-off charge was multiplied by visits.','Place the visit fee beside v and joining fee separately.'),
('standard',4,'A learner sees −2→−3,0→1,2→5 and proposes y=2x−1. Find the first counterexample and predict x=3.',['−2→−3; 0→1; 2→5','learner 2x−1'],3,[('learner',0,2,-1),('correct',0,2,1)],'correct','Correct: y=2x+1; at x=3, y=7','The zero-row intercept sign was copied incorrectly.','Substitute x=0 into the candidate before forecasting.'),
('intermediate',4,'A learner says y=x²+1 has constant differences for x=0,1,2,3. Show the first change that disproves this.',['x=0,1,2,3','learner says constant changes'],3,[('linear claim',0,2,1),('square rule',1,0,1)],'correct','Outputs 1,2,5,10; differences 1,3,5 are not constant','Comparing two outputs without checking later differences.','Compute all successive changes.'),
('intermediate',4,'A learner says 2(x+4) and 2x+4 are equivalent. Give one counterexample at x=1 and repair.',['2(x+4)','learner 2x+4'],1,[('learner',0,2,4),('correct',0,2,8)],'correct','At x=1: 10 versus 6; correct expansion is 2x+8','The outside factor was not applied to four.','Distribute two to both terms.'),
('intermediate',4,'For y=−2x+3 a learner says a negative input makes the output negative. At x=−4 find the first sign error and the correct output.',['rule y=−2x+3','learner treats −2×−4 as −8'], -4,[('learner',0,2,3),('correct',0,-2,3)],'correct','At x=−4, two negative factors give +8, so y=11','A negative times a negative was treated as negative.','Keep the two signs visible before adding three.'),
('exam',5,'Pairs 0→2,1→3,2→6 follow x²+2. A learner fits x+2 from the first two rows. Locate the counterexample.',['0→2; 1→3; 2→6','learner x+2'],2,[('learner',0,1,2),('correct',1,0,2)],'correct','At x=2, learner predicts 4 but given output is 6','Two rows cannot prove a unique rule.','Check every supplied pair before accepting the rule.'),
('exam',5,'A square tile array has side n; learner uses y=4n for area. At n=3 locate and repair the mix-up.',['square side n','learner area 4n'],3,[('learner',0,4,0),('correct',1,0,0)],'correct','Area is n²=9 tiles; 4n=12 counts boundary edges','The learner used perimeter for area.','Count rows times columns for the interior.'),
('exam',5,'A learner reverses y=3x+5 at y=20 by dividing 20 by 3, then subtracting 5. Diagnose and recover x.',['x → ×3 → +5','output 20','learner divide then subtract'],20,[('learner',0,1/3,-5),('correct',0,1/3,-5/3)],'correct','Subtract 5 first, then divide by 3: x=5; check 3·5+5=20','The inverse operations were applied in forward order.','Undo the last +5 before the earlier ×3.'),
('advanced',6,'The rows −1→0,0→1,1→4 agree with x²+2x+1. A learner claims x²+1 from nonnegative rows. Identify a counterexample.',['−1→0; 0→1; 1→4','learner x²+1'],1,[('learner',1,0,1),('correct',1,2,1)],'correct','At x=1, learner gives 2 instead of 4; correct rule gives 4','One matching zero row does not determine a rule.','Check the signed and positive rows.'),
('advanced',6,'A service charges R15 fixed and R4 per unit. Learner sees 0→15,3→27 but uses 15x+4. Find first wrong row and repair at x=5.',['0→15; 3→27','learner 15x+4'],5,[('learner',0,15,4),('correct',0,4,15)],'correct','At x=0 learner gives 4 instead of 15; correct cost at 5 is R35','The fixed charge and variable rate were reversed.','Start at zero, then compute Δcost/Δunits=12/3.'),
('advanced',7,'A learner claims 3(x−2)=3x−2 and that y=3x−2 fits 0→−6,2→0. Find first invalid step and show a fresh check at x=4.',['3(x−2)','0→−6; 2→0','learner 3x−2'],4,[('learner',0,3,-2),('correct',0,3,-6)],'correct','Distribute −2 as −6: 3x−6; at x=4, y=6','The three was not multiplied by −2.','Build three copies of (x−2) and test both given rows.'),
]
assert len(FIVE)==len(SIX)==15

def value(coeff,x):
    _,a,b,c=coeff
    return round(a*x*x+b*x+c,8)

def build(number,rows,title,slug,bankfile):
    items=[]
    for n,(level,marks,prompt,givens,x,candidates,chosen,answer,mistake,repair) in enumerate(rows,1):
        if number==6: chosen=candidates[1][0]
        assert 1<=len(givens)<=4 and len(candidates)==2 and chosen in [c[0] for c in candidates]
        evaluations=[{'label':c[0],'value':value(c,x),'a':c[1],'b':c[2],'c':c[3]} for c in candidates]
        correct=next(c for c in candidates if c[0]==chosen)
        assert evaluations[0]['value']!=evaluations[1]['value'],(number,n)
        if number==5:
            states=['Read the given representations',f'Test input {x} in both rules',f'{candidates[0][0]} → {evaluations[0]["value"]}; {candidates[1][0]} → {evaluations[1]["value"]}',answer]
            actions=[('Identify what is fixed and what changes.',f'At input {x}, substitute in each candidate, keeping the original operation order.'),
                     (f'Evaluate both candidates at input {x}.',f'The candidates give {evaluations[0]["value"]} and {evaluations[1]["value"]}. Compare with the stated relationship.'),
                     (f'Choose {chosen} and state the output.',f'{answer}. Read the input and output with the context units, if any.')]
        else:
            states=['Read the learner claim and original evidence',f'Test the claim at input {x}',f'Learner path → {evaluations[0]["value"]}; repair path → {evaluations[1]["value"]}',answer]
            actions=[('Locate the first unsupported claim.',f'Check the given statement or pair before accepting the learner move. {mistake}'),
                     (f'Compare at input {x}.',f'The learner path gives {evaluations[0]["value"]}; the repaired path gives {evaluations[1]["value"]}. The difference identifies the error.'),
                     ('Repair and verify with the original.',f'{repair} {answer}')]
        steps=[{'title':a,'action':a,'narration':b} for a,b in actions]
        verify=f'At input {x}, {chosen} gives {value(correct,x)}; recheck against the original words, rows or formula.'
        scene={'input':x,'candidates':evaluations,'chosen':chosen,'given':givens,'mode':'match' if number==5 else 'repair'}
        items.append({'id':f'g8-fr-l{number:02}-w{n:02}','number':n,'level':level,'marks':marks,
                      'q':prompt,'answer':answer,'model':{'family':'relationship_match' if number==5 else 'relationship_repair',
                      'inputs':givens if len(givens)>1 else [givens[0],f'test input {x}'],'outputs':[f'{chosen} evaluated at {x}',answer],
                      'description':title,'scene':scene},'states':states,'steps':steps,
                      'verify':verify,'misconception':mistake,'repair':repair})
    document=DOCS/f'lesson-{number:02}-{slug}.md'
    text=[f'# Grade 8 Functions and Relationships — Lesson {number}: {title}','',
          f'Original Athena authoring aligned with Grade 8 CAPS §2.2. Teacher review required. Source: {CAPS}','',
          'This pack specifies individual mathematical states and visual objects. The board starts with the question and givens, shows an operation before its value, keeps prior work visible and checks the original.','',
          '## Worked examples']
    for item in items:
        text += ['',f"### {item['number']:02} — {item['level']} ({item['marks']} marks)",'',
            f"**Question:** {item['q']}",f"**Answer:** {item['answer']}",
            f"**Question scene:** {json.dumps(item['model']['scene'],ensure_ascii=False)}",
            '**Board states:** '+' → '.join(item['states'])]
        for step in item['steps']:
            text += [f"- {step['title']} Narration/caption: {step['narration']}"]
        text += [f"**Verification:** {item['verify']}",f"**Misconception:** {item['misconception']}",f"**Targeted repair:** {item['repair']}"]
    tree=ast.parse((BASE/bankfile).read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in {'PRACTICE','MASTERY','REASSESS'}:
            text += ['',f'## {node.targets[0].id.title()} bank']
            for i,(q,a,memo) in enumerate(ast.literal_eval(node.value),1):
                text += ['',f'{i}. {q}',f'   - Memo: {a}. {memo}']
    text += ['', 'Learner assessment keys stay server-side until submission.','']
    document.write_text('\n'.join(text),encoding='utf-8')
    data={'id':f'g8-functions-relationships-{number:02}','title':title,'source_document':document.name,
          'source_sha256':hashlib.sha256(document.read_bytes()).hexdigest(),'worked_examples':items}
    (BASE/'generated'/f'functions_relationships_{number:02}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(number,len(items),document)

build(5,FIVE,'Matching representations and evaluating rules','matching-representations','assessment_functions_lesson5.py')
build(6,SIX,'First-error diagnosis and relationship repair','relationship-repair','assessment_functions_lesson6.py')
