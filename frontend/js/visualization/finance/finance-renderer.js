(function registerFinanceTimeline(){
  const esc=value=>escapeWhiteboardHtml(String(value));
  AthenaVisualizationRegistry.register("finance","cashflow_timeline",{
    render(parameters,state,phase){
      const periods=Number(parameters.periods),focal=Number(parameters.focal_period),labels=Array.isArray(parameters.cashflows)?parameters.cashflows:[];
      const shown=new Set(state.objects||[]),highlights=new Set(state.highlights||[]),annotations=new Set(state.annotations||[]);
      const left=72,right=650,y=190,ticks=Math.min(periods,12),x=i=>left+(right-left)*(i/ticks);
      const tickMarkup=shown.has("periods")?Array.from({length:ticks+1},(_,i)=>`<g class="finance-tick"><line x1="${x(i)}" y1="178" x2="${x(i)}" y2="202"/><text x="${x(i)}" y="224">${i===ticks?periods:Math.round(periods*i/ticks)}</text></g>`).join(""):"";
      const visibleLabels=phase==="ready"?labels.slice(0,1):labels;
      const flows=shown.has("cashflows")?visibleLabels.map((label,index)=>{const px=labels.length===1?left:left+(right-left)*(index/(labels.length-1)),out=/withdraw|payment|loss/i.test(label),end=out?258:105;return `<g class="finance-cashflow ${highlights.has("date-zero")&&index===0?"is-highlighted":""}"><line x1="${px}" y1="${y}" x2="${px}" y2="${end}"/><path d="M${px-6} ${end+(out?-10:10)} L${px} ${end} L${px+6} ${end+(out?-10:10)}"/><text x="${px}" y="${out?280:88}">${esc(label)}</text></g>`;}).join(""):"";
      const focalMarkup=shown.has("timeline")?`<g class="finance-focal ${highlights.has("focal-date")?"is-highlighted":""}"><line x1="${right}" y1="55" x2="${right}" y2="290"/><text x="${right}" y="42">Focal date: ${focal}</text></g>`:"";
      const rate=shown.has("rate")?`<g class="finance-rate ${highlights.has("rate")?"is-highlighted":""}"><rect x="210" y="20" width="300" height="48" rx="8"/><text x="360" y="50">i=${esc(parameters.periodic_rate)} per ${esc(parameters.period_label||"period")} · n=${periods}</text></g>`:"";
      const movement=shown.has("movement")?`<path class="finance-movement" d="M120 145 C280 95 480 95 620 145"/><text class="finance-movement-label" x="370" y="108">${annotations.has("forward")?"accumulate →":"← discount"}</text>`:"";
      const result=phase==="result"&&shown.has("result")?`<g class="finance-result ${annotations.has("verified")?"is-verified":""}"><rect x="175" y="306" width="370" height="62" rx="10"/><text x="360" y="333">${esc(parameters.formula||"")}</text><text x="360" y="357">${esc(parameters.result||"")}${annotations.has("verified")?" ✓":""}</text></g>`:"";
      return `<figure class="finance-visual ${esc(phase)}"><svg viewBox="0 0 720 390" role="img" aria-labelledby="finance-title finance-desc"><title id="finance-title">${esc(parameters.title||"Cash-flow timeline")}</title><desc id="finance-desc">Cash-flow timeline from date zero to period ${periods}, focal period ${focal}, periodic rate ${esc(parameters.periodic_rate)}. ${esc(visibleLabels.join("; "))}</desc><line class="finance-axis" x1="${left}" y1="${y}" x2="${right}" y2="${y}"/>${tickMarkup}${flows}${focalMarkup}${rate}${movement}${result}</svg><figcaption>${esc(parameters.model||"Financial timeline")}</figcaption></figure>`;
    },destroy(){}
  });
})();
