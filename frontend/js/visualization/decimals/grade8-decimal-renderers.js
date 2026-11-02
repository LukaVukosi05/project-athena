/* Question-specific place columns and midpoint number lines, no result in the initial stage. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 const unit=x=>Math.round(Number(x)*100000);
 const format=(integer,places)=> (integer/100000).toFixed(places);
 const row=(v,stage,target)=>{
  const [whole,decimal='']=String(v).split('.'),digits=decimal.padEnd(4,'0');
  return `<div class="g8-dec-row" data-value="${esc(v)}"><span class="g8-dec-whole ${stage>=2&&target===-1?'g8-dec-active':''}">${stage>=1?esc(whole):'·'}</span><span aria-hidden="true">.</span>${digits.split('').map((digit,j)=>`<span class="g8-dec-digit ${stage>=2&&j===target?'g8-dec-active':''}" data-place="${j+1}">${stage>=1?esc(digit):'·'}</span>`).join('')}</div>`;
 };
 function columns(s,stage){
  const kind=s.kind,nums=kind==='place'?[s.values[0]]:s.values;
  const positions={tenths:0,hundredths:1,thousandths:2};
  let target=kind==='place'?positions[s.values[1]]:-1;
  if(kind!=='place'){
   const aligned=nums.map(v=>String(v).split('.')[0].padStart(4,'0')+'.'+String(v).split('.')[1]?.padEnd(4,'0'));
   const indexes=[...Array(9).keys()].filter(i=>i!==4);
   const different=indexes.find(i=>new Set(aligned.map(v=>v[i])).size>1);
   target=different===undefined?-2:different>4?different-5:-1;
  }
  let out=`<div class="g8-dec-columns" role="img" aria-label="${esc('Place-value columns for '+nums.join(', '))}"><div class="g8-dec-head"><span>whole</span><span>point</span><span>tenths</span><span>hundredths</span><span>thousandths</span><span>ten-thousandths</span></div>`;
  nums.forEach(v=>out+=row(v,stage,target));out+='</div>';
  if(kind==='place'&&stage>=3)out+=`<p data-object-id="selected-column">Read the highlighted ${esc(s.values[1])} digit.</p>`;
  if(kind!=='place'&&stage>=3){
   const numeric=nums.map(Number),low=Math.min(...numeric),high=Math.max(...numeric),span=high-low||1;
   out+=`<svg viewBox="0 0 500 96" role="img" aria-label="${esc('Number line containing '+nums.join(', '))}"><path d="M35 47 H465" stroke="currentColor" stroke-width="2"/>`;
   nums.forEach((v,i)=>{
    const x=35+430*(numeric[i]-low)/span;
    out+=`<circle cx="${x}" cy="47" r="5" fill="#3288aa"/><path d="M${x} 47 L${x} 58" stroke="#3288aa"/><circle cx="${45+i*145}" cy="79" r="4" fill="#3288aa"/><text x="${55+i*145}" y="83" font-size="12">${esc(v)}</text>`;
   });out+='</svg>';
  }
  return out;
 }
 function axis(raw,places,stage,y,label){
  const step=10**(5-places),value=unit(raw),lower=Math.floor(value/step)*step,upper=lower+step,mid=lower+step/2,x=45+400*(value-lower)/step;
  let out=`<g><text x="10" y="${y-28}" font-size="12">${esc(label)}</text><path d="M45 ${y} H445" stroke="currentColor" stroke-width="2"/>`;
  const mark=(u,tx)=>`<path d="M${tx} ${y-7} V${y+7}" stroke="currentColor"/><text x="${tx-15}" y="${y+27}" font-size="11">${esc(format(u,places))}</text>`;
  out+=mark(lower,45)+mark(upper,445);
  if(stage>=2)out+=`<path d="M245 ${y-8} V${y+8}" stroke="#ba6420"/><text x="224" y="${y-12}" font-size="11">${esc(format(mid,places+1))}</text>`;
  if(stage>=3)out+=`<circle cx="${x}" cy="${y}" r="6" fill="#3288aa"/><text x="${Math.max(10,Math.min(425,x-14))}" y="${y-18}" font-size="12">${esc(raw)}</text>`;
  if(stage>=4)out+=`<path d="M${x} ${y-26} L${value>=mid?445:45} ${y-26}" stroke="#3288aa" stroke-width="2" marker-end="url(#dec-arrow)"/>`;
  return out+'</g>';
 }
 function rounding(s,stage){
  const estimate=s.kind==='estimate',places=Number(s.values[estimate?2:1]);
  let svg=`<svg viewBox="0 0 500 ${estimate?265:150}" role="img" aria-label="${esc(estimate?'Two original decimal values, separately rounded':'Original value between neighbouring rounding marks')}"><defs><marker id="dec-arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#3288aa"/></marker></defs>`;
  svg+=axis(s.values[0],places,stage,75,'First value');
  if(estimate&&stage>=2)svg+=axis(s.values[1],places,stage,193,'Second value');
  return svg+'</svg>';
 }
 function register(name,visual){AthenaVisualizationRegistry.register('algebra',name,{
  render(params,state,phase){
   const s=JSON.parse(params.scene_json),requested=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
   const stage=phase==='result'?requested:Math.max(0,requested-1),complete=stage===params.total_steps;
   const rows=(s.rows||[]).slice(0,Math.max(0,Math.min(3,stage-1))).map((line,i)=>`<li data-object-id="reason-${i+1}">${esc(line)}</li>`).join('');
   return `<section class="g8-decimal-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${esc(params.prompt)}</p><div data-object-id="model" class="g8-decimal-visual"><div class="g8-decimal-givens">${s.values.map((value,i)=>`<span data-object-id="decimal-${i+1}">${esc(value)}</span>`).join(' ')}</div>${visual(s,stage)}</div><ol aria-label="Worked solution so far">${rows}</ol><p data-object-id="operation">${phase==='ready'?'':esc(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!complete?esc(state.after_state||''):''}</p><p data-object-id="verification">${complete?`Answer: ${esc(s.answer)}. ${esc(s.memo)}`:''}</p></section>`;
  },destroy(){}
 });}
 register('grade8_decimal_columns',columns);register('grade8_decimal_rounding',rounding);
})();
