"""Private parallel banks for integer properties and contextual operations."""
from app.curriculum.grade8.integers_advanced_runtime import build
from app.curriculum.grade8.integer_evaluator import evaluate
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep

# Each entry is an independently authored question and verified exact expression.
PROPERTY_PRACTICE=[
('6+(-11)','(-11)+6'),('(-5)*8','8*(-5)'),('11-(-4)','(-4)-11'),
('((-7)+3)+(-2)','(-7)+(3+(-2))'),('((-3)*4)*(-5)','(-3)*(4*(-5))'),
('((-9)-4)-3','(-9)-(4-3)'),('(-2)*(5+(-7))','(-2)*5+(-2)*(-7)'),
('6*(4-9)','6*4-6*9'),('(-5)*(2+(-3))','(-5)*2+(-3)'),
('(-13)+13','0'),('(-14)+0','(-14)'),('(-9)*1','(-9)'),
('(-11)*0','0'),('(-7)*(4+(-9))','(-7)*4+(-7)*(-9)'),
('(-18)+(10+(-10))','((-18)+10)+(-10)')]
PROPERTY_MASTERY=[('(-8)+12','12+(-8)'),('(-2)*(7+(-10))','(-2)*7+(-2)*(-10)'),
                  ('(-9)-2','2-(-9)'),('((-4)*(-6))*2','(-4)*((-6)*2)'),('(-15)+15','0')]
PROPERTY_REASSESS=[('(-12)*3','3*(-12)'),('(-6)*(4+(-8))','(-6)*4+(-6)*(-8)'),('(-7)-(-2)','(-2)-(-7)')]
CONTEXT_PRACTICE=[
('It is −6 °C. It rises by 8 °C and falls by 5 °C. What is the temperature?','-6+8-5'),
('An account has R25. R31 leaves, then R10 arrives. What is the balance?','25-31+10'),
('A hiker starts 9 m below sea level, climbs 15 m, then descends 7 m. Where are they?','-9+15-7'),
('A game has four rounds of −3 points, then a +19 point bonus. Find the total.','4*(-3)+19'),
('It is 8 °C, falls by 13 °C, then warms by 4 °C. Find the reading.','8-13+4'),
('R50 pays for three R19 tickets and receives a R12 refund. What is the balance?','50-3*19+12'),
('A lift starts on floor −2, rises 9, falls 8, then rises 5. Which floor?','-2+9-8+5'),
('A quiz gives +7 for each correct answer and −4 for each wrong. Five correct, six wrong: total?','5*7+6*(-4)'),
('A freezer is −15 °C and warms 6 °C per hour for three hours. Reading?','-15+3*6'),
('An account owes R80; six payments of R16 arrive. What is its balance?','-80+6*16'),
('A diver is 7 m below sea level, descends 4 m twice, then rises 9 m. Where?','-7+2*(-4)+9'),
('Six penalties lose 3 points each; five goals earn 4 each. Net points?','6*(-3)+5*4'),
('A R108 bill is shared by six; you start with R12. Balance after paying?','12-108//6'),
('Temperature −5 °C rises 7 °C twice then falls by 11 °C. Final?','-5+2*7-11'),
('A drone at 10 m descends 4 m four times, rises 13 m, then descends 3 m. Final?','10+4*(-4)+13-3')]
CONTEXT_MASTERY=[('A lift starts at −4, rises 12 floors, then descends 5. Which floor?','-4+12-5'),
 ('A quiz gives 9 points per win and loses 4 per penalty. Three wins, five penalties?','3*9+5*(-4)'),
 ('A wallet starts R20 in debt, receives four R11 payments, then spends R18. Balance?','-20+4*11-18'),
 ('A diver begins 8 m below sea level, climbs 5 m, then descends 6 m twice. Elevation?','-8+5+2*(-6)'),
 ('At −7 °C the temperature rises 5 °C three times, then falls 9 °C. Reading?','-7+3*5-9')]
