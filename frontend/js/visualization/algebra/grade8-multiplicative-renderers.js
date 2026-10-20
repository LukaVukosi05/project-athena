/* Four question-specific models for Grade 8 multiplicative inverses. */
(function () {
  const esc = value => escapeWhiteboardHtml(String(value ?? ""));
  const fields = source => Object.fromEntries(String(source || "").split(";").map(part => {
    const at = part.indexOf("=");
    return at < 0 ? ["", ""] : [part.slice(0,at).trim(),part.slice(at+1).trim()];
  }).filter(([key])=>key));
  const step = state => Number(String((state.annotations||[]).find(a=>a.startsWith("stage:"))||"stage:0").split(":")[1]);
  const reveal = (state,phase) => phase === "result" && step(state) >= 2;

  function groups(d,p,state,phase) {
    const count = Math.max(1,Math.min(12,Number(d.groups)||4));
    const total = d.total || (d["unknown total"] ? "?" : "?");
    const known = d["unit value"] || d["unit fraction"] || "x";
    const unit = reveal(state,phase) ? (d["unit value"]||d["solution fraction"]||d["solution decimal"]||d.solution||"one group") : "?";
    return `<div class="multi-model multi-groups" data-object-id="balance-beam" role="img" aria-label="${count} equal groups balanced against ${esc(total)}">
      <div class="multi-group-row">${Array.from({length:count},(_,i)=>`<span class="multi-group" data-group="${i+1}"><small>group ${i+1}</small><strong>${esc(unit)}</strong></span>`).join("")}</div>
      <p data-object-id="context">${count} equal groups <span aria-hidden="true">↔</span> total ${esc(total === "?" && reveal(state,phase) ? d.solution||state.after_state : total)}</p>
      <p class="multi-evidence" data-object-id="balance-left-pan">${esc(d.equation||p.prompt)}</p>
      <span data-object-id="balance-right-pan" hidden>${esc(total)}</span></div>`;
  }
  function inverse(d,p,state,phase) {
    const coefficient = d.coefficient || d.divisor || d["example coefficient"] || (d.general ? "a" : "coefficient");
    const right = d["right value"] || d.quotient || (d.original||p.prompt).split("=").pop().trim();
    const visible = phase !== "initial";
    const condition = d.condition || (d.general ? "a ≠ 0" : "coefficient ≠ 0");
    return `<div class="multi-model multi-inverse" data-object-id="balance-beam">
      <div class="multi-side" data-object-id="balance-left-pan"><small>variable side</small><strong>${esc(d.original||p.prompt)}</strong></div>
      <span class="multi-equals">=</span>
      <div class="multi-side" data-object-id="balance-right-pan"><small>given value</small><strong>${esc(right)}</strong></div>
      <div class="multi-card" data-object-id="inverse-operation"><small>Undo the ${d.divisor ? "division by" : "coefficient"}</small><strong>${esc(coefficient)}</strong><span>${visible ? esc(d.operation||d["correct operation"]||"apply the inverse on both sides") : "choose the inverse"}</span></div>
      ${d.general ? `<p class="multi-condition" data-object-id="context">${visible ? esc(condition) : "When is division allowed?"}</p>` : `<span data-object-id="context" hidden></span>`}
      <span data-object-id="cancellation" hidden>${visible ? "inverse pair becomes one" : ""}</span></div>`;
  }
  function fraction(d,p,state,phase) {
    const fraction = d.fraction || d.coefficient || d.divisor || "1/4";
    const parts = fraction === "2/3" ? 3 : fraction === "1/4" || fraction === "0.25" ? 4 : 2;
    const selected = fraction === "2/3" ? 2 : 1;
    const partValue = d["part litres"] || d["right value"] || d.quotient || "?";
    const whole = reveal(state,phase) ? (d["whole litres"]||d.solution||"whole") : "?";
    return `<div class="multi-model multi-fraction" data-object-id="balance-beam" role="img" aria-label="${esc(fraction)} of the whole, supplied portion ${esc(partValue)}">
       <div class="multi-part-row" data-object-id="balance-left-pan">${Array.from({length:parts},(_,i)=>`<span class="multi-part ${i<selected?"is-known":""}" data-part="${i+1}">${i<selected?"known":"?"}</span>`).join("")}</div>
       <div class="multi-fraction-key" data-object-id="balance-right-pan"><span>${esc(fraction)} of whole = ${esc(partValue)}</span><strong>whole = ${esc(whole)}</strong></div>
       <span data-object-id="inverse-operation" class="multi-card">${phase==="initial"?"Find the reciprocal":esc(d.reciprocal||d.operation||"multiply every part equally")}</span>
       <span data-object-id="context" hidden></span><span data-object-id="cancellation" hidden>fraction × reciprocal = 1</span></div>`;
  }
  function context(d,p,state,phase) {
    const n = Number(d.objects || d.stages || 0), count = Math.max(1,Math.min(10,n||2));
    const isRectangle = d.shape === "rectangle", isRoute = !!d["route km"];
    const total = d["area cm2"] ? `${d["area cm2"]} cm²` : d["total rand"] ? `R${d["total rand"]}` : `${d["route km"]} km`;
    const label = isRectangle ? "length" : isRoute ? "stage" : "bundle";
    const unit = reveal(state,phase) ? (d["solution cm"] ? `${d["solution cm"]} cm` : d["solution rand"] ? `R${d["solution rand"]}` : `${d["solution km"]} km`) : "?";
    return `<div class="multi-model multi-context" data-object-id="balance-beam"><p data-object-id="context">${isRectangle ? "Rectangle: width " + esc(d["width cm"]) + " cm" : isRoute ? "Route split into " + count + " equal stages" : count + " identical data bundles"}</p>
       <div class="multi-group-row" data-object-id="balance-left-pan">${isRectangle ? `<span class="multi-rectangle">area ${esc(total)}<br>length ${esc(unit)}</span>` : Array.from({length:count},(_,i)=>`<span class="multi-group" data-group="${i+1}"><small>${label} ${i+1}</small><strong>${esc(unit)}</strong></span>`).join("")}</div>
       <strong data-object-id="balance-right-pan">Given total: ${esc(total)}</strong>
       <span data-object-id="inverse-operation" hidden></span><span data-object-id="cancellation" hidden></span></div>`;
  }
  const models = {equal_groups:groups,multiplicative_balance:inverse,fraction_scale:fraction,multiplicative_context:context};
  for(const [template,model] of Object.entries(models)) AthenaVisualizationRegistry.register("algebra",template,{
    render(parameters,state,phase) {
      const d=fields(parameters.source_data),n=step(state),done=phase==="result"&&n>=Number(parameters.total_steps);
      const operation=phase==="operation"||phase==="result", result=phase==="result";
      return `<section class="multi-visual" data-question-id="${esc(parameters.question_id)}" data-stage="${n}" data-phase="${esc(phase)}" data-managed-visibility="true">
        <p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(parameters.prompt)}</span></p>
        ${model(d,parameters,state,phase)}
        <div class="g8-mathematical-transition"><div class="g8-state g8-state--before"><span data-object-id="left-expression">${esc(state.before_state)}</span><span data-object-id="right-expression" hidden></span><span data-object-id="variable-slot" hidden></span></div>
          <div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${operation?"is-visible":"is-hidden"}"><span>Operation on both sides</span><strong>${operation?esc(state.working_state):""}</strong></div>
          <div data-object-id="result" class="g8-timeline-object g8-result ${result&&!done?"is-visible":"is-hidden"}"><span>Result of this step</span><strong>${result?esc(state.after_state):""}</strong></div>
          <div data-object-id="verification" class="g8-timeline-object g8-verification ${done?"is-visible":"is-hidden"}"><span>Checked against the original</span><strong>${done?esc(state.after_state):""}</strong></div>
          ${template==="equal_groups"?`<span data-object-id="inverse-operation" hidden></span>`:""}
          ${template==="equal_groups"?`<span data-object-id="cancellation" hidden></span>`:""}
          <span data-object-id="left-operation" hidden></span><span data-object-id="right-operation" hidden></span><span data-object-id="substitution-slot" hidden></span><span data-object-id="conclusion" hidden></span>
        </div></div></section>`;
    },destroy() {},
  });
})();
