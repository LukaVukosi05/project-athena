"""Private unseen practice, mastery and reassessment for straight-line geometry."""
from app.curriculum.grade8.straight_lines_cases import LESSON_1, LESSON_2, parallel_variant
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep


def _answer(case):
    return f'{case.answer}°' if len(case.given)==1 else str(case.answer)


def banks(number):
    cases = (LESSON_1, LESSON_2)[number-1]
    lesson_id=f'g8-straight-lines-{number:02}'
    practice=[]
    for i,worked in enumerate(cases,1):
        case=parallel_variant(worked,1)
        practice.append(PracticeQuestion(id=f'g8-lines-l{number:02}-p{i:02}',lesson_id=lesson_id,
            question_number=i,difficulty='foundation' if i==1 else 'standard',cognitive_level='routine' if i<10 else 'complex',
            marks=2 if i<5 else 4,type='short_text',prompt=case.problem,
            accepted_answers=[_answer(case)],answer_normalisation=AnswerNormalisation(),
            hints=['Mark both angle sectors and identify which lines create them.',
                   f'Decide whether {case.relationship.replace("_"," ")} gives equal angles or a fixed sum.'],
            worked_solution=[WorkedSolutionStep(expression=row,explanation='Apply the named relationship to the marked sectors.',why='Use the line markings; the diagram is not a measurement tool.') for row in case.working]+
                [WorkedSolutionStep(expression=_answer(case),explanation=case.check,why='Check the original labelled angles.',verification=case.check)],
            misconception_tags=['angle-reasoning',case.relationship],verification={'original_question_check':case.check},
            correct_feedback='Correct; the original angle relationship confirms your value.',source=f'geometry-of-straight-lines/lesson-{number:02}.md',answer_hidden_before_submission=True))
    def assessment(index,shift,prefix,number_in_bank):
        case=parallel_variant(cases[index-1],shift)
        return AssessmentQuestion(id=f'g8-lines-l{number:02}-{prefix}{number_in_bank:02}',number=number_in_bank,
            prompt=case.problem,marks=4 if prefix=='m' else None,answer=_answer(case),
            solution=[*case.working,case.check],verification=case.check,
            misconception_tags=['angle-reasoning',case.relationship],accepted_answers=[_answer(case)])
    mastery=[assessment(index,2,'m',j) for j,index in enumerate((3,6,9,12,15),1)]
    reassess=[assessment(index,3,'r',j) for j,index in enumerate((6,11,15),1)]
    tag='angle-reasoning'
    return (practice,mastery,reassess,
        {tag:{'diagnosis':'Locate the first claim unsupported by the actual line markings.',
              'repair':'Re-highlight the relevant angle pair, name the theorem, and solve a changed diagram.'}},
        {tag:'Reassess with parallel lines or intersection values after repairing the incorrect relationship.'})


PRACTICE_1,MASTERY_1,REASSESS_1,REPAIRS_1,RULES_1=banks(1)
PRACTICE_2,MASTERY_2,REASSESS_2,REPAIRS_2,RULES_2=banks(2)
