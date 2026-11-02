/* Distinct property comparisons and signed-context tracks, with cumulative reasoning. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 AthenaVisualizationRegistry.register('algebra','grade8_integer_reasoning',{
   render(params,state,phase){
     const s=JSON.parse(params.scene_json),stage=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
     const done=phase==='result'?stage:Math.max(0,stage-1),visible=Math.max(0,Math.min((s.rows||[]).length,done-1));
     const last=done===params.total_steps;
     let board='';
     if(s.comparison_expression){
       const a=s.source_expression,b=s.comparison_expression;
       const left=visible>=1?esc(s.rows[0]):'Calculate the left side';
       const right=visible>=2?esc(s.rows[1]):'Calculate the right side';
       board=`<div class="g8-intreason-compare" data-object-id="property-model"><div data-object-id="left-claim"><span>Left</span><strong>${esc(a)}</strong><small>${left}</small></div><div data-object-id="equality-claim">= ?</div><div data-object-id="right-claim"><span>Right</span><strong>${esc(b)}</strong><small>${right}</small></div></div>`;
     }else{
       const label={temperature:'Thermometer',bank:'Balance',elevation:'Elevation',score:'Score'}[s.model]||'Signed change';
       board=`<div class="g8-intreason-context" data-object-id="context-model"><div data-object-id="start-value"><span>${esc(label)} starts at</span><strong>${esc(s.start)} ${esc(s.unit)}</strong></div>${(s.rows||[]).slice(0,visible).map((row,i)=>`<div data-object-id="change-${i+1}"><span>Change ${i+1}</span><strong>${esc(row)}</strong></div>`).join('')}</div>`;
     }
     const history=(s.rows||[]).slice(0,visible).map((row,i)=>`<li data-object-id="reason-${i+1}">${esc(row)}</li>`).join('');
     return `<section class="g8-intreason-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${esc(params.prompt)}</p><div data-object-id="model">${board}</div><ol aria-label="Worked reasoning so far">${history}</ol><p data-object-id="operation">${phase==='ready'?'':esc(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!last?esc(state.after_state||''):''}</p><p data-object-id="verification">${last?`Answer: ${esc(s.answer)}. ${esc(s.memo)}`:''}</p></section>`;
   },destroy(){}
 });
})();
