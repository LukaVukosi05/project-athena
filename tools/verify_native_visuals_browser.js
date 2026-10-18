const fs=require("fs"),path=require("path");
const out=path.resolve(__dirname,"../artifacts/curriculum-verification");fs.mkdirSync(out,{recursive:true});
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function main(){
 const pages=await(await fetch("http://127.0.0.1:9225/json")).json(),page=pages.find(candidate=>candidate.type==="page");if(!page)throw new Error("No CDP browser page.");
 const ws=new WebSocket(page.webSocketDebuggerUrl);let id=0;const pending=new Map();ws.onmessage=event=>{const message=JSON.parse(event.data);if(message.id&&pending.has(message.id)){const waiter=pending.get(message.id);pending.delete(message.id);message.error?waiter.reject(message.error):waiter.resolve(message.result);}};await new Promise(resolve=>ws.onopen=resolve);
 const send=(method,params={})=>new Promise((resolve,reject)=>{const request=++id;pending.set(request,{resolve,reject});ws.send(JSON.stringify({id:request,method,params}));});
 const evaluate=async expression=>(await send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true})).result.value;
 const navigate=async url=>{await send("Page.navigate",{url});for(let attempt=0;attempt<120;attempt++){if(await evaluate("document.readyState==='complete'&&Boolean(document.querySelector('.whiteboard-stage svg'))"))break;await sleep(100);}await evaluate("document.querySelector('.stateful-whiteboard').scrollIntoView({block:'start'})");await sleep(100);};
 const shot=async name=>{const capture=await send("Page.captureScreenshot",{format:"png"});fs.writeFileSync(path.join(out,name),Buffer.from(capture.data,"base64"));};
 await send("Page.enable");await send("Runtime.enable");await send("Emulation.setDeviceMetricsOverride",{width:1365,height:900,deviceScaleFactor:1,mobile:false});
 const cases=[
  ["g12-sequences-series-02","g12-seq-l02-wbq-01","term_rows"],
  ["g12-sequences-series-07","g12-seq-l07-wbq-01","difference_table"],
  ["g12-sequences-series-08","g12-seq-l08-wbq-01","sigma_expansion"],
  ["g12-sequences-series-09","g12-seq-l09-wbq-01","partial_sum"],
  ["g12-sequences-series-13","g12-seq-l13-wbq-01","convergence_diagram"],
  ["g12-sequences-series-15","g12-seq-l15-wbq-01","formula_decision"],
  ["g12-sequences-series-17","g12-seq-l17-wbq-01","error_diagnosis"],
  ["g12-statistics-01","G12-STAT-L01-W01","data_studio"],
 ];
 const failures=[];
 for(const [lesson,question,template] of cases){
  const api=await(await fetch("http://127.0.0.1:8010/api/v1/lessons/"+lesson)).json(),board=api.whiteboard_questions[0].whiteboard,last=board.steps.length-1,base="http://127.0.0.1:8010/lesson.html?lesson="+lesson+"&example=1";
  if(board.visualization.template!==template)failures.push(lesson+" expected "+template+" got "+board.visualization.template);
  await navigate(base+"&step=0");const initial=await evaluate("document.querySelector('.whiteboard-stage').innerHTML");await shot(lesson+"__"+question+"__initial.png");
  await navigate(base+"&step=1");const operation=await evaluate("document.querySelector('.whiteboard-stage').innerHTML");await shot(lesson+"__"+question+"__operation.png");
  await navigate(base+"&step="+last);await evaluate("document.querySelector('[data-action=play]').click()");await sleep(1200);const result=await evaluate("document.querySelector('.whiteboard-stage').innerHTML");await shot(lesson+"__"+question+"__result.png");
  const diagnostic=await evaluate("document.querySelector('.whiteboard-stage').dataset.missingTargets||document.querySelector('.whiteboard-stage').dataset.diagnostic||''");
  if(initial===operation||operation===result||initial===result)failures.push(lesson+" has identical DOM states");if(diagnostic)failures.push(lesson+" "+diagnostic);if(!result.includes("<svg"))failures.push(lesson+" has no SVG result");
 }
 await send("Emulation.setDeviceMetricsOverride",{width:390,height:844,deviceScaleFactor:1,mobile:true});
 await navigate("http://127.0.0.1:8010/lesson.html?lesson=g12-statistics-01&example=1&step=1");
 const clipped=await evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth");await shot("g12-statistics-01__G12-STAT-L01-W01__result-mobile.png");if(clipped)failures.push("Statistics data studio clips the mobile document");
 ws.close();console.log(JSON.stringify({cases:cases.length,mobile_document_clipped:clipped,failures},null,2));if(failures.length)process.exitCode=1;
}
main().catch(error=>{console.error(error);process.exit(1);});
