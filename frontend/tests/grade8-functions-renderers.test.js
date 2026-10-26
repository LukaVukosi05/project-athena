const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-functions-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/functions_relationships_01.json'),'utf8')).worked_examples;
function render(q,phase,step=1){
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,given_objects:q.model.inputs,derived_objects:q.model.outputs,total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-functions-relationships-01',question_id:q.id});
 assert.ok(session.instruction,`${q.id}: no visualization registered`);
 return session.render({visualization_state:{annotations:[`stage:${step}`],before_state:q.states[step-1],
  working_state:q.steps[step-1]?.action||'Check the original',after_state:q.states[step]||`Checked: ${q.verify}`}},phase);
}
test('each of 15 worked questions has staged, question-specific mathematical objects',()=>{
 assert.equal(questions.length,15);
 assert.equal(new Set(questions.map(q=>q.model.family)).size,5);
 for(const q of questions){
  const initial=render(q,'ready'),operation=render(q,'operation'),result=render(q,'result');
  assert.notEqual(initial,operation,q.id);assert.notEqual(operation,result,q.id);
  assert.match(initial,/is-concealed/,q.id);assert.match(initial,new RegExp(`data-question-id="${q.id}"`));
  assert.ok(!initial.includes(q.model.outputs[0]),q.id);
  assert.match(operation,/Apply this rule/,q.id);
  assert.match(result,/Result of this arrow/,q.id);
  assert.ok(render(q,'result',q.steps.length+1).includes(q.model.outputs.at(-1)),q.id);
  for(let n=1;n<=q.model.inputs.length;n++)assert.ok(initial.includes(`data-object-id="given-${n}"`),q.id);
  for(let n=1;n<=q.model.outputs.length;n++)assert.ok(initial.includes(`data-object-id="derived-${n}"`),q.id);
 }
});
test('distinct input data changes the diagram while reverse, table and context keep their own layouts',()=>{
 const flow=questions.find(q=>q.model.family==='function_flow');
 const changed={...flow,model:{...flow.model,inputs:['input 19','multiply by 6']}};
 assert.notEqual(render(flow,'ready'),render(changed,'ready'));
 assert.match(render(questions.find(q=>q.model.family==='function_reverse'),'operation'),/function-ex-flow/);
 assert.match(render(questions.find(q=>q.model.family==='function_table'),'ready'),/function-ex-table/);
 assert.match(render(questions.find(q=>q.model.family==='function_context'),'ready'),/function-ex-context/);
 assert.match(render(questions.find(q=>q.model.family==='function_compare'),'ready'),/function-ex-parallel/);
});
test('a two-arrow flow reveals the intermediate output before the final output',()=>{
 const q=questions[1];
 assert.equal(q.model.outputs.length,2);
 const first=render(q,'result',1),next=render(q,'ready',2),second=render(q,'result',2);
 assert.ok(first.includes(q.model.outputs[0]));
 assert.ok(!first.includes(q.model.outputs[1]));
 assert.ok(next.includes(q.model.outputs[0]));
 assert.ok(!next.includes(q.model.outputs[1]));
 assert.ok(second.includes(q.model.outputs[1]));
});
