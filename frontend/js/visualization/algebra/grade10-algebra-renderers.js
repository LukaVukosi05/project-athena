/* Algebra stage renders derived from each question's source values and operation. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 const t=(id,x,y,s,cls='g10-text')=>`<text data-object-id="${id}" x="${x}" y="${y}" class="${cls}">${esc(s)}</text>`;
 const box=(id,x,y,w,h,cls='g10-cell')=>`<rect data-object-id="${id}" x="${x}" y="${y}" width="${w}" height="${h}" class="${cls}"/>`;
 function stage(state,phase){const tag=(state.annotations||[]).find(s=>/^stage:\d+$/.test(s));const n=Number(tag?.slice(6)||0);return phase==='result'?n:Math.max(0,n-1)}
 function sceneImage(v,n,step){
  if(step===0)return '<line class="g10-axis" x1="55" y1="153" x2="445" y2="153"/>';
  let out='';const a=v.a,b=v.b;
  if(n<=2){
   const lo=v.lower??Math.floor(Math.sqrt(v.radicand));const hi=lo+1;const px=x=>90+(x-lo)*300;
   out+=`<line class="g10-axis" x1="55" y1="153" x2="445" y2="153"/>`;
   if(step>=1)out+=t('surd',200,65,`√${v.radicand}`,'g10-title');
   if(step>=2)out+=t('left',px(lo)-10,190,String(lo))+t('right',px(hi)-10,190,String(hi))+box('left-square',px(lo)-22,135,44,7)+box('right-square',px(hi)-22,135,44,7);
   if(step>=3)out+=`<circle data-object-id="surd-point" cx="${px(Math.sqrt(v.radicand))}" cy="153" r="8" class="g10-highlight"/>`;
   if(step>=4)out+=t('bound',80,249,n===1?(v.kind==='rational'?`√${v.radicand} = ${lo}`:`${lo} < √${v.radicand} < ${hi}`):`√${v.radicand} ≈ ${v.decimal}`,'g10-title');
   if(step>=5)out+=t('check',62,286,n===1?(v.kind==='rational'?'A perfect square: rational.':'Not a perfect square: irrational.'):'Square the approximation to check the bound.');
  }else if(n===3){
   out+=t('row-label',31,50,`(x + ${a}) × (x² ${v.d>=0?'+':'−'} ${Math.abs(v.d)}x ${v.t>=0?'+':'−'} ${Math.abs(v.t)})`,'g10-title');
   const cells=[['x³',120,95],['x·x',240,95],['x·1',360,95],[`${a}x²`,120,174],[`${a}·${v.d}x`,240,174],[`${a}·${v.t}`,360,174]];
   cells.forEach(([label,x,y],j)=>{out+=box(`product-${j}`,x-47,y-31,95,51,step>=(j<3?2:3)?'g10-cell g10-active':'g10-cell');if(step>=(j<3?2:3))out+=t(`term-${j}`,x-35,y,label)});
   if(step>=4)out+=t('collect',36,264,'Collect x³, x², x and constants in aligned columns.');
  }else if(n===4){
   out+=t('original',22,55,v.kind==='grouping'?`x² + ${a}x + ${v.d}x + ${a*v.d}`:`x² + (${a+v.d})x + (${a*v.d})`,'g10-title');
   if(step>=2)out+=box('pair-one',37,95,193,78,'g10-cell g10-active')+t('left-pair',45,136,`x(x + ${a})`);
   if(step>=3)out+=box('pair-two',245,95,195,78,'g10-cell g10-active')+t('right-pair',253,136,`${v.d}(x + ${a})`);
   if(step>=4)out+=t('common',38,240,'Both groups share the same binomial.');
  }else if(n===5){
   out+=box('cube-x',60,70,140,140,'g10-cube')+t('x-cube',94,150,'x³','g10-title');
   out+=box('cube-b',300,105,95,95,'g10-cube')+t('b-cube',318,158,`${b}³`,'g10-title');
   if(step>=2)out+=t('identity',61,246,v.kind==='difference'?'u³ − v³ = (u − v)(u² + uv + v²)':'u³ + v³ = (u + v)(u² − uv + v²)');
   if(step>=3)out+=t('linear',61,275,`u = x and v = ${b}: factor each cube.`);
  }else{
   out+=t('fraction-heading',30,38,v.kind==='combine'?'Add like-denominator fractions':'Simplify the original fraction','g10-title');
   const fraction=(id,x,y,w,top,bottom)=>box(`${id}-frame`,x,y,w,116,'g10-cell')+t(`${id}-top`,x+9,y+37,top,'g10-small')+`<line class="g10-axis" x1="${x+9}" y1="${y+56}" x2="${x+w-9}" y2="${y+56}"/>`+t(`${id}-bottom`,x+9,y+89,bottom,'g10-small');
   if(v.kind==='combine')out+=fraction('fraction-one',30,76,203,v.second,v.denominator)+t('plus',240,138,v.operator||'+')+fraction('fraction-two',270,76,203,`${a}${v.second}`,v.denominator);
   else out+=fraction('fraction-one',90,76,320,v.second,v.denominator);
   if(step>=3)out+=t('factor-denominator',43,222,`Denominator = ${v.first} × ${v.second}`,'g10-small');
   if(step>=4)out+=t('cancel',43,259,'Cancel the shared nonzero factor.');
   if(step>=5)out+=t('restriction',43,289,`Original denominator: x ≠ ${v.excluded}`);
  }
  return out+t('progress',424,299,`${step}/5`);
 }
 function render(p,state,phase,n){
  const scene=JSON.parse(p.scene_json),v=scene.visual?.values,step=stage(state,phase);
  if(!v||scene.id!==p.question_id||scene.problem!==p.prompt||scene.lesson!==n||v.lesson!==n)throw Error('Algebra visual belongs to another question');
  const visual=sceneImage(v,n,step);
  return `<section class="g10-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g10-model"><svg viewBox="0 0 500 310" role="img" aria-label="${esc(scene.problem)}"><title>Question-specific algebra working, stage ${step} of 5</title>${visual}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&step<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&step===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('algebra',`grade10_algebra_${n}`,{render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
