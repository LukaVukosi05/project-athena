"""Integrated straight-line lessons must be real, distinct and visually validated."""
import json
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.straight_lines_chain_cases import LESSONS, make_case
from app.curriculum.grade8.straight_lines_chain_runtime import LESSON_3, LESSON_4, LESSON_5
from app.curriculum.grade8.assessment_straight_lines_chain import banks, expected
from app.visualization.registry import validate_visualization
from app.whiteboard.registry import registry
from app.practice.service import check_answer


def test_all_45_cases_have_distinct_diagrams_correct_two_step_math_and_gated_answer():
    lessons=(LESSON_3,LESSON_4,LESSON_5)
    assert all(len(x.whiteboard_questions)==15 for x in lessons)
    assert len({case.problem for cases in LESSONS.values() for case in cases})==45
    for lesson in lessons:
        for index,case in enumerate(LESSONS[lesson.order],1):
            board=lesson.whiteboard_questions[index-1].whiteboard
            validate_visualization(board)
            registry.validate(board)
            assert board.visualization.parameters['question_id']==case.id
            assert json.loads(board.visualization.parameters['scene_json'])==case.scene
            assert 'target_angle' not in case.scene and 'intermediate' not in case.scene
            assert len(board.steps)==len(case.working)+1
            assert not board.steps[0].state_after['verification_complete']
            assert board.steps[-1].state_after['verification_complete']
            assert case.intermediate != case.target_angle or case.family=='cointerior_vertical'
            assert make_case(lesson.order,index,1).problem!=case.problem
            if lesson.order==4: assert case.coefficient*case.answer+case.offset==case.target_angle


def test_three_independent_banks_per_lesson_and_public_gating():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/geometry-of-straight-lines').json()
        assert len(topic['subtopics'][0]['lessons'])==5
        for number in (3,4,5):
            practice,mastery,reassess,repairs,rules=banks(number)
            assert (len(practice),len(mastery),len(reassess))==(15,5,3)
            assert repairs and rules
            assert not {q.prompt for q in practice}&{case.problem for case in LESSONS[number]}
            assert check_answer(practice[0].id,expected(make_case(number,1,1)))
            lesson_id=f'g8-straight-lines-{number:02}'
            lesson=client.get(f'/api/v1/lessons/{lesson_id}')
            assert lesson.status_code==200,lesson.text
            public=lesson.json()['whiteboard_questions']
            assert len(public)==15 and all('answer' not in q and 'full_memo' not in q for q in public)
            assert all(len(q['whiteboard']['steps'])==1 for q in public)
            bank=client.get(f'/api/v1/practice/{lesson_id}')
            assert bank.status_code==200 and len(bank.json()['questions'])==15
            assert all('accepted_answers' not in q for q in bank.json()['questions'])
