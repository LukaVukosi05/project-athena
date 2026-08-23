/* ============================================================
   CURRICULUM DATA (Phase 1 mock)
   ------------------------------------------------------------
   Per the brief: "The curriculum database must not hard-code
   topics into frontend components. Curriculum must be stored
   as data." This file is that boundary for Phase 1 — it is a
   plain JS object standing in for what will become a
   PostgreSQL-backed API response (see
   backend/app/api/v1/curriculum.py). No page should ever
   hard-code a lesson title or topic name; everything reads
   from CURRICULUM via CurriculumAPI below.

   Only a representative slice is authored here (Grade 10 —
   Equations & Inequalities, Grade 12 — Differential Calculus)
   to keep Phase 1 usable end-to-end. The full Grade 8–12
   catalogue is a curriculum-team task and must be validated
   against current DBE CAPS documents before publication.
   ============================================================ */

const CURRICULUM = {
  grades: [
    {
      id: "grade-10",
      label: "Grade 10",
      terms: [
        { label: "Term 1", progress: 1 },
        { label: "Term 2", progress: 0.6 },
        { label: "Term 3", progress: 0.1 },
        { label: "Term 4", progress: 0 }
      ],
      topics: [
        {
          id: "eq-and-inequalities",
          title: "Equations and Inequalities",
          capsRef: "CAPS Grade 10, Topic 3",
          difficulty: "Core",
          whatYoullLearn: [
            "Solving linear equations",
            "Applying an operation to both sides",
            "Solving linear inequalities",
            "Word problems as equations"
          ],
          lessons: [
            {
              id: "l1-intro-linear-equations",
              title: "Introduction to linear equations",
              summary: "What an equation means, and why both sides must stay equal.",
              explainer: "An equation is a balance. Whatever you do to one side, you must do to the other — otherwise the balance breaks and the statement is no longer true.",
              free: true,
              animation: {
                template: "linear_equation_balance",
                title: "Solving 2x + 5 = 15",
                steps: [
                  { op: "show", expression: "2x + 5 = 15", narration: "We start with the equation as given." },
                  { op: "subtract_both_sides", value: 5, before: "2x + 5 = 15", after: "2x = 10", narration: "Subtract 5 from both sides to isolate the term with x." },
                  { op: "divide_both_sides", value: 2, before: "2x = 10", after: "x = 5", narration: "Divide both sides by 2 to leave x on its own." },
                  { op: "substitute", value: "x = 5", before: "2(5) + 5", after: "10 + 5 = 15", narration: "Check the answer by substituting x = 5 back into the original equation." }
                ]
              },
              quiz: {
                passMark: 0.7,
                questions: [
                  { q: "To go from 2x + 5 = 15 to 2x = 10, what operation was applied to both sides?", options: ["Multiplied by 2", "Subtracted 5", "Added 5", "Divided by 5"], correctIndex: 1, explanation: "Subtracting 5 from both sides removes the constant term from the left side." },
                  { q: "After 2x = 10, what is the next correct step?", options: ["Subtract 2 from both sides", "Divide both sides by 2", "Add 10 to both sides", "Square both sides"], correctIndex: 1, explanation: "Dividing both sides by the coefficient of x isolates x." },
                  { q: "Why must an operation be applied to BOTH sides of an equation?", options: ["It makes the numbers smaller", "It keeps the equation balanced and true", "It is only a convention, not a requirement", "It only matters for inequalities"], correctIndex: 1, explanation: "An equation states two sides are equal — any operation must preserve that equality." }
                ]
              }
            },
            {
              id: "l2-inequalities-intro",
              title: "Solving linear inequalities",
              summary: "How inequalities behave like equations — with one important exception.",
              explainer: "Inequalities follow the same rules as equations, except: multiplying or dividing by a negative number flips the inequality sign.",
              free: true,
              animation: {
                template: "linear_equation_balance",
                title: "Solving -2x + 4 > 10",
                steps: [
                  { op: "show", expression: "-2x + 4 > 10", narration: "We start with the inequality as given." },
                  { op: "subtract_both_sides", value: 4, before: "-2x + 4 > 10", after: "-2x > 6", narration: "Subtract 4 from both sides." },
                  { op: "divide_both_sides", value: -2, flipSign: true, before: "-2x > 6", after: "x < -3", narration: "Divide both sides by -2 — because we divided by a negative number, the inequality sign flips." }
                ]
              },
              quiz: {
                passMark: 0.7,
                questions: [
                  { q: "When solving an inequality, when must you flip the inequality sign?", options: ["When you add a positive number", "When you multiply or divide by a negative number", "Whenever x is negative", "Never — inequalities never flip"], correctIndex: 1, explanation: "Multiplying or dividing both sides by a negative number reverses the direction of the inequality." },
                  { q: "Solve: -2x + 4 > 10", options: ["x > -3", "x < -3", "x < 3", "x > 3"], correctIndex: 1, explanation: "Subtract 4: -2x > 6. Divide by -2 and flip the sign: x < -3." }
                ]
              }
            },
            {
              id: "l3-word-problems",
              title: "Equations from word problems",
              summary: "Translating a real-world scenario into an equation before solving it.",
              explainer: "The hardest part is usually not the algebra — it's correctly naming the unknown and writing the sentence as an equation.",
              free: false,
              animation: {
                template: "linear_equation_balance",
                title: "Thabo is 3 years older than twice his sister's age",
                steps: [
                  { op: "show", expression: "T = 2S + 3", narration: "Let S be the sister's age. Thabo's age T is 3 more than twice S." },
                  { op: "substitute", value: "S = 9", before: "T = 2(9) + 3", after: "T = 21", narration: "If the sister is 9, substitute to find Thabo's age." }
                ]
              },
              quiz: {
                passMark: 0.7,
                questions: [
                  { q: "A number increased by 7 gives 20. Which equation represents this?", options: ["x - 7 = 20", "x + 7 = 20", "7x = 20", "x/7 = 20"], correctIndex: 1, explanation: "\"Increased by 7\" means we add 7 to the unknown number." }
                ]
              }
            },
            {
              id: "l2-first-principles",
              title: "Differentiation from first principles",
              summary: "Build the derivative formula step by step using a limit.",
              explainer: "First principles turns the gradient between two nearby points into the exact tangent gradient by letting the horizontal gap h approach zero.",
              free: true,
              animation: {
                template: "linear_equation_balance",
                title: "Differentiate f(x) = x² + 3x from first principles",
                steps: [
                  { op: "show", expression: "f′(x) = lim h→0 [f(x+h)−f(x)]/h", explanation: "Begin with the first-principles definition. The quotient measures the gradient between inputs x and x+h.", narration: "Begin with the first-principles definition." },
                  { op: "show", expression: "f(x+h) = x²+2xh+h²+3x+3h", explanation: "Replace x with x+h, then expand both the square and the linear term completely.", narration: "Substitute x+h and expand every bracket." },
                  { op: "show", expression: "f(x+h)−f(x) = 2xh+h²+3h", explanation: "Subtract x²+3x. The matching x² and 3x terms cancel, leaving only terms containing h.", narration: "Subtract f(x) and cancel matching terms." },
                  { op: "show", expression: "(2xh+h²+3h)/h = 2x+h+3", explanation: "Factor h from the numerator and cancel it while h is non-zero.", narration: "Factor and cancel h." },
                  { op: "show", expression: "f′(x) = 2x+3", explanation: "Now let h approach zero. The remaining h term becomes zero.", narration: "Take the limit as h approaches zero." }
                ]
              },
              quiz: { passMark: 0.7, questions: [
                { q: "Why may h be cancelled before taking the limit?", options: ["h is always 1", "h approaches zero but is not zero in the quotient", "The numerator is zero", "Limits ignore denominators"], correctIndex: 1, explanation: "During simplification h is non-zero; only afterward do we examine what happens as h approaches zero." },
                { q: "What is the derivative of x²+3x?", options: ["x+3", "2x+3", "2x", "x²+3"], correctIndex: 1, explanation: "First principles simplifies to 2x+h+3, whose limit is 2x+3." }
              ] }
            },
            {
              id: "l3-differentiation-rules",
              title: "Rules of differentiation",
              summary: "Differentiate polynomial functions efficiently with the power rule.",
              explainer: "For each term axⁿ, multiply the coefficient by n and reduce the exponent by one. Constants differentiate to zero.",
              free: false,
              animation: {
                template: "linear_equation_balance",
                title: "Differentiate y = 4x⁵ − 3x² + 7",
                steps: [
                  { op: "show", expression: "d/dx(4x⁵) = 20x⁴", explanation: "Multiply 4 by the old exponent 5, then reduce the exponent from 5 to 4.", narration: "Differentiate the first term." },
                  { op: "show", expression: "d/dx(−3x²) = −6x", explanation: "Multiply −3 by 2 and reduce x² to x¹.", narration: "Differentiate the second term and preserve its sign." },
                  { op: "show", expression: "d/dx(7) = 0", explanation: "A constant has no change as x changes, so its derivative is zero.", narration: "Differentiate the constant." },
                  { op: "show", expression: "dy/dx = 20x⁴ − 6x", explanation: "Combine the derivatives of all three terms.", narration: "Combine the differentiated terms." }
                ]
              },
              quiz: { passMark: 0.7, questions: [
                { q: "Differentiate 3x⁴.", options: ["3x³", "12x³", "12x⁴", "4x³"], correctIndex: 1, explanation: "Multiply 3 by 4 and reduce the exponent to 3." },
                { q: "What is the derivative of a constant?", options: ["1", "The constant", "0", "x"], correctIndex: 2, explanation: "A constant does not change with x." }
              ] }
            },
            {
              id: "l4-tangent-lines",
              title: "Equations of tangent lines",
              summary: "Use a derivative to find the gradient and equation of a tangent.",
              explainer: "The original function supplies the point on the curve. Its derivative supplies the tangent gradient at that point.",
              free: false,
              animation: {
                template: "linear_equation_balance",
                title: "Tangent to f(x) = x² − 1 at x = 2",
                steps: [
                  { op: "show", expression: "f(2) = 2²−1 = 3, so P(2,3)", explanation: "Substitute x=2 into the original function to obtain a point on the tangent.", narration: "Find the point on the curve." },
                  { op: "show", expression: "f′(x) = 2x", explanation: "Differentiate x²−1: the derivative of x² is 2x and the constant becomes zero.", narration: "Find the gradient function." },
                  { op: "show", expression: "m = f′(2) = 4", explanation: "Evaluate the derivative at x=2 to get the tangent's gradient.", narration: "Calculate the tangent gradient." },
                  { op: "show", expression: "y−3 = 4(x−2)", explanation: "Insert P(2,3) and m=4 into the point-gradient form y−y₁=m(x−x₁).", narration: "Use point-gradient form." },
                  { op: "show", expression: "y = 4x−5", explanation: "Expand the right side and add 3 to isolate y.", narration: "Simplify the tangent equation." }
                ]
              },
              quiz: { passMark: 0.7, questions: [
                { q: "For a tangent at x=2, where does its gradient come from?", options: ["f(0)", "f(2)", "f′(2)", "The x-intercept"], correctIndex: 2, explanation: "The derivative evaluated at the point gives the tangent gradient." }
              ] }
            },
            {
              id: "l5-stationary-points",
              title: "Cubic graphs and stationary points",
              summary: "Find and classify turning points using first and second derivatives.",
              explainer: "At a stationary point f′(x)=0. The sign of f″(x) then identifies whether the graph is concave down (maximum) or concave up (minimum).",
              free: false,
              animation: {
                template: "linear_equation_balance",
                title: "Stationary points of f(x) = x³ − 3x",
                steps: [
                  { op: "show", expression: "f′(x) = 3x²−3", explanation: "Differentiate the cubic to obtain its gradient function.", narration: "Find the first derivative." },
                  { op: "show", expression: "3x²−3=0 ⇒ x=−1 or x=1", explanation: "Stationary points have zero gradient, so solve f′(x)=0 for both roots.", narration: "Find the stationary x-values." },
                  { op: "show", expression: "f(−1)=2 and f(1)=−2", explanation: "Substitute each x-value into the original function to obtain the coordinates.", narration: "Find both y-values." },
                  { op: "show", expression: "f″(x)=6x", explanation: "Differentiate f′(x) to measure how the gradient changes.", narration: "Find the second derivative." },
                  { op: "show", expression: "max (−1,2); min (1,−2)", explanation: "f″(−1)<0 means concave down and a maximum; f″(1)>0 means concave up and a minimum.", narration: "Classify both stationary points." }
                ]
              },
              quiz: { passMark: 0.7, questions: [
                { q: "What equation finds stationary x-values?", options: ["f(x)=0", "f′(x)=0", "f″(x)=0", "x=0"], correctIndex: 1, explanation: "A stationary point has zero first derivative." },
                { q: "If f″(a)>0 at a stationary point, what is it?", options: ["Local maximum", "Local minimum", "x-intercept", "Asymptote"], correctIndex: 1, explanation: "A positive second derivative means the graph is concave up, giving a local minimum." }
              ] }
            }
          ]
        }
      ]
    },
    {
      id: "grade-12",
      label: "Grade 12",
      terms: [
        { label: "Term 1", progress: 1 },
        { label: "Term 2", progress: 0.75 },
        { label: "Term 3", progress: 0.35 },
        { label: "Term 4", progress: 0 }
      ],
      topics: [
        {
          id: "differential-calculus",
          title: "Differential Calculus",
          capsRef: "CAPS Grade 12, Topic 5",
          difficulty: "Core",
          whatYoullLearn: ["Derivatives", "First principles", "Rules of differentiation", "Gradients and turning points"],
          lessons: [
            {
              id: "l1-gradient-intro",
              title: "Introduction to the derivative",
              summary: "The derivative as the gradient of a curve at a single point.",
              explainer: "The gradient tells us how quickly the function changes. At a curve, the gradient is different at every point — the derivative gives us a formula for that gradient.",
              free: true,
              animation: {
                template: "tangent_line",
                title: "Gradient of f(x) = x² at x = 2",
                steps: [
                  { op: "show", expression: "f(x) = x²", narration: "We start with the curve f(x) = x²." },
                  { op: "plot_point", value: "x = 2", narration: "Mark the point on the curve at x = 2." },
                  { op: "draw_tangent", value: "gradient = 4", narration: "Draw the tangent line at that point — its slope is the derivative, f'(2) = 4." }
                ]
              },
              quiz: {
                passMark: 0.7,
                questions: [
                  { q: "What does the derivative of a function represent at a given point?", options: ["The y-value at that point", "The gradient (rate of change) at that point", "The area under the curve", "The x-intercept"], correctIndex: 1, explanation: "The derivative gives the instantaneous rate of change — the gradient of the tangent line at that point." }
                ]
              }
            }
          ]
        }
      ]
    }
  ]
};

