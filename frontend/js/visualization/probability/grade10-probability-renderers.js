(function(){
 const esc=x=>escapeWhiteboardHtml(String(x));
 const stage=s=>Math.max(1,Math.min(5,Number((s.annotations||[]).find(x=>/^stage:\d+$/.test(x))?.split(':')[1]||1)));
 const text=(id,x,y,value)=>`<text data-object-id="${id}" x="${x}" y="${y}" class="g10p-label">${esc(value)}</text>`;
 function venn(v,k){
  let out=`<rect data-object-id="universe" x="26" y="32" width="448" height="260" rx="12" class="g10p-universe"/>`;
  out+=`<circle data-object-id="event-a" cx="205" cy="152" r="96" class="g10p-event-a"/><circle data-object-id="event-b" cx="295" cy="152" r="96" class="g10p-event-b"/>`;
  out+=text('event-a-label',150,76,'A')+text('event-b-label',345,76,'B')+text('space-label',36,54,'S');
  if(k>=2)out+=text('overlap-count',241,162,v.both);
  if(k>=3)out+=text('a-only-count',150,162,v.a_only)+text('b-only-count',330,162,v.b_only);
  if(k>=4)out+=text('outside-count',415,265,v.neither)+text('universe-total',37,271,`|S| = ${v.total}`);
  if(k>=5)out+=text('event-counts',92,319,`|A|=${v.a}   |B|=${v.b}   |A∪B|=${v.union}`);
  return out;
 }
 function frequency(v,k){
  const obs=v.hits/v.trials,theory=v.favourable/v.faces;
  let out=text('trials',40,50,`${v.hits} successes in ${v.trials} trials`);
  out+=`<line data-object-id="probability-axis" x1="100" y1="260" x2="450" y2="260" class="g10p-axis"/>`;
  out+=text('zero-tick',90,280,'0')+text('one-tick',445,280,'1');
  if(k>=2)out+=`<rect data-object-id="observed-bar" x="100" y="112" width="${Math.round(350*obs)}" height="43" class="g10p-observed"/>`+text('observed-label',20,139,'Observed');
  if(k>=3)out+=`<rect data-object-id="theoretical-bar" x="100" y="191" width="${Math.round(350*theory)}" height="43" class="g10p-theory"/>`+text('theoretical-label',20,218,'Theory');
  if(k>=4)out+=text('fraction-compare',145,316,`${v.hits}/${v.trials} versus ${v.favourable}/${v.faces}`);
  return out;
 }
 function render(p,state,phase,n){
  const q=JSON.parse(p.scene_json),v=q.visual?.values,k=stage(state);
  if(q.id!==p.question_id||q.problem!==p.prompt||q.lesson!==n||v?.lesson!==n||q.visual?.family!=='grade10_probability')throw Error('Probability scene belongs to another question');
  if(n===1){if(!Number.isInteger(v.trials)||v.trials<=0||!Number.isInteger(v.hits)||v.hits>v.trials)throw Error('Invalid frequency model')}
  else if(k>1&&(!['a_only','b_only','both','neither','total'].every(key=>Number.isInteger(v[key])&&v[key]>=0)||v.a_only+v.b_only+v.both+v.neither!==v.total))throw Error('Invalid Venn model');
  const diagram=n===1?frequency(v,k):venn(v,k);
  return `<section class="g10p-board" data-managed-visibility="true" data-question-id="${esc(q.id)}"><p data-object-id="problem">${esc(q.problem)}</p><div data-object-id="model" class="g10p-model"><svg viewBox="0 0 500 340" role="img" aria-label="Probability model for ${esc(q.id)}"><title>Question-specific probability, stage ${k} of 5</title>${diagram}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&k<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&k===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=5;n++)AthenaVisualizationRegistry.register('statistics',`grade10_prob_${n}`,{render:(p,s,phase)=>render(p,s,phase,n)});
})();
