"""Properties and context mathematics, private banks, and staged public payload."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.integer_evaluator import evaluate
from app.curriculum.grade8.integers_advanced_runtime import LESSON_5,LESSON_6,SCENES_5,SCENES_6
from app.curriculum.grade8.assessment_integers_reasoning import banks,PROPERTY_PRACTICE,CONTEXT_PRACTICE,property_answer
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization

def test_authored_math_source_and_every_question():
    for n,lesson,scenes in ((5,LESSON_5,SCENES_5),(6,LESSON_6,SCENES_6)):
        assert not lesson.release_approved
        assert len(scenes)==len(lesson.whiteboard_questions)==15
        assert len({s['problem'] for s in scenes})==15
        assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
        practice,mastery,reassessment,repairs,rules=banks(n)
        assert (len(practice),len(mastery),len(reassessment))==(15,5,3) and repairs and rules
        for q,s,p in zip(lesson.whiteboard_questions,scenes,practice,strict=True):
            assert q.id==s['id'] and len(q.whiteboard.steps)==5
            assert evaluate(s['source_expression'])==(s['left_value'] if n==5 else s['answer'])
            if n==5:assert (evaluate(s['source_expression'])==evaluate(s['comparison_expression'])) is s['claim_true'] and s['answer']==('true' if s['claim_true'] else 'false')
            assert validate_visualization(q.whiteboard) is None
            assert p.prompt!=s['problem'] and p.answer_hidden_before_submission
            assert all(step.narration==next(ev.text for ev in step.events if ev.type=='caption') for step in q.whiteboard.steps)
        assert [p.accepted_answers[0] for p in practice]==([property_answer(pair) for pair in PROPERTY_PRACTICE] if n==5 else [str(evaluate(expr)) for _,expr in CONTEXT_PRACTICE])

def test_false_property_claim_rejected_when_labelled_true():
    validate=CATALOGUE[('algebra','grade8_integer_reasoning')].validate
    params=deepcopy(LESSON_5.whiteboard_questions[2].whiteboard.visualization.parameters)
    scene=json.loads(params['scene_json']);assert not scene['claim_true']
    scene['claim_true']=True;params['scene_json']=json.dumps(scene)
    with pytest.raises(ValueError):validate(params)

def test_topic_api_gates_and_assessments():
    settings=get_settings();previous=settings.unlock_all_lessons;settings.unlock_all_lessons=True
    try:
        with TestClient(app) as client:
            topic=client.get('/api/v1/curriculum/grades/grade-8/topics/integers')
            assert topic.status_code==200
            assert [x['id'] for x in topic.json()['subtopics'][0]['lessons']]==[f'g8-integers-{n:02}' for n in range(1,7)]
            for n in (5,6):
                lid=f'g8-integers-{n:02}'
                payload=client.get('/api/v1/lessons/'+lid)
                assert payload.status_code==200
                for q in payload.json()['whiteboard_questions']:
                    scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                    assert not {'answer','memo','actions','rows','misconception','left_value','claim_true'}&scene.keys()
                    assert len(q['whiteboard']['steps'])==1 and 'answer' not in q
                revealed=client.post(f'/api/v1/lessons/{lid}/questions/g8-int-l{n:02}-w01/reveal')
                assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
                assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
                assert len(client.get(f'/api/v1/practice/{lid}/mastery').json()['questions'])==5
    finally:settings.unlock_all_lessons=previous
