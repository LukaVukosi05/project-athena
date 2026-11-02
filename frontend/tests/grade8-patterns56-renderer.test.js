const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderers={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>renderers[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/patterns/grade8-pattern-renderer.js'),'utf8'));
const render=renderers['algebra:grade8_pattern_board'].render;
for(const n of [5,6])test(`Lesson ${n}: all fifteen questions test or repair their actual pattern`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/numeric-geometric-patterns/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const scene of scenes){
  const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:4};
  const state=k=>({annotations:[`stage:${k}`],before_state:'Read',working_state:'Compare',after_state:`Verified ${scene.answer}`});
  const ready=render(p,state(1),'ready'),working=render(p,state(4),'operation'),result=render(p,state(4),'result');
  assert.match(ready,/data-object-id="model"/);assert.match(ready,/data-object-id="term-4"/);
  assert.match(ready,/data-object-id="target-slot">\?<\/td>/);
  assert.match(result,/data-object-id="verification"/);
  assert.ok(result.includes(`>${scene.answer}</td>`),scene.id);
  assert.notEqual(ready,working);assert.notEqual(working,result);
  if(n===5){assert.match(ready,/Rule A:/);assert.match(ready,/Rule B:/);assert.ok(working.includes('disagrees with the given'));}
  else {assert.ok(ready.includes(`Learner claim: T(${scene.target_position}) = ${scene.claimed}`));
   assert.ok(!ready.includes('Rebuilt rule:'));assert.ok(working.includes(`Rebuilt rule: T(n) = ${global.escapeWhiteboardHtml(scene.rule)}`));}
 }
});
