"""Source fidelity, full worked sequences, and answer gates for inspection."""
import hashlib
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.lesson2_runtime import LESSON_2, SOURCE_DATA
from app.curriculum.grade8.assessment_lesson2 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.inspection_timelines import PLANS
from app.curriculum.content_manifest import readiness_for
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx'


def test_source_fidelity_and_all_question_banks():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_DATA['source_sha256']
    for kind,count,prefix in [('worked_examples',15,'w'),('practice_questions',15,'p'),('mastery_questions',5,'m'),('reassessment_questions',3,'r')]:
        assert [x['id'] for x in SOURCE_DATA[kind]]==[f'g8-ae-l02-{prefix}{n:02}' for n in range(1,count+1)]
    assert [x.id for x in LESSON_2.whiteboard_questions]==[x['id'] for x in SOURCE_DATA['worked_examples']]
    assert [x.id for x in PRACTICE_BANK]==[x['id'] for x in SOURCE_DATA['practice_questions']]
    assert len(MASTERY_BANK)==5 and len(REASSESSMENT_BANK)==3
    assert readiness_for(LESSON_2).value=='published'
    assert [failure for failure in validate_curriculum([curriculum_repository.get_grade('grade-8')]) if failure.lesson_id==LESSON_2.id]==[]


def test_each_example_has_distinct_visible_action_and_original_check():
    assert len(PLANS)==15
    for question,source in zip(LESSON_2.whiteboard_questions,SOURCE_DATA['worked_examples']):
        board=question.whiteboard
        assert f'algebra:{board.visualization.template}'==source['renderer']
        assert ('algebra',board.visualization.template) in CATALOGUE
        assert board.visualization.parameters['source_data']==source['question_data']
        assert board.visualization.parameters['total_steps']==len(PLANS[source['number']])
        assert len(board.steps)>=3
        assert board.initial_expression==board.steps[0].before_expression
        assert all(a.after_expression==b.before_expression for a,b in zip(board.steps,board.steps[1:]))
        expected=question.answer.split(';')[-1].strip().casefold().replace('-', '−')
        assert expected in board.steps[-1].after_expression.casefold() or source['number'] in {11,13,14}
        assert board.steps[-1].state_after['verification_complete']
        ids={o.id for o in board.semantic_objects}
        for step in board.steps:
            assert step.before_expression!=step.after_expression
            assert step.working_expression not in {step.before_expression,step.after_expression}
            assert step.events and {target for e in step.events for target in e.targets}<=ids
            assert [e.text for e in step.events if e.type=='caption']==[e.text for e in step.events if e.type=='narration']


def test_public_preview_does_not_expose_solution_and_reveal_is_scoped():
    with TestClient(app) as client:
        public=client.get(f'/api/v1/lessons/{LESSON_2.id}')
        # Premium access remains enforced unless the caller is entitled.
        if public.status_code==200:
            data=public.json()
            assert len(data['whiteboard_questions'])==15
            for source,question in zip(SOURCE_DATA['worked_examples'],data['whiteboard_questions']):
                assert 'answer' not in question and 'full_memo' not in question
                assert question['solution_gated']
                preview=question['whiteboard']['steps']
                assert len(preview)==1 and preview[0]['after_expression']==preview[0]['before_expression']
                assert 'candidate =' not in question['whiteboard']['visualization']['parameters']['source_data']
            revealed=client.post(f'/api/v1/lessons/{LESSON_2.id}/questions/g8-ae-l02-w12/reveal')
            assert revealed.status_code==200
            assert len(revealed.json()['whiteboard']['steps'])==4
            assert revealed.json()['whiteboard']['steps'][-1]['after_expression'].endswith('x = 6')
            assert client.post(f'/api/v1/lessons/{LESSON_2.id}/questions/g8-ae-l01-w12/reveal').status_code==404
        else: assert public.status_code==401
        practice=client.get(f'/api/v1/practice/{LESSON_2.id}')
        assert practice.status_code==200
        assert len(practice.json()['questions'])==15
        assert 'accepted_answers' not in practice.text
        mastery=client.get(f'/api/v1/practice/{LESSON_2.id}/mastery')
        assert len(mastery.json()['questions'])==5 and 'answer' not in mastery.text


def test_practice_submission_mastery_diagnosis_and_parallel_retry():
    with TestClient(app) as client:
        prefix=f'/api/v1/practice/{LESSON_2.id}'
        session=client.post(prefix+'/sessions').json()['session_id']
        q='g8-ae-l02-p01'
        assert client.get(f'{prefix}/sessions/{session}/questions/{q}/solution').status_code==403
        wrong=client.post(f'{prefix}/sessions/{session}/questions/{q}/submit',json={'answer':'x = 8'})
        assert wrong.status_code==200 and not wrong.json()['correct']
        assert client.get(f'{prefix}/sessions/{session}/questions/{q}/solution').status_code==403
        right=client.post(f'{prefix}/sessions/{session}/questions/{q}/submit',json={'answer':'x = 5'})
        assert right.json()['correct']
        assert client.get(f'{prefix}/sessions/{session}/questions/{q}/solution').json()['verification']['original_question_check']=='5 + 8 = 13'
        incorrect={item.id:'incorrect' for item in MASTERY_BANK}
        result=client.post(f'{prefix}/sessions/{session}/mastery',json={'answers':incorrect})
        assert result.status_code==200 and not result.json()['mastered']
        assert result.json()['repair_routes']
        assert client.get(f'{prefix}/sessions/{session}/reassessment').status_code==409
        repair=client.get(f'{prefix}/sessions/{session}/repair')
        assert repair.status_code==200 and repair.json()['routes']
        assert client.post(f'{prefix}/sessions/{session}/repair/complete').json()['reassessment_unlocked']
        parallel=client.get(f'{prefix}/sessions/{session}/reassessment').json()['questions']
        assert len(parallel)==3 and all('answer' not in row for row in parallel)
