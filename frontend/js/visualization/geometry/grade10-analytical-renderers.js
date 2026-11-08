/* A fixed Cartesian scale keeps every previous coordinate in place. */
(() => {
 const esc=s=>escapeWhiteboardHtml(String(s??''));
 const X=x=>250+9*x,Y=y=>170-9*y;
 const line=(id,a,b,cls='g10ag-line')=>`<line data-object-id="${id}" x1="${X(a[0])}" y1="${Y(a[1])}" x2="${X(b[0])}" y2="${Y(b[1])}" class="${cls}"/>`;
 const label=(id,x,y,t,cls='g10ag-label')=>`<text data-object-id="${id}" x="${x}" y="${y}" class="${cls}">${esc(t)}</text>`;
 const point=(id,p,t)=>`<circle data-object-id="${id}" cx="${X(p[0])}" cy="${Y(p[1])}" r="5" class="g10ag-point"/>`+label(`${id}-label`,Math.min(442,X(p[0])+7),Math.max(25,Y(p[1])-8),`${t}(${p[0]}; ${p[1]})`);
 const stage=(state,phase)=>{const m=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));const n=Number(m?.slice(6)||0);return phase==='result'?n:Math.max(0,n-1)};
 function axes(){
  let o='';for(let t=-20;t<=20;t+=5){
   o+=`<line x1="${X(t)}" y1="18" x2="${X(t)}" y2="322" class="g10ag-grid"/>`;
   o+=`<line x1="28" y1="${Y(t)}" x2="472" y2="${Y(t)}" class="g10ag-grid"/>`;
   if(t && t%10===0)o+=label(`x-tick-${t}`,X(t)-7,186,t)+(Math.abs(t)<=10?label(`y-tick-${t}`,256,Y(t)-3,t):'');
  }
  return o+`<line data-object-id="x-axis" x1="28" y1="170" x2="472" y2="170" class="g10ag-axis"/>`+
   `<line data-object-id="y-axis" x1="250" y1="18" x2="250" y2="322" class="g10ag-axis"/>`+
   label('axis-x',470,164,'x')+label('axis-y',258,25,'y');
 }
 function draw(v,k){
  const pts=v.points;if(!Array.isArray(pts)||!pts.length||pts.some(p=>!Array.isArray(p)||p.length!==2||p.some(c=>!Number.isInteger(c)||Math.abs(c)>23)))throw Error('Invalid Cartesian points');
  let out=axes();
  if(k>=1)pts.forEach((p,i)=>out+=point(`given-${i}`,p,v.mode==='reverse_midpoint'&&i===1?'M':'ABCD'[i]));
  if(k>=2){
   if(v.model==='quadrilateral'){
    for(let i=0;i<4;i++)out+=line(`side-${i}`,pts[i],pts[(i+1)%4]);
   }else if(v.model==='two_segments')out+=line('AB',pts[0],pts[1])+line('CD',pts[2],pts[3]);
   else if(v.mode==='reverse_midpoint')out+=line('AM',pts[0],pts[1]);
   else out+=line('AB',pts[0],pts[1]);
  }
  if(k>=2 && ['distance','gradient','distance_check','gradient_check'].includes(v.mode)){
   const corner=[pts[1][0],pts[0][1]];
   out+=line('run',pts[0],corner,'g10ag-run')+label('run-value',(X(pts[0][0])+X(corner[0]))/2,Y(corner[1])+18,`Δx = ${v.dx}`,'g10ag-focus');
   if(k>=3)out+=line('rise',corner,pts[1],'g10ag-rise')+label('rise-value',Math.min(445,X(corner[0])+5),(Y(corner[1])+Y(pts[1][1]))/2,`Δy = ${v.dy}`,'g10ag-focus');
  }
  if(k>=3 && v.model==='two_segments')out+=label('slope-comparison',35,307,v.mode==='parallel'?'Compare equal slopes':'Multiply the two slopes','g10ag-focus');
  if(k>=3 && v.model==='quadrilateral')out+=label('side-comparison',35,307,'Compare the opposite side vectors','g10ag-focus');
  if(k>=4 && Array.isArray(v.solution_point)){
   const t=v.mode==='reverse_midpoint'?'B':'M';out+=point('constructed-point',v.solution_point,t);
   if(v.mode==='reverse_midpoint')out+=line('MB',pts[1],v.solution_point,'g10ag-rise');
  }
  if(k>=4 && v.model==='two_segments')out+=label('relation',35,330,v.mode==='parallel'?'AB ∥ CD':'AB ⟂ CD','g10ag-focus');
  if(k>=4 && v.model==='quadrilateral')out+=label('shape-conclusion',35,330,v.mode,'g10ag-focus');
  return out;
 }
 function render(p,state,phase,n){
  const scene=JSON.parse(p.scene_json),v=scene.visual?.values,k=stage(state,phase);
  if(scene.id!==p.question_id||scene.problem!==p.prompt||scene.lesson!==n||v?.lesson!==n||scene.visual?.family!=='grade10_analytical')throw Error('Coordinate scene belongs to another question');
  return `<section class="g10ag-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g10ag-model"><svg viewBox="0 0 500 345" role="img" aria-label="${esc(scene.problem)}"><title>Cartesian construction, stage ${k} of 5</title>${draw(v,k)}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&k<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&k===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('geometry',`grade10_ag_${n}`,{render:(p,s,phase)=>render(p,s,phase,n)});
})();
