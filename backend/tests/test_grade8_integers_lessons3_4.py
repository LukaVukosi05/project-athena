"""Source integrity, full arithmetic and public/private gates for integer operations."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.integer_evaluator import evaluate
from app.curriculum.grade8.integers_advanced_runtime import LESSON_3,LESSON_4,SCENES_3,SCENES_4
from app.curriculum.grade8.assessment_integers_advanced import banks,PRACTICE,MASTERY,REASSESS
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization


def test_every_authored_expression_and_parallel_bank():
    for n,lesson,scenes in ((3,LESSON_3,SCENES_3),(4,LESSON_4,SCENES_4)):
        assert not lesson.release_approved
        assert len(scenes)==len(lesson.whiteboard_questions)==15
        assert len({s['expression'] for s in scenes})==15
        assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
        practice,mastery,reassess,repair,rules=banks(n)
        assert (len(practice),len(mastery),len(reassess))==(15,5,3)
        assert repair and rules
        for q,s,p,expr in zip(lesson.whiteboard_questions,scenes,practice,PRACTICE[n],strict=True):
            assert evaluate(s['source_expression'])==s['answer']
            assert q.id==s['id'] and len(q.whiteboard.steps)==len(s['actions'])
            assert q.whiteboard.visualization.template=='grade8_integer_operations'
            assert validate_visualization(q.whiteboard) is None
            assert p.answer_hidden_before_submission and p.accepted_answers==[str(evaluate(expr))]
            assert p.prompt!=s['problem']
            assert all(step.narration==next(ev.text for ev in step.events if ev.type=='caption') for step in q.whiteboard.steps)
        for item,expr in zip(mastery,MASTERY[n],strict=True):assert item.answer==str(evaluate(expr))
        for item,expr in zip(reassess,REASSESS[n],strict=True):assert item.answer==str(evaluate(expr))


def test_invalid_answer_rejected():
    validate=CATALOGUE[('algebra','grade8_integer_operations')].validate
    params=deepcopy(LESSON_4.whiteboard_questions[0].whiteboard.visualization.parameters)
    scene=json.loads(params['scene_json']);scene['answer']=-99;params['scene_json']=json.dumps(scene)
    with pytest.raises(ValueError):validate(params)


def test_topic_and_answer_gates():
    from app.core.config import get_settings
    settings=get_settings()
    previous=settings.unlock_all_lessons
    settings.unlock_all_lessons=True
    try:
        with TestClient(app) as client:
            response=client.get('/api/v1/curriculum/grades/grade-8/topics/integers')
            assert response.status_code==200
            assert [x['id'] for x in response.json()['subtopics'][0]['lessons']]==[f'g8-integers-{n:02}' for n in range(1,7)]
            for n in (3,4):
                lesson_id=f'g8-integers-{n:02}'
                payload=client.get(f'/api/v1/lessons/{lesson_id}')
                assert payload.status_code==200
                for question in payload.json()['whiteboard_questions']:
                    scene=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                    assert not {'answer','memo','actions','rows','misconception'}&scene.keys()
                    assert len(question['whiteboard']['steps'])==1 and 'answer' not in question
                revealed=client.post(f'/api/v1/lessons/{lesson_id}/questions/g8-int-l{n:02}-w01/reveal')
                assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])>=5
                assert len(client.get(f'/api/v1/practice/{lesson_id}').json()['questions'])==15
                assert len(client.get(f'/api/v1/practice/{lesson_id}/mastery').json()['questions'])==5
    finally:
        settings.unlock_all_lessons=previous
