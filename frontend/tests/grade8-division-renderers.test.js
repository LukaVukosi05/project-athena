const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-division-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_05.json'),'utf8')).worked_examples;
function render(q,phase,stage=1){
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,model_tokens:q.model.tokens,model_lanes:q.model.lanes,total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{question_id:q.id});
 assert.ok(session.instruction,`${q.id} visual missing`);
 return session.render({visualization_state:{annotations:[`stage:${stage}`],
   before_state:q.states[stage-1],working_state:q.steps[stage-1]?.action||'Check original',
   after_state:q.states[stage]||`Checked: ${q.verify}`}},phase);
}
test('all 15 division diagrams use current question objects and hide the final answer',()=>{
 assert.equal(data.length,15);
 for(const q of data){
  const initial=render(q,'ready'),operation=render(q,'operation'),result=render(q,'result');
  assert.ok(!initial.includes('Diagram unavailable'),q.id);
  assert.ok(!initial.includes(q.states.at(-1)),`${q.id} reveals result early`);
  assert.notEqual(initial,operation,q.id);assert.notEqual(operation,result,q.id);
  assert.ok(result.includes(`data-question-id="${q.id}"`),q.id);
  for(let n=1;n<=q.model.tokens.length;n++)
   assert.equal((initial.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,q.id);
 }
});
test('signed terms, restrictions, diagnostic claim and paired quotients have distinct scenes',()=>{
 assert.equal((render(data[6],'ready').match(/class="division-lane"/g)||[]).length,3);
 assert.equal((render(data[6],'operation',1).match(/is-drawn/g)||[]).length,3);
 assert.equal((render(data[6],'ready',2).match(/is-drawn/g)||[]).length,3);
 assert.match(render(data[9],'ready'),/excludes zero/);
 assert.match(render(data[11],'ready'),/claim: 3x\+8/);
 assert.equal((render(data[13],'ready').match(/data-division-group="(?:first|second)"/g)||[]).length,2);
 assert.match(render(data[10],'ready'),/Each equal group/);
 assert.equal((render(data[0],'ready').match(/data-share-group=/g)||[]).length,3);
 assert.equal((render(data[10],'ready').match(/data-share-group=/g)||[]).length,6);
 assert.ok(!render(data[11],'ready').includes('data-diagnosis="undivided-constant"'));
 assert.ok(render(data[11],'result',3).includes('data-diagnosis="undivided-constant"'));
 assert.match(render(data[13],'operation',2),/division-group is-active" data-division-group="second"/);
});
