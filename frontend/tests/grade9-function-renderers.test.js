const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','functions/grade9-function-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization',file),'utf8'));
for(let number=1;number<=5;number++){
 const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade9/generated/functions_0${number}.json`),'utf8'));
 const renderer=AthenaVisualizationRegistry.resolve('algebra',`grade9_function_${number}`);
 assert.equal(data.worked.length,15);
 for(const scene of data.worked){
  const args={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.actions.length};
  const at=(n,phase='result')=>renderer.render(args,{annotations:[`stage:${n}`],working_state:scene.actions[n-1],after_state:scene.actions[n-1]},phase);
  const initial=at(0),first=at(1),second=at(2),third=at(3),last=at(4);
  assert.ok(initial.includes('data-object-id="model"')&&!initial.includes(`Result: ${scene.answer}`),scene.id);
  assert.notEqual(initial,first,scene.id);assert.notEqual(first,second,scene.id);
  assert.notEqual(second,third,scene.id);assert.notEqual(third,last,scene.id);
  assert.ok(last.includes(`Result: ${scene.answer}`),scene.id);
  for(const target of ['problem','model','operation','result','verification'])assert.ok(initial.includes(`data-object-id="${target}"`),`${scene.id} ${target}`);
  if(scene.visual.family==='graph'){
   assert.ok(initial.includes('<svg')&&!initial.includes('data-point='),scene.id);
   assert.equal((first.match(/data-point=/g)||[]).length,4,scene.id);
   assert.ok(!first.includes('class="g9-fn-line"')&&second.includes('class="g9-fn-line"'),scene.id);
   for(const [x,y] of scene.visual.known_pairs)assert.ok(second.includes(`data-point="${x},${y}"`),scene.id);
  }
  if(scene.visual.family==='flow')assert.ok(initial.includes(`Input<br><strong>${scene.visual.target_input}</strong>`)&&!initial.includes(`Result: ${scene.answer}`),scene.id);
  if(scene.visual.family==='diagnosis')assert.ok(initial.includes('Claim:')&&!initial.includes('Correct rule:'),scene.id);
 }
}
console.log('Five Grade 9 function renderers and 75 question-specific staged models passed');
