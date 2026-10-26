const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-mixed-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_08.json'),'utf8')).worked_examples;
function render(q,phase,step=1){
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,model_tokens:q.model.tokens,model_scene:q.model.scene,total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-algebraic-expressions-08',question_id:q.id});
 assert.ok(session.instruction,`${q.id}: template unavailable`);
 return session.render({visualization_state:{annotations:[`stage:${step}`],
  before_state:q.states[step-1],working_state:q.steps[step-1]?.action||'Check original',
  after_state:q.states[step]||`Checked: ${q.verify}`}},phase);
}
test('all 15 examples have targetable givens and conceal derived terms',()=>{
 assert.equal(questions.length,15);
 for(const q of questions){
  const initial=render(q,'ready'),operation=render(q,'operation'),result=render(q,'result');
  assert.ok(!initial.includes('Diagram unavailable'),q.id);
  assert.notEqual(initial,operation,q.id);assert.notEqual(operation,result,q.id);
  assert.ok(initial.includes('is-concealed'),q.id);
  assert.match(initial,new RegExp(`data-object-id="token-${q.model.tokens.length}"[^>]*><small>Calculated</small><strong>\\?</strong>`),q.id);
  for(let n=1;n<=q.model.tokens.length;n++)
   assert.equal((initial.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,q.id);
  assert.ok(result.includes(`data-question-id="${q.id}"`),q.id);
  assert.ok(render(q,'result',q.steps.length).includes(q.model.tokens.at(-1)),q.id);
 }
});
test('bracket paths, quotient restriction, powers and perimeter stay question-specific',()=>{
 assert.match(render(questions[6],'ready'),/Two independent bracket paths/);
 assert.match(render(questions[8],'ready'),/p≠0/);
 assert.match(render(questions[9],'ready'),/Square term/);
 assert.match(render(questions[11],'ready'),/mixed-rectangle/);
 assert.match(render(questions[11],'ready'),/length: x\+4 cm/);
 assert.match(render(questions[10],'ready'),/Learner claim/);
 const changed={...questions[11],id:'g8-ex-l08-w12',q:'Rectangle with length y+5 cm and width 3y cm',model:{...questions[11].model,tokens:['length: y+5 cm','width: 3y cm','P=2(l+w)','8y+10 cm','34 cm']}};
 assert.notEqual(render(changed,'ready'),render(questions[11],'ready'));
 assert.ok(!render(questions[11],'ready').includes('24 cm'));
});
