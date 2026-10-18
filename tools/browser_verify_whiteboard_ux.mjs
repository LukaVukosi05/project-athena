import fs from "node:fs";
import path from "node:path";

const origin="http://127.0.0.1:8000";
const output=path.resolve("artifacts/grade8-algebraic-equations-lesson1/ux-repair");
fs.mkdirSync(output,{recursive:true});
const targets=await (await fetch("http://127.0.0.1:9222/json")).json();
const target=targets.find(item=>item.type==="page");
if(!target)throw new Error("No Chrome page target");
const socket=new WebSocket(target.webSocketDebuggerUrl);await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject;});
let sequence=0;const pending=new Map();socket.onmessage=event=>{const message=JSON.parse(event.data);if(!message.id||!pending.has(message.id))return;const task=pending.get(message.id);pending.delete(message.id);message.error?task.reject(new Error(message.error.message)):task.resolve(message.result);};
const command=(method,params={})=>new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function evaluate(expression,awaitPromise=false){const result=await command("Runtime.evaluate",{expression,awaitPromise,returnByValue:true});if(result.exceptionDetails)throw new Error(result.exceptionDetails.exception?.description||result.exceptionDetails.text);return result.result.value;}
async function viewport(width,height,mobile=false){await command("Emulation.setDeviceMetricsOverride",{width,height,deviceScaleFactor:1,mobile});}
async function navigate(url){await command("Page.navigate",{url});await delay(900);}
async function shot(name,video=false){const result=await command("Page.captureScreenshot",{format:"png",captureBeyondViewport:false});const data=Buffer.from(result.data,"base64");fs.writeFileSync(path.join(output,name),data);if(video)videoFrames.push(result.data);}
async function click(selector){return evaluate(`(()=>{const node=document.querySelector(${JSON.stringify(selector)});if(!node)throw new Error('Missing ${selector}');node.click();return true})()`);}
async function audit(label){const result=await evaluate(`(()=>{const stage=document.querySelector('.whiteboard-stage'),page=document.documentElement,buttons=[...document.querySelectorAll('.whiteboard-control-bar button,.whiteboard-control-bar summary')].filter(node=>node.offsetParent!==null),primary=document.querySelector('[data-action="primary"]');return {label:${JSON.stringify(label)},pageWidth:page.clientWidth,pageScrollWidth:page.scrollWidth,stageWidth:stage?.clientWidth,stageScrollWidth:stage?.scrollWidth,stageHeight:stage?.clientHeight,primary:primary?.textContent,state:document.querySelector('.stateful-whiteboard')?.dataset.controllerState,position:document.querySelector('[data-role="position"]')?.textContent,caption:document.querySelector('[data-role="caption"]')?.textContent,missing:stage?.dataset.missingTargets||'',touch:buttons.every(node=>{const r=node.getBoundingClientRect();return r.width>=44&&r.height>=44;}),notesOpen:document.querySelector('.whiteboard-teaching-notes')?.open,primaryCount:[...document.querySelectorAll('.whiteboard-control-bar .btn-primary')].filter(node=>node.offsetParent!==null).length};})()`);if(result.pageScrollWidth>result.pageWidth+1||result.stageScrollWidth>result.stageWidth+1||result.missing||!result.touch||result.primaryCount!==1)throw new Error(`UX audit failed ${JSON.stringify(result)}`);return result;}

await command("Page.enable");await command("Runtime.enable");await command("Emulation.setEmulatedMedia",{features:[{name:"prefers-reduced-motion",value:"no-preference"}]});
const lesson=`${origin}/lesson.html?grade=grade-8&topic=algebraic-equations&lesson=g8-algebraic-equations-01`;
const videoFrames=[];const reports=[];
await viewport(1440,1000);await navigate(lesson);await click('[data-example-action="reveal"]');await delay(250);await evaluate(`document.querySelector('.whiteboard-question-set').scrollIntoView({block:'start'})`);await delay(120);
reports.push(await audit("desktop-initial"));await shot("desktop-initial.png",true);
await click('[data-action="primary"]');await delay(120);let state=await audit("playing");if(state.primary!=="Pause"||state.state!=="playing")throw new Error("Start did not enter playing");await shot("interaction-start.png",true);
await click('[data-action="primary"]');state=await audit("paused");if(state.primary!=="Continue"||state.state!=="paused")throw new Error("Pause did not enter paused");await shot("interaction-pause.png",true);
await click('[data-action="primary"]');state=await audit("continued");if(state.primary!=="Pause"||state.state!=="playing")throw new Error("Continue did not resume");await shot("interaction-continue.png",true);
await click('[data-action="primary"]');await click('.whiteboard-settings>summary');await click('[data-action="reduced-motion"]');await click('[data-action="restart"]');await click('.whiteboard-settings>summary');
await click('[data-action="primary"]');await delay(60);state=await audit("step-1-complete");if(state.primary!=="Next step"||state.position!=="Step 1 of 6")throw new Error(`Step one did not complete: ${JSON.stringify(state)}`);const before=await evaluate(`document.querySelector('.whiteboard-stage').innerHTML`);const beforeCaption=state.caption;await shot("desktop-step-1.png",true);
await click('[data-action="primary"]');await delay(30);state=await audit("next-step");const after=await evaluate(`document.querySelector('.whiteboard-stage').innerHTML`);if(state.position!=="Step 2 of 6"||state.primary!=="Start"||before===after||beforeCaption===state.caption)throw new Error(`Next step regression: ${JSON.stringify(state)}`);await shot("desktop-step-2.png",true);
await click('[data-action="primary"]');await click('[data-action="previous"]');state=await audit("previous-step");if(state.position!=="Step 1 of 6"||state.primary!=="Next step")throw new Error("Previous step failed");await shot("interaction-previous.png",true);
const replayBefore=await evaluate(`document.querySelector('.whiteboard-stage').innerHTML`);await click('[data-action="replay"]');const replayAfter=await evaluate(`document.querySelector('.whiteboard-stage').innerHTML`);if(replayBefore!==replayAfter)throw new Error("Reduced-motion replay was not deterministic");await shot("interaction-replay.png",true);

