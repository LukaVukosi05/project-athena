const {test}=require('node:test'), assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path'), vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-expressions-renderers.js']) vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const pack=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_02.json'),'utf8'));
function render(item,phase,stage=1){
  const params={prompt:item.q,question_id:item.id,model_tokens:item.model.tokens,model_lanes:item.model.lanes,total_steps:item.steps.length+1};
  const state={annotations:[`stage:${stage}`],before_state:item.states[stage-1],working_state:item.steps[stage-1]?.action||item.verify,after_state:item.states[stage]||`Checked: ${item.verify}`};
  return AthenaVisualizationRegistry.resolve('algebra',item.model.family).render(params,state,phase);
}
test('all 15 question visuals have unique targets, no initial answer and distinct teaching states',()=>{
  assert.equal(pack.worked_examples.length,15);
  for(const item of pack.worked_examples){
    const initial=render(item,'initial'),operation=render(item,'operation'),result=render(item,'result');
    assert.notEqual(initial,operation,item.id);assert.notEqual(operation,result,item.id);
    assert.ok(!initial.includes(item.states[1]),item.id);
    for(let n=1;n<=item.model.tokens.length;n++){
      assert.equal((result.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,`${item.id} token ${n}`);
    }
  }
});
test('sorting moves given terms to question-specific lanes and bracket models remain distinct',()=>{
  const mixed=pack.worked_examples[6],signed=pack.worked_examples[1],bracket=pack.worked_examples[7];
  assert.ok(render(mixed,'initial').includes('Expression as given'));
  assert.ok(render(mixed,'result').includes('data-lane="x²"'));
  assert.ok(render(mixed,'result').includes('data-lane="x"'));
  assert.ok(render(signed,'result').includes('data-lane="a"'));
  assert.ok(render(bracket,'result',2).includes('Subtract the whole bracket'));
  assert.ok(render(pack.worked_examples[14],'result').includes('Subtract every term'));
  assert.ok(render(pack.worked_examples[10],'result').includes('<rect'));
});
