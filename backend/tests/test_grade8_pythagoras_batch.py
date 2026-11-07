"""Exact arithmetic, private assessment, withheld answers and visual contracts."""
import json
from math import isqrt
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.pythagoras_cases import LESSONS,root,variant
from app.curriculum.grade8.pythagoras_runtime import LESSONS_RUNTIME
from app.curriculum.grade8.assessment_pythagoras import banks
from app.visualization.registry import validate_visualization
from app.whiteboard.registry import registry


def _squared_root_string(n):
    observed=root(n)
    if '√' not in observed:return int(observed)**2
    coefficient,radicand=observed.split('√')
    return int(coefficient or 1)**2*int(radicand)


def test_exact_squares_and_converse_are_mathematically_correct():
    for cases in LESSONS.values():
        for case in cases:
            if case.lesson in (2,5):
                assert _squared_root_string(case.a**2+case.b**2)==case.a**2+case.b**2
                assert root(case.a**2+case.b**2) in case.answer
            if case.lesson==3:
                n=case.c**2-case.b**2
                assert n>0 and _squared_root_string(n)==n
                assert root(n) in case.answer
            if case.lesson==4:
                x,y,z=sorted((case.a,case.b,case.c))
                assert x+y>z
                assert (case.answer=='right-angled')==(x*x+y*y==z*z)
            changed=variant(case,1)
            assert changed.problem!=case.problem
            if case.lesson==4:
                x,y,z=sorted((changed.a,changed.b,changed.c))
                assert x+y>z
                assert (changed.answer=='right-angled')==(x*x+y*y==z*z)


def test_five_complete_authored_lessons_and_valid_progressive_visuals():
    assert len({case.problem for cases in LESSONS.values() for case in cases})==75
    for number,cases in LESSONS.items():
        lesson=LESSONS_RUNTIME[number]
        source=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/pythagoras'/f'lesson-{number:02}.md'
        assert source.exists() and source.stat().st_size>10000
        assert len(lesson.whiteboard_questions)==15 and not lesson.release_approved
        practice,mastery,reassessment,repairs,rules=banks(number)
        assert (len(practice),len(mastery),len(reassessment))==(15,5,3)
        assert repairs and rules
        assert len({q.problem for q in (case for case in cases)})==15
        for case,q in zip(cases,lesson.whiteboard_questions):
            board=q.whiteboard
            validate_visualization(board);registry.validate(board)
            assert case.answer==q.answer
            assert len(board.steps)==len(case.working)+1>=6
            assert q.full_memo[:-1]==list(case.working)
            assert q.full_memo[-1]==f'Check: {case.check}'
            assert board.steps[-1].state_after['verification_complete']
            assert case.answer in board.steps[-1].after_expression
            assert case.answer not in board.initial_expression if case.lesson!=4 else board.initial_expression==case.problem
            scene=json.loads(board.visualization.parameters['scene_json'])
            assert 'answer' not in scene and 'memo' not in scene
            assert [step.step_number for step in board.steps]==list(range(len(board.steps)))
            assert all(step.events[0].text==step.narration for step in board.steps)
            assert practice[q.order-1].prompt!=case.problem
            assert practice[q.order-1].answer_hidden_before_submission
            altered=dict(board.visualization.parameters)
            altered['scene_json']=json.dumps({**scene,'a':scene['a']+1})
            board.visualization.parameters=altered
            try:
                validate_visualization(board)
            except ValueError:
                pass
            else:
                raise AssertionError(f'{case.id}: mismatched side passed validation')
            finally:
                altered['scene_json']=json.dumps(scene)
                board.visualization.parameters=altered


def test_api_lists_five_and_gates_answers_until_reveal():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/theorem-of-pythagoras')
        assert topic.status_code==200
        assert [row['id'] for row in topic.json()['subtopics'][0]['lessons']]==[f'g8-pythagoras-{n:02}' for n in range(1,6)]
        for n in range(1,6):
            lid=f'g8-pythagoras-{n:02}'
            bank=client.get(f'/api/v1/practice/{lid}')
            assert bank.status_code==200 and len(bank.json()['questions'])==15
            lesson=client.get(f'/api/v1/lessons/{lid}')
            assert lesson.status_code==200
            questions=lesson.json()['whiteboard_questions']
            assert len(questions)==15
            assert all('answer' not in q and 'full_memo' not in q for q in questions)
            assert all(len(q['whiteboard']['steps'])==1 for q in questions)
            revealed=client.post(f'/api/v1/lessons/{lid}/questions/{questions[0]["id"]}/reveal')
            assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])>=6
