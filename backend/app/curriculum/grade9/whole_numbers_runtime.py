"""First Grade 9 runtime batch, compiled from reviewed source tables."""
import hashlib
import json
from pathlib import Path

from app.curriculum.schemas import (
    AccessLevel, ContentStatus, GradeCurriculum, Lesson, LessonBlock, MathematicalOperation,
    SemanticObject, StepExplanation, Subtopic, TeachingStep, TimelineEvent, Topic,
    VisualizationInstruction, VisualizationState, WhiteboardBlock, WhiteboardQuestion,
)

ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'docs/curriculum/grade9/whole-numbers'
GENERATED=Path(__file__).with_name('generated')
EXTENDED_TITLES={3:'Ratio and rate',4:'Direct and inverse proportion',5:'Percentages and transactions',
                 6:'Budgets and accounts',7:'Loans and interest',8:'Exchange, commission and rentals'}
EXTENDED_TEMPLATES={3:'grade9_ratio_rate',4:'grade9_proportion',5:'grade9_transaction',
                    6:'grade9_ledger',7:'grade9_interest',8:'grade9_decision'}
INTEGER_TITLES={1:'Ordering and four operations',2:'Sign rules and integer properties',
                3:'Squares, cubes and integer roots',4:'Multi-operation integer contexts',
                5:'First-error diagnosis and reassessment'}
INTEGER_TEMPLATES={n:f'grade9_integer_{n}' for n in range(1,6)}
EXPONENT_TITLES={1:'Powers and exponent laws',2:'Zero and negative exponents',
                 3:'Scientific notation and small numbers',4:'Combined operations and parentheses',
                 5:'Scientific notation in contexts',6:'Exponent error diagnosis and reassessment'}
EXPONENT_TEMPLATES={n:f'grade9_exponent_{n}' for n in range(1,7)}
PATTERN_TITLES={1:'Visual and numeric patterns',2:'Tables and position rules',
                3:'Changing differences and ratios',4:'General rules and unknown terms',
                5:'Justifying and diagnosing pattern rules'}
PATTERN_TEMPLATES={n:f'grade9_pattern_{n}' for n in range(1,6)}
FUNCTION_TITLES={1:'Flow diagrams and output values',2:'Input-output tables and inverse lookup',
                 3:'Formulae and equations',4:'Equivalent words, tables, formulae and graphs',
                 5:'Mixed representations and first-error repair'}
FUNCTION_TEMPLATES={n:f'grade9_function_{n}' for n in range(1,6)}
EXPRESSION_TITLES={1:'Algebraic language and term classification',2:'Collecting like terms with fractions and decimals',
 3:'Distributing monomials across polynomials',4:'Products and squares of binomials',
 5:'Polynomial division and substitution',6:'Common-factor factorisation',
 7:'Difference of two squares',8:'Trinomials and algebraic fractions',
 9:'Mixed expressions and first-error repair'}
EXPRESSION_TEMPLATES={n:f'grade9_expression_{n}' for n in range(1,10)}
EQUATION_TITLES={1:'Translate situations into equations',2:'Solve using inverse operations',
 3:'Brackets and unknowns on both sides',4:'Solve equations using exponent laws',
 5:'Factorisation and the zero-product property',6:'Substitution tables and first-error repair'}
EQUATION_TEMPLATES={n:f'grade9_equation_{n}' for n in range(1,7)}
GRAPH_TITLES={1:'Global graph features in context',2:'Ordered pairs and Cartesian plotting',
 3:'Gradient as rise over run',4:'Intercepts of straight lines',5:'Draw a line from its equation',
 6:'Find an equation from a graph',7:'Integrated graph interpretation and first-error repair'}
