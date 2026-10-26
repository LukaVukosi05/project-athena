"""The table-rule lesson must carry actual row data and keep answer keys private."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from app.api.v1.practice import _score_assessment
from app.curriculum.grade8.assessment_functions_lesson3 import MASTERY_BANK,PRACTICE_BANK,REASSESSMENT_BANK
from app.curriculum.grade8.functions_relationships_lesson3 import DATA,LESSON,SOURCE
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.main import app

def test_source_semantics_and_question_specific_rows():
    doc=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/functions-relationships'/SOURCE
    assert hashlib.sha256(doc.read_bytes()).hexdigest()==DATA['source_sha256']
    assert len(LESSON.whiteboard_questions)==len(PRACTICE_BANK)==15
    assert len(MASTERY_BANK)==5 and sum(q.marks for q in MASTERY_BANK)==20
    assert len(REASSESSMENT_BANK)==3
    assert len({q.whiteboard.visualization.template for q in LESSON.whiteboard_questions})==6
    assert not [f for f in validate_curriculum([GRADE_8]) if f.lesson_id==LESSON.id]
    for row,q in zip(DATA['worked_examples'],LESSON.whiteboard_questions):
        p=q.whiteboard.visualization.parameters
        assert p['input_values']==[pair[0] for pair in row['model']['rows']]
        assert p['output_values']==[pair[1] if pair[1] is not None else '?' for pair in row['model']['rows']]
        assert len(q.whiteboard.steps)==len(row['steps'])+1
        assert all(s.before_expression!=s.after_expression for s in q.whiteboard.steps)
        assert all(s.narration==next(e.text for e in s.events if e.type=='caption') for s in q.whiteboard.steps)
        assert q.whiteboard.steps[-1].after_expression.startswith('Checked:')
        assert 'Ã' not in ''.join(s.after_expression for s in q.whiteboard.steps)
    assert DATA['worked_examples'][4]['model']['rows']==[[0,3],[2,11],[3,None],[4,19]]
    assert DATA['worked_examples'][8]['answer'].startswith('No;')
    assert DATA['worked_examples'][14]['answer'].endswith('input 6 gives 22.')

def test_public_api_registers_third_lesson_and_conceals_memo():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/functions-relationships')
        assert topic.status_code==200
        assert [row['id'] for sub in topic.json()['subtopics'] for row in sub['lessons']]==[
            'g8-functions-relationships-01','g8-functions-relationships-02',LESSON.id]
        assert 'grade8-table-rules-renderers.js' in client.get('/lesson.html').text
        response=client.get('/api/v1/lessons/'+LESSON.id)
        assert response.status_code==200,response.text
        questions=response.json()['whiteboard_questions']
        assert len(questions)==15
        assert all(q['solution_gated'] and len(q['whiteboard']['steps'])==1 for q in questions)
        assert all('answer' not in q and 'full_memo' not in q for q in questions)
        revealed=client.post(f'/api/v1/lessons/{LESSON.id}/questions/g8-fr-l03-w15/reveal')
        assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==6
        practice=client.get('/api/v1/practice/'+LESSON.id)
        assert practice.status_code==200 and len(practice.json()['questions'])==15
        assert all('accepted_answers' not in q for q in practice.json()['questions'])
        mastery=client.get('/api/v1/practice/'+LESSON.id+'/mastery')
        assert mastery.status_code==200 and len(mastery.json()['questions'])==5
        assert all('answer' not in q for q in mastery.json()['questions'])

def test_mastery_key_scores():
    score,review,tags=_score_assessment(MASTERY_BANK,{q.id:q.answer for q in MASTERY_BANK})
    assert score==5 and all(item['correct'] for item in review) and not tags
