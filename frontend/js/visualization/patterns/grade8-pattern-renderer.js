/* Question-specific numeric rows and counted geometric constructions. */
(() => {
  const esc = value => escapeWhiteboardHtml(String(value ?? ''));
  const points = (kind,n) => {
    const coords=[];
    const add=(x,y)=>coords.push([x,y]);
    if(kind==='square_dots'||kind==='square_plus'||kind==='square_plus_two') {
      for(let y=0;y<n;y++) for(let x=0;x<n;x++) add(x,y);
      const extras=kind==='square_plus'?4:kind==='square_plus_two'?2:0;
      for(let k=0;k<extras;k++) add(n+1,k);
    } else if(kind==='staircase') {for(let y=0;y<n;y++) for(let x=0;x<=y;x++) add(x,y);}
    else if(kind==='border') {for(let y=0;y<=n;y++)for(let x=0;x<=n;x++)if(x===0||y===0||x===n||y===n)add(x,y);}
    else if(kind==='l_shape') {for(let x=0;x<=n;x++)add(x,0);for(let y=1;y<=n;y++)add(0,y);}
    else if(kind==='two_rows') {for(let y=0;y<2;y++)for(let x=0;x<n;x++)add(x,y);}
    else if(kind==='rectangle'||kind==='rectangle_two') {for(let y=0;y<n;y++)for(let x=0;x<n+(kind==='rectangle'?1:2);x++)add(x,y);}
    else if(kind==='three_arms') {add(0,0);for(let k=1;k<=n;k++){add(k,0);add(0,k);add(k,k);}}
    else if(kind==='columns') {for(let y=0;y<2*n+1;y++){add(0,y);add(2,y);}}
    return coords;
  };
  const sticks=(kind,n)=>{
    const lines=[];
    const line=(x,y,X,Y)=>lines.push([x,y,X,Y]);
    if(kind==='joined_squares'||kind==='separate_squares'){
      for(let i=0;i<n;i++){
        const x=i*(kind==='joined_squares'?1:2);
        line(x,0,x+1,0);line(x,1,x+1,1);line(x+1,0,x+1,1);
        if(kind==='separate_squares'||i===0)line(x,0,x,1);
      }
    } else if(kind==='triangle_edges') {
      for(let i=0;i<n;i++){line(i,0,i+1,0);line(i/2,-i,(i+1)/2,-i-1);line(n-i/2,-i,n-(i+1)/2,-i-1);}
    } else if(kind==='fence') {
      for(let i=0;i<n+1;i++){line(i,0,i+1,0);line(i,n+1,i+1,n+1);line(0,i,0,i+1);line(n+1,i,n+1,i+1);}
    }
    return lines;
  };
  const figure=(scene,n,known,answer)=>{
    const kind=scene.kind, count=known?scene.terms[n-1]:answer;
    if(!known && answer===undefined) return `<div class="g8-pattern-figure g8-pattern-ghost" data-object-id="figure-${n}"><b>Figure ${n}</b><span>Build next figure</span><strong>?</strong></div>`;
    const seg=sticks(kind,n),coords=points(kind,n);
    const xMax=Math.max(6,...coords.map(v=>v[0]),...seg.map(v=>Math.max(v[0],v[2])));
    const yMin=Math.min(-1,...coords.map(v=>v[1]),...seg.map(v=>Math.min(v[1],v[3])));
    const yMax=Math.max(5,...coords.map(v=>v[1]),...seg.map(v=>Math.max(v[1],v[3])));
    const shapes=seg.length?seg.map(([x,y,X,Y],i)=>`<line data-object-id="piece-${n}-${i+1}" x1="${12+x*10}" y1="${20+y*10}" x2="${12+X*10}" y2="${20+Y*10}"/>`).join(''):
      coords.map(([x,y],i)=>`<circle data-object-id="piece-${n}-${i+1}" cx="${12+x*10}" cy="${15+y*10}" r="3"/>`).join('');
    // The model's own primitive count is checked before it is shown to a learner.
    if(shapes && (seg.length||coords.length)!==count) return `<div data-object-id="figure-${n}" class="g8-pattern-error" role="alert">Pattern figure mismatch; teacher review required</div>`;
    return `<div class="g8-pattern-figure" data-object-id="figure-${n}"><b>Figure ${n}</b><svg viewBox="0 ${Math.min(-15,15+yMin*10)} ${Math.max(94,22+xMax*10)} ${Math.max(100,35+(yMax-yMin)*10)}" role="img" aria-label="Figure ${n}: ${count} counted pieces">${shapes}</svg><strong>${count} pieces</strong></div>`;
  };
  AthenaVisualizationRegistry.register('algebra','grade8_pattern_board',{
    render(p,state,phase){
      const s=JSON.parse(p.scene_json),stage=Number(((state.annotations||[]).find(v=>v.startsWith('stage:'))||'stage:0').slice(6));
      const done=phase==='result'?stage:Math.max(0,stage-1);
      const final=done===4, showNext=final&&(Number.isFinite(s.answer)||typeof s.answer==='string'&&s.answer.trim().length>0);
      const diffs=s.terms.slice(1).map((v,i)=>v-s.terms[i]);
      const nextPosition=s.terms.length+1;
      const alignedTable=(missing)=>{
        const target=missing?s.target_position:undefined;
        const headers=s.terms.map((_,i)=>`<th scope="col">${i+1}</th>`).join('');
        const outputs=s.terms.map((v,i)=>`<td data-object-id="term-${i+1}">${esc(v)}</td>`).join('');
        const extra=missing?`<th scope="col" class="g8-pattern-target">${esc(target)}</th>`:'';
        const targetCell=missing?`<td data-object-id="target-slot" class="g8-pattern-target">${showNext?esc(s.answer):'?'}</td>`:'';
        const rule=missing?`<p class="g8-pattern-rule" data-object-id="given-rule">Given rule: T(n) = ${esc(s.rule)}</p>`:
          `<p class="g8-pattern-rule" data-object-id="derived-rule">${done>=3?'Proposed rule: ':''}<strong>${showNext?`T(n) = ${esc(s.answer)}`:done>=3?'T(n) = ?':''}</strong></p>`;
        const evidence=done>=2?`<p class="g8-pattern-evidence" data-object-id="position-check">${missing?`Check the given rule at positions 1 and 4 before finding T(${esc(target)}).`:`Every change is ${esc(s.a)}. At n = 1, the fixed part is ${done>=3?esc(s.b):'?'}.`}</p>`:'';
        return `<div class="g8-pattern-table-wrap"><table class="g8-pattern-table" aria-label="Position and output table"><tbody><tr><th scope="row">Position n</th>${headers}${extra}</tr><tr><th scope="row">Output T(n)</th>${outputs}${targetCell}</tr></tbody></table>${rule}${evidence}</div>`;
      };
      const row=s.model==='geometric'?`<div class="g8-pattern-figures">${s.terms.map((_,i)=>figure(s,i+1,true)).join('')}${done>=3?figure(s,nextPosition,false,showNext?s.answer:undefined):''}</div>`:
        s.model==='rule_table'||s.model==='missing_table'?alignedTable(s.model==='missing_table'):
        `<div class="g8-pattern-row">${s.terms.map((v,i)=>`<div class="g8-pattern-term" data-object-id="term-${i+1}"><span>Position ${i+1}</span><strong>${esc(v)}</strong></div>`).join('')}${done>=3?`<div class="g8-pattern-term" data-object-id="term-next"><span>Position ${nextPosition}</span><strong>${showNext?esc(s.answer):'?'}</strong></div>`:''}</div>`;
      const diffRow=done>=2?`<div class="g8-pattern-differences" aria-label="Changes between given values">${diffs.map((v,i)=>`<span data-object-id="change-${i+1}">${v>=0?'+':''}${esc(v)}</span>`).join('')}</div>`:'';
      let evidenceBoard='';
      if(s.model==='compare_rules'){
        const n=s.wrong_index;
        const evaluate=(c,at)=>({linear:()=>c.a*at+c.b,square_offset:()=>c.a*at*at+c.b,
          triangular:()=>c.a*at*(at+1)/2+c.b,rectangle:()=>c.a*at*(at+1)+c.b,
          geometric:()=>c.a*c.b**(at-1)})[c.family]();
        const target=s.target_position;
        evidenceBoard=`<div class="g8-pattern-evidence-board" data-object-id="model"><table class="g8-pattern-table" aria-label="Test both pattern rules against the givens"><tbody><tr><th scope="row">Position</th>${s.terms.map((_,i)=>`<th scope="col">${i+1}</th>`).join('')}<th scope="col">${esc(target)}</th></tr><tr><th scope="row">Given</th>${s.terms.map((v,i)=>`<td data-object-id="term-${i+1}">${esc(v)}</td>`).join('')}<td data-object-id="target-slot">${final?esc(s.answer):'?'}</td></tr>${s.candidates.map((c,i)=>`<tr data-object-id="candidate-${i+1}"><th scope="row">Rule ${i?'B':'A'}: ${esc(c.rule)}</th>${s.terms.map((_,j)=>`<td>${done>=2?esc(evaluate(c,j+1)):'·'}</td>`).join('')}<td>${final&&((i===0?'A':'B')===s.correct_label)?esc(evaluate(c,target)):'?'}</td></tr>`).join('')}</tbody></table><p data-object-id="counterexample">${done>=3?`At position ${esc(n)}, Rule ${s.correct_label==='A'?'B':'A'} disagrees with the given ${esc(s.terms[n-1])}.`:''}</p></div>`;
      }else if(s.model==='repair_claim'){
        evidenceBoard=`<div class="g8-pattern-evidence-board" data-object-id="model"><table class="g8-pattern-table" aria-label="Test and repair the learner prediction"><tbody><tr><th scope="row">Position</th>${s.terms.map((_,i)=>`<th scope="col">${i+1}</th>`).join('')}<th scope="col">${esc(s.target_position)}</th></tr><tr><th scope="row">Output</th>${s.terms.map((v,i)=>`<td data-object-id="term-${i+1}">${esc(v)}</td>`).join('')}<td data-object-id="target-slot">${final?esc(s.answer):'?'}</td></tr>${done>=2?`<tr><th scope="row">Change</th><td>start</td>${diffs.map((v,i)=>`<td data-object-id="change-${i+1}">${v>=0?'+':''}${esc(v)}</td>`).join('')}<td>check</td></tr>`:''}</tbody></table><p data-object-id="student-claim">Learner claim: T(${esc(s.target_position)}) = ${esc(s.claimed)}</p><p data-object-id="derived-rule">${done>=3?`Rebuilt rule: T(n) = ${esc(s.rule)}`:''}</p><p data-object-id="corrected-value">${final?`Corrected: T(${esc(s.target_position)}) = ${esc(s.answer)}`:''}</p></div>`;
      }
      if(evidenceBoard)return `<section class="g8-pattern-board" data-managed-visibility="true" data-question-id="${esc(p.question_id)}" data-phase="${esc(phase)}"><p class="g8-original" data-object-id="problem">${esc(p.prompt)}</p>${evidenceBoard}<div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state||'')}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Pattern action</span><strong>${phase==='ready'?'':esc(state.working_state||'')}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${phase==='result'&&!final?esc(state.after_state||''):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Check against the original terms</span><strong>${final?esc(state.after_state||''):''}</strong></div></div></div></section>`;
      return `<section class="g8-pattern-board" data-managed-visibility="true" data-question-id="${esc(p.question_id)}" data-phase="${esc(phase)}"><p class="g8-original" data-object-id="problem">${esc(p.prompt)}</p><div data-object-id="model">${row}${diffRow}</div><div class="g8-mathematical-transition"><div class="g8-state g8-state--before">${esc(state.before_state||'')}</div><div class="g8-action-slot"><div data-object-id="operation" class="g8-timeline-object g8-operation ${phase==='ready'?'is-hidden':'is-visible'}"><span>Pattern action</span><strong>${phase==='ready'?'':esc(state.working_state||'')}</strong></div><div data-object-id="result" class="g8-timeline-object g8-result ${phase==='result'&&!final?'is-visible':'is-hidden'}"><span>Result of this step</span><strong>${phase==='result'&&!final?esc(state.after_state||''):''}</strong></div><div data-object-id="verification" class="g8-timeline-object g8-verification ${final?'is-visible':'is-hidden'}"><span>Check the rule</span><strong>${final?esc(state.after_state||''):''}</strong></div></div></div></section>`;
    },destroy(){}
  });
})();
