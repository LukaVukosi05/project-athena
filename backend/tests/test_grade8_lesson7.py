"""Lesson 7 release and mathematical gates."""
import hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.content_manifest import readiness_for
from app.curriculum.grade8.lesson7_runtime import LESSON_7,SOURCE_DATA
from app.curriculum.grade8.assessment_lesson7 import PRACTICE_BANK,MASTERY_BANK,REASSESSMENT_BANK,MISCONCEPTION_REPAIRS
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
SOURCE=Path(__file__).resolve().parents[2]/"docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"

def test_source_banks_and_release():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_DATA['source_sha256']
    for bank,prefix,count in ((LESSON_7.whiteboard_questions,'w',15),(PRACTICE_BANK,'p',15),(MASTERY_BANK,'m',5),(REASSESSMENT_BANK,'r',3)):
        assert [q.id for q in bank]==[f'g8-ae-l07-{prefix}{n:02}' for n in range(1,count+1)]
    assert readiness_for(LESSON_7).value=='published'
    assert not [f for f in validate_curriculum([curriculum_repository.get_grade('grade-8')]) if f.lesson_id==LESSON_7.id]
    assert {tag for q in MASTERY_BANK for tag in q.misconception_tags}<=set(MISCONCEPTION_REPAIRS)

def test_complete_worked_steps_and_verifications():
    assert {q.whiteboard.visualization.template for q in LESSON_7.whiteboard_questions}=={'bracket_balance_native','bracket_distribution_native','bracket_paths_native','bracket_area_native','bracket_rectangle_native'}
    for q in LESSON_7.whiteboard_questions:
        board=q.whiteboard
        assert len(board.steps)>=5 and board.initial_expression==board.problem
        assert board.steps[-1].after_expression.startswith('Checked:') and board.steps[-1].state_after['verification_complete']
        assert q.answer and q.full_memo and q.expected_evidence
        for i,step in enumerate(board.steps):
            assert step.before_expression!=step.after_expression,(q.id,i)
            assert [e.text for e in step.events if e.type=='caption']==[e.text for e in step.events if e.type=='narration']
            assert min(e.at_ms for e in step.events if e.type=='show_operation')<min(e.at_ms for e in step.events if e.type=='reveal')
            if i: assert step.before_expression==board.steps[i-1].after_expression
    assert 'R180' in LESSON_7.whiteboard_questions[11].whiteboard.steps[-1].after_expression
    assert 'a ≠ 0' in LESSON_7.whiteboard_questions[14].whiteboard.steps[-1].after_expression

def test_api_preview_and_practice_gate():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/algebraic-equations').json()
        row=next(row for group in topic['subtopics'] for row in group['lessons'] if row['id']==LESSON_7.id)
        assert row['readiness']=='published' and row['usable']
        response=client.get(f'/api/v1/lessons/{LESSON_7.id}')
        if response.status_code==200:
            for q in response.json()['whiteboard_questions']:
                assert 'answer' not in q and 'full_memo' not in q
                board=q['whiteboard']
                assert len(board['steps'])==1 and not board['steps'][0]['events']
                assert board['steps'][0]['after_expression']==board['steps'][0]['before_expression']
                source=board['visualization']['parameters']['source_data']
                assert not any(label in source for label in ('solution =','expanded =','divide first state =','partial products =','restriction =')),q['id']
            for n in range(1,16):
                revealed=client.post(f'/api/v1/lessons/{LESSON_7.id}/questions/g8-ae-l07-w{n:02}/reveal')
                assert revealed.status_code==200,n
                assert revealed.json()['whiteboard']['steps'][-1]['state_after']['verification_complete']
        else:assert response.status_code==401
        prefix=f'/api/v1/practice/{LESSON_7.id}'
        practice=client.get(prefix).json()
        assert len(practice['questions'])==15 and 'accepted_answers' not in str(practice)
        session=client.post(prefix+'/sessions').json()['session_id']
        failed=client.post(prefix+f'/sessions/{session}/mastery',json={'answers':{q.id:'incorrect' for q in MASTERY_BANK}})
        assert failed.status_code==200 and not failed.json()['mastered'] and failed.json()['repair_routes']
        assert client.get(prefix+f'/sessions/{session}/reassessment').status_code==409
        assert client.post(prefix+f'/sessions/{session}/repair/complete').json()['reassessment_unlocked']
        assert len(client.get(prefix+f'/sessions/{session}/reassessment').json()['questions'])==3

def test_source_equations_substitute_correctly():
    assert 2*(4+3)==14 and -2*(-7+4)==6
    assert 5-2*(-1-3)==13 and 3*(5+2)==2*5+11
    assert 2*(3*6-4)==4*(6+1)
    assert 4*(30+15)==3*(30+30)==180
    assert 3*(8+4)-6==30
    assert -2*(3*(-1)-5)==4*(-1+5)==16
    assert -2.5*(-1.8-1.2)==7.5
