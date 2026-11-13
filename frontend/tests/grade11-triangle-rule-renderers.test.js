const assert=require('assert'),fs=require('fs'),vm=require('vm'),path=require('path');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registrations=new Map();global.AthenaVisualizationRegistry={register:(type,template,renderer)=>registrations.set(`${type}:${template}`,renderer)};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/geometry/grade11-triangle-rule-renderers.js'),'utf8'));
let count=0;
for(let n=1;n<=5;n++){
  const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/triangle_rules_${String(n).padStart(2,'0')}.json`),'utf8'));
  const renderer=registrations.get(`trigonometry:grade11_rules_${n}`);assert.ok(renderer);
  for(const scene of bank.worked){
    const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
    const initial=renderer.render(p,{annotations:[]},'ready');
    const operation=renderer.render(p,{annotations:['stage:1'],working_state:scene.actions[0]},'operation');
    const final=renderer.render(p,{annotations:['stage:5'],after_state:scene.actions[4]},'result');
    assert.ok(initial.includes(scene.id)&&initial.includes('<svg')&&initial.includes('g11-rules-side'));
    assert.ok(!initial.includes('g11-rules-answer')&&!initial.includes('g11-rules-branch'));
    assert.ok(operation.includes(scene.actions[0]));
    assert.ok(final.includes('data-object-id="verification"')&&final.includes('g11-rules-answer'));
    if(scene.visual.values.mode==='ambiguous')assert.ok(renderer.render(p,{annotations:['stage:4']},'result').includes('g11-rules-branch'));
    if(scene.visual.values.mode.startsWith('proof_'))assert.ok(renderer.render(p,{annotations:['stage:2']},'result').includes('g11-rules-altitude'));
    count++;
  }
}
assert.strictEqual(count,75);console.log(`Grade 11 triangle rules: ${count} question-specific constructions passed`);
