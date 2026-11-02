const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderers={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>renderers[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/numbers/grade8-whole-number-renderer.js'),'utf8'));
const render=renderers['algebra:grade8_whole_number_board'].render;
for(const n of [1,2])test(`Whole Numbers Lesson ${n}: question-specific states and hidden result`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/whole-numbers/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const scene of scenes){
  const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.actions.length};
  const state=k=>({annotations:[`stage:${k}`],before_state:'Read',working_state:'Work',after_state:`Verified ${scene.answer}`});
  const first=render(p,state(1),'ready'),operation=render(p,state(2),'operation'),last=render(p,state(p.total_steps),'result');
  assert.match(first,/data-object-id="model"/);assert.match(first,/data-object-id="given-1"/);
  assert.match(last,/data-object-id="verification"/);
  assert.notEqual(first,operation);assert.notEqual(operation,last);
  assert.ok(last.includes(String(scene.answer)),scene.id);
  if(n===1){assert.ok(!first.includes(`Check: ${scene.answer}`));}
  else {
   assert.ok(!first.includes('class="g8-whole-leaves"'));
   const splits=scene.factors[0].length-1;
   for(let j=1;j<=splits;j++){
    const prior=render(p,state(j+1),'result'),next=render(p,state(j+2),'result');
    assert.ok(next.includes(`data-object-id="split-1-${j}"`),scene.id);
    if(j>1)assert.ok(prior.includes(`data-object-id="split-1-${j-1}"`),scene.id);
   }
  }
 }
});
