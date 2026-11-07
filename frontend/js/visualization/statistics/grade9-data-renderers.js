/* Native Grade 9 data models: question values own every tally, axis and point. */
(() => {
  const esc=x=>escapeWhiteboardHtml(String(x??''));
  const t=(id,x,y,s)=>`<text data-object-id="${id}" x="${x}" y="${y}">${esc(s)}</text>`;
  const line=(x1,y1,x2,y2,cls='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${cls}"/>`;
  const bar=(x,y,w,h,cls='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" class="${cls}"/>`;
  const phaseStage=(state,phase)=>{
    const match=(state.annotations||[]).find(x=>/^stage:\d+$/.test(x));
    const n=match?Number(match.slice(6)):0;
    return phase==='result'?n:Math.max(0,n-1);
  };
  function axes(xLabel,yLabel,baseline=0){return line(56,238,450,238,'g9-data-axis')+line(56,238,56,24,'g9-data-axis')+t('axis-x',316,268,xLabel)+t('axis-y',4,19,yLabel)+t('zero',35,242,String(baseline))}
  function draw(scene,done){
    const v=scene.visual?.values;if(!v)return '<svg viewBox="0 0 500 290" aria-label="Dataset pending"></svg>';
    const n=scene.lesson;let picture='',note='';
    if(n===1){
      const count=30;picture=t('population',54,35,`Population: ${v.population} learners`);
      picture+=Array.from({length:count},(_,i)=>`<circle cx="${75+(i%10)*38}" cy="${70+Math.floor(i/10)*45}" r="8" class="${i<Math.ceil(count*v.sample/v.population)&&done>=3?'g9-data-selected':'g9-data-person'}"/>`).join('');
      picture+=t('sample',54,246,done>=3?`Sample: ${v.sample} learners asked`:'Each dot represents part of the population');
      if(done>=4)note=t('inference',54,272,'A sample is not the full population.');
    }else if(n===2){
      const total=v.young+v.old;
      picture=axes('learners','count')+bar(95,238-150*v.young/total,145,150*v.young/total,'g9-data-a')+bar(240,238-150*v.old/total,145,150*v.old/total,'g9-data-b');
      picture+=t('young',95,225,`Junior ${v.young}`)+t('old',240,225,`Senior ${v.old}`);
      if(done>=3)picture+=t('ratio',105,55,'Population ratio 3:1');
      if(done>=4)note=t('sampling',60,272,'Fair: 9 junior + 3 senior; all juniors excludes seniors.');
    }else if(n===3||n===6){
      const counts=v.counts,max=Math.max(...counts),labs=n===3?v.categories:v.intervals;
      picture=axes(n===3?'score':'minutes','frequency');
      for(let i=0;i<3;i++){
        const x=95+i*(n===6?98:118),width=n===6?98:75,h=160*counts[i]/max;
        picture+=bar(x,238-(done>=2?h:0),width,done>=2?h:1,`g9-data-bar ${n===6?'g9-data-touching':''}`)+t(`category-${i}`,x+5,256,labs[i]);
        if(done>=2)picture+=t(`count-${i}`,x+26,232-h,String(counts[i]));
      }
      if(done>=4)note=t('summary',60,281,n===3?`Total ${v.total??v.counts.reduce((a,b)=>a+b,0)}; mode 2`:`Total ${v.total??v.counts.reduce((a,b)=>a+b,0)}; modal interval 10–19 min`);
    }else if(n===4){
      const xs=v.values,lo=xs[0],hi=xs.at(-1);picture=axes('ordered counts','frequency');
      xs.forEach((value,i)=>{
        const x=75+350*(value-lo)/(hi-lo);picture+=`<circle data-object-id="point-${i}" cx="${x}" cy="${175-(i===0||i===6?0:8)}" r="6" class="g9-data-point"/>`;
        if(done>=2)picture+=t(`value-${i}`,x-8,196,String(value));
      });
      if(done>=3)picture+=line(75+350*(xs[3]-lo)/(hi-lo),125,75+350*(xs[3]-lo)/(hi-lo),215,'g9-data-median');
      if(done>=4)note=t('summary',60,281,`Mean ${v.mean_rounded??(xs.reduce((a,b)=>a+b,0)/7).toFixed(2)}; median ${xs[3]}; range ${hi-lo}`);
    }else if(n===5){
      const a=v.series_a,b=v.series_b,all=[...a,...b],max=Math.max(...all)+4;
      picture=axes('week 1          week 2','members');
      for(let i=0;i<2;i++)for(const [j,series,cls] of [[0,a,'g9-data-a'],[1,b,'g9-data-b']]){
        const x=117+i*170+j*49,h=165*series[i]/max;
        picture+=bar(x,238-(done>=i+1?h:0),42,done>=i+1?h:1,cls);
        if(done>=i+1)picture+=t(`bar-${i}-${j}`,x+5,229-h,String(series[i]));
      }
      if(done>=4){
        picture+=`<polyline points="138,${238-165*a[0]/max} 308,${238-165*a[1]/max}" class="g9-data-line"/>`;
        note=t('summary',60,280,`A gains ${a[1]-a[0]}; B gains ${b[1]-b[0]}; A gains ${(a[1]-a[0])-(b[1]-b[0])} more.`)
      }
    }else if(n===7&&v.model==='pie'){
      const counts=v.counts,total=counts.reduce((a,b)=>a+b,0);picture=t('legend',25,34,`Walk ${counts[0]} · Bus ${counts[1]} · Car ${counts[2]}`);
      let rotation=-90;
      const colors=['#17808c','#b97636','#556cbe'];
      for(let i=0;i<3;i++){
        const angle=360*counts[i]/total,visible=done>=i+2;
        if(visible){const rad1=rotation*Math.PI/180,rad2=(rotation+angle)*Math.PI/180;
          const d=`M 250 148 L ${250+93*Math.cos(rad1)} ${148+93*Math.sin(rad1)} A 93 93 0 ${angle>180?1:0} 1 ${250+93*Math.cos(rad2)} ${148+93*Math.sin(rad2)} Z`;
          picture+=`<path data-object-id="sector-${i}" d="${d}" fill="${colors[i]}" stroke="white" stroke-width="2"/>`;
        }rotation+=angle;
      }
      if(done<2)picture+='<circle cx="250" cy="148" r="93" fill="none" stroke="#17808c" stroke-width="2"/>';
      if(done>=4)note=t('angle',40,280,`Walk: ${counts[0]}/${total} × 360° = ${(360*counts[0]/total).toFixed(1)}°`);
    }else if(n===7&&v.model==='scatter'){
      const points=v.points;picture=axes('study hours','score');const top=points.at(-1)[1]+8;
      points.forEach(([x,y],i)=>{
        if(done>=2)picture+=`<circle data-object-id="point-${i}" cx="${64+x*55}" cy="${238-y*180/top}" r="6" class="g9-data-point"/>`;
      });
      if(done>=4)picture+=`<polyline points="${points.map(([x,y])=>`${64+x*55},${238-y*180/top}`).join(' ')}" class="g9-data-line"/>`;
      if(done>=5)note=t('prediction',60,280,`Positive association; at 6 h predict ${points.at(-1)[1]+2}.`);
    }else if(n===8){
      const base=v.truncated_baseline;
      picture=axes('group 1        group 2','responses',done>=3?base:0);
      for(const [i,value] of [v.first,v.second].entries()){
        const h=done>=3?(value-base)*10:Math.round(value*175/v.second);
        picture+=bar(128+i*170,238-h,72,h,`g9-data-bar ${done>=3?'g9-data-truncated':''}`)+t(`value-${i}`,135+i*170,227-h,String(value));
      }
      if(done>=2)picture+=t('axis-warning',61,52,`Published baseline: ${base}, not zero`);
      if(done>=4)note=t('report',60,280,`True change: 6 (${v.percent??(600/v.first).toFixed(2)}%). Truncated axis exaggerates it.`);
    }
    return `<svg viewBox="0 0 500 300" role="img" aria-label="${esc(scene.problem)}; ${done>=4?'conclusion visible':'conclusion concealed'}"><title>${esc(v.model)} from this question's data</title>${picture}${note}</svg>`;
  }
  function focus(scene,done){
    if(done<1)return '';
    const v=scene.visual.values;let labels;
    switch(scene.lesson){
      case 1:labels=['Travel investigation',`Population ${v.population}`,`Sample ${v.sample}`,'Sample ≠ population',`${v.sample} < ${v.population}`];break;
      case 2:labels=['Source: school register','Group ratio 3:1','12 ÷ 4 = 3','Survey 9 junior, 3 senior','Check 9:3 = 3:1'];break;
      case 3:case 6:{const counts=v.counts;labels=['Choose the categories',`Record ${counts.join(', ')}`,`Total ${counts.reduce((a,b)=>a+b,0)}`,scene.lesson===3?'Mode: score 2':'Modal class: 10–19','Recheck every tally'];break;}
      case 4:{const x=v.values;labels=['Order all seven values',`Sum ${x.reduce((a,b)=>a+b,0)}`,`Median ${x[3]}`,`Range ${x.at(-1)-x[0]}`,'Inspect the high extreme'];break;}
      case 5:{const a=v.series_a,b=v.series_b;labels=['Week 1 paired bars','Week 2 paired bars',`A gain ${a[1]-a[0]}`,`B gain ${b[1]-b[0]}`,'Compare both gains'];break;}
      case 7:labels=v.model==='pie'?['Three categories',`Total ${v.counts.reduce((a,b)=>a+b,0)}`,'Walking fraction','Sector × 360°','Sectors total 360°']:['Label both axes','Plot five pairs','Rise of 2 per hour','Positive association','Predict at 6 hours'];break;
      case 8:labels=['Read the two counts',`Axis begins at ${v.truncated_baseline}`,`True difference ${v.second-v.first}`,'Calculate percent change','Report the axis bias'];break;
    }
    return `<span data-object-id="visual-focus" class="g9-data-focus">${esc(labels[done-1])}</span>`;
  }
  for(let n=1;n<=8;n++)AthenaVisualizationRegistry.register('statistics',`grade9_data_${n}`,{
    render(params,state,phase){const scene=JSON.parse(params.scene_json),done=phaseStage(state,phase);
      if(scene.lesson!==n||scene.id!==params.question_id)throw Error('Dataset belongs to another question');
      return `<section class="g9-data-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}"><p data-object-id="problem">${esc(params.prompt)}</p><div data-object-id="model" class="g9-data-model">${draw(scene,done)}${focus(scene,done)}</div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&done<Number(params.total_steps)?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&done===Number(params.total_steps)?esc(state.after_state):''}</p></section>`;
    },destroy(){}
  });
})();
