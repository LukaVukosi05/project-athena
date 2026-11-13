"""Grade 11 Probability source, exact-event arithmetic and public gating."""
import json
from fractions import Fraction
from hashlib import sha256
from pathlib import Path

from fastapi.testclient import TestClient

from app.curriculum.grade11 import GRADE_11
from app.curriculum.grade11.assessment_probability import BANKS
from app.curriculum.validation import validate_curriculum
from app.main import app
from app.practice.catalog import PRACTICE_BANKS

ROOT=Path(__file__).resolve().parents[2]

def exact(result):
    return Fraction(result.split(' = ')[-1])

def test_probability_seven_lessons_and_independent_arithmetic():
    assert validate_curriculum([GRADE_11])==[]
    topic=GRADE_11.topics[8]
    assert (topic.id,topic.paper,topic.term)==('probability','Paper 1',3)
    assert len(topic.subtopics[0].lessons)==7
    modes=set()
    for n,lesson in enumerate(topic.subtopics[0].lessons,1):
        assert lesson.status.value=='teacher_review_required' and not lesson.release_approved
        assert len(lesson.whiteboard_questions)==len(PRACTICE_BANKS[lesson.id])==15
        assert tuple(map(len,BANKS[n][:3]))==(15,5,3)
        source=ROOT/'docs/curriculum/grade11/probability'/lesson.source_document
        assert sha256(source.read_bytes()).hexdigest()==lesson.source_sha256
        bank=json.loads((ROOT/f'backend/app/curriculum/grade11/generated/probability_{n:02}.json').read_text())
        assert len({q['problem'] for q in bank['worked']})==15
        for q in bank['worked']:
            v=q['visual']['values'];mode=v['mode'];modes.add(mode)
            assert len(q['actions'])==5 and q['answer'] in q['check']
            if mode=='frequency':
                assert exact(q['answer'])==Fraction(v['red'],v['red']+v['blue'])
            elif mode=='venn2':
                total=v['aonly']+v['both']+v['bonly']+v['neither']
                target={'union':v['aonly']+v['both']+v['bonly'],
                        'complement':v['bonly']+v['neither'],'intersection':v['both']}[v['target']]
                assert exact(q['answer'])==Fraction(target,total)
            elif mode=='independence':
                assert v['both']<=min(v['a'],v['b'])
                assert q['answer']==('Independent' if Fraction(v['both'],v['total'])==Fraction(v['a']*v['b'],v['total']**2) else 'Dependent')
            elif mode=='venn3':
                total=sum(v[key] for key in ('aonly','bonly','conly','ab','ac','bc','abc','outside'))
                count={'exactly one':v['aonly']+v['bonly']+v['conly'],
                       'at least two':v['ab']+v['ac']+v['bc']+v['abc'],
                       'A or B or C':total-v['outside']}[v['target']]
                assert exact(q['answer'])==Fraction(count,total)
            elif mode=='tree':
                r,b=v['red'],v['blue'];N=r+b;after=N if v['replacement'] else N-1
                rr=Fraction(r,N)*Fraction(r if v['replacement'] else r-1,after)
                rb=Fraction(r,N)*Fraction(b,after);br=Fraction(b,N)*Fraction(r,after)
                expected={'two red':rr,'one of each':rb+br,'at least one red':rr+rb+br}[v['target']]
                assert exact(q['answer'])==expected
            else:
                assert mode=='table';ax,ay,bx,by=v['cells']
                expected={'A and X':Fraction(ax,ax+ay+bx+by),
                          'first row given second column':Fraction(ay,ay+by),
                          'first column given first row':Fraction(ax,ax+ay)}[v['target']]
                assert exact(q['answer'])==expected
        for section in ('practice','mastery','reassessment'):
            assert len(bank[section])=={'practice':15,'mastery':5,'reassessment':3}[section]
            for item in bank[section]:
                assert len(set(item['options']))==4
                assert item['options'][item['answer_index']] in item['memo']
    assert modes=={'frequency','venn2','independence','venn3','tree','table'}

def test_probability_public_preview_and_reveal(monkeypatch):
    monkeypatch.setattr('app.api.v1.lessons.enforce_lesson_access',lambda *a:None)
    with TestClient(app) as client:
        for n in range(1,8):
            response=client.get(f'/api/v1/lessons/g11-prob-{n:02}')
            assert response.status_code==200,response.text
            payload=response.json();assert payload['paper']=='Paper 1'
            for q in payload['whiteboard_questions']:
                assert q['solution_gated'] and q['total_step_count']==5
                assert len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert not any(key in scene for key in ('answer','actions','check'))
            qid=payload['whiteboard_questions'][0]['id']
            revealed=client.post(f'/api/v1/lessons/g11-prob-{n:02}/questions/{qid}/reveal')
            assert revealed.status_code==200,revealed.text
            assert len(revealed.json()['whiteboard']['steps'])==5
