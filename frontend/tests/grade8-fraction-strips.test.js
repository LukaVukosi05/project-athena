const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
global.escapeWhiteboardHtml=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const registry={};global.AthenaVisualizationRegistry={register:(t,n,v)=>registry[`${t}:${n}`]=v};
vm.runInThisContext(fs.readFileSync(path.join(__dirname,'../js/visualization/fractions/grade8-fraction-strips.js'),'utf8'));
const render=registry['algebra:grade8_fraction_strips'].render;
for(const n of [1,2])test(`Fractions ${n}: 15 question-specific partition states, hidden answers and retained reasoning`,()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(__dirname,`../../docs/curriculum/grade8/common-fractions/lesson-0${n}-scenes.json`))).scenes;
 assert.equal(scenes.length,15);
 for(const s of scenes){
  const p={scene_json:JSON.stringify(s),question_id:s.id,prompt:s.problem,total_steps:5};
  const state=k=>({annotations:[`stage:${k}`],before_state:'Original',working_state:'Change units',after_state:`Stage ${k}`});
  const initial=render(p,state(1),'ready'),operation=render(p,state(2),'operation'),partition=render(p,state(2),'result'),next=render(p,state(3),'result'),final=render(p,state(5),'result');
  assert.ok(initial.includes('data-object-id="model"'));
  assert.ok(!initial.includes(`Answer: ${s.answer}`));
  assert.notEqual(initial,operation);assert.notEqual(operation,partition);
  assert.ok(next.includes('data-object-id="equal-parts-1"'));
  assert.ok(final.includes(`Answer: ${AthenaFractionNotation.html(s.answer)}`));
  assert.ok(initial.includes(AthenaFractionNotation.html(s.problem)));
  for(const fraction of s.values){
   assert.ok(initial.includes(`aria-label="${AthenaFractionNotation.speech(fraction)}"`));
  }
  for(let i=1;i<=s.values.length;i++)assert.ok(initial.includes(`data-object-id="fraction-${i}"`));
 }
});
test('fraction notation shows a true stacked fraction, a mixed number and escaped text',()=>{
 const simple=AthenaFractionNotation.html('Do 2/3 and 6/9 match?');
 assert.match(simple,/<mfrac><mn>2<\/mn><mn>3<\/mn><\/mfrac>/);
 assert.match(simple,/<mfrac><mn>6<\/mn><mn>9<\/mn><\/mfrac>/);
 assert.doesNotMatch(simple,/>2\/3</);
 const mixed=AthenaFractionNotation.html('1 3/4 and <unsafe>');
 assert.match(mixed,/<mn>1<\/mn><mspace width="0.2em"\/><mfrac>/);
 assert.match(mixed,/&lt;unsafe&gt;/);
 assert.ok(!mixed.includes('<unsafe>'));
 assert.match(AthenaFractionNotation.html('0/0'),/0\/0/);
});
test('fraction strip labels use numerator, bar and denominator',()=>{
 const scene=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/curriculum/grade8/common-fractions/lesson-01-scenes.json'))).scenes[0];
 const p={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
 const state=k=>({annotations:[`stage:${k}`],working_state:'',after_state:''});
 const initial=render(p,state(1),'ready'),parts=render(p,state(3),'result');
 assert.match(initial,/<text[^>]*>2<\/text><line[^>]*><text[^>]*>3<\/text>/);
 assert.match(initial,/<text[^>]*>6<\/text><line[^>]*><text[^>]*>9<\/text>/);
 assert.ok(!initial.includes('>2/3<'));
 assert.match(parts,/data-object-id="equal-parts-1"/);
});
