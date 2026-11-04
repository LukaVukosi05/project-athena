const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','exponents/grade9-exponent-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization',file),'utf8'));
for(let number=1;number<=6;number++){
 const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade9/generated/exponents_0${number}.json`),'utf8'));
 assert.equal(data.worked.length,15);
 const renderer=AthenaVisualizationRegistry.resolve('algebra',`grade9_exponent_${number}`);
 for(const scene of data.worked){
  const count=scene.actions.length,args={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:count};
  const at=(n,phase='result')=>renderer.render(args,{annotations:[`stage:${n}`],working_state:scene.actions[n-1],after_state:scene.actions[n-1]},phase);
  const initial=at(0),middle=at(2),last=at(count);
  assert.ok(initial.includes('data-object-id="model"'),scene.id);
  assert.ok(!initial.includes(`Result: ${scene.answer}`),scene.id);
  assert.ok(!initial.includes('Check:'),scene.id);
  assert.notEqual(initial,middle,scene.id);assert.notEqual(middle,last,scene.id);
  assert.ok(last.includes(`Result: ${scene.answer.includes("/")?"<span class=\"g9-exp-fraction\"":scene.answer}`),scene.id);
  for(const target of ['problem','model','operation','result','verification'])assert.ok(initial.includes(`data-object-id="${target}"`),`${scene.id} ${target}`);
  if(scene.visual.family==='reciprocal'&&scene.visual.operator==='negative')assert.ok(last.includes('g9-exp-fraction'),scene.id);
  if(scene.visual.family==='diagnosis')assert.ok(!initial.includes('Corrected result: '+scene.answer),scene.id);
 }
}
console.log('Six Grade 9 exponent renderers, 90 source-owned scenes and staged results passed');
