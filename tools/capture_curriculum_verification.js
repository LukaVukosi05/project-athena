const fs=require("fs"),path=require("path");
const out=path.resolve(__dirname,"../artifacts/curriculum-verification");
fs.mkdirSync(out,{recursive:true});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
async function main(){
 const pages=await(await fetch("http://127.0.0.1:9225/json")).json(),page=pages.find(p=>p.type==="page");
 const ws=new WebSocket(page.webSocketDebuggerUrl);let id=0;const pending=new Map();
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}};
 await new Promise(r=>ws.onopen=r);
 const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
 const evaluate=async expression=>(await send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true})).result.value;
 const nav=async url=>{await send("Page.navigate",{url});for(let i=0;i<100;i++){if(await evaluate("document.readyState==='complete'"))break;await sleep(100);}await sleep(250);};
 const shot=async name=>{const r=await send("Page.captureScreenshot",{format:"png"});fs.writeFileSync(path.join(out,name),Buffer.from(r.data,"base64"));};
 await send("Page.enable");await send("Runtime.enable");await send("Emulation.setDeviceMetricsOverride",{width:1365,height:900,deviceScaleFactor:1,mobile:false});
 await nav("http://127.0.0.1:8010/grade.html?grade=grade-12");await shot("grade12-paper-sections.png");
 for(const topic of ["statistics-regression","analytical-geometry"]){await nav(`http://127.0.0.1:8010/topic.html?grade=grade-12&topic=${topic}`);await shot(`topic-${topic}.png`);}
 for(const lesson of ["g12-sequences-series-01","g12-sequences-series-02","g12-sequences-series-05","g12-sequences-series-10","g12-sequences-series-17","g12-sequences-series-18","g12-statistics-01","g12-analytical-geometry-01"]){
  await nav(`http://127.0.0.1:8010/lesson.html?lesson=${lesson}&example=1&step=0`);
  const example=await evaluate("document.querySelector('.whiteboard-question-set')?.dataset.questionId||document.querySelector('.stateful-whiteboard')?.parentElement?.dataset.questionId||'example-01'");
  const stem=`${lesson}__${example}`.replace(/[^a-zA-Z0-9_-]/g,"-");
  await shot(`${stem}__initial.png`);await evaluate("document.querySelector('[data-action=next]').click()");await sleep(250);await shot(`${stem}__operation.png`);
  for(let i=0;i<12;i++){if(await evaluate("document.querySelector('[data-action=next]').disabled"))break;await evaluate("document.querySelector('[data-action=next]').click()");await sleep(80);}
  await sleep(1000);await shot(`${stem}__result.png`);
 }
 await send("Emulation.setDeviceMetricsOverride",{width:390,height:844,deviceScaleFactor:1,mobile:true});await nav("http://127.0.0.1:8010/grade.html?grade=grade-12");await shot("grade12-paper-sections-mobile.png");
 ws.close();console.log(out);
}
main().catch(e=>{console.error(e);process.exit(1);});
