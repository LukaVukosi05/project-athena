"""Author original Grade 8 numerical substitution source and runtime records."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson7_Source_Pack_v1.docx'
JSON=ROOT/'backend/app/curriculum/grade8/generated/algebraic_expressions_07.json'
SOURCES=[('DBE Grade 8 Mathematics 2026 ATP','https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208'),('DBE CAPS Grades 7–9 Mathematics','https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf')]


def ex(n,level,marks,skill,q,answer,family,tokens,states,moves,verify,mistake,repair):
    assert len(states)==len(moves)+1 and len(states)>=3 and len(set(states))==len(states)
    return dict(id=f'g8-ex-l07-w{n:02}',number=n,level=level,marks=marks,skill=skill,q=q,
                answer=answer,model={'family':family,'tokens':tokens,'description':skill},
                states=states,steps=[dict(title=a,action=b,narration=c) for a,b,c in moves],
                verify=verify,misconception=mistake,repair=repair)


E=[
 ex(1,'foundation',2,'Replace one variable','Evaluate x+4 when x=3.','7.','value_machine',['x+4','x=3','7'],
    ['x+4; x=3','3+4','7'],
    [('Move the value into the slot','Put three where the x appears.','The variable is a place for a given number.'),('Calculate the output','Three plus four equals seven.','The expression has numerical value seven.')],
    'Original x+4 at x=3 gives 3+4=7.','Keeping x in the calculation after substitution.','Point to x, cover it and replace it with 3.'),
 ex(2,'easy',2,'Keep a signed input in brackets','Evaluate 3a when a=-2.','-6.','signed_slot',['3a','a=-2','-6'],
    ['3a; a=-2','3(-2)','-6'],
    [('Place negative two in the a slot','Write 3(-2), keeping the minus inside brackets.','Juxtaposition means multiplication, not addition.'),('Multiply with signs','Positive three times negative two is negative six.','The negative input stays attached to its value.')],
    'At a=-2, 3a=3(-2)=-6.','Reading 3a as 3+a or dropping the negative.','Show the multiplication dot and the signed chip.'),
 ex(3,'easy',3,'Square a negative substitution','Evaluate t² when t=-3.','9.','exponent_scope',['t²','t=-3','9'],
    ['t²; t=-3','(-3)²','(-3)(-3)','9'],
    [('Put the full signed value in the base','Use (-3)², not -3².','Brackets tell the square to act on the negative value.'),('Open the square','Write two factors of negative three.','The exponent two makes two complete copies.'),('Multiply both negatives','Negative three times negative three is positive nine.','An even number of negative factors is positive.')],
    'Substitute -3 in t²: (-3)(-3)=9.','Squaring three but leaving a minus outside.','Circle the base and duplicate its brackets.'),
 ex(4,'standard',4,'Distinguish a negative outside the square','Evaluate -x² and (-x)² when x=-2.','-4 and 4 respectively.','compare_scope',['-x²','(-x)²','x=-2','-4','4'],
    ['-x² ; (-x)² ; x=-2','-(-2)² ; (-(-2))²','-(4) ; (2)²','-4 ; 4'],
    [('Mark the base of each power','For -x² the minus is outside x²; for (-x)² it is inside.','Exponent scope controls the sign.'),('Square the two bases','Negative two squared is four; negative of negative two is positive two.','The outside minus has not been squared.'),('Complete both branches','Take negative four in the first branch and positive four in the second.','The two numerical values differ.')],
    'Direct check: -(−2·−2)=−4, while (−(−2))·(−(−2))=4.','Treating -x² and (-x)² as equivalent.','Put a bracket boundary around each base first.'),
 ex(5,'standard',3,'Respect multiplication before addition','Evaluate 2x+5 when x=-4.','-3.','value_machine',['2x+5','x=-4','-3'],
    ['2x+5; x=-4','2(-4)+5','-8+5','-3'],
    [('Substitute with brackets','Put negative four into the x slot while retaining plus five.','The coefficient two multiplies the input first.'),('Multiply before adding','Two times negative four is negative eight.','The addition remains visible for the next action.'),('Add the constant','Negative eight plus five is negative three.','Follow the order of operations.')],
    'Original 2(-4)+5=-8+5=-3.','Adding five to negative four before multiplying.','Point to multiplication first, then addition.'),
 ex(6,'standard',4,'Use two distinct input values','Evaluate 4a-3b when a=2 and b=-1.','11.','two_input',['4a-3b','a=2','b=-1','11'],
    ['4a-3b; a=2,b=-1','4(2)-3(-1)','8-(-3)','11'],
    [('Fill both named slots','Put two for a and negative one for b; do not swap them.','Each variable has its own colour and value.'),('Multiply each term','Four times two is eight; three times negative one is negative three.','Keep subtraction of the negative product visible.'),('Resolve double negative','Eight minus negative three equals eleven.','Subtracting a negative adds three.')],
    'At (a,b)=(2,-1), original 4a-3b=8-(-3)=11.','Replacing both a and b with the same number.','Use separate value chips for a and b.'),
 ex(7,'standard',4,'Keep a bracketed difference together','Evaluate 2(x-3) when x=-2.','-10.','bracket_input',['2(x-3)','x=-2','-10'],
    ['2(x-3); x=-2','2((-2)-3)','2(-5)','-10'],
    [('Replace only x inside the bracket','Write negative two in its own brackets; leave the outer two outside.','The outside two multiplies the whole difference.'),('Calculate inside first','Negative two minus three is negative five.','Close the inside operation before multiplying.'),('Multiply the group','Two times negative five is negative ten.','The whole group is one signed factor.')],
    'Original at x=-2 is 2(-2-3)=2(-5)=-10.','Distributing two to x but not the constant, or skipping the inner subtraction.','Keep a border around the bracket until its value is known.'),
 ex(8,'intermediate',4,'Square before subtracting a product','Evaluate x²-2x when x=-3.','15.','layered_order',['x²-2x','x=-3','15'],
    ['x²-2x; x=-3','(-3)²-2(-3)','9-(-6)','15'],
    [('Substitute into both x slots','Put (-3) in the square and in the linear term.','One given value fills every occurrence of x.'),('Do powers and products','Negative three squared is nine; two times negative three is negative six.','Subtract the entire negative product.'),('Finish the signed subtraction','Nine minus negative six is fifteen.','The result is positive fifteen.')],
    'At x=-3 the original is 9+6=15.','Interpreting -2x as -2+x or (-3)² as -9.','Show both occurrences and settle powers and products first.'),
 ex(9,'intermediate',4,'Evaluate a fraction and a constant','Evaluate x/2+3 when x=-4.','1.','fraction_gate',['x/2+3','x=-4','1'],
    ['x/2+3; x=-4','(-4)/2+3','-2+3','1'],
    [('Place the input in the numerator','Write negative four over two, keeping plus three outside the fraction bar.','Only x is divided by two.'),('Divide before adding','Negative four divided by two is negative two.','The outside three is unchanged.'),('Add at the end','Negative two plus three is one.','The fraction bar has a limited scope.')],
    'Original (-4)/2+3=-2+3=1.','Dividing x+3 by two instead of only x.','Draw the fraction bar boundary before substituting.'),
 ex(10,'intermediate',5,'Reject a zero denominator','Evaluate 5/(x-1) at x=3 and at x=1.','At x=3 the value is 5/2; at x=1 it is undefined.','fraction_gate',['5/(x-1)','x=3','x=1','5/2','undefined'],
    ['5/(x-1); x=3 or 1','At x=3: 5/(3-1); at x=1: 5/(1-1)','At x=3: 5/2; at x=1: 5/0','5/2; undefined for x=1'],
    [('Substitute separately','Use a distinct denominator lane for three and for one.','The denominator is the complete x minus one group.'),('Calculate denominators','Three minus one is two; one minus one is zero.','A zero denominator signals an invalid input.'),('Report both outcomes','Five over two is valid; five over zero is undefined.','Do not cancel or invent a value for the invalid branch.')],
    'At x=3, 5/(3-1)=5/2; at x=1, 5/(1-1)=5/0 is undefined.','Treating 5/0 as zero or allowing x=1.','Calculate the whole denominator before dividing.'),
 ex(11,'exam',5,'Evaluate a three-term expression with two inputs','Evaluate 2a²-3ab+b² when a=-2 and b=3.','35.','two_input',['2a²-3ab+b²','a=-2','b=3','35'],
    ['2a²-3ab+b²; a=-2,b=3','2(-2)²-3(-2)(3)+(3)²','2(4)-3(-6)+9','8+18+9','35'],
    [('Fill every named occurrence','Replace both a slots with negative two and both b slots with three.','Retain a bracket around each signed input.'),('Calculate powers and inner product','Negative two squared is four; negative two times three is negative six; three squared is nine.','Do these multiplications before adding terms.'),('Resolve the signed middle term','Negative three times negative six is positive eighteen.','The middle result increases the total.'),('Add the three values','Eight plus eighteen plus nine is thirty five.','All three original terms have contributed.')],
    'At (a,b)=(-2,3): 2·4-3(-6)+9=35.','Dropping the sign of a in one of its occurrences.','Colour every a slot the same before inserting (-2).'),
 ex(12,'exam',5,'Evaluate two equivalent forms','At x=-2, compare 3(x+4) and 3x+12.','Both equal 6.','equivalent_value_paths',['3(x+4)','3x+12','x=-2','6','6'],
    ['3(x+4) ; 3x+12 ; x=-2','3((-2)+4) ; 3(-2)+12','3(2) ; -6+12','6 ; 6'],
    [('Fill both pathways','Put negative two in each complete expression.','Equivalent forms should give the same result at the same input.'),('Evaluate inside each path','First bracket gives two; second expression gives negative six plus twelve.','Keep two independent calculations visible.'),('Compare numerical outputs','Both paths end at six.','This input confirms agreement here; a single test alone is not proof for all x.')],
    'At x=-2, 3(2)=6 and -6+12=6; distribution also shows 3(x+4)=3x+12 for all x.','Claiming equal outputs at one input proves equivalence generally.','Verify this input, then show the distribution identity.'),
 ex(13,'exam',5,'Diagnose a missing signed bracket','A learner evaluates 2x² at x=-3 as -18. Find the first error and correct it.','They used -3² instead of (-3)²; the value is 18.','error_substitution',['2x²','x=-3','claim: -18','18'],
    ['Claim: 2x² at x=-3 is -18','Correct substitution: 2(-3)²','Square the complete input: 2(9)','Correct value: 18'],
    [('Find the substitution slot','The learner wrote a minus without grouping the value negative three.','The exponent applies to the whole substituted value.'),('Show the first correct mathematical action','Write two times negative three in parentheses squared.','The two negative factors make positive nine.'),('Repair the calculation','Two times nine is eighteen.','The learner claim negative eighteen fails the original expression.')],
    'Original 2(-3)(-3)=18, not -18.','Treating (-3)² as -(3²).','Draw the exponent scope around both parentheses.'),
 ex(14,'advanced',7,'Evaluate a contextual perimeter rule','A rectangle has length 4 cm and width (x+1) cm. Its perimeter is P=2(l+w). Find P when x=3.','16 cm.','context_measure',['length=4 cm','width=x+1 cm','x=3','P=2(l+w)','16 cm'],
    ['l=4, w=x+1, x=3; P=2(l+w)','w=3+1=4 cm; P=2(4+4)','P=2(8) cm','P=16 cm'],
    [('Calculate the width first','Substitute three in x plus one to get four centimetres.','The width depends on x; length is already known.'),('Put both dimensions into perimeter','Two groups of length plus width gives two times eight.','Every side is counted: four, four, four and four.'),('Multiply and keep the unit','Two times eight is sixteen centimetres.','Perimeter uses a length unit, not square centimetres.')],
    'Four sides 4+4+4+4=16 cm, matching 2(4+4).','Using area units or only one pair of sides.','Trace all four boundary sides on the rectangle.'),
 ex(15,'advanced',7,'Evaluate with mixed operations and a denominator','Evaluate 3x²-2(x-4)+6/x when x=-2.','21.','layered_order',['3x²','-2(x-4)','+6/x','x=-2','21'],
    ['3x²-2(x-4)+6/x; x=-2','3(-2)²-2((-2)-4)+6/(-2)','3(4)-2(-6)-3','12+12-3','21'],
    [('Insert the signed input everywhere','All three x positions receive negative two with brackets.','The denominator is nonzero at negative two.'),('Resolve powers, brackets and quotient','The square is four, inner bracket negative six, six over negative two is negative three.','Respect the boundaries of each operation.'),('Multiply the remaining factors','Three times four is twelve; negative two times negative six is positive twelve.','Keep the negative three fraction result visible.'),('Add the three terms','Twelve plus twelve minus three is twenty one.','Each branch contributes once to the total.')],
    'At x=-2, original 3·4-2(-6)+6/(-2)=12+12-3=21.','Cancelling the negative denominator or dropping the bracket sign.','Build three parallel calculation lanes before combining.'),
]
P=[
 ('p01','Evaluate y+6 when y=2.','8','Replace y by two.','2+6=8.'),
 ('p02','Evaluate 5m when m=-3.','-15','Bracket the signed input.','5(-3)=-15.'),
 ('p03','Evaluate a² when a=-4.','16','Put -4 inside the squared base.','(-4)²=16.'),
 ('p04','Evaluate -x² and (-x)² when x=-3.','-9 and 9 respectively','Mark where the exponent starts.','-(-3)²=-9; (-(-3))²=9.'),
 ('p05','Evaluate 3x+2 when x=-2.','-4','Multiply before adding.','3(-2)+2=-6+2=-4.'),
 ('p06','Evaluate 2a-4b when a=3 and b=-2.','14','Keep distinct signed value chips.','2(3)-4(-2)=6+8=14.'),
 ('p07','Evaluate 3(x-2) when x=-1.','-9','Calculate inside the bracket first.','3(-1-2)=3(-3)=-9.'),
 ('p08','Evaluate x²-3x when x=-2.','10','Square the signed input.','(-2)²-3(-2)=4+6=10.'),
 ('p09','Evaluate a/3+2 when a=-6.','0','Only a is over three.','(-6)/3+2=-2+2=0.'),
 ('p10','Evaluate 8/(x-2) at x=4 and x=2.','4 at x=4; undefined at x=2','Check both denominators.','8/(4-2)=4; 8/(2-2)=8/0 is undefined.'),
 ('p11','Evaluate a²-2ab+b² when a=-1 and b=2.','9','Substitute twice for each variable.','(-1)²-2(-1)(2)+2²=1+4+4=9.'),
 ('p12','At x=-1 compare 2(x+3) and 2x+6.','Both equal 4','Compute each lane separately.','2(-1+3)=4 and 2(-1)+6=4.'),
 ('p13','Correct a learner who reports x²=-16 when x=-4.','16','Bracket the negative four before squaring.','(-4)(-4)=16.'),
 ('p14','A rectangle has length 5 cm and width x+2 cm. Find P=2(l+w) at x=1.','16 cm','Calculate width, then trace four sides.','w=3 cm; P=2(5+3)=16 cm.'),
 ('p15','Evaluate 2x²-3(x-1)+4/x at x=-2.','15','Use three branches.','2(4)-3(-3)+4/(-2)=8+9-2=15.'),
]
M=[
 ('m01',2,'Evaluate 4x+1 at x=-3.','-11','4(-3)+1=-12+1=-11.'),
 ('m02',3,'Evaluate -a² and (-a)² when a=-2.','-4 and 4 respectively','-(-2)²=-4; (-(-2))²=4.'),
 ('m03',4,'Evaluate 3a²-2b when a=-2 and b=-3.','18','3(-2)²-2(-3)=12+6=18.'),
 ('m04',5,'Evaluate 9/(x-1) at x=4 and x=1.','3 at x=4; undefined at x=1','9/(4-1)=3, while 9/(1-1)=9/0 undefined.'),
 ('m05',6,'A rectangle has length x+2 cm and width 2x-1 cm. Find P=2(l+w) at x=3 and verify four sides.','20 cm','At x=3, l=5 and w=5; P=2(5+5)=20 cm; four sides total 5+5+5+5=20 cm.'),
]
R=[
 ('r01','Evaluate 3x-4 at x=-2.','-10','3(-2)-4=-10.'),
 ('r02','Evaluate 2a²-b when a=-3 and b=-4.','22','2(-3)²-(-4)=18+4=22.'),
 ('r03','Evaluate 6/(x-2) at x=5 and x=2.','2 at x=5; undefined at x=2','6/(5-2)=2; 6/(2-2) is undefined.'),
]

for item,count in zip(E,[2,2,2,3,2,3,2,2,2,3,3,3,3,4,4]):
    item['model']['scene']={'input_count':count}


def build():
    doc=Document();sec=doc.sections[0]
    sec.top_margin=sec.bottom_margin=Inches(.72);sec.left_margin=sec.right_margin=Inches(.78)
    style=doc.styles['Normal'];style.font.name='Arial';style.font.size=Pt(10.5);style.paragraph_format.space_after=Pt(6)
    for name in ('Title','Heading 1','Heading 2'):
        doc.styles[name].font.name='Arial';doc.styles[name].font.color.rgb=RGBColor(0,0,0)
        props=doc.styles[name]._element.pPr
        if props is not None:
            for border in props.xpath('./w:pBdr'):props.remove(border)
    doc.add_paragraph('Grade 8 Algebraic Expressions Lesson 7 Source Pack',style='Title')
    doc.add_paragraph('Substitute numbers and evaluate algebraic expressions')
    doc.add_paragraph('Original Project Athena draft requiring teacher review. All 15 worked examples, 15 independent questions, five mastery questions and three reassessments below are authored and loaded by the runtime; no AI question generation is required.')
    doc.add_heading('Curriculum, prerequisites and teaching rules',1)
    for title,url in SOURCES:doc.add_paragraph(f'{title}. {url}')
    doc.add_paragraph('Prerequisites: signed-number operations, repeated factors, fraction bars, brackets and order of operations. The 2026 Grade 8 ATP specifies the numerical value of expressions by substitution. Every question and value here is original.')
    doc.add_paragraph('The board shows the original expression and each named input first. Map each input to its own variable slot, then reveal the complete bracketed substitution, one operation and one result per step. Keep previous states visible. Separate parallel calculations for two forms or two inputs. Reject division by zero before calculating a quotient. Verify in the original expression.')
    doc.add_heading('Worked examples and scenario-specific whiteboard directions',1)
    for item in E:
        doc.add_heading(f"Example {item['number']} — {item['skill']}",2)
        doc.add_paragraph(f"Difficulty: {item['level']}; marks: {item['marks']}; diagram: {item['model']['family']}")
        doc.add_paragraph('Question: '+item['q'])
        doc.add_paragraph('Initial visual factors: '+'; '.join(f"{i+1}: {token}" for i,token in enumerate(item['model']['tokens']))+'. Hide output factors until the matching operation.')
        doc.add_paragraph('Initial mathematical state: '+item['states'][0])
        for index,step in enumerate(item['steps']):
            doc.add_paragraph(f"Board step {index+1}. {step['title']}. Highlight the corresponding factor group, then perform: {step['action']} Result: {item['states'][index+1]}. Narration and caption: {step['narration']}")
        doc.add_paragraph('Final answer: '+item['answer']+' Verification: '+item['verify'])
        doc.add_paragraph('Misconception: '+item['misconception']+' Targeted repair: '+item['repair'])
    doc.add_heading('Independent practice with authored memos',1)
    for pid,q,a,hint,memo in P:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Hint: '+hint);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Mastery check: 20 marks',1)
    for pid,marks,q,a,memo in M:
        doc.add_heading(f'{pid.upper()} — {marks} marks',2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Parallel reassessment',1)
    for pid,q,a,memo in R:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Review gates',1)
    doc.add_paragraph('Teacher review must check each substitution, signed bracket, zero denominator, first-error repair, spoken caption, event target, desktop and mobile stage layout and independent-attempt gate. Existing short-text grading may reject equivalent forms; review before release.')
    OUT.parent.mkdir(parents=True,exist_ok=True);doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-06','title':'Substitution and numerical value of algebraic expressions','source_document':OUT.name,'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'worked_examples':E,'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True);JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{OUT}\n{JSON}\nSHA-256: {payload["source_sha256"]}')


if __name__=='__main__':build()
