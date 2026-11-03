"""Rebuild readable source packs from checked, authored Pythagoras cases."""
from pathlib import Path
from app.curriculum.grade8.pythagoras_cases import LESSONS,variant
TITLES={1:'Squares on the sides of a right triangle',2:'Find the hypotenuse',3:'Find a missing perpendicular side',4:'Test whether a triangle is right-angled',5:'Pythagoras in practical contexts'}

DEST=Path(__file__).resolve().parents[1]/'docs/curriculum/grade8/pythagoras'
DEST.mkdir(parents=True,exist_ok=True)
for number,cases in LESSONS.items():
    lines=[f'# Grade 8 Pythagoras — Lesson {number}: {TITLES[number]}',
           '', 'Status: authored source for expert Mathematics review; live browser acceptance pending.',
           'Source alignment: DBE 2026 Grade 8 Mathematics ATP, Term 4, Theorem of Pythagoras.',
           'https://www.education.gov.za/Portals/0/Documents/Recovery%20plan%20page/2026%20ATPs/2026_ATP_Mathematics_Grade%208.pdf?ver=2026-01-20-202040-113',
           '', '## Teaching contract',
           'Show the problem and the question-specific triangle first. No final answer appears until the final result.',
           'Reveal one operation at a time; retain every completed equation in the worked-solution history.',
           'For a right triangle, the hypotenuse is opposite the right angle and must be longest. For the converse, show the given triangle without a right-angle mark until equality is established.',
           'Squared lengths are areas; lengths use the positive square root. Preserve exact surds. A different triangle is used for practice and reassessment.',
           '', '## Fifteen worked examples']
    for case in cases:
        lines += ['',f'### {case.id}',f'Question: {case.problem}',f'Visual: family={case.family}; side a={"unknown" if case.lesson == 3 else case.a}, side b={case.b}, side c={case.c}; context={case.context or "triangle"}.']
        lines += [f'{i}. {row}' for i,row in enumerate(case.working,1)]
        lines += [f'Final answer: {case.answer}',f'Check: {case.check}',f'First error to diagnose: {case.misconception}',
                  'Whiteboard: show the complete problem and given figure first; reveal one numbered operation and its matching visual evidence per click; keep earlier operations visible; reveal the answer and original-side check only at the end.']
    lines += ['', '## Independent practice', 'Submit each of 15 changed-data problems before the worked memo becomes available.']
    for case in cases:
        other=variant(case,1)
        lines += ['',f'### Changed-data practice for {case.id}',f'Independent question: {other.problem}',
                  'Whiteboard: keep the memo hidden until submission; construct a fresh diagram from these changed side lengths.']
        lines += [f'{i}. {row}' for i,row in enumerate(other.working,1)]
        lines += [f'Answer (teacher memo): {other.answer}',f'Check: {other.check}']
    lines += ['', '## Mastery and parallel reassessment',
             'Five changed-data mastery items use worked positions 3, 6, 9, 12 and 15 with shift 2. Three further changed-data items use positions 6, 11 and 15 with shift 3.',
             'Pass at 80%. If an error occurs, reteach the first unsupported choice of side or arithmetic square before a parallel retry.', '']
    (DEST/f'lesson-{number:02}.md').write_text('\n'.join(lines),encoding='utf-8')
print('wrote',len(LESSONS),'Pythagoras packs')