GRAPH_TEMPLATES={n:f'grade9_graph_{n}' for n in range(1,8)}
LINE_TITLES={1:'Intersecting and perpendicular angle relationships',2:'Parallel lines and a transversal',3:'Combined angle chains',4:'Algebraic unknowns in line geometry',5:'Proof, first-error diagnosis and reassessment'}
LINE_TEMPLATES={n:f'grade9_lines_{n}' for n in range(1,6)}
SHAPE_TITLES={1:'Triangle classes and angle sum',2:'Exterior angle of a triangle',3:'Quadrilateral properties',4:'Diagonals and polygon interior angles',5:'Congruent triangle conditions',6:'Similar triangles and scale',7:'Unknown sides and angles with reasons',8:'Integrated proof and first-error reassessment'}
SHAPE_TEMPLATES={n:f'grade9_shapes_{n}' for n in range(1,9)}
AREA_TITLES={1:'Polygons and SI units',2:'Composite polygon decomposition',3:'Circles and circumference',4:'Changing dimensions and scale',5:'Applied mixed cases and reassessment'}
AREA_TEMPLATES={n:f'grade9_area_{n}' for n in range(1,6)}
DATA_TITLES={1:'Investigation, population and sample',2:'Collection, representation and bias',3:'Frequency tables and grouped data',4:'Centre, spread and outliers',5:'Bar and broken-line comparisons',6:'Histograms and class intervals',7:'Pie charts and scatter plots',8:'Critical interpretation and written report'}
DATA_TEMPLATES={n:f'grade9_data_{n}' for n in range(1,9)}
SURFACE_TITLES={1:'Cube and rectangular prism surface area from nets',2:'Rectangular prism volume and capacity',3:'Triangular prism surface area and volume',4:'Closed cylinders: surface area and volume',5:'SI conversions and effects of doubling dimensions',6:'Applied measurement, first-error repair and reassessment'}
GRADE10_TITLES={1:'Rational and irrational real numbers',2:'Surds, integer bounds and appropriate rounding',3:'Multiply a binomial by a trinomial',4:'Factorise trinomials and group in pairs',5:'Factorise sums and differences of cubes',6:'Simplify and combine algebraic fractions with cubic denominators'}
GRADE10_TEMPLATES={n:f'grade10_algebra_{n}' for n in range(1,7)}
GRADE10_EEI_TITLES={1:'Exponent laws and zero or negative powers',2:'Fractional exponents and exponential equations',3:'Linear equations with brackets and fractions',4:'Quadratic equations by factorisation',5:'Simultaneous linear equations',6:'Word problems: translate, solve and interpret',7:'Literal equations and changing the subject',8:'Linear inequalities and interval notation',9:'Mixed methods, first-error diagnosis and reassessment'}
GRADE10_EEI_TEMPLATES={n:f'grade10_eei_{n}' for n in range(1,10)}
GRADE10_TRIG_TITLES={1:'Opposite, adjacent and hypotenuse: sine, cosine and tangent',2:'Quadrants and reference angles from 0° to 360°',3:'Reciprocal ratios cosec, sec and cot',4:'Exact ratios at 0°, 30°, 45°, 60° and 90°',5:'Two-dimensional right-triangle applications',6:'Solve acute-angle trigonometric equations',7:'Coordinate diagrams and signed ratios through 360°'}
GRADE10_TRIG_TEMPLATES={n:f'grade10_trig_{n}' for n in range(1,8)}
GRADE10_EUC_TITLES={1:'Intersecting and parallel line angle reasons',2:'Congruent and similar triangles with matching vertices',3:'Properties of kites, parallelograms and trapeziums',4:'Rectangle, rhombus and square diagonals and areas',5:'The midpoint theorem in triangles',6:'Mixed geometric riders and first-error repair'}
GRADE10_EUC_TEMPLATES={n:f'grade10_euc_{n}' for n in range(1,7)}
TRANSFORM_TITLES={1:'Coordinates and translations across quadrants',2:'Reflections in the coordinate axes',3:'Reflection in the line y = x',4:'Quarter-turn rotations around a given centre',5:'Infer a transformation from image coordinates',6:'Enlargement, reduction, perimeter and area',7:'Combined transformations and first-error reassessment'}
TRANSFORM_TEMPLATES={n:f'grade9_transform_{n}' for n in range(1,8)}
SURFACE_TEMPLATES={n:f'grade9_surface_{n}' for n in range(1,7)}
SOLID_TITLES={1:'Platonic solids: faces, edges and vertices',2:'Spheres and cylinders: curved and flat surfaces',3:'Nets of cubes, prisms, pyramids and cylinders',4:'Identify a solid from its net and repair the first error'}
SOLID_TEMPLATES={n:f'grade9_solid_{n}' for n in range(1,5)}
PROB_TITLES={1:'Sample spaces and equally likely outcomes',2:'Two-way tables and conditional counts',3:'Tree diagrams and compound events',4:'Experimental versus theoretical relative frequency',5:'Combined events, first-error diagnosis and reassessment'}
PROB_TEMPLATES={n:f'grade9_probability_{n}' for n in range(1,6)}

