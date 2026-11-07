const {test}=require('node:test');const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');const vm=require('node:vm');
const root=path.resolve(__dirname,'../..');const page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');const ops=vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8'),ops);
const visuals=new Map();vm.runInNewContext(fs.readFileSync(path.join(root,'frontend/js/visualization/geometry/grade9-shape-renderers.js'),'utf8'),{AthenaVisualizationRegistry:{register:(type,name,r)=>visuals.set(`${type}:${name}`,r)},escapeWhiteboardHtml:s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'),Math});
test('120 question-owned shape diagrams preserve givens and reveal each result only at its stage',()=>{
 assert.match(page,/grade9-shape-renderers\.js/);assert.match(page,/grade9-shapes\.css/);
 for(let n=1;n<=8;n++){
  const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',`shapes_${String(n).padStart(2,'0')}.json`),'utf8'));
  const op=vm.runInContext(`AthenaWhiteboardRegistry.resolve("grade9_shapes_${n}_step")`,ops);
  const renderer=visuals.get(`geometry:grade9_shapes_${n}`);assert.ok(renderer);
  for(const scene of data.worked){
   const params={scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5};
   const render=(i,phase)=>renderer.render(params,{annotations:[`stage:${i}`],working_state:scene.actions[Math.max(0,i-1)],after_state:scene.actions[Math.max(0,i-1)]},phase);
   const initial=render(0,'ready');assert.match(initial,/data-object-id="model"/);assert.match(initial,/data-object-id="problem"/);
   assert.doesNotMatch(initial,/data-object-id="verification"[^>]*>[^<]+</);
   for(const tag of initial.matchAll(/<(?:polygon|line|text)[^>]*>/g)){
    for(const match of tag[0].matchAll(/(?:x1|x2|y1|y2|x|y)="(-?\d+(?:\.\d+)?)"/g)){
     const bound=match[0].startsWith('y')?280:500;
     assert.ok(Number(match[1])>=0&&Number(match[1])<=bound,`${scene.id}: coordinate outside SVG`);
    }
    if(tag[0].startsWith('<polygon'))for(const pair of tag[0].matchAll(/(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)/g)){
     assert.ok(Number(pair[1])>=0&&Number(pair[1])<=500&&Number(pair[2])>=0&&Number(pair[2])<=280,`${scene.id}: polygon clipped`);
    }
   }
   for(let i=1;i<=5;i++){assert.equal(op.render({operation:{type:`grade9_shapes_${n}_step`,value:scene.actions[i-1]},before_expression:'before',after_expression:'after'},'result',{hasVisualization:true}),'');assert.match(render(i,'result'),/data-object-id="model"/)}
   const final=render(5,'result');assert.match(final,/data-object-id="verification"/);assert.notEqual(initial,final);
  }
 }
});

test('gated previews retain the actual figure and conceal its calculated measurement',()=>{
 for(let n=1;n<=8;n++){
  const scene=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',`shapes_${String(n).padStart(2,'0')}.json`),'utf8')).worked[0];
  const visual={family:'shapes',values:{...scene.visual.values}};delete visual.values.target;delete visual.values.each;
  const preview={id:scene.id,problem:scene.problem,lesson:n,visual};
  const html=visuals.get(`geometry:grade9_shapes_${n}`).render({scene_json:JSON.stringify(preview),question_id:scene.id,prompt:scene.problem,total_steps:5},{annotations:[],working_state:'',after_state:''},'ready');
  assert.match(html,/data-object-id="model"/);assert.match(html,/data-object-id="problem"/);
  assert.doesNotMatch(html,/<text[^>]*class=""[^>]*>undefined<\/text>/);
 }
});
test('all six quadrilateral families use coherent figure geometry',()=>{
 const scenes=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated/shapes_03.json'),'utf8')).worked;
 assert.equal(new Set(scenes.map(s=>s.visual.values.model)).size,6);
 const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
 for(const scene of scenes){
  const renderer=visuals.get('geometry:grade9_shapes_3');const html=renderer.render({scene_json:JSON.stringify(scene),question_id:scene.id,prompt:scene.problem,total_steps:5},{annotations:[],working_state:'',after_state:''},'ready');
  const coords=[...html.match(/<polygon points="([^"]+)/)[1].matchAll(/(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)/g)].map(m=>[Number(m[1]),Number(m[2])]);
  const length=[0,1,2,3].map(i=>distance(coords[i],coords[(i+1)%4]));
  if(scene.visual.values.model==='square')assert.ok(Math.max(...length)-Math.min(...length)<0.2);
  if(scene.visual.values.model==='rhombus')assert.ok(Math.max(...length)-Math.min(...length)<0.2);
  if(scene.visual.values.model==='rectangle')assert.ok(Math.abs(length[0]-length[2])<0.2&&Math.abs(length[1]-length[3])<0.2);
  if(scene.visual.values.model==='trapezium')assert.ok(Math.abs(coords[0][1]-coords[1][1])<0.1&&Math.abs(coords[2][1]-coords[3][1])<0.1);
 }
});
