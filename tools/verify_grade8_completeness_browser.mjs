import { spawn } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";

const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const baseUrl = "http://127.0.0.1:8010";
const output = path.resolve("artifacts/grade8-algebraic-equations-lesson1/completeness-repair");
mkdirSync(output, { recursive: true });
const chrome = spawn(chromePath, ["--headless=new", "--remote-debugging-port=9227", `--user-data-dir=${path.join(output,"chrome-profile")}`, "--window-size=1365,900", "--disable-gpu", "--no-first-run"], { stdio: "ignore" });

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
async function pollJson(url) { for (let i=0;i<50;i+=1) { try { const result=await fetch(url); if(result.ok)return result.json(); } catch {} await delay(100); } throw new Error(`CDP unavailable: ${url}`); }

class CDP {
  constructor(url) { this.socket=new WebSocket(url); this.next=1; this.pending=new Map(); this.events=new Map(); this.socket.onmessage=event=>{const message=JSON.parse(event.data);if(message.id){const pending=this.pending.get(message.id);this.pending.delete(message.id);message.error?pending.reject(new Error(message.error.message)):pending.resolve(message.result);}else{for(const listener of this.events.get(message.method)||[])listener(message.params);}}; }
  ready(){return new Promise((resolve,reject)=>{this.socket.onopen=resolve;this.socket.onerror=reject;});}
  send(method,params={}){const id=this.next++;return new Promise((resolve,reject)=>{this.pending.set(id,{resolve,reject});this.socket.send(JSON.stringify({id,method,params}));});}
  on(method,listener){this.events.set(method,[...(this.events.get(method)||[]),listener]);}
}

function avi(frames,width,height,fps=10) {
  const u32=value=>{const b=Buffer.alloc(4);b.writeUInt32LE(value>>>0);return b;}, u16=value=>{const b=Buffer.alloc(2);b.writeUInt16LE(value);return b;}, four=value=>Buffer.from(value,"ascii");
  const chunk=(id,data)=>Buffer.concat([four(id),u32(data.length),data,data.length%2?Buffer.alloc(1):Buffer.alloc(0)]);
  const list=(type,data)=>chunk("LIST",Buffer.concat([four(type),data]));
  const avih=Buffer.concat([u32(1e6/fps),u32(width*height*3*fps),u32(0),u32(0x10),u32(frames.length),u32(0),u32(1),u32(width*height*3),u32(width),u32(height),Buffer.alloc(16)]);
  const strh=Buffer.concat([four("vids"),four("MJPG"),u32(0),u16(0),u16(0),u32(0),u32(1),u32(fps),u32(0),u32(frames.length),u32(width*height*3),u32(0xffffffff),u32(0),u16(0),u16(0),u16(width),u16(height)]);
  const strf=Buffer.concat([u32(40),u32(width),u32(height),u16(1),u16(24),four("MJPG"),u32(width*height*3),u32(0),u32(0),u32(0),u32(0)]);
  const hdrl=list("hdrl",Buffer.concat([chunk("avih",avih),list("strl",Buffer.concat([chunk("strh",strh),chunk("strf",strf)]))]));
  let offset=4; const entries=[],movie=[];
  for(const frame of frames){const data=Buffer.from(frame,"base64"),item=chunk("00dc",data);entries.push(Buffer.concat([four("00dc"),u32(0x10),u32(offset),u32(data.length)]));movie.push(item);offset+=item.length;}
  const body=Buffer.concat([four("AVI "),hdrl,list("movi",Buffer.concat(movie)),chunk("idx1",Buffer.concat(entries))]);
  return Buffer.concat([four("RIFF"),u32(body.length),body]);
}

