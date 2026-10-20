"""Lesson 8 release and mathematical gates."""
import hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.content_manifest import readiness_for
from app.curriculum.grade8.lesson8_runtime import LESSON_8,SOURCE_DATA
from app.curriculum.grade8.assessment_lesson8 import PRACTICE_BANK,MASTERY_BANK,REASSESSMENT_BANK,MISCONCEPTION_REPAIRS
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
SOURCE=Path(__file__).resolve().parents[2]/"docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"

def test_source_banks_and_release():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_DATA['source_sha256']
    for bank,prefix,count in ((LESSON_8.whiteboard_questions,'w',15),(PRACTICE_BANK,'p',15),(MASTERY_BANK,'m',5),(REASSESSMENT_BANK,'r',3)):
        assert [q.id for q in bank]==[f'g8-ae-l08-{prefix}{n:02}' for n in range(1,count+1)]
    assert readiness_for(LESSON_8).value=='published'
    assert not [f for f in validate_curriculum([curriculum_repository.get_grade('grade-8')]) if f.lesson_id==LESSON_8.id]
    assert {tag for q in MASTERY_BANK for tag in q.misconception_tags}<=set(MISCONCEPTION_REPAIRS)

def test_complete_worked_steps_and_verifications():
    assert {q.whiteboard.visualization.template for q in LESSON_8.whiteboard_questions}=={'fraction_bar_balance_native','fraction_equivalence_native','fraction_lcd_native','fraction_error_native','fraction_context_native'}
    for q in LESSON_8.whiteboard_questions:
        board=q.whiteboard
        assert len(board.steps)>=4 and board.initial_expression==board.problem
        assert board.steps[-1].after_expression.startswith('Checked:') and board.steps[-1].state_after['verification_complete']
        assert q.answer and q.full_memo and q.expected_evidence
        for i,step in enumerate(board.steps):
            assert step.before_expression!=step.after_expression,(q.id,i)
            assert [e.text for e in step.events if e.type=='caption']==[e.text for e in step.events if e.type=='narration']
            assert min(e.at_ms for e in step.events if e.type=='show_operation')<min(e.at_ms for e in step.events if e.type=='reveal')
            if i: assert step.before_expression==board.steps[i-1].after_expression
    assert '17/2' in LESSON_8.whiteboard_questions[9].whiteboard.steps[-1].after_expression
    assert '42 litres' in LESSON_8.whiteboard_questions[14].whiteboard.steps[-1].after_expression

def test_api_preview_and_practice_gate():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/algebraic-equations').json()
        row=next(row for group in topic['subtopics'] for row in group['lessons'] if row['id']==LESSON_8.id)
        assert row['readiness']=='published' and row['usable']
        response=client.get(f'/api/v1/lessons/{LESSON_8.id}')
        if response.status_code==200:
            for q in response.json()['whiteboard_questions']:
                assert 'answer' not in q and 'full_memo' not in q
                board=q['whiteboard']
                assert len(board['steps'])==1 and not board['steps'][0]['events']
                assert board['steps'][0]['after_expression']==board['steps'][0]['before_expression']
                source=board['visualization']['parameters']['source_data']
                assert not any(label in source for label in ('solution =','cleared_equation =','scaled_terms =','correct_cleared =','lcd =')),q['id']
            for n in range(1,16):
                revealed=client.post(f'/api/v1/lessons/{LESSON_8.id}/questions/g8-ae-l08-w{n:02}/reveal')
                assert revealed.status_code==200,n
                assert revealed.json()['whiteboard']['steps'][-1]['state_after']['verification_complete']
        else:assert response.status_code==401
        prefix=f'/api/v1/practice/{LESSON_8.id}'
        practice=client.get(prefix).json()
        assert len(practice['questions'])==15 and 'accepted_answers' not in str(practice)
        session=client.post(prefix+'/sessions').json()['session_id']
        failed=client.post(prefix+f'/sessions/{session}/mastery',json={'answers':{q.id:'incorrect' for q in MASTERY_BANK}})
        assert failed.status_code==200 and not failed.json()['mastered'] and failed.json()['repair_routes']
        assert client.get(prefix+f'/sessions/{session}/reassessment').status_code==409
        assert client.post(prefix+f'/sessions/{session}/repair/complete').json()['reassessment_unlocked']
        assert len(client.get(prefix+f'/sessions/{session}/reassessment').json()['questions'])==3

def test_source_equations_substitute_correctly():
    from fractions import Fraction as F
    assert F(35,5)==7 and F(20,4)+3==8
    assert F(16+2,3)==6 and F(2*15,3)==10
    assert F(12,2)+F(12,3)==10 and F(24,4)-F(24,6)==2
    assert F(3*7-1,5)==4 and F(3*(14-2),4)==9
    assert F(30,3)+2==F(30,6)+7
    assert F(F(17,2),2)+F(3,4)==5
    assert F(3*28,4)+5==26 and F(72,3)+12==F(72,2)
    assert F(2*10+1,3)-F(10-2,4)==5
    assert F(0-1,2)+F(0+3,5)==F(3*0+1,10)
    assert F(2*60,5)+18==F(7*60,10)==42
