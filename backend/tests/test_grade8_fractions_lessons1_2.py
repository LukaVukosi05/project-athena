"""Exact rational arithmetic, question-specific strips, and answer-gated APIs."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.fractions_runtime import LESSON_1,LESSON_2,SCENES_1,SCENES_2
from app.curriculum.grade8.fractions_math import answer,common_denominator
from app.curriculum.grade8.assessment_fractions import banks
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization

def test_all_authored_questions_and_private_parallel_banks():
    for n,lesson,scenes in ((1,LESSON_1,SCENES_1),(2,LESSON_2,SCENES_2)):
        assert not lesson.release_approved
        assert len(scenes)==len(lesson.whiteboard_questions)==15
        assert len({s['problem'] for s in scenes})==15
        assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
        p,m,r,repairs,rules=banks(n)
        assert (len(p),len(m),len(r))==(15,5,3) and repairs and rules
        for q,s,practice in zip(lesson.whiteboard_questions,scenes,p,strict=True):
            assert q.id==s['id'] and len(q.whiteboard.steps)==5
            assert answer(s['kind'],s['values'],s.get('operators'))==s['answer']
            assert common_denominator(s['values'])==s['common_denominator']
            assert validate_visualization(q.whiteboard) is None
            assert practice.prompt!=s['problem'] and practice.answer_hidden_before_submission
            assert all(step.narration==next(ev.text for ev in step.events if ev.type=='caption') for step in q.whiteboard.steps)

def test_incorrect_fraction_value_or_unit_rejected():
    validate=CATALOGUE[('algebra','grade8_fraction_strips')].validate
    params=deepcopy(LESSON_2.whiteboard_questions[0].whiteboard.visualization.parameters)
    s=json.loads(params['scene_json']);s['answer']='99/100';params['scene_json']=json.dumps(s)
    with pytest.raises(ValueError):validate(params)
    s['answer']='3/4';s['common_denominator']=99;params['scene_json']=json.dumps(s)
    with pytest.raises(ValueError):validate(params)

def test_topic_preview_reveal_and_practice_api():
    settings=get_settings();prior=settings.unlock_all_lessons;settings.unlock_all_lessons=True
    try:
        with TestClient(app) as client:
            topic=client.get('/api/v1/curriculum/grades/grade-8/topics/common-fractions')
            assert topic.status_code==200
            assert [x['id'] for x in topic.json()['subtopics'][0]['lessons']][:6]==['g8-common-fractions-01','g8-common-fractions-02','g8-common-fractions-03','g8-common-fractions-04','g8-common-fractions-05','g8-common-fractions-06']
            for n in (1,2):
                lid=f'g8-common-fractions-{n:02}'
                response=client.get('/api/v1/lessons/'+lid)
                assert response.status_code==200
                for q in response.json()['whiteboard_questions']:
                    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                    assert not {'answer','memo','rows','misconception'}&scene.keys()
                    assert len(q['whiteboard']['steps'])==1 and 'answer' not in q
                revealed=client.post(f'/api/v1/lessons/{lid}/questions/g8-frac-l{n:02}-w01/reveal')
                assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
                assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
                assert len(client.get(f'/api/v1/practice/{lid}/mastery').json()['questions'])==5
    finally:settings.unlock_all_lessons=prior
