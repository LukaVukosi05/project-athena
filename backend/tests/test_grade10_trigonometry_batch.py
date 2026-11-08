import copy
import json
import math
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade10.algebra import GRADE_10,TRIG_LESSONS
from app.curriculum.grade10.assessment import TRIG_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_trig_board

ROOT=Path(__file__).resolve().parents[2]

def test_seven_source_backed_lessons_and_assessments():
    topic=GRADE_10.topics[2]
    assert topic.id=='trigonometry' and topic.term==1 and topic.paper=='Paper 2'
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g10-trig-{n:02}' for n in range(1,8)]
    assert not [error for error in validate_curriculum([GRADE_10]) if error.grade_id=='grade-10']
    manifest=json.loads((ROOT/'docs/curriculum/grade10/trigonometry/topic03-acceptance-manifest.json').read_text())
    for n,(lesson,data) in TRIG_LESSONS.items():
        practice,mastery,reassessment,repairs,rules=TRIG_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert len({q['problem'] for q in data['worked']})>=10
        assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
        assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
        source=ROOT/'docs/curriculum/grade10/trigonometry'/data['source']
        assert sha256(source.read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
        for q in data['worked']:
            params={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
            _grade10_trig_board(params,n)
            altered=copy.deepcopy(q);altered['visual']['values']['opposite']+=1
            params['scene_json']=json.dumps(altered)
            with pytest.raises(ValueError):_grade10_trig_board(params,n)

def test_triangles_ratios_axes_and_signed_coordinate_values():
    for n in (1,3,5,7):
        for q in TRIG_LESSONS[n][1]['worked']:
            v=q['visual']['values'];x,y,h=v['opposite'],v['adjacent'],v['hypotenuse']
            assert x*x+y*y==h*h
            if n==1:
                fn=v['fn'];expected=Fraction(x,h) if fn=='sin' else Fraction(y,h) if fn=='cos' else Fraction(x,y)
                assert q['answer']==f'{fn} A = {expected}'
            if n==3:
                fn=v['fn'];expected=Fraction(h,x) if fn=='cosec' else Fraction(h,y) if fn=='sec' else Fraction(y,x)
                assert q['answer']==f'{fn} A = {expected}'
            if n==5:
                assert abs(v['angle']-math.degrees(math.atan2(x,y)))<.051
            if n==7:
                px,py=v['point'];rad=v['radius']
                assert px*px+py*py==rad*rad
                assert v['sin']==str(Fraction(py,rad))
                assert v['cos']==str(Fraction(px,rad))
                assert v['tan']==str(Fraction(py,px))
    axis=[q for q in TRIG_LESSONS[4][1]['worked'] if q['visual']['values']['degree']==90]
    assert any(q['answer']=='tan 90° = undefined' for q in axis)

def test_public_previews_hide_answers_and_reveal_only_requested_example():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-10/topics/trigonometry')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==7
        for n in range(1,8):
            r=client.get(f'/api/v1/lessons/g10-trig-{n:02}')
            assert r.status_code==200,r.text
            payload=r.json()
            assert payload['paper']=='Paper 2' and len(payload['whiteboard_questions'])==15
            for q in payload['whiteboard_questions']:
                assert 'answer' not in q and len(q['whiteboard']['steps'])==1
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert 'answer' not in scene and 'actions' not in scene
                assert 'answer' not in scene['visual']['values']
                if scene['visual']['values']['model']=='solve':
                    assert 'degree' not in scene['visual']['values']
            revealed=client.post(f'/api/v1/lessons/g10-trig-{n:02}/questions/g10-trig-l{n:02}-w01/reveal')
            assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
