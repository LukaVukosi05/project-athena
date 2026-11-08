/* Each Grade 9 measurement diagram is built from that question's dimensions. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 const t=(id,x,y,s)=>`<text data-object-id="${id}" x="${x}" y="${y}">${esc(s)}</text>`;
 const r=(id,x,y,w,h,cls='g9-sv-face')=>`<rect data-object-id="${id}" x="${x}" y="${y}" width="${w}" height="${h}" class="${cls}"/>`;
 const l=(x,y,X,Y,cls='g9-sv-line')=>`<line x1="${x}" y1="${y}" x2="${X}" y2="${Y}" class="${cls}"/>`;
 const p=(id,pts,cls='g9-sv-face')=>`<polygon data-object-id="${id}" points="${pts}" class="${cls}"/>`;
 const c=(id,x,y,rad,cls='g9-sv-face')=>`<circle data-object-id="${id}" cx="${x}" cy="${y}" r="${rad}" class="${cls}"/>`;
 const done=(state,phase)=>{const mark=(state.annotations||[]).find(s=>/^stage:\d+$/.test(s));const n=mark?Number(mark.slice(6)):0;return phase==='result'?n:Math.max(0,n-1)};
 const clamp=(x,lo,hi)=>Math.min(hi,Math.max(lo,x));
 function boxNet(v,step,open=false){
  const L=v.length,W=v.width,H=v.height,cube=v.shape==='cube';
  const width=cube?55:clamp(48+L,65,86),depth=cube?55:clamp(32+W*2,42,70),height=cube?55:clamp(32+H*2,42,70);
  const x=60,y=122;let markup=t('dimensions',22,29,`length ${L} cm · width ${W} cm · height ${H} cm`);
  if(step>=1)markup+=r('base',x,y+height,width,depth);
  if(step>=2)markup+=open?(step===2?r('incorrect-top',x,y-depth,width,depth,'g9-sv-ghost'):''):r('opposite-base',x,y-depth,width,depth);
  if(step>=3){markup+=r('wall-front',x,y,width,height);
   if(open)markup+=r('side-1',x-depth,y,depth,height);
   else markup+=r('side-1',x+width,y,depth,height)+r('side-2',x+width+depth,y,width,height)+r('side-3',x+2*width+depth,y,depth,height)}
  if(step>=4){if(open)markup+=r('side-2',x+width,y,depth,height)+r('side-3',x+width+depth,y,width,height)+r('side-4',x+2*width+depth,y,depth,height);
   markup+=t('face-pairs',210,251,open?`Material = ${L*W+2*L*H+2*W*H} cm²`:`Area = ${2*(L*W+L*H+W*H)} cm²`)}
  if(step>=5)markup+=t('net-check',18,281,open?'Open top is excluded.':'All six face pieces have matching adjoining edges.');
  return markup;
 }
 function boxLayers(v,step){
  const L=v.length,W=v.width,H=v.height;let out=t('dimensions',17,28,`${L} cm × ${W} cm × ${H} cm`);
  out+=p('base','82,173 270,173 321,132 133,132');
  if(step>=1)out+=t('base-width',126,194,`${L} cm`)+t('base-depth',280,154,`${W} cm`);
  if(step>=2)out+=t('base-area',86,237,`One base layer: ${L} × ${W} cm²`);
  if(step>=3){out+=p('stack-side','82,173 82,91 133,50 133,132','g9-sv-layer')+p('stack-front','82,173 270,173 270,91 82,91','g9-sv-layer');
   out+=p('stack-top','82,91 270,91 321,50 133,50');out+=t('height',19,109,`${H} cm`)}
  if(step>=4)out+=t('volume',315,198,`V = ${L*W*H} cm³`)+t('litre',307,223,`1 L = 1000 cm³`);
  if(step>=5)out+=t('check',22,280,'Multiply litres by 1000 to recover cm³.');
  return out;
 }
 function trianglePrism(v,step){
  const B=v.base,T=v.altitude,C=v.hypotenuse,depth=v.length;let out=t('dimensions',17,28,`Right triangle: ${B}, ${T}, ${C} cm · prism ${depth} cm`);
  out+=p('triangle-front','79,196 199,196 79,61');out+=l(79,183,92,183)+l(92,183,92,196);
  if(step>=1)out+=t('base',132,219,`${B} cm`)+t('altitude',20,134,`${T} cm`)+t('hypotenuse',153,125,`${C} cm`);
  if(step>=2)out+=t('triangle-area',223,57,`A = ½ × ${B} × ${T} cm²`);
  if(step>=3){out+=p('triangle-back','157,141 277,141 157,6','g9-sv-back');out+=l(79,61,157,6)+l(199,196,277,141)+l(79,196,157,141);out+=t('prism-length',276,161,`${depth} cm`)}
  if(step>=4)out+=t('side-faces',213,207,`A = ${B*T+(B+T+C)*depth} cm²`);
  if(step>=5)out+=t('check',18,280,'Two triangles + three rectangles; cm² and cm³ differ.');
  return out;
 }
 function cylinder(v,step){
  const radius=v.radius,height=v.height;let out=t('dimensions',17,28,`radius ${radius} cm · height ${height} cm`);
  out+=r('curved-wall',67,85,149,115,'g9-sv-curved');out+=`<ellipse data-object-id="circle-top" cx="141.5" cy="85" rx="74.5" ry="22" class="g9-sv-face"/>`;
  out+=`<path data-object-id="circle-bottom" d="M 67 200 A 74.5 22 0 0 0 216 200" class="g9-sv-outline"/>`;
  if(step>=1)out+=l(141,85,207,85)+t('radius',157,74,`r=${radius}`)+t('height',15,151,`h=${height}`);
  if(step>=2)out+=c('base-disc',141,85,20,'g9-sv-active')+t('base-area',252,56,`πr² = ${radius*radius}π cm²`);
  if(step>=3)out+=r('volume-layer',91,108,100,62,'g9-sv-layer')+t('volume',252,96,`V = ${radius*radius*height}π cm³`);
  if(step>=4)out+=r('unwrapped-wall',250,130,160,71,'g9-sv-active')+t('unwrapped-label',255,220,`Wall = ${2*radius*height}π cm²`)+t('total-area',250,245,`Total = ${2*radius*(radius+height)}π cm²`);
  if(step>=5)out+=t('check',20,280,'Closed cylinder: two discs plus the curved wall.');
  return out;
 }
 function scaled(v,step){
  const L=v.length,W=v.width,H=v.height;let out=t('dimensions',18,27,`Original ${L} cm × ${W} cm × ${H} cm`);
  out+=p('original-box','65,171 180,171 207,143 92,143')+p('original-top','65,143 180,143 207,115 92,115');
  if(step>=1)out+=t('original-label',55,210,'Original prism');
  if(step>=2)out+=t('original-volume',45,241,`${L} × ${W} × ${H} cm³`);
  if(v.kind==='litres'){
   if(step>=3)out+=t('conversion',243,122,'1000 cm³ = 1 L');
   if(step>=4)out+=t('capacity',243,169,`Capacity: ${(L*W*H)}/1000 L`);
  }else{
   if(step>=3)out+=t('new-dimensions',233,48,v.kind==='one_axis'?`New length ${2*L} cm`:'All three edges double');
   if(step>=4)out+=p('scaled-box','257,172 409,172 442,136 290,136','g9-sv-active')+p('scaled-top','257,136 409,136 442,100 290,100','g9-sv-active')+t('scaled-volume',245,238,`V = ${L*W*H*(v.kind==='one_axis'?2:8)} cm³`);
  }
  if(step>=5)out+=t('check',19,279,v.kind==='litres'?'Convert L back to cm³ to check.':`Volume factor: ${v.kind==='one_axis'?2:8}.`);
  return out;
 }
 function applied(v,step){
  const kind=v.kind;let out='';
  if(kind==='open_box')out=boxNet(v,Math.min(step,4),true);
  else if(kind==='triangle')out=trianglePrism(v,Math.min(step,4));
  else if(kind==='cylinder')out=cylinder(v,Math.min(step,4));
  else out=scaled({...v,kind:kind==='double_all'?'all_axes':'litres'},Math.min(step,4));
  if(step===3)out+=t('first-error',19,255,({open_box:'A top face was included.',triangle:'The ½ in triangle area was omitted.',cylinder:'The diameter was squared instead of the radius.',double_all:'Volume was doubled instead of multiplied by 8.',convert:'Divide by 1000, not 100.'})[kind]);
  if(step>=4&&kind==='triangle')out+=t('correct-volume',19,253,`Volume = ${v.base*v.altitude*v.length/2} cm³`);
  if(step>=4&&kind==='cylinder')out+=t('correct-volume',19,253,`Volume = ${v.radius*v.radius*v.height}π cm³`);
  if(step>=5)out+=t('check',19,279,'Recheck the original dimensions, units and omitted face.');
  return out;
 }
 for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('geometry',`grade9_surface_${n}`,{
  render(params,state,phase){
   const scene=JSON.parse(params.scene_json),v=scene.visual?.values,stage=done(state,phase);
   if(!v||scene.id!==params.question_id||scene.lesson!==n||scene.problem!==params.prompt)throw Error('Measurement scene belongs to another question');
   const picture=n===1?boxNet(v,stage):n===2?boxLayers(v,stage):n===3?trianglePrism(v,stage):n===4?cylinder(v,stage):n===5?scaled(v,stage):applied(v,stage);
   return `<section class="g9-sv-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g9-sv-model"><svg viewBox="0 0 500 300" role="img" aria-label="${esc(scene.problem)}"><title>Labelled ${esc(v.model)} from this question</title>${picture}${t('stage-label',21,298,stage?`Step ${stage} of 5`:'Read the givens')}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&stage<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&stage===5?esc(state.after_state):''}</p></section>`;
  },destroy(){}
 });
})();
