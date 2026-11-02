import json

from fastapi.testclient import TestClient
from app.core.config import get_settings

from app.curriculum.grade8.graphs_lesson2 import LESSON, QUESTIONS, SCENE_DATA
from app.curriculum.grade8.assessment_graphs_lesson2 import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.main import app
from app.visualization.registry import validate_visualization


def test_graphs_pair_has_authored_progressive_question_specific_scenes():
    assert len(SCENE_DATA) == len(QUESTIONS) == len(PRACTICE_BANK) == 15
    assert len(MASTERY_BANK) == 5 and len(REASSESSMENT_BANK) == 3
    assert [lesson.id for lesson in GRADE_8.topics[3].subtopics[0].lessons] == ["g8-graphs-01", "g8-graphs-02", "g8-graphs-03", "g8-graphs-04", "g8-graphs-05", "g8-graphs-06"]
    assert not [failure for failure in validate_curriculum([GRADE_8]) if failure.lesson_id == LESSON.id]
    assert not LESSON.release_approved  # Teacher review is still required.
    for scene, question in zip(SCENE_DATA, QUESTIONS, strict=True):
        assert question.id == scene["id"]
        assert len(question.whiteboard.steps) == 4
        assert all(step.narration == next(event.text for event in step.events if event.type == "caption") for step in question.whiteboard.steps)
        assert json.loads(question.whiteboard.visualization.parameters["scene_json"]) == scene
        assert scene["graph"]["table"] == scene["graph"]["points"]
        assert not validate_visualization(question.whiteboard)


def test_discrete_and_nonlinear_scenes_cannot_imply_straight_lines():
    assert SCENE_DATA[11]["graph"]["mode"] == "discrete"
    assert SCENE_DATA[14]["graph"]["mode"] == "nonlinear"
    assert SCENE_DATA[10]["given"][0]["error"]
    assert SCENE_DATA[10]["derived"][-1]["reveal_step"] == 4
    assert SCENE_DATA[9]["graph"]["mode"] == "given_line"


def test_premium_lesson_is_registered_without_leaking_answers():
    with TestClient(app) as client:
        lesson = client.get('/api/v1/lessons/g8-graphs-02')
        topic = client.get('/api/v1/curriculum/grades/grade-8/topics/graphs')
    if get_settings().unlock_all_lessons:
        assert lesson.status_code == 200
        questions=lesson.json()['whiteboard_questions']
        assert len(questions)==15
        assert all(len(item['whiteboard']['steps']) == 1 and 'answer' not in item for item in questions)
    else:
        assert lesson.status_code == 401
    assert topic.status_code == 200
    assert len(topic.json()['subtopics'][0]['lessons']) == 6
