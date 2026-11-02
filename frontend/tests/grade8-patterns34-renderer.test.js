const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderers={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>renderers[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/patterns/grade8-pattern-renderer.js'),'utf8'));
const render=renderers['algebra:grade8_pattern_board'].render;
for(const n of [3,4])test(`Lesson ${n}: 15 question-specific aligned tables reveal only the taught result`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/numeric-geometric-patterns/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const s of scenes){
  const p={scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:4};
  const state=k=>({annotations:[`stage:${k}`],before_state:'Read',working_state:'Compute',after_state:`Verified ${s.answer}`});
  const ready=render(p,state(1),'ready'),operation=render(p,state(3),'operation'),final=render(p,state(4),'result');
  assert.match(ready,/Position n/);assert.match(ready,/Output T\(n\)/);
  assert.match(ready,/data-object-id="model"/);assert.match(final,/data-object-id="verification"/);
  assert.notEqual(ready,operation);assert.notEqual(operation,final);
  if(n===3){assert.ok(!ready.includes(`T(n) = ${s.answer}`),s.id);assert.ok(final.includes(`T(n) = ${s.answer}`),s.id);}
  else{assert.match(ready,/data-object-id="target-slot"[^>]*>\?<\/td>/);assert.ok(final.includes(`>${s.answer}</td>`),s.id);}
 }
});
