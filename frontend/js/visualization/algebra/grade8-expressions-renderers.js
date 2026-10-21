/* Grade 8 expressions: visual family and given objects are authored per question. */
(() => {
  const safe = value => escapeWhiteboardHtml(String(value ?? ''));
  const stage = state => Number(((state.annotations || []).find(a => a.startsWith('stage:')) || 'stage:0').slice(6));
  const tile = (label, index, phase, current) => `<span class="expression-tile ${phase !== 'initial' && current >= index ? 'expression-tile--focus' : ''}" data-object-id="token-${index}">${safe(label)}</span>`;
  const tokens = (labels, phase, current) => labels.map((label,i)=>tile(label,i+1,phase,current)).join('');
  function diagram(family,labels,phase,current) {
    const objects=tokens(labels,phase,current);
    if(family==='rectangle') return `<div class="expression-geometry" data-object-id="model"><svg viewBox="0 0 440 230" role="img" aria-label="Rectangle with four individually labelled sides"><rect x="92" y="35" width="255" height="148" rx="3" fill="none" stroke="currentColor" stroke-width="3"/><text x="183" y="25">${safe(labels[0])}</text><text x="352" y="113">${safe(labels[1])}</text><text x="183" y="213">${safe(labels[2])}</text><text x="10" y="113">${safe(labels[3])}</text></svg><div class="expression-tokens">${objects}</div></div>`;
    if(family==='receipt') return `<div class="expression-receipt" data-object-id="model"><strong>Trip receipt</strong><div class="expression-tokens">${objects}</div><small>The passenger charge repeats; the booking fee appears once.</small></div>`;
    if(family==='square_comparison') return `<div class="expression-comparison" data-object-id="model"><div class="expression-tokens">${objects}</div><div class="expression-grid" aria-label="Three rows of three squares">${Array.from({length:9},()=>'<i></i>').join('')}</div></div>`;
    if(family==='fraction_bar') return `<div class="expression-fraction" data-object-id="model"><div class="expression-tokens">${objects}</div><div class="expression-halves"><span>first half of p</span><span>second half of p</span></div><small>Seven is outside the division.</small></div>`;
    if(family==='like_term_sort'||family==='unlike_term_sort') return `<div class="expression-sort" data-object-id="model"><div class="expression-lane"><small>variable terms</small>${objects}</div><small>Join only matching variables; keep constants separate.</small></div>`;
    return `<div class="expression-tokens expression-tokens--${safe(family)}" data-object-id="model">${objects}</div>`;
  }
  const families=['expression_tiles','signed_terms','grouped_terms','fraction_bar','square_comparison','like_term_sort','unlike_term_sort','receipt','rectangle'];
  families.forEach(family=>AthenaVisualizationRegistry.register('algebra',family,{render(params,state,phase){
    const current=stage(state), active=phase!=='initial', result=phase==='result';
    const final=result && current >= Number(params.total_steps);
    return `<section class="expression-visual" data-question-id="${safe(params.question_id)}" data-phase="${safe(phase)}" data-stage="${current}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${safe(params.prompt)}</span></p>${diagram(family,params.model_tokens,phase,current)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${safe(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${active?safe(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${result&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result?safe(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?safe(state.after_state):''}</strong></div></div></div></section>`;
  },destroy(){}}));
})();
