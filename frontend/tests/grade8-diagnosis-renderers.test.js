const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-diagnosis-renderers.js'])vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const questions=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/lesson_10.json'))).worked_examples;
const template=q=>'diagnosis_'+q.renderer.split(':')[1]+'_native';
const render=(q,phase='initial',n=1,total=10)=>AthenaVisualizationRegistry.resolve('algebra',template(q)).render({prompt:q.prompt,question_id:q.id,source_data:q.question_data,total_steps:total},{before_state:q.prompt,working_state:'Inspect the next operation',after_state:'Mathematical result',annotations:[`stage:${n}`]},phase);
test('all 15 cases select ten native diagnostic models and reveal mathematics in order',()=>{
  assert.equal(questions.length,15);assert.equal(new Set(questions.map(template)).size,10);
  for(const q of questions){
    const initial=render(q),working=render(q,'operation'),result=render(q,'result',3);
    assert.notEqual(initial,working,q.id);assert.notEqual(working,result,q.id);
    assert.ok(!initial.includes(`<strong>${escapeWhiteboardHtml(q.answer)}</strong>`),q.id);
    for(const id of ['problem','operation','result','verification','fraction-1','fraction-2','denominator'])
      assert.ok(result.includes(`data-object-id="${id}"`),`${q.id}: ${id}`);
  }
});
test('the visual models use their current question data, not fixed picture labels',()=>{
  const fare=questions[13],changed={...fare,question_data:fare.question_data.replace('fixed_fee = 20','fixed_fee = 31').replace('rate = 5','rate = 8')};
  assert.ok(render(fare).includes('R20'));assert.ok(render(changed).includes('R31'));assert.ok(render(changed).includes('R8'));
  const box=render(questions[9],'result',3);assert.ok(box.includes('<rect'));assert.ok(box.includes('x + 2'));assert.ok(box.includes('2(x + 2) + 2x = 24'));
  assert.ok(render(questions[10],'result',3).includes('Always true'));
  assert.ok(render(questions[11],'result',3).includes('Always false'));
  const bracket=render(questions[6],'result',2);assert.ok(bracket.includes('3 × (-2)'));
  assert.ok(!render(questions[6]).includes('3 × (-2)'));
});
