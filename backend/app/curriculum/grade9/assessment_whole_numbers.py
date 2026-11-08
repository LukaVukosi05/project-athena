"""Private four-option practice and assessment banks from the authored packs."""
from pydantic import BaseModel, Field
from app.curriculum.grade9.whole_numbers_runtime import DATA_1,DATA_2,LESSON_1,LESSON_2,EXTENDED,INTEGER_LESSONS,EXPONENT_LESSONS,PATTERN_LESSONS,FUNCTION_LESSONS,EXPRESSION_LESSONS,EQUATION_LESSONS,GRAPH_LESSONS,LINE_LESSONS,SHAPE_LESSONS,AREA_LESSONS,DATA_LESSONS,PROB_LESSONS,SOLID_LESSONS,SURFACE_LESSONS,TRANSFORM_LESSONS
from app.practice.schemas import PracticeQuestion,WorkedSolutionStep

class AssessmentQuestion(BaseModel):
    id:str
    number:int=Field(ge=1,le=5)
    prompt:str
    options:list[str]=Field(min_length=4,max_length=4)
    marks:int|None=None
    answer:str
    solution:list[str]
    verification:str
    misconception_tags:list[str]
    accepted_answers:list[str]
    def public(self):
        return self.model_dump(include={'id','number','prompt','options','marks'})

