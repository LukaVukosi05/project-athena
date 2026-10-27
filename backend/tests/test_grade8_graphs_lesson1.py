from fastapi.testclient import TestClient
from app.curriculum.grade8.graphs_lesson1 import LESSON, QUESTIONS, SCENE_DATA
from app.curriculum.grade8.assessment_graphs_lesson1 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.main import app

def test_graphs_source_question_steps_and_private_assessments():
    assert len(QUESTIONS) == len(SCENE_DATA) == len(PRACTICE_BANK) == 15
    assert len(MASTERY_BANK) == 5 and len(REASSESSMENT_BANK) == 3
    assert len({q.whiteboard.visualization.parameters['scene_json'] for q in QUESTIONS}) == 15
    assert all(len(q.whiteboard.steps) == 4 for q in QUESTIONS)
    assert not [f for f in validate_curriculum([GRADE_8]) if f.lesson_id == LESSON.id]
    assert not LESSON.release_approved

def test_graphs_public_payload_reveals_one_step_at_a_time():
    with TestClient(app) as client:
        result = client.get('/api/v1/lessons/g8-graphs-01')
        topic = client.get('/api/v1/curriculum/grades/grade-8/topics/graphs')
    assert result.status_code == 200
    assert topic.status_code == 200
    assert len(result.json()['whiteboard_questions']) == 15
    assert all(len(q['whiteboard']['steps']) == 1 and 'answer' not in q for q in result.json()['whiteboard_questions'])
    assert topic.json()['subtopics'][0]['lessons'][0]['readiness'] == 'verified'