// Keep the Grade 12 pilot lessons grouped with Differential Calculus at runtime.
// This migration shim can be removed when the frontend switches fully to the
// backend curriculum endpoint.
{
  const grade10Topic = CURRICULUM.grades.find(g => g.id === "grade-10").topics
    .find(t => t.id === "eq-and-inequalities");
  const grade12Topic = CURRICULUM.grades.find(g => g.id === "grade-12").topics
    .find(t => t.id === "differential-calculus");
  const calculusIds = new Set([
    "l2-first-principles", "l3-differentiation-rules",
    "l4-tangent-lines", "l5-stationary-points"
  ]);
  const calculusLessons = grade10Topic.lessons.filter(item => calculusIds.has(item.id));
  grade10Topic.lessons = grade10Topic.lessons.filter(item => !calculusIds.has(item.id));
  grade12Topic.lessons.push(...calculusLessons);
}

const CurriculumAPI = {
  getGrade(gradeId) { return CURRICULUM.grades.find(g => g.id === gradeId) || null; },
  getTopic(gradeId, topicId) {
    const grade = this.getGrade(gradeId);
    return grade ? (grade.topics.find(t => t.id === topicId) || null) : null;
  },
  getLesson(gradeId, topicId, lessonId) {
    const topic = this.getTopic(gradeId, topicId);
    return topic ? (topic.lessons.find(l => l.id === lessonId) || null) : null;
  },
  getAllGrades() { return CURRICULUM.grades; }
};
