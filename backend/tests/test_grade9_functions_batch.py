"""Grade 9 Functions and Relationships source banks, public gates and arithmetic."""
import hashlib
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,FUNCTION_LESSONS,FUNCTION_TEMPLATES
from app.curriculum.grade9.assessment_whole_numbers import FUNCTION_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer


def test_every_worked_scene_and_private_choice_follows_its_own_rule():
    for number,(lesson,data) in FUNCTION_LESSONS.items():
        for c in data['worked']:
            v=c['visual'];a,b=v['a'],v['b'];f=lambda x:x*x+b if v['kind']=='square' else a*x+b
            assert v['known_pairs']==[[x,f(x)] for x in ([-1,0,1,2] if number==4 else [0,1,2,3])]
            assert v['target_output']==f(v['target_input'])
            assert c['answer']==(v['rule'] if number>=4 else str(v['target_input']) if number==2 else str(f(v['target_input'])))
            if number==5:
                x=v['first_error_input'];claimed=(a*x+b+1 if x==0 else (a+1)*x+b)
                assert claimed!=f(x) and str(claimed) in c['actions'][0]
        for c in [*data['practice'],*data['mastery'],*data['reassessment']]:
            assert len(c['options'])==len(set(c['options']))==4
            assert c['options'][c['answer_index']] not in [opt for i,opt in enumerate(c['options']) if i!=c['answer_index']]


def test_five_distinct_lessons_have_separate_assessments_and_registered_timelines():
    topic=GRADE_9.topics[4]
    assert topic.id=='functions-relationships' and topic.product_order==5
    assert [q.id for q in topic.subtopics[0].lessons]==[f'g9-functions-{n:02}' for n in range(1,6)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    for number,(lesson,data) in FUNCTION_LESSONS.items():
        practice,mastery,reassessment,repairs,rules=FUNCTION_BANKS[number]
        assert (len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({x.whiteboard.problem for x in lesson.whiteboard_questions})==15
        assert len({x.prompt for x in [*practice,*mastery,*reassessment]})==23
        for question,c in zip(lesson.whiteboard_questions,data['worked']):
            scene=json.loads(question.whiteboard.visualization.parameters['scene_json'])
            assert scene['visual']==c['visual'] and question.whiteboard.visualization.template==FUNCTION_TEMPLATES[number]
            assert len(question.whiteboard.steps)==len(scene['actions'])==4
            assert len({step.after_expression for step in question.whiteboard.steps})==4
            assert question.whiteboard.steps[-1].after_expression.endswith(c['check'])
        for q in practice:
            assert check_answer(q.id,q.accepted_answers[0])
            assert all(not check_answer(q.id,x) for x in q.options if x!=q.accepted_answers[0])


def test_source_manifest_hashes_and_preview_status():
    base=Path(__file__).resolve().parents[2]/'docs/curriculum/grade9/functions-relationships'
    manifest=json.loads((base/'topic5-acceptance-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==5
    for n,record in enumerate(manifest,1):
        assert record['lesson_id']==f'g9-functions-{n:02}'
        assert hashlib.sha256((base/record['source']).read_bytes()).hexdigest()==record['source_sha256']
        assert [record[f'{bank}_count'] for bank in ('worked','practice','mastery','reassessment')]==[15,15,5,3]
        assert record['status']=='teacher_review_required' and not record['browser_accepted'] and not record['teacher_approved']


def test_api_lists_five_lessons_and_never_sends_answer_before_reveal():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/functions-relationships')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==5
        for n in range(1,6):
            lid=f'g9-functions-{n:02}'
            response=client.get(f'/api/v1/lessons/{lid}')
            practice=client.get(f'/api/v1/practice/{lid}')
            mastery=client.get(f'/api/v1/practice/{lid}/mastery')
            assert response.status_code==practice.status_code==mastery.status_code==200,(lid,response.text[:180])
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            for question in response.json()['whiteboard_questions']:
                scene=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                assert question['solution_gated'] and len(question['whiteboard']['steps'])==1
                assert 'answer' not in question and 'full_memo' not in question
                assert scene['visual']=={'family':'givens'}
                assert not {'actions','answer','check','wrong_methods','wrongs'}&set(scene)
                revealed=client.post(f'/api/v1/lessons/{lid}/questions/{question["id"]}/reveal')
                assert revealed.status_code==200,(question['id'],revealed.text[:180])
                assert len(revealed.json()['whiteboard']['steps'])==question['total_step_count']==4
