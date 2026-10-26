/* Grade 8 Lesson 9: diagrams derive only from this question's given quantities. */
(() => {
  const esc=v=>escapeWhiteboardHtml(String(v??''));
  const families=['unit_receipt','fixed_variable_receipt','flow_rule','input_table','fare_table',
    'decrease_timeline','packs_plus_loose','context_perimeter','plan_comparison','fee_error',
    'equivalence_models','general_table','split_area_context','parallel_flows','fundraiser_audit'];
  const labels={unit_receipt:'One unit price per page',fixed_variable_receipt:'One fixed fee plus a changing cost',
    flow_rule:'Follow the arrows in order',input_table:'Compare input-output rows',
    fare_table:'Tickets and one booking fee',decrease_timeline:'Start volume and equal losses',
    packs_plus_loose:'Packs and loose pencils',context_perimeter:'Trace all four sides',
    plan_comparison:'Separate plans, one input',fee_error:'Spot the repeated fixed fee',
    equivalence_models:'Two descriptions of one rule',general_table:'One rule for every row',
    split_area_context:'Split the rectangle into two regions',parallel_flows:'Operation order changes the output',
    fundraiser_audit:'Separate sales from the one donation'};
  function scene(family,p,state,phase,stage){
    const tokens=p.model_tokens||[],count=p.model_scene?.input_count||2,final=phase==='result'&&stage>=Number(p.total_steps)-1;
    const obj=(token,i)=>`<div class="context-ex-object ${i>=count?'context-ex-object--derived':''} ${i>=count&&!final?'is-concealed':''} ${phase!=='ready'&&i===Math.min(stage-1,count-1)?'is-active':''}" data-object-id="token-${i+1}"><small>${i>=count?'Derived value':family==='input_table'||family==='general_table'||family==='fare_table'?'Table input or given':family==='parallel_flows'?'Flow or input':'Scenario quantity'}</small><strong>${i<count||final?esc(token):'?'}</strong></div>`;
    const given=tokens.slice(0,count).map(obj).join(''),derived=tokens.slice(count).map((v,i)=>obj(v,count+i)).join('');
    const isTable=['input_table','fare_table','general_table','fundraiser_audit'].includes(family);
    const isFlow=['flow_rule','parallel_flows','equivalence_models'].includes(family);
    let picture='';
    if(family==='context_perimeter')picture=`<svg class="context-ex-shape" viewBox="0 0 390 170" role="img" aria-label="Rectangle with the four supplied sides"><rect x="78" y="32" width="220" height="105"/><text x="180" y="24">${esc(tokens[0])}</text><text x="308" y="85">${esc(tokens[1])}</text><text x="180" y="160">${esc(tokens[2])}</text><text x="5" y="85">${esc(tokens[3])}</text></svg>`;
    if(family==='split_area_context')picture=`<svg class="context-ex-shape" viewBox="0 0 390 170" role="img" aria-label="Area split into two parts with supplied length and width"><rect x="54" y="36" width="280" height="108"/><line x1="220" y1="36" x2="220" y2="144"/><text x="94" y="22">${esc(tokens[0])}</text><text x="6" y="93">${esc(tokens[1])}</text><text x="110" y="96">region 1</text><text x="248" y="96">region 2</text></svg>`;
    if(family==='decrease_timeline')picture=`<div class="context-ex-volume" role="img" aria-label="Starting volume ${esc(tokens[0])}; equal loss ${esc(tokens[1])}"><span>${esc(tokens[0])}</span><span>− ${esc(tokens[1])} × ${esc(tokens[2])}</span></div>`;
    if(family==='packs_plus_loose')picture=`<div class="context-ex-groups" role="img" aria-label="${esc(tokens[0])} groups of ${esc(tokens[1])} plus ${esc(tokens[2])}"><span class="context-ex-pack">${esc(tokens[0])} × ${esc(tokens[1])}</span><span class="context-ex-pack">${esc(tokens[2])} outside packs</span></div>`;
    if(family==='plan_comparison'||family==='parallel_flows'||family==='equivalence_models')picture=`<div class="context-ex-comparison"><div><strong>Path A</strong><span>${esc(tokens[0])}</span></div><div><strong>Path B</strong><span>${esc(tokens[family==='plan_comparison'?2:1])}</span></div></div>`;
    if(family==='fee_error'||family==='fundraiser_audit')picture=`<p class="context-ex-claim">Inspect the claim: ${esc(tokens[family==='fee_error'?2:3])}</p>`;
    if(family==='flow_rule')picture=`<div class="context-ex-flow">${tokens.slice(0,count).map((v,i)=>`<span>${esc(v)}</span>${i<count-1?'<b aria-hidden="true">→</b>':''}`).join('')}</div>`;
    const kind=isTable?'context-ex-table':isFlow?'context-ex-flow-input':'context-ex-quantities';
    const move=phase==='operation'?`<div class="context-ex-progress"><small>Now apply</small><strong>${esc(state.working_state)}</strong></div>`:phase==='result'?`<div class="context-ex-progress context-ex-progress--result"><small>Current result</small><strong>${esc(state.after_state)}</strong></div>`:'';
    return `<div class="context-ex-scene context-ex-scene--${esc(family)}" data-object-id="model" role="group" aria-label="${esc(labels[family])}"><strong>${esc(labels[family])}</strong>${picture}<div class="${kind}">${given}</div>${move}<div class="context-ex-output">${derived}</div></div>`;
  }
  for(const family of families) AthenaVisualizationRegistry.register('algebra',family,{render(p,state,phase){
    const stage=Number(((state.annotations||[]).find(v=>v.startsWith('stage:'))||'stage:0').slice(6));
    const active=phase!=='ready',result=phase==='result',final=result&&stage>=Number(p.total_steps)-1;
    return `<section class="context-ex-visual" data-family="${esc(family)}" data-question-id="${esc(p.question_id)}" data-phase="${esc(phase)}" data-stage="${stage}" data-managed-visibility="true"><p class="g8-original"><strong>Original question</strong><span data-object-id="problem">${esc(p.prompt)}</span></p>${scene(family,p,state,phase,stage)}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state)}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${active?'is-visible':'is-hidden'}"><span>Mathematical action</span><strong>${active?esc(state.working_state):''}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${result&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${result?esc(state.after_state):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Checked conclusion</span><strong>${final?esc(state.after_state):''}</strong></div></div></div></section>`;
  },destroy(){}});
})();
