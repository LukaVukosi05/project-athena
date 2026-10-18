/* Headless Edge/CDP capture for every active Grade 12 worked example. */
const fs=require("fs"),path=require("path");
const ROOT=path.resolve(__dirname,"..");
const OUT=path.join(ROOT,"artifacts","whiteboard-audit");
fs.mkdirSync(OUT,{recursive:true});
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function lessons(){
  const grade=await (await fetch("http://127.0.0.1:8010/api/v1/curriculum/grades/grade-12")).json();
  const ids=[];
  for(const topic of grade.topics){
    const payload=await (await fetch(`http://127.0.0.1:8010/api/v1/curriculum/grades/grade-12/topics/${topic.id}`)).json();
    for(const subtopic of payload.subtopics||[])for(const lesson of subtopic.lessons||[])if(lesson.status!=="coming_soon")ids.push(lesson.id);
  }
  return Promise.all(ids.map(id=>fetch(`http://127.0.0.1:8010/api/v1/lessons/${id}`).then(r=>r.json())));
}
async function main(){
  const pages=await (await fetch("http://127.0.0.1:9225/json")).json();
  const page=pages.find(item=>item.type==="page");
  const ws=new WebSocket(page.webSocketDebuggerUrl);let id=0;const pending=new Map();
  ws.onmessage=event=>{const message=JSON.parse(event.data);if(message.id&&pending.has(message.id)){const {resolve,reject}=pending.get(message.id);pending.delete(message.id);message.error?reject(message.error):resolve(message.result);}};
  await new Promise(resolve=>ws.onopen=resolve);
  const send=(method,params={})=>new Promise((resolve,reject)=>{const call=++id;pending.set(call,{resolve,reject});ws.send(JSON.stringify({id:call,method,params}));});
  const evaluate=expression=>send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true});
  const ready=async()=>{for(let attempt=0;attempt<300;attempt++){const value=await evaluate("Boolean(document.querySelector('.whiteboard-stage') && document.querySelector('[data-action=next]'))");if(value.result.value)return;await sleep(100);}const detail=await evaluate("location.href+'\\n'+document.body.innerText");throw new Error(`whiteboard did not mount: ${detail.result.value}`);};
  const shot=async file=>{const data=await send("Page.captureScreenshot",{format:"png",captureBeyondViewport:false});fs.writeFileSync(path.join(OUT,file),Buffer.from(data.data,"base64"));};
  await send("Page.enable");await send("Runtime.enable");await send("Emulation.setDeviceMetricsOverride",{width:1365,height:1000,deviceScaleFactor:1,mobile:false});
  const failures=[];let count=0;
  for(const lesson of await lessons())for(let index=0;index<(lesson.whiteboard_questions||[]).length;index++){
    const question=lesson.whiteboard_questions[index],stem=`${lesson.id}__${question.id}`.replace(/[^a-zA-Z0-9_-]/g,"-");
    await send("Page.navigate",{url:`http://127.0.0.1:8010/lesson.html?lesson=${lesson.id}&example=${index+1}&step=0`});await ready();await sleep(120);
    const initial=(await evaluate("document.querySelector('.whiteboard-stage').innerText")).result.value;
    await shot(`${stem}__initial.png`);
    await evaluate("document.querySelector('[data-action=next]').click()");await sleep(320);
    const operation=(await evaluate("document.querySelector('.whiteboard-stage').innerHTML")).result.value;await shot(`${stem}__operation.png`);
    const steps=question.whiteboard.steps.length;
    for(let step=2;step<steps;step++){await evaluate("document.querySelector('[data-action=next]').click()");await sleep(25);}
    await sleep(950);const final=(await evaluate("document.querySelector('.whiteboard-stage').innerHTML")).result.value;await shot(`${stem}__final.png`);
    if(operation===final)failures.push(`${lesson.id} / ${question.id} / operation equals final DOM`);
    const answer=String(question.answer||"");if(answer&&initial.includes(answer))failures.push(`${lesson.id} / ${question.id} / complete answer visible initially`);
    count++;if(count%20===0)console.log(`captured ${count}`);
  }
  fs.writeFileSync(path.join(OUT,"browser-audit.json"),JSON.stringify({examples:count,failures},null,2));
  ws.close();console.log(JSON.stringify({examples:count,failures:failures.length}));if(failures.length)process.exitCode=1;
}
main().catch(error=>{console.error(error);process.exit(1);});
