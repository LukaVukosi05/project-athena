const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-contextual-expressions-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_09.json'),'utf8')).worked_examples;
function render(q,phase,step=1){
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,model_tokens:q.model.tokens,model_scene:q.model.scene,total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-algebraic-expressions-09',question_id:q.id});
 assert.ok(session.instruction,`${q.id}: template unavailable`);
 return session.render({visualization_state:{annotations:[`stage:${step}`],
  before_state:q.states[step-1],working_state:q.steps[step-1]?.action||'Check original',
  after_state:q.states[step]||`Checked: ${q.verify}`}},phase);
}
test('all 15 contextual visuals preserve given quantities and hide calculated outputs',()=>{
 assert.equal(questions.length,15);
 for(const q of questions){
  const initial=render(q,'ready'),operation=render(q,'operation'),result=render(q,'result');
  assert.ok(!initial.includes('Diagram unavailable'),q.id);
  assert.notEqual(initial,operation,q.id);assert.notEqual(operation,result,q.id);
  assert.ok(initial.includes('is-concealed'),q.id);
  assert.ok(!initial.includes('context-ex-progress'),q.id);
  assert.match(operation,/Now apply/,q.id);
  assert.match(result,/Current result/,q.id);
  assert.ok(initial.includes(`data-object-id="token-${q.model.tokens.length}"`),q.id);
  for(let n=1;n<=q.model.tokens.length;n++)
   assert.equal((initial.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,q.id);
  assert.ok(result.includes(`data-question-id="${q.id}"`),q.id);
  assert.ok(render(q,'result',q.steps.length).includes(q.model.tokens.at(-1)),q.id);
 }
});
test('tables, ordered flows, geometry and learner claim use their own data',()=>{
 assert.match(render(questions[2],'ready'),/Follow the arrows in order/);
 assert.match(render(questions[3],'ready'),/1 → 5/);
 assert.match(render(questions[7],'ready'),/context-ex-shape/);
 assert.match(render(questions[7],'ready'),/top x\+3 cm/);
 assert.match(render(questions[9],'ready'),/claim T=16d/);
 assert.match(render(questions[12],'ready'),/region 1/);
 assert.match(render(questions[13],'ready'),/Path A/);
 assert.match(render(questions[13],'ready'),/Path B/);
 const changed={...questions[7],q:'Rectangle with sides y+5 and y',model:{...questions[7].model,tokens:['top y+5','right y','bottom y+5','left y','P=4y+10','y=2 → 18']}};
 assert.notEqual(render(changed,'ready'),render(questions[7],'ready'));
 assert.ok(!render(questions[7],'ready').includes('P=4x+6 cm'));
});
