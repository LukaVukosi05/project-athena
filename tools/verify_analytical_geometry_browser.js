const fs=require("fs"),path=require("path");
const out=path.resolve(__dirname,"../artifacts/curriculum-verification");fs.mkdirSync(out,{recursive:true});
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));

async function main(){
  const pages=await(await fetch("http://127.0.0.1:9225/json")).json();
  const page=pages.find(candidate=>candidate.type==="page");
  if(!page)throw new Error("No browser page is available on CDP port 9225.");
  const ws=new WebSocket(page.webSocketDebuggerUrl);let id=0;const pending=new Map();
  ws.onmessage=event=>{const message=JSON.parse(event.data);if(message.id&&pending.has(message.id)){const waiter=pending.get(message.id);pending.delete(message.id);message.error?waiter.reject(message.error):waiter.resolve(message.result);}};
  await new Promise(resolve=>ws.onopen=resolve);
  const send=(method,params={})=>new Promise((resolve,reject)=>{const requestId=++id;pending.set(requestId,{resolve,reject});ws.send(JSON.stringify({id:requestId,method,params}));});
  const evaluate=async expression=>(await send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true})).result.value;
  const navigate=async url=>{await send("Page.navigate",{url});for(let attempt=0;attempt<120;attempt++){if(await evaluate("document.readyState==='complete'&&Boolean(document.querySelector('.whiteboard-stage svg'))"))break;await sleep(100);}await evaluate("document.querySelector('.stateful-whiteboard').scrollIntoView({block:'start'})");await sleep(100);};
  const screenshot=async name=>{const capture=await send("Page.captureScreenshot",{format:"png"});fs.writeFileSync(path.join(out,name),Buffer.from(capture.data,"base64"));};
  await send("Page.enable");await send("Runtime.enable");await send("Emulation.setDeviceMetricsOverride",{width:1365,height:900,deviceScaleFactor:1,mobile:false});
  const cases=[
    {lesson:"g12-analytical-geometry-01",question:"G12-AG-L01-W01",template:"coordinate_distance_lab",needles:["A(-3, -2)","B(3, 6)","Δx=6","Δy=8"]},
    {lesson:"g12-analytical-geometry-02",question:"G12-AG-L02-W01",template:"midpoint_bisection",needles:["A(-2, -2)","B(6, 4)","M(2, 1)"]},
    {lesson:"g12-analytical-geometry-03",question:"G12-AG-L03-W01",template:"slope_triangle",needles:["A(0, -1)","B(2, 1)"]},
    {lesson:"g12-analytical-geometry-04",question:"G12-AG-L04-W01",template:"line_equation_link",needles:["P(-1, 1)"]},
    {lesson:"g12-analytical-geometry-05",question:"G12-AG-L05-W01",template:"parallel_comparison",needles:["P(-1, 2)","m=3"]},
    {lesson:"g12-analytical-geometry-06",question:"G12-AG-L06-W01",template:"perpendicular_rotation",needles:["P(-1, 3)"]},
    {lesson:"g12-analytical-geometry-07",question:"G12-AG-L07-W01",template:"inclination_arc",needles:["θ=30°"]},
    {lesson:"g12-analytical-geometry-08",question:"G12-AG-L08-W01",template:"circle_construction",needles:["C(-3, 0)","r=3"]},
    {lesson:"g12-analytical-geometry-09",question:"G12-AG-L09-W01",template:"complete_square_morph",needles:["C(-2, 1), r=4"]},
    {lesson:"g12-analytical-geometry-10",question:"G12-AG-L10-W01",template:"circle_condition_intersection",needles:["P(1, 1)","C(0, 0), r=6"]},
    {lesson:"g12-analytical-geometry-11",question:"G12-AG-L11-W01",template:"radius_tangent_contact",needles:["C(0, 0)","T(6, 8)"]},
    {lesson:"g12-analytical-geometry-12",question:"G12-AG-L12-W01",template:"tangent_equation_construction",needles:["T(4, 8)","C(-2, 0)"]},
    {lesson:"g12-analytical-geometry-13",question:"G12-AG-L13-W01",template:"external_tangent_length",needles:["PT=8"]},
    {lesson:"g12-analytical-geometry-14",question:"G12-AG-L14-W01",template:"coordinate_proof_studio",needles:["A(2, 4)","D(2, 6)","proof-polygon"]},
    {lesson:"g12-analytical-geometry-15",question:"G12-AG-L15-W01",template:"integrated_coordinate_scene",needles:["C(-1, 0)","T(5, 8)"]},
    {lesson:"g12-analytical-geometry-16",question:"G12-AG-L16-W01",template:"question_first_assessment",needles:["C(0, 0)","T(6, 8)"]},
  ];
  const failures=[];
  for(const item of cases){
    const base="http://127.0.0.1:8010/lesson.html?lesson="+item.lesson+"&example=1";
    await navigate(base+"&step=0");const initial=await evaluate("document.querySelector('.whiteboard-stage').innerHTML");await screenshot(item.lesson+"__"+item.question+"__initial.png");
    await navigate(base+"&step=1");const operation=await evaluate("document.querySelector('.whiteboard-stage').innerHTML");await screenshot(item.lesson+"__"+item.question+"__operation.png");
    await evaluate("document.querySelector('[data-action=play]').click()");await sleep(1100);const result=await evaluate("document.querySelector('.whiteboard-stage').innerHTML");await screenshot(item.lesson+"__"+item.question+"__result.png");
    const api=await(await fetch("http://127.0.0.1:8010/api/v1/lessons/"+item.lesson)).json();
    const visual=api.whiteboard_questions[0].whiteboard.visualization;
    if(visual.template!==item.template)failures.push(item.lesson+" expected "+item.template+" got "+visual.template);
    if(initial===operation||operation===result)failures.push(item.lesson+" visual states are identical");
    for(const needle of item.needles)if(!result.includes(needle))failures.push(item.lesson+" missing "+needle);
    const diagnostic=await evaluate("document.querySelector('.whiteboard-stage').dataset.missingTargets||document.querySelector('.whiteboard-stage').dataset.diagnostic||''");
    if(diagnostic)failures.push(item.lesson+" "+diagnostic);
  }
  ws.close();console.log(JSON.stringify({cases:cases.length,failures},null,2));if(failures.length)process.exitCode=1;
}
main().catch(error=>{console.error(error);process.exit(1);});
