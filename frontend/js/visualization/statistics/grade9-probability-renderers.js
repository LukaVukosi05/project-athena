/* Grade 9 probability diagrams are derived from each question's original outcomes. */
(() => {
  const esc = value => escapeWhiteboardHtml(String(value ?? ''));
  const text = (id,x,y,s) => `<text data-object-id="${id}" x="${x}" y="${y}">${esc(s)}</text>`;
  const rect = (x,y,w,h,cls='') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" class="${cls}"/>`;
  const line = (x,y,X,Y,cls='') => `<line x1="${x}" y1="${y}" x2="${X}" y2="${Y}" class="${cls}"/>`;
  const done = (state,phase) => {
    const mark=(state.annotations||[]).find(s=>/^stage:\d+$/.test(s));
    const n=mark?Number(mark.slice(6)):0;
    return phase==='result'?n:Math.max(0,n-1);
  };
  function diagram(scene,step) {
    const v=scene.visual.values, n=scene.lesson;
    let content='', focus='';
    if(n===1){
      const outcomes=v.outcomes, total=outcomes.length, fav=outcomes.filter(x=>x%3===0);
      content+=text('sample-space',18,29,`Spinner outcomes: 1 to ${total}`);
      outcomes.forEach((x,i)=>{
        const col=i%10,row=Math.floor(i/10),sx=20+col*46,sy=46+row*43;
        content+=`<g data-object-id="outcome-${x}">${rect(sx,sy,37,34,step>=2&&x%3===0?'g9-prob-hit':'g9-prob-cell')}${text(`number-${x}`,sx+11,sy+23,x)}</g>`;
      });
      if(step>=3)focus=`${fav.length} favourable outcomes out of ${total}`;
      else if(step>=2)focus=`Multiples of 3: ${fav.join(', ')}`;
      else focus=`Count all ${total} equally likely sectors`;
      if(step>=4)focus+=`; P = ${fav.length}/${total}`;
    }else if(n===2){
      const [[a,b],[c,d]]=v.table, cells=[[a,b],[c,d]], labels=['Bus','Walk'];
      content+=text('head',90,37,'Grade 9')+text('head-8',277,37,'Grade 8');
      for(let r=0;r<2;r++){
        content+=text(`row-${r}`,12,91+r*64,labels[r]);
        for(let col=0;col<2;col++){
          const x=100+col*174,y=52+r*64;
          content+=rect(x,y,145,51,step>=2&&r===0&&col===0?'g9-prob-hit':'g9-prob-cell');
          content+=text(`cell-${r}-${col}`,x+58,y+33,cells[col][r]);
        }
      }
      if(step>=2)content+=text('row-total',90,215,`Grade 9 total: ${a+b}`);
      if(step>=3)content+=text('column-total',277,215,`Bus total: ${a+c}`);
      focus=step>=4?`Given Grade 9, P(bus) = ${a}/${a+b}`:'Use the Grade 9 column as the condition';
    }else if(n===3){
      const red=v.red, blue=v.blue, total=red+blue;
      content+=text('bag',15,31,`Bag: ${red} red, ${blue} blue; two draws without replacement`);
      const branches=[['R',red,total,65],['B',blue,total,184]];
      for(const [label,num,den,y] of branches){
        content+=line(42,133,178,y,step>=2&&label==='R'?'g9-prob-path':'g9-prob-line');
        content+=text(`first-${label}`,189,y+4,`${label}: ${step>=2?`${num}/${den}`:'?'}`);
        const next=label==='R'?[[red-1,'R'],[blue,'B']]:[[red,'R'],[blue-1,'B']];
        next.forEach(([count,l],i)=>{
          const yy=y+(i===0?-28:28);
          content+=line(254,y,352,yy,step>=3&&label==='R'&&l==='R'?'g9-prob-path':'g9-prob-line');
          content+=text(`second-${label}-${l}`,362,yy+4,`${l}: ${step>=3?`${count}/${total-1}`:'?'}`);
        });
      }
      focus=step>=4?`Red then red: ${red}/${total} × ${red-1}/${total-1}`:'Each second branch has one fewer counter';
    }else if(n===4){
      const h=v.heads, trials=v.trials,t=trials-h;
      content+=text('record',20,33,`Coin tossed ${trials} times`);
      content+=rect(77,75,350,50,'g9-prob-cell')+rect(77,145,350,50,'g9-prob-cell');
      content+=text('heads',91,108,`Heads: ${h}`)+text('tails',91,178,`Tails: ${step>=2?t:'count from total'}`);
      if(step>=3){
        content+=rect(275,87,Math.round(140*h/trials),20,'g9-prob-hit');
        content+=text('frequency',282,132,`Observed ${h}/${trials}`);
      }
      focus=step>=4?'Fair coin predicts 25 heads in 50 tosses; observed frequency can differ':'Separate what happened from what fairness predicts';
    }else{
      const total=v.sectors,fav=Math.floor(total/3);
      content+=text('joint-head',13,30,`Spinner 1–${total} × coin H/T${step>=3?`: ${2*total} pairs`:''}`);
      const width=Math.min(27,445/total);
      for(let i=1;i<=total;i++)for(let j=0;j<2;j++){
        const x=20+(i-1)*width,y=61+j*66;
        content+=rect(x,y,width-2,54,step>=2&&i%3===0&&j===0?'g9-prob-hit':'g9-prob-cell');
        if(total<=16)content+=text(`pair-${i}-${j}`,x+2,y+32,`${i}${j?'T':'H'}`);
      }
      if(step>=2)content+=text('event',20,219,`${fav} favourable H pairs (multiple of 3)`);
      focus=step>=4?`For AND: ${fav}/${total} × 1/2 = ${fav}/${2*total}`:'AND means an intersection; adding probabilities is the error';
    }
    if(step>=5)focus='Check against the full sample space and original event.';
    return `<svg viewBox="0 0 500 280" role="img" aria-label="${esc(scene.problem)}"><title>${esc(v.model)} for this question</title>${content}${text('focus-label',20,265,step?`Step ${step}: ${focus}`:'Read the given outcomes and event')}</svg>`;
  }
  for(let n=1;n<=5;n++) AthenaVisualizationRegistry.register('statistics',`grade9_probability_${n}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),step=done(state,phase);
      if(scene.lesson!==n||scene.id!==params.question_id||scene.problem!==params.prompt)throw Error('Probability diagram belongs to another question');
      return `<section class="g9-prob-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p><div data-object-id="model" class="g9-prob-model">${diagram(scene,step)}</div><p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p><p data-object-id="result">${phase==='result'&&step<5?esc(state.after_state):''}</p><p data-object-id="verification">${phase==='result'&&step===5?esc(state.after_state):''}</p></section>`;
    },destroy(){}
  });
})();
