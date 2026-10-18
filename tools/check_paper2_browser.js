/* Focused live desktop/mobile checks for the coordinated Paper 2 batch. */
const fs=require("fs"),path=require("path");
const ROOT=path.resolve(__dirname,"..");
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const packs={
  "g12-statistics-01":JSON.parse(fs.readFileSync(path.join(ROOT,"backend/app/curriculum/grade12/lessons/statistics_regression_pack.json"),"utf8")),
  "g12-analytical-geometry-01":JSON.parse(fs.readFileSync(path.join(ROOT,"backend/app/curriculum/grade12/lessons/analytical_geometry_pack.json"),"utf8")),
};
async function main(){
  const pages=await (await fetch("http://127.0.0.1:9225/json")).json(),page=pages.find(item=>item.type==="page");
  const ws=new WebSocket(page.webSocketDebuggerUrl);let id=0;const pending=new Map(),failures=[];
  ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}};
  await new Promise(resolve=>ws.onopen=resolve);
  const send=(method,params={})=>new Promise((resolve,reject)=>{const call=++id;pending.set(call,{resolve,reject});ws.send(JSON.stringify({id:call,method,params}));});
  const evaluate=async expression=>(await send("Runtime.evaluate",{expression,returnByValue:true,awaitPromise:true})).result.value;
  const waitFor=async expression=>{for(let i=0;i<120;i++){if(await evaluate(expression))return;await sleep(100);}throw new Error(`Timed out: ${expression}`);};
  const navigate=async url=>{await send("Page.navigate",{url});await waitFor("document.readyState==='complete'");await sleep(120);};
  const check=(ok,label)=>{if(!ok)failures.push(label);};
  await send("Page.enable");await send("Runtime.enable");
  await send("Emulation.setDeviceMetricsOverride",{width:1365,height:900,deviceScaleFactor:1,mobile:false});
  await navigate("http://127.0.0.1:8010/grade.html?grade=grade-12");
  await waitFor("document.querySelectorAll('#topics-list .topic-row').length>=7");
  const course=await evaluate("document.querySelector('#topics-list').innerText");
  check(course.indexOf("Statistics and Regression")<course.indexOf("Analytical Geometry"),"course / order / Topics 8 and 9 not ordered");
  check(await evaluate("document.querySelector('#paper-2>h3')?.textContent==='Paper 2'"),"course / Paper 2 section / missing");
  check(await evaluate("[...document.querySelectorAll('#paper-2 .topic-row .badge')].filter(node=>node.textContent==='Paper 2').length===2"),"course / cards / expected two Paper 2 chips");
  for(const [topic,first,last] of [["statistics-regression","g12-statistics-01","g12-statistics-18"],["analytical-geometry","g12-analytical-geometry-01","g12-analytical-geometry-16"]]){
    await navigate(`http://127.0.0.1:8010/topic.html?grade=grade-12&topic=${topic}`);await waitFor("document.querySelectorAll('#lessons-list .topic-row').length>0");
    check(await evaluate("document.querySelector('#topic-paper').textContent==='Paper 2' && document.querySelector('#crumb-paper').textContent==='Paper 2'"),`${topic} / topic / Paper 2 heading or breadcrumb missing`);
    for(const lesson of [first,last]){
      await navigate(`http://127.0.0.1:8010/lesson.html?lesson=${lesson}`);await waitFor("Boolean(document.querySelector('.whiteboard-stage'))");
      check(await evaluate("document.querySelector('#lesson-paper').textContent==='Paper 2' && document.querySelector('#crumb-paper').textContent==='Paper 2'"),`${topic} / ${lesson} / Paper 2 heading or breadcrumb missing`);
      check((await evaluate("document.querySelector('.whiteboard-stage').innerText")).trim().length>20,`${topic} / ${lesson} / safe fallback unreadable`);
    }
  }
  for(const lesson of Object.keys(packs)){
    for(let example=1;example<=10;example++){
      await navigate(`http://127.0.0.1:8010/lesson.html?lesson=${lesson}&example=${example}&step=0`);await waitFor("Boolean(document.querySelector('.whiteboard-stage'))");
      check((await evaluate("document.querySelector('.example-progress').innerText")).includes(`Example ${example} of 10`),`${lesson} / example ${example} / navigation failed`);
      const before=await evaluate("document.querySelector('.whiteboard-stage').innerText");
      await evaluate("document.querySelector('[data-action=next]').click()");await sleep(1050);
      const after=await evaluate("document.querySelector('.whiteboard-stage').innerText");
      check(before!==after,`${lesson} / example ${example} / fallback did not advance`);
    }
    await navigate(`http://127.0.0.1:8010/lesson.html?lesson=${lesson}&example=1&step=1`);await waitFor("Boolean(document.querySelector('[data-example-action=practice]'))");
    await evaluate("document.querySelector('[data-example-action=practice]').click()");await waitFor("Boolean(document.querySelector('.self-guided-practice'))");
    const answers=packs[lesson].lessons[0].practice_questions.map(item=>item["Answer / feedback route"].split(/(?<=[.!?])\s+/)[0].slice(0,500));
    for(let question=1;question<=12;question++){
      check((await evaluate("document.querySelector('.practice-progress').innerText")).includes(`Question ${question} of 12`),`${lesson} / practice ${question} / navigation failed`);
      check(!await evaluate("document.querySelector('[data-role=solution]')?.innerText.includes('Worked Solution')"),`${lesson} / practice ${question} / answer visible before submission`);
      const answer=JSON.stringify(answers[question-1]);
      await evaluate(`(()=>{const input=document.querySelector('.practice-answer-input');input.value=${answer};input.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('[data-role=answer-form]').requestSubmit();return true})()`);
      try{await waitFor("document.querySelector('[data-role=feedback]').innerText.includes('Correct')");}
      catch(error){throw new Error(`${lesson} practice ${question}: ${await evaluate("document.querySelector('.practice-focus')?.innerText")}`);}
      if(question<12){await evaluate("document.querySelector('.self-guided-practice [data-action=next]').click()");await sleep(80);}
    }
  }
  await send("Emulation.setDeviceMetricsOverride",{width:390,height:844,deviceScaleFactor:1,mobile:true});
  for(const url of ["grade.html?grade=grade-12","topic.html?grade=grade-12&topic=statistics-regression","lesson.html?lesson=g12-statistics-01","topic.html?grade=grade-12&topic=analytical-geometry","lesson.html?lesson=g12-analytical-geometry-01","lesson.html?lesson=g12-sequences-series-01"]){
    await navigate(`http://127.0.0.1:8010/${url}`);
    check(await evaluate("document.documentElement.scrollWidth<=document.documentElement.clientWidth"),`${url} / mobile / horizontal clipping`);
  }
  ws.close();console.log(JSON.stringify({desktop_topics:2,opened_lessons:4,guided_examples:20,practice_questions:24,mobile_pages:6,failures},null,2));
  if(failures.length)process.exitCode=1;
}
main().catch(error=>{console.error(error);process.exit(1);});