def banks(number,topic='whole-numbers'):
    lesson,data=__import__('app.curriculum.grade10.algebra',fromlist=['EUC_LESSONS']).EUC_LESSONS[number] if topic=='grade10_euc' else __import__('app.curriculum.grade10.algebra',fromlist=['TRIG_LESSONS']).TRIG_LESSONS[number] if topic=='grade10_trig' else __import__('app.curriculum.grade10.algebra',fromlist=['EEI_LESSONS']).EEI_LESSONS[number] if topic=='grade10_eei' else __import__('app.curriculum.grade10.algebra',fromlist=['LESSONS']).LESSONS[number] if topic=='grade10' else TRANSFORM_LESSONS[number] if topic=='transform' else SURFACE_LESSONS[number] if topic=='surface' else SOLID_LESSONS[number] if topic=='solid' else PROB_LESSONS[number] if topic=='prob' else DATA_LESSONS[number] if topic=='data' else AREA_LESSONS[number] if topic=='area' else SHAPE_LESSONS[number] if topic=='shapes' else LINE_LESSONS[number] if topic=='lines' else GRAPH_LESSONS[number] if topic=='graphs' else EQUATION_LESSONS[number] if topic=='equations' else EXPRESSION_LESSONS[number] if topic=='expressions' else FUNCTION_LESSONS[number] if topic=='functions' else PATTERN_LESSONS[number] if topic=='patterns' else EXPONENT_LESSONS[number] if topic=='exponents' else INTEGER_LESSONS[number] if topic=='integers' else (LESSON_1,DATA_1) if number==1 else (LESSON_2,DATA_2) if number==2 else EXTENDED[number]
    tag=f'grade10-euc-{number:02}' if topic=='grade10_euc' else f'grade10-trig-{number:02}' if topic=='grade10_trig' else f'grade10-eei-{number:02}' if topic=='grade10_eei' else f'grade10-algebra-{number:02}' if topic=='grade10' else f'grade9-transform-{number:02}' if topic=='transform' else f'grade9-surface-{number:02}' if topic=='surface' else f'grade9-solid-{number:02}' if topic=='solid' else f'grade9-probability-{number:02}' if topic=='prob' else f'grade9-data-{number:02}' if topic=='data' else f'grade9-area-{number:02}' if topic=='area' else f'grade9-shapes-{number:02}' if topic=='shapes' else f'grade9-lines-{number:02}' if topic=='lines' else f'grade9-graphs-{number:02}' if topic=='graphs' else f'grade9-equations-{number:02}' if topic=='equations' else f'grade9-expressions-{number:02}' if topic=='expressions' else f'grade9-functions-{number:02}' if topic=='functions' else f'grade9-patterns-{number:02}' if topic=='patterns' else f'grade9-exponents-{number:02}' if topic=='exponents' else f'grade9-integers-{number:02}' if topic=='integers' else 'number-set-classification' if number==1 else 'prime-power-selection' if number==2 else f'grade9-whole-numbers-{number:02}'
    practice=[]
    for index,item in enumerate(data['practice'],1):
        reason=item['memo'].split('. ',1)[-1]
        correct=item['options'][item['answer_index']]
        practice.append(PracticeQuestion(id=item['id'],lesson_id=lesson.id,question_number=index,
            difficulty=lesson.whiteboard_questions[index-1].difficulty,
            cognitive_level=lesson.whiteboard_questions[index-1].cognitive_level,marks=2 if index<=5 else 3,
            type='multiple_choice',prompt=item['prompt'],options=item['options'],accepted_answers=[correct],
            hints=['Write the original expression and mark the factor or real-number interval.' if topic=='grade10' else 'Plot all original vertices and mark the axis or centre before applying the rule.' if topic=='transform' else 'Draw the labelled cross-section or faces, and record the units in your book.' if topic=='surface' else 'Count the solid’s actual faces, edges and vertices or draw its net in your book.' if topic=='solid' else 'List all equally likely outcomes or conditional branches in your book.' if topic=='prob' else 'List every observation, mark the category and use a zero-based axis where relevant.' if topic=='data' else 'Draw the measured boundary or region and write its units in your book.' if topic=='area' else 'Mark the given sides and angles and name the geometric property in your book.' if topic=='shapes' else 'Mark the exact angle sectors and line markings in your book before choosing.' if topic=='lines' else 'Plot the given points on axes in your book before choosing.' if topic=='graphs' else 'Write the original equation and apply the same operation to both sides.' if topic=='equations' else 'Underline matching terms and show the first legal transformation in your book.' if topic=='expressions' else 'Track one input-output pair across the flow, table and equation before choosing.' if topic=='functions' else 'Align each term with its position, then write the next operation in your book.' if topic=='patterns' else 'Identify the base and exponent, then write the first legal operation in your book.' if topic=='exponents' else 'Write the original signed quantities and one operation in your book before choosing.' if topic=='integers' else 'Write or factorise the exact number in your book before choosing.',
                   'Expand or substitute back to check every term and restriction.' if topic=='grade10' else 'Apply the rule to both coordinates of every vertex; preserve original and image.' if topic=='transform' else 'Check each face pair or base layer and distinguish cm² from cm³.' if topic=='surface' else 'Compare each net face with the solid; mark curved surfaces and matching edges.' if topic=='solid' else 'Count favourable and possible outcomes; check the path denominator.' if topic=='prob' else 'Recount the dataset, check the denominator, category and graph scale.' if topic=='data' else 'Recalculate from the original dimensions and distinguish length units from square units.' if topic=='area' else 'Check corresponding sides, angle sum or supplementary pair against the given figure.' if topic=='shapes' else 'Name the angle pair and theorem; check the sum or equality.' if topic=='lines' else 'Compare the plotted points with the scale, gradient and intercept.' if topic=='graphs' else 'Expand, substitute, or multiply back and retain any denominator restriction.' if topic=='expressions' else 'Check the original pair and try another input with the same rule.' if topic=='functions' else 'Test your rule at two given positions and inspect changing differences.' if topic=='patterns' else 'Check the exponent law, parentheses, normalized coefficient and units.' if topic=='exponents' else 'Check sign, parentheses and the first incorrect step against the original question.' if topic=='integers' else 'Check whether the question asks for the smallest set, HCF, LCM or a context quantity.'],
            worked_solution=[WorkedSolutionStep(expression=item['prompt'],explanation='Start with the original givens.',why='A choice without working may hide a misconception.'),
                WorkedSolutionStep(expression=correct,explanation=reason,why=reason,verification=reason)],
            misconception_tags=[tag],verification={'original_question_check':reason},
            correct_feedback='Correct. Compare your written method with the worked review.',source=data['source'],
            answer_hidden_before_submission=True))
    def assessment(item,index,prefix):
        correct=item['options'][item['answer_index']]
        reason=item['memo'].split('. ',1)[-1]
        return AssessmentQuestion(id=item['id'],number=index,prompt=item['prompt'],options=item['options'],
            marks=4 if prefix=='m' else None,answer=correct,accepted_answers=[correct],
            solution=[reason,correct],verification=reason,misconception_tags=[tag])
    mastery=[assessment(item,i,'m') for i,item in enumerate(data['mastery'],1)]
    reassessment=[assessment(item,i,'r') for i,item in enumerate(data['reassessment'],1)]
    repairs={tag:{'diagnosis':'Locate the first unmatched term, sign, bound or excluded denominator.' if topic=='grade10' else 'Locate the first vertex with a wrong sign, swapped component or wrong centre.' if topic=='transform' else 'Find the first incorrect dimension, omitted face, conversion or unit.' if topic=='surface' else 'Find the first missing face, incorrect face shape or confused curved edge.' if topic=='solid' else 'Locate the first incorrect event, denominator, branch or theoretical assumption.' if topic=='prob' else 'Find the first wrong tally, denominator, axis baseline or interpretation.' if topic=='data' else 'Find the first incorrect unit conversion, missing edge or counted region.' if topic=='area' else 'Locate the first unjustified shape property or correspondence.' if topic=='shapes' else 'Identify the first unjustified angle relationship against the actual marked sectors.' if topic=='lines' else 'Locate the first plotted point, gradient or axis reading that differs from the givens.' if topic=='graphs' else 'Find the first term, sign or factor that no longer matches the original expression.' if topic=='expressions' else 'Locate the first input-output pair that the claimed equation gets wrong.' if topic=='functions' else 'Locate the first term or position where the proposed rule fails.' if topic=='patterns' else 'Locate the first wrong exponent law, base or decimal shift.' if topic=='exponents' else 'Check the first sign, grouping or operation that differs from the original expression.' if topic=='integers' else 'The first incorrect choice used the wrong mathematical classification or prime-power rule.',
        'repair':'Restore the first incorrect term and verify by the inverse operation.' if topic=='grade10' else 'Restore the first incorrect vertex, apply the same rule to all three and retry.' if topic=='transform' else 'Restore the missing face or correct base area, then retry with new dimensions.' if topic=='surface' else 'Restore the first incorrect term and verify by the inverse operation.' if topic=='grade10' else 'Restore the first incorrect vertex, apply the same rule to all three and retry.' if topic=='transform' else 'Restore the missing face or correct solid property and retry on a different model.' if topic=='solid' else 'Restore the sample space or tree, then retry with changed outcomes.' if topic=='prob' else 'Restore the source data, recalculate and retry with fresh observations.' if topic=='data' else 'Restore the original dimensions, trace the correct boundary or area and retry changed values.' if topic=='area' else 'Restore the original markings, state the correct geometric reason and retry with changed values.' if topic=='shapes' else 'Restore the correct angle pair, state its theorem and retry with changed angles.' if topic=='lines' else 'Restore the original point and axes, redraw the rise/run triangle and retry with changed values.' if topic=='graphs' else 'Restore that term or factor; check by expansion and preserve any excluded value.' if topic=='expressions' else 'Correct the multiplier or adjustment and verify another original pair.' if topic=='functions' else 'Retain the given terms, replace the wrong rule, then retry with changed values.' if topic=='patterns' else 'Expand the factors or reciprocal, correct the first wrong step, then retry changed values.' if topic=='exponents' else 'Rewrite the signed operation, show its correct result and retry with changed numbers.' if topic=='integers' else 'Rebuild the exact value or every prime tree, identify the first incorrect step, then retry changed numbers.'}}
    rules={tag:'Use a parallel item with new numbers; verify the result against all original givens.'}
    return practice,mastery,reassessment,repairs,rules

