"""Source and assessment gates for the final Grade 8 equations lesson."""
import hashlib
import sys
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.content_manifest import readiness_for
from app.curriculum.grade8.lesson10_runtime import LESSON_10, SOURCE_DATA
from app.curriculum.grade8.assessment_lesson10 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK, MISCONCEPTION_REPAIRS
from app.curriculum.repository import curriculum_repository
from app.curriculum.validation import validate_curriculum
from app.api.v1.practice import _score_assessment

SOURCE=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/algebraic-equations/Project_Athena_Grade8_Algebraic_Equations_Gold_Pack_v1_0.docx'

def test_source_and_release():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_DATA['source_sha256']
    for bank,prefix,count in ((LESSON_10.whiteboard_questions,'w',15),(PRACTICE_BANK,'p',15),(MASTERY_BANK,'m',5),(REASSESSMENT_BANK,'r',3)):
        assert [q.id for q in bank]==[f'g8-ae-l10-{prefix}{i:02}' for i in range(1,count+1)]
    assert readiness_for(LESSON_10).value=='published'
    assert not [x for x in validate_curriculum([curriculum_repository.get_grade('grade-8')]) if x.lesson_id==LESSON_10.id]
    assert len(MISCONCEPTION_REPAIRS)==10
    sys.path.insert(0,str(SOURCE.parents[4]/'tools'))
    from extract_grade8_lesson10 import compile_lesson
    assert compile_lesson()==SOURCE_DATA

def test_fifteen_complete_diagnostic_timelines():
    questions=LESSON_10.whiteboard_questions
    assert len({q.whiteboard.visualization.template for q in questions})==10
    for q in questions:
        board=q.whiteboard
        assert len(board.steps)>=5 and board.initial_expression==board.problem
        assert board.steps[-1].after_expression.startswith('Checked:'),q.id
        assert q.answer and q.full_memo and q.expected_evidence
        for i,step in enumerate(board.steps):
            assert step.before_expression!=step.after_expression,(q.id,i)
            assert [e.text for e in step.events if e.type=='caption']==[e.text for e in step.events if e.type=='narration']
            assert min(e.at_ms for e in step.events if e.type=='show_operation')<min(e.at_ms for e in step.events if e.type=='reveal')
            if i: assert step.before_expression==board.steps[i-1].after_expression
    assert 'is valid' in questions[5].whiteboard.steps[1].after_expression
    assert '12 - 7' in questions[0].whiteboard.steps[3].after_expression
    assert 'distribution-error' in questions[14].whiteboard.steps[-1].after_expression

def test_api_preview_and_transfer_gate():
    with TestClient(app) as client:
        page = client.get('/lesson.html')
        assert 'no-store' in page.headers['cache-control']
        assert 'lesson-block-renderer.js?v=whiteboard-v10' in page.text
        lesson=client.get(f'/api/v1/lessons/{LESSON_10.id}')
        if lesson.status_code==200:
            for question in lesson.json()['whiteboard_questions']:
                assert 'answer' not in question and 'full_memo' not in question
                source = next(q for q in LESSON_10.whiteboard_questions if q.id == question['id'])
                assert question['total_step_count'] == len(source.whiteboard.steps) > 1
                board=question['whiteboard']
                assert len(board['steps'])==1 and not board['steps'][0]['events']
                assert board['steps'][0]['before_expression']==board['steps'][0]['after_expression']
                source_data=board['visualization']['parameters']['source_data']
                keys={field.partition('=')[0].strip() for field in source_data.split('; ')}
                assert not keys.intersection({'solution','correct_equation','correct_expansion','correct_intermediate','first_error_tag','classification','lcd'}),question['id']
            reveal=client.post(f'/api/v1/lessons/{LESSON_10.id}/questions/g8-ae-l10-w06/reveal')
            assert reveal.status_code==409
            submitted=client.post(f'/api/v1/lessons/{LESSON_10.id}/questions/g8-ae-l10-w06/diagnose',json={'first_error_and_repair':'The first line is correct; subtract 3, then divide by 2.'})
            assert submitted.status_code==200 and len(submitted.json()['whiteboard']['steps'])>=9
        else: assert lesson.status_code==401
        base=f'/api/v1/practice/{LESSON_10.id}'
        assert len(client.get(base).json()['questions'])==15
        public=client.get(base+'/mastery').json()
        assert len(public['questions'])==5 and 'answer' not in str(public['questions'])
        session=client.post(base+'/sessions').json()['session_id'];path=base+f'/sessions/{session}'
        answers={q.id:q.accepted_answers[0] for q in MASTERY_BANK}
        assert client.post(path+'/mastery',json={'answers':answers}).json()['mastered']
        answers['g8-ae-l10-m05']='7'
        failed=client.post(path+'/mastery',json={'answers':answers}).json()
        assert failed['questions_correct']==4 and not failed['mastered'] and not failed['context_verified']
        assert client.get(path+'/reassessment').status_code==409
        assert client.post(path+'/repair/complete').json()['reassessment_unlocked']
        fresh={q.id:q.accepted_answers[0] for q in REASSESSMENT_BANK}
        assert client.post(path+'/reassessment',json={'answers':fresh}).json()['ready']
        fresh['g8-ae-l10-r03']='8'
        assert not client.post(path+'/reassessment',json={'answers':fresh}).json()['ready']
        weak=client.post(path+'/mastery',json={'answers':{q.id:'incorrect' for q in MASTERY_BANK}}).json()
        assert weak['readiness_decision']=='repeat_diagnostic_required'
        assert client.post(path+'/repair/complete').status_code==409

def test_context_requires_mathematical_check():
    answers={q.id:q.accepted_answers[0] for q in MASTERY_BANK}
    assert _score_assessment(MASTERY_BANK,answers)[0]==5
    answers['g8-ae-l10-m05']='35+9h=98; h=7'
    assert _score_assessment(MASTERY_BANK,answers)[0]==4
    assert 3*7-5==16 and -2*(-9)==18 and 5-2*(-6)==17
    assert 18/3+18/6==9 and 2*7+2*5==24
    assert 4*(6+3)+2==2*6+26==38
