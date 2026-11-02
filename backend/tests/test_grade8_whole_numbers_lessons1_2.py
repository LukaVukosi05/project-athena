"""Math and API contract for Whole Numbers Lessons 1 and 2."""
import json
from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.whole_numbers_runtime import LESSON_1,LESSON_2,SCENES_1,SCENES_2
from app.curriculum.grade8.assessment_whole_numbers import banks,factor_value,property_value
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization


def test_thirty_questions_and_each_composite_split_are_real():
    for number,lesson,scenes in ((1,LESSON_1,SCENES_1),(2,LESSON_2,SCENES_2)):
        assert not lesson.release_approved
        assert len(scenes)==len(lesson.whiteboard_questions)==15
        assert len({s['problem'] for s in scenes})==15
        assert not [error for error in validate_curriculum([GRADE_8]) if error.lesson_id==lesson.id]
        practice,mastery,parallel,repairs,rules=banks(number)
        assert (len(practice),len(mastery),len(parallel))==(15,5,3)
        assert repairs and rules and len({q.prompt for q in practice})==15
        for question,scene,p in zip(lesson.whiteboard_questions,scenes,practice,strict=True):
            assert question.id==scene['id']
            assert len(question.whiteboard.steps)==len(scene['actions'])
            assert validate_visualization(question.whiteboard) is None
            assert p.answer_hidden_before_submission and p.prompt!=scene['problem']
            assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in question.whiteboard.steps)
            if number==1:
                assert p.accepted_answers==[property_value(scene,1)]
            else:
                assert len(scene['actions'])==3+max(len(leaves)-1 for leaves in scene['factors'])
                assert p.accepted_answers==[factor_value(scene,2)]


def test_bad_factorisation_or_identity_fails_validation():
    validate=CATALOGUE[('algebra','grade8_whole_number_board')].validate
    for question,modify in ((LESSON_1.whiteboard_questions[5],lambda s:s.update(answer=-100)),
                            (LESSON_2.whiteboard_questions[0],lambda s:s['factors'][0].append(2))):
        params=deepcopy(question.whiteboard.visualization.parameters)
        scene=json.loads(params['scene_json']);modify(scene);params['scene_json']=json.dumps(scene)
        with pytest.raises(ValueError):validate(params)


def test_catalogue_and_public_solution_gate():
    with TestClient(app) as client:
        response=client.get('/api/v1/curriculum/grades/grade-8/topics/whole-numbers')
        assert response.status_code==200
        assert [row['id'] for row in response.json()['subtopics'][0]['lessons']]==['g8-whole-numbers-01','g8-whole-numbers-02']
        for number in (1,2):
            lid=f'g8-whole-numbers-{number:02}'
            lesson=client.get(f'/api/v1/lessons/{lid}')
            assert lesson.status_code==200
            questions=lesson.json()['whiteboard_questions'];assert len(questions)==15
            for q in questions:
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert len(q['whiteboard']['steps'])==1 and not {'answer','actions','factors','memo'}&scene.keys()
            reveal=client.post(f'/api/v1/lessons/{lid}/questions/g8-whole-l{number:02}-w01/reveal')
            assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])>=4
            assert len(client.get(f'/api/v1/practice/{lid}').json()['questions'])==15
            assert len(client.get(f'/api/v1/practice/{lid}/mastery').json()['questions'])==5
