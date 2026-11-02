/* Fractions are actual portions of the same sized unit, repartitioned by question LCD. */
(() => {
 const esc=x=>escapeWhiteboardHtml(String(x??''));
 // Keep the curriculum source and answer checker as plain text. Only the lesson
 // display changes, and all non-mathematical text remains HTML escaped.
 const notation={
  html(raw){
   const source=String(raw??'');
   const token=/(?<![\d/])(?:(\d+)\s+)?(\d+)\/(\d+)(?![\d/])/g;
   let output='',end=0,match;
   while((match=token.exec(source))){
    output+=esc(source.slice(end,match.index));
    const [,whole,numerator,denominator]=match;
    if(Number(denominator)===0){output+=esc(match[0]);end=token.lastIndex;continue;}
    const speech=`${whole?whole+' and ':''}${numerator} over ${denominator}`;
    output+=`<math class="g8-fraction-math" aria-label="${speech}"><mrow>${whole?`<mn>${whole}</mn><mspace width="0.2em"/>`:''}<mfrac><mn>${numerator}</mn><mn>${denominator}</mn></mfrac></mrow></math>`;
    end=token.lastIndex;
   }
   return output+esc(source.slice(end));
  },
  speech(raw){return String(raw??'').replace(/(\d+\s+)?(\d+)\/(\d+)/g,(_,whole,n,d)=>`${whole?whole.trim()+' and ':''}${n} over ${d}`);}
 };
 globalThis.AthenaFractionNotation=notation;
 function svgFraction(raw,x,y,id=''){
  const mixed=/^(?:(\d+)\s+)?(\d+)\/(\d+)$/.exec(String(raw));
  if(!mixed)return `<text x="${x}" y="${y+20}" font-size="13">${esc(raw)}</text>`;
  const [,whole,n,d]=mixed,fx=x+(whole?17:0);
  return `<g ${id?`data-object-id="${esc(id)}"`:''} aria-label="${esc(notation.speech(raw))}">${whole?`<text x="${x}" y="${y+21}" font-size="14">${whole}</text>`:''}<text x="${fx+11}" y="${y+10}" font-size="13" text-anchor="middle">${n}</text><line x1="${fx+1}" x2="${fx+21}" y1="${y+15}" y2="${y+15}" stroke="currentColor" stroke-width="1.5"/><text x="${fx+11}" y="${y+29}" font-size="13" text-anchor="middle">${d}</text></g>`;
 }
 function value(raw){const parts=String(raw).split(' ');if(parts.length===2){const [n,d]=parts[1].split('/').map(Number);return {n:Number(parts[0])*d+n,d};}const [n,d=1]=parts[0].split('/').map(Number);return {n,d};}
 AthenaVisualizationRegistry.register('algebra','grade8_fraction_strips',{
  render(params,state,phase){
   const s=JSON.parse(params.scene_json),stage=Number(((state.annotations||[]).find(x=>x.startsWith('stage:'))||'stage:0').slice(6));
   const done=phase==='result'?stage:Math.max(0,stage-1),complete=done===params.total_steps;
   const numbers=s.values.map(value),unit=110,maxWhole=Math.max(1,...numbers.map(v=>Math.ceil(v.n/v.d)));
   const width=80+maxWhole*unit+10,height=36+numbers.length*72;
   let svg=`<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Fraction strips for ${esc(s.values.map(notation.speech).join(', '))}">`;
   numbers.forEach((v,i)=>{
    const y=25+i*72,segments=Math.ceil(v.n/v.d),parts=done>=2?s.common_denominator:v.d;
    svg+=`<g data-object-id="fraction-${i+1}">${svgFraction(s.values[i],8,y)}`;
    for(let whole=0;whole<segments;whole++){
      const x=70+whole*unit;
      svg+=`<rect x="${x}" y="${y}" width="${unit}" height="29" rx="4" fill="#fff" stroke="#294e73"/>`;
      const fraction=Math.max(0,Math.min(1,v.n/v.d-whole));
      for(let part=0;part<parts;part++){
       if((part+.5)/parts<fraction)svg+=`<rect x="${x+part*unit/parts+1}" y="${y+1}" width="${Math.max(0,unit/parts-2)}" height="27" fill="#77bad8"/>`;
       if(part>0)svg+=`<line x1="${x+part*unit/parts}" x2="${x+part*unit/parts}" y1="${y}" y2="${y+29}" stroke="#294e73"/>`;
      }
    }
    if(done>=2)svg+=`<g data-object-id="equal-parts-${i+1}">${svgFraction(`${Math.round(v.n/v.d*s.common_denominator)}/${s.common_denominator}`,72,y+31)}<text x="102" y="${y+51}" font-size="12">equal parts</text></g>`;
    svg+='</g>';
   });svg+='</svg>';
   const rows=(s.rows||[]).slice(0,Math.max(0,Math.min(3,done-1))).map((row,i)=>`<li data-object-id="reason-${i+1}">${notation.html(row)}</li>`).join('');
   return `<section class="g8-fraction-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem">${notation.html(params.prompt)}</p><div data-object-id="model" class="g8-fraction-visual">${svg}</div><ol aria-label="Worked solution so far">${rows}</ol><p data-object-id="operation">${phase==='ready'?'':notation.html(state.working_state||'')}</p><p data-object-id="result">${phase==='result'&&!complete?notation.html(state.after_state||''):''}</p><p data-object-id="verification">${complete?`Answer: ${notation.html(s.answer)}. ${notation.html(s.memo)}`:''}</p></section>`;
  },destroy(){}
 });
})();
