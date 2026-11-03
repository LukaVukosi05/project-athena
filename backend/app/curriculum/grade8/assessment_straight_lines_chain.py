"""Independent practice and changed-value assessments for straight-line chains."""
from app.curriculum.grade8.straight_lines_chain_cases import LESSONS, make_case
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep


def expected(case):
    value=f'{case.answer}°' if case.lesson!=4 else str(case.answer)
    return f'{case.scene["relation"]}; {value}' if case.lesson==5 else value


def banks(number):
    lesson_id=f'g8-straight-lines-{number:02}'
    practice=[]
    for index,worked in enumerate(LESSONS[number],1):
        case=make_case(number,index,1)
        suffix=' State the correct first relationship and x as “relationship; value°”.' if number==5 else ''
        practice.append(PracticeQuestion(id=f'g8-lines-l{number:02}-p{index:02}',lesson_id=lesson_id,
            question_number=index,difficulty='foundation' if index==1 else 'standard',
            cognitive_level='routine' if index<10 else 'complex',marks=2 if index<5 else 5,type='short_text',
            prompt=case.problem+suffix,accepted_answers=[expected(case)],answer_normalisation=AnswerNormalisation(),
            hints=['Highlight the parallel-line marks and both intersections before writing an angle equation.',
                   f'The first marked pair is {case.scene["relation"]}; keep the intermediate sector separate.'],
            worked_solution=[WorkedSolutionStep(expression=row,explanation='Use a marked angle relationship.',why='The given diagram, not its apparent size, determines this step.') for row in case.working]+
                [WorkedSolutionStep(expression=expected(case),explanation=case.check,why='Check both marked angle relationships.',verification=case.check)],
            misconception_tags=['angle-reasoning',case.family],verification={'original_question_check':case.check},
            correct_feedback='Both angle relationships are now verified.',source=f'geometry-of-straight-lines/lesson-{number:02}.md',answer_hidden_before_submission=True))
    def assessment(index,variant,prefix,position):
        case=make_case(number,index,variant)
        suffix=' Answer as “relationship; value°”.' if number==5 else ''
        return AssessmentQuestion(id=f'g8-lines-l{number:02}-{prefix}{position:02}',number=position,
            prompt=case.problem+suffix,marks=4 if prefix=='m' else None,answer=expected(case),
            solution=[*case.working,case.check],verification=case.check,
            misconception_tags=['angle-reasoning',case.family],accepted_answers=[expected(case)])
    mastery=[assessment(index,2,'m',j) for j,index in enumerate((3,6,9,12,15),1)]
    reassess=[assessment(index,3,'r',j) for j,index in enumerate((5,10,15),1)]
    tag='angle-reasoning'
    return (practice,mastery,reassess,
        {tag:{'diagnosis':'The first claimed relationship does not follow from the marked sectors.',
              'repair':'Trace the two intersections, mark the named angle pair, then solve a fresh diagram.'}},
        {tag:'After identifying the first invalid relationship, reassess on changed angles and a changed diagram.'})

PRACTICE_3,MASTERY_3,REASSESS_3,REPAIRS_3,RULES_3=banks(3)
PRACTICE_4,MASTERY_4,REASSESS_4,REPAIRS_4,RULES_4=banks(4)
PRACTICE_5,MASTERY_5,REASSESS_5,REPAIRS_5,RULES_5=banks(5)
