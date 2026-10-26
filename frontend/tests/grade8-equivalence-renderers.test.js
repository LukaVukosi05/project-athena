const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-equivalence-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/functions_relationships_02.json'),'utf8')).worked_examples;
function render(q,phase,step=1){
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,given_objects:q.model.inputs,derived_objects:q.model.outputs,total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-functions-relationships-02',question_id:q.id});
 assert.ok(session.instruction,q.id);
 return session.render({visualization_state:{annotations:[`stage:${step}`],before_state:q.states[step-1],
  working_state:q.steps[step-1]?.action||'Check the original',after_state:q.states[step]||`Checked: ${q.verify}`}},phase);
}
test('15 equivalence questions have family-specific scenes, hidden answers and distinct stages',()=>{
 assert.equal(questions.length,15);assert.equal(new Set(questions.map(q=>q.model.family)).size,6);
 for(const q of questions){
  const ready=render(q,'ready'),operation=render(q,'operation'),result=render(q,'result');
  assert.notEqual(ready,operation,q.id);assert.notEqual(operation,result,q.id);
  assert.match(ready,/is-concealed/,q.id);assert.ok(!ready.includes(q.model.outputs.at(-1)),q.id);
  assert.ok(ready.includes(`data-question-id="${q.id}"`));
  assert.match(operation,/Legal mathematical action/,q.id);
  assert.ok(render(q,'result',q.steps.length+1).includes(q.model.outputs.at(-1)),q.id);
  for(let i=1;i<=q.model.inputs.length;i++)assert.ok(ready.includes(`data-object-id="given-${i}"`),q.id);
  for(let i=1;i<=q.model.outputs.length;i++)assert.ok(ready.includes(`data-object-id="derived-${i}"`),q.id);
 }
});
test('given values alter visuals, and the operation states preserve the earlier derived object',()=>{
 const q=questions[2],changed={...q,model:{...q.model,inputs:['input z','add 19','triple']}};
 assert.notEqual(render(q,'ready'),render(changed,'ready'));
 assert.match(render(questions[4],'ready'),/equiv-table-row/);
 assert.match(render(questions[7],'ready'),/equiv-lane/);
 assert.match(render(questions[8],'ready'),/Fixed once/);
 assert.match(render(questions[11],'ready'),/Allowed inputs/);
 assert.ok(render(q,'result',2).includes(q.model.outputs[0]));
 assert.ok(render(q,'ready',3).includes(q.model.outputs[0]));
});