PRACTICE_1,MASTERY_1,REASSESSMENT_1,REPAIRS_1,RULES_1=banks(1)
PRACTICE_2,MASTERY_2,REASSESSMENT_2,REPAIRS_2,RULES_2=banks(2)
EXTENDED_BANKS={number:banks(number) for number in range(3,9)}
INTEGER_BANKS={number:banks(number,'integers') for number in range(1,6)}
EXPONENT_BANKS={number:banks(number,'exponents') for number in range(1,7)}
PATTERN_BANKS={number:banks(number,'patterns') for number in range(1,6)}
FUNCTION_BANKS={number:banks(number,'functions') for number in range(1,6)}
EXPRESSION_BANKS={number:banks(number,'expressions') for number in range(1,10)}
EQUATION_BANKS={number:banks(number,'equations') for number in range(1,7)}

GRAPH_BANKS={number:banks(number,'graphs') for number in range(1,8)}

LINE_BANKS={number:banks(number,'lines') for number in range(1,6)}
SHAPE_BANKS={number:banks(number,'shapes') for number in range(1,9)}
AREA_BANKS={number:banks(number,'area') for number in range(1,6)}
DATA_BANKS={number:banks(number,'data') for number in range(1,9)}
PROB_BANKS={number:banks(number,'prob') for number in range(1,6)}
SOLID_BANKS={number:banks(number,'solid') for number in range(1,5)}
TRANSFORM_BANKS={number:banks(number,'transform') for number in range(1,8)}
SURFACE_BANKS={number:banks(number,'surface') for number in range(1,7)}
