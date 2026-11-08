"""Grade 10 probability source, sample-space arithmetic and answer gates."""
import copy
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade10.algebra import GRADE_10,PROB_LESSONS
from app.curriculum.grade10.assessment import PROB_BANKS
from app.curriculum.validation import validate_curriculum
from app.visualization.registry import _grade10_prob_board

ROOT=Path(__file__).resolve().parents[2]

def test_complete_source_backed_lesson_bank():
    topic=GRADE_10.topics[7]
    assert (topic.id,topic.term,topic.paper)==('probability',3,'Paper 1')
    assert [l.id for l in topic.subtopics[0].lessons]==[f'g10-prob-{n:02}' for n in range(1,6)]
    assert not [e for e in validate_curriculum([GRADE_10]) if e.grade_id=='grade-10']
    manifest=json.loads((ROOT/'docs/curriculum/grade10/probability/topic08-acceptance-manifest.json').read_text())
    for n,(lesson,data) in PROB_LESSONS.items():
        practice,mastery,reassessment,_,_=PROB_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert len({q['problem'] for q in data['worked']})>=10
        assert all(len(q.whiteboard.steps)==5 for q in lesson.whiteboard_questions)
        assert all(q.type=='multiple_choice' and len(set(q.options))==4 for q in practice)
        source=ROOT/'docs/curriculum/grade10/probability'/data['source']
        assert sha256(source.read_bytes()).hexdigest()==manifest[n-1]['source_sha256']
        for q in data['worked']:
            params={'scene_json':json.dumps(q),'question_id':q['id'],'prompt':q['problem'],'total_steps':5}
            _grade10_prob_board(params,n)
            tampered=copy.deepcopy(q);tampered['visual']['values']['hits' if n==1 else 'both']+=1
            params['scene_json']=json.dumps(tampered)
            with pytest.raises(ValueError):_grade10_prob_board(params,n)

def test_venn_counts_union_complement_and_relative_frequency():
    for n,(_,bank) in PROB_LESSONS.items():
        for q in bank['worked']:
            v=q['visual']['values']
            if n==1:
                assert f'relative frequency {Fraction(v["hits"],v["trials"])}' in q['answer']
                assert f'theoretical probability {Fraction(v["favourable"],v["faces"])}' in q['answer']
            else:
                assert v['a_only']+v['both']+v['b_only']+v['neither']==v['total']
                assert v['a']==v['a_only']+v['both'] and v['b']==v['b_only']+v['both']
                assert v['union']==v['a']+v['b']-v['both']
                if n==4:
                    assert v['both']==0
                    assert ('disjoint and exhaustive' in q['answer'])==(v['neither']==0)
                if n==5:
                    assert v['both']>0
                    assert q['answer'].endswith(str(Fraction(v['union'],v['total'])))

def test_public_preview_hides_derived_venn_regions():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-10/topics/probability')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==5
        for n in range(1,6):
            r=client.get(f'/api/v1/lessons/g10-prob-{n:02}')
            assert r.status_code==200,r.text
            for q in r.json()['whiteboard_questions']:
                assert 'answer' not in q and len(q['whiteboard']['steps'])==1
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert 'answer' not in scene and 'actions' not in scene
                assert 'answer' not in scene['visual']['values']
                if n in (2,5):assert not {'a_only','b_only','neither','union'} & scene['visual']['values'].keys()
            reveal=client.post(f'/api/v1/lessons/g10-prob-{n:02}/questions/g10-prob-l{n:02}-w01/reveal')
            assert reveal.status_code==200 and len(reveal.json()['whiteboard']['steps'])==5
