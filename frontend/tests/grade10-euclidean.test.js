const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const renderers={};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade10-euclidean-renderers.js'),'utf8'),{
 escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;'),
 AthenaVisualizationRegistry:{register:(d,k,r)=>renderers[k]=r}
});
const state=(scene,i)=>({annotations:[`stage:${i}`],working_state:scene.actions[i-1],after_state:scene.actions[i-1]});
test('90 geometry scenes use their own data and reveal markings in sequence',()=>{
 for(let n=1;n<=6;n++){
  const data=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade10/generated/euclidean_${String(n).padStart(2,'0')}.json`)));
  for(const scene of data.worked){
   const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
   const renderer=renderers[`grade10_euc_${n}`];
   const initial=renderer.render(p,state(scene,1),'initial');
   const middle=renderer.render(p,state(scene,3),'result');
   const final=renderer.render(p,state(scene,5),'result');
   assert.ok(initial.includes(scene.id)&&initial.includes('data-object-id="model"'));
   assert.notEqual(initial,middle);assert.notEqual(middle,final);
   assert.ok(!initial.includes('data-object-id="verification">Answer:'));
   assert.ok(final.includes('data-object-id="verification">'));
   assert.ok(!middle.includes('undefined cm')&&!middle.includes('undefined°'));
   assert.throws(()=>renderer.render({...p,question_id:'different'},state(scene,1),'initial'));
  }
 }
});
test('reverse midpoint diagram keeps unknown base hidden until computed',()=>{
 const scene=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade10/generated/euclidean_05.json'))).worked.find(q=>q.visual.values.mode==='reverse');
 const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
 const renderer=renderers.grade10_euc_5;
 const before=renderer.render(p,state(scene,2),'result');
 const after=renderer.render(p,state(scene,4),'result');
 assert.ok(before.includes(`>${scene.visual.values.de} cm<`));
 assert.ok(!before.includes('data-object-id="full-base"'));
 assert.ok(after.includes(`BC = ${scene.visual.values.solution_bc} cm`));
});
test('an angle change rotates the actual marked line',()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,'../../backend/app/curriculum/grade10/generated/euclidean_01.json'))).worked;
 const a=scenes.find(q=>q.visual.values.model==='intersect');
 const b=scenes.find(q=>q.visual.values.model==='intersect' && q.visual.values.given_angle!==a.visual.values.given_angle);
 const p=q=>({scene_json:JSON.stringify(q),question_id:q.id,prompt:q.problem});
 const svg=q=>renderers.grade10_euc_1.render(p(q),state(q,1),'result').match(/data-object-id="CD"[^>]*>/)[0];
 assert.notEqual(svg(a),svg(b));
});
