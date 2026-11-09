const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const root=path.resolve(__dirname,".."),registry=new Map();
const escape=value=>String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const context={escapeWhiteboardHtml:escape,AthenaVisualizationRegistry:{register:(type,name,renderer)=>registry.set(type+":"+name,renderer)}};
vm.runInNewContext(fs.readFileSync(path.join(root,"js/visualization/geometry/grade11-trigonometry-renderers.js"),"utf8"),context);
let count=0;
for(let n=1;n<=7;n++){
  const bank=JSON.parse(fs.readFileSync(path.join(root,`../backend/app/curriculum/grade11/generated/trigonometry_${String(n).padStart(2,"0")}.json`),"utf8"));
  const renderer=registry.get(`algebra:grade11_tr_${n}`);
  assert.ok(renderer);
  for(const scene of bank.worked){
    const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
    const state=i=>({annotations:[`stage:${i}`],working_state:scene.actions[i-1],after_state:scene.actions[i-1]});
    const ready=renderer.render(params,state(1),"ready");
    const working=renderer.render(params,state(3),"operation");
    const final=renderer.render(params,state(5),"result");
    assert.ok(ready.includes(escape(scene.problem)),scene.id);
    assert.ok(ready.includes('data-object-id="verification"></p>'),scene.id);
    assert.ok(ready.includes('data-object-id="result"></p>'),scene.id);
    assert.notEqual(ready,working,scene.id);
    assert.notEqual(working,final,scene.id);
    assert.ok(final.includes(escape(scene.answer)),scene.id);
    assert.throws(()=>renderer.render({...params,question_id:"wrong"},state(1),"ready"));
    count++;
  }
}
const q=JSON.parse(fs.readFileSync(path.join(root,"../backend/app/curriculum/grade11/generated/trigonometry_02.json"),"utf8")).worked;
const renderer=registry.get("algebra:grade11_tr_2");
const draw=scene=>renderer.render({scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem},
  {annotations:["stage:3"],working_state:"step",after_state:"step"},"result");
assert.notEqual(draw(q[0]),draw(q[1]),"a new angle changes the SVG ray and reference construction");
assert.equal(count,105);
assert.match(fs.readFileSync(path.join(root,"lesson.html"),"utf8"),/grade11-trigonometry-renderers\.js\?v=g11-tr-v1/);
console.log("Grade 11 unit-circle stages and exact-question renders passed");
