"""New topic release checks: source integrity, question gates and native visuals."""
import hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.curriculum.grade8.algebraic_expressions import DATA, LESSON, SOURCE
from app.curriculum.grade8.assessment_expressions import PRACTICE_BANK, MASTERY_BANK, REASSESSMENT_BANK
from app.curriculum.validation import validate_curriculum
from app.curriculum.grade8.structure import GRADE_8
from app.api.v1.practice import _score_assessment


def test_source_and_author_banks_are_complete():
    source=Path(__file__).resolve().parents[2]/'docs/curriculum/grade8/algebraic-expressions'/SOURCE
    assert hashlib.sha256(source.read_bytes()).hexdigest()==DATA['source_sha256']
    assert len(LESSON.whiteboard_questions)==len(PRACTICE_BANK)==15
    assert len(MASTERY_BANK)==5 and len(REASSESSMENT_BANK)==3
    assert sum(q.marks for q in MASTERY_BANK)==20
    assert not [x for x in validate_curriculum([GRADE_8]) if x.lesson_id==LESSON.id]
    for q in LESSON.whiteboard_questions:
        board=q.whiteboard
        assert board.steps[-1].state_after['verification_link']==q.expected_evidence
        assert board.steps[0].before_expression==board.initial_expression
        assert all(s.events and s.narration==next(e.text for e in s.events if e.type=='caption') for s in board.steps)
        assert board.visualization.parameters['model_tokens']


def test_learner_sees_question_first_and_reveals_one_example_only():
    with TestClient(app) as client:
        response=client.get('/api/v1/lessons/g8-algebraic-expressions-01')
        assert response.status_code==200
        payload=response.json()
        assert payload['topic_id']=='algebraic-expressions'
        assert len(payload['whiteboard_questions'])==15
        for item in payload['whiteboard_questions']:
            assert item['solution_gated'] and len(item['whiteboard']['steps'])==1
            assert 'answer' not in item and 'full_memo' not in item
            assert item['whiteboard']['steps'][0]['events']==[]
        result=client.post('/api/v1/lessons/g8-algebraic-expressions-01/questions/g8-ex-l01-w01/reveal')
        assert result.status_code==200
        assert len(result.json()['whiteboard']['steps'])==4
        assert result.json()['whiteboard']['steps'][-1]['after_expression'].startswith('Checked:')
        assert result.json()['answer']==DATA['examples'][0]['answer']
        assert client.post('/api/v1/lessons/g8-algebraic-expressions-01/questions/no-such-question/reveal').status_code==404
        bank=client.get('/api/v1/practice/g8-algebraic-expressions-01')
        assert bank.status_code==200
        assert len(bank.json()['questions'])==15
        assert all('accepted_answers' not in q for q in bank.json()['questions'])
        mastery=client.get('/api/v1/practice/g8-algebraic-expressions-01/mastery')
        assert mastery.status_code==200
        assert all('answer' not in q for q in mastery.json()['questions'])


def test_mastery_totals_twenty_marks_and_requires_submitted_answers():
    answers={item.id:item.answer for item in MASTERY_BANK}
    correct, reviewed, tags=_score_assessment(MASTERY_BANK, answers)
    assert correct==5 and not tags and all(row['correct'] for row in reviewed)
    assert sum(q.marks for q in MASTERY_BANK)==20
