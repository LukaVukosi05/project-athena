"""Deterministic authored source for Grade 8 Algebraic Expressions Lesson 2.

All questions are original Athena exercises. The DBE documents determine scope,
not their wording. Run from the repository root using the bundled Python runtime.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson2_Source_Pack_v1.docx'
JSON=ROOT/'backend/app/curriculum/grade8/generated/algebraic_expressions_02.json'


def ex(number,level,marks,skill,q,answer,misconception,repair,family,tokens,lanes,states,moves,verify):
    assert len(states)==len(moves)+1,(number,len(states),len(moves))
    assert len(tokens)==len(lanes) and 2<=len(tokens)<=8
    return dict(id=f'g8-ex-l02-w{number:02}',number=number,level=level,marks=marks,
        skill=skill,q=q,answer=answer,misconception=misconception,repair=repair,
        model={'family':family,'tokens':tokens,'lanes':lanes},states=states,
        steps=[dict(title=t,action=a,narration=n) for t,a,n in moves],verify=verify)

E=[
ex(1,'foundation',2,'Add one kind of term','Simplify 3x + 2x.','5x.',
 'Writing 5x² or adding x to the coefficients as a number.',
 'Make five identical x bars and count bars, not powers.',
 'like_term_sort',['3x','+2x'],['x','x'],
 ['3x + 2x','3 x-bars beside 2 x-bars','(3 + 2)x','5x'],
 [('Name the shared unit','Select the x part of both terms.','Both groups contain the same x unit, so their counts can be added.'),
  ('Join the groups','Move the two x bars beside the three x bars.','Three copies and two copies make five copies of x.'),
  ('Write the result','Calculate 3 + 2, then retain x.','The coefficient becomes five; x is unchanged.')],
 'At x = 4, the original is 12 + 8 = 20 and 5x = 20.'),
ex(2,'easy',2,'Subtract one kind of term','Simplify 8a - 3a.','5a.',
 'Changing the sign of the remaining a term or subtracting exponents.',
 'Keep all eight a bars, remove three, and count five remaining bars.',
 'like_term_sort',['8a','-3a'],['a','a'],
 ['8a - 3a','8 a-bars with 3 marked for removal','(8 - 3)a','5a'],
 [('Identify matching units','Highlight a in both signed terms.','Both terms measure the same unknown a.'),
  ('Remove three copies','Mark three a bars for subtraction from eight.','Removing three of eight a bars leaves five.'),
  ('Write the coefficient','Evaluate 8 - 3 and retain the variable.','The simplified expression is five a.')],
 'At a = 2, 16 - 6 = 10 and 5a = 10.'),
ex(3,'easy',3,'Signed coefficients','Simplify -4m + 7m.','3m.',
 'Treating -4 as +4, or assuming a negative first term makes the total negative.',
 'Show four negative m counters and seven positive m counters, then remove zero pairs.',
 'signed_terms',['-4m','+7m'],['m','m'],
 ['-4m + 7m','4 negative m and 7 positive m counters','4 zero pairs removed; 3 positive m remain','3m'],
 [('Keep each sign','Attach the minus to 4m and plus to 7m.','The first group is negative four m, not positive four m.'),
  ('Make zero pairs','Pair each negative m with one positive m.','Each negative and positive m cancels to zero.'),
  ('Count remaining terms','Count the three unpaired positive m counters.','Three positive m remain.')],
 'At m = 2, -8 + 14 = 6 and 3m = 6.'),
ex(4,'easy',3,'Recognize unlike terms','Simplify 4x + 3y + 2x.','6x + 3y.',
 'Joining the y count with the x count to produce 9xy.',
 'Sort x and y counters into separate lanes before combining the two x groups.',
 'like_term_sort',['4x','+3y','+2x'],['x','y','x'],
 ['4x + 3y + 2x','x lane: 4x, 2x; y lane: 3y','(4 + 2)x + 3y','6x + 3y'],
 [('Sort by variable','Move both x groups into one lane and y into another.','x and y are different units; only matching units can combine.'),
  ('Add the x groups','Put two x bars beside the four x bars.','Four plus two copies give six x.'),
  ('Retain the y group','Leave the three y bars as a separate sum.','The y term remains three y.')],
 'At x = 1 and y = 2, both forms equal 12.'),
ex(5,'standard',3,'Constants and variable terms','Simplify 5p - 4 + 3p + 9.','8p + 5.',
 'Joining constants to p terms, or ignoring the negative sign on four.',
 'Sort p-bars from constant counters; add 5p+3p and -4+9 independently.',
 'like_term_sort',['5p','-4','+3p','+9'],['p','constant','p','constant'],
 ['5p - 4 + 3p + 9','p lane: 5p + 3p; constant lane: -4 + 9','p lane: 8p; constant lane: +5','8p + 5'],
 [('Sort signed terms','Put both p terms in one lane and both constants in another.','The negative four stays attached to its constant card.'),
  ('Combine each lane','Evaluate 5 + 3 and -4 + 9 separately.','The p lane gives eight p; the constants give positive five.'),
  ('Write the expression','Join the two simplified lanes without an equals sign.','Eight p plus five has the same value as the original.')],
 'At p = 2, the original is 10 - 4 + 6 + 9 = 21; 8p + 5 = 21.'),
ex(6,'standard',3,'Negative resulting coefficient','Simplify 2q - 7q + 4.','-5q + 4.',
 'Dropping the minus sign or changing the separate constant.',
 'Use two positive q and seven negative q counters; five negative q remain.',
 'signed_terms',['2q','-7q','+4'],['q','q','constant'],
 ['2q - 7q + 4','2 positive q, 7 negative q, and 4 units','(2 - 7)q + 4','-5q + 4'],
 [('Separate units','Keep the four units outside the q-counter lane.','Four is a constant and does not cancel with q.'),
  ('Remove zero pairs','Pair two positive q with two of seven negative q.','Five negative q counters remain.'),
  ('Carry the constant','Write -5q and the untouched +4.','The q coefficient is negative five, while the constant stays positive four.')],
 'At q = 2, 4 - 14 + 4 = -6 and -10 + 4 = -6.'),
ex(7,'standard',4,'Powers define term type','Simplify 3x² + 2x + 5x² - x.','8x² + x.',
 'Combining x and x² or adding their exponents when terms are only being added.',
 'Use square tiles for x² and length bars for x; sort each type separately.',
 'like_term_sort',['3x²','+2x','+5x²','-x'],['x²','x','x²','x'],
 ['3x² + 2x + 5x² - x','square lane: 3x² + 5x²; bar lane: 2x - x','8x² + (2 - 1)x','8x² + x'],
 [('Sort by variable and power','Place square x² tiles apart from length x bars.','x squared and x are unlike units.'),
  ('Count each type','Add three and five squares; remove one of two x bars.','The square lane gives eight and the bar lane gives one.'),
  ('Write both terms','Keep the square on x² and a single x bar.','The answer contains eight x squared plus x.')],
 'At x = 2, 12 + 4 + 20 - 2 = 34 and 8(4) + 2 = 34.'),
ex(8,'intermediate',4,'Subtract a whole group','Simplify (5a + 3) - (2a - 4).','3a + 7.',
 'Subtracting 2a but leaving -4 unchanged, or treating -(-4) as -4.',
 'Show two intact bracket trays and a minus badge over the entire second tray.',
 'bracket_negation',['5a','+3','-','2a','-4'],['a','constant','operator','a','constant'],
 ['(5a + 3) - (2a - 4)','5a + 3 - 2a + 4','(5 - 2)a + (3 + 4)','3a + 7'],
 [('Apply subtraction to the bracket','Place a negative sign in front of both terms in the second group.','Subtracting the whole tray changes both signed terms inside it.'),
  ('Sort like terms','Place 5a and -2a together, then +3 and +4.','Keep the new positive four after subtracting negative four.'),
  ('Combine each lane','Evaluate 5 - 2 and 3 + 4.','Three a and seven units remain.')],
 'At a = 2, (10 + 3) - (4 - 4) = 13 and 3(2) + 7 = 13.'),
ex(9,'intermediate',4,'Mixed signed variables','Simplify 2r - 3s - 5r + 4s.','-3r + s.',
 'Adding every coefficient despite different variables, or losing the minus on 5r.',
 'Sort signed r and s cards into two lanes and cancel oppositely signed copies.',
 'like_term_sort',['2r','-3s','-5r','+4s'],['r','s','r','s'],
 ['2r - 3s - 5r + 4s','r lane: 2r - 5r; s lane: -3s + 4s','(2 - 5)r + (-3 + 4)s','-3r + s'],
 [('Keep the signs while sorting','Move two r cards and negative five r together; group s cards separately.','The sign travels with each complete term.'),
  ('Count zero pairs per lane','Cancel two r pairs and three s pairs.','Three negative r and one positive s remain.'),
  ('Write the two-term result','Combine the remaining signed counters.','Negative three r plus one s is -3r + s.')],
 'At r = 2 and s = 3, 4 - 9 - 10 + 12 = -3 and -6 + 3 = -3.'),
ex(10,'intermediate',4,'Subtract a binomial','Simplify 8t - (3t + 2) + t.','6t - 2.',
 'Applying subtraction only to 3t and retaining a positive two.',
 'Subtract both cards under the bracket, then collect all t terms.',
 'bracket_negation',['8t','-','3t','+2','+t'],['t','operator','t','constant','t'],
 ['8t - (3t + 2) + t','8t - 3t - 2 + t','(8 - 3 + 1)t - 2','6t - 2'],
 [('Distribute the outer minus','Change the signs of both 3t and +2.','The minus applies to the complete bracket, including its constant.'),
  ('Gather t terms','Move 8t, -3t and +t into one lane.','All three terms have one t factor.'),
  ('Calculate the t coefficient','Evaluate 8 - 3 + 1 and retain -2.','Six t minus two is the simplified expression.')],
 'At t = 2, 16 - (6 + 2) + 2 = 10 and 6(2) - 2 = 10.'),
ex(11,'exam',5,'Perimeter with expressions','A rectangle has length x + 4 cm and width 2x - 1 cm. Find a simplified perimeter expression.','6x + 6 cm.',
 'Adding only adjacent sides or dropping the two constants from the second length.',
 'Trace each of four labelled edges; sort x lengths and constant lengths into separate lanes.',
 'rectangle',['x + 4 cm','2x - 1 cm','x + 4 cm','2x - 1 cm'],['side','side','side','side'],
 ['P = (x + 4) + (2x - 1) + (x + 4) + (2x - 1)','P = x + 4 + 2x - 1 + x + 4 + 2x - 1','P = (1 + 2 + 1 + 2)x + (4 - 1 + 4 - 1)','P = 6x + 6 cm'],
 [('Trace the full boundary','Highlight the top, right, bottom and left labels in turn.','A perimeter uses both lengths and both widths.'),
  ('Separate four complete side expressions','Remove brackets around additions without changing any signs.','Every term from each side remains present.'),
  ('Combine the two lanes','Add four x coefficients and the four signed constants.','Six x plus six centimetres measures the entire boundary.')],
 'At x = 2 cm, the sides are 6, 3, 6 and 3 cm: total 18 cm; 6(2) + 6 = 18 cm.'),
ex(12,'exam',5,'Totals from two groups','A club sells x learner tickets and 2x adult tickets, then cancels 3 learner and 2 adult tickets. Write and simplify the number of valid tickets.','3x - 5 tickets.',
 'Subtracting five from each group or counting cancelled tickets twice.',
 'Use two labelled ticket lanes; add both original groups then remove three and two physical tickets once.',
 'like_term_sort',['x learner','2x adult','-3 learner','-2 adult'],['x','x','constant','constant'],
 ['x + 2x - 3 - 2','ticket lane: x + 2x; cancelled lane: -3 - 2','(1 + 2)x + (-3 - 2)','3x - 5 tickets'],
 [('Count issued tickets','Place one x group and two x groups in the issued lane.','All tickets count as one ticket each, although their types differ.'),
  ('Account for cancellations','Remove three learner tickets and two adult tickets once.','Five total tickets no longer count.'),
  ('Write the valid total','Combine the x groups and the cancelled count.','Three x minus five tickets remain.')],
 'For x = 4, twelve tickets are issued and five cancelled, leaving seven; 3(4) - 5 = 7.'),
ex(13,'exam',5,'Spot unlike-power error','A learner claims 5u + 3u² = 8u³. Identify the first invalid operation and give the correct simplest form.','The terms are unlike; 5u + 3u² is already simplest.',
 'Adding the coefficients and powers of terms that are only joined by addition.',
 'Represent u bars and u-by-u square tiles in two different shapes; mark the proposed merge invalid.',
 'unlike_term_sort',['5u','+3u²','claim: 8u³'],['u','u²','claim'],
 ['5u + 3u²; learner claim 8u³','u bars separate from u² squares','5u and 3u² cannot merge by addition','5u + 3u² remains'],
 [('Model both term types','Place five u bars beside three u² squares.','Length units and square units are different mathematical objects.'),
  ('Find the invalid arrow','Compare the learner merge with the unchanged two groups.','Adding terms never multiplies their variable parts.'),
  ('State the valid form','Keep the two signed groups as a sum.','The original expression is already simplified.')],
 'At u = 2, the original is 10 + 12 = 22, whereas 8u³ = 64.'),
ex(14,'advanced',6,'Prove equivalence with unlike terms','Are 2x + 3y - 5x + y and -3x + 4y equivalent for all x and y? Explain and check at x = -2, y = 3.','Yes; both simplify to -3x + 4y. At (-2, 3), both equal 18.',
 'Treating one numerical check as a proof for every pair x,y.',
 'Sort x and y groups symbolically, then perform a separate numerical check after the identity is established.',
 'like_term_sort',['2x','+3y','-5x','+y'],['x','y','x','y'],
 ['2x + 3y - 5x + y','x lane: 2x - 5x; y lane: 3y + y','(2 - 5)x + (3 + 1)y','-3x + 4y for all x,y'],
 [('Partition the types','Group x terms and y terms independently.','The algebraic grouping is legal for every value of the variables.'),
  ('Simplify the coefficients','Compute 2 - 5 = -3 and 3 + 1 = 4.','The first expression becomes exactly the second for all x and y.'),
  ('Check the given pair','Substitute x = -2 and y = 3 in each expression.','Each side evaluates to eighteen; the numeric check supports the symbolic proof.')],
 'At x = -2, y = 3, original -4 + 9 + 10 + 3 = 18; target 6 + 12 = 18. Symbolic grouping proves all pairs.'),
ex(15,'advanced',7,'Integrated polynomial grouping','Simplify (4x² - 3x + 2) + (2x² + 5x - 7) - (x² - x + 1), then check x = -2.','5x² + 3x - 6; at x = -2 the value is 8.',
 'Negating only the first term in the third bracket, or merging x² and x.',
 'Preserve all three polynomial trays; reverse each sign of the subtracted tray and sort square, bar and constant lanes.',
 'grouped_polynomials',['4x² - 3x + 2','2x² + 5x - 7','- (x² - x + 1)'],['group','group','subtracted group'],
 ['(4x² - 3x + 2) + (2x² + 5x - 7) - (x² - x + 1)',
  '4x² - 3x + 2 + 2x² + 5x - 7 - x² + x - 1',
  '(4 + 2 - 1)x² + (-3 + 5 + 1)x + (2 - 7 - 1)',
  '5x² + 3x - 6'],
 [('Reverse the last tray','Remove all brackets and reverse every signed term in the subtracted group.','The minus applies to x², -x and +1.'),
  ('Sort three kinds of term','Group x² squares, x bars and constants in their own lanes.','A square term cannot be joined with a linear term.'),
  ('Finish the three coefficients','Compute 4+2-1, -3+5+1, and 2-7-1.','The simplified expression is five x squared plus three x minus six.')],
 'At x = -2, the original groups evaluate to 24, -9 and 7; 24 - 9 - 7 = 8. The simplified form gives 20 - 6 - 6 = 8.'),
]

P=[
 ('p01','Simplify 6x + x.','7x.','Seven x tiles remain.','Recognise x as one x; add 6 + 1 while retaining x.'),
 ('p02','Simplify 9a - 5a.','4a.','Count four a tiles after removing five.','Subtract 9 - 5, then retain a.'),
 ('p03','Simplify -2m + 8m.','6m.','Pair two negative m with two positive m.','The six unpaired positive m make 6m.'),
 ('p04','Simplify 3x + 4y + 2x.','5x + 4y.','Sort x and y separately.','3x + 2x = 5x; retain +4y.'),
 ('p05','Simplify 4p - 6 + 3p + 2.','7p - 4.','Keep -6 in the constant lane.','4p + 3p = 7p and -6 + 2 = -4.'),
 ('p06','Simplify 3q - 8q + 5.','-5q + 5.','Use signed q counters.','3 - 8 = -5; the +5 constant remains.'),
 ('p07','Simplify 2x² + 4x + 6x² - x.','8x² + 3x.','Square tiles cannot mix with x bars.','2x² + 6x² = 8x²; 4x - x = 3x.'),
 ('p08','Simplify (6a + 2) - (3a - 5).','3a + 7.','Reverse both signs in the subtracted bracket.','6a + 2 - 3a + 5 = 3a + 7.'),
 ('p09','Simplify 4r - 2s - 7r + 5s.','-3r + 3s.','Sort signed r and s separately.','4r - 7r = -3r; -2s + 5s = 3s.'),
 ('p10','Simplify 7t - (2t + 4) + t.','6t - 4.','Subtract the entire bracket.','7t - 2t - 4 + t = 6t - 4.'),
 ('p11','A rectangle has sides a + 2 cm and 2a + 3 cm. Simplify its perimeter.','6a + 10 cm.','Count four sides.','(a+2)+(2a+3)+(a+2)+(2a+3)=6a+10 cm.'),
 ('p12','A box contains n blue and 3n red counters. Remove four blue and two red. Write the remaining count.','4n - 6 counters.','Add the initial counts, then subtract six.','n + 3n - 4 - 2 = 4n - 6 counters.'),
 ('p13','Explain the first error in 3v + 2v² = 5v³ and state the simplest correct form.','Unlike terms; 3v + 2v² remains.','Separate bars from squares.','At v=2, 6+8=14 but 5v³=40; the terms cannot combine.'),
 ('p14','Simplify 4x - y - 6x + 3y and check at x=1, y=2.','-2x + 2y; value 2.','Group signed x and y terms before substituting.','4x-6x=-2x and -y+3y=2y; at (1,2) both sides equal 2.'),
 ('p15','Simplify (3x² + x - 4) - (x² - 2x + 1), then check x=2.','2x² + 3x - 5; value 9.','Reverse all signs in the second bracket.','3x²+x-4-x²+2x-1=2x²+3x-5; at x=2 both forms equal 9.'),
]
M=[
 ('m01',2,'Simplify 5a + 4a and explain why the exponent stays one.','9a.','Add coefficients 5+4; the unit is a, so no exponent is created.'),
 ('m02',3,'Simplify 3p - 8p + 2.','-5p + 2.','Signed coefficient 3-8=-5; retain the constant.'),
 ('m03',4,'Simplify 4x² + 3x - x² - 5x.','3x² - 2x.','Sort square terms and linear terms; 4-1=3, 3-5=-2.'),
 ('m04',5,'Diagnose the first error in (4n + 2) - (n - 5) = 4n + 2 - n - 5. Repair and simplify.','The last -5 must become +5; simplified form 3n + 7.','Subtract every term in the second bracket: 4n+2-n+5=3n+7.'),
 ('m05',6,'A rectangle has length 2x+1 cm and width x+3 cm. Simplify its perimeter and check x=2 cm.','6x + 8 cm; at x=2, perimeter 20 cm.','All four sides sum to (2x+1)+(x+3)+(2x+1)+(x+3)=6x+8; x=2 gives 5+5+5+5=20.'),
]
R=[
 ('r01','After a sign error, simplify -6k + 2k + 5.','-4k + 5.','Pair positive and negative k counters; keep five units.'),
 ('r02','After a bracket sign error, simplify (5a - 2) - (2a + 4).','3a - 6.','Subtract both terms in the second bracket, then group matching terms.'),
 ('r03','After an unlike term error, simplify 2y² + 5y - 4y² + y and check y=2.','-2y² + 6y; at y=2 the value is 4.','Sort square and linear terms separately; substitute to check both forms.'),
]
assert len(E)==len(P)==15 and len(M)==5 and len(R)==3
assert sum(row[1] for row in M)==20
assert len({x['id'] for x in E})==15


def build():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc=Document();sec=doc.sections[0]
    sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.65);sec.left_margin=Inches(.85);sec.right_margin=Inches(.85)
    st=doc.styles['Normal'];st.font.name='Arial';st.font.size=Pt(10);st.font.color.rgb=RGBColor(30,36,48);st.paragraph_format.space_after=Pt(5)
    for name,size in [('Title',20),('Heading 1',15),('Heading 2',12)]:
        s=doc.styles[name];s.font.name='Arial';s.font.size=Pt(size);s.font.bold=True;s.font.color.rgb=RGBColor(0,0,0)
    doc.add_paragraph('Grade 8 Algebraic Expressions Lesson 2 Source Pack','Title')
    doc.add_paragraph('Adding and subtracting like terms · Authored draft for teacher review')
    doc.add_paragraph('This pack contains every question and step required for the proposed lesson. It develops signed term grouping, mixed variables and powers, subtracting a whole group, and checking equivalence. The learner tries a question before its private answer and memo are revealed. All problems below were written for Athena; DBE sources establish curriculum scope.')
    doc.add_heading('Scope and teaching contract',1)
    for paragraph in [
        'Objective: add and subtract like terms while preserving signed terms, variable parts and exponents; simplify grouped expressions and explain why each legal transformation works.',
        'Prerequisites: Lesson 1 expression vocabulary, integers and zero pairs. Duration: approximately 70 minutes, or two shorter sessions. Mastery: 16 of 20 marks, then targeted repair and a new reassessment if needed.',
        'Teaching method: show the entire original question, group only equal variable parts, perform one visible operation at a time, write each result beneath the previous state, and check by substitution into the original. The verification is the final whiteboard step.',
        'Question visuals: semantic objects are defined per question below. Every initial state hides the final simplified expression; every operation appears before the result. The authored states reconstruct deterministically for Replay, Previous and Next. Caption and narration use the same authored sentence.',
        'Curriculum: 2026 Grade 8 Annual Teaching Plan, Algebraic Expressions, and CAPS Mathematics Grades 7–9, topic 2.3. The scope includes adding and subtracting like terms with rational number laws. Teacher approval is still required.',
        'Sources: https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%208.pdf?ver=2026-01-20-202040-113',
        'CAPS: https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf',
    ]:doc.add_paragraph(paragraph)
    doc.add_heading('Worked example progression',1)
    for item in E:
        doc.add_heading(f"Example {item['number']}   {item['skill']}",2)
        doc.add_paragraph(f"Difficulty: {item['level']} · {item['marks']} marks · ID: {item['id']}")
        doc.add_paragraph('Problem: '+item['q'])
        doc.add_paragraph('Visual objects: '+', '.join(f"{token} [{lane}]" for token,lane in zip(item['model']['tokens'],item['model']['lanes'])))
        doc.add_paragraph('Visual family: '+item['model']['family']+'. The renderer draws these question values, highlights one target and retains prior results.')
        for n,move in enumerate(item['steps']):
            doc.add_paragraph(f"Step {n+1}: {item['states'][n]} → {item['states'][n+1]}. {move['title']}. Animate: {move['action']} Caption and narration: {move['narration']}")
        doc.add_paragraph('Final verification: '+item['verify'])
        doc.add_paragraph('Answer for gated memo: '+item['answer'])
        doc.add_paragraph('First likely error: '+item['misconception']+' Repair: '+item['repair'])
    doc.add_heading('Independent practice and complete worked solutions',1)
    for pid,q,a,hint,memo in P:
        doc.add_heading(pid.upper(),2);doc.add_paragraph('Question: '+q)
        doc.add_paragraph('Hint: '+hint)
        doc.add_paragraph('Worked solution: '+memo)
        doc.add_paragraph('Answer: '+a)
    doc.add_heading('Mastery assessment 20 marks',1)
    for mid,marks,q,a,memo in M:
        doc.add_heading(f'{mid.upper()}   {marks} marks',2)
        doc.add_paragraph('Question: '+q);doc.add_paragraph('Memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.add_heading('Targeted parallel reassessment',1)
    for rid,q,a,memo in R:
        doc.add_heading(rid.upper(),2);doc.add_paragraph('Question: '+q);doc.add_paragraph('Memo: '+memo);doc.add_paragraph('Answer: '+a)
    doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-02','title':'Adding and subtracting like terms',
        'source_document':OUT.name,'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
        'worked_examples':E,'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True)
    JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(OUT,JSON,payload['source_sha256'])

if __name__=='__main__':build()
