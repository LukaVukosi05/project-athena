import copy
import json
from hashlib import sha256
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade10.algebra import EEI_LESSONS, GRADE_10
from app.curriculum.grade10.assessment import EEI_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_eei_board

ROOT=Path(__file__).resolve().parents[2]

def test_nine_source_backed_lessons_with_distinct_scenarios_and_assessments():
    topic=GRADE_10.topics[1]
    assert topic.id=='exponents-equations-inequalities' and topic.paper=='Paper 1'
    assert [lesson.id for lesson in topic.subtopics[0].lessons]==[f'g10-eei-{n:02}' for n in range(1,10)]
    assert not [error for error in validate_curriculum([GRADE_10]) if error.grade_id=='grade-10']
    manifest=json.loads((ROOT/'docs/curriculum/grade10/exponents-equations-inequalities/topic02-acceptance-manifest.json').read_text())
    for n,(lesson,data) in EEI_LESSONS.items():
        practice,mastery,reassessment,repairs,rules=EEI_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert len({q['problem'] for q in data['worked']})>=10
        assert len({q.id for q in lesson.whiteboard_questions})==15
        assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
        assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
        assert all(q['answer'] in q['actions'][-1] for q in data['worked'])
        source=ROOT/'docs/curriculum/grade10/exponents-equations-inequalities'/data['source']
        assert sha256(source.read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
        for q in data['worked']:
            params={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
            _grade10_eei_board(params,n)
            altered=copy.deepcopy(q);altered['visual']['values']['a']+=1
            params['scene_json']=json.dumps(altered)
            import pytest
            with pytest.raises(ValueError):_grade10_eei_board(params,n)

def test_inequality_direction_roots_and_applied_models():
    inequalities=EEI_LESSONS[8][1]['worked']
    assert {'left','right'}=={q['visual']['values']['direction'] for q in inequalities}
    assert all('reverse' in q['actions'][1] for q in inequalities if q['visual']['values']['direction']=='left')
    assert all(']' in q['answer'] for q in inequalities if q['visual']['values']['closed'])
    assert all('(' in q['answer'] for q in inequalities if not q['visual']['values']['closed'])
    assert all(' or ' in q['answer'] for q in EEI_LESSONS[4][1]['worked'])
    assert {'purchase','rectangle','tickets'}=={q['visual']['values']['form'] for q in EEI_LESSONS[6][1]['worked']}

def test_derived_values_satisfy_the_original_equations():
    for q in EEI_LESSONS[3][1]['worked']:
        v=q['visual']['values']
        assert v['a']*(v['target']+v['b'])+v['c']==v['rhs']
    for q in EEI_LESSONS[4][1]['worked']:
        v=q['visual']['values']
        for root in (v['r'],v['t']):
            assert root*root+v['coefficient']*root+v['constant']==0
        assert v['r']!=v['t']
    for q in EEI_LESSONS[5][1]['worked']:
        v=q['visual']['values']
        assert v['x']+v['y']==v['u'] and v['x']-v['y']==v['v']
    for q in EEI_LESSONS[8][1]['worked']:
        v=q['visual']['values']
        at=v['offset']-v['k']*v['bound'] if v['direction']=='left' else v['k']*v['bound']+v['offset']
        assert at==v['rhs']
        assert (v['direction']=='left')==v['closed']

def test_public_preview_reveal_and_practice_answer_gate():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-10/topics/exponents-equations-inequalities')
        assert topic.status_code==200
        assert len(topic.json()['subtopics'][0]['lessons'])==9
        for n in range(1,10):
            lesson=client.get(f'/api/v1/lessons/g10-eei-{n:02}')
            assert lesson.status_code==200,lesson.text
            payload=lesson.json()
            assert len(payload['whiteboard_questions'])==15
            for question in payload['whiteboard_questions']:
                assert 'answer' not in question and len(question['whiteboard']['steps'])==1
                scene=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                assert 'answer' not in scene and 'actions' not in scene
                assert 'result' not in scene['visual']['values']
            revealed=client.post(f'/api/v1/lessons/g10-eei-{n:02}/questions/g10-eei-l{n:02}-w01/reveal')
            assert revealed.status_code==200
            assert len(revealed.json()['whiteboard']['steps'])==5
