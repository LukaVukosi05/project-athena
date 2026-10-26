/* Grade 8 Expressions Lesson 10: the original, learner claim and repair remain visible. */
(() => {
  const esc = value => escapeWhiteboardHtml(String(value ?? ''));
  const families = ['term_sort','signed_terms','factor_array','distribution_paths',
    'signed_distribution','quotient_lanes','exponent_scope','root_pairs',
    'parallel_paths','mixed_trace','restricted_quotient','context_receipt',
    'area_split','parallel_flows','integrated_trace'];
  const name = {
    term_sort:'Sort unlike terms',signed_terms:'Attach each sign',factor_array:'Multiply every factor',
    distribution_paths:'Draw both product arrows',signed_distribution:'Distribute negative one',
    quotient_lanes:'Divide each numerator term',exponent_scope:'Circle the exponent base',
    root_pairs:'Compare paired signed inputs',parallel_paths:'Test two claimed forms',
    mixed_trace:'Follow the first incorrect arrow',restricted_quotient:'Check the original divisor',
    context_receipt:'Separate once-only and repeated charges',area_split:'Split both area regions',
    parallel_flows:'Keep both operation orders',integrated_trace:'Repair both brackets in sequence'
  };
  function picture(family, given) {
    const label = (index) => esc(given[index] || '');
    if (family === 'area_split') return `<svg viewBox="0 0 360 155" class="diagnostic-ex-shape" role="img" aria-label="Split rectangle with given length ${label(0)} and width ${label(1)}"><rect x="40" y="30" width="260" height="95"/><line x1="190" x2="190" y1="30" y2="125"/><text x="99" y="22">${label(0)}</text><text x="5" y="85">${label(1)}</text><text x="92" y="80">part 1</text><text x="213" y="80">part 2</text></svg>`;
    if (family === 'distribution_paths' || family === 'signed_distribution' || family === 'mixed_trace' || family === 'integrated_trace') return `<div class="diagnostic-ex-arrows" role="img" aria-label="Two distribution branches"><span class="diagnostic-ex-factor">${label(family==='distribution_paths'?0:family==='signed_distribution'?1:2)}</span><span aria-hidden="true">↙ &nbsp; ↘</span><span>${label(family==='distribution_paths'?1:0)}</span><span>${label(family==='distribution_paths'?2:family==='signed_distribution'?2:3)}</span></div>`;
    if (family === 'quotient_lanes' || family === 'restricted_quotient') return `<div class="diagnostic-ex-quotients"><span>${label(0)} / ${label(2) || label(1)}</span><span>${label(1)} / ${label(2) || label(1)}</span></div>`;
    if (family === 'factor_array' || family === 'exponent_scope' || family === 'root_pairs') return `<div class="diagnostic-ex-factors" role="group" aria-label="Given factor and scope model">${given.map(value=>`<span>${esc(value)}</span>`).join('')}</div>`;
    if (family === 'parallel_paths' || family === 'parallel_flows') return `<div class="diagnostic-ex-parallel"><div><b>Path A</b><span>${label(0)}</span></div><div><b>Path B</b><span>${label(1)}</span></div></div>`;
    if (family === 'context_receipt') return `<div class="diagnostic-ex-receipt"><span>${label(0)} outside repeated groups</span><span>${label(1)} in each group</span><span>${label(2)}</span></div>`;
    if (family === 'term_sort' || family === 'signed_terms') return `<div class="diagnostic-ex-parallel"><div><b>Term 1</b>${label(0)}</div><div><b>Term 2</b>${label(1)}</div></div>`;
    return '';
  }
  for(const family of families) AthenaVisualizationRegistry.register('algebra',`diagnostic_${family}`,{
    render(p,state,phase){
      const stage = Number(((state.annotations||[]).find(item=>item.startsWith('stage:'))||'stage:0').slice(6));
      const tokens=p.model_tokens||[], count=p.model_scene?.input_count||2;
      const final=phase==='result'&&stage>=Number(p.total_steps)-1;
      const given=tokens.slice(0,count), derived=tokens.slice(count);
      const objects=tokens.map((value,index)=>{
        const visible=index<count||final, active=phase!=='ready'&&index===Math.min(stage-1,count-1);
        return `<div class="diagnostic-ex-object ${visible?'':'is-concealed'} ${active?'is-active':''}" data-object-id="token-${index+1}"><small>${index<count?'Original / claim':'Derived after repair'}</small><strong>${visible?esc(value):'?'}</strong></div>`;
      }).join('');
      const action=phase==='operation' ? `<div class="diagnostic-ex-action"><small>Apply this legal operation</small><strong>${esc(state.working_state)}</strong></div>` : '';
      const result=phase==='result'?`<div class="diagnostic-ex-action diagnostic-ex-action--result"><small>${final?'Verified conclusion':'Result of this operation'}</small><strong>${esc(state.after_state)}</strong></div>`:'';
      return `<section class="diagnostic-ex-visual" data-family="${esc(family)}" data-question-id="${esc(p.question_id)}" data-phase="${esc(phase)}" data-stage="${stage}" data-managed-visibility="true"><p class="g8-original"><strong>Original and learner claim</strong><span data-object-id="problem">${esc(p.prompt)}</span></p><div class="diagnostic-ex-scene" data-object-id="model"><strong>${esc(name[family])}</strong>${picture(family,given)}<div class="diagnostic-ex-objects">${objects}</div></div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase!=='ready'?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${phase!=='ready'?esc(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${phase==='result'?esc(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?esc(state.after_state):''}</strong></div></div></div>${action}${result}</section>`;
    },destroy(){}
  });
})();
