"""Original, deterministic Grade 8 Expressions Lesson 3 authoring source.

DBE ATP and CAPS define scope. No exercise text is copied from them.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson3_Source_Pack_v1.docx'
JSON=ROOT/'backend/app/curriculum/grade8/generated/algebraic_expressions_03.json'

def ex(n,level,marks,skill,q,answer,error,repair,family,tokens,lanes,states,moves,check):
    assert len(states)==4 and len(moves)==3 and len(tokens)==len(lanes) and 2<=len(tokens)<=8
    assert len(set(states))==4
    return dict(id=f'g8-ex-l03-w{n:02}',number=n,level=level,marks=marks,skill=skill,q=q,
        answer=answer,misconception=error,repair=repair,model={'family':family,'tokens':tokens,'lanes':lanes},
        states=states,steps=[dict(title=t,action=a,narration=v) for t,a,v in moves],verify=check)

E=[
ex(1,'foundation',2,'Count repeated x groups','Simplify 3 × 2x.','6x.',
 'Adding 3 and 2 instead of finding three groups of 2x.','Draw three rows of two x tiles and count six.',
 'factor_array',['3 groups','2x each'],['rows','columns'],
 ['3 × 2x','2x + 2x + 2x','(3 × 2)x','6x'],
 [('Build groups','Place two x tiles in each of three rows.','Three groups each hold two copies of x.'),
  ('Count coefficients','Count the six x tiles without changing their unit.','Three multiplied by two gives six copies of x.'),
  ('Write one term','Write the total coefficient beside the x unit.','The product is six x, with x to the first power.')],
 'At x=4, 3×(2×4)=24 and 6×4=24.'),
ex(2,'easy',2,'Carry a negative factor','Simplify -2 × 3a.','-6a.',
 'Dropping the negative on -2.','Represent two negative rows of three a tiles.',
 'sign_grid',['-2','3a'],['first factor','second factor'],
 ['-2 × 3a','negative × positive a-groups','-(2 × 3)a','-6a'],
 [('Read the signs','Highlight the negative first factor and positive second factor.','One negative factor makes the product negative.'),
  ('Multiply magnitudes','Count two groups of three a.','Two times three is six copies of a.'),
  ('Attach the sign','Write the minus in front of 6a.','The signed answer is negative six a.')],
 'At a=2, -2×6=-12 and -6×2=-12.'),
ex(3,'easy',2,'Multiply constants and a variable','Simplify 4x × 3.','12x.',
 'Turning x into x² although the other factor contains no x.','Count three lots of four x; keep one variable factor.',
 'factor_array',['4x','3'],['group','repetitions'],
 ['4x × 3','4x + 4x + 4x','(4 × 3)x','12x'],
 [('Repeat the x group','Show three groups of four x tiles.','The plain number repeats the existing x group three times.'),
  ('Multiply numbers','Multiply four by three.','Twelve x tiles appear in all.'),
  ('Retain the variable','Write twelve times x, with no new x factor.','The answer has x to the first power.')],
 'At x=2, (4×2)×3=24 and 12×2=24.'),
ex(4,'standard',3,'Square the same variable','Simplify 2x × 3x.','6x².',
 'Writing 6x because the second x factor was ignored.','Construct a 2x by 3x rectangle; count square x-by-x tiles.',
 'area_product',['2x width','3x length'],['height','width'],
 ['2x × 3x','(2 × 3)(x × x)','6 × x²','6x²'],
 [('Multiply each kind','Pair the coefficients and pair the variable factors.','Two times three determines the number of x-by-x tiles.'),
  ('Name the area unit','Show x times x as one x² square.','Two copies of x multiply to x squared, rather than x.'),
  ('Write area term','Combine six squares into one algebraic term.','Six x-squared units give six x squared.')],
 'At x=2, (4)(6)=24 and 6(2²)=24.'),
ex(5,'standard',3,'Multiply unlike variables','Simplify 4a × 2b.','8ab.',
 'Combining a and b as though they were like terms.','Use a-length and b-width; each unit square has area ab.',
 'area_product',['4a','2b'],['height','width'],
 ['4a × 2b','(4 × 2)(a × b)','8 × ab','8ab'],
 [('Separate factors','Select 4 and 2, then a and b.','Numbers multiply together; the different variable factors both remain.'),
  ('Count area tiles','Show eight rectangles, each with sides a and b.','Each rectangle has area ab, and there are eight.'),
  ('Write product','Combine the count and unit ab.','The product is eight ab, not eight a plus b.')],
 'At a=2,b=3, (8)(6)=48 and 8ab=48.'),
ex(6,'standard',3,'Two negatives give a positive product','Simplify (-3m)(-2m).','6m².',
 'Keeping a negative sign or omitting one m factor.','Pair sign badges first, then join two m lengths into square tiles.',
 'sign_grid',['-3m','-2m'],['first factor','second factor'],
 ['(-3m)(-2m)','(-3 × -2)(m × m)','+6 × m²','6m²'],
 [('Resolve signs','Highlight both negative factors.','A negative times a negative produces a positive product.'),
  ('Multiply variable factors','Form m-by-m squares from the two m factors.','Each m times m becomes m squared.'),
  ('Finish coefficients','Multiply three by two and retain the positive sign.','Six positive m-squared units remain.')],
 'At m=2, (-6)(-4)=24 and 6(2²)=24.'),
ex(7,'standard',4,'Powers add in multiplication','Simplify 3x² × 2x.','6x³.',
 'Adding coefficients but also adding variables as x²+x.','Show two x factors from x² and one more from x.',
 'power_stack',['3','x','x','2','x'],['coefficient','x factor','x factor','coefficient','x factor'],
 ['3x² × 2x','(3 × 2)(x × x × x)','6 × x³','6x³'],
 [('Expand variable factors','Show x² as x times x, then one more x.','The exponent tells us there are already two x factors.'),
  ('Count factors','Stack all three x factors together.','Multiplication combines two x factors and one x factor into x cubed.'),
  ('Multiply coefficients','Multiply three by two and keep the three x factors.','The coefficient is six and the power is three.')],
 'At x=2, 3(4)×2(2)=48 and 6(8)=48.'),
ex(8,'intermediate',4,'Zero factor stays zero','Simplify 0 × (-5q²).','0.',
 'Reporting -5q² after ignoring the zero factor.','Show an empty set of rows; no product tiles can appear.',
 'factor_array',['0 groups','-5q² each'],['rows','columns'],
 ['0 × (-5q²)','zero groups of -5q²','0 × any expression','0'],
 [('Show zero groups','Remove every repeated row.','Zero groups means there are no tiles to count.'),
  ('Apply the zero rule','Observe that any second factor still gives no groups.','Multiplication by zero has value zero for every q.'),
  ('Write numeric result','Write zero without a variable part.','The product is zero, rather than a signed q term.')],
 'At q=3, 0×(-45)=0 and the answer is 0.'),
ex(9,'intermediate',4,'Fraction coefficient and a square','Simplify (1/2)x × 6x.','3x².',
 'Multiplying by two instead of by one half, or leaving x to the first power.','Partition six x-length columns into two halves; each tile has x×x area.',
 'area_product',['(1/2)x','6x'],['height','width'],
 ['(1/2)x × 6x','(1/2 × 6)(x × x)','3 × x²','3x²'],
 [('Split the coefficient','Take half of six, keeping the variable factors aside.','One half of six is three.'),
  ('Pair variable factors','Join one x from each factor into an x² square.','The x factors multiply into x squared.'),
  ('Write product','Combine three with x squared.','There are three x-squared tiles.')],
 'At x=4, (2)(24)=48 and 3(16)=48.'),
ex(10,'intermediate',4,'Three factors including unlike variables','Simplify (-2a)(3b)(-a).','6a²b.',
 'Dropping a negative factor or changing b into a.','Pair both negative signs; stack two a factors and retain b.',
 'sign_grid',['-2a','3b','-a'],['factor 1','factor 2','factor 3'],
 ['(-2a)(3b)(-a)','(-2 × 3 × -1)(a × b × a)','+6(a × a)b','6a²b'],
 [('Resolve three signs','Pair the negative signs in first and third factors.','Two negatives cancel to make this product positive.'),
  ('Sort variable factors','Place both a factors together and b apart.','a times a is a squared; b is a separate factor.'),
  ('Multiply numbers','Multiply two, three and one, then attach a²b.','The complete product is positive six a squared b.')],
 'At a=2,b=3, (-4)(9)(-2)=72 and 6(4)(3)=72.'),
ex(11,'exam',5,'Rectangle area from algebraic sides','A tile has sides 3t cm and 4t cm. Find its area in cm² and evaluate at t=2.','12t² cm²; at t=2 area 48 cm².',
 'Adding sides as a perimeter or reporting a linear unit.','Grow a 3-by-4 area grid whose little square side is t cm.',
 'area_product',['3t cm','4t cm'],['height','width'],
 ['A=(3t cm)(4t cm)','(3×4)(t×t) cm²','A=12t² cm²','At t=2, A=48 cm²'],
 [('Construct area grid','Mark three rows and four columns of t-by-t squares.','Area counts square units: each small square is t centimetres by t centimetres.'),
  ('Multiply symbolic sides','Count twelve squares and label each t squared.','Three times four gives twelve, while t times t gives t squared.'),
  ('Evaluate given value','Substitute two into the completed area formula.','Twelve times four is forty-eight square centimetres.')],
 'Direct sides at t=2 are 6 cm and 8 cm; 6×8=48 cm².'),
ex(12,'exam',5,'Detect an exponent error','A learner wrote (2x²)(3x)=6x². Identify the missing operation and correct the result.','They omitted the second factor of x; the product is 6x³.',
 'Treating an exponent as a decoration rather than a count of factors.','Expose three x chips: x×x from x² and one x from the second term.',
 'power_stack',['2','x','x','3','x'],['coefficient','x factor','x factor','coefficient','x factor'],
 ['(2x²)(3x) → learner: 6x²','(2×3)(x×x×x)','6 × x³','Correct result: 6x³'],
 [('Find omitted factor','Compare the learner line with the three x chips in the original.','The second factor contributes a third x that cannot disappear.'),
  ('Recount powers','Count two x factors plus one x factor.','There are three x factors, so the exponent is three.'),
  ('Repair the line','Keep six as coefficient and replace x² with x³.','The repaired answer is six x cubed.')],
 'At x=2, original 8×6=48, wrong 6x²=24, and corrected 6x³=48.'),
ex(13,'exam',5,'Cost per learner in grouped packs','A school buys 4 packs of 3n notebooks at R2 each. Express the total cost in rand and check n=5.','R24n; at n=5 cost R120.',
 'Multiplying only four by three and forgetting the price factor.','Show four pack trays, three n notebooks per tray, and a R2 badge on each notebook.',
 'factor_array',['4 packs','3n notebooks each','R2 each'],['packs','notebooks','price'],
 ['4 × 3n × R2','(4 × 3 × 2)n rand','24n rand','At n=5, cost R120'],
 [('Count notebooks','Show four groups of three n notebooks.','Four groups of three n make twelve n notebooks.'),
  ('Apply unit price','Attach the two-rand badge to each notebook.','Each of the twelve n notebooks costs two rand.'),
  ('Substitute n','Multiply twenty-four by five.','The total is one hundred and twenty rand when n is five.')],
 'At n=5: four packs ×15 notebooks ×R2=R120; 24×5=120.'),
ex(14,'advanced',6,'Square a negative monomial','Simplify (-2p)² and explain why the result is positive.','4p².',
 'Squaring only p or keeping a negative result after multiplying two negatives.','Show two complete copies of the bracket, with two negative badges.',
 'power_stack',['(-2p) first','(-2p) second'],['factor 1','factor 2'],
 ['(-2p)²','(-2p)(-2p)','(-2×-2)(p×p)','4p²'],
 [('Expand the square','Replace the exponent 2 with two complete (-2p) factors.','The square applies to the signed coefficient and to p.'),
  ('Resolve signs and powers','Pair negative badges and join the two p factors.','Two negatives give a positive; p times p gives p squared.'),
  ('Multiply magnitudes','Multiply two by two after resolving the signs.','The result is positive four p squared.')],
 'At p=3, (-6)²=36 and 4(9)=36.'),
ex(15,'advanced',7,'Compare area expressions across two tiles','One square has side 2x cm. A rectangle has sides x cm and 3x cm. Find both areas, then the difference square minus rectangle.','Square: 4x² cm²; rectangle: 3x² cm²; difference x² cm².',
 'Adding side lengths or treating x² and x as interchangeable.','Build two scaled area grids: four x² squares beside three x² squares.',
 'area_comparison',['square side 2x','rectangle width x','rectangle length 3x'],['square','rectangle height','rectangle width'],
 ['Square (2x)²; rectangle (x)(3x)','Square 4(x×x); rectangle 3(x×x)','4x² - 3x²','Difference: x² cm²'],
 [('Build both grids','Draw a 2-by-2 square grid and a 1-by-3 rectangle grid.','The first area has four x-squared tiles; the second has three.'),
  ('Compare like area units','Align the x-squared tiles and subtract three from four.','Both are areas, so subtract only their counts of identical x-squared tiles.'),
  ('Write the difference','Show one unmatched x² tile with square-centimetre units.','The square exceeds the rectangle by x squared square centimetres.')],
 'At x=2, square 16 cm², rectangle 12 cm²; difference 4 cm² equals x² cm².'),
]
SCENES={
    1:{'rows':3,'columns':2,'unit':'x'}, 3:{'rows':3,'columns':4,'unit':'x'},
    4:{'rows':2,'columns':3,'unit':'x²'}, 5:{'rows':4,'columns':2,'unit':'ab'},
    8:{'rows':0,'columns':5,'unit':'q²'}, 9:{'rows':1,'columns':6,'unit':'x²','share':.5},
    11:{'rows':3,'columns':4,'unit':'t²'}, 13:{'rows':4,'columns':3,'unit':'n notebooks','unit_price':2},
    15:{'square_rows':2,'square_columns':2,'rectangle_rows':1,'rectangle_columns':3,'unit':'x²'},
}
for item in E:
    if item['number'] in SCENES:
        item['model']['scene']=SCENES[item['number']]

P=[
('p01','Simplify 5 × 2a.','10a.','Make five groups of 2a.','5×2=10; retain a.'),
('p02','Simplify -3 × 4q.','-12q.','One factor is negative.','-3×4=-12 and q remains.'),
('p03','Simplify 6x × 2.','12x.','Only one factor contains x.','6×2=12, so there is still one x factor.'),
('p04','Simplify 3m × 5m.','15m².','Two m factors form an m-by-m square.','3×5=15; m×m=m².'),
('p05','Simplify 2a × 7b.','14ab.','Keep both unlike factors.','2×7=14 and a×b=ab.'),
('p06','Simplify (-4r)(-3r).','12r².','Pair the two negatives.','-4×-3=12; r×r=r².'),
('p07','Simplify 2y² × 4y.','8y³.','Count all y factors.','2×4=8 and y²×y=y³.'),
('p08','Simplify 0 × (7s²).','0.','Zero groups contain no tiles.','Zero times any expression equals zero.'),
('p09','Simplify (1/3)t × 9t.','3t².','One third of nine is three.','(1/3)×9=3 and t×t=t².'),
('p10','Simplify (-2a)(5b)(-3a).','30a²b.','Pair the two minus signs.','(-2)×5×(-3)=30; a×b×a=a²b.'),
('p11','A rectangle has sides 2k cm and 7k cm. Find its area.','14k² cm².','Multiply lengths and use square units.','2×7=14 and k×k=k², so area is 14k² cm².'),
('p12','A learner says 4x² × 2x = 8x². Give the correct product.','8x³.','Count x×x and the additional x.','4×2=8; x²×x=x³.'),
('p13','Three crates each hold 4n pencils at R2 per pencil. Write the total cost.','R24n.','Multiply crates, pencils and rand per pencil.','3×4n×R2=R24n.'),
('p14','Simplify (-3u)².','9u².','Square the whole signed term.','(-3u)(-3u)=9u².'),
('p15','A square has side 3z cm and a rectangle sides z cm and 5z cm. How much larger is the square area?','4z² cm².','Compare square-unit tiles.','Square area 9z²; rectangle 5z²; difference 4z² cm².'),
]
M=[
('m01',2,'Simplify 7 × 2n.','14n.','Seven groups of 2n give fourteen n.'),
('m02',3,'Simplify (-2x)(-5x).','10x².','The two signs give positive; 2×5=10 and x×x=x².'),
('m03',4,'Simplify 3a² × 4a and verify at a=2.','12a³; at a=2 the value is 96.','3×4=12, a²×a=a³; original 12×8=96.'),
('m04',5,'A learner writes (-3p)²=-9p². Identify the first wrong action and correct it.','The square applies to the whole signed term; the result is 9p².','(-3p)(-3p)=9p²; two negatives give a positive product.'),
('m05',6,'A rectangle has sides 2x cm and 3x cm; a square has side x cm. Find their area difference and verify at x=2.','5x² cm²; at x=2 the difference is 20 cm².','Rectangle area 6x²; square x²; difference 5x²; at x=2, 24-4=20.'),
]
R=[
('r01','After a sign mistake, simplify (-4t)(-2t).','8t².','Two negatives make a positive and t×t=t².'),
('r02','After an exponent mistake, simplify 5y² × 2y.','10y³.','Multiply coefficients; count three y factors.'),
('r03','A square has side 3p cm; a rectangle has sides 2p cm and 4p cm. Find area difference and verify p=2.','p² cm²; at p=2 the difference is 4 cm².','Square area 9p²; rectangle 8p²; at p=2, 36-32=4.'),
]
assert len(E)==len(P)==15 and len(M)==5 and len(R)==3 and sum(row[1] for row in M)==20

def build():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc=Document();sec=doc.sections[0]
    sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.65);sec.left_margin=Inches(.85);sec.right_margin=Inches(.85)
    normal=doc.styles['Normal'];normal.font.name='Arial';normal.font.size=Pt(10);normal.font.color.rgb=RGBColor(30,36,48);normal.paragraph_format.space_after=Pt(5)
    for name,size in [('Title',20),('Heading 1',15),('Heading 2',12)]:
        st=doc.styles[name];st.font.name='Arial';st.font.size=Pt(size);st.font.bold=True;st.font.color.rgb=RGBColor(0,0,0)
    doc.add_paragraph('Grade 8 Algebraic Expressions Lesson 3 Source Pack','Title')
    doc.add_paragraph('Multiplying monomials · Original Athena questions · Draft for teacher review')
    doc.add_heading('Scope and teaching contract',1)
    for line in [
        'Objective: multiply integer and monomial factors, including negative and zero factors, different variables and simple powers; explain and check the product. Later examples apply area and grouped quantities.',
        'Prerequisites: Lessons 1–2, signed multiplication, repeated groups, square units, and meaning of exponents. Duration: approximately 75 minutes in one or two sessions. Mastery: 16/20 marks followed by targeted repair and parallel reassessment.',
        'Teaching: show the full original problem, reveal the factors as separate labelled objects, perform one legal operation at a time and retain prior mathematical states. Explain multiplication of numbers, signs and variables separately. End every whiteboard with a numerical check of the original and final forms.',
        'Visual contract: use actual question factors and data. Rows/columns, sign grids, factor stacks and two-area comparisons each have separate renderers. No correct final expression appears in the initial visualization. One authored narration sentence equals one caption for each operation. Every event targets a visible semantic object.',
        'Assessment: 15 original worked examples, 15 independent practice questions with full solutions, five mastery questions worth 20 marks and three parallel reassessments. Answer keys remain private in the runtime until the appropriate learner action.',
        'Curriculum scope: 2026 Grade 8 Mathematics ATP, Algebraic Expressions, multiplying integers and monomials by monomials and using exponent laws. DBE documents determine topic scope; the exercises and wording here are original.',
        'ATP: https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%208.pdf?ver=2026-01-20-202040-113',
        'CAPS: https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf',
    ]: doc.add_paragraph(line)
    doc.add_heading('Worked examples and complete animated states',1)
    for item in E:
        doc.add_heading(f"Example {item['number']}   {item['skill']}",2)
        doc.add_paragraph(f"{item['level'].title()} · {item['marks']} marks · {item['id']}. Problem: {item['q']}")
        doc.add_paragraph('Visual family: '+item['model']['family']+'; given objects: '+', '.join(f"{t} [{lane}]" for t,lane in zip(item['model']['tokens'],item['model']['lanes']))+'; scene data: '+json.dumps(item['model'].get('scene',{})))
        for n,step in enumerate(item['steps']):
            doc.add_paragraph(f"Step {n+1}: {item['states'][n]} → {item['states'][n+1]}. {step['title']}. Visual action: {step['action']} Narration and caption: {step['narration']}")
        doc.add_paragraph('Final checked step: '+item['verify'])
        doc.add_paragraph('Gated answer: '+item['answer'])
        doc.add_paragraph('First likely misconception: '+item['misconception']+' Targeted repair: '+item['repair'])
    doc.add_heading('Independent practice with complete solutions',1)
    for pid,q,a,hint,memo in P:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Hint: '+hint);doc.add_paragraph('Worked memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Mastery assessment: 20 marks',1)
    for mid,marks,q,a,memo in M:
        doc.add_heading(f'{mid.upper()}   {marks} marks',2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Parallel reassessment',1)
    for rid,q,a,memo in R:
        doc.add_heading(rid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-03','title':'Multiplying monomials',
        'source_document':OUT.name,'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
        'worked_examples':E,'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True);JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(OUT,JSON,payload['source_sha256'])

if __name__=='__main__':build()
