"""Write the exact teaching, practice, mastery and reassessment items into the source packs."""
from pathlib import Path
from app.curriculum.grade8.straight_lines_chain_cases import LESSONS, make_case
from app.curriculum.grade8.assessment_straight_lines_chain import expected

ROOT=Path(__file__).resolve().parents[1]/'docs/curriculum/grade8/geometry-of-straight-lines'
for number in (3,4,5):
    path=ROOT/f'lesson-{number:02}.md'
    existing=path.read_text(encoding='utf-8').split('## Authored question bank')[0].rstrip()
    lines=[existing,'','## Authored question bank','',
           'Each whiteboard example shows the problem, marked parallel lines and a visible first angle. '
           'The intermediate angle is concealed until its relationship is explained. The second angle and '
           'final answer appear only after their own mathematical steps. Previous results persist in the written solution.','']
    for index,case in enumerate(LESSONS[number],1):
        lines += [f'### Worked example {index}: {case.id}',case.problem,'',
                  f'Diagram: {case.scene["family"]}; given {case.given}°, first intermediate sector {case.intermediate}°, '
                  f'target sector {case.target_angle}°; initial target label {case.scene["target_label"]}.',
                  'Whiteboard sequence:','']
        lines += [f'{j}. {row}' for j,row in enumerate(case.working,1)]
        lines += ['',f'Answer: {expected(case)}. Check: {case.check}',f'Misconception: {case.misconception}','']
    lines += ['## Independent practice (changed values, gated memo)','']
    for index in range(1,16):
        case=make_case(number,index,1)
        lines += [f'{index}. {case.problem}'+(' Respond as “relationship; value°”.' if number==5 else ''),
                  f'   Memo (after submission): {" ".join(case.working)} Check: {case.check} Answer: {expected(case)}.','']
    lines += ['## Mastery check (five fresh items)','']
    for position,index in enumerate((3,6,9,12,15),1):
        case=make_case(number,index,2)
        lines += [f'{position}. {case.problem}'+(' Respond as “relationship; value°”.' if number==5 else ''),
                  f'   Memo (after submission): {" ".join(case.working)} Check: {case.check} Answer: {expected(case)}.','']
    lines += ['## Targeted repair and parallel reassessment','',
              'First locate the earliest unsupported theorem claim; highlight the correct marked sectors, '
              'recompute the intermediate value, and verify it against the original given. '
              'Then submit three further changed-value items independently.','']
    for position,index in enumerate((5,10,15),1):
        case=make_case(number,index,3)
        lines += [f'{position}. {case.problem}'+(' Respond as “relationship; value°”.' if number==5 else ''),
                  f'   Memo (after submission): {" ".join(case.working)} Check: {case.check} Answer: {expected(case)}.','']
    path.write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    print(path, len(lines))
