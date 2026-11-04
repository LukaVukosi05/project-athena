"""Grade 9 first-batch content, private-answer and whiteboard contracts."""
import json

from fastapi.testclient import TestClient

from app.main import app
from app.curriculum.grade9.whole_numbers_runtime import GRADE_9, LESSON_1, LESSON_2
from app.curriculum.grade9.assessment_whole_numbers import banks
from app.curriculum.validation import validate_curriculum
from app.practice.service import check_answer


def test_first_two_lessons_have_distinct_question_specific_states_and_complete_banks():
    assert [lesson.id for lesson in GRADE_9.topics[0].subtopics[0].lessons]==['g9-whole-numbers-01','g9-whole-numbers-02']
    for number,lesson in enumerate((LESSON_1,LESSON_2),1):
        practice,mastery,reassess,repairs,rules=banks(number)
        assert (len(lesson.whiteboard_questions),len(practice),len(mastery),len(reassess))==(15,15,5,3)
        assert repairs and rules
        for question in lesson.whiteboard_questions:
            scene=json.loads(question.whiteboard.visualization.parameters['scene_json'])
            assert scene['problem']==question.whiteboard.problem
            assert len(question.whiteboard.steps)==len(scene['actions'])>=3
            assert question.whiteboard.steps[-1].after_expression.startswith(f"{len(scene['actions'])}. Check:")
            assert all(step.before_expression!=step.working_expression!=step.after_expression for step in question.whiteboard.steps)
        for item in practice:
            assert len(set(item.options))==4 and item.accepted_answers==[item.options[item.options.index(item.accepted_answers[0])]]
            assert check_answer(item.id,item.accepted_answers[0])
            assert not check_answer(item.id,next(option for option in item.options if option not in item.accepted_answers))
        for item in [*mastery,*reassess]:
            assert len(set(item.options))==4 and item.answer in item.options
            assert set(item.public())=={'id','number','prompt','options','marks'}
    assert not [error for error in validate_curriculum([GRADE_9]) if error.grade_id=='grade-9']


def test_public_preview_conceals_answers_and_reveal_contains_all_steps():
    with TestClient(app) as client:
        topic=client.get('/api/v1/curriculum/grades/grade-9/topics/whole-numbers')
        previews=[client.get(f'/api/v1/lessons/g9-whole-numbers-0{number}') for number in (1,2)]
        reveal=client.post('/api/v1/lessons/g9-whole-numbers-01/questions/g9-whole-l01-w01/reveal')
        banks_public=[client.get(f'/api/v1/practice/g9-whole-numbers-0{number}') for number in (1,2)]
        mastery=client.get('/api/v1/practice/g9-whole-numbers-01/mastery')
    assert all(response.status_code==200 for response in [topic,*previews,reveal,*banks_public,mastery])
    assert [item['id'] for item in topic.json()['subtopics'][0]['lessons']]==['g9-whole-numbers-01','g9-whole-numbers-02']
    for preview in previews:
        public=preview.json()['whiteboard_questions']
        assert len(public)==15 and all(item['solution_gated'] and len(item['whiteboard']['steps'])==1 for item in public)
        assert all('answer' not in item and 'full_memo' not in item for item in public)
        for item in public:
            scene=json.loads(item['whiteboard']['visualization']['parameters']['scene_json'])
            assert not {'actions','memo','check','category','secondary','secondary_category',
                        'primary_stage','secondary_stage','factors','misconception'} & set(scene)
            step=item['whiteboard']['steps'][0]
            assert step['events']==[] and step['before_expression']==step['after_expression']
    assert len(reveal.json()['whiteboard']['steps'])>=3
    for bank in banks_public:
        assert len(bank.json()['questions'])==15 and all(len(item['options'])==4 for item in bank.json()['questions'])
        assert all('answer' not in item for item in bank.json()['questions'])
    assert len(mastery.json()['questions'])==5 and all(len(item['options'])==4 and 'answer' not in item for item in mastery.json()['questions'])
