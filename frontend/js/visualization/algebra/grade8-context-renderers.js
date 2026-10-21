/* Approved Grade 8 Lesson 9: each scenario draws from its own question data. */
(function () {
  const escape = value => escapeWhiteboardHtml(String(value ?? ""));
  const fields = text => Object.fromEntries(String(text || "").split("; ").map(part => {
    const equal = part.indexOf("=");
    return equal < 0 ? ["", ""] : [part.slice(0, equal).trim(), part.slice(equal + 1).trim()];
  }).filter(([key]) => key));
  const step = state => Number(((state.annotations || []).find(value => value.startsWith("stage:")) || "stage:0").slice(6));
  const visible = (state, phase, first) => phase === "result" && step(state) >= first;
  const card = (label, value, objectId = "fraction-1") => `<div class="context-card" data-object-id="${objectId}"><span>${escape(label)}</span><strong>${escape(value)}</strong></div>`;
  const covered = (show, value) => show ? escape(value) : "?";

  function translation(data, params, state, phase) {
    const n = visible(state, phase, 1), relation = visible(state, phase, 2);
    return `<div class="context-strips" data-object-id="model">${card("Unknown", covered(n, data.unknown || data.start || "n"))}<span class="context-join">+</span>${card("Increase", covered(relation, data.change || "+7"), "fraction-2")}${card("Stated total", data.total || "19", "denominator")}</div>`;
  }
  function number(data, params, state, phase) {
    const numbered = visible(state, phase, 1), changed = visible(state, phase, 3);
    const consecutive = (data.relationship || "").includes("consecutive");
    const terms=[...(data.terms || "").matchAll(/'([^']+)'/g)].map(match=>match[1]);
    return `<div class="context-strips" data-object-id="model">${consecutive
      ? terms.map((term,i) => card(`Integer ${i + 1}`, covered(numbered, term), i === terms.length-1 ? "fraction-2" : "fraction-1")).join("")
      : `${card("Starting number", covered(numbered, data.base))}${card("First: multiply", covered(numbered, `${data.multiplier} × ${data.base}`), "fraction-2")}${card("Then change", covered(changed, data.change), "denominator")}`}
      ${card("Given result", data.result || data.total || "", "denominator")}</div>`;
  }
  function money(data, params, state, phase) {
    const savings='starting_amount' in data,delivery='fixed_fee' in data,tickets='adult_difference' in data;
    const price = delivery ? data.unit_rate : savings ? data.weekly_amount : data.learner_price;
    const initial = delivery ? data.fixed_fee : savings ? data.starting_amount : tickets ? data.adult_price : data.teacher_price;
    const first = savings ? "Already saved" : delivery ? "Delivery once" : tickets ? "Learner ticket" : `${data.learner_groups} learner packs`;
    const second = savings ? "Per week" : delivery ? "Per notebook" : tickets ? "Adult ticket" : `${data.teacher_groups} teacher packs`;
    const fmt=value=>/^\d+(?:\.\d+)?$/.test(String(value)) ? `R${value}` : `R(${value})`;
    const difference=tickets?card("Adult count",covered(visible(state,phase,2),`l + ${data.adult_difference}`),"context"):'';
    return `<div class="context-strips" data-object-id="model">${card(first, covered(visible(state,phase,1), fmt(tickets ? price : initial)))}${card(second, covered(visible(state,phase,2), fmt(tickets ? initial : price)), "fraction-2")}${difference}${card("Question total", `R${data.total || data.target}`, "denominator")}</div>`;
  }
  function perimeter(data, params, state, phase) {
    const triangle = data.shape === "triangle";
    const sides = triangle ? [...(data.sides || "").matchAll(/'([^']+)'/g)].map(match=>match[1]) : [data.length, data.width];
    const n = visible(state,phase,1), m = visible(state,phase,2);
    const labels = triangle ? sides.map((side,i) => covered(i===0?n:m, side)) : [covered(n, data.length), covered(m, data.width)];
    const shape = triangle
      ? `<polygon points="180,18 330,176 28,176" fill="none" stroke="currentColor" stroke-width="3"/><text x="235" y="90">${escape(labels[0])}</text><text x="155" y="197">${escape(labels[1])}</text><text x="44" y="92">${escape(labels[2])}</text>`
      : `<rect x="55" y="28" width="245" height="135" fill="none" stroke="currentColor" stroke-width="3"/><text x="170" y="22">${escape(labels[0])}</text><text x="170" y="190">${escape(labels[0])}</text><text x="16" y="101">${escape(labels[1])}</text><text x="307" y="101">${escape(labels[1])}</text>`;
    return `<div class="context-geometry" data-object-id="model"><svg role="img" viewBox="0 0 365 208" aria-label="${triangle?'Three separate triangle sides':'Two equal lengths and two equal widths'}; perimeter ${escape(data.perimeter)} centimetres">${shape}</svg>${card("Perimeter", `${data.perimeter} cm`, "denominator")}<span data-object-id="fraction-1" hidden></span><span data-object-id="fraction-2" hidden></span></div>`;
  }
  function sharing(data, params, state, phase) {
    const unit = data.unit || data.currency || "R";
    const difference = data.difference || (data.second_stage || "").split("+").at(-1).trim();
    return `<div class="context-strips context-strips--stacked" data-object-id="model">${card("Whole", `${unit}${data.total}`, "denominator")}${card(data.base_person || "First stage", covered(visible(state,phase,1),data.base_share || data.first_stage || "d"))}${card(data.other_person || "Second stage", covered(visible(state,phase,2),`${data.base_share || data.first_stage || 'd'} + ${difference} ${unit}`),"fraction-2")}</div>`;
  }
  function age(data,params,state,phase) {
    return `<div class="context-strips context-strips--stacked" data-object-id="model">${card("Present: child", covered(visible(state,phase,1),data.child_age || "c years"))}${card("Present: parent", covered(visible(state,phase,3),data.parent_age || "3c + 4 years"),"fraction-2")}${card("Ages together", `${data.total} years`,"denominator")}</div>`;
  }
  function rate(data,params,state,phase) {
    const compare = Boolean(data.plan_a);
    const plan = source => ({fixed:(source.match(/'fixed':\s*(\d+)/)||[])[1],rate:(source.match(/'rate':\s*(\d+)/)||[])[1]});
    const a=plan(data.plan_a || ''),b=plan(data.plan_b || '');
    const row = (name,fixed,rate,target) => `<tr data-object-id="${target}"><th>${escape(name)}</th><td>R${escape(fixed)}</td><td>R${escape(rate)} per ${compare?'minute':'km'}</td></tr>`;
    const plans = compare ? `<tbody>${row('Plan A',a.fixed,a.rate,'fraction-1')}${row('Plan B',b.fixed,b.rate,'fraction-2')}</tbody>` : `<tbody>${row('Taxi',data.fixed_fee,data.rate,'fraction-1')}<tr data-object-id="fraction-2"><th>Distance</th><td colspan="2">${visible(state,phase,1)?escape(data.quantity):'? kilometres'}</td></tr></tbody>`;
    return `<div class="context-table" data-object-id="model"><table><thead><tr><th>Cost</th><th>Fixed once</th><th>Per unit</th></tr></thead>${plans}</table>${card(compare?'Equal cost':'Trip total',compare?'same total':`R${data.total}`,"denominator")}</div>`;
  }
  function error(data,params,state,phase) {
    return `<div class="context-strips context-strips--stacked" data-object-id="model">${card("Original phrase",data.phrase)}${card("Learner wrote",data.learner_equation,"fraction-2")}${card("Inspect order",visible(state,phase,4)?"Twice first, then subtract three":"Which action comes first?","denominator")}</div>`;
  }
  const models = { context_translation_strip_native:translation, number_relationship_native:number,
    money_model_native:money, perimeter_model_native:perimeter, sharing_bar_model_native:sharing,
    age_timeline_native:age, rate_table_native:rate, error_diagnosis_context_native:error };
  for (const [family, model] of Object.entries(models)) {
    AthenaVisualizationRegistry.register("algebra",family,{render(params,state,phase){
      const data=fields(params.source_data),current=step(state),finished=phase==="result",active=phase!=="initial";
      const final=finished && current >= Number(params.total_steps);
      return `<section class="context-visual" data-question-id="${escape(params.question_id)}" data-stage="${current}" data-phase="${escape(phase)}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${escape(params.prompt)}</span></p>${model(data,params,state,phase)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before"><span data-object-id="left-expression">${escape(state.before_state)}</span><span data-object-id="right-expression" hidden></span><span data-object-id="variable-slot" hidden></span><span data-object-id="balance-beam" hidden></span><span data-object-id="context" hidden></span></div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Current modelling or solving action</span><strong>${active?escape(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${finished&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${finished?escape(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked in the original situation</span><strong>${final?escape(state.after_state):''}</strong></div>${['inverse-operation','left-operation','right-operation','cancellation','substitution-slot','balance-left-pan','balance-right-pan','conclusion'].map(id=>`<span data-object-id="${id}" hidden></span>`).join('')}</div></div></section>`;
    },destroy(){}});
  }
})();
