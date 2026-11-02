/* Grade 8 exponent visuals: original base, factor groups, cancellations and decimal shifts. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 const sup=n=>String(n).replace(/[0-9]/g,d=>'⁰¹²³⁴⁵⁶⁷⁸⁹'[Number(d)]);
 const symbol=s=>{const v=s.values,k=s.kind;if(k==='science')return v[0];if(k==='zero')return v[0]+'⁰';if(k==='power_product')return String(Number(v[0])*Number(v[1]))+sup(v[2]);if(k==='mixed')return `${v[0]}${sup(v[1])} × ${v[0]}${sup(v[2])} ÷ ${v[0]}${sup(v[3])}`;if(k==='product'||k==='quotient')return `${v[0]}${sup(v[1])} ${k==='product'?'×':'÷'} ${v[0]}${sup(v[2])}`;return `${k==='negative'?'('+v[0]+')':v[0]}${sup(v[1])}${k==='compare'?' ? '+v[2]:''}`;};
 const tiles=(base,count,prefix)=>Array.from({length:count},(_,i)=>`<span data-object-id="${prefix}-${i+1}" class="g8-exp-tile">${esc(base)}</span>`).join('<span aria-hidden="true">×</span>');
 function model(s,stage){
  const v=s.values,kind=s.kind;
  let out=`<div class="g8-exponent-stage" role="group" aria-label="${esc('Visual for '+s.problem)}"><p data-object-id="exponent-given">${esc(symbol(s))}</p>`;
  if(kind==='science'){
   const raw=v[0],places=raw.length-1;
   if(stage>=2)out+=`<div class="g8-exp-digit-row" aria-label="Original digit places">${[...raw].map((digit,i)=>`<span data-object-id="digit-${i+1}" class="g8-exp-tile">${digit}</span>`).join('')}</div>`;
   if(stage>=3)out+=`<p data-object-id="original-point">Original decimal point: ${esc(raw)}.</p>`;
   if(stage>=4)out+=`<p data-object-id="shift-count">Shift left ${places} positions <span aria-hidden="true">←</span></p>`;
   if(stage>=5)out+=`<p data-object-id="coefficient">Coefficient: ${esc(raw[0]+(raw.slice(1).replace(/0+$/,'')?'.'+raw.slice(1).replace(/0+$/,''):''))}</p>`;
   if(stage>=6)out+=`<p data-object-id="ten-power">Compensate with 10<sup>${places}</sup></p>`;
  }else if(kind==='expand'||kind==='negative'||kind==='compare'){
   const [base,exponent]=v;
   if(stage>=2)out+=`<p data-object-id="base-exponent">Base <strong>${esc(base)}</strong> · ${esc(exponent)} equal factors</p>`;
   if(stage>=3)out+=`<div class="g8-exp-factor-row" aria-label="Equal factors">${tiles(base,Number(exponent),'factor')}</div>`;
   if(kind==='negative'&&stage>=4)out+=`<p data-object-id="sign-pairs">${exponent} negative factors form ${Number(exponent)%2?'an unpaired negative factor':'only positive pairs'}.</p>`;
   if(kind==='compare'&&stage>=6)out+=`<p data-object-id="comparison-target">Compare the evaluated power with ${esc(v[2])}.</p>`;
  }else if(kind==='zero'){
   if(stage>=2)out+=`<p data-object-id="same-power">${esc(v[0])}² ÷ ${esc(v[0])}²</p>`;
   if(stage>=3)out+=`<p data-object-id="equal-quotient">Equal nonzero quantities divide to one.</p>`;
   if(stage>=4)out+=`<p data-object-id="subtract-exponents">2 − 2 = 0</p>`;
  }else{
   const [base,m,n]=v;
   if(stage>=2)out+=`<p data-object-id="common-base">${kind==='power_product'?'Factor the original base '+(Number(base)*Number(m))+' as '+base+' × '+m:'Common base '+base}</p>`;
   if(kind==='power_product'){
    if(stage>=3)out+=`<div class="g8-exp-factor-row" aria-label="Repeated brackets">${tiles(`(${base} × ${m})`,Number(n),'bracket')}</div>`;
    if(stage>=5)out+=`<p data-object-id="group-factors">Group ${esc(base)} factors and ${esc(m)} factors separately.</p>`;
   }else{
    if(stage>=3)out+=`<div class="g8-exp-factor-row" aria-label="First power factors">${tiles(base,Number(m),'first-factor')}</div>`;
    if(stage>=4)out+=`<div class="g8-exp-factor-row g8-exp-denominator" aria-label="Second power factors">${tiles(base,Number(n),'second-factor')}</div>`;
    if(kind==='quotient'&&stage>=5)out+=`<p data-object-id="cancellation">Cancel ${esc(n)} matching nonzero pairs; ${Number(m)-Number(n)} remain.</p>`;
    if(kind==='product'&&stage>=5)out+=`<p data-object-id="factor-count">Count ${esc(m)} + ${esc(n)} equal factors.</p>`;
    if(kind==='mixed'&&stage>=5)out+=`<div data-object-id="third-power" class="g8-exp-factor-row g8-exp-denominator">${tiles(base,Number(v[3]),'third-factor')}</div>`;
    if(kind==='mixed'&&stage>=6)out+=`<p data-object-id="mixed-cancellation">Combine the numerator, then cancel ${esc(v[3])} nonzero matching factors.</p>`;
   }
  }
  return out+'</div>';
 }
 function rootModel(s,stage){
  const [a,b,c,d]=(s.values||[]).map(Number),kind=s.kind;
  const squareN=kind==='root_pair'?a:kind==='mixed'?c:a;
  const cubeN=kind==='root_pair'?b:kind==='mixed'?d:a;
  const squareSide=Math.round(Math.sqrt(squareN));
  const cubeSide=Math.round(Math.cbrt(cubeN));
  let out='<div class="g8-exponent-stage g8-root-stage" role="group" aria-label="Question-specific square, cube and calculation model">';
  if(['square_root','root_pair','square_area','mixed'].includes(kind)){
   out+=`<div data-object-id="square-model" class="g8-root-shape"><strong>Square ${esc(squareN)}${kind==='square_area'?' cm²':''}</strong>`;
   if(stage>=(kind==='mixed'?4:3))out+=`<div class="g8-root-grid" style="grid-template-columns:repeat(${squareSide},minmax(0,1fr))" aria-label="${squareSide} rows of ${squareSide} unit squares">${Array.from({length:squareN},(_,i)=>`<span data-object-id="square-tile-${i+1}" class="g8-root-unit"></span>`).join('')}</div>`;
   if(stage>=(kind==='mixed'?4:4))out+=`<p data-object-id="square-side">${squareSide} rows × ${squareSide} columns = ${squareN}</p>`;
   out+='</div>';
  }
  if(['cube_root','root_pair','cube_volume','mixed'].includes(kind)){
   out+=`<div data-object-id="cube-model" class="g8-root-shape"><strong>Cube ${esc(cubeN)}${kind==='cube_volume'?' cm³':''}</strong>`;
   if(stage>=(kind==='mixed'?5:kind==='root_pair'?4:3))out+=`<div class="g8-root-layers" aria-label="${cubeSide} layers, each ${cubeSide} by ${cubeSide}">${Array.from({length:cubeSide},(_,i)=>`<span data-object-id="cube-layer-${i+1}" class="g8-root-layer">Layer ${i+1}: ${cubeSide} × ${cubeSide}</span>`).join('')}</div>`;
   if(stage>=(kind==='mixed'?5:kind==='root_pair'?4:4))out+=`<p data-object-id="cube-edge">${cubeSide} × ${cubeSide} × ${cubeSide} = ${cubeN}</p>`;
   out+='</div>';
  }
  if(kind==='mixed'){
   out+=`<div data-object-id="expression-lanes" class="g8-root-shape"><strong>${esc(a)}${sup(b)} + √${esc(c)} × ∛${esc(d)}</strong>`;
   if(stage>=3)out+=`<p data-object-id="power-lane">Power: ${esc(a)}${sup(b)} = ${a**b}</p>`;
   if(stage>=4)out+=`<p data-object-id="square-lane">Square root: √${c} = ${Math.sqrt(c)}</p>`;
   if(stage>=5)out+=`<p data-object-id="cube-lane">Cube root: ∛${d} = ${Math.cbrt(d)}</p>`;
   if(stage>=6)out+=`<p data-object-id="multiply-lane">Multiply roots first: ${Math.sqrt(c)} × ${Math.cbrt(d)}</p>`;
   out+='</div>';
  }
  if(kind==='square_area'&&stage>=6)out+=`<p data-object-id="perimeter-lane">Perimeter: 4 × ${squareSide} = ${4*squareSide} cm</p>`;
  return out+'</div>';
 }
 const measure=(id,kind,number,stage,revealAt,unit='',gridAt=revealAt)=>{
  const side=kind==='square'?Math.round(Math.sqrt(number)):Math.round(Math.cbrt(number));
  const label=kind==='square'?'Square value':'Cube value';
  const visual=kind==='square'?`<div data-object-id="${id}-grid" class="g8-root-grid" style="grid-template-columns:repeat(${side},minmax(0,1fr))" aria-label="${side} rows of ${side} unit squares">${Array.from({length:number},(_,i)=>`<span data-object-id="${id}-tile-${i+1}" class="g8-root-unit"></span>`).join('')}</div>`:`<div data-object-id="${id}-layers" class="g8-root-layers" aria-label="${side} layers of ${side} by ${side} unit cubes">${Array.from({length:side},(_,i)=>`<span data-object-id="${id}-layer-${i+1}" class="g8-root-layer">Layer ${i+1}: ${side} × ${side}</span>`).join('')}</div>`;
  return `<div class="g8-exp-measure" data-object-id="${id}"><strong>${label}: ${esc(number)}${unit?` ${unit}${kind==='square'?'²':'³'}`:''}</strong>${stage>=gridAt?visual:''}${stage>=revealAt?`<span data-object-id="${id}-edge">${kind==='square'?'√':'∛'}${esc(number)} = ${side}${unit?' '+unit:''}</span>`:''}</div>`;
 };
 function auditModel(s,stage){
  const v=s.values.map(Number),kind=s.kind;
  let out=`<div class="g8-exponent-stage g8-exp-audit" role="group" aria-label="Inspect and repair the learner's mathematical claim"><p data-object-id="given-claim">${esc(s.problem)}</p>`;
  if(kind==='sign_audit'){
   const [b,e]=v;if(stage>=3)out+=`<div data-object-id="signed-factors" class="g8-exp-factor-row">${tiles(`(−${b})`,e,'signed-factor')}</div>`;
   if(stage>=4)out+=`<p data-object-id="sign-pairs">${e/2} negative pairs → positive sign</p>`;
  }else if(kind==='root_audit'){
   if(stage>=3)out+=measure('principal-square','square',v[0],stage,4,'',3);
   if(stage>=5)out+=`<p data-object-id="root-scope">The √ symbol selects the nonnegative root.</p>`;
  }else if(kind==='quotient_audit'){
   const [b,m,n]=v;
   if(stage>=3)out+=`<div data-object-id="numerator-factors" class="g8-exp-factor-row">${tiles(b,m,'numerator')}</div>`;
   if(stage>=4)out+=`<div data-object-id="denominator-factors" class="g8-exp-factor-row g8-exp-denominator">${tiles(b,n,'denominator')}</div>`;
   if(stage>=5)out+=`<p data-object-id="cancel-pairs">Cancel ${n} matching pairs; ${m-n} factors remain.</p>`;
  }else if(kind==='root_sum_audit'){
   if(stage>=3)out+=measure('first-square','square',v[0],stage,3);
   if(stage>=4)out+=measure('second-square','square',v[1],stage,4);
   if(stage>=5)out+=`<p data-object-id="separate-addition">Add the two root values after finding each.</p>`;
  }else if(kind==='mixed_audit'){
   const [b,m,n,rad]=v;
   if(stage>=3)out+=`<div data-object-id="first-power" class="g8-exp-factor-row">${tiles(b,m,'first-power-factor')}</div>`;
   if(stage>=4)out+=`<div data-object-id="second-power" class="g8-exp-factor-row">${tiles(b,n,'second-power-factor')}</div>`;
   if(stage>=5)out+=`<p data-object-id="combined-power">${m} + ${n} = ${m+n} equal factors</p>`;
   if(stage>=6)out+=measure('separate-root','square',rad,stage,6);
  }
  return out+'</div>';
 }
 function contextModel(s,stage){
  const v=s.values.map(Number),kind=s.kind;
  let out='<div class="g8-exponent-stage g8-exp-context" role="group" aria-label="Question-specific measured shapes and operations">';
  if(kind==='square_perimeter_gap'||kind==='cube_edge_gap'){
   const shape=kind==='square_perimeter_gap'?'square':'cube';
   out+=measure('first-'+shape,shape,v[0],stage,3,'cm')+measure('second-'+shape,shape,v[1],stage,4,'cm');
   if(stage>=5)out+=`<p data-object-id="comparison-operation">Compare ${shape==='square'?'linear perimeters':'linear edges'} after taking the roots.</p>`;
  }else if(kind==='side_area_gap'){
   const [b,e,area]=v;
   out+=`<div data-object-id="power-side" class="g8-exp-measure"><strong>First side ${b}${sup(e)} cm</strong>${stage>=2?`<span>${b}${sup(e)} = ${b**e} cm</span>`:''}${stage>=3?`<span>First area: ${b**e} × ${b**e} = ${(b**e)**2} cm²</span>`:''}</div>`;
   out+=measure('other-square','square',area,stage,5,'cm');
  }else if(kind==='root_power_compare'){
   const [b,e,a,c]=v;
   out+=`<div data-object-id="left-power" class="g8-exp-measure"><strong>Left ${b}${sup(e)}</strong>${stage>=3?`<span>${b**e}</span>`:''}</div>`;
   out+=measure('right-square','square',a,stage,4)+measure('right-cube','cube',c,stage,5);
   if(stage>=6)out+=`<p data-object-id="right-product">Multiply the two root values before comparing.</p>`;
  }else if(kind==='combined_perimeter'){
   out+=measure('bed-one','square',v[0],stage,3,'m')+measure('bed-two','square',v[1],stage,4,'m')+measure('planter','cube',v[2],stage,5,'m');
   if(stage>=6)out+=`<p data-object-id="perimeters">4 × ${Math.sqrt(v[0])} m + 4 × ${Math.sqrt(v[1])} m + ${Math.cbrt(v[2])} m</p>`;
  }
  return out+'</div>';
 }
 for(const template of ['grade8_exponent_representation','grade8_exponent_laws','grade8_exponent_roots','grade8_exponent_applications','grade8_exponent_error_trace','grade8_exponent_integrated'])AthenaVisualizationRegistry.register('algebra',template,{
  render(params,state,phase){
   const scene=JSON.parse(params.scene_json),requested=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
   const stage=phase==='result'?requested:Math.max(0,requested-1),complete=stage===params.total_steps;
   const rows=(scene.rows||[]).slice(0,Math.max(0,Math.min(scene.rows.length,stage-1))).map((row,i)=>`<li data-object-id="reason-${i+1}">${esc(row)}</li>`).join('');
   const visual=template==='grade8_exponent_roots'||template==='grade8_exponent_applications'?rootModel(scene,stage):template==='grade8_exponent_error_trace'?auditModel(scene,stage):template==='grade8_exponent_integrated'?contextModel(scene,stage):model(scene,stage);
   return `<section class="g8-exponent-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${esc(params.prompt)}</p><div data-object-id="model">${visual}</div><ol aria-label="Worked solution so far">${rows}</ol><p data-object-id="operation">${phase==='ready'?'':esc(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!complete?esc(state.after_state||''):''}</p><p data-object-id="verification">${complete?`Answer: ${esc(scene.answer)}. ${esc(scene.memo)}`:''}</p></section>`;
  },destroy(){}
 });
})();
