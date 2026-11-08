/* Source-owned graph families. Never connect across asymptotes or excluded inputs. */
(() => {
 const esc=s=>escapeWhiteboardHtml(String(s??''));
 const text=(id,x,y,t,cls='g10f-label')=>`<text data-object-id="${id}" x="${x}" y="${y}" class="${cls}">${esc(t)}</text>`;
 const line=(id,x1,y1,x2,y2,cls='g10f-axis')=>`<line data-object-id="${id}" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`;
 const stage=(state,phase)=>{const m=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));const n=Number(m?.slice(6)||0);return phase==='result'?n:Math.max(0,n-1)};
 const isTrig=f=>['sine','cosine','tangent'].includes(f);
 function value(f,a,q,base,x){
  if(f==='linear')return a*x+q;if(f==='parabola')return a*x*x+q;
  if(f==='hyperbola')return x===0?NaN:a/x+q;
  if(f==='exponential')return a*base**x+q;
  const rad=x*Math.PI/180;
  if(f==='sine')return a*Math.sin(rad)+q;
  if(f==='cosine')return a*Math.cos(rad)+q;
  if(f==='tangent')return Math.abs(Math.cos(rad))<.0001?NaN:a*Math.tan(rad)+q;
  throw Error('Unknown graph family');
 }
 function axes(trig){
  let out=line('horizontal-axis',40,160,460,160)+line('vertical-axis',trig?55:250,25,trig?55:250,300);
  if(trig){for(const deg of [0,90,180,270,360])out+=line(`tick-${deg}`,55+deg*390/360,157,55+deg*390/360,163)+text(`tick-label-${deg}`,50+deg*390/360,180,`${deg}°`)}
  else{for(let x=-4;x<=4;x+=2)out+=line(`tick-x-${x}`,250+38*x,156,250+38*x,164)+text(`tick-label-${x}`,244+38*x,180,x);
   for(let y=-6;y<=6;y+=3)if(y)out+=text(`tick-y-${y}`,256,164-18*y,y)}
  return out+text('x-label',465,155,trig?'θ':'x')+text('y-label',trig?62:257,25,'y');
 }
 function trace(v,trig,ghost=false){
  if(v.mode==='discrete' && !ghost)return '';
  const a=ghost?1:v.a,q=ghost?0:v.q,base=v.base??2;
  if(!Number.isFinite(a)||!Number.isFinite(q))return '';
  const project=(x,y)=>[trig?55+x*390/360:250+x*38,160-y*(trig?27:18)];
  const min=trig?0:v.mode==='continuous'?0:-5,max=trig?360:v.mode==='continuous'?2:5,step=trig?1:.035,limit=trig?5.1:7.6;
  let parts=[],segment=[],lastX=null;
  const flush=()=>{if(segment.length>1)parts.push(segment);segment=[];lastX=null};
  for(let x=min;x<=max+.0001;x+=step){
   if(v.family==='hyperbola' && Math.abs(x)<step*1.1){flush();continue}
   if(v.family==='tangent' && (Math.abs(x-90)<step*1.1||Math.abs(x-270)<step*1.1)){flush();continue}
   const y=value(v.family,a,q,base,x);
   if(!Number.isFinite(y)||Math.abs(y)>limit){flush();continue}
   if(lastX!=null && x-lastX>step*1.5)flush();
   const [sx,sy]=project(x,y);segment.push(`${segment.length?'L':'M'}${sx.toFixed(1)},${sy.toFixed(1)}`);lastX=x;
  }
  flush();return parts.map((p,i)=>`<path data-object-id="${ghost?'parent':'curve'}-${i}" d="${p.join(' ')}" class="${ghost?'g10f-parent':'g10f-curve'}"/>`).join('');
 }
 function marker(id,x,y,trig,caption=''){
  const px=trig?55+x*390/360:250+x*38,py=160-y*(trig?27:18);
  if(!Number.isFinite(py)||py<25||py>300)return '';
  return `<circle data-object-id="${id}" cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="5" class="g10f-point"/>`+
   (caption?text(`${id}-label`,Math.min(px+8,425),Math.max(py-8,35),caption):'');
 }
 function diagram(v,k,n){
  const trig=isTrig(v.family),a=v.a,q=v.q,base=v.base??2;
  let out=axes(trig);
  if(n===6){
   for(const [idx,p] of (v.given_points||[]).entries())out+=marker(`given-${idx}`,p[0],p[1],false,`(${p[0]}; ${p[1]})`);
   for(const [idx,rule] of (v.given_asymptotes||[]).entries()){
    const axis=rule.startsWith('x=')?'x':'y',num=Number(rule.slice(2));
    out+=axis==='x'?line(`given-asymptote-${idx}`,250+num*38,30,250+num*38,300,'g10f-asymptote'):
      line(`given-asymptote-${idx}`,40,160-num*18,460,160-num*18,'g10f-asymptote');
   }
  }
  if(n===1){
   const rows=(v.given||[]).slice(0,k>=3?3:2);
   if(k>=2)rows.forEach((p,i)=>out+=marker(`table-point-${i}`,p[0],p[1],false,`(${p[0]}; ${p[1]})`));
  }
  if(n===2 && k>=2 && v.given?.length){const [x]=v.given[0],y=value(v.family,a,q,base,x);out+=marker('parent-point',x,y,false,`(${x}; ${Number.isInteger(y)?y:y.toFixed(2)})`)}
  if(n===3 && k>=2)out+=trace(v,false,true);
  if(n===5 && k>=2)out+=trace(v,true,true);
  if(n===7 && ['secant','discrete','continuous'].includes(v.mode) && k>=(v.mode==='secant'?2:4)){
   for(const [idx,p] of (v.given||[]).entries())out+=marker(`context-point-${idx}`,p[0],p[1],false,`(${p[0]}; ${p[1]})`);
   if(v.mode==='secant' && k>=3 && v.given?.length===2){
    const [p1,p2]=v.given;out+=line('secant',250+p1[0]*38,160-p1[1]*18,250+p2[0]*38,160-p2[1]*18,'g10f-guide');
   }
  }
  if(trig && v.angle!=null && k>=2)out+=line('angle-guide',55+v.angle*390/360,42,55+v.angle*390/360,300,'g10f-guide');
  if(k>=3 && (v.family==='hyperbola'||v.family==='exponential')){
   if(v.family==='hyperbola')out+=line('vertical-asymptote',250,28,250,300,'g10f-asymptote');
   if(Number.isFinite(q))out+=line('horizontal-asymptote',40,160-q*18,460,160-q*18,'g10f-asymptote');
  }
  if(k>=3 && v.family==='tangent')for(const angle of [90,270])out+=line(`vertical-asymptote-${angle}`,55+angle*390/360,28,55+angle*390/360,300,'g10f-asymptote');
  if(k>=4)out+=trace(v,trig);
  if(n===1 && k>=4 && v.target_x!=null && Number.isFinite(a)&&Number.isFinite(q))out+=marker('calculated-pair',v.target_x,a*v.target_x+q,false,`(${v.target_x}; ${a*v.target_x+q})`);
  if(n===5 && k>=4 && Number.isFinite(q))out+=line('midline',55,160-q*27,445,160-q*27,'g10f-guide');
  return out;
 }
 function render(p,state,phase,n){
  const scene=JSON.parse(p.scene_json),v=scene.visual?.values,k=stage(state,phase);
  if(scene.id!==p.question_id||scene.problem!==p.prompt||scene.lesson!==n||v?.lesson!==n||scene.visual?.family!=='grade10_functions')throw Error('Function scene belongs to another question');
  if(!['linear','parabola','hyperbola','exponential','sine','cosine','tangent'].includes(v.family))throw Error('Unsupported graph family');
  const trig=isTrig(v.family);
  return `<section class="g10f-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g10f-model"><svg viewBox="0 0 500 320" role="img" aria-label="${esc(scene.problem)}"><title>${esc(v.family)} graph, stage ${k} of 5</title>${diagram(v,k,n)}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&k<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&k===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=7;n++)AthenaVisualizationRegistry.register('algebra',`grade10_fn_${n}`,{render:(p,s,phase)=>render(p,s,phase,n)});
})();
