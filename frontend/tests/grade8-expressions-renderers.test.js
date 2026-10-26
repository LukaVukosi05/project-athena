const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
global.escapeWhiteboardHtml=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const file of ['visualization-registry.js','algebra/grade8-expressions-renderers.js']) vm.runInThisContext(fs.readFileSync(path.join(root,'frontend/js/visualization',file),'utf8'));
const pack=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/algebraic_expressions_01.json'),'utf8'));
const models=[['expression_tiles',['4','x','+7']],['signed_terms',['-3','a','+5']],['signed_terms',['2x','-4y','+9']],['grouped_terms',['n','n','n','+5']],['grouped_terms',['n','n','n','-5']],['fraction_bar',['p','÷2','+7']],['square_comparison',['x = 3','2 × x','x × x']],['like_term_sort',['4x','+2x','-3']],['unlike_term_sort',['2a','+3b','claim: 5ab']],['square_comparison',['-2','x = -3','x × x']],['receipt',['R12 × t passengers','R8 once']],['receipt',['R12 × 5 passengers','R8 once']],['grouped_terms',['x + 3','x + 3','claim: 2x + 3']],['rectangle',['x + 3 cm','x cm','x + 3 cm','x cm']],['grouped_terms',['n + 2','n + 2','n + 2']]];
function render(item,index,phase,overrides={}){
 const [family,tokens]=models[index],state={annotations:['stage:1'],before_state:item.states[0],working_state:item.steps[0][1],after_state:item.states[1]};
 return AthenaVisualizationRegistry.resolve('algebra',family).render({prompt:item.q,question_id:item.id,model_tokens:tokens,total_steps:3,...overrides},state,phase);
}
test('every authored example uses the given objects and reveals one action then result',()=>{
 assert.equal(pack.examples.length,15);
 pack.examples.forEach((item,index)=>{const initial=render(item,index,'initial'),operation=render(item,index,'operation'),result=render(item,index,'result');
  assert.notEqual(initial,operation,item.id);assert.notEqual(operation,result,item.id);
  assert.ok(!initial.includes(item.states[1]),item.id);
  assert.ok(result.includes('data-object-id="operation"') && result.includes('data-object-id="result"'),item.id);
  models[index][1].forEach((token,n)=>assert.ok(result.includes(`data-object-id="token-${n+1}"`),`${item.id}: ${token}`));
 });
});
test('receipt, rectangle and square encode different mathematical scenarios',()=>{
 assert.ok(render(pack.examples[13],13,'result').includes('<rect'));
 assert.ok(render(pack.examples[6],6,'result').includes('expression-grid'));
 assert.ok(render(pack.examples[11],11,'result').includes('R12 × 5 passengers'));
 assert.ok(render(pack.examples[10],10,'result').includes('R12 × t passengers'));
 assert.notEqual(render(pack.examples[11],11,'result'),render(pack.examples[10],10,'result'));
});
