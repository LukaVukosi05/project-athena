import json
from copy import deepcopy
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.grade8.graphs_lesson5 import LESSON as L5, SCENE_DATA as S5
from app.curriculum.grade8.graphs_lesson6 import LESSON as L6, SCENE_DATA as S6
from app.curriculum.grade8.assessment_graphs_lesson5 import PRACTICE_BANK as P5, MASTERY_BANK as M5, REASSESSMENT_BANK as R5
from app.curriculum.grade8.assessment_graphs_lesson6 import PRACTICE_BANK as P6, MASTERY_BANK as M6, REASSESSMENT_BANK as R6
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import validate_visualization, CATALOGUE

@pytest.mark.parametrize('lesson,scenes,practice,mastery,reassess,kind',[(L5,S5,P5,M5,R5,'compare'),(L6,S6,P6,M6,R6,'diagnose')])
def test_two_lesson_batch_authored_and_legal(lesson,scenes,practice,mastery,reassess,kind):
    assert (len(scenes),len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassess))==(15,15,15,5,3)
    assert not lesson.release_approved
    assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
    assert len({s['title'] for s in scenes})==15
    for scene,q in zip(scenes,lesson.whiteboard_questions,strict=True):
        assert scene['id']==q.id and scene['kind']==kind
        assert len(q.whiteboard.steps)==4 and scene['answer'] in q.whiteboard.steps[-1].after_expression
        assert all(s.narration==next(e.text for e in s.events if e.type=='caption') for s in q.whiteboard.steps)
        assert json.loads(q.whiteboard.visualization.parameters['scene_json'])==scene
        assert validate_visualization(q.whiteboard) is None
    assert len({p.prompt for p in practice})==15

def test_comparison_answers_are_derived_from_same_scale():
    fn={'gain_all':lambda v:v[3]-v[0],'loss_all':lambda v:v[0]-v[3],
        'point2':lambda v:v[2],'point3':lambda v:v[3],'lower_point3':lambda v:-v[3],
        'gain_mid':lambda v:v[2]-v[1],'gain_last':lambda v:v[3]-v[2]}
    for s in S5:
        a=[p['y'] for p in s['points']];b=[p['y'] for p in s['secondary_points']]
        va=fn[s['comparison_metric']](a);vb=fn[s['comparison_metric']](b)
        assert s['answer']==('A' if va>vb else 'B' if vb>va else 'equal')
    altered=deepcopy(L5.whiteboard_questions[0].whiteboard.visualization.parameters)
    scene=json.loads(altered['scene_json']);scene['answer']='B';altered['scene_json']=json.dumps(scene)
    with pytest.raises(ValueError,match='answer disagrees'):
        CATALOGUE[('coordinate_geometry','grade8_global_story')].validate(altered)
    altered=deepcopy(L5.whiteboard_questions[0].whiteboard.visualization.parameters)
    scene=json.loads(altered['scene_json']);scene['secondary_points'][0]['x']=99;altered['scene_json']=json.dumps(scene)
    with pytest.raises(ValueError,match='inputs must align'):
        CATALOGUE[('coordinate_geometry','grade8_global_story')].validate(altered)

def test_diagnosis_has_a_false_claim_and_a_concrete_repair():
    assert all(s['claim'] in s['problem'] and s['claim']!=s['answer'] and s['focus_index'] in (1,2,3) for s in S6)
    assert S6[8]['points'][3]['y']-S6[8]['points'][0]['y']==9
    assert S6[14]['points'][2]['y']-S6[14]['points'][3]['y']==11

def test_public_previews_keep_private_explanations_hidden():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/graphs')
        responses=[client.get(f'/api/v1/lessons/g8-graphs-0{n}') for n in (5,6)]
    assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==6
    if get_settings().unlock_all_lessons:
        for response in responses:
            assert response.status_code==200
            assert len(response.json()['whiteboard_questions'])==15
            for question in response.json()['whiteboard_questions']:
                assert 'answer' not in question and len(question['whiteboard']['steps'])==1
                preview=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                assert not {'answer','memo','actions','repair','misconception'}&preview.keys()
    else:
        assert all(response.status_code==401 for response in responses)
