const assert = require('assert'), fs = require('fs'), vm = require('vm');
const read = p => fs.readFileSync(`${__dirname}/../${p}`, 'utf8');
const nodes = new Map();
function node(id) { if (!nodes.has(id)) nodes.set(id, {value:'',textContent:'',innerHTML:'',hidden:false,replaceChildren(){this.innerHTML='';},focus(){},append(){}}); return nodes.get(id); }
const mounted=[];
const context={document:{addEventListener(){},getElementById:node,querySelectorAll:()=>[],createElement:()=>node('fresh-host')},URLSearchParams,location:{search:''},history:{replaceState(_a,_b,url){context.url=url;}},escapeHtml:s=>String(s).replace(/</g,'&lt;'),encodeURIComponent,SelfGuidedPractice:class{constructor(host,id){mounted.push(id);}async mountPractice(){}},console};
vm.createContext(context);
vm.runInContext(read('js/pages/practice.js')+'\nglobalThis.hub=PracticeHub;',context);
const hub=context.hub;hub.grade=node('practice-grade');hub.topic=node('practice-topic');
const catalogue=(grade,id)=>({grade,topics:[{id:'topic',title:'A <topic>',lessons:[{id,title:'Existing question set',order:1,question_count:4,choice_count:2},{id:'empty',title:'No bank',order:2,question_count:0,choice_count:0}]}]});
(async()=>{
 hub.grade.value='grade-11';hub.topic.value='topic';hub.catalogue=catalogue(11,'g11-es-01');hub.renderTopic();
 assert(node('practice-lessons').innerHTML.includes('2 multiple-choice · 2 written-answer'));
 assert(!node('practice-lessons').innerHTML.includes('data-practice-lesson="empty"'));
 assert(node('practice-topic-title').textContent==='A <topic>');
 await hub.startLesson(hub.currentTopic().lessons[0]);assert.deepEqual(mounted,['g11-es-01']);assert(context.url.includes('lesson=g11-es-01'));
 assert(node('practice-teaching-link').href==='lesson.html?lesson=g11-es-01');
 // A slower earlier grade request must not replace the current grade.
 const resolvers=[];context.AthenaAuth={fetch:()=>new Promise(r=>resolvers.push(r))};
 hub.grade.value='grade-8';const first=hub.loadGrade('topic');hub.grade.value='grade-12';const second=hub.loadGrade('topic');
 resolvers[1]({ok:true,json:async()=>catalogue(12,'g12-sequences-series-01')});await second;
 resolvers[0]({ok:true,json:async()=>catalogue(8,'g8-algebraic-equations-01')});await first;
 assert(hub.catalogue.grade===12);assert(node('practice-workspace').hidden);
 context.AthenaAuth.fetch=async()=>({ok:false});await hub.loadGrade();assert(node('practice-status').textContent.includes('could not be loaded'));
 const navContext={};vm.createContext(navContext);vm.runInContext(read('js/engine/navigation.js'),navContext);
 assert(navContext.linkFor('Learn')==='index.html');assert(navContext.linkFor('Practice')==='practice.html');assert(read('js/engine/navigation.js').includes('href="index.html" class="topnav__logo"'));
 assert(read('index.html').includes('Understand every step. Recover every mark.'));
 assert(!read('index.html').includes('url=dashboard.html'));
 assert(!read('index.html').includes('id="greeting"'));
 assert(read('js/pages/landing.js').includes('renderNav("Learn")'));
 console.log('Practice hub: authored sets, mixed choices, empty banks, session launch, grade race, retry and navigation passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
