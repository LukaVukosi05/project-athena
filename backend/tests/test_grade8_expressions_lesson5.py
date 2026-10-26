"""Grade 8 division lesson, privacy, source integrity and assessment checks."""
import hashlib
from pathlib import Path

from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.practice import _score_assessment
from app.curriculum.grade8.algebraic_expressions_lesson5 import DATA,LESSON,SOURCE
from app.curriculum.grade8.assessment_expressions_lesson5 import PRACTICE_BANK,MASTERY_BANK,REASSESSMENT_BANK
from app.curriculum.grade8.structure import GRADE_8
from app.curriculum.validation import validate_curriculum


def test_authored_source_math_states_and_template_contract():
    doc=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/algebraic-expressions'/SOURCE
    assert hashlib.sha256(doc.read_bytes()).hexdigest()==DATA['source_sha256']
    assert len(LESSON.whiteboard_questions)==len(PRACTICE_BANK)==15
    assert len(MASTERY_BANK)==5 and sum(q.marks for q in MASTERY_BANK)==20
    assert len(REASSESSMENT_BANK)==3
    assert not [failure for failure in validate_curriculum([GRADE_8]) if failure.lesson_id==LESSON.id]
    assert {q.whiteboard.visualization.template for q in LESSON.whiteboard_questions}=={
        'equal_share','signed_quotient','factor_cancel','term_share','three_term_share',
        'exponent_lanes','context_packs','error_division','two_quotients'}
    for item,q in zip(DATA['worked_examples'],LESSON.whiteboard_questions):
        board=q.whiteboard
        assert len(board.steps)==len(item['steps'])+1
        assert board.steps[-1].after_expression.startswith('Checked:')
        assert item['states'][-1] in q.full_memo[-2]
        assert q.full_memo[-1].endswith(item['verify'])
        assert board.visualization.parameters['model_tokens']==item['model']['tokens']
        for step in board.steps:
            assert step.events and step.before_expression!=step.after_expression
            assert step.narration==next(event.text for event in step.events if event.type=='caption')
        if item['number'] in {3,5,8,9,10,13,14,15}:
            assert '≠ 0' in item['q'] or item['number']==10 and 'restriction' in item['q']
            assert '≠ 0' in item['answer']


def test_lesson_reachable_without_early_answers_and_practice_private():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-8/topics/algebraic-expressions')
        assert topic.status_code==200
        assert any(item['id']==LESSON.id for part in topic.json()['subtopics'] for item in part['lessons'])
        page=client.get('/lesson.html')
        assert 'grade8-division-renderers.js?v=g8-ex-l05-v1' in page.text
        lesson=client.get('/api/v1/lessons/'+LESSON.id)
        assert lesson.status_code==200,lesson.text
        examples=lesson.json()['whiteboard_questions']
        assert len(examples)==15
        assert all(q['solution_gated'] and len(q['whiteboard']['steps'])==1 for q in examples)
        assert all('answer' not in q and 'full_memo' not in q and not q['whiteboard']['steps'][0]['events'] for q in examples)
        revealed=client.post(f'/api/v1/lessons/{LESSON.id}/questions/g8-ex-l05-w15/reveal')
        assert revealed.status_code==200 and len(revealed.json()['whiteboard']['steps'])==5
        practice=client.get('/api/v1/practice/'+LESSON.id)
        assert practice.status_code==200 and len(practice.json()['questions'])==15
        assert all('accepted_answers' not in q for q in practice.json()['questions'])
        mastery=client.get('/api/v1/practice/'+LESSON.id+'/mastery')
        assert mastery.status_code==200 and len(mastery.json()['questions'])==5
        assert all('answer' not in q for q in mastery.json()['questions'])


def test_all_authored_mastery_answers_score():
    correct,reviewed,tags=_score_assessment(MASTERY_BANK,{q.id:q.answer for q in MASTERY_BANK})
    assert correct==5 and all(item['correct'] for item in reviewed) and not tags
