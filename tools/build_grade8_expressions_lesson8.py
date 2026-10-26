"""Original mixed-method simplification pack; the DOCX is the authored source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'docs/curriculum/grade8/algebraic-expressions/Project_Athena_Grade8_Algebraic_Expressions_Lesson8_Source_Pack_v1.docx'
JSON = ROOT/'backend/app/curriculum/grade8/generated/algebraic_expressions_08.json'
SOURCES = [
 ('DBE Grade 8 Mathematics 2026 Annual Teaching Plan','https://www.education.gov.za/LinkClick.aspx?fileticket=E68Ig0s3y4U%3D&mid=10749&portalid=0&tabid=3208'),
 ('DBE CAPS Mathematics Grades 7–9','https://www.education.gov.za/Portals/0/CD/National%20Curriculum%20Statements%20and%20Vocational/CAPS%20SP%20%20MATHEMATICS%20GR%207-9.pdf'),
]

def ex(n,level,marks,skill,q,answer,family,tokens,states,moves,verify,mistake,repair,inputs=2):
    assert len(states)==len(moves)+1 and len(states)>=3 and len(set(states))==len(states)
    assert 1<=inputs<len(tokens)<=8
    return dict(id=f'g8-ex-l08-w{n:02}',number=n,level=level,marks=marks,skill=skill,q=q,
      answer=answer,model={'family':family,'tokens':tokens,'description':skill,'scene':{'input_count':inputs}},
      states=states,steps=[dict(title=a,action=b,narration=c) for a,b,c in moves],
      verify=verify,misconception=mistake,repair=repair)

E=[
 ex(1,'foundation',2,'Sort like terms','Simplify 3x+5x.','8x.','term_bins',['3x','+5x','8x'],
    ['3x+5x','(3+5)x','8x'], [('Sort the matching tiles','Place both x terms in one bin.','Both tiles contain one x, so add their coefficients.'),('Combine coefficients','Add three and five, then keep x.','Three x units and five x units make eight x units.')],
    'At x=2: 3(2)+5(2)=16 and 8(2)=16.','Adding x to its coefficient.','Count the x tiles and keep the x label.'),
 ex(2,'easy',3,'Keep the signed constant','Simplify 4a+2-a.','3a+2.','term_bins',['4a','+2','-a','3a+2'],
    ['4a+2-a','(4a-a)+2','(4-1)a+2','3a+2'], [('Separate kinds','Move positive two to the constant bin and minus a beside four a.','A constant cannot join an a term.'),('Read the hidden coefficient','Write minus a as minus one a.','The sign belongs to the a term.'),('Collect the a terms','Four minus one is three.','Leave the constant two unchanged.')],
    'At a=2: 8+2-2=8 and 3(2)+2=8.','Combining two with a or losing the minus.','Place different powers and constants in separate bins.'),
 ex(3,'standard',4,'Distribute then collect','Simplify 2(x+3)+x.','3x+6.','distribute_collect',['2(x+3)','+x','2x+6','3x+6'],
    ['2(x+3)+x','2x+6+x','(2x+x)+6','3x+6'], [('Draw both distribution arrows','Multiply two by x and by positive three.','The outside factor belongs to every term inside the bracket.'),('Find the matching x terms','Group two x and one x; six stays a constant.','Only like terms share a bin.'),('Combine the x count','Two x plus one x equals three x.','The final constant is still six.')],
    'At x=2: 2(5)+2=12 and 3(2)+6=12.','Multiplying only the x inside the bracket.','Trace both arrows before collecting terms.'),
 ex(4,'standard',4,'Distribute a subtraction','Simplify 5(y-2)-2y.','3y-10.','distribute_collect',['5(y-2)','-2y','5y-10','3y-10'],
    ['5(y-2)-2y','5y-10-2y','(5y-2y)-10','3y-10'], [('Multiply both bracket terms','Five times y is five y; five times negative two is negative ten.','The negative constant keeps its sign.'),('Sort matching y terms','Five y and negative two y belong together.','Negative ten is not a y term.'),('Combine y counts','Five minus two is three.','Three y minus ten is the simplified expression.')],
    'At y=3: 5(1)-6=-1 and 9-10=-1.','Writing +10 after distributing a negative term.','Attach a minus card to the two before multiplying.'),
 ex(5,'standard',4,'Distribute a negative multiplier','Simplify -3(t-4)+t.','-2t+12.','signed_distribution_collect',['-3(t-4)','+t','-3t+12','-2t+12'],
    ['-3(t-4)+t','-3t+12+t','(-3t+t)+12','-2t+12'], [('Keep the signed multiplier together','Negative three times t is negative three t; negative three times negative four is plus twelve.','Two negative factors make a positive constant.'),('Place the remaining t beside negative three t','The extra t is positive one t.','Collect only like variable terms.'),('Add signed coefficients','Negative three plus one is negative two.','The plus twelve survives unchanged.')],
    'At t=2: -3(-2)+2=8 and -4+12=8.','Turning the bracket constant into negative twelve.','Show the two negative chips multiplying before writing plus twelve.'),
 ex(6,'standard',4,'Divide each term then collect','Simplify (12x+8)÷4+3x.','6x+2.','quotient_collect',['(12x+8)÷4','+3x','3x+2','6x+2'],
    ['(12x+8)÷4+3x','12x÷4+8÷4+3x','3x+2+3x','6x+2'], [('Split the complete numerator','Divide both twelve x and eight by four.','The division bar covers the two-term numerator.'),('Calculate both quotients','Twelve x over four is three x; eight over four is two.','Keep the additional three x outside the quotient.'),('Combine like terms','Three x plus three x gives six x.','Two is a constant and remains separate.')],
    'At x=2: (24+8)/4+6=14 and 12+2=14.','Dividing twelve x but not eight.','Draw one quotient lane for each numerator term.'),
 ex(7,'intermediate',5,'Expand two brackets independently','Simplify 2(3a-2)+3(a+1).','9a-1.','dual_distribution_collect',['2(3a-2)','+3(a+1)','6a-4','3a+3','9a-1'],
    ['2(3a-2)+3(a+1)','6a-4+3a+3','(6a+3a)+(-4+3)','9a-1'], [('Expand both independent groups','First group becomes six a minus four; second becomes three a plus three.','Keep the two arrow pairs visible.'),('Build variable and constant bins','Put six a with three a, and negative four with positive three.','Do not combine unlike kinds.'),('Total both bins','Nine a and negative one remain.','The simplified result is nine a minus one.')],
    'At a=2: 2(4)+3(3)=17 and 18-1=17.','Distributing only the first bracket.','Complete and colour both bracket paths before sorting.'),
 ex(8,'intermediate',5,'Subtract a whole bracket','Simplify 4x-(2x-3).','2x+3.','negative_bracket',['4x','-(2x-3)','-2x+3','2x+3'],
    ['4x-(2x-3)','4x-2x+3','(4x-2x)+3','2x+3'], [('Distribute minus one','Subtract two x and subtract negative three, which becomes plus three.','The minus belongs to every bracket term.'),('Group the x terms','Four x minus two x leaves two x.','Positive three remains outside the group.'),('State the result','Write two x plus three.','Check the flipped sign on the former negative three.')],
    'At x=2: 8-(4-3)=7 and 4+3=7.','Changing only the first bracket sign.','Mark a negative-one arrow to each term.'),
 ex(9,'intermediate',5,'Preserve a nonzero divisor','Simplify (18p²+12p)÷6p+2p, where p≠0.','5p+2, for p≠0.','variable_quotient_collect',['(18p²+12p)÷6p','+2p','p≠0','3p+2','5p+2'],
    ['(18p²+12p)÷6p+2p; p≠0','18p²÷6p+12p÷6p+2p','3p+2+2p; p≠0','5p+2; p≠0'], [('Divide each numerator term','Eighteen p squared divided by six p is three p; twelve p divided by six p is two.','Cancellation needs p to be nonzero.'),('Expose the constant and extra p','Keep two as a constant while adding the outside two p.','The divisor restriction remains attached.'),('Collect p terms','Three p plus two p is five p.','The original expression is undefined at zero, even though the simplified form is defined there.')],
    'At p=2: (72+24)/12+4=12 and 10+2=12; p=0 is excluded.','Cancelling p at zero or turning 12p÷6p into 2p.','Cancel one p only after stating p≠0.',3),
 ex(10,'exam',5,'Do not combine unlike powers','Simplify 3x²+2x-x²+4x.','2x²+6x.','power_bins',['3x²','+2x','-x²','+4x','2x²+6x'],
    ['3x²+2x-x²+4x','(3x²-x²)+(2x+4x)','(3-1)x²+(2+4)x','2x²+6x'], [('Separate powers','Place x squared terms in one row and x terms in another.','One x and x squared are unlike term types.'),('Read the signs in each row','Three minus one square units; two plus four linear units.','Only the coefficients in the same row combine.'),('Complete both rows','Two x squared plus six x.','Do not invent an x cubed term.')],
    'At x=2: 12+4-4+8=20 and 8+12=20.','Combining x and x² as x³.','Use separate x and x² tiles, never multiply while adding.',4),
 ex(11,'exam',5,'Diagnose the first missed distribution','A learner writes 2(x+4)+3x=2x+4+3x=5x+4. Find the first error and simplify correctly.','The 4 was not multiplied by 2; 5x+8.','distribution_error',['2(x+4)+3x','claim: 2x+4+3x','2x+8+3x','5x+8'],
    ['Original: 2(x+4)+3x; learner: 2x+4+3x','First error: 2×4 was written 4, not 8','Repair: 2x+8+3x','Correct: 5x+8'], [('Compare the first changed line','The arrow from two to positive four was missed.','The first error appears before like terms are collected.'),('Repair the bracket expansion','Multiply two by x and by four.','The correct expanded form is two x plus eight plus three x.'),('Collect x terms','Two x and three x make five x; eight stays.','The repaired answer is five x plus eight.')],
    'At x=1: original 2(5)+3=13; 5(1)+8=13; learner 5(1)+4=9.','Trusting a later line after the first incorrect arrow.','Replay only the missing 2×4 arrow then retry.'),
 ex(12,'exam',6,'Simplify a contextual perimeter','A rectangle has length (x+4) cm and width (2x-1) cm. Write a simplified expression for its perimeter and find it at x=3.','P=6x+6 cm; at x=3, P=24 cm.','perimeter_mixed',['length: x+4 cm','width: 2x-1 cm','P=2(l+w)','6x+6 cm','24 cm'],
    ['l=x+4 cm; w=2x-1 cm; P=2(l+w)','P=2[(x+4)+(2x-1)] cm','P=2(3x+3) cm','P=6x+6 cm','At x=3: P=24 cm'], [('Trace all four sides','Place both different dimensions into two copies each.','Perimeter counts two lengths and two widths.'),('Combine inside the grouped sum','One x plus two x makes three x; four minus one gives three.','Simplify the inner length-plus-width before doubling.'),('Double the complete group','Two times three x plus three gives six x plus six centimetres.','Distribute two to both parts.'),('Use the given value','At three the perimeter is eighteen plus six, or twenty four centimetres.','Verify with four concrete sides.')],
    'At x=3: length 7 cm, width 5 cm; 7+5+7+5=24 cm.','Using area units or forgetting two sides.','Trace each of the four boundaries before substituting.',3),
 ex(13,'exam',6,'Prove two forms equivalent','Show that 3(x-2)+2(x+1) simplifies to 5x-4. Check at x=2.','5x-4; both forms give 6 at x=2.','equivalent_mixed',['3(x-2)','+2(x+1)','claimed: 5x-4','3x-6+2x+2','5x-4'],
    ['3(x-2)+2(x+1) compared with 5x-4','3x-6+2x+2','(3x+2x)+(-6+2)','5x-4','At x=2: both equal 6'], [('Expand both sides of the sum','Three multiplies both first terms; two multiplies both second terms.','Distribution is an identity for every x.'),('Sort like terms','Put x terms together and signed constants together.','The brackets are no longer needed after their products are shown.'),('Compute the general simplified form','Five x minus four matches the claim.','This algebra shows equivalence for every x.'),('Check one numerical case','At x=2 both forms give six.','A single input illustrates rather than proves the general identity.')],
    'For all x distribution gives 5x-4; at x=2 original 3(0)+2(3)=6 and 5(2)-4=6.','Treating one matching input as the proof.','Derive the identity before substituting the check value.',3),
 ex(14,'advanced',7,'Choose order across three operations','Simplify 2(3x-4)-(x+5)+(12x+6)÷3.','9x-11.','layered_mixed',['2(3x-4)','-(x+5)','(12x+6)÷3','6x-8 -x-5 +4x+2','9x-11'],
    ['2(3x-4)-(x+5)+(12x+6)÷3','6x-8-(x+5)+(12x+6)÷3','6x-8-x-5+4x+2','(6x-x+4x)+(-8-5+2)','9x-11'], [('Expand the first bracket','Two times three x is six x and two times negative four is negative eight.','Leave the other two groups intact for now.'),('Finish the remaining paths','Distribute minus one and divide both numerator terms by three.','Keep the sign switch and quotient in separate lanes.'),('Sort matching term types','Collect six x, negative x and four x; group the three signed constants.','An x term cannot combine with a constant.'),('Add each signed group','Six minus one plus four is nine; negative eight minus five plus two is negative eleven.','The result is nine x minus eleven.')],
    'At x=2: 2(2)-7+(24+6)/3=7 and 18-11=7.','Losing the negative bracket or dividing only one numerator term.','Finish each operation lane before merging them.',3),
 ex(15,'advanced',8,'Simplify with a restricted variable divisor','Simplify (18x²-12x)÷6x-2(x-3)+x, where x≠0.','2x+4, where x≠0.','layered_quotient_mixed',['(18x²-12x)÷6x','-2(x-3)','+x','x≠0','2x+4'],
    ['(18x²-12x)÷6x-2(x-3)+x; x≠0','3x-2-2(x-3)+x','3x-2-2x+6+x','(3x-2x+x)+(-2+6)','2x+4; x≠0'], [('Split and divide the numerator','Eighteen x squared divided by six x is three x; negative twelve x over six x is negative two.','x cannot be zero in the original denominator.'),('Distribute negative two','Negative two times x is negative two x; negative two times negative three is plus six.','Both bracket terms receive the factor.'),('Sort terms and constants','Three x, negative two x and positive x form one bin; negative two and positive six form another.','Do not merge the two term types.'),('Calculate both bins','The variable bin gives two x and the constant bin gives four.','Keep the restriction from the original expression.')],
    'At x=2: (72-24)/12-2(-1)+2=4+2+2=8; 2(2)+4=8; x=0 excluded.','Cancelling at zero or losing the positive six.','Mark the domain first, then make quotient and bracket paths independently.',4),
]

P=[
 ('p01','Simplify 6n+2n.','8n','Put both n terms together.','(6+2)n=8n.'),
 ('p02','Simplify 5a+3-2a.','3a+3','Separate a terms from constants.','(5-2)a+3=3a+3.'),
 ('p03','Simplify 3(x+2)+x.','4x+6','Distribute three to both terms.','3x+6+x=4x+6.'),
 ('p04','Simplify 4(y-3)-y.','3y-12','Keep the negative twelve.','4y-12-y=3y-12.'),
 ('p05','Simplify -2(t-5)+3t.','t+10','Negative two times negative five is positive ten.','-2t+10+3t=t+10.'),
 ('p06','Simplify (15x+10)÷5+2x.','5x+2','Divide both numerator terms.','3x+2+2x=5x+2.'),
 ('p07','Simplify 3(2a-1)+2(a+4).','8a+5','Expand each bracket separately.','6a-3+2a+8=8a+5.'),
 ('p08','Simplify 5x-(3x-4).','2x+4','Subtract both bracket terms.','5x-3x+4=2x+4.'),
 ('p09','Simplify (12p²+6p)÷3p+p, p≠0.','5p+2, p≠0','Divide termwise and keep the restriction.','4p+2+p=5p+2, p≠0.'),
 ('p10','Simplify 4x²+x-2x²+3x.','2x²+4x','Separate squared and linear terms.','(4-2)x²+(1+3)x=2x²+4x.'),
 ('p11','Correct 3(x+2)+x=3x+2+x. Give the first error and correct simplified form.','The 2 was not multiplied by 3; 4x+6','Find the missed arrow.','3(x+2)+x=3x+6+x=4x+6.'),
 ('p12','A rectangle has length (x+3) cm and width (x+1) cm. Simplify P=2(l+w) and find P at x=2.','P=4x+8 cm; at x=2, 16 cm','Count each side twice.','P=2[(x+3)+(x+1)]=2(2x+4)=4x+8 cm; at x=2, P=16 cm.'),
 ('p13','Show 2(x-3)+3(x+2) simplifies to 5x. Check at x=1.','5x; both forms give 5 at x=1','Expand generally before testing a value.','2x-6+3x+6=5x; at x=1, 2(-2)+3(3)=5.'),
 ('p14','Simplify 3(2x-1)-(x+4)+(9x+6)÷3.','8x-5','Finish three separate operation lanes.','6x-3-x-4+3x+2=8x-5.'),
 ('p15','Simplify (12x²-6x)÷3x-3(x-2)+x for x≠0.','2x+4, x≠0','Keep x nonzero and divide both terms.','4x-2-3x+6+x=2x+4, x≠0.'),
]
M=[
 ('m01',2,'Simplify 7a+2-a.','6a+2','7a-a+2=6a+2.'),
 ('m02',3,'Simplify 3(x-4)+2x.','5x-12','3x-12+2x=5x-12.'),
 ('m03',4,'Simplify 2(2y-3)-(y-5).','3y-1','4y-6-y+5=3y-1.'),
 ('m04',5,'Simplify (15p²+10p)÷5p+2p, p≠0.','5p+2, p≠0','3p+2+2p=5p+2; p=0 is excluded.'),
 ('m05',6,'A rectangle has length (2x+1) cm and width (x+2) cm. Simplify its perimeter and find it at x=2.','P=6x+6 cm; at x=2, P=18 cm','P=2[(2x+1)+(x+2)]=2(3x+3)=6x+6 cm; x=2 gives length 5 cm, width 4 cm, perimeter 18 cm.'),
]
R=[
 ('r01','Simplify 2(x+5)+3x.','5x+10','2x+10+3x=5x+10.'),
 ('r02','Simplify 6x-(4x-3).','2x+3','6x-4x+3=2x+3.'),
 ('r03','Simplify (8t²-4t)÷4t-2(t-1)+t, t≠0.','t+1, t≠0','2t-1-2t+2+t=t+1, t≠0.'),
]

def build():
    doc=Document();sec=doc.sections[0];sec.top_margin=sec.bottom_margin=Inches(.7);sec.left_margin=sec.right_margin=Inches(.75)
    style=doc.styles['Normal'];style.font.name='Arial';style.font.size=Pt(10);style.paragraph_format.space_after=Pt(5)
    doc.add_heading('Grade 8 Algebraic Expressions | Lesson 8',0)
    doc.add_paragraph('Choosing and combining simplification methods. Original Athena teaching source v1; teacher review required.')
    doc.add_paragraph('Fifteen worked examples, fifteen independent questions, five mastery questions (20 marks), and three parallel reassessments are authored here. The runtime loads these records; it does not generate questions with AI.')
    doc.add_heading('Curriculum and lesson method',1)
    for title,url in SOURCES: doc.add_paragraph(f'{title}: {url}')
    doc.add_paragraph('Prerequisites: lessons 1–7 on algebraic language, like terms, products, distribution, division, powers, and numerical substitution. The Grade 8 ATP includes simplifying expressions involving these operations and determining values by substitution. All examples below are original, modelled on the curriculum scope rather than copied from source questions.')
    doc.add_paragraph('Decision routine: read the entire expression; mark domains before cancelling variable divisors; expand whole brackets, divide every term under a common numerator, then sort by variable and power. Perform one legal operation per board step. Keep the original prompt, completed states and operation path in view. Reveal calculated outputs only as they are taught. Finish with a substitution or context check; the check does not replace an algebraic proof.')
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
    doc.add_paragraph('Teacher must review every signed expansion, domain restriction, input-output reveal, target, narration, independent-attempt gate, desktop and mobile presentation. Equivalent algebraic short-text answers need robust scoring before release approval.')
    OUT.parent.mkdir(parents=True,exist_ok=True);doc.save(OUT)
    payload={'id':'g8-algebraic-expressions-08','title':'Mixed algebraic simplification and verification','source_document':OUT.name,'source_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'worked_examples':E,'practice_questions':P,'mastery_questions':M,'reassessment_questions':R}
    JSON.parent.mkdir(parents=True,exist_ok=True);JSON.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(OUT,JSON,payload['source_sha256'],sep='\n')

if __name__=='__main__':build()
