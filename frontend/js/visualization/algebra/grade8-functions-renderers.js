/* Question-driven flows and tables for Grade 8 functions and relationships. */
(() => {
  const esc=v=>escapeWhiteboardHtml(String(v??''));
  const families=['function_flow','function_table','function_reverse','function_context','function_compare'];
  const title={function_flow:'Follow the input through each arrow',
    function_table:'Test every input-output row',function_reverse:'Undo arrows from the output',
    function_context:'Separate fixed and repeated quantities',function_compare:'Use the same input in both rules'};
  function visual(family,given,phase,state){
    const cell=v=>`<span class="function-ex-cell">${esc(v)}</span>`;
    if(family==='function_table')return `<div class="function-ex-table" role="group" aria-label="Given input and output rows">${given.map((v,i)=>`<div data-row="${i+1}"><small>Given row ${i+1}</small>${cell(v)}</div>`).join('')}</div>`;
    if(family==='function_compare')return `<div class="function-ex-parallel"><div><b>Rule A</b>${cell(given[0])}</div><div><b>Rule B</b>${cell(given[1])}</div><div><b>Shared input</b>${cell(given[2])}</div></div>`;
    if(family==='function_context')return `<div class="function-ex-context"><span class="function-ex-fixed">${cell(given[0])}<small>once or per unit as stated</small></span><span>${cell(given[1])}<small>count or rate</small></span>${given.slice(2).map(cell).join('')}</div>`;
    const reverse=family==='function_reverse'&&phase!=='ready';
    const flow=given.map((v,i)=>`${i?`<span class="function-ex-arrow" aria-hidden="true">${reverse?'←':'→'}</span>`:''}${cell(v)}`).join('');
    return `<div class="function-ex-flow" role="group" aria-label="${esc(reverse?'Undo the given flow from output to input':'Given flow in reading order')}">${flow}</div>`;
  }
  for(const family of families)AthenaVisualizationRegistry.register('algebra',family,{
    render(p,state,phase){
      const stage=Number(((state.annotations||[]).find(v=>v.startsWith('stage:'))||'stage:0').slice(6));
      const givens=p.given_objects||[],derived=p.derived_objects||[];
      const totalSteps=Number(p.total_steps);
      const final=phase==='result'&&stage>=totalSteps;
      const inputObjects=givens.map((v,i)=>`<span class="function-ex-semantic ${phase!=='ready'&&i===Math.min(stage-1,givens.length-1)?'is-active':''}" data-object-id="given-${i+1}">${esc(v)}</span>`).join('');
      const outputObjects=derived.map((v,i)=>{
        const revealAt=Math.ceil((i+1)*(totalSteps-1)/derived.length);
        const visible=stage>revealAt||(stage===revealAt&&phase==='result');
        return `<span class="function-ex-semantic function-ex-output ${visible?'':'is-concealed'}" data-object-id="derived-${i+1}">${visible?esc(v):'?'}</span>`;
      }).join('');
      return `<section class="function-ex-visual" data-family="${esc(family)}" data-question-id="${esc(p.question_id)}" data-phase="${esc(phase)}" data-stage="${stage}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(p.prompt)}</span></p><div class="function-ex-scene" data-object-id="model"><strong>${esc(title[family])}</strong>${visual(family,givens,phase,state)}<div class="function-ex-objects">${inputObjects}${outputObjects}</div></div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Apply this rule</span><strong>${phase==='ready'?'':esc(state.working_state)}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this arrow</span><strong>${phase==='result'?esc(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked against the original</span><strong>${final?esc(state.after_state):''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