const version=await pollJson("http://127.0.0.1:9227/json/version");
const target=await fetch(`http://127.0.0.1:9227/json/new?${encodeURIComponent(`${baseUrl}/lesson.html?lesson=g8-algebraic-equations-01&example=1`)}`,{method:"PUT"}).then(r=>r.json());
const cdp=new CDP(target.webSocketDebuggerUrl);await cdp.ready();await cdp.send("Page.enable");await cdp.send("Runtime.enable");
const evaluate=async(expression)=>{const result=await cdp.send("Runtime.evaluate",{expression,awaitPromise:true,returnByValue:true});if(result.exceptionDetails)throw new Error(`${result.exceptionDetails.text}: ${result.exceptionDetails.exception?.description||expression}`);return result.result.value;};
const waitFor=async(expression,timeout=12000)=>{const started=Date.now();while(Date.now()-started<timeout){if(await evaluate(expression))return;await delay(100);}throw new Error(`Timed out: ${expression}`);};
const click=async(selector)=>evaluate(`(()=>{const node=document.querySelector(${JSON.stringify(selector)});if(!node)return false;node.click();return true})()`);
const scrollTo=async(selector,block="center")=>{await evaluate(`document.querySelector(${JSON.stringify(selector)})?.scrollIntoView({block:${JSON.stringify(block)}})`);await delay(180);};
const screenshot=async(name)=>{const result=await cdp.send("Page.captureScreenshot",{format:"png",captureBeyondViewport:false});writeFileSync(path.join(output,name),Buffer.from(result.data,"base64"));};
const screenshotElement=async(name,selector)=>{const rect=await evaluate(`(()=>{const r=document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,width:r.width,height:r.height,scale:1}})()`);const result=await cdp.send("Page.captureScreenshot",{format:"png",captureBeyondViewport:true,clip:rect});writeFileSync(path.join(output,name),Buffer.from(result.data,"base64"));};
const navigate=async(example)=>{await cdp.send("Page.navigate",{url:`${baseUrl}/lesson.html?lesson=g8-algebraic-equations-01&example=${example}`});await waitFor(`document.querySelector('[data-example-action="reveal"]')`);await click('[data-example-action="reveal"]');await waitFor(`document.querySelector('.stateful-whiteboard')`);await scrollTo('.stateful-whiteboard','start');};
const enableReduced=async()=>{await evaluate(`(()=>{const input=document.querySelector('[data-action="reduced-motion"]');if(input&&!input.checked)input.click();return input?.checked})()`);};
const finishExample=async()=>{
  await click('[data-action="restart"]'); await waitFor(`document.querySelector('.stateful-whiteboard')?.dataset.controllerState==='idle'`); await enableReduced();
  const count=await evaluate(`Number(document.querySelector('[data-role="position"]').textContent.split(' of ')[1])`);
  for(let attempt=0;attempt<count+3;attempt+=1){
    const status=await evaluate(`document.querySelector('.stateful-whiteboard')?.dataset.controllerState`);
    if(status==="example_complete")return count;
    await click('[data-action="primary"]'); await delay(150);
  }
  const debug=await evaluate(`({status:document.querySelector('.stateful-whiteboard')?.dataset.controllerState,step:document.querySelector('[data-role="position"]')?.textContent,reduced:document.querySelector('[data-action="reduced-motion"]')?.checked})`);
  throw new Error(`Example did not finish: ${JSON.stringify(debug)}`);
};
const frames=[];cdp.on("Page.screencastFrame",async params=>{frames.push(params.data);await cdp.send("Page.screencastFrameAck",{sessionId:params.sessionId});});
await cdp.send("Page.startScreencast",{format:"jpeg",quality:72,maxWidth:1365,maxHeight:900,everyNthFrame:1});

const findings=[];
for(let example=1;example<=15;example+=1){
  await navigate(example);
  const id=String(example).padStart(2,"0");
  if([1,5,10,15].includes(example))await screenshot(`example-${id}-initial.png`);
  if(example===1){
    await scrollTo('.whiteboard-control-bar','end');await screenshot("desktop-integrated-controls.png");await scrollTo('.stateful-whiteboard','start');
    await click('[data-action="primary"]');await delay(700);await screenshot("example-01-mid-animation.png");
    await click('[data-action="primary"]');await delay(200);await click('[data-action="primary"]');
    await waitFor(`document.querySelector('.stateful-whiteboard')?.dataset.controllerState==='step_complete'`,15000);
    await click('[data-action="next"]');await delay(150);await click('[data-action="previous"]');await delay(150);await click('[data-action="replay"]');await delay(250);await click('[data-action="primary"]');
  }
  const steps=await finishExample();
  const state=await evaluate(`(()=>{const stage=document.querySelector('.whiteboard-stage'),board=document.querySelector('.stateful-whiteboard');return {question:document.querySelector('.g8-equation-visual')?.dataset.questionId,terminal:stage?.innerText,status:board?.dataset.controllerState,missing:stage?.dataset.missingTargets||'',pageOverflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,stageOverflow:stage.scrollWidth-stage.clientWidth,step:document.querySelector('[data-role="position"]')?.textContent}})()`);
  findings.push({example,steps,...state});
  if([1,5,10,15].includes(example)){await scrollTo('.g8-verification','center');await screenshot(`example-${id}-final-verified.png`);}
}

