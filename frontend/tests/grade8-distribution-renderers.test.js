const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-distribution-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_04.json'),'utf8')).worked_examples;
const render=(q,phase,stage=1)=>{
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,model_tokens:q.model.tokens,model_lanes:q.model.lanes,model_scene:q.model.scene,total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{question_id:q.id});
 assert.ok(session.instruction,`${q.id}: renderer missing`);
 return session.render({visualization_state:{annotations:[`stage:${stage}`],before_state:q.states[stage-1],working_state:q.steps[stage-1]?.action||'Check original',after_state:q.states[stage]||`Checked: ${q.verify}`}},phase);
};
test('all 15 authored visual scenarios resolve without fallback or premature answers',()=>{
 assert.equal(questions.length,15);
 for(const q of questions){
  const ready=render(q,'ready'),operation=render(q,'operation'),result=render(q,'result');
  assert.ok(!ready.includes('Diagram unavailable'),q.id);
  assert.ok(!ready.includes(q.states.at(-1)),`${q.id}: final answer leaked`);
  assert.notEqual(ready,operation,q.id);assert.notEqual(operation,result,q.id);
  assert.ok(result.includes(`data-question-id="${q.id}"`),q.id);
  for(let n=1;n<=q.model.tokens.length;n++)assert.equal((ready.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,q.id);
 }
});
test('question-specific group boundaries and split areas are retained',()=>{
 assert.equal((render(questions[10],'result').match(/data-object-id="region-/g)||[]).length,2);
 assert.equal((render(questions[14],'ready').match(/class="distribution-group"/g)||[]).length,2);
 assert.ok(render(questions[13],'ready').includes('claim: 2x+3'));
 const q=questions[0],ready=render(q,'ready');
 assert.ok(!ready.includes('distribution-term--reached'));
 assert.ok(render(q,'operation').includes('distribution-term--reached'));
 const three=questions[6];
 assert.equal((render(three,'operation',1).match(/class="distribution-term distribution-term--reached"/g)||[]).length,3);
 assert.equal((render(three,'ready',2).match(/class="distribution-term distribution-term--reached"/g)||[]).length,3);
});
