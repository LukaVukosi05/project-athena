const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../js/visualization/algebra/grade8-relationship-compare.js'),'utf8');
const registry=new Map(),ctx={AthenaVisualizationRegistry:{register:(type,family,renderer)=>registry.set(family,renderer)},escapeWhiteboardHtml:v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))};
vm.runInNewContext(source,ctx);
const root=path.join(__dirname,'../../backend/app/curriculum/grade8/generated');
for(const n of [5,6])test(`Lesson ${n} paths use the question values and conceal the result until teaching`,()=>{
  const data=JSON.parse(fs.readFileSync(path.join(root,`functions_relationships_0${n}.json`),'utf8'));
  const renderer=registry.get(n===5?'relationship_match':'relationship_repair');
  assert.ok(renderer);
  const outputs=new Set();
  for(const item of data.worked_examples){
    const p={question_id:item.id,prompt:item.q,total_steps:4,given_objects:item.model.inputs,derived_objects:item.model.outputs,scene_json:JSON.stringify(item.model.scene)};
    const ready=renderer.render(p,{annotations:['stage:0'],before_state:item.states[0]},'ready');
    const operation=renderer.render(p,{annotations:['stage:1'],before_state:item.states[0],working_state:item.steps[0].action},'operation');
    const result=renderer.render(p,{annotations:['stage:4'],before_state:item.states[3],working_state:'Verify',after_state:item.verify},'result');
    assert.notEqual(ready,operation);assert.notEqual(operation,result);
    assert.match(ready,/data-object-id="problem"/);assert.doesNotMatch(ready,/is-chosen/);
    assert.match(result,/is-chosen/);assert.match(result,/data-object-id="verification"/);
    assert.match(result,new RegExp(`data-question-id="${item.id}"`));
    outputs.add(item.model.scene.candidates.map(c=>c.value).join(':'));
  }
  assert.ok(outputs.size>10,'Question-specific paths must vary across examples');
});
