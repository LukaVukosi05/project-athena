"""Independent geometry identities and public/private payload contract."""
import copy
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade10.algebra import GRADE_10, EUC_LESSONS
from app.curriculum.grade10.assessment import EUC_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_euc_board

ROOT=Path(__file__).resolve().parents[2]

def test_six_geometry_lessons_and_authored_assessments():
    topic=GRADE_10.topics[3]
    assert topic.id=='euclidean-geometry' and topic.term==2 and topic.paper=='Paper 2'
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g10-euc-{n:02}' for n in range(1,7)]
    assert not [e for e in validate_curriculum([GRADE_10]) if e.grade_id=='grade-10']
    manifest=json.loads((ROOT/'docs/curriculum/grade10/euclidean-geometry/topic04-acceptance-manifest.json').read_text())
    for n,(lesson,data) in EUC_LESSONS.items():
        practice,mastery,reassessment,_,_=EUC_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
        assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
        source=ROOT/'docs/curriculum/grade10/euclidean-geometry'/data['source']
        assert sha256(source.read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
        for q in data['worked']:
            params={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
            _grade10_euc_board(params,n)
            tampered=copy.deepcopy(q);tampered['visual']['values']['a']+=1
            params['scene_json']=json.dumps(tampered)
            with pytest.raises(ValueError):_grade10_euc_board(params,n)

def test_geometric_answers_agree_with_marked_givens():
    for n,(_,data) in EUC_LESSONS.items():
        for q in data['worked']:
            v=q['visual']['values'];answer=q['answer']
            if n==1:
                expected=v['given_angle'] if v['target'] in ('vertically opposite','alternate interior') else 180-v['given_angle']
                assert v['result']==expected and answer==f'x = {expected}°'
            if v['model']=='paired_triangles':
                if v['mode']=='sss':assert sorted((v['side_ab'],v['side_ac'],v['side_bc']))==sorted((v['side_de'],v['side_df'],v['side_ef']))
                if v['mode']=='similar_sas':assert Fraction(v['side_de'],v['side_ab'])==Fraction(v['side_df'],v['side_ac'])==v['scale']
            if v['model']=='midpoint' and v['mode']=='reverse':assert v['solution_bc']==2*v['de']
            if v['model']=='midpoint' and v['mode']=='half':assert 2*v['solution_de']==v['bc']
            if v.get('shape') in ('kite','rhombus') and 'area =' in answer:
                expected=Fraction(v['diagonal_ac']*v['diagonal_bd'],2)
                assert str(int(expected)) in answer

def test_public_preview_does_not_expose_solution_and_reveal_has_all_steps():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-10/topics/euclidean-geometry')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==6
        for n in range(1,7):
            response=client.get(f'/api/v1/lessons/g10-euc-{n:02}')
            assert response.status_code==200,response.text
            lesson=response.json()
            assert lesson['paper']=='Paper 2' and len(lesson['whiteboard_questions'])==15
            for q in lesson['whiteboard_questions']:
                assert 'answer' not in q and len(q['whiteboard']['steps'])==1
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert 'answer' not in scene and 'actions' not in scene
                assert 'answer' not in scene['visual']['values']
                assert all(key not in scene['visual']['values'] for key in ('a','b','c','solution_bc','solution_de'))
                if scene['visual']['values'].get('mode')=='reverse':
                    assert 'solution_bc' not in scene['visual']['values']
            revealed=client.post(f'/api/v1/lessons/g10-euc-{n:02}/questions/g10-euc-l{n:02}-w01/reveal')
            assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
