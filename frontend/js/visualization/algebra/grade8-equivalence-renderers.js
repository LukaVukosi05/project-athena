/* Grade 8 Lesson 2: simultaneous representations with question-bound objects. */
(() => {
  const esc=v=>escapeWhiteboardHtml(String(v??''));
  const kinds=['equivalence_translation','equivalence_flow_table','equivalence_counterexample',
    'equivalence_context','equivalence_domain','equivalence_algebra'];
  const headings={equivalence_translation:'Words become operations',
    equivalence_flow_table:'Test each stated row',equivalence_counterexample:'One shared input, two outputs',
    equivalence_context:'Fixed fee and repeated charge',equivalence_domain:'A rule and its allowed inputs',
    equivalence_algebra:'Transform every term legally'};
  function scene(kind,givens){
    const tile=(v,i)=>`<span class="equiv-given" data-object-id="given-${i+1}">${esc(v)}</span>`;
    if(kind==='equivalence_flow_table')return `<div class="equiv-table" role="group" aria-label="Given input-output rows">${givens.map((v,i)=>`<div class="equiv-table-row"><small>${i<3?'Row '+(i+1):'Candidate '+(i-2)}</small>${tile(v,i)}</div>`).join('')}</div>`;
    if(kind==='equivalence_counterexample')return `<div class="equiv-lanes" role="group" aria-label="Representations compared at a common input">${givens.map((v,i)=>`<div class="equiv-lane"><small>${i<2?'Rule '+String.fromCharCode(65+i):'Given'}</small>${tile(v,i)}</div>`).join('')}</div>`;
    if(kind==='equivalence_context')return `<div class="equiv-context" role="group" aria-label="Fixed amount, repeated amount and input">${givens.map((v,i)=>`<div class="equiv-lane"><small>${i===0?'Fixed once':i===1?'Per unit':'Input or candidate'}</small>${tile(v,i)}</div>`).join('')}</div>`;
    if(kind==='equivalence_domain')return `<div class="equiv-domain" role="group" aria-label="Given relationship and valid input domain">${givens.map((v,i)=>`<div class="equiv-lane"><small>${i===givens.length-1?'Allowed inputs':'Relationship'}</small>${tile(v,i)}</div>`).join('')}</div>`;
    return `<div class="equiv-flow" role="group" aria-label="Given representations">${givens.map((v,i)=>`${i?'<span class="equiv-arrow" aria-hidden="true">→</span>':''}${tile(v,i)}`).join('')}</div>`;
  }
  for(const kind of kinds)AthenaVisualizationRegistry.register('algebra',kind,{
    render(p,state,phase){
      const stage=Number(((state.annotations||[]).find(s=>s.startsWith('stage:'))||'stage:0').slice(6));
      const total=Number(p.total_steps),givens=p.given_objects||[],derived=p.derived_objects||[];
      const final=phase==='result'&&stage>=total;
      const results=derived.map((v,i)=>{
        const revealAt=Math.ceil((i+1)*(total-1)/derived.length);
        const visible=stage>revealAt||(stage===revealAt&&phase==='result');
        return `<div data-object-id="derived-${i+1}" class="equiv-derived ${visible?'is-visible':'is-concealed'}"><small>Derived ${i+1}</small><strong>${visible?esc(v):'?'}</strong></div>`;
      }).join('');
      return `<section class="equiv-board" data-managed-visibility="true" data-question-id="${esc(p.question_id)}" data-family="${esc(kind)}" data-phase="${esc(phase)}" data-stage="${stage}"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(p.prompt)}</span></p><div class="equiv-scene" data-object-id="model"><strong>${esc(headings[kind])}</strong>${scene(kind,givens)}<div class="equiv-results">${results}</div></div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Legal mathematical action</span><strong>${phase==='ready'?'':esc(state.working_state)}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this action</span><strong>${phase==='result'?esc(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Check the original representations</span><strong>${final?esc(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
