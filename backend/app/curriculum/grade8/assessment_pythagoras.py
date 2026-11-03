"""Unseen, server-only practice and assessments for five Pythagoras lessons."""
from app.curriculum.grade8.pythagoras_cases import LESSONS,variant
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation,PracticeQuestion,WorkedSolutionStep


def banks(number):
    cases=LESSONS[number];lesson_id=f'g8-pythagoras-{number:02}'
    practice=[]
    for i,worked in enumerate(cases,1):
        case=variant(worked,1)
        accepted=[case.answer]
        if case.answer.endswith((' cm',' m',' km')):accepted.append(case.answer.rsplit(' ',1)[0])
        practice.append(PracticeQuestion(id=f'g8-pythagoras-l{number:02}-p{i:02}',lesson_id=lesson_id,question_number=i,
            difficulty='foundation' if i==1 else 'standard',cognitive_level='routine' if i<10 else 'complex',marks=2 if i<5 else 4,
            type='short_text',prompt=case.problem,accepted_answers=accepted,answer_normalisation=AnswerNormalisation(),
            hints=['Highlight the exact sides or angles given in this figure.',f'Use the {case.family.replace("_"," ")} property; state it before substituting.'],
            worked_solution=[WorkedSolutionStep(expression=row,explanation='Follow the marked right angle and the named property.',why='Only the given labels and valid properties justify this step.') for row in case.working]+
              [WorkedSolutionStep(expression=case.answer,explanation=case.check,why='Return to the original given.',verification=case.check)],
            misconception_tags=['pythagoras-reasoning',case.family],verification={'original_question_check':case.check},
            correct_feedback='Correct; the original squared side relationship confirm the result.',source=f'pythagoras/lesson-{number:02}.md',answer_hidden_before_submission=True))
    def assessment(index,shift,prefix,j):
        case=variant(cases[index-1],shift)
        accepted=[case.answer]
        if case.answer.endswith((' cm',' m',' km')):accepted.append(case.answer.rsplit(' ',1)[0])
        return AssessmentQuestion(id=f'g8-pythagoras-l{number:02}-{prefix}{j:02}',number=j,prompt=case.problem,
            marks=4 if prefix=='m' else None,answer=case.answer,solution=[*case.working,case.check],verification=case.check,
            misconception_tags=['pythagoras-reasoning',case.family],accepted_answers=accepted)
    mastery=[assessment(index,2,'m',j) for j,index in enumerate((3,6,9,12,15),1)]
    reassess=[assessment(index,3,'r',j) for j,index in enumerate((6,11,15),1)]
    return (practice,mastery,reassess,
        {'pythagoras-reasoning':{'diagnosis':'Locate the first claim unsupported by the marked triangle.',
                            'repair':'Mark the given property, redo that step, then try a changed figure.'}},
        {'pythagoras-reasoning':'Retry a changed figure after explaining the relevant Pythagorean relation.'})

PRACTICE={n:banks(n)[0] for n in LESSONS}