def build_lesson(number,topic='whole-numbers'):
    integers=topic=='integers'
    exponents=topic=='exponents'
    patterns=topic=='numeric-geometric-patterns'
    functions=topic=='functions-relationships'
    expressions=topic=='algebraic-expressions'
    equations=topic=='algebraic-equations'
    graphs=topic=='graphs'
    lines=topic=='geometry-of-straight-lines'
    shapes=topic=='geometry-of-2d-shapes'
    area=topic=='area-and-perimeter'
    handling=topic=='data-handling'
    probability=topic=='probability'
    solids=topic=='geometry-of-3d-objects'
    grade10=topic.startswith('grade10-')
    grade10_eei=topic=='grade10-exponents-equations-inequalities'
    grade10_trig=topic=='grade10-trigonometry'
    grade10_euc=topic=='grade10-euclidean-geometry'
    transform=topic=='transformation-geometry'
    surface=topic=='surface-area-and-volume'
    content_dir=ROOT/"backend/app/curriculum/grade10/generated" if grade10 else GENERATED
    data=json.loads((content_dir/f'{"euclidean" if grade10_euc else "trig" if grade10_trig else "eei" if grade10_eei else "algebra" if grade10 else "transformation" if transform else "surface_volume" if surface else "geometry_3d" if solids else "probability" if probability else "data" if handling else "area" if area else "shapes" if shapes else "straight_lines" if lines else "graphs" if graphs else "equations" if equations else "expressions" if expressions else "functions" if functions else "patterns" if patterns else topic.replace("-","_")}_{number:02}.json').read_text(encoding='utf-8'))
    source=(ROOT/"docs/curriculum/grade10"/('euclidean-geometry' if grade10_euc else 'trigonometry' if grade10_trig else 'exponents-equations-inequalities' if grade10_eei else 'algebraic-expressions') if grade10 else ROOT/'docs/curriculum/grade9'/topic if integers or exponents or patterns or functions or expressions or equations or graphs or lines or shapes or area or handling or probability or solids or surface or transform else SOURCE)/data['source']
    lesson_id=f'g10-euc-{number:02}' if grade10_euc else f'g10-trig-{number:02}' if grade10_trig else f'g10-eei-{number:02}' if grade10_eei else f'g10-algebra-{number:02}' if grade10 else f'g9-tg-{number:02}' if transform else f'g9-sv-{number:02}' if surface else f'g9-solid-{number:02}' if solids else f'g9-prob-{number:02}' if probability else f'g9-data-{number:02}' if handling else f'g9-area-{number:02}' if area else f'g9-shapes-{number:02}' if shapes else f'g9-straight-lines-{number:02}' if lines else f'g9-graphs-{number:02}' if graphs else f'g9-equations-{number:02}' if equations else f'g9-expressions-{number:02}' if expressions else f'g9-functions-{number:02}' if functions else f'g9-patterns-{number:02}' if patterns else f'g9-{topic}-{number:02}'
    template=GRADE10_EUC_TEMPLATES[number] if grade10_euc else GRADE10_TRIG_TEMPLATES[number] if grade10_trig else GRADE10_EEI_TEMPLATES[number] if grade10_eei else GRADE10_TEMPLATES[number] if grade10 else TRANSFORM_TEMPLATES[number] if transform else SURFACE_TEMPLATES[number] if surface else SOLID_TEMPLATES[number] if solids else PROB_TEMPLATES[number] if probability else DATA_TEMPLATES[number] if handling else AREA_TEMPLATES[number] if area else SHAPE_TEMPLATES[number] if shapes else LINE_TEMPLATES[number] if lines else GRAPH_TEMPLATES[number] if graphs else EQUATION_TEMPLATES[number] if equations else EXPRESSION_TEMPLATES[number] if expressions else FUNCTION_TEMPLATES[number] if functions else PATTERN_TEMPLATES[number] if patterns else EXPONENT_TEMPLATES[number] if exponents else INTEGER_TEMPLATES[number] if integers else 'grade9_number_sets' if number==1 else 'grade9_prime_factors' if number==2 else EXTENDED_TEMPLATES[number]
    questions=[]
    for index,scene in enumerate(data['worked'],1):
        qid=scene['id'];actions=scene['actions'];previous='Read the original question';steps=[]
        ids=['problem','model','token','category','factor-roots','prime-leaves','selection','operation','result','verification']
        objects=[SemanticObject(id=key,type='label' if key in {'problem','model','category','selection','factor-roots','prime-leaves'} else 'operation' if key=='operation' else 'verification' if key=='verification' else 'result' if key=='result' else 'token',value=key.replace('-',' ')) for key in ids]
        for j,action in enumerate(actions,1):
            final=j==len(actions)
            # The result of each stage is retained by the shared cumulative memo.
            after=f'{j}. {action}'
            why=('Keep the original expression, every partial term and all domain restrictions in view.' if grade10 else 'Keep each original vertex, transformed vertex, centre and axis on the same coordinate plane.' if transform else 'Keep each labelled dimension, net face, volume layer and squared or cubed unit visible.' if surface else 'Keep every original face or net edge visible and distinguish flat from curved surfaces.' if solids else 'Keep each side of the equality visible and check all solutions in the original equation.' if equations else 'Keep the whole outcome space, event condition and branch denominator visible.' if probability else 'Keep the dataset, denominator and axis scale visible while deriving the statistic.' if handling else 'Keep the axes and original coordinates fixed, and reveal each plotted point or line in order.' if graphs else 'Trace the actual boundary and square units, and keep unit conversions explicit.' if area else 'Mark the given sides and angles and justify the shape property before calculating.' if shapes else 'Mark the exact angle pair and justify its relationship before calculating.' if lines else 'Match each highlighted term or factor to the original expression and preserve domain restrictions.' if expressions else
                 'Follow one input-output pair through each linked representation.' if functions else
                 'Read the term positions and compare the actual figures before choosing a rule.' if patterns else
                 'Apply the exponent law to the specified base, and preserve the unit or fraction.' if exponents else
                 'Keep the signed values and legal order of operations visible.' if integers else
                 'The exact value decides its number set.' if number==1 else
                 'Each selected prime power must satisfy every original number.' if number==2 else
                 'Read the labelled quantities and units before changing the model.')
            spoken=(f'Let us check {action[7:]}' if action.startswith('Check: ')
                    else f'Our written result is {action[9:]}' if action.startswith('Written: ')
                    else f'{action} {why}' if grade10 or transform or exponents or patterns or functions or expressions or equations or graphs or lines or shapes or area or handling or probability or solids or surface
                    else f'We {action[0].lower()}{action[1:]}. {why}')
            duration=max(5500,min(24000,len(spoken.split())*500))
            steps.append(TeachingStep(id=f'{qid}-step-{j:02}',step_number=j-1,title=action,
                before_expression=previous,working_expression=f'From {previous} → {action}',
                operation=MathematicalOperation(type=f'grade10_euc_{number}_step' if grade10_euc else f'grade10_trig_{number}_step' if grade10_trig else f'grade10_eei_{number}_step' if grade10_eei else f'grade10_algebra_{number}_step' if grade10 else f'grade9_transform_{number}_step' if transform else f'grade9_surface_{number}_step' if surface else f'grade9_solid_{number}_step' if solids else f'grade9_area_{number}_step' if area else f'grade9_probability_{number}_step' if probability else f'grade9_data_{number}_step' if handling else f'grade9_shapes_{number}_step' if shapes else f'grade9_lines_{number}_step' if lines else f'grade9_graph_{number}_step' if graphs else f'grade9_equation_{number}_step' if equations else f'grade9_expression_{number}_step' if expressions else f'grade9_function_{number}_step' if functions else f'grade9_pattern_{number}_step' if patterns else f'grade9_exponent_{number}_step' if exponents else f'grade9_integer_{number}_step' if integers else 'grade9_set_step' if number==1 else 'grade9_factor_step' if number==2 else f'grade9_{number}_step',value=action,
                    action='verify_solution' if final else 'transform_expression'),
                after_expression=after,
                explanation=StepExplanation(what=action,
                    why='Justify each identity, factor or interval, then check by substitution or expansion.' if grade10 else 'Use the same coordinate rule on every vertex; keep the original point visible.' if transform else 'Attach the unit to every face or layer, then use the relevant formula or conversion.' if surface else 'Count face pieces against the corresponding solid and justify each matching edge.' if solids else 'Apply the stated inverse to both sides and substitute back into the original.' if equations else 'Draw each outcome or branch first; multiply along a path and check the denominator.' if probability else 'Retain the original data and show each count, denominator or axis choice before the conclusion.' if handling else 'Plot the stated point or triangle; retain earlier marks and verify the result against the givens.' if graphs else 'Keep the measured lengths and square units attached to the correct region or boundary.' if area else 'Use the marked shape property, congruency or similarity criterion and state the reason.' if shapes else 'Use only marked parallel, perpendicular or intersecting relationships; state the theorem.' if lines else 'Pair every new term with its origin; maintain excluded denominator values.' if expressions else 'Keep the original pair visible as the flow, table, formula and graph change.' if functions else 'Keep the actual positions and terms visible while deriving the rule.' if patterns else 'Identify the base and scope before changing its exponent.' if exponents else
                        'Show one signed operation, then check it against the original values.' if integers else
                        'Classify the exact value after simplifying it.' if number==1 else
                        'Prime leaves reproduce the given number; compare powers only after factorising.' if number==2 else
                        'Keep the original quantities and units attached to each calculation.',
                    purpose=action,remember='A cancelled factor leaves its original denominator restrictions; multiply back to check factorisation.' if grade10 else 'Translate both coordinates; reflections change or swap exact components; a scale factor k multiplies perimeter by k and area by k².' if transform else 'Area is measured in cm², volume in cm³, and 1 000 cm³ equals 1 L.' if surface else 'Use F + V = E + 2 only for convex polyhedra; a sphere and cylinder have curved surfaces.' if solids else 'Substitute every candidate into the original; a zero product may have two roots.' if equations else 'Compare favourable outcomes with the full sample space and check for replacement.' if probability else 'Check every calculation against the original observations and compare the axis with zero.' if handling else 'Re-read both coordinates and the graph scale before deciding.' if graphs else 'Check the boundary or region against the original dimensions and units.' if area else 'Check the derived measure against the original sides and angle sum.' if shapes else 'Check the derived measure in the original marked angle pair.' if lines else 'Expand, substitute or multiply back into the original, and retain restrictions.' if expressions else 'Check the result in the original representation and another given pair.' if functions else 'Test the rule at a second known position.' if patterns else 'Check the law with expanded factors or a reciprocal.' if exponents else 'Check the original signs and order of operations.' if integers else 'Check against the original expression.' if number==1 else
                        'For HCF choose shared smaller powers; for LCM choose all larger powers.' if number==2 else
                        'Check every derived amount against the original givens.'),
                common_mistake=scene['misconception'],animation_template=template,
                screen_reader_description=f'{previous}. {spoken}',
                visualization_state=VisualizationState(objects=ids,highlights=['model'],
                    annotations=[f'stage:{j}'],target='model',before_state=previous,
                    working_state=f'From {previous} → {action}',after_state=after),instructional_goal=action,
                duration_ms=duration,events=[TimelineEvent(at_ms=0,type='caption',text=spoken),
                    TimelineEvent(at_ms=0,type='narration',text=spoken),
                    TimelineEvent(at_ms=350,type='focus',targets=['model']),
                    TimelineEvent(at_ms=1100,type='show_operation',targets=['operation'],label=action[:200]),
                    TimelineEvent(at_ms=duration-600,type='reveal',targets=['result'],label=after[:200]),
                    TimelineEvent(at_ms=duration-120,type='verify' if final else 'complete',targets=['verification' if final else 'result'])],
                narration=spoken,state_after={'stage':j,'question_id':qid,'verification_complete':final,
                    'verification_link':scene['check'] if final else '', 'completion_state':after}))
            previous=after
        board=WhiteboardBlock(id=f'{qid}-board',representation='visual',problem=scene['problem'],
            initial_expression='Read the original question',steps=steps,
            visualization=VisualizationInstruction(type='statistics' if handling or probability else 'geometry' if grade10_euc or grade10_trig or lines or shapes or area or solids or surface or transform else 'algebra',template=template,parameters={
                'scene_json':json.dumps(scene,ensure_ascii=False),'question_id':qid,
                'prompt':scene['problem'],'total_steps':len(actions)}),semantic_objects=objects)
        questions.append(WhiteboardQuestion(id=qid,order=index,difficulty=scene['difficulty'],
            is_core_example=index==1,guidance_level='high' if index<=5 else 'moderate' if index<=10 else 'reduced',
            cognitive_level='knowledge' if index<=3 else 'routine' if index<=7 else 'complex' if index<=13 else 'problem_solving',
            marks=2 if index<=3 else 3 if index<=7 else 5 if index<=13 else 7,
            whiteboard=board,answer=scene['check'],full_memo=actions,
            misconception_tags=[scene['misconception'] if grade10 or integers or exponents or patterns or functions or expressions or equations or graphs or lines or shapes or handling or probability or solids or surface else 'number-set-classification' if number==1 else 'prime-power-selection' if number==2 else scene['misconception']],
            expected_evidence=scene['check']))
    title=GRADE10_EUC_TITLES[number] if grade10_euc else GRADE10_TRIG_TITLES[number] if grade10_trig else GRADE10_EEI_TITLES[number] if grade10_eei else GRADE10_TITLES[number] if grade10 else TRANSFORM_TITLES[number] if transform else SURFACE_TITLES[number] if surface else SOLID_TITLES[number] if solids else PROB_TITLES[number] if probability else DATA_TITLES[number] if handling else AREA_TITLES[number] if area else SHAPE_TITLES[number] if shapes else LINE_TITLES[number] if lines else GRAPH_TITLES[number] if graphs else EQUATION_TITLES[number] if equations else EXPRESSION_TITLES[number] if expressions else FUNCTION_TITLES[number] if functions else PATTERN_TITLES[number] if patterns else EXPONENT_TITLES[number] if exponents else INTEGER_TITLES[number] if integers else 'The real number system' if number==1 else 'Prime factors, HCF and LCM' if number==2 else EXTENDED_TITLES[number]
    lesson=Lesson(id=lesson_id,order=number,title=title,estimated_minutes=70 if number==1 else 80,
        objective=f'Explain and verify {title.lower()} with exact algebraic steps.' if grade10 else f'Plot and justify {title.lower()} with exact image coordinates.' if transform else f'Calculate and verify {title.lower()} with labelled dimensions and correct units.' if surface else f'Describe, count and justify {title.lower()} with a matched solid and net.' if solids else f'List outcomes, calculate and check {title.lower()} using exact fractions.' if probability else f'Collect, represent and interpret {title.lower()} from labelled observations.' if handling else f'Measure, calculate and check {title.lower()} with the correct SI units.' if area else f'Identify marked relationships and justify {title.lower()} with a calculation and check.' if shapes or lines else f'Plot, calculate and interpret {title.lower()} with a visible coordinate check.' if graphs else f'Carry out {title.lower()} with valid transformations, exact answers and verification.' if expressions else f'Link flow diagrams, tables, equations and graphs for {title.lower()}.' if functions else f'Extend, describe and justify {title.lower()} using positions, tables and diagrams.' if patterns else f'Use exponent laws and scientific notation to solve {title.lower()} with exact values.' if exponents else
            f'Calculate and explain {title.lower()} with signed integers and verify each result.' if integers else
            'Distinguish natural, whole, integer, rational and irrational real numbers using exact values.' if number==1 else
            'Factorise positive integers, calculate HCF and LCM with prime powers, and check context units.' if number==2 else
            f'Use exact Grade 9 methods for {title.lower()} and verify the result with units.',
        why_it_matters='These algebraic methods support equations, functions and later Grade 12 work.' if grade10 else 'Coordinate transformations support maps, drawings and later analytic geometry.' if transform else 'Correct surface and volume estimates inform materials and real container capacity.' if surface else 'Solid properties and nets determine whether a model folds and closes correctly.' if solids else 'Probabilities distinguish possible outcomes from observed results and support careful predictions.' if probability else 'Data summaries and honest scales help us compare groups without misleading readers.' if handling else 'Area estimates material; perimeter measures a boundary, so their units and scale factors differ.' if area else 'Geometric reasons support conclusions that cannot be read reliably from appearance.' if shapes or lines else 'Graphs show how quantities change and let us test algebraic relationships.' if graphs else 'Expressions connect patterns, equations, geometric area and rational quantities.' if expressions else 'One input-output relationship can be read from several equivalent representations.' if functions else 'Pattern rules connect growing figures and numbers to algebra.' if patterns else 'Powers express repeated factors and very large or small measured quantities.' if exponents else
            'Signed quantities model changes, debt, temperature and later algebra.' if integers else
            'Exact number classifications guide later algebra.' if number==1 else
            'Prime factors make shared groups and repeated cycles precise.' if number==2 else
            'A correct relationship and the right base prevent costly arithmetic errors.',
        intuition='Keep every original term visible, transform one part, then verify by reversing the operation.' if grade10 else 'Plot the original triangle, mark the centre or axis, and construct each image vertex one at a time.' if transform else 'Draw the actual faces and cross-section, then stack layers or unwrap the cylinder before calculating.' if surface else 'Count the given faces, vertices and edges, then match the solid to its net one face at a time.' if solids else 'Show the full sample space, mark the event, then count or multiply paths before simplifying.' if probability else 'Start with the original observations; build the table or graph, then calculate and interpret.' if handling else 'Label the original dimensions, mark the boundary or region, then update one measurement at a time.' if area else 'Trace the exact angle sectors and parallel markings before writing the theorem or equation.' if shapes or lines else 'Plot one coordinate at a time on fixed axes; keep the rise, run, intercept and written record together.' if graphs else 'Track each term to its original factor or bracket; justify every rewrite and check the starting expression.' if expressions else 'Track one input from flow machine to table, formula and coordinate pair.' if functions else 'Count the actual figures, align each term with its position, then test a rule.' if patterns else 'Show the base, expand or shift it, then compress to the correct power or reciprocal.' if exponents else
            'Keep the zero reference, the operation and the sign of each result visible.' if integers else
            'Simplify the value, then choose its smallest set and all containing sets.' if number==1 else
            'HCF keeps shared lowest powers; LCM keeps the highest powers present in any original number.' if number==2 else
            'Keep the original givens visible, apply one justified action and check units.',
        prerequisites=[] if number==1 else [f'g10-trig-{number-1:02}' if grade10_trig else f'g10-eei-{number-1:02}' if grade10_eei else f'g10-algebra-{number-1:02}' if grade10 else f'g9-tg-{number-1:02}' if transform else f'g9-sv-{number-1:02}' if surface else f'g9-solid-{number-1:02}' if solids else f'g9-prob-{number-1:02}' if probability else f'g9-data-{number-1:02}' if handling else f'g9-area-{number-1:02}' if area else f'g9-shapes-{number-1:02}' if shapes else f'g9-straight-lines-{number-1:02}' if lines else f'g9-graphs-{number-1:02}' if graphs else f'g9-equations-{number-1:02}' if equations else f'g9-expressions-{number-1:02}' if expressions else f'g9-functions-{number-1:02}' if functions else f'g9-patterns-{number-1:02}' if patterns else f'g9-{topic}-{number-1:02}'],difficulty='foundation' if number==1 else 'standard',
        access_level=AccessLevel.FREE if number==1 else AccessLevel.PREMIUM,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,release_approved=False,
        blocks=[LessonBlock(type='concept',title=title,content='Read the original givens and predict the next mathematical action.'),
            questions[0].whiteboard,
            LessonBlock(type='mistake',title='First error to avoid',content='Check the exact expression and the chosen mathematical rule.'),
            LessonBlock(type='practice',title='Work in your book, then choose',content='Choose one of four answers after working independently.',data={'practice_bank_id':lesson_id}),
            LessonBlock(type='summary',title='Check the original',content='Verify the result against the question, including units.')],
        whiteboard_questions=questions,mastery_threshold=.8,paper=('Paper 2' if grade10_euc or grade10_trig else 'Paper 1') if grade10 else None,source_document=source.name,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),assessment_contract={
            'worked_example_count':15,'practice_count':15,'mastery_question_count':5,
            'parallel_reassessment_count':3,'answer_hidden_before_submission':True,
            'progression_threshold':.8,'runtime_conversion':'grade9_teacher_review_required'})
    return lesson,data

