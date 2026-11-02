"""End to end contract for two mathematically distinct pattern investigations."""
from copy import deepcopy
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.patterns_runtime import LESSON_5,LESSON_6,SCENES_5,SCENES_6
from app.curriculum.grade8.assessment_patterns_56 import banks,value
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import CATALOGUE,validate_visualization


def test_thirty_examples_prove_their_answers_and_have_independent_assessment():
    for number,lesson,scenes in ((5,LESSON_5,SCENES_5),(6,LESSON_6,SCENES_6)):
        assert len(scenes)==len(lesson.whiteboard_questions)==15 and not lesson.release_approved
        assert len({s['problem'] for s in scenes})==15
        assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
        practice,mastery,parallel,repairs,rules=banks(number)
        assert (len(practice),len(mastery),len(parallel))==(15,5,3)
        assert repairs and rules and len({p.prompt for p in practice})==15
        for question,scene,p in zip(lesson.whiteboard_questions,scenes,practice,strict=True):
            assert scene['id']==question.id and len(question.whiteboard.steps)==4
            assert validate_visualization(question.whiteboard) is None
            assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in question.whiteboard.steps)
            assert p.answer_hidden_before_submission and p.prompt!=scene['problem']
            if number==5:
                good=scene['candidates'][0 if scene['correct_label']=='A' else 1]
                bad=scene['candidates'][1 if scene['correct_label']=='A' else 0]
                assert scene['terms']==[value(good['family'],good['a'],good['b'],n) for n in range(1,5)]
                n=scene['wrong_index']
                assert value(bad['family'],bad['a'],bad['b'],n)!=scene['terms'][n-1]
                assert scene['answer']==value(good['family'],good['a'],good['b'],scene['target_position'])
            else:
                assert scene['terms']==[value(scene['family'],scene['a'],scene['b'],n) for n in range(1,5)]
                assert scene['claimed']!=scene['answer']==value(scene['family'],scene['a'],scene['b'],scene['target_position'])


def test_invalid_counterexample_or_repaired_answer_is_rejected():
    definition=CATALOGUE[('algebra','grade8_pattern_board')]
    for lesson,wrong in ((LESSON_5,{'wrong_index':0}),(LESSON_6,{'answer':-999})):
        params=deepcopy(lesson.whiteboard_questions[0].whiteboard.visualization.parameters)
        scene=json.loads(params['scene_json']);scene.update(wrong);params['scene_json']=json.dumps(scene)
        with pytest.raises(ValueError):definition.validate(params)


def test_api_lists_six_and_conceals_private_math_until_reveal():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/numeric-geometric-patterns')
        assert topic.status_code==200
        assert [r['id'] for r in topic.json()['subtopics'][0]['lessons']]==[f'g8-patterns-{n:02}' for n in range(1,7)]
        for number in (5,6):
            lesson_id=f'g8-patterns-{number:02}'
            response=client.get('/api/v1/lessons/'+lesson_id)
            assert response.status_code==200
            questions=response.json()['whiteboard_questions'];assert len(questions)==15
            for question in questions:
                scene=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                assert not {'answer','memo','actions','correct_label','rule','a','b','family'}&scene.keys()
                assert len(question['whiteboard']['steps'])==1 and 'answer' not in question
            reveal=client.post(f'/api/v1/lessons/{lesson_id}/questions/g8-patterns-l{number:02}-w01/reveal')
            assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==4
            assert len(client.get(f'/api/v1/practice/{lesson_id}').json()['questions'])==15
            assert len(client.get(f'/api/v1/practice/{lesson_id}/mastery').json()['questions'])==5
