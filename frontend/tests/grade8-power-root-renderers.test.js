const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-power-root-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_06.json'),'utf8')).worked_examples;
function render(item,phase,step=1){
 const block={representation:'visual',id:`${item.id}-board`,visualization:{type:'algebra',template:item.model.family,
  parameters:{prompt:item.q,question_id:item.id,model_tokens:item.model.tokens,model_scene:item.model.scene,total_steps:item.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-algebraic-expressions-06',question_id:item.id});
 assert.ok(session.instruction,`${item.id} template not registered`);
 return session.render({visualization_state:{annotations:[`stage:${step}`],
   before_state:item.states[step-1],working_state:item.steps[step-1]?.action||'Check original',
   after_state:item.states[step]||`Checked: ${item.verify}`}},phase);
}
test('all 15 visuals are question-specific, targetable and keep answers hidden initially',()=>{
 assert.equal(questions.length,15);
 for(const q of questions){
  const ready=render(q,'ready'),working=render(q,'operation'),result=render(q,'result');
  assert.ok(!ready.includes('Diagram unavailable'),q.id);
  assert.ok(!ready.includes(q.states.at(-1)),q.id);
  assert.notEqual(ready,working,q.id);assert.notEqual(working,result,q.id);
  assert.ok(result.includes(`data-question-id="${q.id}"`));
  for(let n=1;n<=q.model.tokens.length;n++)
   assert.equal((ready.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,q.id);
  assert.ok(ready.includes('is-concealed'),q.id);
  assert.ok(result.includes('data-object-id="result"'),q.id);
 }
});
test('sign scope, factor pairs, negative test, cube and paired roots show distinct cases',()=>{
 assert.match(render(questions[4],'ready'),/Minus inside the square/);
 assert.match(render(questions[4],'ready'),/Minus outside the square/);
 assert.match(render(questions[8],'ready'),/Principal root/);
 assert.ok(render(questions[8],'ready').includes('√(a²) gives |a|'));
 assert.ok(!render(questions[11],'ready').includes('4|x|'));
 assert.ok(render(questions[11],'result',3).includes('4|x|'));
 assert.match(render(questions[12],'ready'),/Three factors in each cube group/);
 assert.match(render(questions[14],'ready'),/Square-root branch/);
 assert.match(render(questions[14],'ready'),/Cube-root branch/);
 assert.notEqual(render(questions[8],'ready'),render(questions[9],'ready'));
});
