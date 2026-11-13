const test=require('node:test'), assert=require('node:assert/strict'), fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registrations=new Map();global.AthenaVisualizationRegistry={register:(type,name,renderer)=>registrations.set(`${type}:${name}`,renderer)};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/probability/grade11-probability-renderers.js'),'utf8'));

test('105 original Probability examples preserve question-owned givens and reveal five diagram stages',()=>{
  let count=0;const families=new Set();
  for(let n=1;n<=7;n++){
    const bank=JSON.parse(fs.readFileSync(path.join(__dirname,`../../backend/app/curriculum/grade11/generated/probability_${String(n).padStart(2,'0')}.json`),'utf8'));
    const renderer=registrations.get(`statistics:grade11_prob_${n}`);assert.ok(renderer);
    for(const scene of bank.worked){
      families.add(scene.visual.values.mode);
      const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem};
      const initial=renderer.render(params,{annotations:['stage:1']},'ready');
      const first=renderer.render(params,{annotations:['stage:1'],after_state:scene.actions[0]},'result');
      const fourth=renderer.render(params,{annotations:['stage:4'],after_state:scene.actions[3]},'result');
      const final=renderer.render(params,{annotations:['stage:5'],after_state:scene.actions[4]},'result');
      assert.match(initial,/<svg/);assert.ok(initial.includes(scene.id));
      assert.ok(!initial.includes(scene.answer),'answer leaked before the first step');
      assert.notEqual(first,initial);assert.notEqual(fourth,first);assert.notEqual(final,fourth);
      assert.ok(initial.includes('data-object-id="model"'));
      assert.ok(final.includes('data-object-id="verification"'));
      assert.ok(final.includes(scene.actions[4].replaceAll('&','&amp;'))||final.includes(scene.actions[4]));
      const a=scene.visual.values;
      if(a.mode==='venn2'&&n===2){assert.ok(!initial.includes('g11-prob-region'));assert.ok(first.includes('g11-prob-region'));}
      if(a.mode==='tree'){assert.ok(!initial.includes('RR'));assert.ok(fourth.includes('RR'));}
      if(a.mode==='table'){assert.ok(!initial.includes('g11-prob-cell'));assert.ok(fourth.includes('g11-prob-cell'));}
      assert.throws(()=>renderer.render({...params,question_id:'another-question'},{annotations:[]},'ready'));
      count++;
    }
  }
  assert.equal(count,105);
  assert.deepEqual([...families].sort(),['frequency','independence','table','tree','venn2','venn3']);
});
