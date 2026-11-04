"""The entire authored Grade 9 exponent topic stays internally consistent."""
import hashlib
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,EXPONENT_LESSONS,EXPONENT_TEMPLATES
from app.curriculum.grade9.assessment_whole_numbers import EXPONENT_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer


def test_exponent_answers_from_visual_inputs():
    """Independently recompute the arithmetic-bearing family from the visual inputs."""
    from decimal import Decimal
    from fractions import Fraction
    for number in range(1,7):
        cases=EXPONENT_LESSONS[number][1]['worked']
        for case in cases:
            v=case['visual'];kind=v.get('operator');value=None
            if v['family']=='factors':
                value=v['base']**v['exponents'][-1]
            elif v['family']=='law':
                if kind=='product_power':value=(v['values'][0]*v['values'][1])**v['exponents'][0]
                elif kind=='product':value=v['base']**(v['exponents'][0]+v['exponents'][1])
                elif kind=='quotient':value=v['base']**(v['exponents'][0]-v['exponents'][1])
                elif kind=='nested':value=v['base']**(v['exponents'][0]*v['exponents'][1])
                elif kind=='combined':value=v['base']**(v['exponents'][0]+v['exponents'][1]-v['exponents'][2])
            elif v['family']=='reciprocal':
                value=1 if kind=='zero' else Fraction(1,v['denominator'])
            elif v['family']=='compare':
                a=Decimal(v['a'][0])*Decimal(10)**v['a'][1]
                b=Decimal(v['b'][0])*Decimal(10)**v['b'][1]
                value='A is greater' if a>b else 'B is greater' if b>a else 'Equal'
            elif v['family']=='scale':
                assert Decimal(v['raw'])==Decimal(v['coefficient'])*Decimal(10)**v['exponent']
            elif v['family']=='context':
                total=Decimal(v['coefficient'])*Decimal(10)**v['exponent']*v['multiplier']
                assert total==Decimal(v['result_coefficient'])*Decimal(10)**v['result_exponent']
            if value is not None:assert case['answer']==str(value),case['id']


def test_six_lessons_are_distinct_and_have_private_assessment_banks():
    topic=GRADE_9.topics[2]
    assert topic.id=='exponents' and topic.product_order==3
    assert [q.id for q in topic.subtopics[0].lessons]==[f'g9-exponents-{n:02}' for n in range(1,7)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    prompts=set()
    for number,(lesson,data) in EXPONENT_LESSONS.items():
        practice,mastery,reassessment,repairs,rules=EXPONENT_BANKS[number]
        assert (len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({q.whiteboard.problem for q in lesson.whiteboard_questions})==15
        assert len({q.prompt for q in [*practice,*mastery,*reassessment]})==23
        for q,case in zip(lesson.whiteboard_questions,data['worked']):
            scene=json.loads(q.whiteboard.visualization.parameters['scene_json'])
            assert q.whiteboard.visualization.template==EXPONENT_TEMPLATES[number]
            assert scene['problem']==q.whiteboard.problem and scene['visual']==case['visual']
            assert q.whiteboard.steps[-1].after_expression.endswith(case['check'])
            assert len(q.whiteboard.steps)==len(scene['actions'])==4
            assert len(set(step.after_expression for step in q.whiteboard.steps))==4
        for q in practice:
            assert len(q.options)==len(set(q.options))==4
            assert check_answer(q.id,q.accepted_answers[0])
            assert all(not check_answer(q.id,x) for x in q.options if x!=q.accepted_answers[0])
        assert not prompts.intersection(q['problem'] for q in data['worked'])
        prompts.update(q['problem'] for q in data['worked'])


def test_manifest_matches_static_sources_and_all_question_ids():
    base=Path(__file__).resolve().parents[2]/'docs/curriculum/grade9/exponents'
    manifest=json.loads((base/'topic3-acceptance-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==6
    for number,record in enumerate(manifest,1):
        assert record['lesson_id']==f'g9-exponents-{number:02}'
        assert hashlib.sha256((base/record['source']).read_bytes()).hexdigest()==record['source_sha256']
        assert [record[f'{bank}_count'] for bank in ('worked','practice','mastery','reassessment')]==[15,15,5,3]
        assert all(len(record[f'{bank}_ids'])==len(set(record[f'{bank}_ids']))==record[f'{bank}_count'] for bank in ('worked','practice','mastery','reassessment'))
        assert record['status']=='teacher_review_required' and not record['browser_accepted'] and not record['teacher_approved']


def test_public_api_gates_90_answers_and_reveals_the_registered_steps():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/exponents')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==6
        for number in range(1,7):
            lid=f'g9-exponents-{number:02}'
            preview=client.get(f'/api/v1/lessons/{lid}')
            practice=client.get(f'/api/v1/practice/{lid}')
            mastery=client.get(f'/api/v1/practice/{lid}/mastery')
            assert preview.status_code==practice.status_code==mastery.status_code==200,(lid,preview.text[:200])
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            questions=preview.json()['whiteboard_questions']
            assert len(questions)==15
            for question in questions:
                board=question['whiteboard'];scene=json.loads(board['visualization']['parameters']['scene_json'])
                assert question['solution_gated'] and len(board['steps'])==1
                assert 'answer' not in question and 'full_memo' not in question
                assert not {'actions','check','answer','wrongs','wrong_methods','misconception'}&set(scene)
                assert scene['visual']=={'family':'givens'}
                result=client.post(f'/api/v1/lessons/{lid}/questions/{question["id"]}/reveal')
                assert result.status_code==200,(question['id'],result.text[:200])
                assert len(result.json()['whiteboard']['steps'])==question['total_step_count']==4