CONTEXT_REASSESS=[('An account owes R45. Three payments of R20 arrive, then R7 leaves. Balance?','-45+3*20-7'),
 ('A lift at floor −5 rises 14, descends 8 and rises 3. Floor?','-5+14-8+3'),
 ('Four rounds lose 6 points each; three bonuses add 9 each. Net score?','4*(-6)+3*9')]

def property_answer(pair):return 'true' if evaluate(pair[0])==evaluate(pair[1]) else 'false'

def banks(number):
    if number not in (5,6):raise ValueError('Unsupported integer reasoning lesson')
    lesson,questions,scenes,source=build(number)
    tag='integer-property-claim' if number==5 else 'integer-context-translation'
    variants=PROPERTY_PRACTICE if number==5 else CONTEXT_PRACTICE
    practice=[]
    for i,(variant,question) in enumerate(zip(variants,questions,strict=True),1):
        if number==5:
            a,b=variant;answer=property_answer(variant);prompt=f'Is {a} = {b} true or false? Calculate both sides and explain.'
            memo=f'Left side = {evaluate(a)}, right side = {evaluate(b)}; therefore the claim is {answer}.'
        else:
            prompt,expression=variant;answer=str(evaluate(expression));memo=f'Translate as {expression}, follow the story in order, and check the signed result {answer}.'
        practice.append(PracticeQuestion(id=f'g8-int-l{number:02}-p{i:02}',lesson_id=lesson.id,
            question_number=i,difficulty=question.difficulty,cognitive_level=question.cognitive_level,marks=question.marks,
            type='short_text',prompt=prompt,accepted_answers=[answer],answer_normalisation=AnswerNormalisation(),
            hints=['Name each signed quantity and the operation it requires.',
                   'Calculate the first complete stage before deciding the sign or truth of the claim.'],
            worked_solution=[WorkedSolutionStep(expression='Original question',explanation=prompt,why='Preserve original order and signs.'),
                WorkedSolutionStep(expression=answer,explanation=memo,why='Check the original values.',verification=memo)],
            misconception_tags=[tag],verification={'original_question_check':memo},
            correct_feedback='Correct; the original signed quantities support this result.',source=source.name,
            answer_hidden_before_submission=True))
    def assess(variant,i,prefix):
        if number==5:
            a,b=variant;answer=property_answer(variant);prompt=f'Is {a} = {b} true or false? Justify with both values.'
            memo=f'{a} = {evaluate(a)} and {b} = {evaluate(b)}; the claim is {answer}.'
        else:
            prompt,expr=variant;answer=str(evaluate(expr));memo=f'{expr} = {answer}; check the original story and unit.'
        return AssessmentQuestion(id=f'g8-int-l{number:02}-{prefix}{i:02}',number=i,prompt=prompt,
            marks=4 if prefix=='m' else None,answer=answer,solution=[memo,answer],verification=memo,
            misconception_tags=[tag],accepted_answers=[answer])
    m=PROPERTY_MASTERY if number==5 else CONTEXT_MASTERY
    r=PROPERTY_REASSESS if number==5 else CONTEXT_REASSESS
    mastery=[assess(item,i,'m') for i,item in enumerate(m,1)]
    reassessment=[assess(item,i,'r') for i,item in enumerate(r,1)]
    repairs={tag:{'diagnosis':'The first claimed property or signed story change was not justified by the original values.',
                  'repair':'Return to that step; compute each side or balance in order, then try different values.'}}
    rules={tag:'Reassess on a changed, parallel question after explaining the first wrong stage.'}
    return practice,mastery,reassessment,repairs,rules

PRACTICE_5,MASTERY_5,REASSESSMENT_5,REPAIRS_5,RULES_5=banks(5)
PRACTICE_6,MASTERY_6,REASSESSMENT_6,REPAIRS_6,RULES_6=banks(6)
