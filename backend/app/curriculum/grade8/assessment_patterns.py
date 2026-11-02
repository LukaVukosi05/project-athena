"""Private practice and reassessment for the two Patterns lessons."""
from app.curriculum.grade8.patterns_runtime import build
from app.curriculum.grade8.assessment_expressions import AssessmentQuestion
from app.practice.schemas import AnswerNormalisation, PracticeQuestion, WorkedSolutionStep

def banks(number):
    lesson,questions,scenes,source=build(number)
    # Practice changes each source pattern's starting value. It does not display worked answers until submission.
    practice=[]
    for index,scene in enumerate(scenes,1):
        terms=scene['terms']; offset=2 if number==1 else 0
        # A different position prevents geometric practice from repeating the worked answer.
        n=6
        next_figure={"joined_squares":3*n+1,"separate_squares":4*n,"square_dots":n*n,
            "staircase":n*(n+1)//2,"border":4*n,"l_shape":2*n+1,"triangle_edges":3*n,
            "two_rows":2*n,"rectangle":n*(n+1),"square_plus":n*n+4,"fence":4*(n+1),
            "three_arms":3*n+1,"columns":4*n+2,"square_plus_two":n*n+2,"rectangle_two":n*(n+2)}
        prompt=(f'The sequence {", ".join(map(str,[v+offset for v in terms]))} continues with the same changes as {scene["title"]}. Find the next term.'
                if number==1 else f'{scene["title"]}: the first four figures contain {", ".join(map(str,terms))} pieces. How many pieces are in Figure 6? Explain the missing Figure 5 step.')
        answer=str(scene['answer']+offset if number==1 else next_figure[scene['kind']])
        memo=(f'{scene["memo"]} Shift every given term and the next term by {offset}.' if number==1 else
              f'Use the same figure construction at position 5 and then position 6. Figure 6 has {answer} pieces; check the earlier four counts.')
        practice.append(PracticeQuestion(id=f'g8-patterns-l{number:02}-p{index:02}',lesson_id=lesson.id,question_number=index,
            difficulty=questions[index-1].difficulty,cognitive_level=questions[index-1].cognitive_level,marks=questions[index-1].marks,
            type='short_text',prompt=prompt,accepted_answers=[answer],answer_normalisation=AnswerNormalisation(),
            hints=['Write the positions and changes before extending the pattern.','Check that the same construction explains all four givens.'],
            worked_solution=[WorkedSolutionStep(expression='Inspect the given terms',explanation='Check the proposed rule at every position.',why='One matching interval is insufficient.'),
                WorkedSolutionStep(expression=answer,explanation=memo,why=memo,verification=memo)],
            misconception_tags=['pattern-rule-from-too-few-terms'],verification={'original_question_check':memo},
            correct_feedback='Correct. Your rule also fits the given terms.',source=source.name,answer_hidden_before_submission=True))
    def assess(index,mastery):
        s=scenes[index]; answer=str(s['answer']); prefix='m' if mastery else 'r'; n=index+1 if mastery else index-4
        return AssessmentQuestion(id=f'g8-patterns-l{number:02}-{prefix}{n:02}',number=n,
            prompt=f'{s["title"]}: {", ".join(map(str,s["terms"]))}. What is the next value?',marks=4 if mastery else None,
            answer=answer,solution=[s['memo'],answer],verification=s['memo'],accepted_answers=[answer],
            misconception_tags=['pattern-rule-from-too-few-terms'])
    mastery=[assess(i,True) for i in range(5)]
    parallel=[assess(i,False) for i in range(5,8)]
    repairs={'pattern-rule-from-too-few-terms':{'diagnosis':'The proposed rule did not explain every given position.',
        'repair':'Write the positions and first differences, inspect the figure groups, test all given values, then extend once.'}}
    return practice,mastery,parallel,repairs

PRACTICE_1,MASTERY_1,REASSESSMENT_1,REPAIRS_1=banks(1)
PRACTICE_2,MASTERY_2,REASSESSMENT_2,REPAIRS_2=banks(2)
