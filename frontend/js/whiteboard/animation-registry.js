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
      ${phase === "ready" ? "" : phase === "operation" ? `${renderMathExpression(workingExpression, "working")}${operationMarkup(step)}` : ""}
      ${phase === "result" && keepWorking ? renderMathExpression(workingExpression, "history") : ""}
      ${phase === "result" && showResult ? renderMathExpression(step.after_expression, "result") : ""}</div>`;
  }});
}

["identify_objective", "subtract_both_sides", "divide_both_sides", "substitute_value", "equivalent_transform", "apply_both_sides_display", "simplify_equation", "divide_both_sides_display", "verification_line"].forEach(registerEquationOperation);

function genericSemanticEquation(expression) {
  const equals=String(expression).indexOf("=");
  if(equals<0)return escapeWhiteboardHtml(expression);
  const renderSide=(source,side)=>{let cursor=0,constantSeen=false;const parts=[];const pattern=/([+-]?\d*x|[+-]\s*\d+|\/\s*\d+)/g;let match;
    while((match=pattern.exec(source))){parts.push(escapeWhiteboardHtml(source.slice(cursor,match.index)));const token=match[0];let id="";
      if(/x$/.test(token))id="variable-term";
      else if(/^\//.test(token))id=`divide-${side}`;
      else if(/[+-]/.test(token)){if(side==="left"&&!constantSeen){id="constant-term";constantSeen=true;}else id=`${token.trim().startsWith("+")?"add":"subtract"}-${side}`;}
      const content=id==="variable-term"?`<span data-object-id="coefficient">${escapeWhiteboardHtml(token.slice(0,-1)||"1")}</span>x`:escapeWhiteboardHtml(token);
      parts.push(`<span class="math-token"${id?` data-object-id="${id}"`:""}>${content}</span>`);cursor=pattern.lastIndex;}
    parts.push(escapeWhiteboardHtml(source.slice(cursor)));return parts.join("");};
  const left=expression.slice(0,equals).trim(),right=expression.slice(equals+1).trim();
  return `<span data-object-id="left-side">${renderSide(left,"left")}</span> <span data-object-id="equals">=</span> <span data-object-id="right-side">${renderSide(right,"right")}</span>`;
}

function semanticBalanceExpression(expression,state="current") {
  const escaped=escapeWhiteboardHtml(expression);
  const known={
    "3x + 7 = 22":'<span data-object-id="left-side"><span class="math-token variable-term" data-object-id="variable-term"><span data-object-id="coefficient">3</span>x</span> <span class="math-token" data-object-id="constant-term">+ 7</span></span> <span data-object-id="equals">=</span> <span data-object-id="right-side">22</span>',
    "3x + 7 - 7 = 22 - 7":'<span data-object-id="left-side"><span class="math-token variable-term" data-object-id="variable-term"><span data-object-id="coefficient">3</span>x</span> <span data-object-id="cancel-pair"><span data-object-id="constant-term">+ 7</span> <span data-object-id="subtract-left">- 7</span></span></span> <span data-object-id="equals">=</span> <span data-object-id="right-side">22 <span data-object-id="subtract-right">- 7</span></span>',
    "3x = 15":'<span data-object-id="left-side"><span class="math-token variable-term" data-object-id="variable-term"><span data-object-id="coefficient">3</span>x</span></span> <span data-object-id="equals">=</span> <span data-object-id="right-side">15</span>',
    "3x / 3 = 15 / 3":'<span data-object-id="left-side"><span class="math-token variable-term" data-object-id="variable-term"><span data-object-id="coefficient">3</span>x</span> <span data-object-id="divide-left">÷ 3</span></span> <span data-object-id="equals">=</span> <span data-object-id="right-side">15 <span data-object-id="divide-right">÷ 3</span></span>',
    "x = 5":'<span data-object-id="left-side">x</span> <span data-object-id="equals">=</span> <span data-object-id="right-side" data-object-id-result="answer">5</span>',
    "3(5) + 7 = 22":'<span data-object-id="verification">3(5) + 7</span> <span data-object-id="equals">=</span> <span data-object-id="right-side">22</span>',
    "15 + 7 = 22":'<span data-object-id="verification">15 + 7</span> <span data-object-id="equals">=</span> <span data-object-id="right-side">22</span>',
    "22 = 22 ✓":'<span data-object-id="verification">22</span> <span data-object-id="equals">=</span> <span data-object-id="right-side">22</span> <span class="verified-indicator" aria-label="Verified">✓ Verified</span>'
    ,"5x - 4 = 11":'<span data-object-id="left-side"><span class="math-token variable-term" data-object-id="variable-term"><span data-object-id="coefficient">5</span>x</span> <span data-object-id="constant-term">- 4</span></span> <span data-object-id="equals">=</span> <span data-object-id="right-side">11</span>'
    ,"5x - 4 + 4 = 11 + 4":'<span data-object-id="left-side"><span class="math-token variable-term" data-object-id="variable-term"><span data-object-id="coefficient">5</span>x</span> <span data-object-id="cancel-pair"><span data-object-id="constant-term">- 4</span> <span data-object-id="add-left">+ 4</span></span></span> <span data-object-id="equals">=</span> <span data-object-id="right-side">11 <span data-object-id="add-right">+ 4</span></span>'
    ,"5x = 15":'<span data-object-id="left-side"><span class="math-token variable-term" data-object-id="variable-term"><span data-object-id="coefficient">5</span>x</span></span> <span data-object-id="equals">=</span> <span data-object-id="right-side">15</span>'
    ,"5x / 5 = 15 / 5":'<span data-object-id="left-side"><span class="math-token variable-term" data-object-id="variable-term"><span data-object-id="coefficient">5</span>x</span> <span data-object-id="divide-left">÷ 5</span></span> <span data-object-id="equals">=</span> <span data-object-id="right-side">15 <span data-object-id="divide-right">÷ 5</span></span>'
    ,"x = 3":'<span data-object-id="left-side">x</span> <span data-object-id="equals">=</span> <span data-object-id="right-side">3</span>'
    ,"5(3) - 4 = 11":'<span data-object-id="verification">5(3) - 4</span> <span data-object-id="equals">=</span> <span data-object-id="right-side">11</span>'
    ,"15 - 4 = 11":'<span data-object-id="verification">15 - 4</span> <span data-object-id="equals">=</span> <span data-object-id="right-side">11</span>'
    ,"11 = 11 ✓":'<span data-object-id="verification">11</span> <span data-object-id="equals">=</span> <span data-object-id="right-side">11</span> <span class="verified-indicator" aria-label="Verified">✓ Verified</span>'
  };
  return `<div class="math-expression math-expression--${state}"><div class="math-line math-equation">${known[expression]||genericSemanticEquation(expression)}</div></div>`;
}

function renderSemanticBalance(step,phase,context={}) {
  const prior=(context.history||[]).filter(Boolean).slice(-1)[0];
  const active=phase==="ready"?step.before_expression:step.after_expression;
  const previous=prior&&prior!==active?semanticBalanceExpression(prior,"history"):"";
  return `<div class="equation-state semantic-balance ${phase}">${previous}${semanticBalanceExpression(active,phase==="ready"?"current":phase==="operation"?"working":"result")}</div>`;
}
["balance_focus_goal","balance_focus_constant","apply_both_sides_display","simplify_equation","divide_both_sides_display","verification_line"].forEach(operation=>AthenaWhiteboardRegistry.renderers.set(operation,{render:renderSemanticBalance}));

AthenaWhiteboardRegistry.register("present_expression", { render(step) {
  return `<div class="equation-state identity-state"><p class="math-prompt">Simplify:</p>${renderMathExpression(step.before_expression, "working")}</div>`;
}});
AthenaWhiteboardRegistry.register("identity_recognition", { render(step, phase, context = {}) {
  return `<div class="equation-state identity-state">${renderMathHistory(context.history || [])}<div class="identity-highlight">${renderMathExpression(step.before_expression, "working")}</div>${phase === "result" ? renderMathExpression(step.operation.value, "result") : ""}</div>`;
}});
AthenaWhiteboardRegistry.register("state_simplified_result", { render(step, phase, context = {}) {
  return `<div class="equation-state">${renderMathHistory(context.history || [])}${renderMathExpression(phase === "result" ? step.after_expression : step.working_expression, phase === "result" ? "result" : "working")}</div>`;
}});

function registerTeachingOperation(operation) {
  AthenaWhiteboardRegistry.register(operation, { render(step, phase, context = {}) {
    if (context.hasVisualization) return "";
    const history = context.history || [];
    const workingExpression = step.working_expression || step.before_expression;
    const result = history[history.length - 1] === step.after_expression ? "" : renderMathExpression(step.after_expression, "result");
    const keepWorking = workingExpression !== history[history.length - 1] && workingExpression !== step.after_expression;
    return `<div class="teaching-transition ${phase}">${renderMathHistory(history)}${phase === "ready" ? "" : phase === "operation" ? renderMathExpression(workingExpression, "working") : `${keepWorking ? renderMathExpression(workingExpression, "history") : ""}${result}`}</div>`;
  }});
}

["equality_balance","additive_inverse","multiplicative_inverse","two_step_balance","variables_both_sides","context_to_equation","distributive_equation"].forEach(template=>registerTeachingOperation(`${template}_step`));

["identify_interval", "substitute_function_value", "calculate_average_rate", "interpret_rate", "read_problem", "select_method", "show_working", "verify_result"].forEach(registerTeachingOperation);

["timeline_orient", "timeline_inspect", "timeline_select", "timeline_verify", "timeline_summarize"].forEach(operation => AthenaWhiteboardRegistry.register(operation, { render(step, phase, context={}) { return context.hasVisualization ? "" : `${renderMathHistory(context.history||[])}${renderMathExpression(phase==="operation"?(step.working_expression||step.before_expression):step.after_expression,phase==="operation"?"working":"result")}`; } }));

["place_cashflow", "set_focal_date", "match_rate_period", "accumulate", "discount", "calculate", "verify_financial_sense", "label_period", "count_payments", "split_phase", "mark_payment", "highlight_remaining_payments", "compare_options"].forEach(operation => AthenaWhiteboardRegistry.register(operation, { render() { return ""; } }));

["build_geometry_scene", "highlight_geometry", "apply_geometry_theorem", "solve_geometry", "complete_geometry"].forEach(operation => AthenaWhiteboardRegistry.register(operation, { render(step, phase) {
  if (step.before_expression === step.after_expression) return "";
  return `<div class="geometry-mathematics">${phase === "ready" ? "" : renderMathExpression(phase === "operation" ? step.working_expression || step.before_expression : step.after_expression, phase === "operation" ? "working" : "result")}</div>`;
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
  return `<div class="calculus-transition">${renderMathHistory(context.history || [])}${legacyGraph}${phase === "ready" ? "" : phase === "operation" ? renderMathExpression(step.working_expression || step.before_expression, "working") : renderMathExpression(step.after_expression, "result")}</div>`;
}

["draw_secant", "calculate_secant_gradient", "approach_limit", "draw_tangent"].forEach(operation => AthenaWhiteboardRegistry.register(operation, { render: calculusGraph }));

["plot_function", "place_curve_point", "show_change_triangle", "move_point", "differentiate_term", "substitute_derivative_value", "solve_derivative_zero", "test_derivative_sign", "classify_stationary", "shade_concavity", "mark_inflection", "build_objective", "mark_feasible_domain", "compare_boundaries", "verify_calculus_sense", "factor_common", "substitute", "cancel", "calculus_limit", "calculus_tangent"].forEach(operation => {
  if (!AthenaWhiteboardRegistry.renderers.has(operation)) AthenaWhiteboardRegistry.register(operation, { render: calculusGraph });
});

["algebra_orient", "algebra_inspect", "algebra_select", "algebra_transform", "algebra_validate", "algebra_verify", "algebra_summarize"].forEach(operation => AthenaWhiteboardRegistry.register(operation, { render(step, phase, context={}) {
  const history=phase==="ready"&&context.hasVisualization?"":renderMathHistory(context.history||[]);
  return `<div class="algebra-transition ${phase}">${history}${phase==="ready"?"":renderMathExpression(phase==="operation"?(step.working_expression||step.before_expression):step.after_expression,phase==="operation"?"working":"result")}</div>`;
}}));

function renderMathHistory(expressions) {
  return `<div class="math-history">${expressions.map(expression => renderMathExpression(expression, "history")).join("")}</div>`;
}

function renderMathExpression(value, state) {
  const lines = String(value).split(/;\s*/).filter(Boolean);
  return `<div class="math-expression math-expression--${state}">${lines.map(line => {
    const fractions = line.match(/^(.+?)\s*\/\s*(.+?)\s*=\s*(.+?)\s*\/\s*(.+)$/);
    if (fractions) return `<div class="math-line"><span class="math-fraction"><span>${escapeWhiteboardHtml(fractions[1])}</span><span>${escapeWhiteboardHtml(fractions[2])}</span></span><span class="math-equals">=</span><span class="math-fraction"><span>${escapeWhiteboardHtml(fractions[3])}</span><span>${escapeWhiteboardHtml(fractions[4])}</span></span></div>`;
    const equals=line.indexOf("=");
    if(equals>=0){const left=line.slice(0,equals).trim(),right=line.slice(equals+1).trim();return `<div class="math-line math-equation"><span data-object-id="left-side">${renderMathTokens(left)}</span><span class="math-equals" data-object-id="equals">=</span><span data-object-id="right-side">${renderMathTokens(right)}</span></div>`;}
    return `<div class="math-line">${renderMathTokens(line)}</div>`;
  }).join("")}</div>`;
}

function renderMathTokens(value){let index=0;return String(value).split(/(\s+|(?=[+−\-÷])|(?<=[+−\-÷]))/).filter(Boolean).map(token=>{if(/^\s+$/.test(token))return token;index+=1;const role=/^[−-]\s*\d/.test(token)?" negative-term":/^\d*x$/.test(token)?" variable-term":"";return `<span class="math-token${role}" data-object-id="token-${index}">${escapeWhiteboardHtml(token)}</span>`;}).join("");}

function escapeWhiteboardHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
}

function renderGraphSpec(spec, step, phase) {
  const stageAnnotation=(step?.annotations||[]).find(item=>String(item).startsWith("stage:"));
  const stage=stageAnnotation?Number(stageAnnotation.split(":")[1]):3;
  const traces = (spec.data || []).filter(trace => ["scatter", "scattergl"].includes(trace.type || "scatter"));
  const values = traces.flatMap(trace => (trace.x || []).map((x, index) => [Number(x), Number((trace.y || [])[index])]));
  if (!values.length || values.some(pair => pair.some(value => !Number.isFinite(value)))) return "";
  const xs = values.map(pair => pair[0]), ys = values.map(pair => pair[1]);
  const minX = Math.min(...xs), maxX = Math.max(...xs), minY = Math.min(...ys), maxY = Math.max(...ys);
  const sx = value => 42 + ((value - minX) / (maxX - minX || 1)) * 336;
  const sy = value => 198 - ((value - minY) / (maxY - minY || 1)) * 160;
  const drawings = traces.map(trace => {
    const pairs = (trace.x || []).map((x, index) => [Number(x), Number(trace.y[index])]);
    if (String(trace.mode || "").includes("lines")) return stage<2?"":`<polyline class="generated-graph__curve ${phase}" points="${pairs.map(pair => `${sx(pair[0])},${sy(pair[1])}`).join(" ")}"/>`;
    const visible=stage<2?0:stage===2?Math.min(2,pairs.length):pairs.length;
    return pairs.slice(0,visible).map((pair, index) => `<g><circle class="generated-graph__point" cx="${sx(pair[0])}" cy="${sy(pair[1])}" r="5"/><text x="${sx(pair[0]) + 7}" y="${sy(pair[1]) - 7}">${escapeWhiteboardHtml((trace.text || [])[index] || "")}</text></g>`).join("");
  }).join("");
  const title = spec.layout?.title?.text || "Mathematical graph";
  return `<figure class="generated-graph"><svg viewBox="0 0 420 220" role="img" aria-label="${escapeWhiteboardHtml(title)}"><line x1="42" y1="198" x2="390" y2="198" class="axis"/><line x1="42" y1="205" x2="42" y2="20" class="axis"/>${drawings}</svg><figcaption>${escapeWhiteboardHtml(title)}</figcaption></figure>`;
}
