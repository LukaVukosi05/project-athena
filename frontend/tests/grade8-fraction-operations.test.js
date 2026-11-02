const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,v)=>registry[`${t}:${n}`]=v};
for(const name of ['grade8-fraction-strips.js','grade8-fraction-operations.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/fractions',name),'utf8'));
const render=registry['algebra:grade8_fraction_operations'].render;
for(const n of [3,4])test(`Fraction lesson ${n}: 15 operation-specific visuals with hidden initial answers`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/common-fractions/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const scene of scenes){
  const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
  const state=k=>({annotations:[`stage:${k}`],working_state:'Repartition',after_state:`Stage ${k}`});
  const initial=render(p,state(1),'ready'),working=render(p,state(2),'operation'),model=render(p,state(3),'result'),final=render(p,state(5),'result');
  assert.ok(!initial.includes(`Answer: ${scene.answer}.`));
  assert.notEqual(initial,working);assert.notEqual(working,model);
  assert.ok(final.includes('data-object-id="verification"'));
  assert.ok(final.includes(`Answer: ${AthenaFractionNotation.html(scene.answer)}`));
  for(const id of ['problem','model','fraction-1','fraction-2','operation','result','verification'])assert.ok(initial.includes(`data-object-id="${id}"`));
  assert.ok(initial.includes(AthenaFractionNotation.html(scene.problem)));
  assert.ok(model.includes('<svg') && model.includes('stroke'));
 }
});
test('group count changes with original divisor and multiplication uses original quantities',()=>{
 const scene={id:'q',kind:'divide',values:['3/4','1/2'],common_denominator:4,answer:'1 1/2',rows:['one','two','three'],memo:'check',problem:'How many halves fit in 3/4?'};
 const state={annotations:['stage:4'],working_state:'count',after_state:'result'};
 const a=render({scene_json:JSON.stringify(scene),question_id:'q',prompt:scene.problem,total_steps:5},state,'result');
 scene.values[1]='1/4';scene.common_denominator=4;
 const b=render({scene_json:JSON.stringify(scene),question_id:'q',prompt:scene.problem,total_steps:5},state,'result');
 assert.notEqual(a,b);
 assert.ok(a.includes('One group uses 2'));
 assert.ok(b.includes('One group uses 1'));
});
test('all counter coordinates stay within the viewBox and fractional collections have exact shares',()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/common-fractions/lesson-03-scenes.json'))).scenes;
 for(const scene of scenes){
  const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
  const markup=render(p,{annotations:['stage:3'],working_state:'select',after_state:'selected'},'result');
  const height=Number(/viewBox="0 0 540 (\d+)"/.exec(markup)[1]);
  for(const [,cy] of markup.matchAll(/<circle cx="[^"]+" cy="([\d.]+)"/g))assert.ok(Number(cy)+13<height,scene.id);
 }
 const fractional=scenes.find(s=>s.values[0]==='7/12'&&s.values[1]==='18');
 const p={scene_json:JSON.stringify(fractional),question_id:fractional.id,prompt:fractional.problem,total_steps:5};
 const model=render(p,{annotations:['stage:3'],working_state:'select',after_state:'selected'},'result');
 assert.ok(model.includes('width="210"') || model.includes('width="208"'));
 assert.ok(model.includes('Each share is 18 ÷ 12 counters'));
});
