const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const root=path.resolve(__dirname,"..");
const registry=new Map();
const context={
  escapeWhiteboardHtml:value=>String(value).replace(/[&<>"']/g,
    char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char])),
  AthenaVisualizationRegistry:{register:(type,template,renderer)=>registry.set(type+":"+template,renderer)}
};
vm.runInNewContext(fs.readFileSync(path.join(root,"js/visualization/algebra/grade11-exponents-surds-renderers.js"),"utf8"),context);
for(let n=1;n<=6;n++){
  const bank=JSON.parse(fs.readFileSync(path.join(root,`../backend/app/curriculum/grade11/generated/exponents_surds_${String(n).padStart(2,"0")}.json`),"utf8"));
  const renderer=registry.get(`algebra:grade11_es_${n}`);
  assert.ok(renderer);
  for(const scene of bank.worked){
    const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
    const state=stage=>({annotations:[`stage:${stage}`],working_state:scene.actions[stage-1],after_state:scene.actions[stage-1]});
    const initial=renderer.render(params,state(1),"ready");
    assert.ok(initial.includes(context.escapeWhiteboardHtml(scene.problem)),scene.id);
    assert.ok(!initial.includes('data-object-id="verification"') || initial.includes('data-object-id="verification"></p>'),scene.id);
    assert.ok(!initial.includes('data-object-id="check"'),scene.id);
    const operation=renderer.render(params,state(2),"operation");
    const result=renderer.render(params,state(5),"result");
    assert.notEqual(initial,operation);
    assert.notEqual(operation,result);
    assert.ok(result.includes('data-object-id="verification"'));
    assert.throws(()=>renderer.render({...params,question_id:"wrong"},state(1),"ready"));
  }
}
console.log("Grade 11 question-specific exponents and surds visuals passed");
