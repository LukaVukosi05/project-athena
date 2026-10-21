"""Lesson 9 release and mathematical gates."""
import hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.content_manifest import readiness_for
from app.curriculum.grade8.lesson9_runtime import LESSON_9,SOURCE_DATA
from app.curriculum.grade8.assessment_lesson9 import PRACTICE_BANK,MASTERY_BANK,REASSESSMENT_BANK,MISCONCEPTION_REPAIRS
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
SOURCE=Path(__file__).resolve().parents[2]/"docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx"

def test_source_banks_and_release():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_DATA['source_sha256']
    for bank,prefix,count in ((LESSON_9.whiteboard_questions,'w',15),(PRACTICE_BANK,'p',15),(MASTERY_BANK,'m',5),(REASSESSMENT_BANK,'r',3)):
        assert [q.id for q in bank]==[f'g8-ae-l09-{prefix}{n:02}' for n in range(1,count+1)]
    assert readiness_for(LESSON_9).value=='published'
    assert not [f for f in validate_curriculum([curriculum_repository.get_grade('grade-8')]) if f.lesson_id==LESSON_9.id]
    assert {tag for q in MASTERY_BANK for tag in q.misconception_tags}<=set(MISCONCEPTION_REPAIRS)

def test_complete_worked_steps_and_verifications():
    assert {q.whiteboard.visualization.template for q in LESSON_9.whiteboard_questions}=={'context_translation_strip_native','number_relationship_native','money_model_native','perimeter_model_native','sharing_bar_model_native','age_timeline_native','rate_table_native','error_diagnosis_context_native'}
    for q in LESSON_9.whiteboard_questions:
        board=q.whiteboard
        assert len(board.steps)>=4 and board.initial_expression==board.problem
        assert board.steps[-1].after_expression.startswith('Checked:') and board.steps[-1].state_after['verification_complete']
        assert q.answer and q.full_memo and q.expected_evidence
        for i,step in enumerate(board.steps):
            assert step.before_expression!=step.after_expression,(q.id,i)
            assert [e.text for e in step.events if e.type=='caption']==[e.text for e in step.events if e.type=='narration']
            assert min(e.at_ms for e in step.events if e.type=='show_operation')<min(e.at_ms for e in step.events if e.type=='reveal')
            if i: assert step.before_expression==board.steps[i-1].after_expression
    assert 'both plans cost R120' in LESSON_9.whiteboard_questions[9].whiteboard.steps[-1].after_expression
    assert 'R515' in LESSON_9.whiteboard_questions[14].whiteboard.steps[-1].after_expression

def test_api_preview_and_practice_gate():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/algebraic-equations').json()
        row=next(row for group in topic['subtopics'] for row in group['lessons'] if row['id']==LESSON_9.id)
        assert row['readiness']=='published' and row['usable']
        response=client.get(f'/api/v1/lessons/{LESSON_9.id}')
        if response.status_code==200:
            for q in response.json()['whiteboard_questions']:
                assert 'answer' not in q and 'full_memo' not in q
                board=q['whiteboard']
                assert len(board['steps'])==1 and not board['steps'][0]['events']
                assert board['steps'][0]['after_expression']==board['steps'][0]['before_expression']
                source=board['visualization']['parameters']['source_data']
                keys={part.partition('=')[0].strip() for part in source.split('; ')}
                assert not keys.intersection({'solution','equation','correct_equation','final_prices','dimensions'}),q['id']
            for n in range(1,16):
                revealed=client.post(f'/api/v1/lessons/{LESSON_9.id}/questions/g8-ae-l09-w{n:02}/reveal')
                assert revealed.status_code==200,n
                assert revealed.json()['whiteboard']['steps'][-1]['state_after']['verification_complete']
        else:assert response.status_code==401
        prefix=f'/api/v1/practice/{LESSON_9.id}'
        practice=client.get(prefix).json()
        assert len(practice['questions'])==15 and 'accepted_answers' not in str(practice)
        session=client.post(prefix+'/sessions').json()['session_id']
        failed=client.post(prefix+f'/sessions/{session}/mastery',json={'answers':{q.id:'incorrect' for q in MASTERY_BANK}})
        assert failed.status_code==200 and not failed.json()['mastered'] and failed.json()['repair_routes']
        assert client.get(prefix+f'/sessions/{session}/reassessment').status_code==409
        assert client.post(prefix+f'/sessions/{session}/repair/complete').json()['reassessment_unlocked']
        assert len(client.get(prefix+f'/sessions/{session}/reassessment').json()['questions'])==3

def test_context_equations_and_constraints():
    assert 12+7==19 and 2*13-5==21
    assert 12*5+18==78 and 2*9+2*5==28
    assert 36+48==84 and 48-36==12
    assert 18+19+20==57 and 10+34==44 and 3*10+4==34
    assert 15+6*7==57 and 2*10-3==17
    assert 80+2*20==20+5*20==120
    assert 8.5+12+11.5==32 and 8.5+11.5>12
    assert 150+25*10==400 and 90+120==210
    assert 30*5+50*8==550 and 4*65+3*85==515


def test_concise_learner_answers_are_scored_without_partial_multipart_credit():
    from app.practice.service import check_answer
    from app.api.v1.practice import _score_assessment
    assert check_answer('g8-ae-l09-p01','16')
    assert check_answer('g8-ae-l09-p04','10 cm by 6 cm')
    assert not check_answer('g8-ae-l09-p04','6')
    assert check_answer('g8-ae-l09-p15','x=R50; learner=R58; premium=R78')
    assert not check_answer('g8-ae-l09-p15','50')
    answers={item.id:item.accepted_answers[0] for item in MASTERY_BANK}
    assert _score_assessment(MASTERY_BANK,answers)[0]==5


def test_source_extractor_is_deterministic():
    import sys
    sys.path.insert(0,str(SOURCE.parents[4]/"tools"))
    from extract_grade8_lesson9 import compile_lesson
    assert compile_lesson()==SOURCE_DATA
