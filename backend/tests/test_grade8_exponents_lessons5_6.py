"""Exact checks and public answer gate for diagnosis and integrated exponent lessons."""
import json
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.exponent_reasoning_math import solve
from app.curriculum.grade8.exponent_reasoning_inputs import WORKED, PRACTICE, MASTERY, REASSESS
from app.curriculum.grade8.exponents_runtime import LESSON_5, LESSON_6, SCENES_5, SCENES_6
from app.curriculum.grade8.assessment_exponents import banks
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE


def test_authored_mathematics_and_independent_assessments():
    failures=[f for f in validate_curriculum([GRADE_8]) if f.topic_id=='exponents']
    assert not failures,failures[:3]
    for n,lesson,scenes in ((5,LESSON_5,SCENES_5),(6,LESSON_6,SCENES_6)):
        practice,mastery,reassess,repairs,rules=banks(n)
        assert (len(scenes),len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassess))==(15,15,15,5,3)
        assert len({s['problem'] for s in scenes})==15
        assert len({p.prompt for p in practice})==15
        assert {p.prompt for p in practice}.isdisjoint(s['problem'] for s in scenes)
        assert {p.prompt for p in mastery}.isdisjoint(s['problem'] for s in scenes)
        assert all('^' not in s['problem'] for s in scenes)
        assert set(s['kind'] for s in scenes)==({
            'sign_audit','root_audit','quotient_audit','root_sum_audit','mixed_audit'} if n==5 else {
            'square_perimeter_gap','cube_edge_gap','side_area_gap','root_power_compare','combined_perimeter'})
        for scene,question in zip(scenes,lesson.whiteboard_questions,strict=True):
            assert solve(scene['kind'],scene['values'])==(scene['answer'],scene['rows'],scene['problem'],scene['memo'])
            assert len(question.whiteboard.steps)==len(scene['rows'])+2
            assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in question.whiteboard.steps)
            params=deepcopy(question.whiteboard.visualization.parameters)
            tampered=json.loads(params['scene_json']);tampered['answer']='wrong';params['scene_json']=json.dumps(tampered)
            with pytest.raises(ValueError):CATALOGUE[('algebra',question.whiteboard.visualization.template)].validate(params)
    assert solve('sign_audit',['3','2'])[0]=='9'
    assert solve('root_sum_audit',['25','49'])[0]=='12'
    assert solve('square_perimeter_gap',['36','64'])[0]=='8 cm'
    assert solve('combined_perimeter',['36','64','27'])[0]=='59 m'
    with pytest.raises(ValueError):solve('square_perimeter_gap',['37','64'])


def test_topic_api_reveal_and_private_practice():
    settings=get_settings();previous=settings.unlock_all_lessons;settings.unlock_all_lessons=True
    try:
        with TestClient(app) as client:
            response=client.get('/api/v1/curriculum/grades/grade-8/topics/exponents')
            assert response.status_code==200
            assert [x['id'] for x in response.json()['subtopics'][0]['lessons']]==[f'g8-exponents-{i:02}' for i in range(1,7)]
            for n in (5,6):
                lid=f'g8-exponents-{n:02}'
                lesson=client.get(f'/api/v1/lessons/{lid}')
                assert lesson.status_code==200
                for q in lesson.json()['whiteboard_questions']:
                    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                    assert not {'answer','memo','rows','misconception'}&scene.keys()
                    assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
                assert client.post(f'/api/v1/lessons/{lid}/questions/g8-exp-l{n:02}-w01/reveal').status_code==200
                assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
    finally:
        settings.unlock_all_lessons=previous
