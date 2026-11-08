(function(){
 const esc=x=>escapeWhiteboardHtml(String(x));
 const stage=(state,phase)=>Math.max(1,Math.min(5,Number((state.annotations||[]).find(x=>/^stage:\d+$/.test(x))?.split(':')[1]||1)));
 const label=(id,x,y,t)=>`<text data-object-id="${id}" x="${x}" y="${y}" class="g10s-label">${esc(t)}</text>`;
 function raw(v,k,n){
  const data=v.data||[],other=v.other||[],all=data.concat(other),low=Math.min(...all),high=Math.max(...all),span=Math.max(1,high-low);let out='';
  const map=x=>50+420*(x-low)/span;
  out+=`<line data-object-id="axis" x1="50" y1="250" x2="470" y2="250" class="g10s-axis"/>`;
  for(const [j,x] of [[0,low],[1,high]])out+=label(`tick-${j}`,map(x)-9,275,x);
  for(const [j,x] of data.entries())out+=`<circle data-object-id="observation-${j}" cx="${map(x)}" cy="${215-12*(j%3)}" r="4" class="g10s-dot"/>`;
  if(other.length){for(const [j,x] of other.entries())out+=`<circle data-object-id="other-${j}" cx="${map(x)}" cy="${100-12*(j%3)}" r="4" class="g10s-other"/>`;out+=label('group-a',52,150,'Group A')+label('group-b',52,55,'Group B')}
  if(n===1&&k>=3){
   const mean=data.reduce((a,b)=>a+b,0)/data.length,median=(data[4]+data[5])/2;
   out+=`<line data-object-id="mean-marker" x1="${map(mean)}" y1="68" x2="${map(mean)}" y2="145" class="g10s-median"/>`;
   out+=`<line data-object-id="median-marker" x1="${map(median)}" y1="154" x2="${map(median)}" y2="215" class="g10s-whisker"/>`;
   if(k>=4)out+=label('mean-label',Math.min(map(mean)+7,410),61,`mean ${mean.toFixed(1)}`)+label('median-label',Math.min(map(median)+7,410),165,`median ${median}`);
  }
  if(n!==1&&k>=3){
   const groups=other.length?[[data,195,'a'],[other,95,'b']]:[[data,145,'a']];
   for(const [a,y,id] of groups){const median=(a[4]+a[5])/2,q1=a[2],q3=a[7];
    out+=`<line data-object-id="whisker-${id}" x1="${map(a[0])}" y1="${y}" x2="${map(a[9])}" y2="${y}" class="g10s-whisker"/>`;
    out+=`<rect data-object-id="box-${id}" x="${map(q1)}" y="${y-18}" width="${map(q3)-map(q1)}" height="36" class="g10s-box"/>`;
    out+=`<line data-object-id="median-${id}" x1="${map(median)}" y1="${y-18}" x2="${map(median)}" y2="${y+18}" class="g10s-median"/>`;
    for(const [j,t] of [a[0],q1,median,q3,a[9]].entries())out+=label(`summary-${id}-${j}`,Math.max(38,Math.min(450,map(t)-9)),y+38,t);
   }
  }
  if(k>=2)out+=label('count',55,305,`n = ${data.length}${other.length?` in each group`:''}`);
  return out;
 }
 function grouped(v,k,n){
  const f=v.frequencies,lo=v.lower,hi=v.upper,width=390/f.length,top=Math.max(...f)+1;let out='';
  if(n===2){
   out+=label('table-title',55,46,'Class interval       frequency       midpoint       cumulative');
   let cumulative=0;
   for(let j=0;j<f.length;j++){
    cumulative+=f[j];let y=95+j*55;
    out+=`<line data-object-id="row-rule-${j}" x1="48" y1="${y+15}" x2="455" y2="${y+15}" class="g10s-axis"/>`;
    out+=label(`class-${j}`,55,y,`${lo[j]}–${hi[j]}`);
    if(k>=2)out+=label(`frequency-${j}`,175,y,f[j]);
    if(k>=3)out+=label(`midpoint-${j}`,275,y,v.midpoints[j]);
    if(k>=4)out+=label(`cumulative-${j}`,390,y,cumulative);
   }
   return out;
  }
  out+=`<line data-object-id="frequency-axis" x1="50" y1="260" x2="455" y2="260" class="g10s-axis"/>`;
  for(let j=0;j<f.length;j++){
   const x=50+j*width,h=170*f[j]/top;
   out+=label(`class-${j}`,x+5,283,`${lo[j]}–${hi[j]}`);
   if(k>=2)out+=`<rect data-object-id="frequency-${j}" x="${x}" y="${260-h}" width="${n===5?width:width-8}" height="${h}" class="g10s-bar"/>`;
   if(k>=3)out+=label(`frequency-label-${j}`,x+width/2-4,250-h,f[j]);
   if(n===2 && k>=4)out+=label(`midpoint-${j}`,x+5,309,`m=${v.midpoints[j]}`);
  }
  out+=label('frequency-heading',55,42,n===5?'Frequency (touching bars: equal-width continuous classes)':'Grouped frequencies');
  return out;
 }
 function render(p,state,phase,n){
  const scene=JSON.parse(p.scene_json),v=scene.visual?.values,k=stage(state,phase);
  if(scene.id!==p.question_id||scene.problem!==p.prompt||scene.lesson!==n||v?.lesson!==n||scene.visual?.family!=='grade10_statistics')throw Error('Statistics scene belongs to another question');
  if(!Array.isArray(v.data)||v.data.length!==10||v.data.some(x=>!Number.isFinite(x)))throw Error('Statistics values missing');
  const model=n===2||n===5?grouped(v,k,n):raw(v,k,n);
  return `<section class="g10s-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g10s-model"><svg viewBox="0 0 500 330" role="img" aria-label="Statistics display for ${esc(scene.id)}"><title>Question-specific statistics, stage ${k} of 5</title>${model}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&k<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&k===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('statistics',`grade10_stat_${n}`,{render:(p,s,phase)=>render(p,s,phase,n)});
})();
