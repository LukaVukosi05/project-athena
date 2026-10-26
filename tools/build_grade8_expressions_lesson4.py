"""Original authored Grade 8 Expressions Lesson 4: distributing a monomial.

DBE CAPS determines scope; all question wording and numbers here are original.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson4_Source_Pack_v1.docx'
JSON = ROOT / 'backend/app/curriculum/grade8/generated/algebraic_expressions_04.json'
SOURCES = [
    ('Department of Basic Education', 'CAPS Mathematics Grades 7 to 9', 'https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf'),
    ('Siyavula', 'Grade 8 Algebraic Expressions Part 2', 'https://www.siyavula.com/read/za/mathematics/grade-8/algebraic-expressions-part-2/08-algebraic-expressions-part-2-02'),
]

def ex(n, level, marks, skill, q, answer, mistake, repair, family, tokens, lanes, states, moves, verify, scene=None):
    assert len(states)==len(moves)+1 and len(states)>=3 and len(tokens)==len(lanes)
    assert len(set(states))==len(states)
    return dict(id=f'g8-ex-l04-w{n:02}', number=n, level=level, marks=marks, skill=skill,
        q=q, answer=answer, misconception=mistake, repair=repair,
        model={'family':family,'tokens':tokens,'lanes':lanes,**({'scene':{**scene,'segments':'|'.join(scene['segments'])}} if scene else {})},
        states=states, steps=[dict(title=t,action=a,narration=v) for t,a,v in moves],verify=verify)

E = [
ex(1,'foundation',2,'Share a positive multiplier','Expand 2(x + 3).','2x + 6.',
   'Multiplying x but leaving the 3 unchanged.','Show two copies of both x and 3, then regroup matching parts.',
   'distribute_strip',['2','x','+3'],['multiplier','first bracket term','second bracket term'],
   ['2(x + 3)','2·x + 2·3','2x + 6'],
   [('Reach both terms','Draw one arrow from 2 to x and another from 2 to 3.','Both parts inside the bracket are doubled.'),
    ('Calculate both products','Evaluate 2 times x and 2 times 3 separately.','Two x terms and six units give two x plus six.')],
   'At x=4: 2(4+3)=14 and 2(4)+6=14.'),
ex(2,'easy',2,'Preserve subtraction in a bracket','Expand 3(a - 4).','3a - 12.',
   'Treating -4 as +4.','Keep the minus sign attached to 4 while each arrow lands.',
   'signed_distribute',['3','a','-4'],['multiplier','first bracket term','signed second term'],
   ['3(a - 4)','3·a + 3·(-4)','3a - 12'],
   [('Attach the signed term','Multiply 3 by a and by the whole signed value -4.','The minus belongs to four, so the second product is negative.'),
    ('Resolve the products','Simplify 3a and 3 times negative 4.','The result is three a minus twelve.')],
   'At a=6: 3(6-4)=6 and 3(6)-12=6.'),
ex(3,'easy',3,'Distribute a negative integer','Expand -2(x + 5).','-2x - 10.',
   'Applying the minus only to x.','Put a negative badge on each of the two arrows.',
   'signed_distribute',['-2','x','+5'],['negative multiplier','first bracket term','second bracket term'],
   ['-2(x + 5)','(-2)·x + (-2)·5','-2x - 10'],
   [('Send the negative to both terms','Place negative two at x and at positive five.','Both terms are multiplied by negative two.'),
    ('Read each signed product','Calculate negative two x and negative ten.','A negative multiplier makes both positive bracket terms negative.')],
   'At x=3: -2(3+5)=-16 and -2(3)-10=-16.'),
ex(4,'standard',3,'Multiply x across a bracket','Expand x(x + 4).','x² + 4x.',
   'Writing x for x times x.','Use an x-by-x square and an x-by-four rectangle.',
   'area_distribute',['x width','x length','+4 length'],['shared side','square segment','rectangle segment'],
   ['x(x + 4)','x·x + x·4','x² + 4x'],
   [('Partition the area','Show the square x by x beside the rectangle x by 4.','Each piece shares the x height.'),
    ('Name both area units','Convert x times x to x squared and x times four to four x.','The two areas have different powers and cannot be merged.')],
   'At x=2: 2(2+4)=12 and 2²+4(2)=12.',{'segments':['x','4'],'side':'x'}),
ex(5,'standard',4,'Multiply coefficient and variable','Expand 2x(3x + 5).','6x² + 10x.',
   'Multiplying coefficients but dropping one x in the first product.','Separate coefficient pairs and x factors on the two arrows.',
   'area_distribute',['2x','3x','+5'],['shared height','first width','second width'],
   ['2x(3x + 5)','(2x)(3x) + (2x)(5)','(2·3)(x·x) + (2·5)x','6x² + 10x'],
   [('Split the rectangle','Make a 2x by 3x piece and a 2x by 5 piece.','The common height reaches each width.'),
    ('Expand each factor pair','Separate two times three and x times x; then two times five and x.','Only the first region contains two x factors.'),
    ('Name the areas','Finish six x squared and ten x.','Different powers describe different area pieces.')],
   'At x=2: 4(6+5)=44 and 6(4)+10(2)=44.',{'segments':['3x','5'],'side':'2x'}),
ex(6,'standard',4,'Negative variable multiplier','Expand -3a(2a - 4).','-6a² + 12a.',
   'Making the second product negative instead of positive.','Reveal sign badges for (-3a)(2a) and (-3a)(-4).',
   'signed_distribute',['-3a','2a','-4'],['signed multiplier','first term','negative second term'],
   ['-3a(2a - 4)','(-3a)(2a) + (-3a)(-4)','-6a² + 12a'],
   [('Attach both signed terms','Keep the negative on -3a and on -4 as they pair.','One negative product and one positive product will appear.'),
    ('Multiply the pairs','Calculate each sign, coefficient and variable separately.','Negative six a squared plus twelve a remains.')],
   'At a=2: -6(4-4)=0 and -6(4)+12(2)=0.'),
ex(7,'standard',4,'Three-term bracket','Expand 4(2m - 3n + 1).','8m - 12n + 4.',
   'Missing the middle negative term or the constant.','Use three persistent arrows, one per signed term.',
   'trinomial_branches',['4','2m','-3n','+1'],['multiplier','term 1','term 2','term 3'],
   ['4(2m - 3n + 1)','4(2m) + 4(-3n) + 4(1)','8m + 4(-3n) + 4(1)','8m - 12n + 4(1)','8m - 12n + 4'],
   [('Create three paths','Connect 4 to 2m, negative 3n and positive 1.','A trinomial has three terms, so the multiplier travels three times.'),
    ('Finish the first path','Calculate four times two m.','The first product is eight m.'),
    ('Finish the signed path','Multiply four by negative three n.','The second product is negative twelve n.'),
    ('Finish the constant path','Multiply four by one.','The last product is positive four.')],
   'At m=2,n=1: 4(4-3+1)=8 and 16-12+4=8.'),
ex(8,'intermediate',4,'Exponent across a trinomial','Expand x(2x² - 3x + 5).','2x³ - 3x² + 5x.',
   'Adding exponents to the constant or dropping an x factor.','Count the x factors in each of three paths.',
   'trinomial_branches',['x','2x²','-3x','+5'],['multiplier','cubic path','square path','linear path'],
   ['x(2x² - 3x + 5)','x(2x²) + x(-3x) + x(5)','2x³ + x(-3x) + x(5)','2x³ - 3x² + x(5)','2x³ - 3x² + 5x'],
   [('Separate the three terms','Show an x arrow to every signed bracket term.','None of the three terms can be skipped.'),
    ('Count cubic factors','Multiply x by x squared.','One x and two x factors give x cubed.'),
    ('Count square factors','Multiply x by negative three x.','Two x factors give negative three x squared.'),
    ('Finish the linear term','Multiply x by five.','The constant becomes five x.')],
   'At x=2: 2(8-6+5)=14 and 16-12+10=14.'),
ex(9,'intermediate',5,'Negative trinomial distribution','Expand -2y(3y² - 4y + 1).','-6y³ + 8y² - 2y.',
   'Changing the first sign but leaving the other signs unchanged.','Attach -2y to all three terms and resolve each sign independently.',
   'signed_distribute',['-2y','3y²','-4y','+1'],['multiplier','term 1','term 2','term 3'],
   ['-2y(3y² - 4y + 1)','(-2y)(3y²) + (-2y)(-4y) + (-2y)(1)','-6y³ + (-2y)(-4y) + (-2y)(1)','-6y³ + 8y² + (-2y)(1)','-6y³ + 8y² - 2y'],
   [('Reach each signed term','Draw three arrows from negative two y.','The negative multiplier acts on every term.'),
    ('Resolve the first path','Multiply negative two y by positive three y squared.','The first product is negative six y cubed.'),
    ('Resolve the double negative','Multiply negative two y by negative four y.','Two negative factors make positive eight y squared.'),
    ('Resolve the last path','Multiply negative two y by positive one.','The final product is negative two y.')],
   'At y=1: -2(3-4+1)=0 and -6+8-2=0.'),
ex(10,'intermediate',4,'Fractional coefficient','Expand (1/2)x(6x + 8).','3x² + 4x.',
   'Multiplying six by two rather than halving it.','Show half of each width in a two-part area model.',
   'area_distribute',['(1/2)x','6x','+8'],['half-height','first width','second width'],
   ['(1/2)x(6x + 8)','((1/2)x)(6x) + ((1/2)x)(8)','((1/2)·6)x² + ((1/2)·8)x','3x² + 4x'],
   [('Split both regions','Send one half x to six x and eight.','Halving applies to both bracket terms.'),
    ('Calculate coefficients','Take half of six and half of eight.','The coefficients become three and four.'),
    ('Keep the correct powers','Place x squared on the first product and x on the second.','Only one region multiplies x by x.')],
   'At x=2: 1(12+8)=20 and 3(4)+4(2)=20.',{'segments':['6x','8'],'side':'(1/2)x'}),
ex(11,'exam',5,'Interpret a rectangular garden','A garden is x m wide and (x + 5) m long. Expand an expression for its area.','x² + 5x m².',
   'Adding side lengths instead of multiplying for area.','Draw an x by x square and x by 5 extension with square-metre units.',
   'area_distribute',['x m width','x m length','+5 m length'],['height','first width','extra width'],
   ['Area = x(x + 5) m²','Area = x·x + x·5 m²','Area = x² + 5x m²'],
   [('Partition the garden','Divide the long side into x metres and five metres.','The common width x is multiplied by both pieces.'),
    ('Count square metres','Add the two region areas.','The square has area x squared and the extension has area five x.')],
   'At x=3 m: original area 3·8=24 m² and 3²+5·3=24 m².',{'segments':['x','5'],'side':'x'}),
ex(12,'exam',5,'Distribute and collect like terms','Simplify 3(x + 2) + 2x.','5x + 6.',
   'Multiplying 2x by three although it lies outside the bracket.','Draw a boundary around the bracket; the outside 2x remains untouched.',
   'compare_paths',['3','x','+2','+2x outside'],['multiplier','term 1','term 2','separate addend'],
   ['3(x + 2) + 2x','3x + 3(2) + 2x','3x + 6 + 2x','5x + 6'],
   [('Respect bracket boundary','Send three only to x and two inside the bracket.','The separate plus two x stays outside the distribution.'),
    ('Finish the constant','Evaluate three times two.','The constant contribution is six.'),
    ('Collect matching x terms','Join three x and two x.','Five x and six are unlike terms, so keep both.')],
   'At x=4: 3(4+2)+2(4)=26 and 5(4)+6=26.'),
ex(13,'exam',6,'Unlike variable trinomial','Expand -2(3a - 4b + 5).','-6a + 8b - 10.',
   'Treating -4b as positive inside the bracket.','Show the signed term cards before the three arrows land.',
   'trinomial_branches',['-2','3a','-4b','+5'],['negative multiplier','term 1','term 2','term 3'],
   ['-2(3a - 4b + 5)','(-2)(3a) + (-2)(-4b) + (-2)(5)','-6a + (-2)(-4b) + (-2)(5)','-6a + 8b + (-2)(5)','-6a + 8b - 10'],
   [('Separate every signed term','Draw a path to 3a, -4b and +5.','The sign stays attached to its own term.'),
    ('Finish a path','Calculate negative two times three a.','The first term is negative six a.'),
    ('Use the double negative','Calculate negative two times negative four b.','The second term is positive eight b.'),
    ('Finish the constant','Calculate negative two times five.','The last term is negative ten.')],
   'At a=2,b=1: -2(6-4+5)=-14 and -12+8-10=-14.'),
ex(14,'advanced',6,'Find a false distribution','A learner claims 2(x + 3) = 2x + 3. Find the first wrong step and repair it.','The 3 was not doubled; 2x + 6.',
   'Checking only the x part of a claimed expansion.','Compare the claimed route and two correct arrows with the undoubled 3 marked.',
   'compare_paths',['2','x','+3','claim: 2x+3'],['multiplier','term 1','term 2','learner claim'],
   ['Claim: 2(x + 3) = 2x + 3','2·x + 2·3 must both appear','The learner wrote 2x + 3 instead of 2x + 6','Correct expansion: 2x + 6'],
   [('Compare both routes','Put the learner claim beside an arrow for each bracket term.','The claimed route has only one completed multiplication.'),
    ('Locate the first mistake','Highlight the second path, where three was copied unchanged.','Two must multiply three as well as x.'),
    ('Repair and check','Replace the incorrect constant by six.','The correct expansion is two x plus six.')],
   'At x=1: original 2(1+3)=8, wrong claim 2(1)+3=5, repair 2(1)+6=8.'),
ex(15,'advanced',7,'Two distributions and simplification','Simplify 2x(x + 3) - x(x - 2).','x² + 8x.',
   'Failing to subtract both terms from the second product.','Keep two bracket strips separate, then place negative badges on both second-strip products.',
   'compare_paths',['2x','x','+3','−','x','x','-2'],['first multiplier','first term','first extra','difference','second multiplier','second term','second extra'],
   ['2x(x + 3) - x(x - 2)','2x² + 6x - (x² - 2x)','2x² + 6x - x² + 2x','x² + 8x'],
   [('Expand each bracket independently','Draw two arrows from 2x and two arrows from x.','Each multiplier acts only within its own bracket.'),
    ('Subtract the whole second expansion','Distribute the minus to x squared and to negative two x.','The minus reverses both signs in the second group.'),
    ('Collect like powers','Combine two x squared minus x squared, and six x plus two x.','The simplified result is x squared plus eight x.')],
   'At x=2: 4(5)-2(0)=20 and 2²+8(2)=20.'),
]

P = [
('p01','Expand 5(t + 2).','5t + 10','Double-check that 5 reaches the constant.','5(t+2)=5t+5·2=5t+10.'),
('p02','Expand 4(b - 3).','4b - 12','Keep the negative with 3.','4(b-3)=4b+4(-3)=4b-12.'),
('p03','Expand -3(k + 2).','-3k - 6','A negative factor reaches both terms.','-3(k+2)=(-3)k+(-3)2=-3k-6.'),
('p04','Expand y(y + 6).','y² + 6y','y multiplied by y gives y squared.','y(y+6)=y·y+y·6=y²+6y.'),
('p05','Expand 3z(2z + 4).','6z² + 12z','Separate coefficients and variable factors.','3z(2z+4)=6z²+12z.'),
('p06','Expand -2c(3c - 5).','-6c² + 10c','Two negative factors give a positive second product.','-2c(3c-5)=-6c²+10c.'),
('p07','Expand 2(4m - 3n + 7).','8m - 6n + 14','Count three signed terms.','2·4m+2(-3n)+2·7=8m-6n+14.'),
('p08','Expand a(3a² - 2a + 4).','3a³ - 2a² + 4a','Count factors of a on each path.','a(3a²-2a+4)=3a³-2a²+4a.'),
('p09','Expand -3q(2q² - q + 2).','-6q³ + 3q² - 6q','Track each product sign.','-3q(2q²-q+2)=-6q³+3q²-6q.'),
('p10','Expand (1/2)p(4p + 6).','2p² + 3p','Take half of each coefficient.','(1/2)p(4p+6)=2p²+3p.'),
('p11','A rectangle is r m wide and (r + 7) m long. Express its area after expansion.','r² + 7r m²','Multiply the width by both parts of the length.','r(r+7)=r²+7r square metres.'),
('p12','Simplify 4(x + 1) + 3x.','7x + 4','Three x lies outside the bracket.','4x+4+3x=7x+4.'),
('p13','Expand -3(2u - 5v + 4).','-6u + 15v - 12','Keep the sign of each bracket term.','-6u+15v-12.'),
('p14','A learner says 5(n - 2)=5n - 2. Correct the expansion.','5n - 10','Five must multiply negative two.','5(n-2)=5n+5(-2)=5n-10.'),
('p15','Simplify 3x(x + 2) - x(x - 4).','2x² + 10x','Subtract the complete second expansion.','3x²+6x-(x²-4x)=2x²+10x.'),
]
M = [
('m01',2,'Expand 6(a + 2).','6a + 12','Six reaches a and two: 6a+12.'),
('m02',3,'Expand -4(y - 3).','-4y + 12','Negative four times negative three is positive twelve.'),
('m03',4,'Expand 2x(3x + 4).','6x² + 8x','First term contains x·x; second contains one x.'),
('m04',5,'Expand 3(2p - q + 5).','6p - 3q + 15','Three arrows produce three signed products.'),
('m05',6,'Simplify 2x(x + 4) - x(x - 1), then check x=2.','x² + 9x; at x=2 both forms equal 22.','2x²+8x-(x²-x)=x²+9x; x=2: 2·2·6-2·1=22 and 4+18=22.'),
]
R = [
('r01','Expand -5(t - 2).','-5t + 10','Negative five times negative two is positive ten.'),
('r02','Expand 4a(a + 3).','4a² + 12a','Four a times a is four a squared; four a times three is twelve a.'),
('r03','Simplify 2x(x + 5) - x(x - 3), then check x=2.','x² + 13x; at x=2 both forms equal 30.','2x²+10x-(x²-3x)=x²+13x; x=2: 4·7-2(-1)=30 and 4+26=30.'),
]

def build():
    doc=Document();sec=doc.sections[0];sec.top_margin=sec.bottom_margin=Inches(.72)
    sec.left_margin=sec.right_margin=Inches(.78)
    style=doc.styles['Normal'];style.font.name='Arial';style.font.size=Pt(10.5)
    style.paragraph_format.space_after=Pt(6)
    for name in ('Title','Heading 1','Heading 2'):
        doc.styles[name].font.name='Arial'
        doc.styles[name].font.color.rgb=RGBColor(0,0,0)
        props=doc.styles[name]._element.pPr
        if props is not None:
            for border in props.xpath('./w:pBdr'):
                props.remove(border)
    doc.add_paragraph('Grade 8 Algebraic Expressions Lesson 4 Source Pack',style='Title')
    doc.add_paragraph('Distributing a monomial across a binomial or trinomial')
    doc.add_paragraph('Authoring status: original Project Athena draft for teacher review. It follows Lesson 3 and covers the Grade 8 CAPS expansion scope. The 15 worked examples, 15 independent questions, five mastery questions and three reassessments below are the complete authored bank used by the runtime; do not replace them with AI output.')
    doc.add_heading('Curriculum and originality',1)
    for owner,title,url in SOURCES:doc.add_paragraph(f'{owner}: {title}. {url}')
    doc.add_paragraph('These sources were used to verify scope and progression. All questions, numbers, explanations and visual directions below are original. Human mathematical and classroom review is still required.')
    doc.add_heading('Teaching rule',1)
    doc.add_paragraph('Preserve each signed bracket term. Show the complete problem first; reveal a path from the outside multiplier to each term; display the legal multiplication before the resulting partial product; then check the final expression by numerical substitution. A wrong learner path stays visible when diagnosed. Do not show the final answer initially.')
    doc.add_heading('Worked examples and exact whiteboard directions',1)
    for item in E:
        doc.add_heading(f"Example {item['number']}  {item['skill']}",2)
        doc.add_paragraph(f"Difficulty: {item['level']}; marks: {item['marks']}; visual: {item['model']['family']}")
        doc.add_paragraph('Question: '+item['q'])
        doc.add_paragraph('Given objects and roles: '+ '; '.join(f'{label} ({lane})' for label,lane in zip(item['model']['tokens'],item['model']['lanes'])))
        doc.add_paragraph('Initial board: '+item['states'][0]+'; show the multiplier and every signed bracket term. Keep all results hidden.')
        for index,step in enumerate(item['steps']):
            doc.add_paragraph(f"Board step {index+1}. {step['title']}: {step['action']} Visible result: {item['states'][index+1]} Narration and caption: {step['narration']}")
        doc.add_paragraph('Final answer: '+item['answer']+' Verification: '+item['verify'])
        doc.add_paragraph('First misconception: '+item['misconception']+' Targeted repair: '+item['repair'])
    doc.add_heading('Independent practice with authored answers',1)
    for pid,q,a,hint,memo in P:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Hint: '+hint);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Mastery check 20 marks',1)
    for pid,marks,q,a,memo in M:
        doc.add_heading(f'{pid.upper()}  {marks} marks',2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Parallel reassessment',1)
    for pid,q,a,memo in R:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    OUT.parent.mkdir(parents=True,exist_ok=True);doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-04','title':'Distributing a monomial','source_document':OUT.name,
        'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'worked_examples':E,
        'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True);JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{OUT}\n{JSON}\nSHA-256: {payload["source_sha256"]}')

if __name__=='__main__':build()
