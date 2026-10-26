const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-products-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_03.json'),'utf8')).worked_examples;
function render(item,phase,step=1){
 const state={annotations:[`stage:${step}`],before_state:item.states[step-1],working_state:item.steps[step-1]?.action||item.verify,after_state:item.states[step]||`Checked: ${item.verify}`};
 return AthenaVisualizationRegistry.resolve('algebra',item.model.family).render({prompt:item.q,question_id:item.id,model_tokens:item.model.tokens,model_lanes:item.model.lanes,model_scene:item.model.scene,total_steps:4},state,phase);
}
test('every product has targetable given factors and distinct initial, action and result',()=>{
 assert.equal(questions.length,15);
 for(const q of questions){const before=render(q,'initial'),working=render(q,'operation'),after=render(q,'result');
  assert.notEqual(before,working,q.id);assert.notEqual(working,after,q.id);
  assert.ok(!before.includes(q.states[1]),q.id);
  for(let n=1;n<=q.model.tokens.length;n++)assert.equal((after.match(new RegExp(`data-object-id="token-${n}"`,'g'))||[]).length,1,q.id);
  assert.ok(after.includes('data-object-id="operation"')&&after.includes('data-object-id="result"'),q.id);
 }
});
test('area, signs, zero groups, powers and two-area comparison use question data',()=>{
 assert.equal((render(questions[0],'result').match(/class="product-area-cell /g)||[]).length,6);
 assert.ok(render(questions[7],'result').includes('Zero groups'));
 assert.equal((render(questions[10],'result').match(/class="product-area-cell /g)||[]).length,12);
 assert.ok(render(questions[12],'result').includes('Each item costs R2'));
 assert.equal((render(questions[14],'result').match(/class="product-area-cell /g)||[]).length,7);
 assert.ok(render(questions[5],'result').includes('product-sign-badge'));
 assert.equal((render(questions[13],'result').match(/class="product-power-chip"/g)||[]).length,2);
 assert.ok(!render(questions[3],'initial').includes('product-area-cell'));
 assert.ok(render(questions[3],'result').includes('x²'));
});
test('the lesson page loads the product renderer and every authored product resolves without fallback',()=>{
 const html=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');
 assert.match(html,/js\/visualization\/algebra\/grade8-products-renderers\.js\?v=g8-ex-l03-v2/);
 assert.match(html,/js\/whiteboard\/animation-registry\.js\?v=math-whiteboard-v17/);
 for(const q of questions){
  const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,parameters:{prompt:q.q,question_id:q.id,model_tokens:q.model.tokens,model_lanes:q.model.lanes,model_scene:q.model.scene,total_steps:4}}};
  const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-algebraic-expressions-03',question_id:q.id});
  assert.ok(session.instruction,`${q.id}: template was not registered`);
  const step={visualization_state:{annotations:['stage:4'],before_state:q.states.at(-1),working_state:q.steps.at(-1).action,after_state:`Checked: ${q.verify}`}};
  const markup=session.render(step,'result');
  assert.ok(markup.includes(`data-question-id="${q.id}"`),`${q.id}: wrong diagram`);
  assert.ok(!markup.includes('Diagram unavailable'),`${q.id}: renderer fell back`);
 }
});
