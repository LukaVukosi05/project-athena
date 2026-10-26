/* Question-specific mixed simplification models: operation paths remain on board. */
(() => {
  const esc=v=>escapeWhiteboardHtml(String(v??''));
  const families=['term_bins','distribute_collect','signed_distribution_collect','quotient_collect',
    'dual_distribution_collect','negative_bracket','variable_quotient_collect','power_bins',
    'distribution_error','perimeter_mixed','equivalent_mixed','layered_mixed','layered_quotient_mixed'];
  const label={term_bins:'Sort matching terms',distribute_collect:'Expand and collect',
    signed_distribution_collect:'Follow the signed arrows',quotient_collect:'Divide each numerator term',
    dual_distribution_collect:'Two independent bracket paths',negative_bracket:'Subtract the whole bracket',
    variable_quotient_collect:'Divide with the restriction',power_bins:'Separate powers',
    distribution_error:'Find the first missed arrow',perimeter_mixed:'Trace four sides',
    equivalent_mixed:'Compare general forms',layered_mixed:'Complete three operation paths',
    layered_quotient_mixed:'Complete quotient and bracket paths'};
  function draw(family,p,state,phase){
    const tokens=p.model_tokens||[],count=p.model_scene?.input_count||2;
    const n=Number(((state.annotations||[]).find(a=>a.startsWith('stage:'))||'stage:0').slice(6));
    const final=phase==='result'&&n>=Number(p.total_steps)-1;
    const active=phase!=='ready',result=phase==='result';
    const input=(v,i)=>`<div class="mixed-object" data-object-id="token-${i+1}"><small>${family==='power_bins'?(v.includes('²')?'Square term':'Linear or other term'):family==='perimeter_mixed'?(i===0?'Length':i===1?'Width':'Rule'):family==='distribution_error'&&i===1?'Learner claim':family.includes('quotient')&&v.includes('≠')?'Domain restriction':'Given part'}</small><strong>${esc(v)}</strong></div>`;
    const output=(v,i)=>`<div class="mixed-object mixed-object--derived ${final?'':'is-concealed'}" data-object-id="token-${i+1}"><small>Calculated</small><strong>${final?esc(v):'?'}</strong></div>`;
    const given=tokens.slice(0,count).map(input).join('');
    const derived=tokens.slice(count).map((v,i)=>output(v,count+i)).join('');
    const path=tokens.slice(0,count).map((v,i)=>`<div class="mixed-path ${active&&i===Math.min(n-1,count-1)?'is-active':''}" data-path="${i+1}"><span class="mixed-path-arrow">${family==='negative_bracket'&&i===1?'−1 × each term':family==='term_bins'||family==='power_bins'?'sort by kind':family.includes('quotient')&&i===0?'÷ each term':family==='perimeter_mixed'?'trace twice':family==='distribution_error'?'inspect arrow':'→ each term'}</span><span>${esc(v)}</span></div>`).join('');
    const rect=family==='perimeter_mixed'?`<svg class="mixed-rectangle" viewBox="0 0 320 170" role="img" aria-label="Rectangle with ${esc(tokens[0])} and ${esc(tokens[1])}"><rect x="65" y="28" width="180" height="100"/><text x="155" y="20" text-anchor="middle">${esc(tokens[0])}</text><text x="155" y="153" text-anchor="middle">${esc(tokens[0])}</text><text x="30" y="83">${esc(tokens[1])}</text><text x="255" y="83">${esc(tokens[1])}</text></svg>`:'';
    const domain=tokens.slice(0,count).filter(v=>v.includes('≠')).map(v=>`<p class="mixed-domain">Restriction: ${esc(v)}</p>`).join('');
    return `<section class="mixed-visual" data-family="${esc(family)}" data-question-id="${esc(p.question_id)}" data-stage="${n}" data-phase="${esc(phase)}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(p.prompt)}</span></p><div class="mixed-scene" data-object-id="model" role="group" aria-label="${esc(label[family])} for the current question"><strong>${esc(label[family])}</strong>${rect}<div class="mixed-givens">${given}</div><div class="mixed-paths">${path}</div><div class="mixed-outputs">${derived}</div>${domain}</div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${active?esc(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${result&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result?esc(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?esc(state.after_state):''}</strong></div></div></div></section>`;
  }
  for(const family of families) AthenaVisualizationRegistry.register('algebra',family,{render(p,s,phase){return draw(family,p,s,phase);},destroy(){}});
})();