await navigate(15);await finishExample();await click('[data-example-action="practice"]');await waitFor(`document.querySelector('.self-guided-practice')`);
await evaluate(`(()=>{const input=document.querySelector('.practice-answer-input');input.value='wrong';input.dispatchEvent(new Event('input',{bubbles:true}));return true})()`);await click('[data-action="submit"]');await waitFor(`document.querySelector('[data-action="hint"]')`);
await click('[data-action="hint"]');await waitFor(`document.querySelectorAll('[data-role="hints"] p').length===1`);await scrollTo('[data-role="hints"]','center');await screenshot("practice-hint-1.png");
await click('[data-action="hint"]');await waitFor(`document.querySelectorAll('[data-role="hints"] p').length===2`);await scrollTo('[data-role="hints"]','center');await screenshot("practice-hint-2.png");
const hintTerminal=await evaluate(`({count:document.querySelectorAll('[data-role="hints"] p').length,disabled:document.querySelector('[data-action="hint"]')?.disabled,label:document.querySelector('[data-action="hint"]')?.textContent})`);
await click('[data-action="retry"]');await waitFor(`document.querySelectorAll('[data-role="hints"] p').length===0`);await scrollTo('.practice-support','center');await screenshot("practice-hint-reset.png");
await click('.self-guided-practice [data-action="hint"]');await waitFor(`document.querySelectorAll('[data-role="hints"] p').length===1`);await click('.self-guided-practice [data-action="solution"]');await waitFor(`document.querySelector('.worked-solution')`);await click('.practice-navigation [data-action="next"]');await waitFor(`document.querySelector('.practice-progress')?.innerText.includes('Question 2 of 15')`);
const navigationForward=await evaluate(`document.querySelectorAll('[data-role="hints"] p').length`);await click('.practice-navigation [data-action="previous"]');await waitFor(`document.querySelector('.practice-progress')?.innerText.includes('Question 1 of 15')`);const navigationReset=await evaluate(`document.querySelectorAll('[data-role="hints"] p').length`);

await cdp.send("Emulation.setDeviceMetricsOverride",{width:390,height:844,deviceScaleFactor:1,mobile:true});await navigate(1);await screenshotElement("mobile-390-integrated-controls.png",'.whiteboard-control-bar');await finishExample();await scrollTo('.g8-verification','center');await screenshot("mobile-390-final-verified.png");
const mobile390=await evaluate(`({pageOverflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,stageOverflow:document.querySelector('.whiteboard-stage').scrollWidth-document.querySelector('.whiteboard-stage').clientWidth,minTouch:Math.min(...[...document.querySelectorAll('.whiteboard-control-bar button,.whiteboard-control-bar summary')].map(node=>Math.min(node.getBoundingClientRect().width,node.getBoundingClientRect().height)))})`);
await cdp.send("Emulation.setDeviceMetricsOverride",{width:320,height:568,deviceScaleFactor:1,mobile:true});await navigate(1);await screenshotElement("mobile-320-integrated-controls.png",'.whiteboard-control-bar');
const mobile320=await evaluate(`({pageOverflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,stageOverflow:document.querySelector('.whiteboard-stage').scrollWidth-document.querySelector('.whiteboard-stage').clientWidth})`);
await cdp.send("Page.stopScreencast");await delay(200);
writeFileSync(path.join(output,"browser-verification.json"),JSON.stringify({checkedAt:new Date().toISOString(),findings,hintTerminal,navigationForward,navigationReset,mobile390,mobile320},null,2));
if(frames.length)writeFileSync(path.join(output,"examples-01-05-10-15-interactions.avi"),avi(frames,1365,900,10));
cdp.socket.close();chrome.kill();
console.log(JSON.stringify({examples:findings.length,frames:frames.length,hintTerminal,navigationForward,navigationReset,mobile390,mobile320},null,2));
