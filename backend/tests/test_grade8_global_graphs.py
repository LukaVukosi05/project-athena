import json
from copy import deepcopy
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.core.config import get_settings
from app.curriculum.grade8.graphs_lesson3 import LESSON as READING, SCENE_DATA as READ_SCENES
from app.curriculum.grade8.graphs_lesson4 import LESSON as DRAWING, SCENE_DATA as DRAW_SCENES
from app.curriculum.grade8.assessment_graphs_lesson3 import PRACTICE_BANK as P3, MASTERY_BANK as M3, REASSESSMENT_BANK as R3
from app.curriculum.grade8.assessment_graphs_lesson4 import PRACTICE_BANK as P4, MASTERY_BANK as M4, REASSESSMENT_BANK as R4
from app.curriculum.validation import validate_curriculum
from app.curriculum.grade8.structure import GRADE_8
from app.visualization.registry import validate_visualization

@pytest.mark.parametrize('lesson,scenes,practice,mastery,reassess,kind',[(READING,READ_SCENES,P3,M3,R3,'read'),(DRAWING,DRAW_SCENES,P4,M4,R4,'draw')])
def test_authored_graph_lessons(lesson,scenes,practice,mastery,reassess,kind):
    assert (len(scenes),len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassess)) == (15,15,15,5,3)
    assert not lesson.release_approved
    assert not [e for e in validate_curriculum([GRADE_8]) if e.lesson_id==lesson.id]
    for scene,q in zip(scenes,lesson.whiteboard_questions,strict=True):
        assert scene['kind']==kind and scene['id']==q.id
        assert len(q.whiteboard.steps)==4
        assert len({(p['x'],p['y']) for p in scene['points']})==4
        assert len(scene['actions'])==4 and scene['answer'] in q.whiteboard.steps[-1].after_expression
        assert all(step.narration==next(e.text for e in step.events if e.type=='caption') for step in q.whiteboard.steps)
        assert json.loads(q.whiteboard.visualization.parameters['scene_json'])==scene
        assert validate_visualization(q.whiteboard) is None
    assert len({s['title'] for s in scenes}) == 15

def test_domain_and_bounds_are_checked():
    q=DRAWING.whiteboard_questions[11].whiteboard
    parameters=deepcopy(q.visualization.parameters)
    scene=json.loads(parameters['scene_json'])
    scene['points'][0]['y']=5000
    parameters['scene_json']=json.dumps(scene)
    from app.visualization.registry import CATALOGUE
    with pytest.raises(ValueError,match='outside'):
        CATALOGUE[('coordinate_geometry','grade8_global_story')].validate(parameters)
    assert DRAW_SCENES[11]['domain']=='discrete' and READ_SCENES[11]['domain']=='discrete'

def test_public_lessons_and_source_gating():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/graphs')
        responses=[client.get(f'/api/v1/lessons/g8-graphs-0{n}') for n in (3,4)]
    assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==6
    if get_settings().unlock_all_lessons:
        assert all(response.status_code==200 for response in responses)
        for response in responses:
            assert len(response.json()['whiteboard_questions'])==15
            assert all('answer' not in q and len(q['whiteboard']['steps'])==1 for q in response.json()['whiteboard_questions'])
            for question in response.json()['whiteboard_questions']:
                preview=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                assert not {'answer','memo','actions','repair','misconception'} & preview.keys()
    else:
        assert all(response.status_code==401 for response in responses)
