/* Native Lesson 3 models. Existing Lesson 1 and Lesson 2 registrations stay intact. */
(function () {
  const esc = value => escapeWhiteboardHtml(String(value ?? ""));
  const fields = source => Object.fromEntries(String(source || "").split(";").map(part => {
    const at = part.indexOf("=");
    return at < 0 ? ["", ""] : [part.slice(0, at).trim(), part.slice(at + 1).trim()];
  }).filter(([key]) => key));
  const stage = state => Number(String((state.annotations || []).find(a => a.startsWith("stage:")) || "stage:0").split(":")[1]);
  const original = (d, parameters) => d.original || d.equation || d.example ||
    (d["left expression"] ? `${d["left expression"]} = ${d["right value"]}` : parameters.prompt);
  function balance(d, parameters, state, phase) {
    const n = stage(state), result = phase === "result", op = d["inverse operation"] || d["correct operation"] || d["legal operation"] || "same operation";
    const left = d["left expression"] || d.original || d.equivalent || d.example || original(d,parameters);
    const right = d["right value"] || d.total || d.final || "";
    return `<div class="additive-model additive-balance" data-object-id="balance-beam" data-stage="${n}">
      <div class="additive-pan" data-object-id="balance-left-pan"><strong>${esc(left)}</strong><span>left side</span></div>
      <span class="additive-balance-bar" aria-hidden="true">=</span>
      <div class="additive-pan" data-object-id="balance-right-pan"><strong>${esc(right || "same value")}</strong><span>right side</span></div>
      <div class="additive-pair ${n>0 ? "is-revealed" : ""}"><span data-object-id="inverse-operation">${n>0 ? esc(op) : "inverse hidden"}</span>
      <span data-object-id="left-operation">${phase!=="initial" ? "applied to left" : "waiting"}</span>
      <span data-object-id="right-operation">${phase!=="initial" ? "applied to right" : "waiting"}</span>
      <span data-object-id="cancellation">${result && /cancel|zero pair/i.test(state.working_state) ? "zero pair cancels" : "zero pair pending"}</span></div></div>`;
  }
  function numberLine(d, parameters, state, phase) {
    const start=Number(d.start), landing=Number(d.landing), jump=Number(d.jump);
    const valid=[start,landing,jump].every(Number.isFinite), low=valid?Math.min(start,landing)-2:-12, high=valid?Math.max(start,landing)+2:12;
    const x=value=>45+(value-low)/(high-low)*470, n=stage(state), show=phase==="result" && n>=3;
    if (!valid) return `<div class="additive-model" data-object-id="balance-beam">${esc(original(d,parameters))}</div>`;
    const ticks=Array.from({length:Math.min(13,high-low+1)},(_,i)=>low+i*(high-low)/Math.min(12,high-low));
    return `<div class="additive-model" data-object-id="balance-beam"><svg class="additive-line" viewBox="0 0 560 150" role="img" aria-label="Number line: start ${start}, reverse jump ${jump}${show?`, land ${landing}`:""}">
       <line x1="35" y1="95" x2="530" y2="95" stroke="currentColor" stroke-width="2"/>
       ${ticks.map(v=>`<line x1="${x(v)}" y1="90" x2="${x(v)}" y2="101" stroke="currentColor"/>`).join("")}
       <circle cx="${x(start)}" cy="95" r="5" fill="currentColor"/><text x="${x(start)}" y="125" text-anchor="middle">${start}</text>
       ${show?`<path d="M${x(start)} 75 Q${(x(start)+x(landing))/2} 10 ${x(landing)} 75" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="${x(landing)}" cy="95" r="5" fill="currentColor"/><text x="${x(landing)}" y="125" text-anchor="middle">${landing}</text>`:""}</svg>
       <span data-object-id="balance-left-pan">${esc(d.equation)}</span><span data-object-id="balance-right-pan">${show?esc(state.after_state):"reverse jump hidden"}</span></div>`;
  }
  function context(d, parameters, state, phase) {
    const show=phase==="result" && stage(state)>=3;
    if (d.context === "temperature") return `<div class="additive-model additive-context" data-object-id="balance-beam"><div class="additive-thermometer" data-object-id="context"><span>Starting temperature ${show?esc(d.solution)+"°C":"?"}</span><span>↓ ${esc(d.change)}°</span><strong>Final ${esc(d.final)}°C</strong></div><span data-object-id="balance-left-pan">${esc(state.before_state)}</span><span data-object-id="balance-right-pan">${show?esc(state.after_state):"unknown start"}</span></div>`;
    return `<div class="additive-model additive-context" data-object-id="balance-beam"><div class="additive-receipt" data-object-id="context"><span>Price before delivery ${show?"R"+esc(d.solution):"?"}</span><span>Delivery R${esc(d["delivery fee"])}</span><strong>Total R${esc(d.total)}</strong></div><span data-object-id="balance-left-pan">${esc(state.before_state)}</span><span data-object-id="balance-right-pan">${show?esc(state.after_state):"subtotal hidden"}</span></div>`;
  }
  const models={additive_balance:balance,additive_number_line:numberLine,additive_context:context};
  for(const [template,model] of Object.entries(models)) AthenaVisualizationRegistry.register("algebra",template,{
    render(parameters,state,phase) {
      const d=fields(parameters.source_data), result=phase==="result", operation=phase==="operation"||result;
      const n=stage(state), done=result && n>=Number(parameters.total_steps);
      return `<section class="additive-visual" data-question-id="${esc(parameters.question_id)}" data-stage="${n}" data-phase="${esc(phase)}" data-managed-visibility="true">
        <p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(parameters.prompt)}</span></p>
        ${model(d,parameters,state,phase)}
        <div class="g8-mathematical-transition"><div class="g8-state g8-state--before"><span data-object-id="left-expression">${esc(state.before_state)}</span><span data-object-id="right-expression" hidden></span><span data-object-id="variable-slot" hidden></span></div>
        <div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${operation?"is-visible":"is-hidden"}"><span>Operation on the whiteboard</span><strong>${operation?esc(state.working_state):""}</strong></div>
        <div data-object-id="result" class="g8-timeline-object g8-result ${result&&!done?"is-visible":"is-hidden"}"><span>Result of this step</span><strong>${result?esc(state.after_state):""}</strong></div>
        <div data-object-id="verification" class="g8-timeline-object g8-verification ${done?"is-visible":"is-hidden"}"><span>Checked against the original</span><strong>${done?esc(state.after_state):""}</strong></div>
        ${template==="additive_balance"?"":`<span data-object-id="inverse-operation" hidden></span><span data-object-id="left-operation" hidden></span><span data-object-id="right-operation" hidden></span><span data-object-id="cancellation" hidden></span>`}
        <span data-object-id="substitution-slot" hidden></span><span data-object-id="conclusion" hidden></span></div></div></section>`;
    }, destroy() {},
  });
})();
