"""Signed math, staged whiteboards, and private assessment gates."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.integers_runtime import LESSON_1,LESSON_2,SCENES_1,SCENES_2
from app.curriculum.grade8.assessment_integers import banks,variant
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization


def test_signed_math_and_each_independent_question():
    for n,lesson,scenes in ((1,LESSON_1,SCENES_1),(2,LESSON_2,SCENES_2)):
        assert not lesson.release_approved
        assert len(scenes)==len(lesson.whiteboard_questions)==15
        assert len({s['problem'] for s in scenes})==15
        assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
        p,m,r,repairs,rules=banks(n)
        assert (len(p),len(m),len(r))==(15,5,3) and repairs and rules
        for q,s,pr in zip(lesson.whiteboard_questions,scenes,p,strict=True):
            assert q.id==s['id'] and len(q.whiteboard.steps)==len(s['actions'])
            assert validate_visualization(q.whiteboard) is None
            assert pr.answer_hidden_before_submission and pr.prompt!=s['problem']
            assert pr.accepted_answers[0]==variant(s,2)[1]
            assert all(step.narration==next(ev.text for ev in step.events if ev.type=='caption') for step in q.whiteboard.steps)
            if n==2:
                path=[s['start']]
                for sign,v in s['operations']:path.append(path[-1]+(v if sign=='+' else -v))
                assert path==s['path'] and path[-1]==s['answer']
                assert len(s['actions'])==len(s['operations'])+3


def test_wrong_direction_and_wrong_comparison_rejected():
    validate=CATALOGUE[('algebra','grade8_integer_board')].validate
    for q,wrong in ((LESSON_1.whiteboard_questions[0],lambda s:s.update(answer=-999)),
                    (LESSON_2.whiteboard_questions[0],lambda s:s['path'].pop())):
        params=deepcopy(q.whiteboard.visualization.parameters)
        s=json.loads(params['scene_json']);wrong(s);params['scene_json']=json.dumps(s)
        with pytest.raises(ValueError):validate(params)


def test_topic_appears_and_api_conceals_answer_until_reveal():
    with TestClient(app) as client:
        response=client.get('/api/v1/curriculum/grades/grade-8/topics/integers')
        assert response.status_code==200
        assert [x['id'] for x in response.json()['subtopics'][0]['lessons']]==[f'g8-integers-{i:02}' for i in range(1,7)]
        for n in (1,2):
            lesson_id=f'g8-integers-{n:02}'
            resp=client.get(f'/api/v1/lessons/{lesson_id}')
            assert resp.status_code==200
            for q in resp.json()['whiteboard_questions']:
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert not {'answer','memo','actions','path'}&scene.keys()
                assert len(q['whiteboard']['steps'])==1 and 'answer' not in q
            revealed=client.post(f'/api/v1/lessons/{lesson_id}/questions/g8-int-l{n:02}-w01/reveal')
            assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])>=4
            assert len(client.get(f'/api/v1/practice/{lesson_id}').json()['questions'])==15
            assert len(client.get(f'/api/v1/practice/{lesson_id}/mastery').json()['questions'])==5
