"""Grade 9 equation source, arithmetic, public API and answer gates."""
import json
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,EQUATION_LESSONS
from app.curriculum.grade9.assessment_whole_numbers import EQUATION_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer

ROOT=Path(__file__).resolve().parents[2]

def test_six_lessons_have_mathematically_correct_independent_banks():
    assert len(GRADE_9.topics)==13
    topic=GRADE_9.topics[6]
    assert topic.id=='algebraic-equations' and topic.product_order==7
    assert [lesson.id for lesson in topic.subtopics[0].lessons]==[f'g9-equations-{n:02}' for n in range(1,7)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    manifest=json.loads((ROOT/'docs/curriculum/grade9/algebraic-equations/topic7-acceptance-manifest.json').read_text())
    assert len(manifest)==6
    for n,(lesson,data) in EQUATION_LESSONS.items():
        practice,mastery,reassess,repairs,rules=EQUATION_BANKS[n]
        assert (len(data['worked']),len(practice),len(mastery),len(reassess))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({item['problem'] for item in data['worked']})==15
        assert len({item['prompt'] for item in [*data['practice'],*data['mastery'],*data['reassessment']]})==23
        assert not {c['problem'] for c in data['worked']} & {c['prompt'] for c in data['practice']}
        source=(ROOT/'docs/curriculum/grade9/algebraic-equations'/data['source']).read_text()
        assert manifest[n-1]['source_sha256']==hashlib.sha256(source.encode()).hexdigest()
        assert not manifest[n-1]['teacher_approved'] and not manifest[n-1]['browser_accepted']
        for item in data['worked']:
            assert item['problem'] in source and item['answer'] in source
            v=item['visual']['values'];family=item['visual']['family']
            if family=='zero_product':
                a,b=v['first'],v['second']
                assert (a-a)*(a-b)==(b-a)*(b-b)==0
                assert v['middle']==-a-b and v['constant']==a*b
                assert item['answer']==f'x = {a} or x = {b}'
            elif family=='powers':assert v['solution']+v['left']==v['power'] and v['base']>1
            elif family=='brackets':assert v['multiplier']*(v['solution']+v['offset'])==v['other']*v['solution']+v['right']
            elif family=='table':
                for x,y in [('input_one','out_one'),('input_two','out_two'),('solution','target')]:
                    assert v['multiplier']*v[x]+v['offset']==v[y]
            else:assert v['multiplier']*v['solution']+v['offset']==v['total']
        for q in practice:
            assert len(set(q.options))==4
            assert check_answer(q.id,q.accepted_answers[0])
            assert all(not check_answer(q.id,other) for other in q.options if other!=q.accepted_answers[0])

def test_all_equation_previews_hide_answers_and_reveal_every_step():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/algebraic-equations')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==6
        for n in range(1,7):
            lesson_id=f'g9-equations-{n:02}'
            public=client.get(f'/api/v1/lessons/{lesson_id}')
            assert public.status_code==200
            for q in public.json()['whiteboard_questions']:
                assert q['solution_gated'] and len(q['whiteboard']['steps'])==1
                assert 'answer' not in q and 'full_memo' not in q
                scene=json.loads(q['whiteboard']['visualization']['parameters']['scene_json'])
                assert scene['visual']=={'family':'givens'}
                assert not {'answer','actions','check'} & scene.keys()
                full=client.post(f'/api/v1/lessons/{lesson_id}/questions/{q["id"]}/reveal')
                assert full.status_code==200 and len(full.json()['whiteboard']['steps'])==q['total_step_count']
            practice=client.get(f'/api/v1/practice/{lesson_id}')
            mastery=client.get(f'/api/v1/practice/{lesson_id}/mastery')
            assert practice.status_code==mastery.status_code==200
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            assert all('accepted_answers' not in item for item in practice.json()['questions'])
