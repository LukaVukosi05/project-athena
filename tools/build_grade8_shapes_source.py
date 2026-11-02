"""Emit explicit teacher-review source packs and private changed-value memos."""
from pathlib import Path
from app.curriculum.grade8.shapes_cases import LESSONS,variant

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'docs/curriculum/grade8/geometry-of-2d-shapes'
ATP='https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%208.pdf?ver=2026-01-20-202040-113'
TITLES={1:'Classify triangles by their sides',2:'Interior angles of triangles',3:'Equilateral and isosceles triangles',4:'Classify quadrilaterals from evidence',5:'Quadrilateral and parallelogram angles'}

def build(n):
    cases=LESSONS[n]
    rows=[f'# Grade 8 Geometry of 2D Shapes — Lesson {n}: {TITLES[n]}','',
          'Status: original authoring draft; mathematical teacher review and device browser acceptance pending.','',
          f'Curriculum: [DBE 2026 Grade 8 Mathematics ATP]({ATP}), Term 3, Geometry of 2D Shapes.','',
          f'Objective: {TITLES[n].lower()} using stated geometric properties and verified reasoning.','',
          'Prerequisites: labelled vertices and sides, right and straight angles, and equality markings.','',
          'Duration: about 90 minutes. Fifteen worked examples, fifteen independent practice questions, five mastery questions and three parallel reassessments.','',
          '## Whiteboard contract','',
          '- Plot actual labelled vertices and edges from the current question; preserve aspect ratio and do not substitute a generic triangle or quadrilateral.',
          '- Initially show the complete question and unannotated figure. Reveal a given label, then the relevant relationship, one operation, its result, and a check.',
          '- Keep earlier written steps visible alongside the shape; do not display the final answer in the initial scene.',
          '- Show matching equal-side markings or parallel/right-angle evidence when the question states them. Classify from stated evidence, not the apparent drawing alone.',
          '- Previous, Next and Replay must reconstruct deterministic stages. Captions and narration use the same sentence.', '', '## Worked examples','']
    for i,c in enumerate(cases,1):
        rows.extend([f'### Example {i:02} — {c.id}','',f'**Problem:** {c.problem}','',
                     f'**Visual:** {c.scene["shape"]} with question-specific vertices {c.scene["points"]}, labels {c.scene.get("labels",c.scene.get("angles",{}))}.','',
                     '**Whiteboard sequence:**',''])
        rows.extend(f'{j}. {step}' for j,step in enumerate(c.working,1))
        rows.extend([f'{len(c.working)+1}. Check the original figure: {c.check}','',f'**Answer:** {c.answer}','',
                     f'**First-error diagnosis:** {c.misconception}','',
                     '**Targeted repair:** redraw the same type of figure with different given measures; make the learner identify the relevant property before calculating.',''])
    for title,ids,shift in [('Independent practice',range(1,16),1),('Mastery check',(3,6,9,12,15),2),('Parallel reassessment',(6,11,15),3)]:
        rows.extend([f'## {title}','','Attempt independently; the following memo is withheld in the app until submission.',''])
        for j,index in enumerate(ids,1):
            c=variant(cases[index-1],shift)
            rows.extend([f'### Question {j:02}','',c.problem,'','**Complete memo:**',''])
            rows.extend(f'{k}. {step}' for k,step in enumerate(c.working,1))
            rows.extend([f'{len(c.working)+1}. Check: {c.check}',f'**Answer:** {c.answer}',''])
    rows.extend(['## Release decision','','Teacher checks all classifications, diagrams, marking and equivalent answer scoring. Browser QA tests every step and narrow screen. Keep the lesson marked for review until that evidence exists.',''])
    DEST.mkdir(parents=True,exist_ok=True)
    path=DEST/f'lesson-{n:02}.md';path.write_text('\n'.join(rows),encoding='utf-8');return path

if __name__=='__main__':
    for n in LESSONS:print(build(n))
