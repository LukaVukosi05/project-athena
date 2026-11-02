const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderers={};global.AthenaVisualizationRegistry={register:(type,name,renderer)=>renderers[`${type}:${name}`]=renderer};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/numbers/grade8-integer-renderer.js'),'utf8'));
const render=renderers['algebra:grade8_integer_board'].render;
for(const n of [1,2])test(`Integers Lesson ${n}: fifteen question-specific axes and ordered states`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/integers/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const s of scenes){
  const p={scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:s.actions.length};
  const state=k=>({annotations:[`stage:${k}`],before_state:'Read',working_state:'Move',after_state:`Verified ${s.answer}`});
  const initial=render(p,state(1),'ready'),operation=render(p,state(2),'operation'),final=render(p,state(p.total_steps),'result');
  assert.match(initial,/data-object-id="model"/);assert.match(initial,/data-object-id="problem"/);
  assert.match(final,/data-object-id="verification"/);assert.ok(final.includes(`Answer: ${s.answer}`),s.id);
  assert.notEqual(initial,operation);assert.notEqual(operation,final);
  assert.ok(!initial.includes(`Answer: ${s.answer}`),s.id);
  if(n===2){
   assert.ok(!initial.includes('data-object-id="jump-1"'));
   for(let j=1;j<=s.operations.length;j++){
    const html=render(p,state(j+2),'result');
    assert.ok(html.includes(`data-object-id="jump-${j}"`),s.id);
    if(j>1)assert.ok(html.includes(`data-object-id="jump-${j-1}"`),s.id);
   }
  }
 }
});
