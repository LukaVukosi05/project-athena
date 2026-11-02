/* A 100-unit scale and original/new bars for authored percentage questions. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 const math=x=>globalThis.AthenaFractionNotation?.html(x)??esc(x);
 function grid(s,stage){
  const kind=s.kind,change=['increase','decrease','change'].includes(kind);
  const values=s.values.map(raw=>String(raw).includes('/')?Number(String(raw).split('/')[0])/Number(String(raw).split('/')[1]):Number(raw)),original=change?values[1]:kind==='of'?values[1]:kind==='part'?values[1]:1;
  const percentage=kind==='convert'?values[0]*100:kind==='of'?values[0]:kind==='part'?values[0]/values[1]*100:kind==='change'?Math.abs(values[0]-values[1])/values[1]*100:values[0];
  const fill=Math.max(0,Math.min(100,percentage));
  let svg=`<svg viewBox="0 0 500 170" role="img" aria-label="${esc(change?'Original and changed amounts':'One hundred equal percentage units')}"><text x="10" y="18" font-size="13">${esc(change?'Original amount is the 100% reference':'The whole represents 100%')}</text>`;
  if(change){
   const next=kind==='change'?values[0]:kind==='increase'?original*(1+percentage/100):original*(1-percentage/100);
   const scale=420/Math.max(original,next);
   svg+=`<text x="10" y="54" font-size="12">Original ${esc(original)}</text><rect x="88" y="35" width="${original*scale}" height="24" fill="#8ebfd5"/>`;
   if(stage>=2)svg+=`<text x="10" y="102" font-size="12">New</text><rect x="88" y="78" width="${stage>=3?next*scale:original*scale}" height="24" fill="#3288aa"/>`;
   if(stage>=3)svg+=`<path d="M ${88+original*scale} 112 V 130 H ${88+next*scale}" fill="none" stroke="#a45519" stroke-width="3"/><text x="90" y="151" font-size="12">Change measured against original ${esc(original)}</text>`;
  }else{
   const cell=19,gap=2;
   for(let i=0;i<100;i++){const x=10+(i%20)*(cell+gap),y=32+Math.floor(i/20)*(cell+gap);
    const opacity=stage>=2?Math.max(0,Math.min(1,fill-i)):0;
    svg+=`<rect x="${x}" y="${y}" width="${cell}" height="${cell}" fill="${opacity?'#3288aa':'#edf6fa'}" fill-opacity="${opacity||1}" stroke="#315374" stroke-width=".4"/>`;
   }
   if(stage>=2&&percentage>100){svg+=`<rect x="10" y="142" width="420" height="10" fill="#e8f4f9" stroke="#315374"/><rect x="10" y="142" width="${420*(percentage%100)/100}" height="10" fill="#3288aa"/><text x="10" y="167" font-size="11">${esc(Math.floor(percentage/100))} complete hundred(s), then ${esc(percentage%100)}% of another</text>`;}
   else svg+=`<text x="10" y="151" font-size="12">${stage>=2?esc(percentage)+' out of 100 parts':'100 equal parts'}</text>`;
  }
  return svg+'</svg>';
 }
 AthenaVisualizationRegistry.register('algebra','grade8_percentage_grid',{
  render(params,state,phase){
   const s=JSON.parse(params.scene_json),requested=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
   const stage=phase==='result'?requested:Math.max(0,requested-1),complete=stage===params.total_steps;
   const rows=(s.rows||[]).slice(0,Math.max(0,Math.min(3,stage-1))).map((row,i)=>`<li data-object-id="reason-${i+1}">${math(row)}</li>`).join('');
   return `<section class="g8-fraction-board g8-percentage-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${math(params.prompt)}</p><div data-object-id="model" class="g8-fraction-visual">${grid(s,stage)}</div><ol aria-label="Worked solution so far">${rows}</ol><p data-object-id="operation">${phase==='ready'?'':math(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!complete?math(state.after_state||''):''}</p><p data-object-id="verification">${complete?`Answer: ${math(s.answer)}. ${math(s.memo)}`:''}</p></section>`;
  },destroy(){}
 });
})();
