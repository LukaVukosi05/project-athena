"""Private independently authored variants for signed products, powers and roots."""
from app.curriculum.grade8.integers_advanced_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep
from app.curriculum.grade8.integer_evaluator import evaluate

PRACTICE={
3:['3*(-4)','(-6)*2','(-3)*(-5)','24//(-4)','(-30)//5','(-42)//(-6)','0*(-25)','(-9)*6','(-81)//9','(-11)*(-4)','(-169)//(-13)','(-7)*(-3)*(-2)','((-80)//8)*(-2)','(-120)//(-5)//4','(-2)*(-3)*(-4)*(-5)'],
4:['(-6)**2','-6**2','(-3)**3','sqrt(121)','cbrt(-64)','(-4)**2+sqrt(25)','cbrt(-125)*(-3)','(-2)**3+19','sqrt(81)-(-3)**3','(-8)**2//(-4)','cbrt(-216)+sqrt(49)','(-3)**4-cbrt(-27)','(-2)**2*(cbrt(-8)+7)','(sqrt(100)-cbrt(-27))*(-3)','(-3)**3//cbrt(-27)+sqrt(169)']}
MASTERY={3:['(-7)*8','(-54)//(-6)','(-8)*(-2)*(-3)','(-84)//7*(-2)','(-144)//(-6)//4'],
4:['(-7)**2','cbrt(-343)','sqrt(169)-(-3)**2','(-2)**3*(sqrt(64)-5)','(-5)**3//cbrt(-125)+sqrt(100)']}
REASSESS={3:['(-9)*(-8)','(-132)//(-11)','(-4)*(-3)*(-2)*(-1)'],
4:['(-6)**3','cbrt(-216)+sqrt(81)','(-4)**2//cbrt(-8)+sqrt(25)']}

def notation(expression):
    return expression.replace('**','^').replace('//',' ÷ ').replace('*',' × ')

def banks(number):
    lesson,questions,scenes,source=build(number)
    tag='integer-product-sign' if number==3 else 'integer-operation-order'
    practice=[]
    for i,(source_expr,question) in enumerate(zip(PRACTICE[number],questions,strict=True),1):
        result=evaluate(source_expr)
        prompt=f'Evaluate {notation(source_expr)}. Show the sign and each calculation stage.'
        memo=f'Apply the signed-number rules and operation order to {notation(source_expr)}. The result is {result}. Check by substituting into the original expression.'
        practice.append(PracticeQuestion(id=f'g8-int-l{number:02}-p{i:02}',lesson_id=lesson.id,
            question_number=i,difficulty=question.difficulty,cognitive_level=question.cognitive_level,marks=question.marks,
            type='short_text',prompt=prompt,accepted_answers=[str(result)],answer_normalisation=AnswerNormalisation(),
            hints=['Identify the sign and the exact scope of each operation.','Evaluate one group, power or root; keep that intermediate value visible.'],
            worked_solution=[WorkedSolutionStep(expression=notation(source_expr),explanation='Read the complete original expression.',why='Avoid changing signs or bracket scope.'),
                WorkedSolutionStep(expression=str(result),explanation=memo,why='Verify against the original.',verification=memo)],
            misconception_tags=[tag],verification={'original_question_check':memo},
            correct_feedback='Correct; each operation agrees with the original expression.',source=source.name,
            answer_hidden_before_submission=True))
    def item(expr,i,prefix):
        answer=str(evaluate(expr));memo=f'Calculate {notation(expr)} in order; confirm the final signed value is {answer}.'
        return AssessmentQuestion(id=f'g8-int-l{number:02}-{prefix}{i:02}',number=i,prompt=f'Evaluate {notation(expr)}.',
            marks=4 if prefix=='m' else None,answer=answer,solution=[memo,answer],verification=memo,
            misconception_tags=[tag],accepted_answers=[answer])
    mastery=[item(expr,i,'m') for i,expr in enumerate(MASTERY[number],1)]
    reassess=[item(expr,i,'r') for i,expr in enumerate(REASSESS[number],1)]
    repairs={tag:{'diagnosis':'The first product sign, exponent scope or calculation order did not match the original.',
        'repair':'Replay the first incorrect mathematical action, keep each earlier result, then attempt a parallel expression.'}}
    rules={tag:'Try new signed values and explain the first incorrect operation before checking the memo.'}
    return practice,mastery,reassess,repairs,rules

PRACTICE_3,MASTERY_3,REASSESSMENT_3,REPAIRS_3,RULES_3=banks(3)
PRACTICE_4,MASTERY_4,REASSESSMENT_4,REPAIRS_4,RULES_4=banks(4)
