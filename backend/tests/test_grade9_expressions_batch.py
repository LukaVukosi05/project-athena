"""Grade 9 Topic 6: independently check the authored symbolic maths and API."""
import hashlib
import json
import re
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9,EXPRESSION_LESSONS,EXPRESSION_TEMPLATES
from app.curriculum.grade9.assessment_whole_numbers import EXPRESSION_BANKS
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer


def symbolic(text):
    text=text.replace('−','-').replace('×','*').replace('²','**2').replace('³','**3')
    return parse_expr(text,local_dict={'x':sp.Symbol('x')},
        transformations=standard_transformations+(implicit_multiplication_application,))


def test_exact_symbolic_equivalence_and_denominator_restrictions():
    x=sp.Symbol('x')
    for number,(lesson,data) in EXPRESSION_LESSONS.items():
        for scene in data['worked']:
            prompt,answer=scene['problem'],scene['answer']
            if number==1:
                assert answer in scene['actions'][2]
                continue
            if number==2:
                original=prompt.removeprefix('Simplify ').split(', keeping exact fractions')[0]
            elif number in (3,4):
                original=prompt.removeprefix('Expand ').split(' and collect')[0].split(' using all')[0]
            elif number==5:
                if prompt.startswith('Evaluate '):
                    expr,value=prompt.removeprefix('Evaluate ').split(' when x = ')
                    assert symbolic(expr).subs(x,int(value.rstrip('.')))==int(answer)
                    continue
                original=prompt.removeprefix('Simplify ').split(' for x ≠ 0')[0].rstrip('.').replace(' ÷ ','/')
            elif number in (6,7,8):
                if number==6:original=prompt.removeprefix('Factorise ').split(' completely')[0]
                elif number==7:original=prompt.removeprefix('Factorise ').split(' completely')[0]
                elif prompt.startswith('Factorise '):original=prompt.removeprefix('Factorise ').rstrip('.')
                else:original=prompt.removeprefix('Simplify ').split(', stating any restriction')[0]
            else:
                original=prompt.removeprefix('A learner writes ').split(' = ')[0]
            reduced=answer.split(';')[0]
            assert sp.simplify(symbolic(original)-symbolic(reduced))==0,(number,prompt,answer)
            if number==6:
                polynomial=symbolic(original)
                assert sp.simplify(symbolic(answer)-polynomial)==0
            if number==7:
                # No integer factor remains common to both final conjugates.
                factors=sp.factor_list(symbolic(original))[1]
                assert sp.simplify(symbolic(answer)-symbolic(original))==0 and factors
            if number==8 and ';' in answer:
                denominator=prompt.split(')/(')[1].split('), stating')[0]
                excluded=int(answer.split('≠ ')[1]);assert symbolic(denominator).subs(x,excluded)==0


def test_nine_lessons_banks_and_source_hashes():
    topic=GRADE_9.topics[5]
    assert topic.id=='algebraic-expressions' and topic.product_order==6
    assert [lesson.id for lesson in topic.subtopics[0].lessons]==[f'g9-expressions-{n:02}' for n in range(1,10)]
    assert not [e for e in validate_curriculum([GRADE_9]) if e.grade_id=='grade-9']
    base=Path(__file__).resolve().parents[2]/'docs/curriculum/grade9/algebraic-expressions'
    manifest=json.loads((base/'topic6-acceptance-manifest.json').read_text(encoding='utf-8'))
    assert len(manifest)==9
    assert any(' ÷ 3.' in scene['problem'] or ' ÷ 2.' in scene['problem'] or ' ÷ 4.' in scene['problem']
               for scene in EXPRESSION_LESSONS[5][1]['worked'])
    assert any(scene['answer'].startswith(('2×','3×','4×'))
               for scene in EXPRESSION_LESSONS[8][1]['worked'])
    for number,record in enumerate(manifest,1):
        lesson,data=EXPRESSION_LESSONS[number]
        practice,mastery,reassessment,repairs,rules=EXPRESSION_BANKS[number]
        assert hashlib.sha256((base/record['source']).read_bytes()).hexdigest()==record['source_sha256']
        assert record['status']=='teacher_review_required' and not record['teacher_approved'] and not record['browser_accepted']
        assert (len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassessment))==(15,15,5,3)
        assert repairs and rules and not lesson.release_approved
        assert len({c['problem'] for c in data['worked']})==15
        assert len({c['prompt'] for c in [*data['practice'],*data['mastery'],*data['reassessment']]})==23
        for question,scene in zip(lesson.whiteboard_questions,data['worked']):
            assert question.whiteboard.visualization.template==EXPRESSION_TEMPLATES[number]
            assert len(question.whiteboard.steps)==4
            assert question.whiteboard.steps[-1].after_expression.endswith(scene['check'])
        for item in practice:
            assert len(set(item.options))==4 and check_answer(item.id,item.accepted_answers[0])
            assert all(not check_answer(item.id,option) for option in item.options if option!=item.accepted_answers[0])


def test_api_gates_all_135_solutions_and_exposes_full_reveals():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/algebraic-expressions')
        assert topic.status_code==200 and len(topic.json()['subtopics'][0]['lessons'])==9
        for n in range(1,10):
            lesson_id=f'g9-expressions-{n:02}'
            response=client.get(f'/api/v1/lessons/{lesson_id}')
            practice=client.get(f'/api/v1/practice/{lesson_id}')
            mastery=client.get(f'/api/v1/practice/{lesson_id}/mastery')
            assert response.status_code==practice.status_code==mastery.status_code==200
            assert len(practice.json()['questions'])==15 and len(mastery.json()['questions'])==5
            for question in response.json()['whiteboard_questions']:
                assert question['solution_gated'] and len(question['whiteboard']['steps'])==1
                assert 'answer' not in question and 'full_memo' not in question
                scene=json.loads(question['whiteboard']['visualization']['parameters']['scene_json'])
                assert scene['visual']=={'family':'givens'}
                assert not {'actions','answer','check','wrongs'}&set(scene)
                result=client.post(f'/api/v1/lessons/{lesson_id}/questions/{question["id"]}/reveal')
                assert result.status_code==200,(question['id'],result.text[:200])
                assert len(result.json()['whiteboard']['steps'])==question['total_step_count']==4
