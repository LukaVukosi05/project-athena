const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','numbers/grade9-whole-number-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization',file),'utf8'));
const base=path.join(__dirname,'../../backend/app/curriculum/grade9/generated');
for(const [n,template] of [[1,'grade9_number_sets'],[2,'grade9_prime_factors']]){
  const scenes=JSON.parse(fs.readFileSync(path.join(base,`whole_numbers_0${n}.json`),'utf8')).worked;
  assert.equal(scenes.length,15);
  for(const scene of scenes){
    const render=AthenaVisualizationRegistry.resolve('algebra',template);
    const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.actions.length};
    const before=render.render(params,{annotations:['stage:1'],before_state:'Read the original question'},'ready');
    const middle=render.render(params,{annotations:[`stage:${Math.ceil(scene.actions.length/2)}`],working_state:'Apply the next action'},'result');
    const final=render.render(params,{annotations:[`stage:${scene.actions.length}`],after_state:scene.check},'result');
    assert.ok(before.includes(scene.problem.replace(/&/g,'&amp;')));
    assert.notEqual(before,middle,scene.id);
    assert.notEqual(middle,final,scene.id);
    assert.ok(!before.includes('Smallest set:') && !before.includes('Check:'),scene.id);
    assert.ok(final.includes('data-object-id="verification"'),scene.id);
    if(n===2)assert.ok(scene.numbers.every(v=>final.includes(String(v))),scene.id);
  }
}
const first=JSON.parse(fs.readFileSync(path.join(base,'whole_numbers_02.json'),'utf8')).worked;
const one=first[2],two=first[3],renderer=AthenaVisualizationRegistry.resolve('algebra','grade9_prime_factors');
const draw=s=>renderer.render({scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:s.actions.length},{annotations:[`stage:${s.actions.length}`],after_state:s.check},'result');
assert.notEqual(draw(one),draw(two));
const comparisons=JSON.parse(fs.readFileSync(path.join(base,'whole_numbers_01.json'),'utf8')).worked;
const sets=AthenaVisualizationRegistry.resolve('algebra','grade9_number_sets');
for(const [index,primary,secondary,primarySet,secondarySet] of [[7,'√2','√4','I','N'],[9,'π','22/7','I','Q'],[14,'√(−9)','−√9','outside','Z']]){
  const scene=comparisons[index],params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.actions.length};
  const at=stage=>sets.render(params,{annotations:[`stage:${stage}`],after_state:scene.actions[stage-1]},'result');
  const initial=at(0),early=at(scene.primary_stage),late=at(scene.secondary_stage),end=at(scene.actions.length);
  assert.ok(initial.includes(primary) && initial.includes(secondary),scene.id);
  assert.ok(!initial.includes('Smallest set for'),scene.id);
  assert.ok(early.includes(`Smallest set for ${primary}:`),scene.id);
  assert.ok(late.includes(`data-set="${secondarySet}"`),scene.id);
  assert.ok(end.includes(`${secondary}:`),scene.id);
  assert.ok(end.includes(`data-set="${primarySet}"`) || primarySet==='outside',scene.id);
  assert.ok(!end.includes('π and 22/7</strong>'),scene.id);
}
console.log('Grade 9 source-specific sets and factor-tree rendering passed');
