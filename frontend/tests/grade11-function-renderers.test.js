const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderers={};
global.AthenaVisualizationRegistry={register:(type,name,definition)=>renderers[`${type}:${name}`]=definition};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/functions/grade11-function-renderers.js'),'utf8'));

test('120 question-owned functions draw distinct parent, transform and feature stages',()=>{
  let count=0;
  for(let n=1;n<=8;n++){
    const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/functions_${String(n).padStart(2,'0')}.json`)));
    for(const scene of bank.worked){
      const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
      const renderer=renderers[`function_graph:grade11_fn_${n}`];
      const initial=renderer.render(p,{annotations:['stage:1']},'ready');
      const parent=renderer.render(p,{annotations:['stage:1'],after_state:'step 1'},'result');
      const transformed=renderer.render(p,{annotations:['stage:3'],after_state:'step 3'},'result');
      const final=renderer.render(p,{annotations:['stage:5'],after_state:scene.check},'result');
      assert.ok(initial.includes('viewBox="0 0 550 380"'));
      assert.ok(!initial.includes('g11-fn-parent') && !initial.includes('g11-fn-curve'));
      assert.ok(parent.includes('g11-fn-parent') && !parent.includes('g11-fn-curve'));
      assert.ok(transformed.includes('g11-fn-curve'));
      assert.ok(final.includes(escapeWhiteboardHtml(scene.check)));
      assert.ok(final!==transformed);
      count++;
    }
  }
  assert.equal(count,120);
});

test('tangent and hyperbola never draw a continuous path over a pole',()=>{
  for(const [n,mode] of [[2,'hyperbola'],[5,'trig_point']]){
    const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/functions_${String(n).padStart(2,'0')}.json`)));
    const scene=bank.worked.find(q=>q.visual.values.mode===mode && (n===2||q.visual.values.fn==='tan'));
    assert.ok(scene);
    const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
    const html=renderers[`function_graph:grade11_fn_${n}`].render(p,{annotations:['stage:2']},'result');
    assert.ok((html.match(/class="g11-fn-curve"/g)||[]).length>=2,scene.id);
  }
});
