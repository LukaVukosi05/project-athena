import hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from app.curriculum.grade8.functions_relationships_lesson4 import DATA, LESSON, QUESTIONS, SOURCE
from app.curriculum.grade8.assessment_functions_lesson4 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.main import app

def test_source_math_and_distinct_visual_contract():
    source=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/functions-relationships'/SOURCE
    assert hashlib.sha256(source.read_bytes().replace(b'\r\n',b'\n')).hexdigest()==DATA['source_sha256']
    assert len(QUESTIONS)==len(PRACTICE_BANK)==15
    assert len(MASTERY_BANK)==5 and len(REASSESSMENT_BANK)==3
    assert len({q.whiteboard.visualization.parameters['scene_json'] for q in QUESTIONS})==15
    assert all(len(q.whiteboard.steps)==4 for q in QUESTIONS)
    assert not [f for f in validate_curriculum([GRADE_8]) if f.lesson_id==LESSON.id]
    for row in DATA['worked_examples']:
        scene=row['model']['scene']
        assert scene['length']*scene['width']==scene['area']
        if 'perimeter' in scene:
            assert 2*(scene['length']+scene['width'])==scene['perimeter']
    assert not LESSON.release_approved

def test_topic_three_has_six_lessons_and_topic_four_remains():
    with TestClient(app) as client:
        grade=client.get('/api/v1/curriculum/grades/grade-8')
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/functions-relationships')
        lesson=client.get('/api/v1/lessons/g8-functions-relationships-04')
        graphs=client.get('/api/v1/curriculum/grades/grade-8/topics/graphs')
        practice=client.get('/api/v1/practice/g8-functions-relationships-04')
        mastery=client.get('/api/v1/practice/g8-functions-relationships-04/mastery')
        revealed=client.post('/api/v1/lessons/g8-functions-relationships-04/questions/g8-fr-l04-w03/reveal')
    assert grade.status_code==topic.status_code==lesson.status_code==graphs.status_code==200
    assert [row['id'] for row in grade.json()['topics']][2:4]==['functions-relationships','graphs']
    assert [row['id'] for sub in topic.json()['subtopics'] for row in sub['lessons']]==[
        f'g8-functions-relationships-{n:02}' for n in range(1,7)]
    assert len(lesson.json()['whiteboard_questions'])==15
    assert all(len(q['whiteboard']['steps'])==1 and 'answer' not in q for q in lesson.json()['whiteboard_questions'])
    assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==4
    assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
