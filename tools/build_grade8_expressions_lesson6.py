"""Author original Grade 8 expression powers and roots source and runtime records."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson6_Source_Pack_v1.docx'
JSON=ROOT/'backend/app/curriculum/grade8/generated/algebraic_expressions_06.json'
SOURCES=[('DBE Grade 8 Mathematics 2026 ATP','https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208'),('DBE CAPS Grades 7–9 Mathematics','https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf')]


def ex(n,level,marks,skill,q,answer,family,tokens,states,moves,verify,mistake,repair):
    assert len(states)==len(moves)+1 and len(states)>=3 and len(set(states))==len(states)
    return dict(id=f'g8-ex-l06-w{n:02}',number=n,level=level,marks=marks,skill=skill,q=q,
                answer=answer,model={'family':family,'tokens':tokens,'description':skill},
                states=states,steps=[dict(title=a,action=b,narration=c) for a,b,c in moves],
                verify=verify,misconception=mistake,repair=repair)


E=[
 ex(1,'foundation',2,'Square a positive monomial','Find (3x)².','9x².','square_grid',['3x','3x','9x²'],
    ['(3x)²','(3x)(3x)','9x²'],
    [('Open the square','Make two identical factors of the complete term 3x.','The exponent two applies to both three and x.'),('Multiply the two factors','Three times three is nine; x times x is x squared.','The area of the three x by three x square is nine x squared.')],
    'At x=2: (3·2)²=36 and 9·2²=36.','Squaring x but leaving the coefficient at three.','Draw two 3x sides; multiply coefficient by coefficient and x by x.'),
 ex(2,'easy',3,'Square a negative monomial','Find (-2a)².','4a².','signed_square',['-2a','-2a','+4a²'],
    ['(-2a)²','(-2a)(-2a)','4a²'],
    [('Duplicate the signed factor','Place two full negative 2a factors, including both parentheses.','The negative sign is inside the squared group.'),('Resolve sign and factors','Negative times negative is positive; two times two is four.','Multiplying the a factors gives a squared.')],
    'At a=3: (-6)²=36 and 4·3²=36.','Keeping a negative sign after squaring the entire term.','Use a two-sign grid before multiplying magnitudes.'),
 ex(3,'easy',3,'Cube a positive monomial','Find (2y)³.','8y³.','cube_stack',['2y','2y','2y','8y³'],
    ['(2y)³','(2y)(2y)(2y)','4y²(2y)','8y³'],
    [('Open the cube','Build three identical complete factors of 2y.','A cube uses three factors, not two.'),('Multiply the first pair','Two times two is four; y times y is y squared.','Keep the third 2y factor ready.'),('Multiply the third factor','Four times two is eight; y squared times y is y cubed.','The complete product is eight y cubed.')],
    'At y=2: (4)³=64 and 8·2³=64.','Cubing only the variable.','Stack all three coefficient and variable factors.'),
 ex(4,'standard',3,'Cube a negative monomial','Find (-3t)³.','-27t³.','signed_cube',['-3t','-3t','-3t','-27t³'],
    ['(-3t)³','(-3t)(-3t)(-3t)','9t²(-3t)','-27t³'],
    [('Show three signed factors','The whole negative 3t term appears three times.','An odd number of negative factors produces a negative result.'),('Pair two negatives','The first pair makes positive nine t squared.','A third negative factor remains.'),('Multiply the last negative','Positive nine times negative three is negative twenty seven.','The three t factors make t cubed.')],
    'At t=1: (-3)³=-27 and -27·1³=-27.','Assuming all powers erase the minus sign.','Count negative factors: odd leaves negative.'),
 ex(5,'standard',4,'Distinguish an outside minus','Compare (-4x)² and -(4x)².','16x² and -16x² respectively.','sign_scope',['(-4x)²','-(4x)²','+16x²','-16x²'],
    ['Two expressions: (-4x)² ; -(4x)²','(-4x)(-4x) ; -[(4x)(4x)]','16x² ; -16x²'],
    [('Mark exponent scope','In the first expression the minus is inside both factors; in the second it is outside the square.','Parentheses decide whether the minus is squared.'),('Resolve both paths','The first two negatives multiply to positive; the outside minus remains on the second.','These expressions differ by a sign for nonzero x.')],
    'At x=1: (-4)²=16 whereas -(4)²=-16.','Reading -(4x)² as (-4x)².','Draw a boundary around the base before multiplying.'),
 ex(6,'standard',3,'Square a product with two letters','Find (-2ab)².','4a²b².','square_grid',['-2ab','-2ab','4a²b²'],
    ['(-2ab)²','(-2ab)(-2ab)','4(a·a)(b·b)','4a²b²'],
    [('Duplicate every factor','Both negative 2ab factors contain a and b.','The exponent reaches the coefficient and both letters.'),('Resolve the coefficient and signs','Negative two times negative two is positive four.','Keep both letter pairs visible.'),('Group matching letters','Two a factors give a squared; two b factors give b squared.','The result has two separate square powers.')],
    'At a=2,b=3: (-12)²=144 and 4·4·9=144.','Applying the square only to b.','List the factor copies for both a and b.'),
 ex(7,'standard',4,'Square an existing power','Find (3x²)².','9x⁴.','power_factor_stack',['3','x·x','3','x·x','9x⁴'],
    ['(3x²)²','(3x²)(3x²)','(3·3)(x·x·x·x)','9x⁴'],
    [('Write two copies','Two complete 3x squared factors are multiplied.','An outer exponent counts copies of the entire base.'),('Collect coefficient and x factors','Three times three is nine and there are four x factors.','The inner two and outer two make four x factors.'),('Write one power','Four copies of x are x to the fourth.','The coefficient nine remains outside the variable power.')],
    'At x=2: (3·4)²=144 and 9·16=144.','Adding the exponents 2+2 incorrectly to the coefficient too.','Count variable factors, then handle coefficients separately.'),
 ex(8,'intermediate',4,'Take a principal square root','For x ≥ 0, simplify √(25x²).','5x for x ≥ 0.','root_pairs',['25','x·x','5','x'],
    ['√(25x²), x ≥ 0','√[(5·5)(x·x)], x ≥ 0','5x, x ≥ 0'],
    [('Pair the factors','Twenty five is five times five; x squared is x times x.','Each matching pair contributes one factor outside the square root.'),('Take the nonnegative root','Choose positive five and nonnegative x.','The principal square root is nonnegative under the stated condition.')],
    'At x=3: √(25·9)=15 and 5·3=15; x is nonnegative.','Assuming a square root returns both plus and minus.','The principal √ symbol selects the nonnegative value.'),
 ex(9,'intermediate',5,'Root without a sign assumption','Simplify √(9a²) for any real a.','3|a|.','absolute_root',['9','a·a','3','|a|'],
    ['√(9a²), a any real','√[(3·3)(a·a)]','3|a|'],
    [('Find matched factors','Three times three makes nine, while a times a makes a squared.','The coefficient contributes positive three.'),('Respect principal-root sign','The nonnegative number whose square is a squared is absolute a.','Use absolute a because a might be negative.')],
    'At a=-2: √(9·4)=6 and 3|-2|=6; writing 3a would give -6.','Replacing √(a²) by a for negative a.','Test a negative input and choose the nonnegative magnitude.'),
 ex(10,'intermediate',4,'Take a cube root with a negative','Find ∛(-8m³).','-2m.','cube_root',['-8','m·m·m','-2','m'],
    ['∛(-8m³)','∛[(-2)(-2)(-2)(m·m·m)]','-2m'],
    [('Build three equal factors','Negative eight is three copies of negative two; m cubed is three m factors.','An odd root can take a negative input.'),('Take one from each triple','One negative two and one m leave the cube root.','Cubing negative two m reconstructs negative eight m cubed.')],
    'At m=3: ∛(-216)=-6 and -2·3=-6.','Rejecting a negative cube root.','A negative times negative times negative stays negative.'),
 ex(11,'exam',5,'Cube a signed fraction','Find (-a/2)³.','-a³/8.','fraction_cube',['-a/2','-a/2','-a/2','-a³/8'],
    ['(-a/2)³','(-a/2)(-a/2)(-a/2)','(-a·-a·-a)/(2·2·2)','-a³/8'],
    [('Copy the fraction three times','Both numerator and denominator occur in each full factor.','The cube applies to the whole fraction.'),('Multiply top and bottom','Three negative a factors make negative a cubed; three twos make eight.','An odd number of negatives remains negative.'),('Reduce to one fraction','Keep the negative numerator over positive eight.','The final quotient is negative a cubed over eight.')],
    'At a=2: (-1)³=-1 and -8/8=-1.','Cubing the numerator but leaving denominator as two.','Make three complete fraction cards before multiplying.'),
 ex(12,'exam',5,'Diagnose a square-root error','A learner writes √(16x²) = 4x for every real x. Locate the error and repair it.','The sign condition was ignored; √(16x²)=4|x|.','error_root',['√(16x²)','claim: 4x','x=-2','4|x|'],
    ['Claim: √(16x²)=4x for every real x','At x=-2: √(16·4)=8 but 4(-2)=-8','The first error is assuming √(x²)=x for negative x','Correct: √(16x²)=4|x|'],
    [('Test a negative input','Substitute negative two in both the original and the learner claim.','The two values disagree, exposing the sign error.'),('Locate the first invalid step','Four is correct, but x is negative when x is negative.','The principal root cannot be negative.'),('Repair with magnitude','Replace x by absolute x so the answer is nonnegative.','The repaired rule works on either side of zero.')],
    'At x=-2: original 8 and repaired 4|-2|=8; at x=2 both are 8.','Accepting a single positive test as a proof for every real input.','Test both signs and restore the principal-root condition.'),
 ex(13,'exam',5,'Cube root of multiple factor groups','Simplify ∛(-27a³b³).','-3ab.','cube_root',['-27','a·a·a','b·b·b','-3ab'],
    ['∛(-27a³b³)','∛[(-3)³(a³)(b³)]','-3ab'],
    [('Group the triples','Make three negative threes, three a factors and three b factors.','Each cube-root group has three matching factors.'),('Take one factor from every triple','One negative three, one a and one b remain.','An odd root does not need absolute-value bars.')],
    'At a=-2,b=1: ∛216=6 and -3(-2)(1)=6.','Adding absolute bars to cube-root variables.','Cube a negative test value to see the original sign is preserved.'),
 ex(14,'advanced',7,'Simplify before evaluating a square','Simplify (2x)² + (x)², then evaluate at x=-3.','5x²; at x=-3 the value is 45.','compare_powers',['(2x)²','x²','4x²','x²','5x²','x=-3'],
    ['(2x)² + x²; x=-3','4x² + x²; x=-3','5x²; x=-3','5(-3)²','45'],
    [('Square the first whole term','Two x times two x makes four x squared.','The second x squared stays visible.'),('Combine like powers','Four x squared plus one x squared makes five x squared.','Both terms have the same variable power.'),('Substitute the signed input','Put negative three inside parentheses before squaring.','The square is positive nine, not negative nine.'),('Multiply the coefficient','Five multiplied by nine equals forty five.','The numerical value is forty five.')],
    'Original at x=-3: (2·-3)²+(-3)²=36+9=45.','Treating (-3)² as -9 or (2x)² as 2x².','Square complete bases, combine like terms, then substitute.'),
 ex(15,'advanced',7,'Compare square and cube roots','For x ≥ 0, simplify √(36x²) + ∛(-8x³), then evaluate at x=4.','4x; at x=4 the value is 16.','compare_roots',['√(36x²)','∛(-8x³)','6x','-2x','x=4'],
    ['√(36x²)+∛(-8x³), x ≥ 0','6x + ∛(-8x³), x ≥ 0','6x - 2x, x ≥ 0','4x, x ≥ 0','16 at x=4'],
    [('Pair square-root factors','Six times six is thirty six and x times x is x squared.','Because x is nonnegative the principal square root is six x.'),('Group cube-root triples','Negative two cubed is negative eight, while x cubed gives x.','The cube root is negative two x.'),('Collect like terms','Six x minus two x equals four x.','Retain the original x at least zero condition.'),('Evaluate the chosen input','Four times four is sixteen.','This is the value at x equal to four.')],
    'Original at x=4: √576 + ∛(-512)=24-8=16.','Forgetting the negative cube-root term or the square-root condition.','Place a sign and root badge on each independent branch.'),
]

P=[
 ('p01','Find (4x)².','16x²','Duplicate 4x as a whole factor.','(4x)(4x)=16x².'),
 ('p02','Find (-5a)².','25a²','Two negative factors make a positive.','(-5a)(-5a)=25a².'),
 ('p03','Find (3t)³.','27t³','Use three complete 3t factors.','(3t)(3t)(3t)=27t³.'),
 ('p04','Find (-2m)³.','-8m³','Count three negative factors.','(-2m)(-2m)(-2m)=-8m³.'),
 ('p05','Compare (-3y)² and -(3y)².','9y² and -9y² respectively','Mark the scope of each minus.','(-3y)²=9y²; -(3y)²=-9y².'),
 ('p06','Find (-3ab)².','9a²b²','Square the coefficient and both letters.','(-3ab)(-3ab)=9a²b².'),
 ('p07','Find (2p²)².','4p⁴','Count four copies of p.','(2p²)(2p²)=4p⁴.'),
 ('p08','For x ≥ 0, simplify √(49x²).','7x for x ≥ 0','Pair sevens and x factors.','√[(7·7)(x·x)]=7x for x ≥ 0.'),
 ('p09','Simplify √(16a²) for any real a.','4|a|','Test a negative a.','√(16a²)=4|a|; the principal root is nonnegative.'),
 ('p10','Find ∛(-64q³).','-4q','Group three negative fours.','∛[(-4q)³]=-4q.'),
 ('p11','Find (-b/3)³.','-b³/27','Cube both numerator and denominator.','(-b/3)³=(-b)³/3³=-b³/27.'),
 ('p12','A learner claims √(25n²)=5n for every real n. Correct it.','5|n|','Test n=-1.','At n=-1 the left is 5, not -5; correct form is 5|n|.'),
 ('p13','Simplify ∛(-8a³b³).','-2ab','One factor from every triple.','∛[(-2ab)³]=-2ab.'),
 ('p14','Simplify (3x)²+x², then evaluate at x=-2.','10x²; 40 at x=-2','Square the whole 3x first.','9x²+x²=10x²; 10(-2)²=40.'),
 ('p15','For x ≥ 0, simplify √(25x²)+∛(-x³), then evaluate at x=3.','4x for x ≥ 0; 12 at x=3','Use separate square and cube-root branches.','5x-x=4x; at x=3: 15-3=12.'),
]
M=[
 ('m01',2,'Find (-6u)².','36u²','(-6u)(-6u)=36u².'),
 ('m02',3,'Find (-2a)³.','-8a³','Three negative 2a factors give -8a³.'),
 ('m03',4,'Simplify √(49x²) for any real x and check x=-2.','7|x|; at x=-2 the value is 14.','√(49x²)=7|x|; √(49·4)=14.'),
 ('m04',5,'Simplify ∛(-64p³q³).','-4pq','Three copies of -4, p and q give -4pq.'),
 ('m05',6,'For x ≥ 0 simplify √(9x²)+∛(-8x³)+(2x)², then evaluate at x=2.','4x²+x for x ≥ 0; 18 at x=2.','3x-2x+4x²=4x²+x; original at x=2 is 6-4+16=18.'),
]
R=[
 ('r01','Find (-4t)³.','-64t³','(-4t)(-4t)(-4t)=-64t³.'),
 ('r02','Simplify √(36a²) for any real a.','6|a|','At a=-2, √144=12=6|-2|.'),
 ('r03','For x ≥ 0 simplify √(16x²)+∛(-27x³), then evaluate at x=5.','x for x ≥ 0; 5 at x=5.','4x-3x=x; at x=5 original is 20-15=5.'),
]

# The author marks which tokens belong to the original problem. Later tokens
# become visible only as their corresponding mathematical action is taught.
for item,count in zip(E,[2,2,3,3,2,2,4,2,2,2,3,2,3,2,2]):
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
    doc.add_paragraph('Grade 8 Algebraic Expressions Lesson 6 Source Pack',style='Title')
    doc.add_paragraph('Squares, cubes, square roots and cube roots of algebraic terms')
    doc.add_paragraph('Original Project Athena draft requiring teacher review. All 15 worked examples, 15 independent questions, five mastery questions and three reassessments below are authored and loaded by the runtime; no AI question generation is required.')
    doc.add_heading('Curriculum, prerequisites and teaching rules',1)
    for title,url in SOURCES:doc.add_paragraph(f'{title}. {url}')
    doc.add_paragraph('Prerequisites: multiply signed monomials, write repeated factors, divide integers and recognize square and cube numbers. The 2026 Grade 8 ATP specifies squares, cubes, square roots and cube roots of algebraic terms. Questions and values here are original, not copies of a study guide.')
    doc.add_paragraph('The board shows the exact question and factors first. The complete answer is hidden. Display one legal factor grouping, sign decision or root pair at a time. Keep previous mathematical states visible. A square root means the nonnegative principal root: √(a²)=|a| for unrestricted real a, or a when a≥0. A cube root preserves negative input signs. For each example check the original expression at the stated input, not merely the final form.')
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
    doc.add_paragraph('Teacher review must check every sign and root domain, first-error repairs, spoken captions, event targets, desktop/mobile stage layouts and independent-attempt gating. Existing short-text grading may reject equivalent forms; review before release.')
    OUT.parent.mkdir(parents=True,exist_ok=True);doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-06','title':'Powers and roots of algebraic terms','source_document':OUT.name,'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'worked_examples':E,'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True);JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{OUT}\n{JSON}\nSHA-256: {payload["source_sha256"]}')


if __name__=='__main__':build()
