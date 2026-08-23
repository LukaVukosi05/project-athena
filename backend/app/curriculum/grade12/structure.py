"""Complete Grade 12 product hierarchy; lesson prose is seeded separately."""

from app.curriculum.grade12.lessons.linear_equations import LINEAR_EQUATIONS
from app.curriculum.grade12.lessons.calculus_foundations import AVERAGE_RATE, SECANT_TO_TANGENT
from app.curriculum.grade12.lessons.paper2_practice import PAPER2_PRACTICE
from app.curriculum.schemas import ContentStatus, GradeCurriculum, Subtopic, Topic


MODULES = [
    ("algebra-readiness", "Algebra Foundations / Readiness", None, "Readiness", ["Algebraic language", "Algebraic manipulation", "Exponent laws", "Surds", "Factorisation revision", "Equations", "Inequalities", "Algebraic fractions", "Readiness assessment"]),
    ("sequences-series", "Patterns, Sequences and Series", 1, "Paper 1", ["Number patterns revision", "Arithmetic sequences", "Arithmetic series", "Geometric sequences", "Geometric series", "Infinite geometric series", "Sigma notation", "Mixed problems", "Exam-style questions"]),
    ("functions-inverses", "Functions and Inverses", 1, "Paper 1", ["Function fundamentals", "One-to-one functions", "Many-to-one functions", "Restricting a domain", "Inverse functions", "Finding inverses algebraically", "Function and inverse graphs", "Linear inverses", "Quadratic inverses", "Exponential inverses", "Domain and range relationships", "Graph interpretation", "Exam questions"]),
    ("exponential-logarithmic", "Exponential and Logarithmic Functions", 1, "Paper 1", ["Exponential revision", "Exponential laws", "Exponential graphs", "Meaning of a logarithm", "Exponential and logarithmic form", "Logarithmic functions", "Logarithmic graphs", "Inverse relationship", "Logarithmic laws", "Exponential equations", "Domain, range and asymptotes", "Exam questions"]),
    ("finance", "Finance, Growth and Decay", 1, "Paper 1", ["Growth revision", "Compound interest", "Depreciation", "Effective and nominal rates", "Future value", "Present value", "Annuities", "Future-value annuities", "Present-value annuities", "Loans", "Outstanding balances", "Sinking funds", "Solving for time", "Timelines", "Comparing options", "Exam questions"]),
    ("trigonometry", "Trigonometry", 1, "Paper 2", ["Diagnostic revision", "Compound angles", "Double-angle identities", "Deriving identities", "Simplifying expressions", "Proving identities", "Trigonometric equations", "General solutions", "Sine rule", "Cosine rule", "Area rule", "Two-dimensional problems", "Three-dimensional problems", "Elevation and depression", "Exam questions"]),
    ("polynomials", "Polynomials", 2, "Paper 1", ["Polynomial vocabulary", "Division and remainder intuition", "Remainder Theorem", "Factor Theorem", "Unknown coefficients", "Factorising cubics", "Solving cubics", "Factors and intercepts", "Exam questions"]),
    ("differential-calculus", "Differential Calculus", 2, "Paper 1", ["Rate of change", "Average gradient", "Secant lines", "Secant to tangent", "Intuitive limits", "First principles", "Derivative notation", "First-principles differentiation", "Power rule", "Constant rule", "Sum and difference rule", "Tangents", "Tangent equations", "Stationary points", "Local extrema", "Second derivative", "Concavity", "Points of inflection", "Cubic sketching", "Optimisation", "Rate applications", "Motion", "Exam questions"]),
    ("analytical-geometry", "Analytical Geometry", 2, "Paper 2", ["Distance", "Midpoint", "Gradient", "Straight lines", "Parallel lines", "Perpendicular lines", "Inclination", "Circle equation", "Centre and radius", "Circle conditions", "Circle tangents", "Radius and tangent", "Tangent equation", "Intersections", "Complex problems", "Exam questions"]),
    ("euclidean-geometry", "Euclidean Geometry", 3, "Paper 2", ["Proof language", "Similar polygons", "Similar triangles", "Proportionality theorem", "Converse proportionality", "Midpoint theorem", "Pythagorean revision", "Circle theorems", "Proof construction", "Choosing the theorem", "Multi-step proofs", "Exam riders", "Integrated problems", "Exam questions"]),
    ("statistics", "Statistics", 3, "Paper 2", ["Data types", "Central tendency", "Measures of spread", "Five-number summary", "Box plots", "Outliers", "Standard deviation", "Variance", "Scatter plots", "Correlation", "Regression", "Least-squares line", "Interpolation", "Extrapolation", "Interpreting correlation", "Distribution shape", "Data interpretation", "Exam questions"]),
    ("counting-probability", "Counting and Probability", 3, "Paper 1", ["Probability revision", "Sample spaces", "Venn diagrams", "Tree diagrams", "Mutually exclusive events", "Complements", "Independent events", "Dependent events", "Addition rules", "Multiplication rules", "Conditional reasoning", "Fundamental counting principle", "Arrangements", "Probability using counting", "At least one", "Complex problems", "Exam questions"]),
    ("paper-1-preparation", "Paper 1 Exam Preparation", 4, "Paper 1", ["Topic practice", "Mixed practice", "Timed practice", "Past-paper questions", "Error diagnosis"]),
    ("paper-2-preparation", "Paper 2 Exam Preparation", 4, "Paper 2", ["Topic practice", "Mixed practice", "Timed practice", "Past-paper questions", "Error diagnosis"]),
    ("final-readiness", "Final Revision / Exam Readiness", 4, "Both", ["Diagnostic assessment", "Weak-topic identification", "Personalised revision", "Paper 1 simulation", "Paper 2 simulation", "Readiness score", "Final recommendations"]),
]


def make_subtopics(module_id: str, titles: list[str]) -> list[Subtopic]:
    result = []
    if module_id in PAPER2_PRACTICE:
        result.append(Subtopic(id=f"{module_id}-learning-path", order=1,
            title="Start here — complete learning path",
            lessons=PAPER2_PRACTICE[module_id]))
    offset = 1 if module_id in PAPER2_PRACTICE else 0
    for order, title in enumerate(titles, 1):
        lessons = [LINEAR_EQUATIONS] if module_id == "algebra-readiness" and title == "Equations" else []
        if module_id == "differential-calculus" and title == "Rate of change":
            lessons = [AVERAGE_RATE]
        elif module_id == "differential-calculus" and title == "Average gradient":
            lessons = [SECANT_TO_TANGENT]
        result.append(Subtopic(id=f"{module_id}-{order}", order=order + offset, title=title, lessons=lessons))
    return result


GRADE_12 = GradeCurriculum(id="grade-12", grade=12,
    status=ContentStatus.TEACHER_REVIEW_REQUIRED,
    topics=[Topic(id=module_id, product_order=order, title=title,
        official_caps_topic=None if order == 0 else title,
        caps_sequence=None, term=term, paper=paper,
        caps_reference=None, exam_relevance=None,
        status=ContentStatus.TEACHER_REVIEW_REQUIRED,
        subtopics=make_subtopics(module_id, subtopics))
        for order, (module_id, title, term, paper, subtopics) in enumerate(MODULES)])
