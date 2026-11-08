/* Grade 10 source-driven triangle, unit-circle and coordinate constructions. */
(() => {
 const esc=s=>escapeWhiteboardHtml(String(s??''));
 const txt=(id,x,y,value,cls='g10t-label')=>`<text data-object-id="${id}" x="${x}" y="${y}" class="${cls}">${esc(value)}</text>`;
 const line=(id,x1,y1,x2,y2,cls='g10t-line')=>`<line data-object-id="${id}" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`;
 function stage(state,phase){const match=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));const n=Number(match?.slice(6)||0);return phase==='result'?n:Math.max(0,n-1)}
 function triangle(v,step,model){
  const flip=v.orientation==='opposite-horizontal';
  const A=flip?[370,80]:[80,235],B=flip?[370,235]:[370,235],C=flip?[80,235]:[370,80];
  let out=line('adjacent-side',...A,...B)+line('opposite-side',...B,...C)+line('hypotenuse-side',...C,...A);
  const mid=(p,q)=>[(p[0]+q[0])/2,(p[1]+q[1])/2];
  let [ax,ay]=mid(A,B),[ox,oy]=mid(B,C),[hx,hy]=mid(C,A);
  out+=txt('right-angle',B[0]-32,B[1]-22,'∟','g10t-emphasis')+txt('angle-A',A[0]+(flip?-23:11),A[1]+(flip?24:-12),model==='application'?'θ':'A','g10t-emphasis');
  if(step>=(model==='triangle'&&v.lesson===1?2:1))out+=txt('adjacent-label',ax-18,ay+19,`${v.adjacent}${model==='application'?' m':' cm'}`)+txt('opposite-label',ox+13,oy,`${v.opposite}${model==='application'?' m':' cm'}`);
  if(step>=(v.lesson===1?3:2) && v.hypotenuse!=null)out+=txt('hypotenuse-label',hx-5,hy-16,`${v.hypotenuse}${model==='application'?' m':' cm'}`,'g10t-emphasis');
  if(step>=3)out+=line('focus-opposite',...B,...C,'g10t-highlight')+line('focus-adjacent',...A,...B,'g10t-highlight');
  if(step>=4)out+=txt('ratio',55,284,model==='application'?`tan θ = ${v.opposite}/${v.adjacent}`:model==='special'?v.answer:`${v.fn} A = ${v.numerator}/${v.denominator}`,'g10t-emphasis');
  return out;
 }
 function circle(v,step,model){
  const deg=v.degree??0,phi=deg*Math.PI/180,cx=250,cy=155,r=100;
  let out=`<circle data-object-id="unit-circle" cx="${cx}" cy="${cy}" r="${r}" class="g10t-circle"/>`+
   line('horizontal-axis',48,cy,452,cy)+line('vertical-axis',cx,20,cx,290)+txt('origin',257,176,'O')+
   txt('positive-x',440,150,'x')+txt('positive-y',258,28,'y');
  if(model==='solve'){
   if(step>=2)out+=`<path data-object-id="first-quadrant" d="M350 155 A100 100 0 0 0 250 55" class="g10t-highlight" fill="none"/>`;
   if(step>=4 && v.degree!=null)out+=txt('acute-angle',320,130,`${deg}°`,'g10t-emphasis');
   return out;
  }
  const px=cx+r*Math.cos(phi),py=cy-r*Math.sin(phi);
  if(step>=2)out+=line('terminal-side',cx,cy,px,py,'g10t-highlight')+
   `<circle data-object-id="terminal-point" cx="${px.toFixed(2)}" cy="${py.toFixed(2)}" r="6" class="g10t-point"/>`+
   txt('angle',Math.min(410,px+7),Math.max(35,py-7),`${deg}°`,'g10t-emphasis');
  if(step>=3)out+=line('reference-leg',px,py,px,cy,'g10t-dash');
  if(step>=4)out+=txt('quadrant-sign',62,260,v.quadrant??'Mark coordinate signs','g10t-emphasis');
  if(step>=4)out+=txt('exact-value',62,288,v.answer??'Read the signed ratio','g10t-emphasis');
  return out;
 }
 function coordinate(v,step){
  const [x,y]=v.point??[0,0];let out=line('horizontal-axis',40,155,460,155)+line('vertical-axis',250,20,250,290);
  const scale=135/Math.max(1,Math.abs(x),Math.abs(y)),px=250+x*scale,py=155-y*scale;
  if(step>=1)out+=line('radius',250,155,px,py,'g10t-highlight')+
   `<circle data-object-id="point" cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="7" class="g10t-point"/>`+
   txt('point-label',Math.min(px+8,405),Math.max(py-8,30),`P(${x}, ${y})`,'g10t-emphasis');
  if(step>=2)out+=line('vertical-leg',px,py,px,155,'g10t-dash')+line('horizontal-leg',250,155,px,155,'g10t-dash');
  if(step>=3)out+=txt('radius-label',40,285,`r = ${v.radius}`,'g10t-emphasis');
  if(step>=4)out+=txt('signed-ratios',285,285,`y/r, x/r, y/x`,'g10t-emphasis');
  return out;
 }
 function render(p,state,phase,n){
  const scene=JSON.parse(p.scene_json),v=scene.visual?.values,step=stage(state,phase);
  if(scene.id!==p.question_id||scene.problem!==p.prompt||scene.lesson!==n||v?.lesson!==n||scene.visual?.family!=='grade10_trigonometry')throw Error('Trigonometry scene belongs to another question');
  let svg='';
  if(v.model==='triangle'||v.model==='application')svg=triangle(v,step,v.model);
  else if(v.model==='coordinate')svg=coordinate(v,step);
  else if(v.model==='circle'||v.model==='solve')svg=circle(v,step,v.model);
  else if(v.model==='special'){
   if(v.degree===0||v.degree===90)svg=circle(v,step,'circle');
   else{
    const given=v.degree===45?{opposite:1,adjacent:1,hypotenuse:'√2'}:{opposite:v.degree===30?1:'√3',adjacent:v.degree===30?'√3':1,hypotenuse:2};
    svg=triangle({...v,...given,orientation:'opposite-vertical'},step,'special');
   }
  }else throw Error('Unsupported trigonometry scene');
  if(step===5)svg+=txt('answer',40,307,v.answer,'g10t-answer');
  return `<section class="g10t-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g10t-model"><svg viewBox="0 0 500 320" role="img" aria-label="${esc(scene.problem)}"><title>${esc(v.model)} construction, stage ${step} of 5</title>${svg}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&step<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&step===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=7;n++)AthenaVisualizationRegistry.register('geometry',`grade10_trig_${n}`,{render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
