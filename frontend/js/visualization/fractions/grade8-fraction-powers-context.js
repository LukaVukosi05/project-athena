/* Question-specific fraction powers, inverse roots and measurement contexts. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 const math=x=>globalThis.AthenaFractionNotation?.html(x)??esc(x);
 function value(raw){const pieces=String(raw).split(' '),terms=pieces.at(-1).split('/').map(Number),d=terms[1]||1;return {n:(pieces.length===2?Number(pieces[0])*d:0)+terms[0],d};}
 function powScene(s,stage){
  const v=value(s.values[0]),k=s.exponent,root=s.kind==='root';
  // Perfect roots in the authored set have exact integer numerator/denominator sides.
  const dimension=root?Math.round(Math.pow(v.d,1/k)):v.d;
  const shaded=root?Math.round(Math.pow(v.n,1/k)):v.n;
  const span=Math.max(dimension,shaded),layers=k===3?span:1;
  const cell=k===3?Math.min(20,78/span):Math.min(24,260/span);
  const width=k===3?Math.max(440,layers*(span*cell+12)+38):440,height=k===3?170:Math.max(160,span*cell+61);
  let svg=`<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(root?'Build equal square or cube layers to find the positive root':'Build a square or cube of fraction sides')}">`;
  svg+=`<text x="12" y="21" font-size="14">${root?'Find a positive side length from the area or volume':'Repeat the same fraction as every side'}</text>`;
  if(stage>=1)for(let z=0;z<layers;z++){
   const left=24+z*(span*cell+12),top=39;
   if(k===3)svg+=`<text x="${left}" y="${height-12}" font-size="11">Layer ${z+1}</text>`;
   for(let row=0;row<span;row++)for(let col=0;col<span;col++){
    const selected=col<shaded&&row<shaded&&(k===2||z<shaded);
    svg+=`<rect x="${left+col*cell}" y="${top+row*cell}" width="${cell-1}" height="${cell-1}" stroke="#315374" fill="${stage>=3&&selected?'#3787a9':stage>=2?'#e8f5fb':'#fff'}"/>`;
   }
  }
  if(stage>=2)svg+=`<text x="12" y="${height-31}" font-size="12">${k} equal dimensions: numerator and denominator both change</text>`;
  if(stage>=4)svg+=`<text data-object-id="result-marker" x="12" y="${height-4}" font-size="13">Simplified exact result appears below</text>`;
  return svg+'</svg>';
 }
 function contextScene(s,stage){
  const [a,b]=s.values,[x,y]=[value(a),value(b)],answer=stage>=3&&s.answer?value(s.answer):null;
  const [left,right]=[x.n/x.d,y.n/y.d];
  const max=Math.max(1,Math.ceil(left),Math.ceil(right),s.operation==='multiply'?Math.ceil(left*right):s.operation==='add'?Math.ceil(left+right):0);
  const scale=n=>Math.min(420,420*n/max),lcd=Math.min(24,Math.max(x.d,y.d));
  let svg=`<svg viewBox="0 0 520 205" role="img" aria-label="${esc(`Fraction context in ${s.unit}, showing ${a} and ${b}`)}">`;
  svg+=`<text x="14" y="23" font-size="14">Original unit: ${esc(s.unit)}</text>`;
  const captions={multiply:['Fraction','Whole amount'],divide:['Original amount','Group size'],subtract:['Starting amount','Amount used'],add:['First amount','Second amount']}[s.operation];
  [[a,x,51],[b,y,104]].forEach(([label,v,top],i)=>{
   svg+=`<text x="14" y="${top+18}" font-size="12">${captions[i]}</text>`;
   svg+=`<rect x="88" y="${top}" width="420" height="28" fill="#fff" stroke="#315374" rx="4"/>`;
   if(stage>=1)svg+=`<rect x="89" y="${top+1}" width="${Math.max(0,scale(v.n/v.d)-2)}" height="26" fill="${i?'#b6dbe9':'#6aaac7'}"/>`;
   if(stage>=2)for(let tick=1;tick<max*lcd;tick++){
    const pos=88+420*tick/(max*lcd);svg+=`<line x1="${pos}" y1="${top}" x2="${pos}" y2="${top+28}" stroke="#315374" stroke-opacity=".38"/>`;
   }
  });
  if(stage>=3){
   if(s.operation==='divide'){
    const count=answer.n/answer.d,boxes=Math.min(20,Math.ceil(count));
    for(let i=0;i<boxes;i++){
     const bx=88+i*420/boxes,bw=Math.max(3,420/boxes-3),fraction=Math.max(0,Math.min(1,count-i));
     svg+=`<rect x="${bx}" y="157" width="${bw}" height="18" rx="3" fill="#e9f5fa" stroke="#315374"/>`;
     if(fraction)svg+=`<rect x="${bx+1}" y="158" width="${Math.max(0,(bw-2)*fraction)}" height="16" fill="#3787a9"/>`;
    }
   }else svg+=`<rect x="88" y="157" width="${Math.max(0,scale(answer.n/answer.d))}" height="18" fill="#3787a9"/>`;
   svg+=`<text x="90" y="195" font-size="13">Result in ${esc(s.answer_unit||s.unit)} shown below</text>`;
  }
  svg+='</svg>';return svg;
 }
 AthenaVisualizationRegistry.register('algebra','grade8_fraction_powers_context',{
  render(params,state,phase){
   const s=JSON.parse(params.scene_json),requested=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
   const stage=phase==='result'?requested:Math.max(0,requested-1),complete=stage===params.total_steps;
   const visual=s.kind==='context'?contextScene(s,stage):powScene(s,stage);
   const rows=(s.rows||[]).slice(0,Math.max(0,Math.min(3,stage-1))).map((row,i)=>`<li data-object-id="reason-${i+1}">${math(row)}</li>`).join('');
   const operands=s.values.map((v,i)=>`<span data-object-id="fraction-${i+1}">${math(v)}</span>`).join(s.kind==='context'?' · ':' ');
   return `<section class="g8-fraction-board g8-fraction-operations" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${math(params.prompt)}</p><div data-object-id="model" class="g8-fraction-visual"><div class="g8-fraction-operands">${operands}</div>${visual}</div><ol aria-label="Worked solution so far">${rows}</ol><p data-object-id="operation">${phase==='ready'?'':math(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!complete?math(state.after_state||''):''}</p><p data-object-id="verification">${complete?`Answer: ${math(s.answer)}. ${math(s.memo)}`:''}</p></section>`;
  },destroy(){}
 });
})();
