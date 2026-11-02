"""Pattern rule tables: mathematical validity, original assessments and answer gate."""
from copy import deepcopy
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.patterns_runtime import LESSON_3,LESSON_4,SCENES_3,SCENES_4
from app.curriculum.grade8.assessment_patterns_34 import banks,evaluate
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization


def test_each_rule_matches_given_terms_and_all_question_states():
    for lesson,scenes in ((LESSON_3,SCENES_3),(LESSON_4,SCENES_4)):
        assert not lesson.release_approved
        assert (len(scenes),len(lesson.whiteboard_questions))==(15,15)
        assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
        assert len({s['title'] for s in scenes})==15
        for q,scene in zip(lesson.whiteboard_questions,scenes,strict=True):
            assert scene['id']==q.id and scene['terms']==[evaluate(scene,n) for n in range(1,5)]
            assert len(q.whiteboard.steps)==4
            assert validate_visualization(q.whiteboard) is None
            assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in q.whiteboard.steps)
            assert str(scene['answer']) in q.whiteboard.steps[-1].after_expression
            if lesson==LESSON_4:assert scene['answer']==evaluate(scene,scene['target_position'])
        practice,mastery,parallel,repairs,rules=banks(lesson.order)
        assert (len(practice),len(mastery),len(parallel))==(15,5,3)
        assert len({p.prompt for p in practice})==15
        assert all(p.answer_hidden_before_submission for p in practice)
        assert repairs and rules
        assert all(m.prompt!=scenes[i+8]['problem'] for i,m in enumerate(mastery))


def test_bad_formula_or_missing_value_rejected():
    definition=CATALOGUE[('algebra','grade8_pattern_board')]
    for question,mutation in ((LESSON_3.whiteboard_questions[0],lambda s:s.update(rule='9n+1')),
                              (LESSON_4.whiteboard_questions[0],lambda s:s.update(answer=-999))):
        params=deepcopy(question.whiteboard.visualization.parameters)
        scene=json.loads(params['scene_json']);mutation(scene);params['scene_json']=json.dumps(scene)
        with pytest.raises(ValueError):definition.validate(params)


def test_api_lists_both_and_keeps_rule_private_until_reveal():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/numeric-geometric-patterns')
        assert topic.status_code==200
        assert [row['id'] for row in topic.json()['subtopics'][0]['lessons']][:4]==[f'g8-patterns-{n:02}' for n in range(1,5)]
        for number in (3,4):
            lesson_id=f'g8-patterns-{number:02}'
            preview=client.get('/api/v1/lessons/'+lesson_id)
            assert preview.status_code==200
            questions=preview.json()['whiteboard_questions']
            assert len(questions)==15
            for question in questions:
                scene=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                assert not {'answer','memo','actions'}&scene.keys()
                if number==3:assert not {'rule','a','b'}&scene.keys()
                assert len(question['whiteboard']['steps'])==1
                assert 'answer' not in question
            revealed=client.post(f'/api/v1/lessons/{lesson_id}/questions/g8-patterns-l{number:02}-w01/reveal')
            assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==4
            practice=client.get(f'/api/v1/practice/{lesson_id}')
            mastery=client.get(f'/api/v1/practice/{lesson_id}/mastery')
            assert practice.status_code==mastery.status_code==200
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
