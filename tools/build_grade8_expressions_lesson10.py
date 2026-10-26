"""Author the original Grade 8 expressions transfer and error-repair source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson10_Source_Pack_v1.docx'
JSON = ROOT / 'backend/app/curriculum/grade8/generated/algebraic_expressions_10.json'
SOURCES = [
    ('DBE CAPS Mathematics Grades 7–9', 'https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf'),
    ('DBE Grade 8 Mathematics 2026 Annual Teaching Plan', 'https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208'),
]


def ex(n, level, marks, skill, q, answer, family, tokens, states, moves, verify, mistake, repair, inputs):
    assert len(states) == len(moves) + 1 and len(states) >= 3 and len(set(states)) == len(states)
    assert 1 <= inputs < len(tokens) <= 8
    return dict(id=f'g8-ex-l10-w{n:02}', number=n, level=level, marks=marks, skill=skill,
        q=q, answer=answer, model={'family':'diagnostic_'+family,'tokens':tokens,'description':skill,
        'scene':{'input_count':inputs}}, states=states,
        steps=[dict(title=a, action=b, narration=c) for a,b,c in moves],
        verify=verify, misconception=mistake, repair=repair)


E = [
 ex(1,'foundation',2,'Keep unlike terms separate',
    'A learner writes 3x+2y=5xy. Identify the first error and give the correct expression.',
    '3x+2y; unlike terms cannot combine.','term_sort',
    ['3x','+2y','claim 5xy','correct 3x+2y'],
    ['3x+2y; learner claims 5xy','3x and 2y have different variable labels','3x+2y remains unchanged'],
    [('Compare variable labels','Move x and y terms into separate lanes.','An x tile cannot be counted as a y tile.'),
     ('Repair the first error','Keep the two unlike groups separate.','Adding the coefficients does not multiply the variables.')],
    'At x=1,y=2, original is 7 while claimed 5xy is 10.','The learner treats unlike terms as like terms.','Use two labelled lanes, then test one input.',3),
 ex(2,'easy',3,'Repair a lost negative sign',
    'A learner simplifies 7a-3a as 10a. Identify the first error and simplify.',
    '4a; the signed coefficient is −3.','signed_terms',
    ['+7a','−3a','claim +10a','result +4a'],
    ['7a−3a; learner claims 10a','Coefficients are +7 and −3','7a−3a=4a'],
    [('Carry the sign','Put plus seven and minus three on the a lane.','The minus sign belongs to three a.'),
     ('Combine signed counts','Seven minus three copies leaves four copies.','Only the a coefficients change.')],
    'At a=2 the original gives 14−6=8, and 4a=8.','The learner changes subtraction into addition.','Attach the sign to each term before moving tiles.',3),
 ex(3,'easy',3,'Separate multiplication from powers',
    'A learner writes (2x)(3x)=6x. Find the first error and correct the product.',
    '6x²; multiply both coefficients and both x factors.','factor_array',
    ['2','x','3','x','claim 6x','result 6x²'],
    ['(2x)(3x); learner claims 6x','Coefficient factors 2×3 give 6','Variable factors x×x give x²','(2x)(3x)=6x²'],
    [('Multiply numbers','Group the two numeric factors into six.','The variable factors still have to be multiplied.'),
     ('Multiply variables','Two copies of x produce x squared.','One x factor must not disappear.'),
     ('Join both products','Place six beside x squared.','Every factor in the original is represented.')],
    'For x=2 original 4×6=24; 6x²=6×4=24.','The learner drops one variable factor.','Use separate number and variable factor rows.',4),
 ex(4,'standard',4,'Diagnose a missed distribution branch',
    'A learner writes 3(x+4)=3x+4. Mark the first invalid move and expand correctly.',
    '3x+12; multiply both bracket terms by 3.','distribution_paths',
    ['outer 3','x','+4','claim 3x+4','result 3x+12'],
    ['3(x+4); learner claims 3x+4','First branch: 3×x=3x','Second branch: 3×4=12','3(x+4)=3x+12'],
    [('Trace first arrow','Connect three to x.','The first product is three x.'),
     ('Trace missing arrow','Connect the same three to four.','The outside factor multiplies every bracket term.'),
     ('Combine two paths','Write both products with their signs.','The original sum is preserved.')],
    'At x=2 original 3(6)=18; 3x+12=18.','The learner multiplies only the first bracket term.','Draw one arrow from the outside factor to each term.',3),
 ex(5,'standard',4,'Repair a sign after bracket subtraction',
    'A learner simplifies 5p-(2p-3) to 3p-3. Locate the first wrong sign and simplify.',
    '3p+3; subtract both bracket terms.','signed_distribution',
    ['+5p','outside −','+2p','−3','claim 3p−3','result 3p+3'],
    ['5p−(2p−3); learner claims 3p−3','−(2p−3) becomes −2p+3','5p−2p+3','3p+3'],
    [('Reverse both signs','Apply minus one to two p and minus three.','Subtracting negative three adds three.'),
     ('Rewrite all signed terms','Keep five p and the converted bracket.','Do not change the earlier five p.'),
     ('Collect like terms','Five p minus two p gives three p.','The constant plus three remains.')],
    'At p=2 original 10−(4−3)=9; 3p+3=9.','The learner leaves the inner negative three unchanged.','Show the minus-one arrows to both bracket terms.',4),
 ex(6,'standard',4,'Divide every numerator term',
    'A learner claims (12m+8)/4=3m+8. Locate the first missed division and correct it.',
    '3m+2; divide both terms by 4.','quotient_lanes',
    ['12m','+8','÷4','claim 3m+8','result 3m+2'],
    ['(12m+8)/4; learner claims 3m+8','12m÷4=3m','8÷4=2','(12m+8)/4=3m+2'],
    [('Split the numerator','Place the common divisor under each numerator term.','A denominator divides the entire numerator.'),
     ('Divide the constant','Eight shared in four equal groups gives two.','The original eight is not carried through unchanged.'),
     ('Join the quotients','Keep the plus sign between three m and two.','Each original term has a matching quotient.')],
    'At m=2 original (24+8)/4=8; 3m+2=8.','The learner divides only the variable term.','Use separate quotient lanes for each numerator term.',3),
 ex(7,'intermediate',5,'Check exponent scope with a negative input',
    'A learner substitutes x=−3 into 2x² and writes (2×−3)²=36. Find the first error and evaluate.',
    '18; only x is squared.','exponent_scope',
    ['coefficient 2','x=−3','square x only','claim 36','result 18'],
    ['2x² with x=−3; learner claims 36','Substitute 2(−3)²','(−3)²=9','2×9=18'],
    [('Mark the exponent base','The exponent belongs to x, not to two x.','The coefficient stays outside the square.'),
     ('Square the signed input','Negative three times negative three gives positive nine.','Brackets keep the negative input together.'),
     ('Multiply by two','Two groups of nine give eighteen.','Squaring the whole product would be a different expression.')],
    'At x=−3, 2x²=2(9)=18; (2x)²=36 belongs to a different rule.','The learner squares the coefficient as well as x.','Circle just the exponent base before substituting.',3),
 ex(8,'intermediate',5,'Repair a root shortcut',
    'A learner says √(t²)=t for every real t. Diagnose the first false claim and write the correct result.',
    '|t|, the nonnegative magnitude of t.','root_pairs',
    ['t²','principal √','t=−5 counterexample','claim t','result |t|'],
    ['Claim √(t²)=t for every real t','Square −5 to obtain 25','Principal √25 is 5, not −5','Therefore √(t²)=|t|'],
    [('Choose a negative test','Negative five is allowed as an input.','A universal claim must work for negative values too.'),
     ('Square then root','The square is twenty five; its principal square root is five.','The square root symbol selects a nonnegative output.'),
     ('Repair the universal rule','Absolute value produces five for negative five.','The output is magnitude for either sign.')],
    't=−5 gives √((-5)²)=√25=5 and |−5|=5.','The learner assumes the principal root preserves a negative sign.','Show paired +5 and −5 inputs mapping to the same square.',2),
 ex(9,'intermediate',5,'Check two paths for equivalence',
    'A learner claims 2(x+5) and 2x+5 are equivalent. Find a counterexample and the correct expansion.',
    'Not equivalent; 2(x+5)=2x+10.','parallel_paths',
    ['path A: 2(x+5)','path B: 2x+5','x=1','claim equal','correct 2x+10'],
    ['Claim 2(x+5)=2x+5','At x=1, first path is 12','At x=1, second path is 7','Distribute: 2(x+5)=2x+10'],
    [('Test the first path','One plus five gives six, then times two gives twelve.','Apply the bracket before the outside factor.'),
     ('Test the second path','Two times one plus five gives seven.','The two stated forms disagree.'),
     ('Repair the expansion','The outside two also multiplies five.','A correct equivalent form gives twelve for this test.')],
    'At x=1 original 2(6)=12; 2x+10=12, while 2x+5=7.','The learner omits the second distribution branch.','Keep two paths visible and compare the same input.',2),
 ex(10,'exam',6,'Find the first bad line in mixed algebra',
    'A learner writes 4(2y−1)−3y → 8y−1−3y → 5y−1. Identify the first invalid arrow and simplify.',
    'First arrow is invalid: 4(−1)=−4; result 5y−4.','mixed_trace',
    ['4(2y−1)−3y','claimed 8y−1−3y','outer 4','−1 in bracket','correct 5y−4'],
    ['4(2y−1)−3y; first claimed line 8y−1−3y','Distribute 4: 8y−4−3y','Collect y terms: 5y−4','First invalid arrow was the missed 4×(−1)'],
    [('Repair the first arrow','Four times two y is eight y; four times minus one is minus four.','The claimed line forgot the second product.'),
     ('Collect after repair','Eight y minus three y leaves five y.','Keep the repaired constant minus four.'),
     ('Name the error location','The initial expansion is where the work first diverges.','A later line cannot repair an earlier wrong constant by itself.')],
    'At y=2 original 4(3)−6=6; 5y−4=6.','The learner notices the last line but misses the first illegal distribution.','Compare consecutive lines and stop at the earliest invalid arrow.',4),
 ex(11,'exam',6,'Protect a zero divisor while simplifying',
    'A learner simplifies (6a²+9a)/(3a) to 2a+3 and says it works at a=0. Identify the first false domain claim.',
    '2a+3 for a≠0; the original is undefined at a=0.','restricted_quotient',
    ['numerator 6a²+9a','divisor 3a','claim a=0 allowed','result 2a+3 for a≠0'],
    ['(6a²+9a)/(3a); learner allows a=0','Original denominator 3a=0 when a=0','For a≠0 split: 6a²/3a+9a/3a','Simplify to 2a+3, with a≠0'],
    [('Inspect the original denominator','Three a cannot equal zero.','At zero the original quotient does not exist.'),
     ('Separate two legal quotients','Only after excluding zero divide each numerator term.','Cancellation requires the divisor to be nonzero.'),
     ('Carry the restriction','The shortened expression is valid only for nonzero a.','A simplified formula does not restore the removed input.')],
    'At a=2 original (24+18)/6=7; 2a+3=7; at zero original has denominator zero.','The learner cancels a then admits a forbidden input.','Mark the domain gate before cancelling any factor.',3),
 ex(12,'exam',6,'Audit units and a fixed fee',
    'A courier charges R12 once plus R4 per kilometre. A learner writes C(k)=16k. Find the first modelling error and cost for 5 km.',
    'C(k)=12+4k rand; C(5)=R32.','context_receipt',
    ['fixed R12 once','R4 per km','5 km','claim 16k','correct 12+4k; R32'],
    ['Fixed R12 and R4 per kilometre; learner writes 16k','Variable portion after k km is 4k','One fixed fee gives C(k)=12+4k','At 5 km: C=12+20=R32'],
    [('Count repeated charges','Four rand repeats for every kilometre.','The twelve-rand fee is not a price per kilometre.'),
     ('Add the fixed fee once','Keep the fixed tile outside the kilometre groups.','The total cost is twelve plus four k.'),
     ('Check five kilometres','Five kilometre tiles total twenty rand; add twelve.','Thirty two rand follows from the original charges.')],
    'For zero kilometres cost is R12, not R0; for five kilometres cost is R32.','The learner repeats a once-only charge.','Build separate fixed and repeating rows, labelled rand and kilometre.',3),
 ex(13,'advanced',7,'Diagnose an area model after substitution',
    'A rectangle has sides (x+2) cm and 3 cm. A learner writes area 3x+2 cm² and gets 14 cm² at x=4. Find the first error and correct both.',
    'Area 3x+6 cm²; at x=4 it is 18 cm².','area_split',
    ['length x+2 cm','width 3 cm','x=4','claim 3x+2; 14 cm²','result 3x+6; 18 cm²'],
    ['Area is 3(x+2); learner claims 3x+2','Split length into x and 2; both share width 3','Area parts 3x and 6: total 3x+6 cm²','At x=4, sides 6 cm and 3 cm give 18 cm²'],
    [('Draw the split rectangle','Split the x-plus-two side into x and two.','Both regions still have width three.'),
     ('Calculate both regions','Areas are three x and six.','The second region is three times two, not two.'),
     ('Verify with the given input','At four the whole rectangle measures six by three.','Its area is eighteen square centimetres.')],
    'At x=4 area 3(4+2)=18 and 3(4)+6=18; claimed 14 is wrong.','The learner forgets to multiply the extra length by the width.','Highlight both rectangles with a shared height of three.',3),
 ex(14,'advanced',7,'Audit two orderings of a flow',
    'Rule A triples n then subtracts 2; Rule B subtracts 2 then triples. A learner says both rules give the same output. Test n=4 and write both rules.',
    'A(n)=3n−2 gives 10; B(n)=3(n−2) gives 6; they differ.','parallel_flows',
    ['A: ×3 then −2','B: −2 then ×3','n=4','claim same','A=10; B=6'],
    ['Two flow rules; learner claims equality','A at 4: 4→12→10','B at 4: 4→2→6','A(n)=3n−2; B(n)=3(n−2); not equal'],
    [('Trace A in order','Triple four to twelve then subtract two to ten.','The subtraction happens after multiplying.'),
     ('Trace B in order','Subtract two first to get two then triple to six.','The bracket groups the subtraction before multiplying.'),
     ('Compare one shared input','Ten differs from six, so the universal claim fails.','A single counterexample is sufficient.')],
    'At n=4 A=10 and B=6; 3(n−2)=3n−6, not 3n−2.','The learner ignores the order of flow operations.','Place both flows in parallel lanes and track the same input.',3),
 ex(15,'advanced',8,'Integrated first-error diagnosis and reassessment',
    'A learner writes 2(3z−4)−(z+1) → 6z−4−z+1 → 5z−3. Name the first incorrect operation, simplify, and check at z=2.',
    'First error: 2(−4) should be −8. Correct result 5z−9; at z=2 both original and result equal 1.','integrated_trace',
    ['2(3z−4)−(z+1)','claimed 6z−4−z+1','outer 2','outside − before z+1','correct 5z−9'],
    ['2(3z−4)−(z+1); claimed 6z−4−z+1','First distribution: 6z−8−(z+1)','Subtract second bracket: 6z−8−z−1','Collect: 5z−9','At z=2 both forms give 1'],
    [('Find the first illegal product','Two times minus four is minus eight, not minus four.','Stop at the earliest incorrect arrow.'),
     ('Expand the second bracket','Subtract z and also subtract one.','The minus sign applies to both terms.'),
     ('Collect after both repairs','Six z minus z is five z; minus eight minus one is minus nine.','Keep variable and constant lanes separate.'),
     ('Check the original at two','Original is two times two minus three, which equals one.','Five times two minus nine also equals one.')],
    'At z=2, original 2(6−4)−(2+1)=4−3=1 and result 10−9=1.','The learner misses two distribution signs; the first is 2×(−4).','Repair the first illegal arrow, then continue every bracket term.',4),
]

# Separate values and contexts from the worked examples; the independent
# assessment banks never appear in the lesson payload before submission.
P = [
 ('p01','Is 4a+3b=7ab valid? Give the simplest correct expression.','4a+3b.','Sort by variable label first.','Unlike a and b terms remain separate.'),
 ('p02','Simplify 9q−5q.','4q.','Carry the negative sign.','The signed coefficients are +9 and −5; their sum is 4.'),
 ('p03','Multiply (4x)(2x).','8x².','Count both x factors.','4×2=8 and x×x=x².'),
 ('p04','Expand 5(y+2).','5y+10.','Two distribution arrows.','5×y+5×2=5y+10.'),
 ('p05','Simplify 6t−(t−4).','5t+4.','The outside minus changes both terms.','6t−t+4=5t+4.'),
 ('p06','Simplify (15k+10)/5.','3k+2.','Divide both numerator terms.','15k/5+10/5=3k+2.'),
 ('p07','Evaluate 3v² at v=−2.','12.','Square only the variable in brackets.','3(−2)²=3×4=12.'),
 ('p08','Write √(u²) valid for every real u.','|u|.','The principal root is nonnegative.','For u=−4, √16=4, which equals |−4|.'),
 ('p09','Is 4(x+1) equivalent to 4x+1? Give the correct expansion.','4x+4.','Distribute four to each bracket term.','At x=1 original 8; correct 4x+4 also 8.'),
 ('p10','A learner expands 3(2w−5) as 6w−5. Correct the first error.','6w−15.','Trace the missing negative branch.','3×(−5)=−15, so the true expansion is 6w−15.'),
 ('p11','Simplify (8r²+12r)/(4r) and state the excluded value.','2r+3; r≠0.','Check the original denominator before dividing.','For r≠0 the two quotient terms are 2r and 3; r=0 is undefined.'),
 ('p12','A taxi costs R9 once and R6 per kilometre. Give C(d) and C(3).','C(d)=9+6d; C(3)=R27.','The fee occurs once.','For three kilometres cost is R9+R18=R27.'),
 ('p13','A rectangle has sides (s+4) cm and 2 cm. Find area and evaluate at s=3.','2s+8 cm²; 14 cm².','Split the length into s and four.','2(s+4)=2s+8; at three the area is 2×7=14.'),
 ('p14','Flow A doubles t then adds 3. Flow B adds 3 then doubles. Give both outputs at t=2.','A=7; B=10.','Follow each arrow in its own lane.','A: 2→4→7; B: 2→5→10.'),
 ('p15','Simplify 3(2h−3)−(h−2); verify at h=1.','5h−7; at h=1 both give −2.','Distribute three and negative one separately.','6h−9−h+2=5h−7; original 3(−1)−(−1)=−2.'),
]
M = [
 ('m01',2,'Simplify 8x−3x+2y.','5x+2y.','Eight x minus three x gives five x; y stays separate.'),
 ('m02',3,'Expand and simplify 4(a−3)−a.','3a−12.','4a−12−a=3a−12.'),
 ('m03',4,'Simplify (10b²+15b)/(5b); state the restriction.','2b+3; b≠0.','The original denominator is zero at b=0; for b≠0 the quotients are 2b and 3.'),
 ('m04',5,'A booking costs R11 once plus R7 per seat. Give C(n) and cost for 4 seats.','C(n)=11+7n; C(4)=R39.','Seven repeats four times: 28; add the one eleven-rand charge to get 39.'),
 ('m05',6,'A learner writes 2(4p−3)−(p−5) → 8p−3−p+5. Identify first error; simplify and check at p=1.','First error: 2(−3)=−6; result 7p−1; at p=1 both equal 6.','Correctly distribute two then minus one: 8p−6−p+5=7p−1; original at one is 2(1)−(−4)=6.'),
]
R = [
 ('r01','A learner says 5(2q+1)=10q+1. Diagnose and repair.','10q+5.','Five multiplies two q and one; at q=1 both correct forms equal 15.'),
 ('r02','Simplify (12c²+8c)/(4c), including a domain restriction.','3c+2; c≠0.','The original denominator 4c excludes zero. Divide both numerator terms by 4c.'),
 ('r03','A ticket costs R8 plus R3 per bag. Give C(b) and its value for 4 bags.','C(b)=8+3b; C(4)=R20.','Four bag charges cost R12; add the one R8 ticket fee.'),
]


def build():
    assert len(E)==len(P)==15 and len(M)==5 and sum(item[1] for item in M)==20 and len(R)==3
    doc=Document(); sec=doc.sections[0];sec.top_margin=sec.bottom_margin=914400
    style=doc.styles['Normal']; style.font.name='Arial';style.font.size=Pt(11)
    for key in ('Title','Heading 1','Heading 2'):
        doc.styles[key].font.name='Arial';doc.styles[key].font.color.rgb=RGBColor(0,0,0)
    title_style=doc.styles['Title'].element
    borders=title_style.find('.//'+qn('w:pBdr'))
    if borders is not None:borders.getparent().remove(borders)
    doc.add_paragraph('Grade 8 Algebraic Expressions Lesson 10',style='Title')
    doc.add_heading('Diagnosis Repair and Transfer',1)
    doc.add_paragraph('Authoring status: original draft. Teacher mathematical review and learner desktop/mobile acceptance are required before release. No source questions are copied. The document and runtime data are generated together from original authored question records in the repository. The DOCX is the review copy and remains subject to teacher approval.')
    doc.add_heading('Curriculum scope and sources',1)
    for title,url in SOURCES:doc.add_paragraph(f'{title}: {url}')
    doc.add_paragraph('The Grade 8 CAPS and 2026 ATP include like terms, multiplication and division, powers and roots of algebraic terms, substitution and equivalence between words, tables, flows and formulae. This lesson revisits those skills through first-error diagnosis and fresh transfer. Factorising trinomials and multiplying two binomials remain outside the Grade 8 target.')
    doc.add_heading('Objective, prerequisites and teaching routine',1)
    doc.add_paragraph('Objective: identify the earliest mathematically invalid transformation, explain the misconception, repair that operation, finish the expression or model, verify in the original, then attempt parallel values independently. Prerequisites: Lessons 1–9. Estimate: 110 minutes.')
    doc.add_paragraph('Show the complete original and learner claim first. Keep both visible. Reveal the operation arrow before its resulting state. Preserve earlier lines in a trace. Sort terms, branch multiplication, split a quotient, mark exponent scope, or trace contextual charges according to the question. Keep all derived values hidden before their step. End with an independent check. Do not reveal practice, mastery or reassessment answers before submission.')
    doc.add_heading('Fifteen progressive, question-specific whiteboards',1)
    for item in E:
        doc.add_heading(f"Example {item['number']}: {item['skill']}",2)
        doc.add_paragraph(f"{item['level']} · {item['marks']} marks · visual family: {item['model']['family']}")
        doc.add_paragraph('Question: '+item['q'])
        doc.add_paragraph('Initially visible objects: '+'; '.join(f"token-{i+1}: {v}" for i,v in enumerate(item['model']['tokens'][:item['model']['scene']['input_count']]))+'. Remaining objects are concealed until the taught result.')
        doc.add_paragraph('Initial state: '+item['states'][0])
        for n,step in enumerate(item['steps']):
            doc.add_paragraph(f"Step {n+1}, {step['title']}: operation first — {step['action']}; then result — {item['states'][n+1]}. Caption and narration: {step['narration']}")
        doc.add_paragraph('Complete answer: '+item['answer']+' Verify the original: '+item['verify'])
        doc.add_paragraph('First-error diagnosis: '+item['misconception']+' Repair rule: '+item['repair'])
    doc.add_heading('Fifteen independent practice questions · answers after submission',1)
    for suffix,q,a,hint,memo in P:
        doc.add_heading(suffix.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Hint: '+hint);doc.add_paragraph('Answer: '+a);doc.add_paragraph('Full memo: '+memo)
    doc.add_heading('Five mastery questions · 20 marks',1)
    for suffix,marks,q,a,memo in M:
        doc.add_heading(f'{suffix.upper()} · {marks} marks',2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Answer: '+a);doc.add_paragraph('Full memo: '+memo)
    doc.add_heading('Three parallel reassessments',1)
    for suffix,q,a,memo in R:
        doc.add_heading(suffix.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Answer: '+a);doc.add_paragraph('Full memo: '+memo)
    doc.add_heading('Release gates',1)
    doc.add_paragraph('Independent teacher check of every result and explanation, equivalence-aware answer scoring, keyboard/mobile navigation, answer gating, first-error identification and full learner browser journey are required. This authored pack alone does not certify publication.')
    OUT.parent.mkdir(parents=True,exist_ok=True);doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-10','title':'Diagnosis and transfer of expressions','source_document':OUT.name,'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'worked_examples':E,'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True);JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(OUT,JSON,payload['source_sha256'],sep='\n')


if __name__=='__main__':build()
