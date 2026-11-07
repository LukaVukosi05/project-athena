/* Grade 9 equations: question-owned models with ordered mathematical states. */
(() => {
  const esc=value=>escapeWhiteboardHtml(String(value??''));
  const stage=(state,phase)=>{
    const match=(state.annotations||[]).find(value=>/^stage:\d+$/.test(value))||'stage:0';
    const n=Number(match.slice(6));return phase==='result'?n:Math.max(0,n-1);
  };
  const line=(label,value,visible=true)=>`<div class="g9-eq-line"><span>${esc(label)}</span><strong>${visible?esc(value):'?'}</strong></div>`;
  function model(scene,done){
    const {family,values:v,givens}=scene.visual;
    if(family==='givens')return '<div class="g9-eq-givens"><span>Read the original equation and mark its known quantities.</span></div>';
    if(family==='groups')return `<div class="g9-eq-groups" aria-label="Equal group boxes and separate helpers">
      <div class="g9-eq-boxes">${Array.from({length:v.multiplier},()=>'<span>x</span>').join('')}<b>+ ${v.offset} helpers</b></div>
      ${line('Total people',v.total)}${line('Equation',`${v.multiplier}x + ${v.offset} = ${v.total}`,done>=2)}${line('Learners in each group',v.solution,done>=4)}</div>`;
    if(family==='zero_product')return `<div class="g9-eq-branches" aria-label="Two zero-product branches">
      ${v.expanded?line('Original',`x² ${v.middle>=0?'+':'−'} ${Math.abs(v.middle)}x ${v.constant>=0?'+':'−'} ${Math.abs(v.constant)} = 0`):''}
      ${line('Product',`(x − ${v.first})(x + ${-v.second}) = 0`,!v.expanded||done>=2)}
      ${line('First factor',`x − ${v.first} = 0 ⇒ x = ${v.first}`,done>=(v.expanded?4:2))}
      ${line('Second factor',`x + ${-v.second} = 0 ⇒ x = ${v.second}`,done>=(v.expanded?5:3))}</div>`;
    if(family==='table')return `<div class="g9-eq-table" aria-label="Ordered input and output pairs">
      <div class="g9-eq-row"><b>x input</b><b>y output</b></div>
      ${[[v.input_one,v.out_one,2],[v.input_two,v.out_two,3],[v.solution,v.target,4]].map(([x,y,stageNumber],i)=>{
        const at=stageNumber+(v.diagnostic?1:0);
        return `<div class="g9-eq-row"><span>${i===2&&done<at?'?':esc(x)}</span><span>${i===2||done>=at?esc(y):'?'}</span></div>`;
      }).join('')}</div>`;
    if(family==='powers')return `<div class="g9-eq-balance" aria-label="Matching bases and exponents">
      ${line('Same base',`${v.base} = ${v.base}`)}${line('Equate exponents',`x + ${v.left} = ${v.power}`,done>=2)}${line('Unknown exponent',`x = ${v.solution}`,done>=3)}</div>`;
    if(family==='brackets')return `<div class="g9-eq-balance" aria-label="Brackets and two sides of equality">
      ${line('Left side',`${v.multiplier}(x + ${v.offset})`)}${line('Right side',`${v.other}x ${v.right>=0?'+':'−'} ${Math.abs(v.right)}`)}
      ${line('Expanded left',`${v.multiplier}x + ${v.multiplier*v.offset}`,done>=1)}${line('Solution',`x = ${v.solution}`,done>=4)}</div>`;
    return `<div class="g9-eq-balance" aria-label="The same inverse operation on both sides">
      ${line('Original',`${v.multiplier}x + ${v.offset} = ${v.total}`)}
      ${line(`Subtract ${v.offset} on both sides`,`${v.multiplier}x = ${v.total-v.offset}`,done>=2)}
      ${line(`Divide both sides by ${v.multiplier}`,`x = ${v.solution}`,done>=3)}</div>`;
  }
  for(let number=1;number<=6;number++)AthenaVisualizationRegistry.register('algebra',`grade9_equation_${number}`,{
    render(params,state,phase){
      const scene=JSON.parse(params.scene_json),done=stage(state,phase),total=Number(params.total_steps);
      if(scene.lesson!==number)throw Error('The equation diagram belongs to another lesson');
      return `<section class="g9-eq-board" data-managed-visibility="true" data-question-id="${esc(params.question_id)}">
        <p data-object-id="problem" class="g9-eq-question">${esc(params.prompt)}</p>
        <div data-object-id="model" class="g9-eq-model">${model(scene,done)}</div>
        <p data-object-id="operation" class="g9-eq-operation">${phase==='operation'?esc(state.working_state):''}</p>
        <p data-object-id="result" class="g9-eq-result">${phase==='result'&&done<total?esc(state.after_state):''}</p>
        <p data-object-id="verification" class="g9-eq-verification">${phase==='result'&&done===total?esc(state.after_state):''}</p>
      </section>`;
    },destroy(){}
  });
})();
