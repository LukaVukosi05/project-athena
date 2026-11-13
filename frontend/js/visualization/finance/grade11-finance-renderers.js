/* Grade 11 Finance: staged timelines and conversions based only on this question. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  const stage=(state,phase)=>{
    const tag=(state.annotations||[]).find(value=>/^stage:\d+$/.test(value));
    const n=Number(tag?.slice(6)||0);
    return phase==='result'?n:Math.max(0,n-1);
  };
  const line=(x1,y1,x2,y2,klass='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${klass}"/>`;
  const text=(x,y,label,klass='')=>`<text x="${x}" y="${y}" class="${klass}">${esc(label)}</text>`;
  const box=(x,y,w,h,klass='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" class="${klass}"/>`;
  const number=v=>Number(v).toLocaleString('en-ZA',{minimumFractionDigits:2,maximumFractionDigits:2});
  function timeline(v,s){
    const p=Number(v.principal),r=Number(v.rate),n=Number(v.years)||1;
    const decay=v.mode==='decay',simple=Boolean(v.simple),rise=v.mode==='growth_then_decay';
    const amount=k=>p*(simple?(1+(decay?-1:1)*r*k):(1+(decay?-1:1)*r)**k);
    let out=text(35,50,`Initial ${v.mode==='population'?'population':'amount'}: ${v.mode==='population'?Math.round(p):`R${number(p)}`}`,'g11-fin-given');
    out+=line(65,200,505,200,'g11-fin-axis');
    for(let k=0;k<=n;k++){
      const x=65+440*k/n;
      out+=line(x,193,x,207,'g11-fin-tick')+text(x-8,226,`${k}`,'g11-fin-tick-label');
      if(k===0||s>=3&&k===1||s>=4&&k<=n){
        out+=`<circle cx="${x}" cy="200" r="${k===n&&s>=5?8:6}" class="g11-fin-point"/>`;
        if(k<n||s>=5)out+=text(Math.max(35,x-35),174,v.mode==='population'?Math.round(amount(k)):`R${number(amount(k))}`,'g11-fin-amount');
      }
    }
    if(s>=2)out+=text(35,90,`${decay?'Depreciation':'Growth'}: ${simple?'original base each year':'changing balance each year'}`,'g11-fin-method');
    if(s>=3)out+=text(35,119,`Annual rate ${r*100}% over ${n} year(s)`,'g11-fin-method');
    if(rise&&s>=4)out+=text(35,271,`Then one fall of ${Number(v.decline)*100}% on the grown price`,'g11-fin-method');
    if(rise&&s>=5)out+=text(35,296,`Final after fall: R${number(amount(n)*(1-Number(v.decline)))}`,'g11-fin-check');
    if(s>=5)out+=text(35,316,'Check direction, units and final rounding in the written solution.','g11-fin-check');
    return out;
  }
  function steps(v,s){
    const segments=v.mode==='hire'?
      [`Cash price R${number(v.principal)}`,`Deposit ${Number(v.deposit_rate)*100}%`,`Financed balance`,`Simple interest ${Number(v.rate)*100}%`,`Pay over ${v.months} months`]:
      v.mode==='exchange'?
      [`Earlier: R${number(v.old)} / ${v.currency}`,`Later: R${number(v.new)} / ${v.currency}`,v.direction==='foreign_to_rand'?`${v.quantity} ${v.currency} to rand`:`R${number(v.quantity)} to ${v.currency}`,'Multiply or divide by new quote','Check conversion units']:
      v.mode==='rate_diagnosis'?
      [`Nominal ${Number(v.rate)*100}%`,`Quarterly rate: divide by 4`,'Compound all 4 quarters','Compare nominal with effective','Correct the first error']:
      [`Principal R${number(v.principal)}`,`Nominal ${Number(v.rate)*100}%`,`Period: ${12/v.periods} month(s)`,`Compound ${v.periods} times in one year`,'Compare annual effective rate'];
    let out=line(65,192,500,192,'g11-fin-axis');
    for(let i=0;i<5;i++){
      const x=35+(i%3)*175,y=i<3?48:232;
      out+=box(x,y,160,90,'g11-fin-card')+text(x+11,y+34,`0${i+1}`,'g11-fin-number');
      if(i===0||s>=i)out+=`<foreignObject x="${x+10}" y="${y+44}" width="140" height="43"><div xmlns="http://www.w3.org/1999/xhtml" class="g11-fin-card-text">${esc(segments[i])}</div></foreignObject>`;
    }
    if(s>=5)out+=text(35,350,'Verify the original amount and the units.','g11-fin-check');
    return out;
  }
  function render(p,state,phase,lesson){
    const scene=JSON.parse(p.scene_json);
    if(scene.id!==p.question_id||scene.problem!==p.prompt||scene.lesson!==lesson||scene.visual?.family!=='grade11_finance')throw Error('Finance timeline belongs to another question');
    const s=stage(state,phase),v=scene.visual.values;
    const visual=['growth','inflation','population','decay','growth_then_decay','compare_methods'].includes(v.mode)?timeline(v,s):steps(v,s);
    return `<section class="g11-fin-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-fin-model"><svg viewBox="0 0 560 375" role="img" aria-label="Finance timeline for ${esc(scene.id)}"><title>Question-specific ${esc(v.mode)} model, stage ${s} of 5</title>${visual}</svg></div>
      <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
      <p data-object-id="result">${phase==='result'&&s<5?esc(state.after_state):''}</p>
      <p data-object-id="verification">${phase==='result'&&s===5?esc(state.after_state):''}</p></section>`;
  }
  for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register('finance',`grade11_fin_${n}`,{render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
