/* Original factors -> scale -> one partial product or quotient digit per state -> reverse check. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 function multiplication(scene,stage){
  const [a,b]=scene.values,left=Number(a.replace('.','')),right=Number(b.replace('.',''));
  const p=a.split('.')[1].length,q=b.split('.')[1].length;
  const digits=String(right).split('').reverse();const parts=digits.map((d,j)=>left*Number(d)*10**j);
  let html=`<div class="g8-dec-operation-frame" role="img" aria-label="${esc(`Multiply ${a} by ${b} with aligned partial products`)}"><div class="g8-dec-factor-row"><span data-object-id="factor-a">${esc(a)}</span><span>×</span><span data-object-id="factor-b">${esc(b)}</span></div>`;
  if(stage>=2)html+=`<p class="g8-dec-op-scale">First factor: ${esc(a)} = ${left} ÷ 10<sup>${p}</sup></p>`;
  if(stage>=3)html+=`<p class="g8-dec-op-scale">Second factor: ${esc(b)} = ${right} ÷ 10<sup>${q}</sup></p>`;
  const visible=Math.max(0,Math.min(digits.length,stage-3));
  if(visible)html+='<div class="g8-dec-partials" aria-label="Aligned integer partial products">'+parts.slice(0,visible).map((part,j)=>`<div data-object-id="partial-${j+1}" class="g8-dec-partial ${j===visible-1?'g8-dec-current':''}"><span>${left} × ${esc(digits[j])} × 10<sup>${j}</sup></span><strong>${String(part).padStart(String(parts.reduce((x,y)=>x+y,0)).length,' ')}</strong></div>`).join('')+'</div>';
  if(stage>=4+digits.length)html+=`<p data-object-id="partial-sum" class="g8-dec-op-sum">Sum of aligned products: ${parts.reduce((x,y)=>x+y,0)}</p>`;
  if(stage>=5+digits.length)html+=`<p data-object-id="decimal-shift" class="g8-dec-op-shift">Restore ${p} + ${q} = ${p+q} decimal places.</p>`;
  return html+'</div>';
 }
 function division(scene,stage){
  const [a,b]=scene.values,p=a.split('.')[1].length,q=b.split('.')[1].length,scale=10**Math.max(p,q);
  const N=Math.round(Number(a)*scale),D=Math.round(Number(b)*scale),rows=scene.rows||[];
  const digits=rows.slice(2,-1).map(line=>({digit:(line.match(/gives digit (\d+)/)||[])[1],remainder:(line.match(/remainder (\d+)/)||[])[1],decimal:line.startsWith('Add a decimal zero')}));
  const visible=Math.max(0,Math.min(digits.length,stage-3));
  let html=`<div class="g8-dec-operation-frame" role="img" aria-label="${esc(`Divide ${a} by ${b}, scaling both and recording each quotient digit`)}"><div class="g8-dec-factor-row"><span data-object-id="factor-a">${esc(a)}</span><span>÷</span><span data-object-id="factor-b">${esc(b)}</span></div>`;
  if(stage>=2)html+=`<p class="g8-dec-op-scale">Scale BOTH quantities by 10<sup>${Math.max(p,q)}</sup>.</p>`;
  if(stage>=3)html+=`<div class="g8-dec-division-bracket" data-object-id="scaled-division"><span>${D}</span><span class="g8-dec-dividend">${N}</span></div>`;
  if(visible){
   html+='<div class="g8-dec-quotient" aria-label="Quotient digits so far">';
   digits.slice(0,visible).forEach((x,j)=>{
    if(x.decimal&&!digits[j-1]?.decimal)html+='<span class="g8-dec-point">.</span>';
    html+=`<span data-object-id="quotient-digit-${j+1}" class="g8-dec-q-digit ${j===visible-1?'g8-dec-current':''}">${esc(x.digit??'?')}</span>`;
   });html+='</div>';
   const last=digits[visible-1];html+=`<p data-object-id="current-remainder">Remainder after this digit: ${esc(last.remainder??'?')}</p>`;
  }
  if(stage>=rows.length+1)html+='<p data-object-id="decimal-quotient">Read the completed quotient below and verify by multiplication.</p>';
  return html+'</div>';
 }
 function register(template,model){AthenaVisualizationRegistry.register('algebra',template,{
  render(params,state,phase){
   const scene=JSON.parse(params.scene_json),requested=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
   const stage=phase==='result'?requested:Math.max(0,requested-1),complete=stage===params.total_steps;
   const rows=(scene.rows||[]).slice(0,Math.max(0,Math.min(scene.rows.length,stage-1))).map((row,i)=>`<li data-object-id="reason-${i+1}">${esc(row)}</li>`).join('');
   const givens=scene.values.map((v,j)=>`<span data-object-id="decimal-${j+1}">${esc(v)}</span>`).join(' · ');
   return `<section class="g8-decimal-board g8-decimal-operations" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${esc(params.prompt)}</p><div data-object-id="model" class="g8-decimal-visual"><div class="g8-decimal-givens">Given: ${givens}</div>${model(scene,stage)}</div><ol aria-label="Worked solution so far">${rows}</ol><p data-object-id="operation">${phase==='ready'?'':esc(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!complete?esc(state.after_state||''):''}</p><p data-object-id="verification">${complete?`Answer: ${esc(scene.answer)}. ${esc(scene.memo)}`:''}</p></section>`;
  },destroy(){}
 });}
 register('grade8_decimal_product',multiplication);register('grade8_decimal_quotient',division);
})();

/* Powers and principal roots: the current factor or candidate is revealed at its own stage. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 function renderModel(scene,stage){
  const degree=Number(scene.values[1]),raw=scene.values[0],isPower=scene.kind==='power';
  let html=`<div class="g8-dec-operation-frame g8-dec-powers" role="group" aria-label="${esc(isPower?'Repeated factors of '+raw:'Root search for '+raw)}"><div class="g8-dec-factor-row"><span data-object-id="power-given">${isPower?`(${esc(raw)})<sup>${degree}</sup>`:`${degree===2?'√':'∛'}${esc(raw)}`}</span></div>`;
  if(isPower){
   if(stage>=2) html+=`<p data-object-id="power-exponent">${degree} equal factors</p>`;
   if(stage>=3)html+=`<div class="g8-dec-factor-tiles" aria-label="Repeated decimal factors">${Array.from({length:degree},(_,i)=>`<span data-object-id="factor-${i+1}" class="g8-dec-factor-tile">${esc(raw)}</span>`).join('<span>×</span>')}</div>`;
   if(stage>=4)html+=`<p data-object-id="power-scale">Count decimal places in each factor: ${raw.split('.')[1].length} × ${degree}.</p>`;
   if(stage>=5)html+=`<p data-object-id="power-integer">Integer product: ${esc(raw.replace('.',''))}<sup>${degree}</sup>.</p>`;
  }else{
   if(stage>=2)html+=`<p data-object-id="root-index">Find a non-negative number whose ${degree===2?'square':'cube'} is ${esc(raw)}.</p>`;
   if(stage>=3)html+=`<p data-object-id="root-estimate">Estimate its size before calculating.</p>`;
   // The candidate remains concealed until the authored test step has been reached.
   if(stage>=4){const test=(scene.rows[2].match(/^Test (.+?) as a candidate/ )||[])[1];html+=`<div class="g8-dec-factor-tiles" aria-label="Candidate test">${Array.from({length:degree},(_,i)=>`<span data-object-id="root-factor-${i+1}" class="g8-dec-factor-tile">${esc(test)}</span>`).join('<span>×</span>')}</div>`;}
   if(stage>=6)html+=`<p data-object-id="root-check">Check every factor against the original radicand ${esc(raw)}.</p>`;
  }
  return html+'</div>';
 }
 for(const [kind,template] of [['power','grade8_decimal_power'],['root','grade8_decimal_root']]){
  AthenaVisualizationRegistry.register('algebra',template,{render(params,state,phase){
   const scene=JSON.parse(params.scene_json),requested=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
   const stage=phase==='result'?requested:Math.max(0,requested-1),complete=stage===params.total_steps;
   const rows=(scene.rows||[]).slice(0,Math.max(0,Math.min(scene.rows.length,stage-1))).map((row,i)=>`<li data-object-id="reason-${i+1}">${esc(row)}</li>`).join('');
   return `<section class="g8-decimal-board g8-decimal-operations" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${esc(params.prompt)}</p><div data-object-id="model" class="g8-decimal-visual">${renderModel(scene,stage)}</div><ol aria-label="Worked solution so far">${rows}</ol><p data-object-id="operation">${phase==='ready'?'':esc(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!complete?esc(state.after_state||''):''}</p><p data-object-id="verification">${complete?`Answer: ${esc(scene.answer)}. ${esc(scene.memo)}`:''}</p></section>`;
  },destroy(){}});
 }
})();
