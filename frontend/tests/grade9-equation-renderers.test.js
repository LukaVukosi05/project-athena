const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');const path=require('node:path');const vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),renderers={};
vm.runInNewContext(fs.readFileSync(path.join(root,'frontend/js/visualization/algebra/grade9-equation-renderers.js'),'utf8'),{
  AthenaVisualizationRegistry:{register:(type,name,renderer)=>renderers[`${type}:${name}`]=renderer},
  escapeWhiteboardHtml:value=>String(value).replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]))
});
test('each of 90 question-owned equation diagrams reveals a new stage without early answer',()=>{
  for(let n=1;n<=6;n++){
    const bank=JSON.parse(fs.readFileSync(path.join(root,`backend/app/curriculum/grade9/generated/equations_${String(n).padStart(2,'0')}.json`),'utf8'));
    assert.equal(bank.worked.length,15);
    for(const scene of bank.worked){
      const renderer=renderers[`algebra:grade9_equation_${n}`];assert.ok(renderer);
      const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:scene.actions.length};
      const state=(at)=>({annotations:[`stage:${at}`],working_state:scene.actions[at-1],after_state:scene.actions[at-1]});
      const initial=renderer.render(params,state(1),'initial');
      const operation=renderer.render(params,state(2),'operation');
      const final=renderer.render(params,state(scene.actions.length),'result');
      assert.match(initial,/data-object-id="model"/);assert.match(operation,/data-object-id="operation"/);
      assert.match(final,/data-object-id="verification"/);
      assert.notEqual(initial,operation,scene.id);assert.notEqual(operation,final,scene.id);
      assert.doesNotMatch(initial,/class="g9-eq-verification">[^<]+</,scene.id);
      const sanitized={...scene,visual:{family:'givens'}};
      delete sanitized.answer;delete sanitized.actions;delete sanitized.check;
      const preview=renderer.render({...params,scene_json:JSON.stringify(sanitized)},state(1),'initial');
      assert.match(preview,/g9-eq-givens/);assert.doesNotMatch(preview,/undefined|NaN/);
    }
  }
});