LESSON_1,DATA_1=build_lesson(1)
LESSON_2,DATA_2=build_lesson(2)
EXTENDED={number:build_lesson(number) for number in range(3,9)}
INTEGER_LESSONS={number:build_lesson(number,'integers') for number in range(1,6)}
EXPONENT_LESSONS={number:build_lesson(number,'exponents') for number in range(1,7)}
PATTERN_LESSONS={number:build_lesson(number,'numeric-geometric-patterns') for number in range(1,6)}
FUNCTION_LESSONS={number:build_lesson(number,'functions-relationships') for number in range(1,6)}
EXPRESSION_LESSONS={number:build_lesson(number,'algebraic-expressions') for number in range(1,10)}
EQUATION_LESSONS={number:build_lesson(number,'algebraic-equations') for number in range(1,7)}
GRAPH_LESSONS={number:build_lesson(number,'graphs') for number in range(1,8)}
LINE_LESSONS={number:build_lesson(number,'geometry-of-straight-lines') for number in range(1,6)}
SHAPE_LESSONS={number:build_lesson(number,'geometry-of-2d-shapes') for number in range(1,9)}
AREA_LESSONS={number:build_lesson(number,'area-and-perimeter') for number in range(1,6)}
DATA_LESSONS={number:build_lesson(number,'data-handling') for number in range(1,9)}
PROB_LESSONS={number:build_lesson(number,'probability') for number in range(1,6)}
SOLID_LESSONS={number:build_lesson(number,'geometry-of-3d-objects') for number in range(1,5)}
TRANSFORM_LESSONS={number:build_lesson(number,'transformation-geometry') for number in range(1,8)}
SURFACE_LESSONS={number:build_lesson(number,'surface-area-and-volume') for number in range(1,7)}

