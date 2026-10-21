/* Grade 8 Lesson 10: native, case-specific diagnostic models. */
(function () {
  const esc = value => escapeWhiteboardHtml(String(value ?? ''));
  const fields = value => Object.fromEntries(String(value || '').split('; ').map(part => {
    const index = part.indexOf('=');
    return index < 0 ? ['', ''] : [part.slice(0, index).trim(), part.slice(index + 1).trim()];
  }).filter(pair => pair[0]));
  const stage = state => Number(((state.annotations || []).find(x => x.startsWith('stage:')) || 'stage:0').slice(6));
  const seen = (state, phase, at) => phase === 'result' && stage(state) >= at;
  const cell = (label, value, id = 'fraction-1') => `<div class="diagnosis-card" data-object-id="${id}"><small>${esc(label)}</small><strong>${esc(value)}</strong></div>`;
  const reveal = (condition, value) => condition ? esc(value) : '—';
  const heading = (data, params) => data.original || params.prompt;

  function replay(data, params, state, phase) {
    const lines = data.learner_steps || data.learner_step || data.learner_answer || data.learner_expansion || 'learner line';
    const first = data.first_error_index === '2' ? 4 : 3;
    return `<div class="diagnosis-replay">${cell('Original equation', heading(data, params))}${cell('Learner attempt', lines, 'fraction-2')}${cell('First incorrect change', reveal(seen(state, phase, first), data.first_error || data.first_error_tag || 'The next line does not preserve equality'), 'denominator')}</div>`;
  }
  function balance(data, params, state, phase) {
    const n = Number(data.coefficient || (data.original || '').match(/^\s*(\d+)/)?.[1] || 3);
    const groups = Array.from({length: Math.min(n, 6)}, (_, i) => `<span class="diagnosis-tile" ${i > 1 ? '' : `data-object-id="${i ? 'fraction-2' : 'fraction-1'}"`}>${esc((data.original || '').match(/[a-z]/)?.[0] || 'x')}</span>`).join('');
    return `<div class="diagnosis-balance" data-object-id="model"><div><small>${esc(n)} joined variable groups</small><div class="diagnosis-tiles">${groups}</div></div><span class="diagnosis-equals">=</span>${cell('Right-side total', (data.original || '').split('=').at(-1).trim(), 'denominator')}${cell('Equal partition', reveal(seen(state, phase, 3), `÷ ${n} on both sides`), 'context')}</div>`;
  }
  function signed(data, params, state, phase) {
    return `<div class="diagnosis-row">${cell('Complete coefficient', data.coefficient || '-2')}${cell('Learner input', data.learner_answer || '9', 'fraction-2')}${cell('Gate output', reveal(seen(state, phase, 2), '-18 ≠ 18'), 'denominator')}${cell('Reverse operation', reveal(seen(state, phase, 3), `÷ (${data.coefficient || '-2'})`), 'context')}</div>`;
  }
  function brackets(data, params, state, phase) {
    const factor = (data.original || '').match(/^\s*(\d+)\s*\(/)?.[1] || '2';
    const inner = (data.original || '').match(/\(([^)]+)\)/)?.[1] || 'group';
    const parts = inner.match(/^\s*([^+-]+)\s*([+-])\s*(\d+)/);
    return `<div class="diagnosis-row">${cell('Outside factor', factor)}${cell('First bracket term', parts?.[1] || inner, 'fraction-2')}${cell('Second bracket term', parts ? `${parts[2]} ${parts[3]}` : inner, 'denominator')}${cell('Both distribution arrows', reveal(seen(state, phase, 2), `${factor} × (${parts?.[1] || 'first term'}); ${factor} × (${parts ? parts[2] + parts[3] : 'second term'})`), 'context')}</div>`;
  }
  function fractions(data, params, state, phase) {
    const terms = (data.original || '').split('=').at(0).split('+');
    return `<div class="diagnosis-row">${cell('First fraction', terms[0]?.trim())}${cell('Second fraction', terms[1]?.trim(), 'fraction-2')}${cell('Common denominator', reveal(seen(state, phase, 1), data.lcd || '6'), 'denominator')}${cell('Every term scaled', reveal(seen(state, phase, 4), data.cleared_equation || 'multiply the whole equation'), 'context')}</div>`;
  }
  function words(data, params, state, phase) {
    return `<div class="diagnosis-row">${cell('Given phrase', data.phrase || params.prompt)}${cell('Learner model', data.learner_equation, 'fraction-2')}${cell('Quantity before subtraction', reveal(seen(state, phase, 1), (data.correct_equation || '').split('-')[0]), 'denominator')}${cell('Correct order', reveal(seen(state, phase, 4), data.correct_equation), 'context')}</div>`;
  }
  function perimeter(data, params, state, phase) {
    const length = data.length || 'x + 2', width = data.width || 'x';
    const second = seen(state, phase, 2), all = seen(state, phase, 3);
    const side = (x, y, value, shown, target) => `<text x="${x}" y="${y}" data-object-id="${target}" class="${shown ? '' : 'diagnosis-muted'}">${esc(shown ? value : '?')}</text>`;
    return `<div class="diagnosis-geometry"><svg viewBox="0 0 370 215" role="img" aria-label="Rectangle with ${esc(length)} and ${esc(width)}; opposite sides revealed during repair"><rect x="60" y="32" width="245" height="145" fill="none" stroke="currentColor" stroke-width="3"/>${side(145,24,length,true,'fraction-1')}${side(18,108,width,true,'fraction-2')}${side(145,204,length,second,'context')}${side(310,108,width,second,'denominator')}</svg>${cell('Full perimeter', reveal(all, data.correct_equation), 'model')}</div>`;
  }
  function classify(data, params, state, phase) {
    const trueState = data.classification === 'infinitely many solutions';
    return `<div class="diagnosis-row">${cell('Original sides', data.original)}${cell('Learner conclusion', data.learner_conclusion, 'fraction-2')}${cell('After variable cancellation', reveal(seen(state, phase, 2), data.reduced_statement), 'denominator')}${cell('Truth test', reveal(seen(state, phase, 3), trueState ? 'Always true' : 'Always false'), 'context')}</div>`;
  }
  function fare(data, params, state, phase) {
    return `<table class="diagnosis-table" data-object-id="model"><thead><tr><th>Fare part</th><th>Amount</th><th>Frequency</th></tr></thead><tbody><tr data-object-id="fraction-1"><th>Starting charge</th><td>R${esc(data.fixed_fee)}</td><td>Once</td></tr><tr data-object-id="fraction-2"><th>Distance charge</th><td>R${esc(data.rate)}</td><td>Per ${esc(data.unit || 'km')}</td></tr><tr data-object-id="denominator"><th>Trip total</th><td>R${esc(data.total)}</td><td>Given</td></tr></tbody></table>${cell('Repaired cost model', reveal(seen(state, phase, 4), data.correct_equation), 'context')}`;
  }
  function mastery(data, params, state, phase) {
    const active = seen(state, phase, 2), routed = seen(state, phase, Number(params.total_steps));
    return `<div class="diagnosis-row">${cell('Original', data.original)}${cell('Learner expansion', data.learner_expansion, 'fraction-2')}${cell('First error cluster', reveal(active, data.first_error_tag), 'denominator')}${cell('Repair and new assessment', reveal(routed, data.repair_route), 'context')}</div>`;
  }
  const families = {
    diagnosis_first_error_replay_native: replay, diagnosis_balance_equation_native: balance,
    diagnosis_signed_balance_native: signed, diagnosis_bracket_distribution_native: brackets,
    diagnosis_denominator_lcm_native: fractions, diagnosis_error_diagnosis_context_native: words,
    diagnosis_perimeter_model_native: perimeter, diagnosis_identity_contradiction_native: classify,
    diagnosis_rate_table_native: fare, diagnosis_mastery_map_native: mastery
  };
  for (const [family, model] of Object.entries(families)) {
    AthenaVisualizationRegistry.register('algebra', family, {render(params, state, phase) {
      const data=fields(params.source_data), n=stage(state), active=phase!=='initial';
      const finished=phase==='result', final=finished&&n>=Number(params.total_steps);
      return `<section class="diagnosis-visual" data-question-id="${esc(params.question_id)}" data-stage="${n}" data-phase="${esc(phase)}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(params.prompt)}</span></p>${model(data,params,state,phase)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before"><span data-object-id="left-expression">${esc(state.before_state)}</span><span data-object-id="right-expression" hidden></span><span data-object-id="variable-slot" hidden></span><span data-object-id="balance-beam" hidden></span></div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>What changes now</span><strong>${active?esc(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${finished&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${finished?esc(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>${params.question_id.endsWith('w15')?'Checked and routed':'Check the original'}</span><strong>${final?esc(state.after_state):''}</strong></div>${['inverse-operation','left-operation','right-operation','cancellation','substitution-slot','balance-left-pan','balance-right-pan','conclusion'].map(id=>`<span data-object-id="${id}" hidden></span>`).join('')}</div></div></section>`;
    },destroy(){}});
  }
})();
