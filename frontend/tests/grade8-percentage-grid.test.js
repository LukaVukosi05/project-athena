const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,v)=>registry[`${t}:${n}`]=v};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/fractions/grade8-percentage-grid.js'),'utf8'));
const render=registry['algebra:grade8_percentage_grid'].render;
for(const n of [7,8])test(`Percentage lesson ${n}: 15 question-specific progressive visual states`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/common-fractions/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const scene of scenes){
  const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
  const state=k=>({annotations:[`stage:${k}`],working_state:`Action ${k}`,after_state:`State ${k}`});
  const ready=render(p,state(1),'ready'),model=render(p,state(2),'result'),worked=render(p,state(4),'result'),final=render(p,state(5),'result');
  assert.ok(!ready.includes('Answer:'));assert.ok(ready.includes('data-object-id="model"'));
  assert.notEqual(ready,model);assert.notEqual(model,worked);assert.ok(final.includes('Answer: '));
  assert.ok(!ready.includes('NaN')&&!worked.includes('NaN'));
  assert.ok(worked.includes('Worked solution so far'));
 }
});
test('large percentages and decrease use appropriate original-amount visuals',()=>{
 const seven=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/common-fractions/lesson-07-scenes.json'))).scenes;
 const eight=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/common-fractions/lesson-08-scenes.json'))).scenes;
 const s=seven.find(x=>x.values[0]==='17/8'),p={scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:5};
 assert.ok(render(p,{annotations:['stage:3'],working_state:'',after_state:''},'result').includes('2 complete hundred(s)'));
 const q=eight.find(x=>x.kind==='decrease'),params={scene_json:JSON.stringify(q),question_id:q.id,prompt:q.problem,total_steps:5};
 assert.ok(render(params,{annotations:['stage:2'],working_state:'',after_state:''},'result').includes('Original amount is the 100% reference'));
});