GRADE_9=GradeCurriculum(id='grade-9',grade=9,status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    topics=[Topic(id='whole-numbers',product_order=1,title='Whole Numbers',official_caps_topic='Whole numbers',
        caps_sequence=1,term=1,expected_duration='Eight authored lessons awaiting teacher and browser review',
        caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 1',paper=None,
        exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
        subtopics=[Subtopic(id='whole-numbers-learning-path',order=1,title='Properties, prime factors and applications',
            prerequisites=[],lessons=[LESSON_1,LESSON_2,*[EXTENDED[n][0] for n in range(3,9)]])]),
        Topic(id='integers',product_order=2,title='Integers',official_caps_topic='Integers',
            caps_sequence=2,term=1,expected_duration='Five authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 1',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='integers-learning-path',order=1,title='Signed operations, properties, powers and contexts',
                prerequisites=[],lessons=[INTEGER_LESSONS[n][0] for n in range(1,6)])]),
        Topic(id='exponents',product_order=3,title='Exponents',official_caps_topic='Exponents',
            caps_sequence=3,term=1,expected_duration='Six authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 1',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='exponents-learning-path',order=1,title='Powers, laws and scientific notation',
                prerequisites=[],lessons=[EXPONENT_LESSONS[n][0] for n in range(1,7)])]),
        Topic(id='numeric-geometric-patterns',product_order=4,title='Numeric and Geometric Patterns',official_caps_topic='Numeric and geometric patterns',
            caps_sequence=4,term=1,expected_duration='Five authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 1',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='patterns-learning-path',order=1,title='Figures, tables, general rules and justification',
                prerequisites=[],lessons=[PATTERN_LESSONS[n][0] for n in range(1,6)])]),
        Topic(id='functions-relationships',product_order=5,title='Functions and Relationships',official_caps_topic='Functions and relationships',
            caps_sequence=5,term=1,expected_duration='Five authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 1',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='functions-learning-path',order=1,title='Flows, tables, formulae, graphs and equivalence',
                prerequisites=[],lessons=[FUNCTION_LESSONS[n][0] for n in range(1,6)])]),
        Topic(id='algebraic-expressions',product_order=6,title='Algebraic Expressions',official_caps_topic='Algebraic expressions',
            caps_sequence=6,term=1,expected_duration='Nine authored lessons across Terms 1–2 awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Terms 1–2',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='expressions-learning-path',order=1,title='Terms, products, factorisation and algebraic fractions',
                prerequisites=[],lessons=[EXPRESSION_LESSONS[n][0] for n in range(1,10)])]),
        Topic(id='algebraic-equations',product_order=7,title='Algebraic Equations',official_caps_topic='Algebraic equations',
            caps_sequence=7,term=2,expected_duration='Six authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 2',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='equations-learning-path',order=1,title='Situations, inverses, factorisation and substitution',
                prerequisites=[],lessons=[EQUATION_LESSONS[n][0] for n in range(1,7)])]),
        Topic(id='graphs',product_order=8,title='Graphs',official_caps_topic='Graphs',
            caps_sequence=8,term=2,expected_duration='Seven authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 2',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='graphs-learning-path',order=1,title='Global features, coordinate plotting and straight lines',
                prerequisites=[],lessons=[GRAPH_LESSONS[n][0] for n in range(1,8)])]),
        Topic(id='geometry-of-straight-lines',product_order=9,title='Geometry of Straight Lines',official_caps_topic='Geometry of straight lines',
            caps_sequence=9,term=2,expected_duration='Five authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 2',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='straight-lines-learning-path',order=1,title='Intersecting, parallel and perpendicular line angle reasoning',
                prerequisites=[],lessons=[LINE_LESSONS[n][0] for n in range(1,6)])]),
        Topic(id='geometry-of-2d-shapes',product_order=10,title='Geometry of 2D Shapes',official_caps_topic='Geometry of 2D shapes',
            caps_sequence=10,term=3,expected_duration='Eight authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 3',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='shapes-learning-path',order=1,title='Triangles, polygons, congruency and similarity',
                prerequisites=[],lessons=[SHAPE_LESSONS[n][0] for n in range(1,9)])]),
        Topic(id='area-and-perimeter',product_order=11,title='Area and Perimeter',official_caps_topic='Area and perimeter',
            caps_sequence=11,term=3,expected_duration='Five authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 3',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='area-learning-path',order=1,title='Polygon and circle measures, units, scaling and applications',
                prerequisites=[],lessons=[AREA_LESSONS[n][0] for n in range(1,6)])]),
        Topic(id='data-handling',product_order=12,title='Data Handling',official_caps_topic='Data handling',
            caps_sequence=12,term=3,expected_duration='Eight authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 3',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='data-learning-path',order=1,title='Collect, organise, represent and critically interpret data',
                prerequisites=[],lessons=[DATA_LESSONS[n][0] for n in range(1,9)])]),
        Topic(id='probability',product_order=13,title='Probability',official_caps_topic='Probability',
            caps_sequence=13,term=3,expected_duration='Five authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 3',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='probability-learning-path',order=1,title='Sample spaces, tables, trees and relative frequency',
                prerequisites=[],lessons=[PROB_LESSONS[n][0] for n in range(1,6)])]),
        Topic(id='geometry-of-3d-objects',product_order=14,title='Geometry of 3D Objects',official_caps_topic='Geometry of 3-D objects',
            caps_sequence=14,term=4,expected_duration='Four authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 4',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='solids-learning-path',order=1,title='Platonic solids, curved surfaces and folding nets',
                prerequisites=[],lessons=[SOLID_LESSONS[n][0] for n in range(1,5)])]),
        Topic(id='surface-area-and-volume',product_order=15,title='Surface Area and Volume',official_caps_topic='Surface area and volume of 3-D objects',
            caps_sequence=15,term=4,expected_duration='Six authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 4',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='measurement-learning-path',order=1,title='Prism and cylinder surface area, volume and capacity',
                prerequisites=[],lessons=[SURFACE_LESSONS[n][0] for n in range(1,7)])]),
        Topic(id='transformation-geometry',product_order=16,title='Transformation Geometry',official_caps_topic='Transformation geometry',
            caps_sequence=16,term=4,expected_duration='Seven authored lessons awaiting teacher and browser review',
            caps_reference='DBE 2026 Grade 9 Mathematics ATP, Term 4',paper=None,
            exam_relevance='Grade 9 classroom and formal assessment',status=ContentStatus.TEACHER_REVIEW_REQUIRED,
            subtopics=[Subtopic(id='transformation-learning-path',order=1,title='Translation, reflection, rotation, enlargement and first-error repair',
                prerequisites=[],lessons=[TRANSFORM_LESSONS[n][0] for n in range(1,8)])])])
