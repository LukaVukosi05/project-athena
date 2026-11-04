import { spawn } from 'node:child_process';
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const root=path.resolve(import.meta.dirname,'..');
const base=process.env.ATHENA_URL||'http://127.0.0.1:8096';
const port=new URL(base).port||'8096';
const python=process.env.ATHENA_PYTHON||'python';
const server=spawn(python,['-m','uvicorn','app.main:app','--host','127.0.0.1','--port',port],{
    cwd:path.join(root,'backend'),env:{...process.env,ATHENA_JWT_SECRET:'browser-test-local-only',ATHENA_UNLOCK_ALL_LESSONS:'true',ATHENA_DATABASE_URL:'sqlite:////tmp/athena-g9-browser-check.db'},stdio:['ignore','pipe','pipe']});
let serverLog='';server.stderr.on('data',chunk=>{serverLog+=chunk.toString()});
let browser;
try{
  for(let n=0;n<80;n++){
    try{if((await fetch(base+'/api/v1/curriculum/grades/grade-9')).ok)break}catch{}
    if(n===79)throw Error('Server did not start: '+serverLog.slice(-1200));
    await new Promise(resolve=>setTimeout(resolve,250));
  }
  browser=await chromium.launch({headless:true,executablePath:process.env.ATHENA_CHROME_PATH||chromium.executablePath(),args:['--no-sandbox']});
  const out=path.join(root,'artifacts','grade9-topic2-browser');mkdirSync(out,{recursive:true});
  const observations=[];
  for(const width of [1360,390])for(const number of [1,2,3,4,5]){
    const page=await browser.newPage({viewport:{width,height:850},reducedMotion:'reduce'});
    const errors=[];page.on('pageerror',error=>errors.push(error.message));
    const url=`${base}/lesson.html?grade=grade-9&topic=integers&lesson=g9-integers-0${number}`;
    await page.goto(url,{waitUntil:'domcontentloaded'});
    await page.locator('.stateful-whiteboard').waitFor({timeout:20000});
    await page.waitForTimeout(500);
    const initial=await page.evaluate(()=>({
      title:document.querySelector('#lesson-title')?.textContent,
      examples:document.querySelectorAll('[data-example-index]').length,
      board:document.querySelector('.g9-integer-board')?.innerText?.slice(0,500),
      overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,
      stageOverflow:document.querySelector('.whiteboard-stage')?.scrollWidth-document.querySelector('.whiteboard-stage')?.clientWidth,
      primary:document.querySelector('[data-action="primary"]')?.textContent
    }));
    if(!initial.title||!initial.board||errors.length||initial.overflow>1||initial.stageOverflow>1)throw Error(JSON.stringify({width,number,errors,initial}));
    await page.screenshot({path:path.join(out,`lesson-0${number}-${width}-initial.png`),fullPage:false});
    await page.waitForFunction(()=>!document.querySelector('[data-role="example-loading"]')?.textContent?.includes('Loading'),{timeout:18000}).catch(()=>{});
    const loaded=await page.evaluate(()=>({step:document.querySelector('[data-role="position"]')?.textContent,primary:document.querySelector('[data-action="primary"]')?.textContent,error:document.querySelector('[data-role="example-loading"] [role="alert"]')?.textContent}));
    if(loaded.error)throw Error(JSON.stringify({width,number,loaded}));
    observations.push({width,number,initial,loaded,errors});
    await page.close();
  }
  console.log(JSON.stringify({observations,output:out},null,2));
}finally{await browser?.close();server.kill('SIGTERM')}
