const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderers={};
global.AthenaVisualizationRegistry={register:(type,name,definition)=>renderers[`${type}:${name}`]=definition};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade11-analytical-renderers.js'),'utf8'));

test('90 coordinate examples plot actual points and retain constructions',()=>{
  let count=0;
  for(let n=1;n<=6;n++){
    const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/analytical_${String(n).padStart(2,'0')}.json`)));
    for(const scene of bank.worked){
      const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
      const renderer=renderers[`coordinate_geometry:grade11_ag_${n}`];
      const initial=renderer.render(p,{annotations:['stage:1']},'ready');
      const operation=renderer.render(p,{annotations:['stage:3'],after_state:'step 3'},'result');
      const result=renderer.render(p,{annotations:['stage:5'],after_state:scene.check},'result');
      assert.match(initial,/viewBox="0 0 540 370"/);
      assert.ok(initial.includes('g11-ag-point'),scene.id);
      assert.ok(!initial.includes('g11-ag-derived'),scene.id);
      assert.ok(operation!==initial && result!==operation,scene.id);
      assert.ok(result.includes(escapeWhiteboardHtml(scene.check)));
      if(n===3 && scene.visual.values.missing){
        assert.ok(initial.includes('g11-ag-midpoint'));
        assert.ok(!initial.includes('>B ('),scene.id);
        assert.ok(result.includes('>B ('),scene.id);
      }
      count++;
    }
  }
  assert.equal(count,90);
});
