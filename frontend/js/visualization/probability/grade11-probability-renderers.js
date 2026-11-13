/* Grade 11 Probability: the current question owns every region, branch and cell. */
(() => {
  const esc = value => escapeWhiteboardHtml(String(value ?? ''));
  const position = (state,phase) => {
    const tag=(state.annotations||[]).find(value=>/^stage:\d+$/.test(value));
    const n=Number(tag?.slice(6)||0);
    return phase==='result'?n:Math.max(0,n-1);
  };
  const txt=(x,y,value,klass='')=>`<text x="${x}" y="${y}" class="${klass}">${esc(value)}</text>`;
  const line=(x1,y1,x2,y2,klass='')=>`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${klass}"/>`;
  const frac=(a,b)=>`${a}/${b}`;

  function venn2(v,s) {
    const total=v.aonly+v.both+v.bonly+v.neither;
    let out=`<rect x="35" y="35" width="480" height="255" rx="10" class="g11-prob-universe"/>${txt(45,55,`S: ${total} outcomes`)}`;
    out+=`<circle cx="225" cy="165" r="85" class="g11-prob-circle"/><circle cx="325" cy="165" r="85" class="g11-prob-circle"/>`;
    out+=txt(169,94,'A')+txt(371,94,'B');
    if(s>=1)out+=txt(263,169,v.both,'g11-prob-region');
    if(s>=2)out+=txt(184,169,v.aonly,'g11-prob-region')+txt(357,169,v.bonly,'g11-prob-region');
    if(s>=3)out+=txt(470,265,v.neither,'g11-prob-region');
    if(s>=4){const selected=v.target==='union'?[v.aonly,v.both,v.bonly]:v.target==='intersection'?[v.both]:[v.bonly,v.neither];out+=txt(60,267,`Selected: ${selected.join(' + ')}`, 'g11-prob-working');}
    if(s>=5){const c=v.target==='union'?v.aonly+v.both+v.bonly:v.target==='intersection'?v.both:v.bonly+v.neither;out+=txt(62,314,`Favourable ${c} of ${total}`, 'g11-prob-answer');}
    return out;
  }
  function venn3(v,s){
    const total=v.aonly+v.bonly+v.conly+v.ab+v.ac+v.bc+v.abc+v.outside;
    let out=`<rect x="20" y="25" width="520" height="275" rx="12" class="g11-prob-universe"/>`;
    out+=`<circle cx="220" cy="155" r="92" class="g11-prob-circle"/><circle cx="335" cy="155" r="92" class="g11-prob-circle"/><circle cx="277" cy="214" r="92" class="g11-prob-circle"/>`;
    out+=txt(135,91,'A')+txt(409,91,'B')+txt(277,298,'C');
    if(s>=1)out+=txt(273,180,v.abc,'g11-prob-region');
    if(s>=2)out+=txt(270,104,v.ab,'g11-prob-region')+txt(216,211,v.ac,'g11-prob-region')+txt(332,211,v.bc,'g11-prob-region');
    if(s>=3)out+=txt(173,147,v.aonly,'g11-prob-region')+txt(377,147,v.bonly,'g11-prob-region')+txt(277,259,v.conly,'g11-prob-region')+txt(482,273,v.outside,'g11-prob-region');
    if(s>=4)out+=txt(28,321,`8 disjoint regions; N = ${total}`, 'g11-prob-working');
    if(s>=5){const c=v.target==='exactly one'?v.aonly+v.bonly+v.conly:v.target==='at least two'?v.ab+v.ac+v.bc+v.abc:total-v.outside;out+=txt(293,321,`${v.target}: ${c} of ${total}`,'g11-prob-answer');}
    return out;
  }
  function tree(v,s){
    const n=v.red+v.blue,second=v.replacement?n:n-1;
    let out=txt(35,44,`${v.red} red + ${v.blue} blue; ${v.replacement?'with':'without'} replacement`);
    out+=line(65,160,230,90,'g11-prob-branch')+line(65,160,230,240,'g11-prob-branch');
    out+=txt(110,110,frac(v.red,n))+txt(110,220,frac(v.blue,n));
    out+=txt(229,84,'R')+txt(229,258,'B');
    if(s>=2){out+=line(250,90,440,48,'g11-prob-branch')+line(250,90,440,133,'g11-prob-branch');out+=txt(315,65,frac(v.replacement?v.red:v.red-1,second))+txt(315,130,frac(v.blue,second));out+=txt(445,50,'RR')+txt(445,138,'RB');}
    if(s>=3){out+=line(250,240,440,188,'g11-prob-branch')+line(250,240,440,280,'g11-prob-branch');out+=txt(315,190,frac(v.red,second))+txt(315,278,frac(v.replacement?v.blue:v.blue-1,second));out+=txt(445,188,'BR')+txt(445,286,'BB');}
    if(s>=4)out+=txt(34,321,`Multiply along each branch; add disjoint paths for ${v.target}.`,'g11-prob-working');
    if(s>=5)out+=txt(34,347,`Second-draw denominator: ${second}`,'g11-prob-answer');
    return out;
  }
  function table(v,s){
    const [ax,ay,bx,by]=v.cells,all=ax+ay+bx+by,rect=(x,y,w,h)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}"/>`;
    let out=`<g class="g11-prob-grid">${rect(65,60,425,190)}${[145,230,315,395].map(x=>line(x,60,x,250)).join('')}${[105,155,205].map(y=>line(65,y,490,y)).join('')}</g>`;
    out+=txt(166,91,'X')+txt(250,91,'Y')+txt(332,91,'Total')+txt(74,141,'A')+txt(74,191,'B')+txt(70,238,'Total');
    if(s>=1)out+=txt(170,141,ax,'g11-prob-cell')+txt(252,141,ay,'g11-prob-cell')+txt(170,191,bx,'g11-prob-cell')+txt(252,191,by,'g11-prob-cell');
    if(s>=2)out+=txt(333,141,ax+ay,'g11-prob-cell')+txt(333,191,bx+by,'g11-prob-cell')+txt(170,238,ax+bx,'g11-prob-cell')+txt(252,238,ay+by,'g11-prob-cell');
    if(s>=3)out+=txt(333,238,all,'g11-prob-cell');
    if(s>=4)out+=txt(70,285,`Selection: ${v.target}; favourable cell ${v.target==='first row given second column'?ay:ax}`,'g11-prob-working');
    if(s>=5)out+=txt(70,314,`Denominator: ${v.target==='first row given second column'?ay+by:v.target==='first column given first row'?ax+ay:all}`,'g11-prob-answer');
    return out;
  }
  function model(scene,s){
    const v=scene.visual.values;
    if(v.mode==='venn2')return venn2(v,s);
    if(v.mode==='venn3')return venn3(v,s);
    if(v.mode==='tree')return tree(v,s);
    if(v.mode==='table')return table(v,s);
    if(v.mode==='independence')return venn2({aonly:v.a-v.both,both:v.both,bonly:v.b-v.both,neither:v.total-v.a-v.b+v.both,target:'intersection'},s)+
      (s>=4?txt(55,342,`Compare ${v.both}/${v.total} with (${v.a}/${v.total}) × (${v.b}/${v.total})`,'g11-prob-working'):'');
    const n=v.red+v.blue;
    let out=txt(55,52,`Bag: ${v.red} red, ${v.blue} blue`);
    for(let j=0;j<n;j++){const x=72+(j%12)*37,y=105+Math.floor(j/12)*44;out+=`<circle cx="${x}" cy="${y}" r="13" class="g11-prob-${j<v.red?'red':'blue'}"/>`;}
    if(s>=2)out+=txt(55,223,`Favourable red counters: ${v.red} / total ${n}`,'g11-prob-working');
    if(s>=4)out+=txt(55,260,`Observed red: ${v.observed} / ${v.trials} replacement draws`,'g11-prob-working');
    return out;
  }
  function render(parameters,state,phase,lesson){
    const scene=JSON.parse(parameters.scene_json);
    if(scene.id!==parameters.question_id||scene.problem!==parameters.prompt||scene.lesson!==lesson||scene.visual?.family!=='grade11_probability')throw Error('Probability model belongs to another question');
    const s=position(state,phase);
    return `<section class="g11-prob-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}"><p data-object-id="problem">${esc(scene.problem)}</p>
      <div data-object-id="model" class="g11-prob-model"><svg viewBox="0 0 560 365" role="img" aria-label="Probability diagram for ${esc(scene.id)}"><title>Question-specific ${esc(scene.visual.values.mode)} model, stage ${s} of 5</title>${model(scene,s)}</svg></div>
      <p data-object-id="operation">${phase==='operation'?esc(state.working_state):''}</p>
      <p data-object-id="result">${phase==='result'&&s<5?esc(state.after_state):''}</p>
      <p data-object-id="verification">${phase==='result'&&s===5?esc(state.after_state):''}</p></section>`;
  }
  for(let n=1;n<=7;n++)AthenaVisualizationRegistry.register('statistics',`grade11_prob_${n}`,{render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
