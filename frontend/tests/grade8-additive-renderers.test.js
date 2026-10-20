const {test}=require("node:test"), assert=require("node:assert/strict"),fs=require("node:fs"),path=require("node:path"),vm=require("node:vm");
const root=path.resolve(__dirname,"../..");
global.escapeWhiteboardHtml=value=>String(value).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
for(const file of ["visualization-registry.js","algebra/grade8-additive-renderers.js"])
  vm.runInThisContext(fs.readFileSync(path.join(root,"frontend/js/visualization",file),"utf8"));
const examples=JSON.parse(fs.readFileSync(path.join(root,"backend/app/curriculum/grade8/generated/lesson_03.json"),"utf8")).worked_examples;
const family={"algebra:additive_inverse":"additive_balance","algebra:inspection_number_line":"additive_number_line","algebra:inspection_context":"additive_context"};
const state=(before,working,after,index)=>({before_state:before,working_state:working,after_state:after,annotations:[`stage:${index}`]});

test("all 15 approved questions have question-specific initial, operation, and result states",()=>{
  for(const item of examples){
    const renderer=AthenaVisualizationRegistry.resolve("algebra",family[item.renderer]);
    const params={prompt:item.prompt,question_id:item.id,source_data:item.question_data,total_steps:4};
    const before=state(item.prompt,"Select inverse",item.answer,1);
    const initial=renderer.render(params,before,"initial");
    const operation=renderer.render(params,before,"operation");
    const result=renderer.render(params,before,"result");
    assert.ok(initial.includes(item.prompt));assert.ok(initial.includes(`data-question-id="${item.id}"`));
    assert.notEqual(initial,operation);assert.notEqual(operation,result);
    assert.ok(!initial.includes(`>${item.answer}</strong>`),item.id);
    for(const target of ["problem","operation","result","verification","left-expression","right-expression","balance-beam","inverse-operation","left-operation","right-operation","cancellation"])
      assert.ok(result.includes(`data-object-id="${target}"`),`${item.id}: ${target}`);
  }
});

test("signed number lines and contexts use the current question's values",()=>{
  const line=AthenaVisualizationRegistry.resolve("algebra","additive_number_line");
  const a=examples[2],b=examples[3];
  const render=item=>line.render({prompt:item.prompt,question_id:item.id,source_data:item.question_data,total_steps:4},state(item.prompt,"jump",item.answer,3),"result");
  assert.notEqual(render(a),render(b));assert.ok(render(a).includes("−8") || render(a).includes("-8"));
  const ctx=AthenaVisualizationRegistry.resolve("algebra","additive_context");
  const receipt=ctx.render({prompt:examples[12].prompt,question_id:examples[12].id,source_data:examples[12].question_data,total_steps:4},state("p + 35 = 284","Subtract 35", "p = R249",3),"result");
  assert.ok(receipt.includes("R35")&&receipt.includes("R284")&&receipt.includes("R249"));
});
