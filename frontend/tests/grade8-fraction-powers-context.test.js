const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,v)=>registry[`${t}:${n}`]=v};
for(const name of ['grade8-fraction-strips.js','grade8-fraction-powers-context.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/fractions',name),'utf8'));
const render=registry['algebra:grade8_fraction_powers_context'].render;
for(const n of [5,6])test(`Fraction lesson ${n}: 15 distinct progressive models, gated solutions and semantic targets`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/common-fractions/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const scene of scenes){
  const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
  const state=k=>({annotations:[`stage:${k}`],working_state:`Action ${k}`,after_state:`State ${k}`});
  const initial=render(params,state(1),'ready'),partition=render(params,state(2),'result'),work=render(params,state(3),'result'),final=render(params,state(5),'result');
  assert.ok(!initial.includes('Answer:'));
  assert.ok(initial.includes(AthenaFractionNotation.html(scene.problem)));
  assert.notEqual(initial,partition);assert.notEqual(partition,work);
  assert.ok(final.includes(`Answer: ${AthenaFractionNotation.html(scene.answer)}`));
  for(const id of ['problem','model','fraction-1','operation','result','verification'])assert.ok(initial.includes(`data-object-id="${id}"`),`${scene.id}: ${id}`);
  assert.ok(initial.includes('<svg') && !initial.includes('NaN'));
 }
});
test('root layers match positive perfect power and context division shows partial groups',()=>{
 const roots=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/common-fractions/lesson-05-scenes.json'))).scenes;
 const cube=roots.find(s=>s.problem.includes('64/125'));
 const p={scene_json:JSON.stringify(cube),question_id:cube.id,prompt:cube.problem,total_steps:5};
 const visual=render(p,{annotations:['stage:3'],working_state:'construct',after_state:'select'},'result');
 assert.ok(visual.includes('Layer 5'));assert.ok(visual.includes('#3787a9'));
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/common-fractions/lesson-06-scenes.json'))).scenes;
 const share=scenes.find(s=>s.answer==='3/4');const q={scene_json:JSON.stringify(share),question_id:share.id,prompt:share.problem,total_steps:5};
 const ready=render(q,{annotations:['stage:1'],working_state:'',after_state:''},'ready');
 const selected=render(q,{annotations:['stage:3'],working_state:'',after_state:''},'result');
 assert.ok(!ready.includes('Result in litres per learner'));
 assert.ok(selected.includes('Result in litres per learner'));
 assert.ok(selected.includes('width="'));assert.ok(!selected.includes('NaN'));
});
