const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-diagnostic-expressions-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_10.json'),'utf8')).worked_examples;
function render(q,phase,step=1){
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,model_tokens:q.model.tokens,model_scene:q.model.scene,total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-algebraic-expressions-10',question_id:q.id});
 assert.ok(session.instruction,`${q.id}: registered renderer required`);
 return session.render({visualization_state:{annotations:[`stage:${step}`],
  before_state:q.states[step-1],working_state:q.steps[step-1]?.action||'Check the original',
  after_state:q.states[step]||`Checked: ${q.verify}`}},phase);
}
test('15 distinct diagnosis templates show given quantities without premature answers',()=>{
 assert.equal(questions.length,15);
 assert.equal(new Set(questions.map(q=>q.model.family)).size,15);
 for(const q of questions){
  assert.match(q.model.family,/^diagnostic_/);
  const initial=render(q,'ready'),action=render(q,'operation'),result=render(q,'result');
  assert.notEqual(initial,action,q.id);assert.notEqual(action,result,q.id);
  assert.match(initial,/is-concealed/,q.id);
  assert.ok(!initial.includes('Checked conclusion</span><strong>Checked:'),q.id);
  assert.ok(initial.includes(`data-question-id="${q.id}"`),q.id);
  assert.ok(!initial.includes(q.model.tokens.at(-1)),q.id);
  assert.match(action,/Apply this legal operation/,q.id);
  assert.match(result,/Result of this operation/,q.id);
  assert.ok(render(q,'result',q.steps.length).includes(q.model.tokens.at(-1)),q.id);
  for(let n=1;n<=q.model.tokens.length;n++) assert.equal((initial.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,q.id);
 }
});
test('question values alter the diagram and earlier lesson templates remain separate',()=>{
 assert.match(render(questions[3],'ready'),/diagnostic-ex-arrows/);
 assert.match(render(questions[12],'ready'),/diagnostic-ex-shape/);
 assert.match(render(questions[13],'ready'),/Path A/);
 assert.match(render(questions[13],'ready'),/Path B/);
 assert.match(render(questions[10],'ready'),/divisor 3a/);
 const changed={...questions[12],q:'A rectangle is y+5 by 7.',model:{...questions[12].model,tokens:['length y+5','width 7','y=2','claim wrong','result 7y+35']}};
 assert.notEqual(render(changed,'ready'),render(questions[12],'ready'));
 assert.ok(!AthenaVisualizationRegistry.manifest().includes('algebra:distribution_paths'));
});
