const test=require("node:test"),assert=require("node:assert/strict"),fs=require("node:fs"),vm=require("node:vm"),path=require("node:path");
function registryFor(file){const registered=new Map(),context={AthenaVisualizationRegistry:{register(type,template,renderer){registered.set(`${type}:${template}`,renderer);}},escapeWhiteboardHtml(value){return String(value).replace(/[&<>\"]/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[char]));}};vm.runInNewContext(fs.readFileSync(path.join(__dirname,"../js/visualization",file),"utf8"),context);return registered;}

test("native sequence templates consume question values and expose semantic targets",()=>{
 const registry=registryFor("sequences/sequence-renderer.js"),renderer=registry.get("sequences:term_rows");
 const parameters={title:"Arithmetic",method:"Use nth term",working_lines:["T_6=27"],answer:"103",objects:["left-side","equals","right-side","operation","result","verification"],positions:[1,2,3,4,5,6],terms:[7,11,15,19,23,27],differences:[4,4,4,4,4],second_differences:[0,0,0,0],partial_sums:[7,18,33,52,75,102]};
 const initial=renderer.render(parameters,{annotations:["visual-stage:0"]},"ready"),operation=renderer.render(parameters,{annotations:["visual-stage:1"]},"operation"),result=renderer.render(parameters,{annotations:["visual-stage:3"]},"result");
 assert.notEqual(initial,operation);assert.notEqual(operation,result);for(const value of [7,11,15,19,23,27])assert.match(result,new RegExp(`>${value}<`));for(const id of parameters.objects)assert.match(result,new RegExp(`data-object-id="${id}"`));
});

test("data studio and geometry renderers use their current question parameters",()=>{
 const stats=registryFor("statistics/statistics-renderers.js").get("statistics:data_studio");
 const common={population:"all Grade 12 learners",variable_type:"quantitative continuous",display:"histogram",objects:["source","method","evidence"],title:"Study"};
 const travel=stats.render({...common,sample_size:44,variable:"travel time"},{annotations:["visual-stage:1"]},"result"),siblings=stats.render({...common,sample_size:53,variable:"number of siblings",variable_type:"quantitative discrete",display:"bar chart"},{annotations:["visual-stage:1"]},"result");
 assert.match(travel,/sample n=44/);assert.match(travel,/travel time/);assert.notEqual(travel,siblings);
 const geometry=registryFor("analytical-geometry/analytical-geometry-renderers.js").get("coordinate_geometry:coordinate_proof_studio");
 const polygon=geometry.render({x_values:[2,6,6,2],y_values:[4,4,6,6],labels:["A","B","C","D"],values:[2,4,6],result:"rectangle",objects:["source","method","evidence"],title:"Proof"},{annotations:["visual-stage:1"]},"result");
 assert.match(polygon,/proof-polygon/);assert.match(polygon,/fill="none"/);assert.match(polygon,/A\(2, 4\)/);assert.match(polygon,/D\(2, 6\)/);
});

test("Grade 8 equation families are native, question-specific and stateful",()=>{
 const registry=registryFor("algebra/grade8-equation-renderers.js"),templates=["equality_balance","additive_inverse","multiplicative_inverse","two_step_balance","variables_both_sides","context_to_equation","distributive_equation"];
 assert.deepEqual([...registry.keys()].sort(),templates.map(name=>`algebra:${name}`).sort());
 for(const template of templates){
 const renderer=registry.get(`algebra:${template}`),parameters={prompt:`${template} question`,source_data:`${template} exact values`,question_id:"g8-ae-l01-w01"},initial=renderer.render(parameters,{objects:["stage-00"],highlights:[],annotations:["stage:0"]},"ready"),operation=renderer.render(parameters,{objects:["stage-00","stage-01"],highlights:["stage-01"],annotations:["stage:1"]},"operation"),result=renderer.render(parameters,{objects:["stage-00","stage-01","stage-02"],highlights:["stage-02"],annotations:["stage:2"]},"result");
  const state={objects:["problem","left-expression","right-expression","operation","result","verification"],highlights:["left-expression"],annotations:["stage:2","action:evaluate_expression","phase:operation"],target:"left-expression",before_state:"7 + 5 = 9 + 3",working_state:"7 + 5 → 12",after_state:"12 = 9 + 3"};
  const ready=renderer.render(parameters,state,"ready"),working=renderer.render(parameters,state,"operation"),settled=renderer.render(parameters,state,"result");
  assert.notEqual(ready,working);assert.notEqual(working,settled);assert.match(settled,new RegExp(template.replaceAll("_","-")));assert.match(settled,/data-object-id="problem"/);for(const id of ["left-expression","right-expression","operation","result","verification"])assert.match(settled,new RegExp(`data-object-id="${id}"`));
  assert.match(ready,/7 \+ 5/);assert.ok(working.includes("7 + 5")&&working.includes("12"));assert.match(settled,/12 = 9 \+ 3/);assert.match(ready,/g8-operation is-hidden/);assert.match(settled,/g8-result is-visible/);assert.match(settled,/g8-operation is-visible/);
  assert.match(ready,/data-term-id="left-term-/,"individual mathematical terms are targetable");
  assert.match(working,/data-operation-action="evaluate_expression"/);
  assert.match(working,/g8-operation-path/,"the operation has targetable motion objects before its result");
  assert.match(settled,/data-action="evaluate_expression"/);
  assert.match(settled,/Result of this step/,"an intermediate state is not labelled as the final answer");
 }
});

test("additive equations do not show a permanent cancellation slogan or empty unknown slot",()=>{
 const registry=registryFor("algebra/grade8-equation-renderers.js"),renderer=registry.get("algebra:additive_inverse");
 const markup=renderer.render({prompt:"□ + 3 = 10",question_id:"g8-ae-l01-w03",source_data:""},{before_state:"□ + 3 = 10",working_state:"subtract 3 from both sides",after_state:"□ = 7",target:"left-expression",annotations:["stage:2","action:remove_from_both_sides"]},"result");
 assert.doesNotMatch(markup,/inverse pairs cancel to zero/);
 assert.match(markup,/data-object-id="variable-slot"[^>]* hidden/);
 assert.match(markup,/subtract 3 from both sides/);
});
