const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-table-rules-renderers.js'])
 vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/functions_relationships_03.json'),'utf8')).worked_examples;
function render(q,phase,step=1){
 const block={representation:'visual',id:`${q.id}-board`,visualization:{type:'algebra',template:q.model.family,
  parameters:{prompt:q.q,question_id:q.id,given_objects:q.model.inputs,derived_objects:q.model.outputs,
   input_values:q.model.rows.map(r=>r[0]),output_values:q.model.rows.map(r=>r[1]===null?'?':r[1]),
   resolved_outputs:q.model.resolved_outputs,output_reveal_steps:q.model.output_reveal_steps,
   total_steps:q.steps.length+1}}};
 const session=AthenaVisualizationResolver.resolve(block,{lesson_id:'g8-functions-relationships-03',question_id:q.id});
 assert.ok(session.instruction,q.id);
 return session.render({visualization_state:{annotations:[`stage:${step}`],before_state:q.states[step-1],
  working_state:q.steps[step-1]?.action||'Check original',after_state:q.states[step]||`Checked: ${q.verify}`}},phase);
}
test('every authored table has semantic rows, concealed results and changing states',()=>{
 assert.equal(questions.length,15);assert.equal(new Set(questions.map(q=>q.model.family)).size,6);
 for(const q of questions){
  const ready=render(q,'ready'),operation=render(q,'operation'),result=render(q,'result');
  assert.notEqual(ready,operation,q.id);assert.notEqual(operation,result,q.id);
  assert.match(ready,/is-concealed/,q.id);assert.ok(!ready.includes(q.model.outputs.at(-1)),q.id);
  assert.ok(ready.includes(`data-question-id="${q.id}"`));
  assert.match(operation,/Action on this table/,q.id);
  assert.ok(render(q,'result',q.steps.length+1).includes(q.model.outputs.at(-1)),q.id);
  for(let i=1;i<=q.model.rows.length;i++){
   assert.ok(ready.includes(`data-object-id="input-${i}"`),q.id);
   assert.ok(ready.includes(`data-object-id="output-${i}"`),q.id);
  }
  for(let i=1;i<=q.model.inputs.length;i++)assert.ok(ready.includes(`data-object-id="given-${i}"`),q.id);
 }
});
test('actual numerical input/output rows and gaps determine visual states',()=>{
 const q=questions[4],first=render(q,'ready');
 assert.ok(first.includes('>11</span>'),q.id);
 assert.ok(first.includes('>?</span>'),q.id);
 assert.ok(!first.includes('Δx 2, Δy 8'));
 assert.ok(render(q,'result').includes('Δx 2, Δy 8'));
 const altered={...q,model:{...q.model,rows:[[0,2],[2,15],[3,null],[4,25]]}};
 assert.notEqual(first,render(altered,'ready'));
 assert.match(render(questions[6],'ready'),/rules-square/);
 assert.match(render(questions[2],'ready'),/rules-signs/);
 assert.match(render(questions[9],'ready'),/costs retain their stated units/);
 const multi=questions[7];
 assert.ok(render(multi,'result',1).includes(multi.model.outputs[0]));
 assert.ok(render(multi,'ready',2).includes(multi.model.outputs[0]));
});
test('every adjacent change is explained together, and solved outputs enter the table at their teaching step',()=>{
 const signed=questions[2];
 assert.match(render(signed,'ready',1),/data-object-id="output-1">\?<\/span>/);
 assert.match(render(signed,'result',1),/data-object-id="output-1">1<\/span>/);
 assert.match(render(signed,'result',1),/data-object-id="output-2">\?<\/span>/);
 assert.match(render(signed,'result',3),/data-object-id="output-3">9<\/span>/);
 assert.match(render(signed,'result',3),/Δx 2, Δy 4/);
 const zero=questions[3];
 const first=render(zero,'result',1);
 assert.match(first,/data-object-id="delta-2"[^>]*>Δx 1, Δy 3<\/span>/);
 assert.match(first,/data-object-id="delta-3"[^>]*>Δx 1, Δy 3<\/span>/);
 assert.match(first,/data-object-id="output-1">\?<\/span>/);
 assert.match(render(zero,'result',2),/data-object-id="output-1">4<\/span>/);
 assert.match(render(zero,'result',2),/data-object-id="delta-1"[^>]*>Δx 1, Δy 3<\/span>/);
 const nextReady=render(zero,'ready',2),nextOperation=render(zero,'operation',2);
 for(const markup of [nextReady,nextOperation]){
  assert.match(markup,/data-object-id="delta-2"[^>]*>Δx 1, Δy 3<\/span>/);
  assert.match(markup,/data-object-id="delta-3"[^>]*>Δx 1, Δy 3<\/span>/);
 }
 assert.match(render(zero,'operation',1),/data-object-id="delta-2"[^>]*>Δx 1, Δy 3<\/span>/);
 assert.doesNotMatch(render(zero,'operation',1),/data-object-id="delta-3"[^>]*>Δx 1, Δy 3<\/span>/);
 assert.match(nextReady,/data-object-id="output-1">\?<\/span>/);
 assert.match(render(zero,'ready',3),/data-object-id="output-1">4<\/span>/);
 assert.match(render(zero,'operation',3),/data-object-id="output-1">4<\/span>/);
 assert.equal(zero.states[1],'Both known output gaps are three for one input step');
 assert.equal(zero.states[2],'Undo one step from x=1: 7−3=4 at x=0');
 for(const q of questions){
  const final=render(q,'result',q.steps.length+1);
  q.model.rows.forEach((row,i)=>{
   const solved=q.model.resolved_outputs?.[i];
   if(solved!==null&&solved!==undefined)assert.ok(final.includes(`data-object-id="output-${i+1}">${solved}</span>`),q.id);
  });
  for(let step=2;step<=q.steps.length+1;step++){
   const previous=render(q,'result',step-1),ready=render(q,'ready',step),working=render(q,'operation',step);
   for(let i=1;i<q.model.rows.length;i++){
    const cell=new RegExp(`data-object-id="delta-${i}"[^>]*>([^<]*)<\\/span>`);
    const old=previous.match(cell)?.[1];
    if(old&&old.startsWith('Δx')){
     assert.equal(ready.match(cell)?.[1],old,`${q.id} change ${i} erased at step ${step}`);
     assert.equal(working.match(cell)?.[1],old,`${q.id} change ${i} erased during step ${step}`);
    }
   }
   for(let i=1;i<=q.model.rows.length;i++){
    const cell=new RegExp(`data-object-id="output-${i}">([^<]*)<\\/span>`);
    const old=previous.match(cell)?.[1];
    if(old&&old!=='?'){
     assert.equal(ready.match(cell)?.[1],old,`${q.id} output ${i} erased at step ${step}`);
     assert.equal(working.match(cell)?.[1],old,`${q.id} output ${i} erased during step ${step}`);
    }
   }
  }
 }
});
