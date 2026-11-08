/* Question-specific Grade 10 algebra stages. Previous stages stay in the cumulative memo. */
(() => {
 const esc=s=>escapeWhiteboardHtml(String(s??''));
 const tag=(id,x,y,value,cls='g10e-text')=>`<text data-object-id="${id}" x="${x}" y="${y}" class="${cls}">${esc(value)}</text>`;
 const rect=(id,x,y,w,h)=>`<rect data-object-id="${id}" x="${x}" y="${y}" width="${w}" height="${h}" rx="11" class="g10e-box"/>`;
 function stepOf(state,phase){const found=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));return phase==='result'?Number(found?.slice(6)||0):Math.max(0,Number(found?.slice(6)||0)-1)}
 function render(p,state,phase,n){
  const scene=JSON.parse(p.scene_json),v=scene.visual?.values,step=stepOf(state,phase);
  if(scene.id!==p.question_id||scene.problem!==p.prompt||scene.lesson!==n||v?.lesson!==n||v?.family==='missing')throw Error('Equation visual belongs to another question');
  const kind=v.kind;
  let svg='';
  if(kind==='inequality'){
   svg+=`<line class="g10e-axis" x1="48" y1="165" x2="452" y2="165"/>`;
   const bound=v.bound??v.a+1;const neg=v.direction==='left'||v.form==='negative_divisor';
   if(step>=2)for(let j=-3;j<=3;j++)svg+=`<line class="g10e-tick" x1="${250+j*56}" y1="155" x2="${250+j*56}" y2="175"/>`+tag('tick-'+j,239+j*56,197,bound+j);
   if(step>=1)svg+=tag('given',36,49,scene.problem,'g10e-small');
   if(step>=2)svg+=tag('inverse',42,92,neg?'Divide by a negative: reverse the sign.':'Divide by a positive: keep the sign.','g10e-emphasis');
   if(step>=3)svg+=`<circle data-object-id="boundary" cx="250" cy="165" r="9" class="${v.closed?'g10e-closed':'g10e-open'}"/>`;
   if(step>=4)svg+=`<path data-object-id="solution-ray" d="M250 165 L${neg?64:435} 165" class="g10e-ray"/>`+
    `<path d="M${neg?64:435} 165 l${neg?12:-12} -8 m${neg?-12:12} 8 l${neg?12:-12} 8" class="g10e-ray"/>`;
   if(step>=5)svg+=tag('interval',37,258,v.result,'g10e-emphasis');
  }else if(kind==='quadratic'){
   svg+=rect('original-equation',65,30,370,65)+tag('original',83,72,scene.problem,'g10e-small');
   if(step>=2)svg+=`<path d="M250 96 V134 M250 134 H125 V165 M250 134 H375 V165" class="g10e-axis"/>`;
   if(step>=2)svg+=rect('factor-left',47,165,170,74)+tag('factor-one',57,208,`x − ${v.r}`,'g10e-emphasis');
   if(step>=3)svg+=rect('factor-right',284,165,170,74)+tag('factor-two',294,208,`x ${v.t<0?'+':'−'} ${Math.abs(v.t)}`,'g10e-emphasis');
   if(step>=4)svg+=tag('roots',95,276,`x = ${v.r}       or       x = ${v.t}`,'g10e-emphasis');
  }else if(kind==='simultaneous'||(kind==='word'&&v.form==='tickets')){
   const eq1=kind==='simultaneous'?`x + y = ${v.u}`:`2A + C = ${v.total}`;
   const eq2=kind==='simultaneous'?`x − y = ${v.v}`:`A − C = ${v.a}`;
   svg+=rect('first-equation',50,47,395,69)+tag('eq1',72,90,eq1,'g10e-emphasis');
   if(step>=2)svg+=rect('second-equation',50,125,395,69)+tag('eq2',72,168,eq2,'g10e-emphasis');
   if(step>=3)svg+=tag('method',65,222,kind==='simultaneous'?'Add columns to eliminate y.':'Substitute A = C + difference.','g10e-small');
   if(step>=4)svg+=tag('solution',65,266,v.result,'g10e-emphasis');
  }else if(kind==='exponent'){
   svg+=tag('base',42,52,'SAME BASE','g10e-small')+rect('first-power',45,80,160,80)+rect('second-power',295,80,160,80);
   svg+=tag('first',80,130,v.form==='zero'?`${v.a} × x⁰`:`x^${v.m}`,'g10e-emphasis');
   if(step>=2)svg+=tag('second',330,130,v.form==='zero'?'x^−2':`x^${v.k}`,'g10e-emphasis');
   if(step>=3)svg+=`<path d="M205 120 H290" class="g10e-axis"/>`+tag('law',60,218,v.form==='zero'?'x⁰ = 1; x^−2 = 1/x²':v.form==='product'?'Distribute the power across both bases.':'Add powers in the numerator; subtract for division.','g10e-small');
   if(step>=4)svg+=tag('reciprocal',60,258,'A negative power means reciprocal.','g10e-small');
   if(step>=5)svg+=tag('derived',60,292,v.result,'g10e-emphasis');
  }else if(kind==='rational'){
   svg+=rect('radical',60,52,380,90)+tag('root',85,107,v.form==='root'? `√x = ${v.a}`:`∛x = ${v.a}`,'g10e-emphasis');
   if(step>=2)svg+=`<path d="M250 144 V195" class="g10e-axis"/>`+tag('inverse',83,218,v.form==='root'?'Square both sides.':'Cube both sides.','g10e-emphasis');
   if(step>=3)svg+=tag('power',83,260,v.form==='root'?`${v.a}² = ${v.base}`:`${v.a}³ = ${v.base}`,'g10e-emphasis');
   if(step>=5)svg+=tag('derived',300,260,v.result,'g10e-emphasis');
  }else if(kind==='linear'||kind==='literal'){
   svg+=rect('left-side',45,47,180,90)+rect('right-side',275,47,180,90);
   svg+=tag('left-label',57,72,'LEFT SIDE','g10e-small')+tag('right-label',287,72,'RIGHT SIDE','g10e-small');
   svg+=tag('left',55,113,kind==='linear'?`${v.a}(x+${v.b})+${v.c}`:v.form==='motion'?`u + ${v.a}t`:`½(${v.a}+${v.b})h`,'g10e-small');
   if(step>=2)svg+=tag('right',289,113,kind==='linear'?String(v.rhs):v.form==='motion'?'v':'A','g10e-emphasis');
   if(step>=3)svg+=`<path d="M130 141 V188 M370 141 V188" class="g10e-axis"/>`+tag('both-sides',80,213,'Apply the same legal inverse to both sides.','g10e-small');
   if(step>=4)svg+=rect('isolated',75,239,350,57)+tag('isolated-text',95,275,v.result,'g10e-emphasis');
  }else if(kind==='word'){
   if(v.form==='rectangle'){
    svg+=rect('rectangle',105,62,288,157)+tag('length',239,52,`${v.a} cm`,'g10e-emphasis')+tag('width',400,154,'w ?','g10e-emphasis');
    if(step>=2)svg+=tag('perimeter',90,254,`Perimeter = ${v.perimeter} cm`,'g10e-emphasis');
   }else{
    svg+=rect('notebook-one',47,65,95,121)+rect('notebook-two',164,65,95,121)+rect('fee',293,80,159,82);
    svg+=tag('price-one',67,132,'p','g10e-emphasis')+tag('price-two',184,132,'p','g10e-emphasis')+tag('price-fee',306,131,`Fee R${v.b}`,'g10e-small');
    if(step>=2)svg+=tag('total',96,247,`Total R${v.total}`,'g10e-emphasis');
   }
   if(step>=5)svg+=tag('derived',100,289,v.result,'g10e-emphasis');
  }
  svg+=tag('stage',429,302,`${step}/5`,'g10e-small');
  return `<section class="g10e-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g10e-model"><svg viewBox="0 0 500 315" role="img" aria-label="${esc(scene.problem)}"><title>Question-specific ${esc(kind)} model, stage ${step} of 5</title>${svg}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&step<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&step===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=9;n++)AthenaVisualizationRegistry.register('algebra',`grade10_eei_${n}`,{render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
