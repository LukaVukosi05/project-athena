import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";

const baseUrl = process.env.ATHENA_URL || "http://127.0.0.1:8011";
const output = path.resolve("artifacts/grade8-algebraic-equations-lesson1/navigation-acceptance");
mkdirSync(output, { recursive:true });
const chromePath = process.env.CHROME_PATH || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const chrome = spawn(chromePath, ["--headless=new", "--remote-debugging-port=9228",
  `--user-data-dir=${path.join(output, "chrome-profile")}`, "--window-size=1440,1000",
  "--disable-gpu", "--no-first-run"], { stdio:"ignore" });
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function poll(url) {
  for (let index=0; index<100; index++) {
    try { const response=await fetch(url); if (response.ok) return response.json(); } catch {}
    await delay(100);
  }
  throw new Error(`Chrome not available: ${url}`);
}
class CDP {
  constructor(url) {
    this.socket=new WebSocket(url); this.next=1; this.pending=new Map();
    this.socket.onmessage=event => {
      const message=JSON.parse(event.data); if (!message.id) return;
      const task=this.pending.get(message.id); this.pending.delete(message.id);
      message.error ? task.reject(new Error(message.error.message)) : task.resolve(message.result);
    };
  }
  ready() { return new Promise((resolve,reject) => { this.socket.onopen=resolve; this.socket.onerror=reject; }); }
  send(method,params={}) { const id=this.next++; return new Promise((resolve,reject) => {
    this.pending.set(id,{resolve,reject}); this.socket.send(JSON.stringify({id,method,params}));
  }); }
}
let cdp;
try {
  await poll("http://127.0.0.1:9228/json/version");
  const target=await fetch(`http://127.0.0.1:9228/json/new?${encodeURIComponent(baseUrl)}`,{method:"PUT"}).then(r=>r.json());
  cdp=new CDP(target.webSocketDebuggerUrl); await cdp.ready();
  await cdp.send("Page.enable"); await cdp.send("Runtime.enable");
  const evaluate=async expression => {
    const result=await cdp.send("Runtime.evaluate",{expression,awaitPromise:true,returnByValue:true});
    if (result.exceptionDetails) throw new Error(result.exceptionDetails.exception?.description || result.exceptionDetails.text);
    return result.result.value;
  };
  const waitFor=async (expression,timeout=20000) => {
    const start=Date.now();
    while (Date.now()-start<timeout) { if (await evaluate(expression)) return; await delay(80); }
    throw new Error(`Timed out: ${expression}; page=${await evaluate("document.body?.innerText?.slice(0,800)")}`);
  };
  const click=selector=>evaluate(`(()=>{const node=document.querySelector(${JSON.stringify(selector)});if(!node)throw Error('Missing ${selector}');node.click();return true})()`);
  const state=()=>evaluate(`(()=>{const board=document.querySelector('.stateful-whiteboard'),stage=document.querySelector('.whiteboard-stage');return {status:board?.dataset.controllerState,example:Number(document.querySelector('[data-example-index][aria-current="step"]')?.dataset.exampleIndex)+1,step:document.querySelector('[data-role="position"]')?.textContent,history:stage?.querySelectorAll('.g8-completed-steps li').length||0,text:stage?.innerText||'',missing:stage?.dataset.missingTargets||'',overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,stageOverflow:stage?.scrollWidth-stage?.clientWidth||0,primary:document.querySelector('[data-action="primary"]')?.textContent};})()`);
  const layout=()=>evaluate(`(()=>{const stage=document.querySelector('.whiteboard-stage'),visual=stage?.querySelector('.whiteboard-visual-pane'),written=stage?.querySelector('.g8-completed-steps');if(!stage||!visual||!written)return null;const a=visual.getBoundingClientRect(),b=written.getBoundingClientRect();return {mode:stage.dataset.layout,visual:{left:a.left,right:a.right,top:a.top,bottom:a.bottom},written:{left:b.left,top:b.top},latestVisible:written.scrollTop+written.clientHeight>=written.scrollHeight-3};})()`);
  async function shot(name) {
    const data=(await cdp.send("Page.captureScreenshot",{format:"png",captureBeyondViewport:false})).data;
    writeFileSync(path.join(output,name),Buffer.from(data,"base64"));
  }
  async function navigate(number,width=1440,height=1000) {
    await cdp.send("Emulation.setDeviceMetricsOverride",{width,height,deviceScaleFactor:1,mobile:width<700});
    await cdp.send("Page.navigate",{url:`${baseUrl}/lesson.html?grade=grade-8&topic=algebraic-equations&lesson=g8-algebraic-equations-01&example=${number}`});
    await waitFor(`document.querySelector('.stateful-whiteboard') && !document.querySelector('[data-action="primary"]')?.disabled`);
    await evaluate("document.querySelector('.stateful-whiteboard').scrollIntoView({block:'start'})");
  }
  const settings=(name,value)=>evaluate(`(()=>{const input=document.querySelector('[data-action="${name}"]');if(input.checked!==${value})input.click();return input.checked})()`);
  const pick=async number=>{await click(`[data-example-index="${number-1}"]`);await waitFor(`document.querySelector('[data-example-index="${number-1}"][aria-current="step"]') && !document.querySelector('[data-action="primary"]')?.disabled`);};
  const payload=number=>evaluate(`fetch('/api/v1/lessons/g8-algebraic-equations-01/questions/g8-ae-l01-w${String(number).padStart(2,"0")}/reveal',{method:'POST'}).then(r=>r.json())`);
  const results=[];
  for (let number=1; number<=15; number++) {
    await navigate(number);
    if (number===1) {
      const desktop=await layout();
      if (desktop?.mode!=="split" || desktop.visual.right>desktop.written.left+2 || Math.abs(desktop.visual.top-desktop.written.top)>20)
        throw Error(`The active visual and written solution are not side by side: ${JSON.stringify(desktop)}`);
    }
    await settings("reduced-motion",true);
    const data=await payload(number), steps=data.whiteboard.steps;
    const initial=await state();
    if (initial.history || initial.missing || initial.overflow>1 || initial.stageOverflow>1) throw Error(`Example ${number}: bad initial state ${JSON.stringify(initial)}`);
    for (let index=0; index<steps.length; index++) {
      const ready=await state();
      if (ready.history!==index || ready.status!==(index===0?"idle":"step_complete")) throw Error(`Example ${number}: step ${index+1} not ready ${JSON.stringify(ready)}`);
      await click('[data-action="primary"]');
      const result=await state();
      if (result.status!==(index===steps.length-1?"example_complete":"step_complete") || result.history!==index+1) throw Error(`Example ${number}: result not complete ${JSON.stringify(result)}`);
      if (!result.text.includes(steps[index].after_expression)) throw Error(`Example ${number}: current written result is missing`);
      if (index>0 && !result.text.includes(steps[index-1].after_expression))
        throw Error(`Example ${number}: previous mathematics disappeared on step ${index+1}`);
    }
    const final=await state();
    const finalLayout=await layout();
    if (!finalLayout?.latestVisible) throw Error(`Example ${number}: latest written step is out of view`);
    if (final.missing || final.overflow>1 || final.stageOverflow>1) throw Error(`Example ${number}: missing targets or overflow`);
    results.push({example:number,steps:steps.length,retainedHistory:final.history});
    if ([1,8,15].includes(number)) await shot(`example-${String(number).padStart(2,"0")}-final.png`);
  }

  await navigate(8);
  await settings("reduced-motion",true);
  await click('[data-action="primary"]');
  const saved=await state();
  await pick(5);
  if ((await state()).example!==5) throw Error("Example picker failed to jump from 8 to 5");
  await pick(8);
  const returned=await state();
  if (returned.step!==saved.step || returned.status!==saved.status) throw Error("Returning to example 8 lost its completed step");
  await shot("example-8-returned.png");

  await navigate(2);
  await settings("reduced-motion",false);
  await click('[data-action="primary"]');
  await waitFor(`document.querySelector('.stateful-whiteboard')?.dataset.controllerState==='playing'`);
  await click('[data-action="pause"]');
  if ((await state()).status!=="paused") throw Error("Pause did not stop the explanation");
  await click('[data-action="primary"]');
  if ((await state()).status!=="playing") throw Error("Continue did not resume the explanation");
  await pick(5); await pick(2);
  if ((await state()).status==="playing") throw Error("Switching examples left stale narration playing");

  await navigate(5,390,844);
  const mobileLayout=await layout();
  if (mobileLayout?.mode!=="split" || mobileLayout.visual.bottom>mobileLayout.written.top+2)
    throw Error(`Mobile visual and solution do not stack in reading order: ${JSON.stringify(mobileLayout)}`);
  await shot("mobile-example-5.png");
  const mobile=await state();
  if (mobile.overflow>1 || mobile.stageOverflow>1) throw Error(`Mobile overflow: ${JSON.stringify(mobile)}`);
  writeFileSync(path.join(output,"browser-verification.json"),JSON.stringify({checkedAt:new Date().toISOString(),results,mobile,journeys:["all 15 examples","8 to 5 to 8","pause/continue/switch","390px mobile"]},null,2));
  console.log(JSON.stringify({examples:results.length,journeys:4,mobileOverflow:mobile.overflow,output},null,2));
} finally {
  cdp?.socket.close();
  chrome.kill();
}
