/* Question-bound parallel rule paths. Previous mathematical states remain visible. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  const substitution=(rule,x)=>{
    const terms=[];
    if(rule.a) terms.push(`${rule.a} × (${x})²`);
    if(rule.b) terms.push(`${rule.b} × (${x})`);
    if(rule.c || !terms.length) terms.push(String(rule.c));
    return terms.join(' + ').replace(/\+ -/g,'− ');
  };
  for(const family of ['relationship_match','relationship_repair']) AthenaVisualizationRegistry.register('algebra',family,{
    render(p,state,phase){
      const scene=JSON.parse(p.scene_json),stage=Number(((state.annotations||[]).find(v=>v.startsWith('stage:'))||'stage:0').slice(6));
      const completed=phase==='result'?stage:stage-1;
      const final=phase==='result'&&stage>=p.total_steps;
      const candidates=scene.candidates.map((rule,i)=>{
        const showValue=completed>=2;
        const showChoice=final;
        const label=scene.mode==='repair'&&i===1&&!showChoice?'Repair path':rule.label;
        return `<div class="relation-path ${showChoice&&rule.label===scene.chosen?'is-chosen':''}" data-object-id="candidate-${i+1}"><span class="relation-rule">${esc(label)}</span><span class="relation-substitution" data-object-id="substitution-${i+1}">${completed>=1?`input ${esc(scene.input)} → ${esc(substitution(rule,scene.input))}`:'Input waits for substitution'}</span><strong data-object-id="value-${i+1}">${showValue?esc(rule.value):'?'}</strong></div>`;
      }).join('');
      const givens=p.given_objects.map((v,i)=>`<span data-object-id="given-${i+1}">${esc(v)}</span>`).join('');
      const derived=p.derived_objects.map((v,i)=>`<span class="${final?'':'is-concealed'}" data-object-id="derived-${i+1}">${final?esc(v):'?'}</span>`).join('');
      return `<section class="relation-board" data-managed-visibility="true" data-phase="${esc(phase)}" data-question-id="${esc(p.question_id)}"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(p.prompt)}</span></p><div class="relation-scene" data-object-id="model"><strong>${scene.mode==='repair'?'Diagnose the first wrong step':'Match the representations'}</strong><div class="relation-givens">${givens}</div><p class="relation-input">Test the same input: <b>${esc(scene.input)}</b></p><div class="relation-paths">${candidates}</div><div class="relation-derived">${derived}</div></div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Mathematical action</span><strong>${phase==='ready'?'':esc(state.working_state)}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${phase==='result'?esc(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Check the original</span><strong>${final?esc(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
