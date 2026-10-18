const fs=require("fs"),path=require("path");
const out=path.resolve(__dirname,"../artifacts/curriculum-verification");fs.mkdirSync(out,{recursive:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function main(){
 const pages=await(await fetch("http://127.0.0.1:9225/json")).json(),page=pages.find(p=>p.type==="page"),ws=new WebSocket(page.webSocketDebuggerUrl);let id=0;const pending=new Map();
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}};await new Promise(r=>ws.onopen=r);
 const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
 const evalJs=async expression=>(await send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true})).result.value;
 const nav=async url=>{await send("Page.navigate",{url});for(let i=0;i<120;i++){if(await evalJs("document.readyState==='complete'&&Boolean(document.querySelector('.whiteboard-stage svg'))"))break;await sleep(100);}await evalJs("document.querySelector('.stateful-whiteboard').scrollIntoView({block:'start'})");await sleep(100);};
 const shot=async name=>{const r=await send("Page.captureScreenshot",{format:"png"});fs.writeFileSync(path.join(out,name),Buffer.from(r.data,"base64"));};
 await send("Page.enable");await send("Runtime.enable");await send("Emulation.setDeviceMetricsOverride",{width:1365,height:900,deviceScaleFactor:1,mobile:false});
 const cases=[["g12-statistics-08","G12-STAT-L08-W01","deviation_panel"],["g12-statistics-10","G12-STAT-L10-W01","scatter_plot"],["g12-statistics-12","G12-STAT-L12-W01","regression_line"],["g12-statistics-17","G12-STAT-L17-W01","regression_line"]];
 const failures=[];
 for(const [lesson,question,template] of cases){
  const base="http://127.0.0.1:8010/lesson.html?lesson="+lesson+"&example=1";
  await nav(base+"&step=0");const initial=await evalJs("document.querySelector('.whiteboard-stage').innerHTML");await shot(lesson+"__"+question+"__initial.png");
  await nav(base+"&step=1");const operation=await evalJs("document.querySelector('.whiteboard-stage').innerHTML");await shot(lesson+"__"+question+"__operation.png");
  await evalJs("document.querySelector('[data-action=play]').click()");await sleep(1100);const result=await evalJs("document.querySelector('.whiteboard-stage').innerHTML");await shot(lesson+"__"+question+"__result.png");
  const api=await(await fetch("http://127.0.0.1:8010/api/v1/lessons/"+lesson)).json(),actual=api.whiteboard_questions[0].whiteboard.visualization.template;
  const diagnostic=await evalJs("document.querySelector('.whiteboard-stage').dataset.missingTargets||document.querySelector('.whiteboard-stage').dataset.diagnostic||''");
  if(actual!==template)failures.push(lesson+" expected "+template+" got "+actual);if(initial===operation||operation===result)failures.push(lesson+" visual states are identical");if(diagnostic)failures.push(lesson+" "+diagnostic);
 }
 ws.close();console.log(JSON.stringify({cases:cases.length,failures},null,2));if(failures.length)process.exitCode=1;
}
main().catch(e=>{console.error(e);process.exit(1);});