const exampleAudits=[];
for(let example=0;example<15;example++){
  if(example>0){await click('[data-example-action="reveal"]');await delay(80);await click('.whiteboard-settings>summary');const reduced=await evaluate(`document.querySelector('[data-action="reduced-motion"]').checked`);if(!reduced)await click('[data-action="reduced-motion"]');await click('.whiteboard-settings>summary');}
  let guard=0;
  while((await evaluate(`document.querySelector('.stateful-whiteboard').dataset.controllerState`))!=="example_complete"&&guard++<30)await click('[data-action="primary"]');
  const check=await audit(`example-${example+1}-final`);if(check.state!=="example_complete")throw new Error(`Example ${example+1} did not finish`);exampleAudits.push(check);
  if(example===0){await shot("desktop-final.png",true);await click('.whiteboard-teaching-notes>summary');const widthBefore=await evaluate(`document.querySelector('.whiteboard-stage').clientWidth`);await shot("desktop-teaching-notes-open.png");const widthAfter=await evaluate(`document.querySelector('.whiteboard-stage').clientWidth`);if(widthBefore!==widthAfter)throw new Error("Teaching notes resized stage");await click('.whiteboard-teaching-notes>summary');}
  if(example<14)await click('[data-action="primary"]');
}

for(const [width,height] of [[320,568],[360,800],[390,844],[412,915]]){
  await viewport(width,height,true);await navigate(`${lesson}&example=1&step=0`);await click('[data-example-action="reveal"]');await delay(120);await evaluate(`document.querySelector('.whiteboard-question-set').scrollIntoView({block:'start'})`);await delay(60);
  const mobile=await audit(`mobile-${width}-initial`);reports.push(mobile);if(width===320)await shot("mobile-320-initial.png");if(width===390)await shot("mobile-390-initial.png");
  if(width===412){await evaluate(`document.querySelector('[data-action="primary"]').focus()`);await command("Input.dispatchKeyEvent",{type:"rawKeyDown",key:"Enter",code:"Enter",windowsVirtualKeyCode:13,nativeVirtualKeyCode:13});await command("Input.dispatchKeyEvent",{type:"char",text:"\r",key:"Enter",code:"Enter",windowsVirtualKeyCode:13});await command("Input.dispatchKeyEvent",{type:"keyUp",key:"Enter",code:"Enter",windowsVirtualKeyCode:13,nativeVirtualKeyCode:13});await delay(30);const keyboard=await audit("mobile-412-keyboard");reports.push(keyboard);if(keyboard.state!=="playing")throw new Error(`Keyboard activation failed: ${JSON.stringify(keyboard)}`);await click('[data-action="primary"]');}
  await click('.whiteboard-settings>summary');await click('[data-action="reduced-motion"]');if(width===412)await click('[data-action="restart"]');await click('.whiteboard-settings>summary');await click('[data-action="primary"]');await delay(30);reports.push(await audit(`mobile-${width}-step`));if(width===320)await shot("mobile-320-step.png");
  let guard=0;while((await evaluate(`document.querySelector('.stateful-whiteboard').dataset.controllerState`))!=="example_complete"&&guard++<20)await click('[data-action="primary"]');
  reports.push(await audit(`mobile-${width}-final`));if(width===390)await shot("mobile-390-final.png");
}

const video=await evaluate(`(async()=>{const frames=${JSON.stringify(videoFrames)};const canvas=document.createElement('canvas');canvas.width=960;canvas.height=667;const ctx=canvas.getContext('2d');const stream=canvas.captureStream(4);const recorder=new MediaRecorder(stream,{mimeType:'video/webm'});const chunks=[];recorder.ondataavailable=e=>chunks.push(e.data);const stopped=new Promise(resolve=>recorder.onstop=resolve);recorder.start();for(const frame of frames){const image=new Image();image.src='data:image/png;base64,'+frame;await image.decode();ctx.drawImage(image,0,0,canvas.width,canvas.height);await new Promise(resolve=>setTimeout(resolve,650));}recorder.stop();await stopped;const bytes=new Uint8Array(await new Blob(chunks,{type:'video/webm'}).arrayBuffer());let binary='';for(let i=0;i<bytes.length;i+=8192)binary+=String.fromCharCode(...bytes.subarray(i,i+8192));return btoa(binary);})()`,true);
fs.writeFileSync(path.join(output,"whiteboard-controls-interaction.webm"),Buffer.from(video,"base64"));
fs.writeFileSync(path.join(output,"verification.json"),JSON.stringify({reports,exampleAudits},null,2));
console.log(JSON.stringify({reports,examples:exampleAudits.length,files:fs.readdirSync(output)},null,2));socket.close();
