const test=require("node:test");
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const path=require("node:path");

function loadRenderer(){
  const registered=new Map();
  const context={
    AthenaVisualizationRegistry:{register(type,template,renderer){registered.set(`${type}:${template}`,renderer);}},
    escapeWhiteboardHtml(value){return String(value).replace(/[&<>"]/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[char]));},
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname,"../js/visualization/statistics/statistics-renderers.js"),"utf8"),context);
  return registered.get("statistics:box_plot");
}

const first={minimum:8,q1:13,median:17,q3:22,maximum:28,title:"Five-number summary",show_iqr:true,show_range:true};
const second={minimum:-5,q1:-1,median:3,q3:8,maximum:14,title:"Different summary",show_iqr:true,show_range:true};
const finalState={annotations:["boxplot-stage:13"]};

test("box plot renderer is registered and uses all five supplied values",()=>{
  const renderer=loadRenderer();
  assert.ok(renderer);
  const svg=renderer.render(first,finalState,"result");
  for(const value of [8,13,17,22,28])assert.match(svg,new RegExp(`>${value}<`));
  for(const id of ["boxplot-axis","boxplot-minimum","boxplot-q1","boxplot-median","boxplot-q3","boxplot-maximum","boxplot-left-whisker","boxplot-right-whisker","boxplot-box","boxplot-iqr","boxplot-range","boxplot-conclusion"])assert.match(svg,new RegExp(`data-object-id="${id}"`));
  assert.match(svg,/IQR = 9/);
  assert.match(svg,/Range = 20/);
  assert.equal((svg.match(/<rect /g)||[]).length,1);
});

test("box and median coordinates are scaled from question-specific values",()=>{
  const renderer=loadRenderer();
  const a=renderer.render(first,finalState,"result");
  const b=renderer.render(second,finalState,"result");
  assert.notEqual(a,b);
  assert.match(a,/data-object-id="boxplot-box"[^>]*x="175"[^>]*width="225"/);
  assert.match(a,/x1="275"[^>]*x2="275"[^>]*class="boxplot-median-line/);
  assert.match(b,/data-object-id="boxplot-box"[^>]*x="155\.263/);
  assert.match(b,/x1="260\.526[^>]*x2="260\.526[^>]*class="boxplot-median-line/);
});

test("initial, operation and result states differ without losing mathematical objects",()=>{
  const renderer=loadRenderer();
  const state={annotations:["boxplot-stage:7"]};
  const initial=renderer.render(first,{annotations:["boxplot-stage:0"]},"ready");
  const operation=renderer.render(first,state,"operation");
  const result=renderer.render(first,finalState,"result");
  assert.notEqual(initial,operation);
  assert.notEqual(operation,result);
  assert.match(initial,/data-object-id="boxplot-box" class="semantic-object is-hidden"/);
  assert.match(operation,/data-object-id="boxplot-box" class="semantic-object is-visible"/);
  assert.doesNotMatch(result,/data-object-id="boxplot-(?:axis|values|minimum|q1|median|q3|maximum|left-whisker|right-whisker|box|iqr|range|conclusion)" class="semantic-object is-hidden"/);
});
