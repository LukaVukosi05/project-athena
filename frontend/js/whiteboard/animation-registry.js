class WhiteboardAnimationRegistry {
  constructor() { this.renderers = new Map(); }
  register(operation, renderer) {
    if (this.renderers.has(operation)) throw new Error(`Duplicate whiteboard operation: ${operation}`);
    this.renderers.set(operation, renderer);
  }
  resolve(operation) {
    const renderer = this.renderers.get(operation);
    if (!renderer) throw new Error(`Unsupported whiteboard operation: ${operation}`);
    return renderer;
  }
}

const AthenaWhiteboardRegistry = new WhiteboardAnimationRegistry();

function operationMarkup(step) {
  const value = escapeWhiteboardHtml(step.operation.value ?? "");
  if (step.operation.type === "subtract_both_sides") return `<div class="equation-operation"><span>− ${value}</span><span>− ${value}</span></div><div class="cancellation-label">+${value} − ${value} = 0</div>`;
  if (step.operation.type === "divide_both_sides") return `<div class="equation-operation fraction-operation"><span>÷ ${value}</span><span>÷ ${value}</span></div><div class="cancellation-label">${value} ÷ ${value} = 1</div>`;
  return "";
}

function registerEquationOperation(operation) {
  AthenaWhiteboardRegistry.register(operation, { render(step, phase, context = {}) {
    const history = context.history || [];
    const workingExpression = step.working_expression || step.before_expression;
    const showResult = history[history.length - 1] !== step.after_expression;
    const keepWorking = workingExpression !== history[history.length - 1] && workingExpression !== step.after_expression;
    return `<div class="equation-state ${phase === "result" ? "show-result" : "show-operation"}">${renderMathHistory(history)}
      ${phase === "operation" ? `${renderMathExpression(workingExpression, "working")}${operationMarkup(step)}` : ""}
      ${phase === "result" && keepWorking ? renderMathExpression(workingExpression, "history") : ""}
      ${phase === "result" && showResult ? renderMathExpression(step.after_expression, "result") : ""}</div>`;
  }});
}

["identify_objective", "subtract_both_sides", "divide_both_sides", "substitute_value", "equivalent_transform"].forEach(registerEquationOperation);

AthenaWhiteboardRegistry.register("present_expression", { render(step) {
  return `<div class="equation-state identity-state"><p class="math-prompt">Simplify:</p>${renderMathExpression(step.before_expression, "working")}</div>`;
}});
AthenaWhiteboardRegistry.register("identity_recognition", { render(step, phase, context = {}) {
  return `<div class="equation-state identity-state">${renderMathHistory(context.history || [])}<div class="identity-highlight">${renderMathExpression(step.before_expression, "working")}</div>${renderMathExpression(step.operation.value, "result")}</div>`;
}});
AthenaWhiteboardRegistry.register("state_simplified_result", { render(step, phase, context = {}) {
  return `<div class="equation-state">${renderMathHistory(context.history || [])}${renderMathExpression(phase === "result" ? step.after_expression : step.working_expression, phase === "result" ? "result" : "working")}</div>`;
}});

function registerTeachingOperation(operation) {
  AthenaWhiteboardRegistry.register(operation, { render(step, phase, context = {}) {
    const history = context.history || [];
    const workingExpression = step.working_expression || step.before_expression;
    const result = history[history.length - 1] === step.after_expression ? "" : renderMathExpression(step.after_expression, "result");
    const keepWorking = workingExpression !== history[history.length - 1] && workingExpression !== step.after_expression;
    return `<div class="teaching-transition ${phase}">${renderMathHistory(history)}${phase === "operation" ? renderMathExpression(workingExpression, "working") : `${keepWorking ? renderMathExpression(workingExpression, "history") : ""}${result}`}</div>`;
  }});
}

["identify_interval", "substitute_function_value", "calculate_average_rate", "interpret_rate", "read_problem", "select_method", "show_working", "verify_result"].forEach(registerTeachingOperation);

["build_geometry_scene", "highlight_geometry", "apply_geometry_theorem", "solve_geometry", "complete_geometry"].forEach(operation => AthenaWhiteboardRegistry.register(operation, { render(step, phase) {
  if (step.before_expression === step.after_expression) return "";
  return `<div class="geometry-mathematics">${renderMathExpression(phase === "operation" ? step.working_expression || step.before_expression : step.after_expression, phase === "operation" ? "working" : "result")}</div>`;
}}));

