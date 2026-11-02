/* Question-specific signed axis with persistent markers and cumulative jumps. */
(() => {
  const esc=v=>escapeWhiteboardHtml(String(v??''));
  AthenaVisualizationRegistry.register('algebra','grade8_integer_board',{
    render(p,state,phase){
      const s=JSON.parse(p.scene_json),step=Number(((state.annotations||[]).find(v=>v.startsWith('stage:'))||'stage:0').slice(6));
      const done=phase==='result'?step:Math.max(0,step-1),final=done===p.total_steps;
      const [lo,hi]=s.axis,at=v=>32+((v-lo)/(hi-lo))*536;
      const points=new Set([lo,hi,0]);
      if(s.model==='integer_line') for(const v of s.values)points.add(v);
      else {points.add(s.start);for(const v of (s.path||[]).slice(0,Math.max(1,done-1)))points.add(v);}
      const tick=Array.from(points).sort((a,b)=>a-b).map(v=>`<g data-object-id="tick-${v}" transform="translate(${at(v)},0)"><line y1="70" y2="81" stroke="#6482a5"/><text y="101" text-anchor="middle">${esc(v)}</text></g>`).join('');
      let motion='';
      if(s.model==='integer_line'){
        const revealed=done>=2;
        motion=s.values.map((v,i)=>revealed?`<g data-object-id="given-${i+1}" transform="translate(${at(v)},70)"><circle r="6" fill="#215eaf"/><text text-anchor="middle" y="-12">${esc(v)}</text></g>`:'').join('');
        if(done>=3&&s.kind==='distance')motion+=`<path data-object-id="measured-gap" d="M${at(s.values[0])} 48 H${at(s.values[1])}" stroke="#d07629" stroke-width="3" fill="none"/>`;
        if(done>=3&&s.kind==='opposite')motion+=`<circle data-object-id="opposite-slot" cx="${at(-s.values[0])}" cy="70" r="7" fill="none" stroke="#d07629" stroke-dasharray="3 2"/>`;
        if(done>=3&&s.kind==='order')motion+=`<text data-object-id="chosen-direction" x="300" y="24" text-anchor="middle">${s.decision==='least'?'Look left for the least':'Look right for the greatest'}</text>`;
      }else{
        let current=s.start;
        motion=`<g data-object-id="given-1" transform="translate(${at(current)},70)"><circle r="7" fill="#215eaf"/><text text-anchor="middle" y="-12">Start ${esc(current)}</text></g>`;
        const count=Math.min(s.operations.length,Math.max(0,done-2));
        s.operations.slice(0,count).forEach(([sign,v],i)=>{const next=current+(sign==='+'?v:-v),y=42-(i%2)*22;
          motion+=`<g data-object-id="jump-${i+1}"><path d="M${at(current)} ${y} Q${(at(current)+at(next))/2} ${y-22} ${at(next)} ${y}" fill="none" stroke="#d07629" stroke-width="3" marker-end="url(#g8-int-arrow)"/><text x="${(at(current)+at(next))/2}" y="${y-25}" text-anchor="middle">${esc(sign)} (${esc(v)})</text><circle cx="${at(next)}" cy="70" r="5" fill="#267c74"/></g>`;
          current=next;});
        if(done>=2&&count===0)motion+=`<text data-object-id="direction" x="300" y="24" text-anchor="middle">${s.operations[0][0]==='-'?'Reverse the next signed move':'Follow the next signed move'}</text>`;
      }
      const visual=`<div class="g8-int-stage" data-object-id="model"><svg viewBox="0 0 600 126" role="img" aria-label="Signed number line from ${esc(lo)} to ${esc(hi)}; ${esc(s.problem)}"><defs><marker id="g8-int-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="#d07629"/></marker></defs><line x1="32" y1="70" x2="568" y2="70" stroke="#456482" stroke-width="2"/>${tick}${motion}</svg><p data-object-id="selected-answer">${final?`Answer: ${esc(s.answer)}. ${esc(s.memo)}`:''}</p></div>`;
      return `<section class="g8-int-board" data-managed-visibility="true" data-question-id="${esc(p.question_id)}" data-phase="${esc(phase)}"><p class="g8-original" data-object-id="problem">${esc(p.prompt)}</p>${visual}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state||'')}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Signed action</span><strong>${phase==='ready'?'':esc(state.working_state||'')}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${phase==='result'&&!final?esc(state.after_state||''):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Verify the original values</span><strong>${final?esc(state.after_state||''):''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
