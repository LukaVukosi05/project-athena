"""Function identities, graph restrictions, source integrity and answer gates."""
import copy
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade10.algebra import GRADE_10,FN_LESSONS
from app.curriculum.grade10.assessment import FN_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_fn_board

ROOT=Path(__file__).resolve().parents[2]

def test_seven_source_backed_lessons_and_private_banks():
    topic=GRADE_10.topics[5]
    assert (topic.id,topic.term,topic.paper)==('functions-and-graphs',2,'Paper 1')
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g10-fn-{n:02}' for n in range(1,8)]
    assert not [e for e in validate_curriculum([GRADE_10]) if e.grade_id=='grade-10']
    manifest=json.loads((ROOT/'docs/curriculum/grade10/functions-and-graphs/topic06-acceptance-manifest.json').read_text())
    for n,(lesson,data) in FN_LESSONS.items():
        practice,mastery,reassessment,_,_=FN_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
        assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
        source=ROOT/'docs/curriculum/grade10/functions-and-graphs'/data['source']
        assert sha256(source.read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
        for q in data['worked']:
            params={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
            _grade10_fn_board(params,n)
            tampered=copy.deepcopy(q);tampered['visual']['values']['a']+=1
            params['scene_json']=json.dumps(tampered)
            with pytest.raises(ValueError):_grade10_fn_board(params,n)

def test_derived_table_features_and_undefined_tangent():
    for n,(_,data) in FN_LESSONS.items():
        for q in data['worked']:
            v=q['visual']['values'];ans=q['answer'];family=v['family'];a=v['a'];shift=v['q']
            if n==1:
                x=v['target_x'];assert q['answer']==f'({x}; {a*x+shift})'
            if n==2 and family=='hyperbola':assert ans=='x = 0'
            if n==2 and family=='exponential':assert ans=='y = 0'
            if n==3:
                if family in ('linear','parabola'):assert ans==f'(0; {shift})'
                else:assert ans==f'y = {shift}'
            if n==4 and family=='tangent' and v['angle'] in (90,270):
                assert 'undefined' in ans
            if n==5:
                value=a+shift if family=='cosine' else shift
                assert ans==f'midline y = {shift}; y(0°) = {value}'
            if n==6:
                for x,y in v['given_points']:
                    expected=a*x+shift if family=='linear' else a*x*x+shift if family=='parabola' else Fraction(a,x)+shift if family=='hyperbola' else a*v['base']**x+shift
                    assert y==expected
            if n==7 and family in ('parabola','sine','exponential'):
                if v['mode']=='diagnosis':assert shift!=0
            if n==7 and v['mode']=='secant':
                (x1,y1),(x2,y2)=v['given']
                assert ans==f'average gradient = {Fraction(y2-y1,x2-x1)}'
            if n==7 and v['mode']=='discrete':
                assert 'only whole counts' in ans
            if n==7 and v['mode']=='continuous':
                assert 'any real value' in ans

def test_public_preview_keeps_given_features_but_hides_derived_answers():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-10/topics/functions-and-graphs')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==7
        for n in range(1,8):
            r=client.get(f'/api/v1/lessons/g10-fn-{n:02}')
            assert r.status_code==200,r.text
            payload=r.json();assert payload['paper']=='Paper 1' and len(payload['whiteboard_questions'])==15
            for q in payload['whiteboard_questions']:
                assert 'answer' not in q and len(q['whiteboard']['steps'])==1
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert 'answer' not in scene and 'actions' not in scene
                assert 'answer' not in scene['visual']['values']
                if n==1:assert len(scene['visual']['values']['given'])==2
                if n==6:assert 'a' not in scene['visual']['values'] and 'q' not in scene['visual']['values']
                if n==7:assert 'mode' not in scene['visual']['values']
            reveal=client.post(f'/api/v1/lessons/g10-fn-{n:02}/questions/g10-fn-l{n:02}-w01/reveal')
            assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==5
