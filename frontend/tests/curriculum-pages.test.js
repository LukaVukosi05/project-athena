const assert=require('assert'),fs=require('fs'),vm=require('vm');
const host={innerHTML:''};let ready;
const grades=[{id:'grade-8',grade:8,curriculum:'CAPS',availability:'available',topic_count:13,expected_lesson_count:81,published_interactive_lesson_count:10,interactive_lesson_count:81},{id:'grade-11',grade:11,curriculum:'CAPS',availability:'available',topic_count:12,expected_lesson_count:76,published_interactive_lesson_count:0,interactive_lesson_count:76}];
const c={document:{addEventListener:(_n,f)=>ready=f,getElementById:()=>host},AthenaAuth:{restoreSession:async()=>null},renderNav(){},fetch:async()=>({ok:true,json:async()=>grades}),encodeURIComponent};
vm.createContext(c);vm.runInContext(fs.readFileSync(__dirname+'/../js/pages/landing.js','utf8'),c);
(async()=>{await ready();assert(host.innerHTML.includes('Grade 8'));assert(host.innerHTML.includes('grade=grade-11'));assert(host.innerHTML.includes('76'));c.fetch=async()=>({ok:false,status:503});await ready();assert(host.innerHTML.includes('Curriculum could not be loaded'));assert(!host.innerHTML.includes('grade=grade-11'));console.log('Landing catalogue uses current backend grades and replaces stale results on failure');})().catch(e=>{console.error(e);process.exitCode=1;});
// Signed-in active members get a useful onward action instead of a second trial.
(async()=>{
 const nodes=new Map(); const n=id=>{if(!nodes.has(id))nodes.set(id,{innerHTML:'',textContent:'',href:''});return nodes.get(id);};let init;
 const signed={document:{addEventListener:(_n,f)=>init=f,getElementById:n},AthenaAuth:{restoreSession:async()=>({grade:'grade-9'}),request:async()=>({has_access:true})},AthenaOffer:{setAccess(){}},renderNav(){},fetch:async()=>({ok:true,json:async()=>grades}),encodeURIComponent};
 vm.createContext(signed);vm.runInContext(fs.readFileSync(__dirname+'/../js/pages/landing.js','utf8'),signed);await init();
 assert.equal(n('landing-primary-cta').textContent,'Continue learning');assert.equal(n('landing-primary-cta').href,'grade.html?grade=grade-9');assert.equal(n('landing-account-link').href,'account.html');
})().catch(e=>{console.error(e);process.exitCode=1;});
