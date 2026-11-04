/* Question-owned Grade 9 ratio, finance and decision diagrams. */
(() => {
  const esc = value => escapeWhiteboardHtml(String(value ?? ''));
  const currency = value => `R${Number(value).toLocaleString('en-ZA')}`;
  const visible = (scene,state,phase) => {
    const marker=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x))||'stage:0';
    const stage=Number(marker.slice(6));
    return phase==='result'?stage:Math.max(0,stage-1);
  };
  const row=(label,value,active=false)=>`<div class="g9-context-row ${active?'is-active':''}"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`;
  const action=(state,phase,done,count)=>`<div class="g9-board-action"><div data-object-id="operation" class="g9-action ${phase==='operation'?'is-active':''}">${phase==='operation'?esc(state.working_state):''}</div><div data-object-id="result" class="g9-action ${phase==='result' && done<count?'is-active':''}">${phase==='result' && done<count?esc(state.after_state):''}</div><div data-object-id="verification" class="g9-action ${phase==='result' && done===count?'is-active':''}">${phase==='result' && done===count?esc(state.after_state):''}</div></div>`;
  const given=scene=>`<div class="g9-context-givens">${(scene.givens||[]).map((x,i)=>`<span data-given="${i}">${esc(x)}</span>`).join('')}</div>`;
  const ratio=(v,done)=>{
    if(v.family==='rate'){
      const t=v.table||[];
      return `<div class="g9-context-table" aria-label="Rate table">${row(`Given ${v.units?.[0]||''}`,t[0]?.[0]??'?',true)}${row(`Given ${v.units?.[1]||''}`,t[0]?.[1]??'?',true)}${done>=2?row('Per one unit',`${t[1]?.[0]} ${v.units?.[0]||''} per ${t[1]?.[1]} ${v.units?.[1]||''}`,true):row('Per one unit','?',false)}</div>`;
    }
    const bars=v.bars||[], labels=v.labels||['first','second'],max=Math.max(1,...bars);
    return `<div class="g9-ratio-bars" aria-label="Ordered ratio bars">${bars.map((n,i)=>`<div class="g9-ratio-item"><span>${esc(labels[i])}: ${esc(n)}</span><div class="g9-ratio-track"><span style="width:${Math.max(5,100*n/max)}%" class="${done>=2?'is-active':''}"></span></div></div>`).join('')}</div>`;
  };
  const proportion=(v,done)=>v.family==='share'?ratio(v,done):`<div class="g9-context-table" aria-label="${v.family==='inverse'?'Inverse':'Direct'} proportion table">${row(v.units?.[0]||'Quantity 1',v.table?.[0]?.[0],true)}${row(v.units?.[1]||'Quantity 2',v.table?.[0]?.[1],true)}${row('Changed '+(v.units?.[0]||'quantity'),v.table?.[1]?.[0],true)}${row('Required '+(v.units?.[1]||'quantity'),done>=3?v.table?.[1]?.[1]:'?',done>=3)}</div><p class="g9-context-rule">${done>=1?(v.family==='inverse'?'Inverse: the product stays fixed':'Direct: the quotient stays fixed'):'Test how both quantities change first'}</p>`;
  const timeline=(v,done,count)=>`<div class="g9-context-timeline" aria-label="Price stages">${(v.timeline||[]).map((n,i)=>`<div class="g9-timeline-node ${i<=done?'is-active':''}"><small>${esc(v.labels?.[i]||'stage')}</small><strong>${i===0||done>=i+1||done>=count-1?currency(n):'?'}</strong></div>`).join('<span class="g9-timeline-arrow" aria-hidden="true">→</span>')}</div>`;
  const ledger=(v,done)=>`<div class="g9-context-ledger" aria-label="Monthly ledger">${row('Income',currency(v.income),true)}${v.planned?row('Planned expenses',v.planned.map(currency).join(' + '),true):''}${(v.expenses||[]).map((n,i)=>row(`${v.planned?'Actual':'Expense'} ${i+1}`,currency(n),done>=1)).join('')}${v.plan?row('Proposed payment',currency(v.plan),true):''}${row('Total fixed expenses',done>=2?currency(v.expenses.reduce((sum,n)=>sum+n,0)):'?',done>=2)}${row('Balance after fixed expenses',done>=3?currency(v.balance):'?',done>=3)}</div>`;
  const interest=(v,done,count)=>`<div class="g9-interest-timeline" aria-label="${esc(v.kind)} interest balance">${(v.balances||[]).map((n,i)=>`<div class="g9-timeline-node ${i<=done?'is-active':''}"><small>${v.kind==='compare'?esc(v.labels[i]):v.kind==='hire'?(i?'All payments':'Deposit'):`Year ${i}`}</small><strong>${(v.kind==='compare'?done>=2:i===0||done>=i+1||done>=count-1)?currency(n):'?'}</strong></div>`).join('<span class="g9-timeline-arrow" aria-hidden="true">→</span>')}</div>`;
  const decision=(v,done)=>{
    if(v.family==='rental_exchange')return `<div class="g9-context-table" aria-label="Foreign and local rental totals">${row('Foreign fixed fee',v.foreign_base+' units',true)}${row('Foreign daily fee',v.foreign_daily+' units/day',true)}${row('Foreign subtotal',done>=1?v.foreign+' units':'?',done>=1)}${row('Rand per unit',currency(v.rate),true)}${row('Conversion fee',currency(v.fee),true)}${row('Foreign plan in rand',done>=2?currency(v.rand_total):'?',done>=2)}${row('Local plan in rand',currency(v.local_total),true)}</div>`;
    if(v.family==='exchange')return `<div class="g9-context-table" aria-label="Currency conversion">${row('Rand supplied',currency(v.source),true)}${row('Rand per foreign unit',currency(v.rate),true)}${row('Foreign units before fee',done>=2?v.gross:'?',done>=2)}${row('Fee, foreign units',v.fee,true)}${row('Foreign units remaining',done>=3?v.net:'?',done>=3)}</div>`;
    if(v.family==='commission')return `<div class="g9-context-table" aria-label="Commission and pay">${row('Sales base',currency(v.sales),true)}${row('Commission rate',`${v.rate}%`,true)}${row('Commission',done>=2?currency(v.commission):'?',done>=2)}${row('Basic pay',currency(v.basic),true)}${row('Total pay',done>=3?currency(v.total):'?',done>=3)}</div>`;
    return `<div class="g9-context-table" aria-label="Rental plan comparison">${row('Rental days',v.days,true)}${['A','B'].map((name,i)=>row(`Plan ${name}: fixed + daily`,`${currency(v.base[i])} + ${currency(v.daily[i])}/day`,true)).join('')}${['A','B'].map((name,i)=>row(`Plan ${name}: total`,done>=2?currency(v.totals[i]):'?',done>=2)).join('')}</div>`;
  };
  const visual={grade9_ratio_rate:ratio,grade9_proportion:proportion,grade9_transaction:timeline,grade9_ledger:ledger,grade9_interest:interest,grade9_decision:decision};
  for(const [template,draw] of Object.entries(visual))AthenaVisualizationRegistry.register('algebra',template,{
    render(parameters,state,phase){
      const scene=JSON.parse(parameters.scene_json),count=Number(parameters.total_steps),done=visible(scene,state,phase);
      const family=scene.visual||{family:'givens'};
      const model=family.family==='givens'?given(scene):draw(family,done,count);
      return `<section class="g9-context-board" data-managed-visibility="true" data-question-id="${esc(parameters.question_id)}" data-phase="${esc(phase)}"><p class="g9-given" data-object-id="problem">${esc(parameters.prompt)}</p>${given(scene)}<div class="g9-context-model" data-object-id="model">${model}</div><p class="g9-selection" data-object-id="selection">${scene.answer && done>=count-1?`Result: ${esc(scene.answer)}`:''}</p>${action(state,phase,done,count)}</section>`;
    },destroy(){}
  });
})();
