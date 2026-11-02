/* Exact, question-specific group/area and measured-division models. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 const math=x=>globalThis.AthenaFractionNotation?.html(x)??esc(x);
 const speech=x=>globalThis.AthenaFractionNotation?.speech(x)??String(x);
 function value(raw){const s=String(raw).split(' '),frac=s.at(-1).split('/').map(Number),d=frac[1]||1;return {n:(s.length===2?Number(s[0])*d:0)+frac[0],d};}
 function productModel(s,stage){
  const [a,b]=s.values,[x,y]=[value(a),value(b)];
  const counterMode=y.d===1&&y.n<=27&&y.n%x.d===0;
  const height=counterMode?Math.max(195,65+Math.ceil(x.d/2)*38):195;
  let svg=`<svg viewBox="0 0 540 ${height}" role="img" aria-label="`;
  svg+=esc(`Multiplication model for ${speech(a)} of ${speech(b)}`)+'">';
  if(counterMode){
   // The whole-number quantity is a set of individual counters, not an arbitrary bar.
   const perGroup=y.n/x.d,cell=Math.min(30,205/perGroup),start=88,selected=x.n*y.n/x.d;
   svg+=`<text x="7" y="23" font-size="14">${esc(y.n)} counters</text>`;
   for(let i=0;i<y.n;i++){
    const group=Math.floor(i/perGroup),cx=start+(group%2)*225+(i%perGroup)*cell,cy=30+Math.floor(group/2)*38;
    if(stage>=2&&i%perGroup===0)svg+=`<rect x="${cx-17}" y="${cy-16}" width="${perGroup*cell+5}" height="32" rx="6" fill="none" stroke="#ae643b" stroke-width="2"/>`;
    svg+=`<circle cx="${cx}" cy="${cy}" r="13" stroke="#315374" fill="${stage>=3&&i<Math.floor(selected)?'#3787a9':'#fff'}"/>`;
    if(stage>=3&&i===Math.floor(selected)&&selected%1>0){
     const portion=selected%1,clip=`g8-counter-clip-${esc(s.id)}`;
     svg+=`<defs><clipPath id="${clip}"><circle cx="${cx}" cy="${cy}" r="12"/></clipPath></defs><path d="M ${cx-13} ${cy-13} h ${26*portion} v 26 h ${-26*portion} Z" fill="#3787a9" clip-path="url(#${clip})"/>`;
    }
   }
   if(stage>=2)svg+=`<text x="${start}" y="${height-10}" font-size="12">${x.d} equal groups of ${perGroup} counters; select ${x.n} groups</text>`;
  }else if(y.d===1 && y.n<=27){
   const segment=360/x.d;
   svg+=`<text x="8" y="23" font-size="13">Partition the collection into ${x.d} equal shares</text>`;
   svg+=`<rect x="88" y="52" width="360" height="52" rx="4" stroke="#315374" fill="#fff"/>`;
   if(stage>=2)for(let i=1;i<x.d;i++)svg+=`<line x1="${88+i*segment}" x2="${88+i*segment}" y1="52" y2="104" stroke="#315374"/>`;
   if(stage>=3)svg+=`<rect x="89" y="53" width="${x.n*segment-2}" height="50" fill="#3787a9" fill-opacity=".75"/>`;
   if(stage>=2)svg+=`<text x="88" y="139" font-size="12">Each share is ${y.n} ÷ ${x.d} counters</text>`;
  }else{
   // An area of unit squares: one operand selects columns, the other rows.
   const cols=Math.ceil(x.n/x.d)*x.d,rows=Math.ceil(y.n/y.d)*y.d,w=360/cols,h=115/rows;
   svg+=`<text x="8" y="23" font-size="13">Fraction of a fraction</text>`;
   for(let row=0;row<rows;row++)for(let col=0;col<cols;col++){
    const inX=col<x.n,inY=row<y.n;
    svg+=`<rect x="${88+col*w}" y="${32+row*h}" width="${w-1}" height="${h-1}" stroke="#315374" fill="${stage>=3&&inX&&inY?'#3787a9':stage>=2&&inY?'#9cd5e8':'#fff'}"/>`;
   }
  }
  if(stage>=4)svg+=`<text data-object-id="result-marker" x="90" y="${height-29}" font-size="14">Result shown below</text>`;
  return svg+'</svg>';
 }
 function divisionModel(s,stage){
  const [dividend,divisor]=s.values,[x,y]=[value(dividend),value(divisor)],lcd=s.common_denominator;
  const pieces=Math.round(x.n/x.d*lcd),perGroup=Math.round(y.n/y.d*lcd);
  const max=Math.max(1,Math.ceil(x.n/x.d),Math.ceil(y.n/y.d)),width=430,origin=64,step=width/(max*lcd);
  let svg=`<svg viewBox="0 0 540 180" role="img" aria-label="${esc(`How many ${speech(divisor)} groups fit in ${speech(dividend)}`)}">`;
  svg+=`<text x="6" y="20" font-size="14">Original amount and group size</text>`;
  svg+=`<line x1="${origin}" y1="75" x2="${origin+width}" y2="75" stroke="#315374" stroke-width="2"/>`;
  for(let i=0;i<=max*lcd;i++){
   const px=origin+i*step;
   if(stage>=2||i%lcd===0)svg+=`<line x1="${px}" x2="${px}" y1="69" y2="82" stroke="#315374"/>`;
   if(i%lcd===0)svg+=`<text x="${px-4}" y="99" font-size="11">${i/lcd}</text>`;
   if(stage>=3&&i<pieces)svg+=`<rect x="${px}" y="52" width="${step-1}" height="15" fill="${Math.floor(i/perGroup)%2?'#9cd5e8':'#3787a9'}"/>`;
  }
  if(stage>=1)svg+=`<rect x="${origin}" y="53" width="${pieces*step}" height="13" fill="#7dbbd5" fill-opacity=".55"/>`;
  if(stage>=2)svg+=`<path d="M ${origin} 116 v 9 H ${origin+perGroup*step} v -9" fill="none" stroke="#ae643b" stroke-width="3"/>`;
  if(stage>=2)svg+=`<text x="${origin}" y="135" font-size="13">Each small interval is one of ${lcd} equal parts</text>`;
  if(stage>=3)svg+=`<text x="${origin}" y="155" font-size="13">One group uses ${perGroup} of those intervals</text>`;
  if(stage>=4)svg+=`<text data-object-id="result-marker" x="${origin}" y="174" font-size="14">Group count shown below</text>`;
  return svg+'</svg>';
 }
 AthenaVisualizationRegistry.register('algebra','grade8_fraction_operations',{
  render(params,state,phase){
   const s=JSON.parse(params.scene_json),requested=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
   const stage=phase==='result'?requested:Math.max(0,requested-1),complete=stage===params.total_steps;
   const visual=s.kind==='multiply'?productModel(s,stage):divisionModel(s,stage);
   const rows=(s.rows||[]).slice(0,Math.max(0,Math.min(3,stage-1))).map((row,i)=>`<li data-object-id="reason-${i+1}">${math(row)}</li>`).join('');
   return `<section class="g8-fraction-board g8-fraction-operations" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${math(params.prompt)}</p><div data-object-id="model" class="g8-fraction-visual"><div class="g8-fraction-operands"><span data-object-id="fraction-1">${math(s.values[0])}</span> ${s.kind==='multiply'?'×':'÷'} <span data-object-id="fraction-2">${math(s.values[1])}</span></div>${visual}</div><ol aria-label="Worked solution so far">${rows}</ol><p data-object-id="operation">${phase==='ready'?'':math(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!complete?math(state.after_state||''):''}</p><p data-object-id="verification">${complete?`Answer: ${math(s.answer)}. ${math(s.memo)}`:''}</p></section>`;
  },destroy(){}
 });
})();
