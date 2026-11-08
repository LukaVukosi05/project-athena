/* Source-driven Grade 10 geometry constructions. Earlier marks stay visible. */
(() => {
 const esc=s=>escapeWhiteboardHtml(String(s??''));
 const line=(id,x1,y1,x2,y2,cls='g10e-line')=>`<line data-object-id="${id}" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`;
 const text=(id,x,y,value,cls='g10e-label')=>`<text data-object-id="${id}" x="${x}" y="${y}" class="${cls}">${esc(value)}</text>`;
 const polygon=(id,points)=>`<polygon data-object-id="${id}" points="${points.map(p=>p.join(',')).join(' ')}" class="g10e-shape"/>`;
 const point=(id,p,label,dx=7,dy=-7)=>text(id,p[0]+dx,p[1]+dy,label);
 function stage(state,phase){const match=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));const n=Number(match?.slice(6)||0);return phase==='result'?n:Math.max(0,n-1)}
 function crossings(v,k){
  if(v.model==='intersect'){
   const rad=v.given_angle*Math.PI/180, O=[250,160],C=[250-160*Math.cos(rad),160-160*Math.sin(rad)],D=[250+160*Math.cos(rad),160+160*Math.sin(rad)];
   let o=line('AB',40,160,460,160)+line('CD',...C,...D)+point('O',O,'O')+point('A',[40,160],'A')+point('B',[460,160],'B')+point('C',C,'C')+point('D',D,'D');
   if(k>=1)o+=text('given',250-74*Math.cos(rad/2),160-74*Math.sin(rad/2),`${v.given_angle}°`);
   if(k>=2)o+=text('target',v.target==='vertically opposite'?250+75*Math.cos(rad/2):250+70*Math.sin(rad/2),v.target==='vertically opposite'?160+75*Math.sin(rad/2):160-70*Math.cos(rad/2),'x','g10e-focus');
   if(k>=4)o+=text('computed',43,300,`x = ${v.result}°`,'g10e-focus');
   return o;
  }
  const theta=v.given_angle*Math.PI/180,dx=100/Math.tan(theta),x0=250,x1=250+dx;
  let o=line('p',35,95,465,95)+line('q',35,195,465,195)+line('t',x0-dx*.65,30,x1+dx*.85,280)+text('p-label',466,99,'p')+text('q-label',466,199,'q');
  if(k>=1)o+=text('given',x0+25,121,`${v.given_angle}°`);
  if(k>=2)o+=text('target',x1+(v.target==='alternate interior'?-30:30),180,'x','g10e-focus');
  if(k>=3)o+=line('parallel-mark-p',375,86,390,95,'g10e-focus')+line('parallel-mark-q',375,186,390,195,'g10e-focus');
  if(k>=4)o+=text('computed',42,300,`x = ${v.result}°`,'g10e-focus');
  return o;
 }
 function triangles(v,k){
  const a=[[55,235],[175,235],[93,70]],b=[[285,235],[405,235],[323,70]];
  let o=polygon('ABC',a)+polygon('DEF',b);
  for(let j=0;j<3;j++)o+=point(`vertex-${j}`,a[j],'ABC'[j])+point(`vertex-${j+3}`,b[j],'DEF'[j]);
  if(k>=2 && v.side_ab!=null)o+=line('first-pair-A',55,235,175,235,'g10e-focus')+line('first-pair-D',285,235,405,235,'g10e-focus')+text('side-ab',108,255,`${v.side_ab} cm`)+text('side-de',340,255,`${v.side_de} cm`);
  if(k>=(v.mode==='sss'?3:2) && v.side_ac!=null)o+=line('second-pair-A',55,235,93,70,'g10e-focus')+line('second-pair-D',285,235,323,70,'g10e-focus')+text('side-ac',48,150,`${v.side_ac} cm`)+text('side-df',285,150,`${v.side_df} cm`);
  if(k>=2 && v.side_bc!=null)o+=text('side-bc',152,144,`${v.side_bc} cm`)+text('side-ef',382,144,`${v.side_ef} cm`);
  if(k>=(v.mode==='sas'?3:2) && v.angle!=null)o+=text('given-angle',65,213,`${v.angle}°`);
  if(k>=2 && v.second_angle!=null)o+=text('second-angle',170,214,`${v.second_angle}°`);
  if(k>=4)o+=text('criterion',55,295,v.mode.replaceAll('_',' ').toUpperCase(),'g10e-focus');
  if(v.mode==='similar_sas')o+=text('schematic',335,295,'not to scale');
  return o;
 }
 function quadrilateral(v,k){
  const coords={kite:[[245,45],[420,150],[245,260],[100,150]],parallelogram:[[100,85],[365,85],[425,245],[160,245]],trapezium:[[100,245],[430,245],[355,70],[175,70]],rectangle:[[110,70],[390,70],[390,250],[110,250]],rhombus:[[250,40],[420,160],[250,280],[80,160]],square:[[115,55],[385,55],[385,265],[115,265]]};
  const p=coords[v.shape];if(!p)throw Error('Unknown quadrilateral');
  let o=polygon(v.shape,p);for(let j=0;j<4;j++)o+=point(`vertex-${j}`,p[j],'ABCD'[j]);
  if(k>=1){
   if(v.base!=null)o+=text('base-label',230,92,`${v.base} cm`);
   if(v.side!=null)o+=text('side-label',230,49,`${v.side} cm`);
   if(v.width!=null)o+=text('width-label',228,63,`${v.width} cm`);
   if(v.diagonal_ac!=null)o+=line('AC',...p[0],...p[2],'g10e-focus')+text('AC-label',175,145,`${v.diagonal_ac} cm`);
  }
  if(k>=2){
   if(v.diagonal_bd!=null)o+=line('BD',...p[1],...p[3],'g10e-focus')+text('BD-label',270,150,`${v.diagonal_bd} cm`);
   if(v.height!=null && v.operation!=='diagonal' && v.shape!=='rectangle')o+=line('perpendicular-height',p[0][0],p[0][1],p[0][0],p[2][1],'g10e-dash')+text('height-label',p[0][0]+8,170,`${v.height} cm`);
   if(v.top!=null)o+=text('top-label',230,65,`${v.top} cm`);
   if(v.width!=null)o+=text('height-label',395,165,`${v.height} cm`);
  }
  if(k>=3 && v.shape==='parallelogram' && v.operation==='diagonal')o+=line('diagonal-AC',...p[0],...p[2],'g10e-focus')+line('diagonal-BD',...p[1],...p[3],'g10e-dash')+text('AO-label',180,150,`AO = ${v.height} cm`);
  if(k>=4 && v.angle!=null)o+=text('angle',270,95,`${v.angle}°`,'g10e-focus');
  return o;
 }
 function midpoint(v,k){
  const A=[240,45],B=[65,265],C=[435,265],D=[152.5,155],E=[337.5,155];
  let o=polygon('ABC',[A,B,C]);[A,B,C].forEach((p,j)=>o+=point(`vertex-${j}`,p,'ABC'[j]));
  if(k>=1)o+=point('D',D,'D')+point('E',E,'E')+text('equal-halves-left',110,168,'|')+text('equal-halves-right',364,168,'|');
  if(k>=2)o+=line('DE',...D,...E,'g10e-focus')+(v.mode==='reverse'?text('midsegment-given',230,145,`${v.de} cm`):v.bc!=null?text('base-given',215,285,`${v.bc} cm`):text('angle-given',90,245,`${v.angle}°`));
  if(k>=3)o+=text('parallel',235,148,'DE ∥ BC','g10e-focus');
  if(k>=4 && v.solution_de!=null)o+=text('half-base',241,185,`DE = ${v.solution_de} cm`,'g10e-focus');
  if(k>=4 && v.solution_bc!=null)o+=text('full-base',220,290,`BC = ${v.solution_bc} cm`,'g10e-focus');
  if(k>=4 && v.mode==='diagnosis')o+=text('corrected-midsegment',230,185,`DE = ${v.de} cm`,'g10e-focus');
  return o;
 }
 function render(params,state,phase,n){
  const scene=JSON.parse(params.scene_json),v=scene.visual?.values,k=stage(state,phase);
  if(scene.id!==params.question_id||scene.problem!==params.prompt||scene.lesson!==n||v?.lesson!==n||scene.visual?.family!=='grade10_euclidean')throw Error('Geometry scene belongs to another question');
  const svg=v.model==='parallel'||v.model==='intersect'?crossings(v,k):v.model==='paired_triangles'?triangles(v,k):v.model==='quadrilateral'?quadrilateral(v,k):v.model==='midpoint'?midpoint(v,k):null;
  if(svg==null)throw Error('Unsupported geometry model');
  return `<section class="g10e-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g10e-model"><svg viewBox="0 0 500 320" role="img" aria-label="${esc(scene.problem)}"><title>${esc(v.model)} construction, stage ${k} of 5</title>${svg}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&k<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&k===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('geometry',`grade10_euc_${n}`,{render:(p,s,phase)=>render(p,s,phase,n)});
})();
