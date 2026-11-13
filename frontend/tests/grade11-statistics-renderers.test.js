const assert=require('assert'),fs=require('fs'),vm=require('vm'),path=require('path');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registrations=new Map();global.AthenaVisualizationRegistry={register:(type,template,renderer)=>registrations.set(`${type}:${template}`,renderer)};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/statistics/grade11-statistics-renderers.js'),'utf8'));
let count=0;
for(let n=1;n<=7;n++){
  const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/statistics_${String(n).padStart(2,'0')}.json`),'utf8'));
  const renderer=registrations.get(`statistics:grade11_stat_${n}`);assert.ok(renderer);
  for(const scene of bank.worked){
    const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
    const initial=renderer.render(p,{annotations:[]},'ready');
    const operation=renderer.render(p,{annotations:['stage:1'],working_state:scene.actions[0]},'operation');
    const final=renderer.render(p,{annotations:['stage:5'],after_state:scene.actions[4]},'result');
    assert.ok(initial.includes(scene.id)&&initial.includes('<svg'));
    assert.ok(!initial.includes('g11-stat-answer-label')&&!initial.includes('g11-stat-box')&&!initial.includes('g11-stat-poly'));
    assert.ok(operation.includes(scene.actions[0]));
    assert.ok(final.includes('data-object-id="verification"')&&final.includes('g11-stat-answer-label'));
    if(scene.visual.values.mode==='box')assert.ok(renderer.render(p,{annotations:['stage:4']},'result').includes('g11-stat-box'));
    if(scene.visual.values.mode==='ogive')assert.ok(renderer.render(p,{annotations:['stage:3']},'result').includes('g11-stat-ogive'));
    if(scene.visual.values.mode==='scatter'){
      const first=renderer.render(p,{annotations:['stage:1']},'result');
      const fourth=renderer.render(p,{annotations:['stage:4']},'result');
      assert.strictEqual((first.match(/g11-stat-point/g)||[]).length,2);
      assert.strictEqual((fourth.match(/g11-stat-point/g)||[]).length,6);
      assert.ok(fourth.includes('<path d="M ')&&fourth.includes('class="g11-stat-poly"'));
    }
    count++;
  }
}
assert.strictEqual(count,105);console.log(`Grade 11 Statistics: ${count} question-specific graphical constructions passed`);
