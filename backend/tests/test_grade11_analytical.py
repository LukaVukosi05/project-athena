"""Coordinate calculations and learner-facing gates for Grade 11 Topic 5."""
import json
from fractions import Fraction
from hashlib import sha256
from math import isqrt
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_analytical import BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.catalog import PRACTICE_BANKS

DATA=Path(__file__).resolve().parents[1]/'app/curriculum/grade11/generated'
SOURCES=Path(__file__).resolve().parents[2]/'docs/curriculum/grade11/analytical-geometry'
def fr(x):return Fraction(x)

def test_six_lessons_have_source_banks_and_independent_coordinate_arithmetic():
    assert validate_curriculum([GRADE_11])==[]
    topic=GRADE_11.topics[4]
    assert (topic.id,topic.paper,topic.term)==('analytical-geometry','Paper 2',2)
    assert len(topic.subtopics[0].lessons)==6
    total=0
    for n,lesson in enumerate(topic.subtopics[0].lessons,1):
        assert lesson.status.value=='teacher_review_required' and not lesson.release_approved
        assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
        assert tuple(map(len,BANKS[n][:3]))==(15,5,3)
        assert sha256((SOURCES/lesson.source_document).read_bytes()).hexdigest()==lesson.source_sha256
        bank=json.loads((DATA/f'analytical_{n:02}.json').read_text())
        assert len({s['problem'] for s in bank['worked']})==15
        for item in bank['worked']:
            v=item['visual']['values'];answer=item['answer']
            assert len(item['actions'])==5 and answer in item['check']
            if n==6:
                assert (v['theta'],v['m']) in [(30,'√3/3'),(45,'1'),(60,'√3'),
                                                (120,'−√3'),(135,'−1'),(150,'−√3/3')]
                assert answer==f'θ = {v["theta"]}°'
                continue
            ax,ay=map(fr,v['a']);bx,by=map(fr,v['b']);dx,dy=bx-ax,by-ay
            if n==1:
                assert dx*dx+dy*dy==fr(v['length'])**2
                assert answer==f'{v["length"]} units'
            if n==2:assert fr(v['m'])==dy/dx
            if n==3:
                midpoint=((ax+bx)/2,(ay+by)/2)
                assert midpoint==tuple(map(fr,v['mid']))
                assert answer==(f'B({bx}, {by})' if v['missing'] else
                                f'M({midpoint[0]}, {midpoint[1]})')
            if n==4:
                m,c=fr(v['m']),fr(v['c'])
                assert m==dy/dx and ay==m*ax+c and by==m*bx+c
            if n==5:
                m,target,c=fr(v['base_m']),fr(v['target_m']),fr(v['c'])
                px,py=map(fr,v['p'])
                assert m==dy/dx and py==target*px+c
                assert target==m if v['relation']=='parallel' else target*m==-1
        for section in ('practice','mastery','reassessment'):
            for item in bank[section]:
                assert len(set(item['options']))==4
                assert item['options'][item['answer_index']] in item['memo']
                assert not any(' + -' in option for option in item['options'])
        total+=sum(len(bank[section]) for section in ('worked','practice','mastery','reassessment'))
    assert total==228


def test_public_preview_hides_computed_outputs_and_reveals_five_steps(monkeypatch):
    monkeypatch.setattr('app.api.v1.lessons.enforce_lesson_access',lambda *a:None)
    with TestClient(app) as client:
        for n in range(1,7):
            response=client.get(f'/api/v1/lessons/g11-ag-{n:02}')
            assert response.status_code==200,response.text
            payload=response.json()
            assert payload['paper']=='Paper 2'
            for q in payload['whiteboard_questions']:
                assert q['solution_gated'] and q['total_step_count']==5
                assert len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert not any(k in scene for k in ('actions','answer','check'))
                v=scene['visual']['values']
                assert not any(k in v for k in ('length','m','c','target_m','base_m','theta'))
                if n==3:assert ('b' not in v) if v['missing'] else ('mid' not in v)
            qid=payload['whiteboard_questions'][0]['id']
            reveal=client.post(f'/api/v1/lessons/g11-ag-{n:02}/questions/{qid}/reveal')
            assert reveal.status_code==200
            assert len(reveal.json()['whiteboard']['steps'])==5
