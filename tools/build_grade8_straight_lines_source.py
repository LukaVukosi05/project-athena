"""Write the two teacher-review source packs from explicit checked geometry cases."""
from pathlib import Path
from app.curriculum.grade8.straight_lines_cases import LESSON_1, LESSON_2

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/curriculum/grade8/geometry-of-straight-lines'
DBE = 'https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%208.pdf?ver=2026-01-20-202040-113'

def build(cases, number, title):
    out = [f'# Grade 8 Geometry of Straight Lines — Lesson {number}: {title}', '',
           'Status: original Athena authoring draft; teacher review and native visual runtime required before publication.',
           f'Curriculum: [DBE 2026 Grade 8 Mathematics ATP]({DBE}), Term 3, Geometry of Straight Lines.', '',
           'Learning objective: identify the angle relationship in an accurately labelled diagram, justify the equation, solve for the marked quantity and verify the original diagram.', '',
           'Why it matters: a visually plausible angle is not a reason. Learners must link each equality or sum to intersecting, perpendicular or parallel lines.', '',
           'Prerequisites: straight angle 180°, right angle 90°, basic algebraic equations and angle notation.',
           'Estimated duration: 90 minutes; 15 worked examples, 15 parallel independent questions to author and five mastery items to author.', '',
           '## Whiteboard contract', '',
           '- Draw the stated line family before any angle number. Give each ray and intersection a stable label. Parallel lines receive visible matching arrow marks.',
           '- Show the complete question and the given angle first. Keep x and the final calculation hidden.',
           '- Highlight exactly the two regions to which the stated theorem applies. Display that theorem before writing its equation.',
           '- Add one mathematical line per step beside the diagram. Preserve every earlier line; highlight the active line.',
           '- Verify by substituting into the original diagram. Previous, Next and Replay reconstruct the same labels and states.',
           '- Captions and eventual narration must use the same teaching sentence; reduced motion preserves the reveal order.', '',
           '## Worked examples', '']
    for i,c in enumerate(cases,1):
        difficulty = 'foundation' if i==1 else 'easy' if len(c.given)==1 else 'standard'
        angle_value = c.given[0] if len(c.given)==1 and c.relationship in {'vertical','corresponding','alternate'} else c.answer if len(c.given)==1 else c.given[0]*c.answer+c.given[1]
        out.extend([f'### {i:02} · {c.id} · {difficulty}', '',
                    f'**Question:** {c.problem}', '',
                    f'**Visual:** {c.diagram} diagram; two separately targetable angle sectors; {c.relationship} relationship. Given values: {c.given}.', '',
                    '**Whiteboard teaching:**', ''])
        for n,row in enumerate(c.working,1): out.append(f'{n}. Reveal and explain: {row}')
        out.extend([f'{len(c.working)+1}. Verify against the original diagram: {c.check}', '',
                    f'**Answer:** {"x = " if len(c.given)>1 else "Marked angle = "}{c.answer}{"°" if len(c.given)==1 else ""}' + (f'; labelled angle = {angle_value}°.' if len(c.given)>1 else '.'), '',
                    f'**First-error diagnosis:** {c.misconception}', '',
                    '**Reteaching:** redraw only the relevant angle pair with changed values; require the learner to name the relationship before writing a new equation.', ''])
    out.extend(['## Release gate', '',
                'Do not mark interactive or publish yet. Increase later-question complexity through multi-relationship diagrams; author unseen practice, mastery and parallel reassessment. Register the appropriate geometry renderer and semantic targets; prove that initial, operation and result states differ for all 15 examples. Obtain mathematical teacher review and browser QA on mobile and desktop.', ''])
    DEST.mkdir(parents=True,exist_ok=True)
    path=DEST/f'lesson-{number:02}.md';path.write_text('\n'.join(out),encoding='utf-8');return path

if __name__=='__main__':
    for path in (build(LESSON_1,1,'Angles at intersecting and perpendicular lines'), build(LESSON_2,2,'Parallel lines and a transversal')): print(path)