function calculusGraph(step, phase, context = {}) {
  const approaching = step.operation.type === "approach_limit";
  const tangent = step.operation.type === "draw_tangent";
  const legacyGraph = context.hasVisualization ? "" : `<svg viewBox="0 0 420 230" role="presentation" aria-hidden="true">
    <line x1="45" y1="195" x2="395" y2="195" class="axis"/><line x1="70" y1="215" x2="70" y2="20" class="axis"/>
    <path d="M70 195 Q190 190 330 35" class="curve"/><circle cx="190" cy="142" r="6" class="point"/><text x="175" y="132">P</text>
    <circle cx="${approaching ? 220 : 285}" cy="${approaching ? 120 : 72}" r="6" class="point second-point"/><text x="${approaching ? 226 : 291}" y="${approaching ? 114 : 66}">Q</text>
    <line x1="160" y1="165" x2="320" y2="45" class="${tangent ? "tangent" : "secant"}"/>${approaching ? '<path d="M275 82 Q250 95 225 112" class="approach-arrow"/><text x="250" y="110">h → 0</text>' : ""}
  </svg>`;
  return `<div class="calculus-transition">${renderMathHistory(context.history || [])}${legacyGraph}${phase === "operation" ? renderMathExpression(step.working_expression || step.before_expression, "working") : renderMathExpression(step.after_expression, "result")}</div>`;
}

["draw_secant", "calculate_secant_gradient", "approach_limit", "draw_tangent"].forEach(operation => AthenaWhiteboardRegistry.register(operation, { render: calculusGraph }));

function renderMathHistory(expressions) {
  return `<div class="math-history">${expressions.map(expression => renderMathExpression(expression, "history")).join("")}</div>`;
}

function renderMathExpression(value, state) {
  const lines = String(value).split(/;\s*/).filter(Boolean);
  return `<div class="math-expression math-expression--${state}">${lines.map(line => {
    const fractions = line.match(/^(.+?)\s*\/\s*(.+?)\s*=\s*(.+?)\s*\/\s*(.+)$/);
    if (fractions) return `<div class="math-line"><span class="math-fraction"><span>${escapeWhiteboardHtml(fractions[1])}</span><span>${escapeWhiteboardHtml(fractions[2])}</span></span><span class="math-equals">=</span><span class="math-fraction"><span>${escapeWhiteboardHtml(fractions[3])}</span><span>${escapeWhiteboardHtml(fractions[4])}</span></span></div>`;
    return `<div class="math-line">${escapeWhiteboardHtml(line)}</div>`;
  }).join("")}</div>`;
}

function escapeWhiteboardHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}

function renderGraphSpec(spec, step, phase) {
  const traces = (spec.data || []).filter(trace => ["scatter", "scattergl"].includes(trace.type || "scatter"));
  const values = traces.flatMap(trace => (trace.x || []).map((x, index) => [Number(x), Number((trace.y || [])[index])]));
  if (!values.length || values.some(pair => pair.some(value => !Number.isFinite(value)))) return "";
  const xs = values.map(pair => pair[0]), ys = values.map(pair => pair[1]);
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const sx = value => 42 + ((value - minX) / (maxX - minX || 1)) * 336;
  const sy = value => 198 - ((value - minY) / (maxY - minY || 1)) * 160;
  const drawings = traces.map(trace => {
    const pairs = (trace.x || []).map((x, index) => [Number(x), Number(trace.y[index])]);
    if (String(trace.mode || "").includes("lines")) return `<polyline class="generated-graph__curve ${phase}" points="${pairs.map(pair => `${sx(pair[0])},${sy(pair[1])}`).join(" ")}"/>`;
    return pairs.map((pair, index) => `<g><circle class="generated-graph__point" cx="${sx(pair[0])}" cy="${sy(pair[1])}" r="5"/><text x="${sx(pair[0]) + 7}" y="${sy(pair[1]) - 7}">${escapeWhiteboardHtml((trace.text || [])[index] || "")}</text></g>`).join("");
  }).join("");
  const title = spec.layout?.title?.text || "Mathematical graph";
  return `<figure class="generated-graph"><svg viewBox="0 0 420 220" role="img" aria-label="${escapeWhiteboardHtml(title)}"><line x1="42" y1="198" x2="390" y2="198" class="axis"/><line x1="42" y1="205" x2="42" y2="20" class="axis"/>${drawings}</svg><figcaption>${escapeWhiteboardHtml(title)}</figcaption></figure>`;
}
