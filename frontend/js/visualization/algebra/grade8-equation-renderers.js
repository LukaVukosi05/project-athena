(function () {
  const esc = value => escapeWhiteboardHtml(String(value ?? ""));
  const fields = parameters => Object.fromEntries(String(parameters.source_data || "").split(";").map(part => {
    const index = part.indexOf("=");
    return index < 0 ? [part.trim(), ""] : [part.slice(0, index).trim(), part.slice(index + 1).trim()];
  }));
  const annotation = (state, name, fallback) => String((state.annotations || []).find(item => item.startsWith(`${name}:`)) || `${name}:${fallback}`).split(":").slice(1).join(":");
  const stageNumber = state => Number(annotation(state, "stage", "0"));
  const action = state => annotation(state, "action", "show_object");
  const teachingPhase = state => annotation(state, "phase", "operation");
  const tokens = (value, side) => String(value || "").split(/(\s+|(?=[+−×÷()])|(?<=[+−×÷()]))/).filter(Boolean).map((token, index) => {
    if (/\s+/.test(token)) return token;
    return `<span class="g8-math-token" data-term-id="${side}-term-${index}">${esc(token)}</span>`;
  }).join("");
  const cleanState = value => String(value || "").replace(/^Checked:\s*/i, "").replace(/^Reset:\s*/i, "").replace(/;.*$/, "").replace(/\s+is true$/i, "").replace(/\s[—-]\s(?:balanced|level).*$/i, "").trim();
  const splitEquation = value => {
    const match = cleanState(value).match(/^(.*?)\s*(=|≠)\s*(.*)$/);
    return match ? [match[1].trim(), match[2], match[3].trim()] : [cleanState(value), "", ""];
  };
  const equation = value => {
    const [left, relation, right] = splitEquation(value);
    if (!relation) return `<span data-object-id="left-expression" class="g8-side">${tokens(left, "left")}</span><span data-object-id="right-expression" class="g8-side g8-side--empty" aria-hidden="true">unchanged</span>`;
    return `<span data-object-id="left-expression" class="g8-side">${tokens(left, "left")}</span><b class="g8-equals">${esc(relation)}</b><span data-object-id="right-expression" class="g8-side">${tokens(right, "right")}</span>`;
  };
  const numericValue = expression => {
    const safe = String(expression).replace(/−/g, "-").trim();
    return /^-?\d+(?:\.\d+)?$/.test(safe) ? Number(safe) : NaN;
  };
  const balanceRelation = state => {
    const [left, relation, right] = splitEquation(state);
    if (relation !== "≠") return "level";
    const leftValue = numericValue(left), rightValue = numericValue(right);
    return Number.isFinite(leftValue) && Number.isFinite(rightValue) && leftValue > rightValue ? "left-heavy" : "right-heavy";
  };
  const balanceModel = (state, family, afterState) => {
    const [left, relation, right] = splitEquation(state), [afterLeft, afterRelation, afterRight] = splitEquation(afterState), balance = balanceRelation(state), afterBalance = balanceRelation(afterState);
    return `<div class="g8-model-frame" data-family="${esc(family)}"><svg viewBox="0 0 560 210" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Balance comparing ${esc(left)} and ${esc(right || "the other side")}"><g data-object-id="balance-beam" class="g8-balance is-${balance}" data-balance-state="${balance}" data-after-balance="${afterBalance}"><line x1="280" y1="40" x2="280" y2="165"/><g class="g8-beam"><line x1="90" y1="75" x2="470" y2="75"/><path d="M45 80 L175 80 L155 145 L65 145 Z"/><path d="M385 80 L515 80 L495 145 L405 145 Z"/><text data-object-id="balance-left-pan" data-after-label="${esc(afterLeft)}" x="110" y="120">${esc(left)}</text><text data-object-id="balance-right-pan" data-after-label="${esc(afterRight || afterRelation || "?")}" x="450" y="120">${esc(right || relation || "?")}</text></g></g></svg></div>`;
  };
  const model = (family, parameters, state, phase) => {
    const data = fields(parameters), current = phase === "result" ? state.after_state : state.before_state;
    if (family === "equality-balance") return balanceModel(current, family, state.after_state);
    const [left, , right] = splitEquation(current);
    const [afterLeft, , afterRight] = splitEquation(state.after_state);
    const sides = `<span data-object-id="balance-left-pan" data-after-label="${esc(afterLeft)}">${esc(left || data["left expression"] || "left side")}</span><b>=</b><span data-object-id="balance-right-pan" data-after-label="${esc(afterRight)}">${esc(right || data["right expression"] || "right side")}</span>`;
    if (family === "additive-inverse") return `<div data-object-id="balance-beam" class="counter-model">${sides}<div class="zero-pair">inverse pairs cancel to zero</div></div>`;
    if (family === "multiplicative-inverse") return `<div data-object-id="balance-beam" class="factor-blocks"><div class="factor-row">${sides}</div><div class="division-arrow">equal groups on both sides</div></div>`;
    if (family === "variables-both-sides") return `<div data-object-id="balance-beam" class="variable-rows">${sides}<div>matching variable groups remain equal</div></div>`;
    if (family === "context-to-equation") return `<div data-object-id="balance-beam" class="context-flow"><article data-object-id="context">${esc(data.objects)}</article><b>has total ${esc(data.total)}</b><article>${esc(data.equation)}</article><span data-object-id="balance-left-pan">${esc(left)}</span><span data-object-id="balance-right-pan">${esc(right)}</span></div>`;
    if (family === "distributive-equation") return `<div data-object-id="balance-beam" class="distribution-model">${sides}<div class="distribution-arrows">one complete bracket group stays together</div></div>`;
    return `<div data-object-id="balance-beam" class="operation-chain">${sides}<div class="reverse-chain">undo operations equally on both sides</div></div>`;
  };
  const render = family => (parameters, state, phase) => {
    const target = state.target || "left-expression", isResult = phase === "result", operationAction = action(state), statePhase = teachingPhase(state);
    const resultLabel = statePhase === "verification" ? "Verified conclusion" : statePhase === "explicit_answer" ? "Answer" : "Result of this step";
    const needsVariable = /x|□/.test(String(parameters.prompt)) || target === "variable-slot";
    return `<section class="g8-equation-visual g8-${family}" data-question-id="${esc(parameters.question_id)}" data-stage="${stageNumber(state)}" data-phase="${esc(phase)}" data-action="${esc(operationAction)}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(parameters.prompt)}</span></p><div class="g8-native-model">${model(family, parameters, state, phase)}</div><div class="g8-mathematical-transition" aria-label="Current mathematical transformation"><div class="g8-state g8-state--before">${equation(state.before_state)}</div><div data-object-id="variable-slot" class="g8-variable-slot ${target === "variable-slot" ? "g8-active-target" : ""}" ${needsVariable ? "" : "hidden"}>unknown value</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation is-hidden" data-operation-action="${esc(operationAction)}"><span>Operation</span><strong>${esc(state.working_state)}</strong><div class="g8-operation-path" aria-hidden="true"><i data-object-id="inverse-operation">inverse</i><i data-object-id="left-operation">left side</i><i data-object-id="right-operation">right side</i><i data-object-id="cancellation">cancel</i><i data-object-id="substitution-slot">substitute</i></div></div><div data-object-id="result" class="g8-timeline-object g8-result ${isResult && operationAction !== "verify_solution" ? "is-visible" : "is-hidden"}"><span>${resultLabel}</span><strong>${esc(state.after_state)}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${isResult && operationAction === "verify_solution" ? "is-visible" : "is-hidden"}"><span>Check against the original</span><strong>${esc(state.after_state)}</strong></div></div><div data-object-id="conclusion" class="g8-conclusion ${isResult && statePhase !== "operation" ? "is-visible" : "is-hidden"}">${esc(state.after_state)}</div></div></section>`;
  };
  for (const family of ["equality_balance", "additive_inverse", "multiplicative_inverse", "two_step_balance", "variables_both_sides", "context_to_equation", "distributive_equation"]) AthenaVisualizationRegistry.register("algebra", family, { render:render(family.replaceAll("_", "-")), destroy(){} });
})();
