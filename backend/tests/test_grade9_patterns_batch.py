"""The entire authored Grade 9 pattern topic stays internally consistent."""
import hashlib
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,PATTERN_LESSONS,PATTERN_TEMPLATES
from app.curriculum.grade9.assessment_whole_numbers import PATTERN_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer


def test_75_worked_and_115_independent_answers_use_exact_source_rule():
    for number,(_,data) in PATTERN_LESSONS.items():
        for case in data['worked']:
            v=case['visual'];a,b=v['a'],v['b']
            def term(n):
                return {'linear':lambda:a*n+b,'geometric':lambda:a*b**(n-1),
                    'square':lambda:a*n*n+b,'stair':lambda:a*n*(n+1)//2+b,
                    'border':lambda:a*(2*n+1)+b}[v['kind']]()
            assert v['known']==[term(i) for i in range(1,len(v['known'])+1)]
            assert v['target_value']==term(v['target'])
            assert case['answer']==(v['rule'] if v['family'] in {'rule','diagnosis'} else str(term(v['target'])))
        for item in [*data['practice'],*data['mastery'],*data['reassessment']]:
            assert len(item['options'])==len(set(item['options']))==4
            assert item['options'][item['answer_index']] not in [x for i,x in enumerate(item['options']) if i!=item['answer_index']]


def test_five_lessons_are_distinct_and_have_private_assessment_banks():
    topic=GRADE_9.topics[3]
    assert topic.id=='numeric-geometric-patterns' and topic.product_order==4
    assert [q.id for q in topic.subtopics[0].lessons]==[f'g9-patterns-{n:02}' for n in range(1,6)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    prompts=set()
    for number,(lesson,data) in PATTERN_LESSONS.items():
        practice,mastery,reassessment,repairs,rules=PATTERN_BANKS[number]
        assert (len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({q.whiteboard.problem for q in lesson.whiteboard_questions})==15
        assert len({q.prompt for q in [*practice,*mastery,*reassessment]})==23
        for q,case in zip(lesson.whiteboard_questions,data['worked']):
            scene=json.loads(q.whiteboard.visualization.parameters['scene_json'])
            assert q.whiteboard.visualization.template==PATTERN_TEMPLATES[number]
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
    base=Path(__file__).resolve().parents[2]/'docs/curriculum/grade9/numeric-geometric-patterns'
    manifest=json.loads((base/'topic4-acceptance-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==5
    for number,record in enumerate(manifest,1):
        assert record['lesson_id']==f'g9-patterns-{number:02}'
        assert hashlib.sha256((base/record['source']).read_bytes()).hexdigest()==record['source_sha256']
        assert [record[f'{bank}_count'] for bank in ('worked','practice','mastery','reassessment')]==[15,15,5,3]
        assert all(len(record[f'{bank}_ids'])==len(set(record[f'{bank}_ids']))==record[f'{bank}_count'] for bank in ('worked','practice','mastery','reassessment'))
        assert record['status']=='teacher_review_required' and not record['browser_accepted'] and not record['teacher_approved']


def test_public_api_gates_75_answers_and_reveals_the_registered_steps():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/numeric-geometric-patterns')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==5
        for number in range(1,6):
            lid=f'g9-patterns-{number:02}'
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
