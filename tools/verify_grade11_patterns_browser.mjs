import {spawn} from 'node:child_process';
import {createRequire} from 'node:module';
import path from 'node:path';
import os from 'node:os';
const require=createRequire(import.meta.url),{chromium}=require('playwright');
const root=path.resolve(import.meta.dirname,'..'),base=process.env.ATHENA_URL||'http://127.0.0.1:8121';
const port=new URL(base).port||'8121';
const dbPath=path.join(os.tmpdir(),'athena-g11-pat-browser.db').replace(/\\/g,'/');
const dbUrl=process.platform==='win32'?`sqlite:///${dbPath}`:`sqlite:////${dbPath.replace(/^\//,'')}`;
const server=spawn(process.env.ATHENA_PYTHON||'python',['-m','uvicorn','app.main:app','--host','127.0.0.1','--port',port],{
  cwd:path.join(root,'backend'),env:{...process.env,ATHENA_JWT_SECRET:'browser-test-local-only',
    ATHENA_UNLOCK_ALL_LESSONS:'true',ATHENA_DATABASE_URL:dbUrl},stdio:['ignore','pipe','pipe']});
let log='';server.stderr.on('data',chunk=>log+=chunk.toString());let browser;
try{
  for(let i=0;i<100;i++){
    try{if((await fetch(base+'/api/v1/curriculum/grades/grade-11')).ok)break}catch{}
    if(i===99)throw Error(`Server did not start: ${log.slice(-1200)}`);
    await new Promise(resolve=>setTimeout(resolve,250));
  }
  browser=await chromium.launch({headless:true,executablePath:process.env.ATHENA_CHROME_PATH||chromium.executablePath(),args:['--no-sandbox']});
  const outcomes=[];
  for(const width of [1360,390])for(let number=1;number<=5;number++){
    const page=await browser.newPage({viewport:{width,height:850},reducedMotion:'reduce'}),errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    const lesson=`g11-pat-${String(number).padStart(2,'0')}`;
    await page.goto(`${base}/lesson.html?grade=grade-11&topic=quadratic-number-patterns&lesson=${lesson}`);
    await page.locator('.g11-pat-board').waitFor({timeout:20000});
    const details=await page.evaluate(()=>({
      trace:document.querySelector('[aria-label="Written solution so far"]')?.textContent,
      title:document.querySelector('#lesson-title')?.textContent,
      board:document.querySelector('.g11-pat-board')?.textContent?.slice(0,130),
      examples:document.querySelectorAll('[data-example-index]').length,
      stage:document.querySelector('[data-role="position"]')?.textContent,
      overflow:document.documentElement.scrollWidth-document.documentElement.clientWidth,
      stageOverflow:document.querySelector('.whiteboard-stage')?.scrollWidth-document.querySelector('.whiteboard-stage')?.clientWidth,
      fallback:document.querySelector('.whiteboard-stage')?.textContent?.includes('Diagram unavailable'),
      error:document.querySelector('[data-role="example-loading"] [role="alert"]')?.textContent
    }));
    if(errors.length||details.examples!==15||!details.title||!details.trace||details.fallback||details.error||details.overflow>1||details.stageOverflow>1)
      throw Error(JSON.stringify({width,lesson,errors,details}));
    await page.locator('[data-example-index="14"]').click();
    await page.waitForFunction(()=>document.querySelector('[data-example-index="14"]')?.getAttribute('aria-current')==='step',{timeout:10000});
    const last=await page.locator('.g11-pat-board').getAttribute('data-question-id');
    if(last!==`g11-pat-l${String(number).padStart(2,'0')}-w15`)throw Error(JSON.stringify({width,lesson,last}));
    outcomes.push({width,lesson,examples:details.examples,overflow:details.overflow,stageOverflow:details.stageOverflow,last});
    await page.close();
  }
  console.log(JSON.stringify({pages:outcomes.length,outcomes},null,2));
}finally{await browser?.close();server.kill('SIGTERM')}
