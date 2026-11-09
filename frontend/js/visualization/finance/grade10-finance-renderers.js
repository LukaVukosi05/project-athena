(function(){
 const esc=x=>escapeWhiteboardHtml(String(x));
 const stage=s=>Math.max(1,Math.min(5,Number((s.annotations||[]).find(x=>/^stage:\d+$/.test(x))?.split(':')[1]||1)));
 const fmt=x=>`R${Number(x).toLocaleString('en-ZA',{minimumFractionDigits:2,maximumFractionDigits:2})}`;
 const txt=(id,x,y,value)=>`<text data-object-id="${id}" x="${x}" y="${y}" class="g10fin-label">${esc(value)}</text>`;
 function render(p,state,phase,n){
  const q=JSON.parse(p.scene_json),v=q.visual?.values,k=stage(state);
  if(q.id!==p.question_id||q.problem!==p.prompt||q.lesson!==n||q.visual?.family!=='grade10_finance'||v?.lesson!==n)throw Error('Finance scene belongs to another question');
  if(!Number.isFinite(Number(v.principal))||Number(v.principal)<=0||!Number.isFinite(Number(v.rate))||Number(v.rate)<=0)throw Error('Invalid financial givens');
  const mode=v.mode,principal=Number(v.principal),rate=Number(v.rate),years=Number(v.years);
  let plot=`<line data-object-id="time-axis" x1="45" y1="240" x2="535" y2="240" class="g10fin-axis"/>`;
  const labels=mode===4?['Deposit','Balance','Interest','Instalment']:mode===5?['Starting currency','Rate','Convert','Answer']:['Principal','Rate','Periods','Amount'];
  let details;
  if(v.unit==='people') details=[`${Number(principal).toLocaleString('en-ZA')} residents`,`${(rate*100).toFixed(0)}% per year`,`${years} years`,v.amount?`${Number(v.amount).toLocaleString('en-ZA')} residents`:'future population'];
  else if(mode===4) details=[fmt(principal),`${(rate*100).toFixed(0)}% simple interest`,`${years} years`,v.instalment?fmt(v.instalment):'monthly amount'];
  else if(mode===5&&v.direction==='compare') details=[`US$${principal.toFixed(2)}`,`R${rate.toFixed(2)} → R${Number(v.new_rate).toFixed(2)} per US$`,v.old_amount?`Old cost: ${fmt(v.old_amount)}`:'old cost',v.amount?`New cost: ${fmt(v.amount)}`:'new cost'];
  else if(mode===5) details=[`${v.unit==='USD'?'Rand':'US dollars'} ${principal.toFixed(2)}`,`R${rate.toFixed(2)} per US$`,v.direction==='divide'?'÷ rate':'× rate',v.amount?`${v.unit==='USD'?'US$':'R'}${Number(v.amount).toFixed(2)}`:'converted amount'];
  else details=[fmt(principal),`${(rate*100).toFixed(0)}% per year`,v.periods?`${v.periods} months`:`${years} years`,v.amount?fmt(v.amount):'final value'];
  for(let j=0;j<4;j++){
   const x=75+j*143,active=j<Math.min(k,4);
   plot+=`<circle data-object-id="stage-${j+1}" cx="${x}" cy="240" r="${active?11:7}" class="g10fin-${active?'active':'pending'}"/>`+txt(`stage-label-${j+1}`,x-45,210,labels[j]);
   if(active)plot+=txt(`stage-value-${j+1}`,x-51,275,details[j]);
  }
  if(k>=4&&mode===2&&v.simple)plot+=txt('comparison',55,335,`Simple amount: ${fmt(v.simple)}; compound amount: ${fmt(v.amount)}`);
  if(k>=4&&mode===4&&v.deposit)plot+=txt('payment-split',55,335,`Deposit ${fmt(v.deposit)}; financed balance ${fmt(v.balance)}`);
  if(k>=4&&mode===5&&v.direction==='compare'&&v.difference)plot+=txt('rate-difference',55,335,`Additional rand cost: ${fmt(v.difference)}`);
  if(k>=4&&mode===3)plot+=txt('growth-direction',55,335,v.direction==='down'?'Value falls each year':'Value rises each year');
  return `<section class="g10fin-board" data-managed-visibility="true" data-question-id="${esc(q.id)}"><p data-object-id="problem">${esc(q.problem)}</p><div data-object-id="model" class="g10fin-model"><svg viewBox="0 0 580 380" role="img" aria-label="Finance calculation for ${esc(q.id)}"><title>Question-specific finance timeline, stage ${k} of 5</title>${plot}</svg></div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&k<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&k===5?esc(state.after_state):''}</p></section>`;
 }
 for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('finance',`grade10_fin_${n}`,{render:(p,s,phase)=>render(p,s,phase,n)});
})();
