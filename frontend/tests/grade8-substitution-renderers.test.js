const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-substitution-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_07.json'),'utf8')).worked_examples;
function render(q,phase,step=1){
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,model_tokens:q.model.tokens,model_scene:q.model.scene,total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-algebraic-expressions-07',question_id:q.id});
 assert.ok(session.instruction,`${q.id}: template unavailable`);
 return session.render({visualization_state:{annotations:[`stage:${step}`],
  before_state:q.states[step-1],working_state:q.steps[step-1]?.action||'Check original',
  after_state:q.states[step]||`Checked: ${q.verify}`}},phase);
}
test('every example has its own targetable inputs and hides its calculated output',()=>{
 assert.equal(questions.length,15);
 for(const q of questions){
  const initial=render(q,'ready'),operation=render(q,'operation'),result=render(q,'result');
  assert.ok(!initial.includes('Diagram unavailable'),q.id);
  assert.notEqual(initial,operation,q.id);assert.notEqual(operation,result,q.id);
  assert.ok(initial.includes('is-concealed'),q.id);
  assert.ok(initial.includes(`data-object-id="token-${q.model.tokens.length}"><small>Calculated value</small><strong>?</strong>`),q.id);
  for(let n=1;n<=q.model.tokens.length;n++)
   assert.equal((initial.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,q.id);
  assert.ok(result.includes(`data-question-id="${q.id}"`),q.id);
  assert.ok(render(q,'result',q.steps.length).includes(q.model.tokens.at(-1)),q.id);
 }
});
test('signed inputs, two variables, denominator cases and perimeter have distinct scenes',()=>{
 assert.match(render(questions[3],'ready'),/First expression/);
 assert.match(render(questions[3],'ready'),/Second expression/);
 assert.match(render(questions[5],'ready'),/Separate variable slots/);
 assert.match(render(questions[9],'ready'),/First denominator/);
 assert.match(render(questions[9],'ready'),/Second denominator/);
 assert.match(render(questions[9],'ready'),/zero denominator/);
 assert.match(render(questions[13],'ready'),/substitution-rectangle/);
 assert.match(render(questions[13],'ready'),/width=x\+1 cm/);
 assert.match(render(questions[11],'ready'),/Second expression/);
 assert.ok(!render(questions[12],'ready').includes('Repaired result</strong><div class="substitution-cards"><div class="substitution-card substitution-card--output is-visible"'));
});
