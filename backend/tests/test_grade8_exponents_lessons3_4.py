"""Content, gated endpoints and exact scene contract for Grade 8 roots."""
import json
from copy import deepcopy
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.exponent_roots_math import solve
from app.curriculum.grade8.exponents_runtime import LESSON_3, LESSON_4, SCENES_3, SCENES_4
from app.curriculum.grade8.assessment_exponents import banks
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE


def test_exact_scenes_private_banks_and_validation():
    failures=[e for e in validate_curriculum([GRADE_8]) if e.topic_id=='exponents']
    assert failures == [], failures[:3]
    for n, lesson, scenes in ((3,LESSON_3,SCENES_3),(4,LESSON_4,SCENES_4)):
        practice, mastery, reassess, repair, rules = banks(n)
        assert (len(scenes),len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassess)) == (15,15,15,5,3)
        assert {q.prompt for q in practice}.isdisjoint(s['problem'] for s in scenes)
        assert {q.prompt for q in mastery}.isdisjoint(s['problem'] for s in scenes)
        assert all('^' not in s['problem'] for s in scenes)
        for scene, question in zip(scenes,lesson.whiteboard_questions,strict=True):
            assert solve(scene['kind'],scene['values']) == (scene['answer'],scene['rows'],scene['problem'],scene['memo'])
            assert len(question.whiteboard.steps) == len(scene['rows'])+2
            assert all(st.narration == next(e.text for e in st.events if e.type=='caption') for st in question.whiteboard.steps)
            params=deepcopy(question.whiteboard.visualization.parameters)
            tampered=json.loads(params['scene_json']);tampered['values'][0]='999';params['scene_json']=json.dumps(tampered)
            with pytest.raises(ValueError):
                CATALOGUE[('algebra',question.whiteboard.visualization.template)].validate(params)
    assert solve('square_area',['169'])[0] == '13 cm; 52 cm'
    assert solve('cube_volume',['343'])[0] == '7 cm'
    assert solve('mixed',['2','3','36','8'])[0] == '20'


def test_lessons_practice_and_answer_gate():
    settings=get_settings();previous=settings.unlock_all_lessons;settings.unlock_all_lessons=True
    try:
        with TestClient(app) as client:
            topic=client.get('/api/v1/curriculum/grades/grade-8/topics/exponents')
            assert topic.status_code == 200
            assert [x['id'] for x in topic.json()['subtopics'][0]['lessons']] == [f'g8-exponents-{n:02}' for n in range(1,7)]
            for n in (3,4):
                lid=f'g8-exponents-{n:02}'
                response=client.get(f'/api/v1/lessons/{lid}')
                assert response.status_code == 200
                for question in response.json()['whiteboard_questions']:
                    scene=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                    assert not {'answer','memo','rows','misconception'} & scene.keys()
                    assert len(question['whiteboard']['steps'])==1 and question['solution_gated']
                reveal=client.post(f'/api/v1/lessons/{lid}/questions/g8-exp-l{n:02}-w01/reveal')
                assert reveal.status_code == 200
                assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
    finally:
        settings.unlock_all_lessons=previous
