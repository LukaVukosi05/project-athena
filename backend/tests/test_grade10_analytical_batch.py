"""Coordinate identities, answer gates and stage contracts."""
import copy
import json
import math
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade10.algebra import GRADE_10, AG_LESSONS
from app.curriculum.grade10.assessment import AG_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_ag_board

ROOT=Path(__file__).resolve().parents[2]

def test_six_coordinate_lessons_and_private_banks():
    topic=GRADE_10.topics[4]
    assert (topic.id,topic.term,topic.paper)==('analytical-geometry',2,'Paper 2')
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g10-ag-{n:02}' for n in range(1,7)]
    assert not [e for e in validate_curriculum([GRADE_10]) if e.grade_id=='grade-10']
    manifest=json.loads((ROOT/'docs/curriculum/grade10/analytical-geometry/topic05-acceptance-manifest.json').read_text())
    for n,(lesson,data) in AG_LESSONS.items():
        practice,mastery,reassessment,_,_=AG_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert len({q['problem'] for q in data['worked']})==15
        assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
        assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
        source=ROOT/'docs/curriculum/grade10/analytical-geometry'/data['source']
        assert sha256(source.read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
        for q in data['worked']:
            params={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
            _grade10_ag_board(params,n)
            tampered=copy.deepcopy(q);tampered['visual']['values']['points'][0][0]+=1
            params['scene_json']=json.dumps(tampered)
            with pytest.raises(ValueError):_grade10_ag_board(params,n)

def test_distance_midpoint_gradient_and_shape_conclusions():
    for n,(_,data) in AG_LESSONS.items():
        for q in data['worked']:
            v=q['visual']['values'];pts=v['points'];ans=q['answer']
            if n==1:
                A,B=pts
                assert math.isqrt((B[0]-A[0])**2+(B[1]-A[1])**2)**2==(B[0]-A[0])**2+(B[1]-A[1])**2
                assert ans==f'AB = {math.isqrt((B[0]-A[0])**2+(B[1]-A[1])**2)} units'
            if n==2:
                if v['mode']=='reverse_midpoint':A,M=pts;B=v['solution_point']
                else:A,B=pts;M=v['solution_point']
                assert [A[j]+B[j] for j in (0,1)]==[2*M[j] for j in (0,1)]
            if n==3:
                A,B=pts;assert ans==f'm = {Fraction(B[1]-A[1],B[0]-A[0])}'
            if n==4:
                A,B,C,D=pts;m1=Fraction(B[1]-A[1],B[0]-A[0]);m2=Fraction(D[1]-C[1],D[0]-C[0])
                assert m1==m2 if v['mode']=='parallel' else m1*m2==-1
            if n==5:
                A,B,C,D=pts;AB=[B[j]-A[j] for j in (0,1)];BC=[C[j]-B[j] for j in (0,1)]
                CD=[D[j]-C[j] for j in (0,1)];DA=[A[j]-D[j] for j in (0,1)]
                para=AB==[-z for z in CD] and BC==[-z for z in DA]
                equal=sum(z*z for z in AB)==sum(z*z for z in BC)
                right=sum(AB[j]*BC[j] for j in (0,1))==0
                assert para==(v['mode']!='trapezium')
                if v['mode']=='square':assert equal and right
                elif v['mode']=='rhombus':assert equal and not right
                elif v['mode']=='rectangle':assert right and not equal
                elif v['mode']=='parallelogram':assert not equal and not right
                assert v['mode'] in ans

def test_public_coordinate_previews_and_reveal():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-10/topics/analytical-geometry')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==6
        for n in range(1,7):
            response=client.get(f'/api/v1/lessons/g10-ag-{n:02}')
            assert response.status_code==200,response.text
            payload=response.json();assert payload['paper']=='Paper 2' and len(payload['whiteboard_questions'])==15
            for q in payload['whiteboard_questions']:
                assert 'answer' not in q and len(q['whiteboard']['steps'])==1
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert 'answer' not in scene and 'actions' not in scene
                assert 'answer' not in scene['visual']['values'] and 'solution_point' not in scene['visual']['values']
                if scene['visual']['values']['model'] in {'two_segments','quadrilateral'}:
                    assert 'mode' not in scene['visual']['values']
            revealed=client.post(f'/api/v1/lessons/g10-ag-{n:02}/questions/g10-ag-l{n:02}-w01/reveal')
            assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
