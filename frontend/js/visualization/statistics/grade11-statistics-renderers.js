/* Grade 11 Statistics: values, scales and cumulative graphical marks belong to the question. */
(() => {
  const esc=x=>escapeWhiteboardHtml(String(x??''));
  const f=x=>Number(x).toFixed(1);
  const stage=(state,phase)=>{
    const mark=(state.annotations||[]).find(a=>/^stage:\d+$/.test(a));
    const n=Number(mark?.slice(6)||0);
    return phase==='result'?n:Math.max(0,n-1);
  };
  const line=(x1,y1,x2,y2,klass='guide')=>`<line x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}" class="g11-stat-${klass}"/>`;
  const text=(x,y,label,klass='label')=>`<text x="${f(x)}" y="${f(y)}" class="g11-stat-${klass}">${esc(label)}</text>`;
  const dot=(x,y,klass='point')=>`<circle cx="${f(x)}" cy="${f(y)}" r="5" class="g11-stat-${klass}"/>`;
  const axis=(x0=55,y0=258,x1=530,y1=35)=>line(x0,y0,x1,y0,'axis')+line(x0,y0,x0,y1,'axis');
  const scale=(a,b,lo,hi)=>x=>a+(x-lo)*(b-a)/(hi-lo||1);
  function plot(scene,s){
    const v=scene.visual.values,mode=v.mode;
    if(mode==='ungrouped'||mode==='deviation'||mode==='box'||mode==='outlier'){
      const xs=v.data,min=Math.min(...xs),max=Math.max(...xs),sx=scale(65,515,min-2,max+2);
      let out=axis();
      for(const value of [...new Set(xs)]){
        const occurrences=xs.filter(x=>x===value).length;
        out+=text(sx(value)-7,277,value);
        for(let j=0;j<occurrences;j++)out+=dot(sx(value),245-14*j);
      }
      if(mode==='ungrouped'){
        if(s>=1)out+=text(68,55,`n = ${xs.length}`,'note');
        if(s>=2)out+=text(68,81,`Σx = ${v.sum??xs.reduce((a,b)=>a+b,0)}`,'note');
        if(s>=3)out+=text(68,108,`Mean = Σx / ${xs.length}`,'note');
        if(s>=4)out+=text(68,135,`Mean ≈ ${f(xs.reduce((a,b)=>a+b,0)/xs.length)}`,'note');
        if(s>=5)out+=line(sx(v.mean),140,sx(v.mean),256,'answer')+text(sx(v.mean)+6,145,`Mean = ${v.mean.toFixed(2)}`,'answer-label');
      }else if(mode==='deviation'){
        const mean=v.mean??xs.reduce((a,b)=>a+b,0)/xs.length;
        if(s>=1)out+=text(70,48,`N = ${xs.length}`,'note');
        if(s>=2)out+=line(sx(mean),115,sx(mean),255,'highlight')+text(70,72,`x̄ = ${f(mean)}`,'note');
        if(s>=3)xs.forEach((x,j)=>out+=line(sx(mean),170-j*12,sx(x),170-j*12,'deviation'));
        if(s>=4)out+=text(70,107,'σ² = Σ(x − x̄)² / N','note');
        if(s>=5)out+=text(70,135,`σ = ${(v.sd??Math.sqrt(xs.reduce((a,x)=>a+(x-mean)**2,0)/xs.length)).toFixed(2)}`,'answer-label');
      }else{
        const five=v.five??(()=>{
          const a=[...xs].sort((a,b)=>a-b),h=a.length>>1;return [a[0],(a[1]+a[2])/2,a[h],(a[h+2]+a[h+3])/2,a.at(-1)];
        })();
        if(s>=1)out+=text(65,52,`Ordered observations: ${xs.length}`,'note');
        if(s>=2)out+=line(sx(five[2]),135,sx(five[2]),256,'highlight')+text(sx(five[2])+4,130,`median ${five[2]}`,'note');
        if(s>=3)out+=line(sx(five[1]),180,sx(five[1]),256,'highlight')+line(sx(five[3]),180,sx(five[3]),256,'highlight')+text(65,80,`Q1 = ${five[1]}, Q3 = ${five[3]}`,'note');
        if(s>=4 || mode==='outlier'&&s>=3){
          out+=`<rect x="${f(sx(five[1]))}" y="175" width="${f(sx(five[3])-sx(five[1]))}" height="38" class="g11-stat-box"/>`;
          out+=line(sx(five[0]),194,sx(five[1]),194,'whisker')+line(sx(five[3]),194,sx(five[4]),194,'whisker');
        }
        if(mode==='outlier'&&s>=3){
          const iqr=five[3]-five[1],fence=five[3]+1.5*iqr;
          out+=line(sx(fence),130,sx(fence),255,'fence')+text(65,112,`Upper fence = ${fence}`,'note');
          if(s>=4)out+=dot(sx(max),245,'outlier');
        }
        if(s>=5)out+=text(65,52,mode==='outlier'?`Upper outlier ${max}; right-skewed`:`IQR = ${five[3]-five[1]}`,'answer-label');
      }
      return out;
    }
    if(mode==='grouped'||mode==='histogram'||mode==='ogive'){
      const start=v.start,width=v.width,freq=v.frequencies,top=Math.max(...freq);
      const sy=scale(250,68,0,Math.max(mode==='ogive'?freq.reduce((a,b)=>a+b,0):top,1)*1.2),sx=scale(65,515,start,start+5*width);
      let out=axis();
      freq.forEach((count,j)=>{
        const left=sx(start+j*width),right=sx(start+(j+1)*width),mid=(left+right)/2;
        out+=text(left-4,278,start+j*width);
        out+=text(mid-6,62,count,'given');
        if(mode==='histogram'&&s>=2){
          out+=`<rect x="${f(left)}" y="${f(sy(count))}" width="${f(right-left)}" height="${f(258-sy(count))}" class="g11-stat-bar"/>`;
          out+=text(mid-6,sy(count)-7,count,'bar-label');
        }
      });
      out+=text(495,278,start+5*width);
      if(mode==='grouped'){
        if(s>=1)out+=text(72,110,`Σf = ${freq.reduce((a,b)=>a+b,0)}`,'note');
        if(s>=2)freq.forEach((_,j)=>out+=text(sx(start+(j+.5)*width)-12,183,start+(j+.5)*width,'midpoint'));
        if(s>=3)out+=text(72,140,`Σ(fm) = ${freq.reduce((sum,count,j)=>sum+count*(start+(j+.5)*width),0)}`,'note');
        if(s>=4)out+=text(72,165,'Estimated mean = Σ(fm) / Σf','note');
        if(s>=5)out+=text(72,210,`Estimated mean = ${v.mean.toFixed(2)}`,'answer-label');
      }else if(mode==='histogram'){
        if(s>=3)freq.forEach((count,j)=>out+=dot(sx(start+(j+.5)*width),sy(count),'midpoint-dot'));
        if(s>=4){const points=freq.map((count,j)=>`${f(sx(start+(j+.5)*width))},${f(sy(count))}`).join(' ');
          out+=`<polyline points="${points}" class="g11-stat-poly"/>`;}
        if(s>=4)out+=text(70,47,'The highest bar gives the modal class.','note');
        if(s>=5){const peak=v.peak??freq.indexOf(Math.max(...freq));out+=text(70,33,`Modal interval: ${start+peak*width}≤x<${start+(peak+1)*width}`,'answer-label');}
      }else{
        const cum=[0];for(const count of freq)cum.push(cum.at(-1)+count);
        const cumulativeScale=scale(250,60,0,cum.at(-1));
        const shown=s<2?Math.min(s+1,2):6;
        for(let j=0;j<shown;j++){
          const pointX=sx(start+j*width),pointY=cumulativeScale(cum[j]);out+=dot(pointX,pointY,'cumulative');
          if(j)out+=line(sx(start+(j-1)*width),cumulativeScale(cum[j-1]),pointX,pointY,'ogive');
          if(s>=2)out+=text(pointX-10,pointY-9,cum[j],'small');
        }
        if(s>=4){const N=cum.at(-1),target=(N+1)/2,medianClass=cum.findIndex((x,j)=>j<5&&x<target&&target<=cum[j+1]);
          out+=line(55,cumulativeScale(target),515,cumulativeScale(target),'fence');
          out+=text(72,cumulativeScale(target)-7,`Median position ≈ ${f(target)}`,'note');
          if(s>=5)out+=text(72,40,`Median class ${start+medianClass*width}≤x<${start+(medianClass+1)*width}`,'answer-label');
        }
      }
      return out;
    }
    const xs=v.x,ys=v.y,sy=scale(250,50,0,Math.max(...ys)*1.15),sx=scale(65,515,1,6);
    let out=axis();
    xs.forEach((x,j)=>{out+=text(sx(x)-5,277,x);if(s>=1&&j<(s===1?2:6))out+=dot(sx(x),sy(ys[j]));});
    if(s>=4){
      const model=v.model??(()=>{const d=ys.slice(1).map((y,j)=>y-ys[j]);if(d.every(x=>x===d[0]))return'linear';
        const second=d.slice(1).map((x,j)=>x-d[j]);return second.every(x=>x===second[0])?'quadratic':'exponential';})();
      const d0=ys[1]-ys[0],d1=ys[2]-ys[1];
      const curve=model==='linear'?x=>ys[0]+d0*(x-1):
        model==='quadratic'?x=>x*x+(d0-3)*x+(ys[0]-d0+2):
        x=>{const growth=d1/d0;return growth**x+(ys[0]-growth)};
      const path=Array.from({length:101},(_,j)=>{const x=1+j/20;
        return `${j?'L':'M'} ${f(sx(x))} ${f(sy(curve(x)))}`;}).join(' ');
      out+=`<path d="${path}" class="g11-stat-poly"/>`;
      if(s>=5)out+=text(70,39,`Model = ${model}`,'answer-label');
    }
    return out;
  }
  function render(parameters,state,phase,n){
    const scene=JSON.parse(parameters.scene_json);
    if(scene.id!==parameters.question_id||scene.problem!==parameters.prompt||scene.lesson!==n||scene.visual?.family!=='grade11_statistics')throw Error('Statistics plot belongs to another question');
    const s=stage(state,phase);
    return `<section class="g11-stat-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}">
      <p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-stat-model"><svg viewBox="0 0 560 305" role="img" aria-label="${esc(scene.problem)}"><title>Question-specific statistics construction, step ${s} of 5</title>${plot(scene,s)}</svg></div>
      <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
      <p data-object-id="result">${phase==='result'&&s<5?esc(state.after_state):''}</p>
      <p data-object-id="verification">${phase==='result'&&s===5?esc(state.after_state):''}</p>
    </section>`;
  }
  for(let n=1;n<=7;n++)AthenaVisualizationRegistry.register('statistics',`grade11_stat_${n}`,
    {render:(p,state,phase)=>render(p,state,phase,n),destroy(){}});
})();
