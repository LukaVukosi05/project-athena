"""The entire authored Grade 9 integer topic stays internally consistent."""
import hashlib
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,INTEGER_LESSONS,INTEGER_TEMPLATES
from app.curriculum.grade9.assessment_whole_numbers import INTEGER_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer


def test_arithmetic_oracle_for_every_worked_and_independent_item():
    """Recalculate from source numbers, separate from the displayed answer and memo."""
    import importlib.util
    script=Path(__file__).resolve().parents[2]/'tools/build_grade9_integers.py'
    spec=importlib.util.spec_from_file_location('grade9_integer_authoring',script)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    for number in range(1,6):
        cases=[*module.WORKED[number]]
        seed=1
        while len(cases)<38:
            cases.extend(module.candidates(number,seed));seed+=1
        for case in cases:
            v=case['visual'];a=v['values'][0];b=v['values'][1] if len(v['values'])>1 else 0
            if number==1:
                if len(v['values'])==3:assert case['answer']==', '.join(map(str,sorted(v['values'])));continue
                expected={'+':lambda:a+b,'−':lambda:a-b,'×':lambda:a*b,'÷':lambda:a//b}[v['operator']]()
            elif number==2:
                c=v['values'][2]
                expected=a if v['operator']=='inverse' else a+b+c if v['operator']=='associative' else a*(b+c)
            elif number==3:
                expected={'square':lambda:a*a,'cube':lambda:a**3,'square_root':lambda:b,'cube_root':lambda:b}[v['operator']]()
                if v['operator']=='square_root':assert b>=0 and b*b==a
                if v['operator']=='cube_root':assert b**3==a
            elif number==4:
                c=v['values'][2]
                expected=(a+b)*c if v['operator']=='brackets' else a*b+c if v['operator']=='game' else a+b-c
            else:
                expected=a-b if v['operator']=='subtraction' else a*b if v['operator']=='product' else a*a if v['operator']=='square' else a+b*v['values'][2]
            assert v['path'][-1]==expected,case['problem']
            import re
            assert int(re.match(r'-?\d+',case['answer']).group())==expected,case['problem']


def test_five_lessons_are_distinct_and_have_private_assessment_banks():
    topic=GRADE_9.topics[1]
    assert topic.id=='integers' and topic.product_order==2
    assert [q.id for q in topic.subtopics[0].lessons]==[f'g9-integers-{n:02}' for n in range(1,6)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    prompts=set()
    for number,(lesson,data) in INTEGER_LESSONS.items():
        practice,mastery,reassessment,repairs,rules=INTEGER_BANKS[number]
        assert (len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({q.whiteboard.problem for q in lesson.whiteboard_questions})==15
        assert len({q.prompt for q in [*practice,*mastery,*reassessment]})==23
        for q,case in zip(lesson.whiteboard_questions,data['worked']):
            scene=json.loads(q.whiteboard.visualization.parameters['scene_json'])
            assert q.whiteboard.visualization.template==INTEGER_TEMPLATES[number]
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
    base=Path(__file__).resolve().parents[2]/'docs/curriculum/grade9/integers'
    manifest=json.loads((base/'topic2-acceptance-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==5
    for number,record in enumerate(manifest,1):
        assert record['lesson_id']==f'g9-integers-{number:02}'
        assert hashlib.sha256((base/record['source']).read_bytes()).hexdigest()==record['source_sha256']
        assert [record[f'{bank}_count'] for bank in ('worked','practice','mastery','reassessment')]==[15,15,5,3]
        assert all(len(record[f'{bank}_ids'])==len(set(record[f'{bank}_ids']))==record[f'{bank}_count'] for bank in ('worked','practice','mastery','reassessment'))
        assert record['status']=='teacher_review_required' and not record['browser_accepted'] and not record['teacher_approved']


def test_public_api_gates_75_answers_and_reveals_the_registered_steps():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/integers')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==5
        for number in range(1,6):
            lid=f'g9-integers-{number:02}'
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
