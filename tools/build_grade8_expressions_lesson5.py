"""Original Grade 8 Algebraic Expressions Lesson 5, division by a monomial.

The DBE CAPS determines the scope. Questions and teaching sequences are
original. This script creates the reviewed-source candidate and runtime data.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson5_Source_Pack_v1.docx'
JSON = ROOT / 'backend/app/curriculum/grade8/generated/algebraic_expressions_05.json'
SOURCES = [
    ('DBE CAPS Mathematics Grades 7–9', 'https://www.education.gov.za/LinkClick.aspx?fileticket=uCNqOwfGbmc%3D&mid=1629&portalid=0&tabid=573'),
    ('Siyavula Grade 8 Algebraic Expressions Part 2', 'https://www.siyavula.com/read/za/mathematics/grade-8/algebraic-expressions-part-2'),
]


def ex(n, level, marks, skill, q, answer, family, tokens, lanes, states, moves, check, mistake, repair):
    assert len(states) == len(moves) + 1 and len(states) >= 3
    assert len(tokens) == len(lanes) and len(set(states)) == len(states)
    return dict(id=f'g8-ex-l05-w{n:02}', number=n, level=level, marks=marks, skill=skill,
                q=q, answer=answer, model={'family': family, 'tokens': tokens, 'lanes': lanes},
                states=states, steps=[dict(title=t, action=a, narration=v) for t, a, v in moves],
                verify=check, misconception=mistake, repair=repair)


E = [
    ex(1,'foundation',2,'Share a coefficient','Simplify 12x ÷ 3.','4x.','equal_share',
       ['12','x','3'],['coefficient','variable','groups'],
       ['12x ÷ 3','(12 ÷ 3)x','4x'],
       [('Separate coefficient and variable','Make three equal groups of the twelve coefficient units; keep x in each group.','Only the coefficient is shared into three groups.'),
        ('Count one group','Twelve divided by three is four.','Each group contains four x, so the quotient is four x.')],
       'At x=2: 12(2) ÷ 3=8 and 4(2)=8.',
       'Dropping x while dividing twelve.','Keep the variable attached to each equal group.'),
    ex(2,'easy',2,'Preserve a negative dividend','Simplify -15a ÷ 5.','-3a.','signed_quotient',
       ['-15','a','+5'],['signed coefficient','variable','positive divisor'],
       ['-15a ÷ 5','(-15 ÷ 5)a','-3a'],
       [('Carry the sign','Place negative fifteen over positive five without changing the sign.','A negative dividend divided by a positive number stays negative.'),
        ('Share the magnitude','Divide fifteen by five and retain a.','Three a remains negative.')],
       'At a=2: -30 ÷ 5=-6 and -3(2)=-6.',
       'Discarding the negative sign.','Check the signs before sharing the coefficient.'),
    ex(3,'easy',3,'Cancel a common variable factor','Simplify 18x² ÷ 6x for x ≠ 0.','3x, where x ≠ 0.','factor_cancel',
       ['18','x·x','6','x'],['numerator coefficient','two x factors','divisor coefficient','divisor x'],
       ['18x² ÷ 6x','(18 ÷ 6)·(x·x ÷ x)','3x'],
       [('Split factors','Divide eighteen by six and cancel exactly one x from x times x, provided x is nonzero.','The divisor contains x, so zero is excluded.'),
        ('Count factors left','Three remains with one x.','One x factor survives, giving three x.')],
       'At x=2: 72 ÷ 12=6 and 3(2)=6; x=0 is excluded.',
       'Cancelling both x factors.','Cross out only one numerator x for the one divisor x.'),
    ex(4,'standard',3,'Divide both terms by an integer','Simplify (8x + 12) ÷ 4.','2x + 3.','term_share',
       ['8x','+12','4'],['first signed term','second signed term','common divisor'],
       ['(8x + 12) ÷ 4','8x ÷ 4 + 12 ÷ 4','2x + 12 ÷ 4','2x + 3'],
       [('Create two quotient lanes','Copy the divisor four under eight x and under twelve.','Each signed term needs its own division path.'),
        ('Divide the variable term','Eight x divided by four is two x.','Keep the second quotient visible for the next step.'),
        ('Divide the constant','Twelve divided by four is three.','Two x plus three is the complete answer.')],
       'At x=2: (16+12) ÷ 4=7 and 2(2)+3=7.',
       'Dividing only the first term.','Draw a separate path from four to each bracket term.'),
    ex(5,'standard',4,'Divide a binomial by a monomial','Simplify (12x² + 18x) ÷ 6x for x ≠ 0.','2x + 3, where x ≠ 0.','factor_cancel',
       ['12x²','+18x','6x'],['first numerator term','second numerator term','common divisor'],
       ['(12x² + 18x) ÷ 6x','12x² ÷ 6x + 18x ÷ 6x','2x + 18x ÷ 6x','2x + 3'],
       [('Split the numerator','Place six x under both signed terms, with x nonzero.','The denominator acts on both terms.'),
        ('Cancel the first term','Twelve divided by six is two; x squared divided by x leaves x.','The first quotient is two x.'),
        ('Cancel the second term','Eighteen divided by six is three; x divided by x is one.','The second quotient is three, not three x.')],
       'At x=2: (48+36) ÷ 12=7 and 2(2)+3=7.',
       'Leaving an x on the second quotient.','Match each numerator x with one divisor x.'),
    ex(6,'standard',4,'Divide signed terms by a negative','Simplify (-16a + 24) ÷ (-8).','2a - 3.','signed_quotient',
       ['-16a','+24','-8'],['negative first term','positive second term','negative divisor'],
       ['(-16a + 24) ÷ (-8)','(-16a) ÷ (-8) + 24 ÷ (-8)','2a + 24 ÷ (-8)','2a - 3'],
       [('Preserve term signs','Copy negative eight beneath negative sixteen a and positive twenty four.','Each quotient has its own sign pair.'),
        ('Resolve double negative','Negative sixteen a divided by negative eight is positive two a.','Two negatives make a positive first result.'),
        ('Resolve positive over negative','Positive twenty four divided by negative eight is negative three.','The second result is negative three.')],
       'At a=2: (-32+24) ÷ (-8)=1 and 2(2)-3=1.',
       'Treating both resulting signs as positive.','Check each dividend and divisor pair separately.'),
    ex(7,'standard',4,'Three-term integer divisor','Simplify (15x² - 10x + 5) ÷ 5.','3x² - 2x + 1.','three_term_share',
       ['15x²','-10x','+5','5'],['square term','negative linear term','constant','divisor'],
       ['(15x² - 10x + 5) ÷ 5','15x² ÷ 5 - 10x ÷ 5 + 5 ÷ 5','3x² - 10x ÷ 5 + 5 ÷ 5','3x² - 2x + 5 ÷ 5','3x² - 2x + 1'],
       [('Make three quotient lanes','Send five to the square, linear and constant terms.','A trinomial needs three division paths.'),
        ('Divide the square term','Fifteen x squared divided by five is three x squared.','The x squared factor remains.'),
        ('Divide the negative term','Negative ten x divided by five is negative two x.','The second signed result stays negative.'),
        ('Divide the constant','Five divided by five is one.','The complete result has three unlike terms.')],
       'At x=2: (60-20+5) ÷ 5=9 and 12-4+1=9.',
       'Forgetting to divide the constant.','Count three input terms and three separate quotients.'),
    ex(8,'intermediate',5,'Cancel powers across three terms','Simplify (24p³ - 12p² + 6p) ÷ 6p for p ≠ 0.','4p² - 2p + 1, where p ≠ 0.','exponent_lanes',
       ['24p³','-12p²','+6p','6p'],['cubic term','square term','linear term','divisor'],
       ['(24p³ - 12p² + 6p) ÷ 6p','24p³ ÷ 6p - 12p² ÷ 6p + 6p ÷ 6p','4p² - 12p² ÷ 6p + 6p ÷ 6p','4p² - 2p + 6p ÷ 6p','4p² - 2p + 1'],
       [('Separate every quotient','Write one six p divisor for each signed term, provided p is nonzero.','The shared divisor does not disappear from later terms.'),
        ('Reduce cubic term','Twenty four over six is four; three p factors over one leave two.','The first quotient is four p squared.'),
        ('Reduce square term','Negative twelve over six is negative two; two p factors over one leave one.','The second quotient is negative two p.'),
        ('Reduce last term','Six p divided by six p is one.','The last quotient is one, not p.')],
       'At p=2: (192-48+12) ÷ 12=13 and 16-4+1=13.',
       'Subtracting exponents from only the first term.','Make a factor cancellation lane for every term.'),
    ex(9,'intermediate',4,'Cancel a shared letter, retain another','Simplify (18ab - 12a) ÷ 6a for a ≠ 0.','3b - 2, where a ≠ 0.','factor_cancel',
       ['18ab','-12a','6a'],['term with a and b','term with a','divisor with a'],
       ['(18ab - 12a) ÷ 6a','18ab ÷ 6a - 12a ÷ 6a','3b - 12a ÷ 6a','3b - 2'],
       [('Give each term a divisor','Place six a under eighteen a b and under negative twelve a.','A is cancelled only because it is a nonzero common factor.'),
        ('Keep b in first result','Eighteen over six is three; the a pair cancels, leaving b.','The first quotient is three b.'),
        ('Resolve the signed constant','Negative twelve over six is negative two; cancel the a pair.','The second quotient is negative two.')],
       'At a=2,b=3: (108-24) ÷ 12=7 and 9-2=7.',
       'Cancelling b even though it is absent from the divisor.','Only matching factors cancel.'),
    ex(10,'intermediate',4,'Recognize zero exclusion','Simplify (x² + 5x) ÷ x. State any restriction.','x + 5, where x ≠ 0.','factor_cancel',
       ['x²','+5x','x'],['square term','linear term','variable divisor'],
       ['(x² + 5x) ÷ x; x ≠ 0','x² ÷ x + 5x ÷ x; x ≠ 0','x + 5x ÷ x; x ≠ 0','x + 5; x ≠ 0'],
       [('Mark the excluded input','Since x is the divisor, x cannot equal zero; split the two terms.','A quotient cannot have a zero denominator.'),
        ('Cancel the square term','One x factor cancels from x times x.','One x survives in the first quotient.'),
        ('Cancel the second term','Five x over x leaves five.','The result x plus five retains the original exclusion.')],
       'At x=2: (4+10) ÷ 2=7 and 2+5=7; x=0 is undefined in the original.',
       'Claiming x=0 is allowed because the simplified form has no fraction.','Carry the original domain restriction into the answer.'),
    ex(11,'exam',5,'Share a contextual total','Six identical packs contain 24x + 12 counters altogether. Write an expression for the counters in one pack.','4x + 2 counters.','context_packs',
       ['24x','+12','6 packs'],['variable counters','loose counters','equal packs'],
       ['One pack = (24x + 12) ÷ 6','One pack = 24x ÷ 6 + 12 ÷ 6','One pack = 4x + 12 ÷ 6','One pack = 4x + 2 counters'],
       [('Draw six equal packs','Split both twenty four x and twelve across the six packs.','Each pack receives a share of both kinds of counters.'),
        ('Share the x counters','Twenty four x divided into six packs is four x per pack.','Each pack gets four x counters.'),
        ('Share the loose counters','Twelve divided by six is two.','Each pack contains four x plus two counters.')],
       'At x=1: total 36, each pack 6; 6·(4+2)=36.',
       'Dividing only the loose counters.','Show both types repeated in each of six packs.'),
    ex(12,'exam',5,'Diagnose a missed quotient','A learner writes (12x + 8) ÷ 4 = 3x + 8. Find the first mistake and correct it.','Eight was not divided; 3x + 2.','error_division',
       ['12x','+8','4','claim: 3x+8'],['first term','second term','divisor','learner claim'],
       ['Claim: (12x + 8) ÷ 4 = 3x + 8','Both 12x and 8 must be divided by 4','First quotient: 12x ÷ 4 = 3x','Second quotient: 8 ÷ 4 = 2','Correct: (12x + 8) ÷ 4 = 3x + 2'],
       [('Trace both paths','Inspect the written three x and eight against the two required quotient lanes.','The first term is divided; the second is merely copied.'),
        ('Check first quotient','Twelve x over four is three x.','The first part of the learner answer is correct.'),
        ('Find the first error','Eight over four is two, not eight.','The error begins at the unchanged constant.'),
        ('Replace the wrong constant','Keep three x and replace eight by two.','The repaired result is three x plus two.')],
       'At x=1: original 20 ÷ 4=5, wrong claim 11, corrected 3+2=5.',
       'Accepting the first correct term as proof of the whole answer.','Check each signed term against its own denominator.'),
    ex(13,'exam',5,'Negative monomial divisor','Simplify (6x² - 9x) ÷ (-3x) for x ≠ 0.','-2x + 3, where x ≠ 0.','signed_quotient',
       ['6x²','-9x','-3x'],['positive square term','negative linear term','negative divisor'],
       ['(6x² - 9x) ÷ (-3x)','6x² ÷ (-3x) + (-9x) ÷ (-3x)','-2x + (-9x) ÷ (-3x)','-2x + 3'],
       [('Give both terms the signed divisor','Write negative three x under each signed numerator term; x is nonzero.','The same negative divisor changes each quotient sign separately.'),
        ('Reduce positive over negative','Six over negative three is negative two; x squared over x is x.','The first result is negative two x.'),
        ('Reduce negative over negative','Negative nine x over negative three x is positive three.','The second result is positive three.')],
       'At x=2: (24-18) ÷ (-6)=-1 and -4+3=-1.',
       'Making the second quotient negative.','Use a sign pair for each term, then cancel factors.'),
    ex(14,'advanced',7,'Two quotients and subtraction','Simplify (18x² + 12x) ÷ 6x - (8x + 4) ÷ 4 for x ≠ 0.','x + 1, where x ≠ 0.','two_quotients',
       ['18x²','+12x','6x','−','8x','+4','4'],['first term','second term','first divisor','subtraction','third term','fourth term','second divisor'],
       ['(18x² + 12x) ÷ 6x - (8x + 4) ÷ 4','(3x + 2) - (8x + 4) ÷ 4','(3x + 2) - (2x + 1)','3x + 2 - 2x - 1','x + 1'],
       [('Finish first quotient','Divide both eighteen x squared and twelve x by six x.','The first bracket becomes three x plus two.'),
        ('Finish second quotient','Divide both eight x and four by four.','The second bracket becomes two x plus one.'),
        ('Subtract the whole second result','Change both signs in the second bracket before collecting.','Subtracting two x plus one means subtracting two x and one.'),
        ('Collect like terms','Three x minus two x is x; two minus one is one.','The result is x plus one with x still nonzero.')],
       'At x=2: (72+24) ÷ 12 - (16+4) ÷ 4=8-5=3 and 2+1=3.',
       'Subtracting only 2x and retaining positive one.','Put a subtraction badge on both terms of the second quotient.'),
    ex(15,'advanced',6,'Three powers over a common monomial','Simplify (12x³ - 18x² + 6x) ÷ 6x for x ≠ 0.','2x² - 3x + 1, where x ≠ 0.','exponent_lanes',
       ['12x³','-18x²','+6x','6x'],['cubic term','square term','linear term','monomial divisor'],
       ['(12x³ - 18x² + 6x) ÷ 6x','12x³ ÷ 6x - 18x² ÷ 6x + 6x ÷ 6x','2x² - 18x² ÷ 6x + 6x ÷ 6x','2x² - 3x + 6x ÷ 6x','2x² - 3x + 1'],
       [('Make three factor lanes','Put six x beneath every signed numerator term, excluding x=0.','The shared denominator reaches all three terms.'),
        ('Cancel a cubic factor','Twelve over six is two; three x factors over one leave two.','The first quotient is two x squared.'),
        ('Cancel a square factor','Negative eighteen over six is negative three; two x factors over one leave one.','The second quotient is negative three x.'),
        ('Reduce the final term','Six x divided by six x is one.','The final constant is one, while x=0 stays excluded.')],
       'At x=2: (96-72+12) ÷ 12=3 and 8-6+1=3.',
       'Keeping x on the last quotient or losing the restriction.','Cancel equal factors one lane at a time and preserve the original domain.'),
]

P = [
('p01','Simplify 20a ÷ 5.','4a','Divide the coefficient; keep a.','20a ÷ 5=(20 ÷ 5)a=4a.'),
('p02','Simplify -24t ÷ 6.','-4t','Track the negative dividend.','-24t ÷ 6=(-24 ÷ 6)t=-4t.'),
('p03','Simplify 21y² ÷ 7y for y ≠ 0.','3y, where y ≠ 0','Cancel one matching y factor.','21y² ÷ 7y=3y; y cannot be zero.'),
('p04','Simplify (10x + 15) ÷ 5.','2x + 3','Divide both terms by five.','10x ÷ 5+15 ÷ 5=2x+3.'),
('p05','Simplify (15a² + 10a) ÷ 5a for a ≠ 0.','3a + 2, where a ≠ 0','Give each term a 5a divisor.','15a² ÷ 5a+10a ÷ 5a=3a+2; a ≠ 0.'),
('p06','Simplify (-18b + 12) ÷ (-6).','3b - 2','Check two separate sign pairs.','(-18b) ÷ (-6)+12 ÷ (-6)=3b-2.'),
('p07','Simplify (12m² - 8m + 4) ÷ 4.','3m² - 2m + 1','Count three signed terms.','12m² ÷ 4-8m ÷ 4+4 ÷ 4=3m²-2m+1.'),
('p08','Simplify (18p³ - 12p² + 6p) ÷ 6p for p ≠ 0.','3p² - 2p + 1, where p ≠ 0','Subtract one exponent in each lane.','18p³ ÷ 6p-12p² ÷ 6p+6p ÷ 6p=3p²-2p+1; p ≠ 0.'),
('p09','Simplify (20ab - 15a) ÷ 5a for a ≠ 0.','4b - 3, where a ≠ 0','Only a cancels, not b.','20ab ÷ 5a-15a ÷ 5a=4b-3; a ≠ 0.'),
('p10','Simplify (y² + 7y) ÷ y. Give the restriction.','y + 7, where y ≠ 0','The original denominator excludes zero.','y² ÷ y+7y ÷ y=y+7, y ≠ 0.'),
('p11','Five identical packs contain 15x + 10 counters. Express one pack.','3x + 2 counters','Share both types among five packs.','(15x+10) ÷ 5=3x+2 counters.'),
('p12','A learner writes (16x + 12) ÷ 4 = 4x + 12. Correct it.','4x + 3','Divide the copied constant too.','16x ÷ 4+12 ÷ 4=4x+3.'),
('p13','Simplify (8x² - 12x) ÷ (-4x) for x ≠ 0.','-2x + 3, where x ≠ 0','Check each quotient sign separately.','8x² ÷ (-4x)+(-12x) ÷ (-4x)=-2x+3; x ≠ 0.'),
('p14','Simplify (12x² + 6x) ÷ 6x - (4x + 8) ÷ 4 for x ≠ 0.','x - 1, where x ≠ 0','Subtract both terms of the second quotient.','(2x+1)-(x+2)=x-1; x ≠ 0.'),
('p15','Simplify (18x³ - 12x² + 6x) ÷ 6x for x ≠ 0.','3x² - 2x + 1, where x ≠ 0','Keep the term signs and zero exclusion.','18x³ ÷ 6x-12x² ÷ 6x+6x ÷ 6x=3x²-2x+1; x ≠ 0.'),
]
M = [
('m01',2,'Simplify 28c ÷ 7.','4c','28c ÷ 7=4c.'),
('m02',3,'Simplify (-20a + 15) ÷ (-5).','4a - 3','-20a ÷ -5=4a and 15 ÷ -5=-3.'),
('m03',4,'Simplify (18x² + 12x) ÷ 6x, x ≠ 0.','3x + 2, where x ≠ 0','18x² ÷ 6x=3x; 12x ÷ 6x=2; x ≠ 0.'),
('m04',5,'Simplify (12p³ - 8p² + 4p) ÷ 4p, p ≠ 0.','3p² - 2p + 1, where p ≠ 0','Three quotients are 3p², -2p and 1; p ≠ 0.'),
('m05',6,'Simplify (12x² + 6x) ÷ 6x - (4x + 8) ÷ 4, x ≠ 0; check x=2.','x - 1, where x ≠ 0; at x=2 both forms equal 1.','(2x+1)-(x+2)=x-1; x=2: (48+12) ÷ 12-(8+8) ÷ 4=5-4=1.'),
]
R = [
('r01','Simplify (-21t + 14) ÷ (-7).','3t - 2','-21t ÷ -7=3t; 14 ÷ -7=-2.'),
('r02','Simplify (20q² + 15q) ÷ 5q for q ≠ 0.','4q + 3, where q ≠ 0','20q² ÷ 5q=4q and 15q ÷ 5q=3; q ≠ 0.'),
('r03','Simplify (18x² + 6x) ÷ 6x - (8x + 4) ÷ 4 for x ≠ 0; check x=2.','x, where x ≠ 0; at x=2 both forms equal 2.','(3x+1)-(2x+1)=x; x=2: (72+12) ÷ 12-(16+4) ÷ 4=7-5=2.'),
]


def build():
    doc=Document()
    sec=doc.sections[0]
    sec.top_margin=sec.bottom_margin=Inches(.72)
    sec.left_margin=sec.right_margin=Inches(.78)
    style=doc.styles['Normal']
    style.font.name='Arial'; style.font.size=Pt(10.5)
    style.paragraph_format.space_after=Pt(6)
    for name in ('Title','Heading 1','Heading 2'):
        doc.styles[name].font.name='Arial'
        doc.styles[name].font.color.rgb=RGBColor(0,0,0)
        properties=doc.styles[name]._element.pPr
        if properties is not None:
            for border in properties.xpath('./w:pBdr'):
                properties.remove(border)
    doc.add_paragraph('Grade 8 Algebraic Expressions Lesson 5 Source Pack',style='Title')
    doc.add_paragraph('Divide a monomial, binomial or trinomial by an integer or monomial')
    doc.add_paragraph('Authoring status: original Project Athena draft requiring teacher review. The exact 15 worked examples, 15 independent questions, five mastery questions and three reassessments are authored below and loaded by the runtime. Do not generate replacements with AI.')
    doc.add_heading('Curriculum, prerequisites and teaching rule',1)
    for title,url in SOURCES: doc.add_paragraph(f'{title}. {url}')
    doc.add_paragraph('Prerequisites: Lesson 2 signed like terms, Lesson 3 monomial multiplication and factor counting, Lesson 4 distributing an outside factor. Grade 8 CAPS includes dividing monomials, binomials and trinomials by integers or monomials. All wording and numbers in this pack are original.')
    doc.add_paragraph('The board shows the complete numerator and divisor first, with the answer hidden. Draw one divisor path to every signed numerator term. For variable divisors, state the excluded zero value before cancelling. Reveal the operation, then its partial quotient, keeping earlier results visible. Verify by multiplying the result by the original divisor at a permitted value. Diagnose the first incorrect quotient.')
    doc.add_heading('Worked examples and question-specific whiteboard directions',1)
    for item in E:
        doc.add_heading(f"Example {item['number']}  {item['skill']}",2)
        doc.add_paragraph(f"Difficulty: {item['level']}; marks: {item['marks']}; visual: {item['model']['family']}")
        doc.add_paragraph('Question: '+item['q'])
        doc.add_paragraph('Original visual objects: '+'; '.join(f'{value} ({lane})' for value,lane in zip(item['model']['tokens'],item['model']['lanes'])))
        doc.add_paragraph('Initial board: '+item['states'][0]+'; show all signed numerator terms and the divisor. Hide quotient values and final answer.')
        for index,step in enumerate(item['steps']):
            doc.add_paragraph(f"Board step {index+1}. {step['title']}: {step['action']} New state: {item['states'][index+1]}. Narration and caption: {step['narration']}")
        doc.add_paragraph('Final answer: '+item['answer']+' Verification: '+item['verify'])
        doc.add_paragraph('First misconception: '+item['misconception']+' Targeted repair: '+item['repair'])
    doc.add_heading('Independent practice and authored memos',1)
    for pid,q,a,hint,memo in P:
        doc.add_heading(pid.upper(),2)
        doc.add_paragraph('Question: '+q);doc.add_paragraph('Hint: '+hint);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Mastery check: 20 marks',1)
    for pid,marks,q,a,memo in M:
        doc.add_heading(f'{pid.upper()}  {marks} marks',2)
        doc.add_paragraph('Question: '+q);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Parallel reassessment',1)
    for pid,q,a,memo in R:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Full memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Review gates',1)
    doc.add_paragraph('Check every division by substitution, including negative and fractional cases; check no denominator is zero; confirm semantic object targets, voice/caption equality, final verification, mobile layout and independent attempt gating. Teacher review and learner browser acceptance are pending.')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-05','title':'Dividing algebraic expressions','source_document':OUT.name,
             'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'worked_examples':E,
             'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True)
    JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'{OUT}\n{JSON}\nSHA-256: {payload["source_sha256"]}')


if __name__=='__main__': build()
