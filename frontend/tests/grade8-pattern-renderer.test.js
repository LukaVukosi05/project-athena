const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderers={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>renderers[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/patterns/grade8-pattern-renderer.js'),'utf8'));
const render=renderers['algebra:grade8_pattern_board'].render;
const scenes=[1,2].map(n=>JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/numeric-geometric-patterns/lesson-0${n}-scenes.json`))).scenes);
test('all 30 scenes hide answers, expose semantic targets, and complete question-specific models',()=>{
 for(const group of scenes) for(const scene of group){
  const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:4};
  const state=(n)=>({annotations:[`stage:${n}`],before_state:'Read',working_state:'Count',after_state:`Verified ${scene.answer}`});
  const ready=render(p,state(1),'ready'),operation=render(p,state(2),'operation'),final=render(p,state(4),'result');
  assert.ok(ready.includes('data-object-id="model"')&&ready.includes('data-object-id="operation"'));
  assert.ok(!ready.includes(`>${scene.answer}</strong>`));
  assert.notEqual(ready,operation);assert.notEqual(operation,final);
  assert.ok(final.includes(scene.model==='geometric'?`>${scene.answer} pieces</strong>`:`>${scene.answer}</strong>`),scene.id);
  assert.ok(!final.includes('Pattern figure mismatch'),scene.id);
 }
});
