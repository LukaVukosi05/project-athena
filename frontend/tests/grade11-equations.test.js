const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const root=path.resolve(__dirname,".."),registry=new Map();
const escape=value=>String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const context={escapeWhiteboardHtml:escape,AthenaVisualizationRegistry:{register:(type,template,renderer)=>registry.set(type+":"+template,renderer)}};
vm.runInNewContext(fs.readFileSync(path.join(root,"js/visualization/algebra/grade11-equations-renderers.js"),"utf8"),context);
for(let n=1;n<=7;n++){
  const bank=JSON.parse(fs.readFileSync(path.join(root,`../backend/app/curriculum/grade11/generated/equations_inequalities_${String(n).padStart(2,"0")}.json`),"utf8"));
  const renderer=registry.get(`algebra:grade11_ei_${n}`);
  assert.ok(renderer);
  for(const scene of bank.worked){
    const parameters={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
    const state=s=>({annotations:[`stage:${s}`],working_state:scene.actions[s-1],after_state:scene.actions[s-1]});
    const initial=renderer.render(parameters,state(1),"ready");
    const middle=renderer.render(parameters,state(3),"operation");
    const final=renderer.render(parameters,state(5),"result");
    assert.ok(initial.includes(escape(scene.problem)),scene.id);
    assert.ok(initial.includes('data-object-id="result"></p>'),scene.id);
    assert.ok(initial.includes('data-object-id="verification"></p>'),scene.id);
    assert.notEqual(initial,middle,scene.id);
    assert.notEqual(middle,final,scene.id);
    assert.ok(final.includes(escape(scene.answer))||final.includes(escape(scene.actions[4])),scene.id);
    assert.throws(()=>renderer.render({...parameters,question_id:"another"},state(1),"ready"));
  }
}
const lesson=fs.readFileSync(path.join(root,"lesson.html"),"utf8");
assert.match(lesson,/grade11-equations-renderers\.js\?v=g11-ei-v1/);
console.log("Grade 11 equation scenes reveal mathematical steps on question-specific models");
