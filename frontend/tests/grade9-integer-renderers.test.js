const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','numbers/grade9-integer-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization',file),'utf8'));
for(let number=1;number<=5;number++){
 const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade9/generated/integers_0${number}.json`),'utf8'));
 assert.equal(data.worked.length,15);
 const renderer=AthenaVisualizationRegistry.resolve('algebra',`grade9_integer_${number}`);
 for(const scene of data.worked){
  const count=scene.actions.length,args={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:count};
  const at=(n,phase='result')=>renderer.render(args,{annotations:[`stage:${n}`],working_state:scene.actions[n-1],after_state:scene.actions[n-1]},phase);
  const initial=at(0),middle=at(2),last=at(count);
  assert.ok(initial.includes('data-object-id="model"'),scene.id);
  assert.ok(!initial.includes(`Result: ${scene.answer}`),scene.id);
  assert.ok(!initial.includes('Check:'),scene.id);
  assert.notEqual(initial,middle,scene.id);assert.notEqual(middle,last,scene.id);
  assert.ok(last.includes(`Result: ${scene.answer}`),scene.id);
  for(const target of ['problem','model','operation','result','verification'])assert.ok(initial.includes(`data-object-id="${target}"`),`${scene.id} ${target}`);
  if(scene.visual.family==='line')assert.ok(initial.includes('<svg')&&initial.includes('viewBox'),scene.id);
  if(scene.visual.family==='diagnosis')assert.ok(!initial.includes('Corrected result: '+scene.answer),scene.id);
 }
}
console.log('Five Grade 9 integer renderers, 75 source-owned scenes and staged results passed');
