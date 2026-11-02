/* Signed groups and staged expressions, one question-specific mathematical action at a time. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  AthenaVisualizationRegistry.register('algebra','grade8_integer_operations',{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json);
      const stage=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
      const done=phase==='result'?stage:Math.max(0,stage-1);
      const final=done===params.total_steps;
      const rows=scene.rows||[];
      const show=Math.max(0,Math.min(rows.length,done-1));
      let visual='';
      if(scene.model==='groups'){
        const parsed=scene.source_expression.match(/^\(?(-?\d+)\)?\*\(?(-?\d+)\)?$/);
        const a=parsed?Number(parsed[1]):0,b=parsed?Number(parsed[2]):0;
        const groups=Math.min(12,Math.max(Math.abs(a),Math.abs(b)));
        const unit=Math.min(12,Math.min(Math.abs(a),Math.abs(b)));
        const negative=(a<0)!==(b<0);
        visual=`<div class="g8-intop-groups" data-object-id="groups" aria-label="${esc(groups)} groups of ${esc(unit)}; ${negative?'negative':'positive'} product">${Array.from({length:groups},(_,i)=>`<span class="g8-intop-group" data-object-id="group-${i+1}">${show>=1?`${esc(unit)} ${negative?'negative':'positive'} counters`:''}</span>`).join('')}</div>`;
      }else if(scene.model==='sign_pattern'){
        const left=scene.source_expression.split('*')[0];
        visual=`<div class="g8-intop-pattern" data-object-id="sign-pattern"><span>${esc(left)} × 2</span><span>${esc(left)} × 1</span><span>${esc(left)} × 0</span><span>${show>=1?`${esc(left)} × (−1) → continue in equal steps`: 'Continue the product pattern'}</span></div>`;
      }else if(scene.model==='inverse'){
        visual=`<div class="g8-intop-inverse" data-object-id="inverse"><strong>${esc(scene.expression)}</strong><span>÷ undoes ×</span><span>${show>=2?esc(scene.rows[1]):'Find the missing factor'}</span></div>`;
      }else if(scene.model==='powers'){
        const pieces=scene.source_expression.match(/\(?-?\d+\)?\*\*\d+/);
        visual=`<div class="g8-intop-power" data-object-id="power-base"><span>Base: ${esc(pieces?pieces[0].split('**')[0]:'?')}</span><span>Exponent: ${esc(pieces?pieces[0].split('**')[1]:'?')}</span><span>${show>=1?esc(scene.rows[0]):'Circle the exact base first'}</span></div>`;
      }else if(scene.model==='roots'){
        visual=`<div class="g8-intop-root" data-object-id="root-inverse"><span>${esc(scene.expression)}</span><span>${show>=1?esc(scene.rows[0]):'Which number raises to the radicand?'}</span></div>`;
      }else{
        visual=`<div class="g8-intop-order" data-object-id="order-lane"><span>${esc(scene.expression)}</span><span>${show>=1?esc(scene.rows[0]):'Identify the first operation'}</span></div>`;
      }
      const history=rows.slice(0,show).map((row,i)=>`<li data-object-id="reason-${i+1}">${esc(row)}</li>`).join('');
      return `<section class="g8-intop-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${esc(params.prompt)}</p><div data-object-id="model">${visual}</div><ol class="g8-intop-history" aria-label="Worked reasoning so far">${history}</ol><div data-object-id="operation" class="g8-intop-operation">${phase==='ready'?'':esc(state.working_state||'')}</div><div data-object-id="result" class="g8-intop-result">${phase==='result'&&!final?esc(state.after_state||''):''}</div><div data-object-id="verification" class="g8-intop-check">${final?`Answer: ${esc(scene.answer)}. ${esc(scene.memo)}`:''}</div></section>`;
    },destroy(){}
  });
})();
