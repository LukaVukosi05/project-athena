const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');

global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const renderers={};
global.AthenaVisualizationRegistry={register:(type,name,definition)=>renderers[`${type}:${name}`]=definition};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade11-euclidean-renderers.js'),'utf8'));

test('120 circle diagrams use their question values and reveal one cumulative stage',()=>{
  let count=0;
  for(let n=1;n<=8;n++){
    const source=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/euclidean_${String(n).padStart(2,'0')}.json`)));
    for(const scene of source.worked){
      const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
      const renderer=renderers[`geometry:grade11_euc_${n}`];
      const before=renderer.render(p,{annotations:['stage:1']},'ready');
      const middle=renderer.render(p,{annotations:['stage:3'],after_state:'step 3'},'result');
      const final=renderer.render(p,{annotations:['stage:5'],after_state:scene.check},'result');
      assert.match(before,/viewBox="0 0 500 335"/);
      assert.ok(!before.includes('g11-euc-derived'),scene.id);
      assert.ok(middle!==before && final!==middle,scene.id);
      assert.ok(final.includes('data-object-id="verification"'));
      assert.ok(final.includes(escapeWhiteboardHtml(scene.check)));
      count++;
    }
  }
  assert.equal(count,120);
});
