"""Original two-intersection angle chains; numeric values and diagrams share one source."""
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class ChainCase:
    id: str
    lesson: int
    family: str
    given: int
    intermediate: int
    target_angle: int
    coefficient: int
    offset: int
    answer: int
    problem: str
    working: tuple[str, ...]
    check: str
    misconception: str
    wrong_claim: str
    scene: dict


def make_case(lesson: int, index: int, variant: int = 0) -> ChainCase:
    if not 3 <= lesson <= 5 or not 1 <= index <= 15 or not 0 <= variant <= 3:
        raise ValueError('Unknown angle chain')
    family = ('corresponding_linear', 'alternate_linear', 'cointerior_vertical')[(index-1)//5]
    relation = {'corresponding_linear':'corresponding', 'alternate_linear':'alternate interior',
                'cointerior_vertical':'co-interior'}[family]
    if lesson == 3:
        given = (43,58,72,105,126,49,63,77,109,131,52,69,84,117,138)[index-1] + 2*variant
        intermediate = 180-given if family == 'cointerior_vertical' else given
        target = intermediate if family == 'cointerior_vertical' else 180-intermediate
        coeff,offset,answer = 0,0,target
    elif lesson == 4:
        answer = 8 + index*2 + variant
        coeff = 1 + index%3
        offset = 8 + index%5
        target = coeff*answer+offset
        if target >= 170: raise ValueError('Invalid target angle')
        intermediate = 180-target if family != 'cointerior_vertical' else target
        given = 180-intermediate if family == 'cointerior_vertical' else intermediate
    else:
        given = (45,56,67,78,89,51,62,73,84,95,47,59,71,83,101)[index-1] + 2*variant
        intermediate = 180-given if family == 'cointerior_vertical' else given
        target = intermediate if family == 'cointerior_vertical' else 180-intermediate
        coeff,offset,answer = 0,0,target
    wrong = {
        'corresponding_linear': ('The marked angles are equal because they look the same.',
                                 'The corresponding angles add to 180°.'),
        'alternate_linear': ('The alternate interior angles add to 180°.',
                              'The marked angles are equal only because the drawing looks symmetric.'),
        'cointerior_vertical': ('The co-interior angles are equal.',
                                'The co-interior angles add to 90°.'),
    }[family][index%2]
    expression = f'({coeff}x + {offset})°' if lesson==4 else 'x'
    if lesson == 5:
        problem = (f'Two parallel lines are cut by a transversal. The upper marked angle is {given}°. '
                   f'A learner writes: “{wrong}” Find the first unsupported claim, repair it, then find the lower angle x.')
    else:
        problem = (f'Two parallel lines are cut by a transversal. The upper marked angle is {given}°. '
                   f'The marked pair is {relation}. An angle beside the lower marked angle is labelled {expression}. '
                   f'Find {"x" if lesson==4 else "the angle x"} and justify both angle steps.') if family != 'cointerior_vertical' else (
                   f'Two parallel lines are cut by a transversal. An upper interior angle is {given}°. '
                   f'The lower interior angle on the same side has a vertically opposite angle labelled {expression}. '
                   f'Find {"x" if lesson==4 else "the angle x"} and justify both angle steps.')
    first = (f'Co-interior angles add to 180°, so the lower interior angle is 180° − {given}° = {intermediate}°.'
             if family == 'cointerior_vertical' else
             f'{relation.capitalize()} angles are equal, so the lower marked angle is {intermediate}°.')
    second = (f'Vertically opposite angles are equal, so the target angle is {target}°.'
              if family == 'cointerior_vertical' else
              f'Adjacent angles on a straight line add to 180°, so the target angle is 180° − {intermediate}° = {target}°.')
    steps = [f'Locate the two marked parallel lines and transversal; read the given {given}° angle.',
             f'Identify the {relation} angle pair before calculating.', first, second]
    if lesson == 4:
        steps += [f'The marked target is {coeff}x + {offset} degrees, so {coeff}x + {offset} = {target}.',
                  f'Subtract {offset} from both sides: {coeff}x = {target-offset}.',
                  f'Divide by {coeff}: x = {answer}.']
        check = f'{coeff}({answer}) + {offset} = {target}°; the original parallel-line pair checks against {given}°.'
    else:
        steps += [f'Therefore x = {target}°.']
        check = (f'{given}° + {intermediate}° = 180° and the vertical target is {target}°.'
                 if family == 'cointerior_vertical' else
                 f'The transferred angle is {given}°; {given}° + {target}° = 180°.')
    if lesson == 5:
        steps = [steps[0],f'Read the learner claim exactly: “{wrong}”',
                 f'The first unsupported claim is “{wrong}”: the marked pair is {relation}.',
                 first,second,steps[-1]]
    scene={'family':family,'given':given,'target_label':expression,'wrong_claim':wrong if lesson==5 else '',
           'relation':relation,'lesson':lesson}
    case=ChainCase(f'g8-lines-{lesson:02}-w{index:02}',lesson,family,given,intermediate,target,coeff,offset,answer,
                   problem,tuple(steps),check,'Use the named angle theorem, then the second relationship; do not measure the picture.',wrong if lesson==5 else '',scene)
    assert 0 < given < 180 and 0 < intermediate < 180 and 0 < target < 180
    assert (given+intermediate==180 if family=='cointerior_vertical' else given==intermediate)
    assert (target==intermediate if family=='cointerior_vertical' else target+intermediate==180)
    if lesson==4: assert coeff*answer+offset==target
    return case

LESSONS={n:tuple(make_case(n,i) for i in range(1,16)) for n in (3,4,5)}
