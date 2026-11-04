/* Grade 9 Topic 1: exact set placement and question-specific prime trees. */
(() => {
  const esc = value => escapeWhiteboardHtml(String(value ?? ""));
  const stageOf = (state, phase) => {
    const annotation = (state.annotations || []).find(item => /^stage:\d+$/.test(item)) || "stage:0";
    const stage = Number(annotation.slice(6));
    return phase === "result" ? stage : Math.max(0, stage - 1);
  };
  const transition = (state, phase, final) => `<div class="g9-board-action">
    <div data-object-id="operation" class="g9-action ${phase === "operation" ? "is-active" : ""}">${phase === "operation" ? esc(state.working_state) : ""}</div>
    <div data-object-id="result" class="g9-action ${phase === "result" && !final ? "is-active" : ""}">${phase === "result" && !final ? esc(state.after_state) : ""}</div>
    <div data-object-id="verification" class="g9-action ${final ? "is-active" : ""}">${final ? esc(state.after_state) : ""}</div>
  </div>`;
  AthenaVisualizationRegistry.register("algebra", "grade9_number_sets", {
    render(parameters, state, phase) {
      const scene=JSON.parse(parameters.scene_json);
      const done=stageOf(state,phase), count=Number(parameters.total_steps);
      const classified=Boolean(scene.category) && done>=(scene.primary_stage || Math.max(2,count-2));
      const secondClassified=Boolean(scene.secondary_category) && done>=scene.secondary_stage;
      const final=done===count;
      const ordered=["R","Q","Z","W","N"];
      const label={R:"Real numbers R",Q:"Rational Q",Z:"Integers Z",W:"Whole W",N:"Natural N",I:"Irrational I",outside:"Outside the real numbers"};
      const visible=[classified ? scene.category : null,secondClassified ? scene.secondary_category : null].filter(Boolean);
      const nested=ordered.map((set,index)=>`<div class="g9-set g9-set--${set} ${visible.some(category=>category===set || (category!=="I" && category!=="outside" && ordered.indexOf(set)<=ordered.indexOf(category))) ? "g9-set--active" : ""}" data-set="${set}" data-object-id="${set==='N'?'category':'model'}"><span>${label[set]}</span>${secondClassified && scene.secondary_category===set?`<strong>${esc(scene.secondary)}</strong>`:""}${classified && scene.category===set?`<strong data-object-id="token">${esc(scene.token)}</strong>`:""}</div>`).join("");
      const branch=classified && scene.category==="I" ? `<strong data-object-id="token">${esc(scene.token)}</strong>` : "";
      const outside=classified && scene.category==="outside" ? `<strong data-object-id="token">${esc(scene.token)}</strong>` : "";
      const secondBranch=secondClassified && scene.secondary_category==='I' ? `<strong>${esc(scene.secondary)}</strong>` : '';
      const secondOutside=secondClassified && scene.secondary_category==='outside' ? `<strong>${esc(scene.secondary)}</strong>` : '';
      return `<section class="g9-number-board" data-managed-visibility="true" data-question-id="${esc(parameters.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem" class="g9-given">${esc(parameters.prompt)}</p>
        <div class="g9-number-stage"><div class="g9-set-stack" aria-label="Nested real-number sets">${nested}<div data-set="I" class="g9-set g9-set--irrational ${branch||secondBranch?'g9-set--active':''}">${label.I}${branch}${secondBranch}</div></div>
        <div class="g9-token-tray"><span>${classified ? "Classified value" : "Value to classify"}</span>${outside || (!classified ? `<strong data-object-id="token">${esc(scene.token || 'Read the given expression')}</strong>` : '')}${scene.secondary_input?`<span>${secondClassified ? 'Compared value' : 'Value to compare'}</span><strong>${esc(secondClassified ? scene.secondary : scene.secondary_input)}</strong>`:''}${secondOutside}${classified && scene.category==='outside'?`<small>${label.outside}</small>`:''}</div></div>
        <div data-object-id="selection" class="g9-selection">${classified?`Smallest set for ${esc(scene.token)}: ${esc(label[scene.category])}`:''}${secondClassified?` · ${esc(scene.secondary_input)}: ${esc(label[scene.secondary_category])}`:''}</div>${transition(state,phase,final)}</section>`;
    },destroy(){}
  });
  AthenaVisualizationRegistry.register("algebra", "grade9_prime_factors", {
    render(parameters,state,phase) {
      const scene=JSON.parse(parameters.scene_json), done=stageOf(state,phase), count=Number(parameters.total_steps);
      const roots=scene.numbers || [], factors=scene.factors || [];
      const cards=roots.map((n,i)=>{
        const leaves=factors[i] || [];
        let quotient=n;
        const visible=Math.min(Math.max(0,done-i),Math.max(0,leaves.length-1));
        const branches=leaves.slice(0,visible).map((prime,j)=>{
          const next=quotient/prime;
          const line=`<div class="g9-factor-branch" data-object-id="prime-leaves"><span>${esc(quotient)}</span><span>→</span><span>${esc(prime)} × ${esc(next)}</span></div>`;
          quotient=next;return line;
        }).join('');
        return `<article class="g9-factor-card" data-object-id="factor-roots"><strong>${esc(n)}</strong>${branches}${done>=Math.max(i+2,count-2) && leaves.length?`<p>${leaves.map(esc).join(' × ')}</p>`:''}</article>`;
      }).join('');
      let context='';
      if(scene.kind?.includes('clock')) context=`<div class="g9-context-track" data-object-id="selection">${roots.map(n=>`<span>Every ${esc(n)} min</span>`).join('')}</div>`;
      if(scene.kind==='hcf_ribbon') context=`<div class="g9-context-track" data-object-id="selection">${roots.map(n=>`<span class="g9-ribbon">${esc(n)} cm</span>`).join('')}</div>`;
      if(scene.kind==='hcf_pack') context=`<div class="g9-context-track" data-object-id="selection">${esc(roots[0])} red · ${esc(roots[1])} blue</div>`;
      if(scene.kind==='candidate_hcf') context=`<div class="g9-context-track" data-object-id="selection">Candidates: ${roots.slice(1).map(esc).join(', ')}</div>`;
      const final=done===count;
      return `<section class="g9-number-board" data-managed-visibility="true" data-question-id="${esc(parameters.question_id)}" data-phase="${esc(phase)}"><p data-object-id="problem" class="g9-given">${esc(parameters.prompt)}</p>
        <div data-object-id="model" class="g9-factor-stage">${cards}</div>${context}<p class="g9-selection" data-object-id="selection">${done>=count-2?`Compare prime powers for ${esc(scene.kind?.replace('_',' ') || 'the requested result')}.`:''}</p>
        ${transition(state,phase,final)}</section>`;
    },destroy(){}
  });
})();
