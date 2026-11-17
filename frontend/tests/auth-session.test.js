const {test}=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../js/engine/state.js'),'utf8');
const user={id:1,first_name:'Lerato',email:'lerato@example.com',grade:'grade-11',curriculum_mode:'CAPS',role:'learner',is_premium:false};
const response=(status,data)=>({ok:status>=200&&status<300,status,json:async()=>data});
function browser(fetch,shared=new Map()){
 const storage=map=>({getItem:key=>map.get(key)||null,setItem:(key,value)=>map.set(key,value),removeItem:key=>map.delete(key)});
 const location={origin:'http://127.0.0.1:8000',href:'http://127.0.0.1:8000/account.html',pathname:'/account.html',search:''};
 const notices=[];
 const context=vm.createContext({fetch,localStorage:storage(shared),sessionStorage:storage(new Map()),location,URL,URLSearchParams,console,window:{addEventListener(){}},document:{querySelector:()=>({prepend:n=>notices.push(n)}),createElement:()=>({setAttribute(){}})}});
 vm.runInContext(source,context);
 return {auth:vm.runInContext('AthenaAuth',context),state:vm.runInContext('AthenaState',context),location,shared,notices};
}

test('a new tab restores through the cookie without putting tokens in localStorage',async()=>{
 const first=browser(async()=>response(200,{access_token:'token-one',user}));
 await first.auth.login({email:user.email,password:'secret',rememberMe:true});
 assert.equal(JSON.parse(first.shared.get('athena_v1_state')).accessToken,null);
 const calls=[];const second=browser(async(p,o)=>{calls.push([p,o]);return response(200,{access_token:'new-tab-token',user});},first.shared);
 assert.equal(second.state.accessToken(),null);
 assert.equal((await second.auth.restoreSession()).email,user.email);
 assert.equal(calls[0][0],'/api/v1/auth/refresh');
 assert.equal(second.state.accessToken(),'new-tab-token');
});

test('temporary server and network failures preserve a signed-in user',async()=>{
 const page=browser(async()=>response(503,{detail:'Try later'}));page.state.setSession({access_token:'existing',user});
 await assert.rejects(page.auth.restoreSession());assert.equal(page.state.accessToken(),'existing');assert.equal(page.state.get().user.email,user.email);
 const original=page.location.href;await page.auth.requireSession();assert.equal(page.location.href,original);assert.equal(page.notices.length,1);
});

test('expired bearer token is renewed once and the original request is retried',async()=>{
 const calls=[];let checks=0;
 const page=browser(async(p,o)=>{calls.push([p,o]);if(p.endsWith('/refresh'))return response(200,{access_token:'fresh',user});return ++checks===1?response(401,{}):response(200,user);});
 page.state.setSession({access_token:'expired',user});
 assert.equal((await page.auth.restoreSession()).email,user.email);
 assert.equal(calls.length,3);assert.equal(calls[2][1].headers.Authorization,'Bearer fresh');
});

test('concurrent renewal is deduplicated and an invalid cookie clears the session',async()=>{
 let calls=0;const page=browser(async()=>{calls++;return response(200,{access_token:'shared',user});});
 await Promise.all([page.auth.renewSession(),page.auth.renewSession()]);assert.equal(calls,1);
 const invalid=browser(async()=>response(401,{}));invalid.state.setSession({access_token:'old',user});
 assert.equal(await invalid.auth.renewSession(),null);assert.equal(invalid.state.get().user,null);
});

test('next destination cannot leave Athena',()=>{
 const page=browser(()=>{});
 for(const url of ['//evil.example','https://evil.example','/\\evil.example','/\nevil'])assert.equal(page.auth.safeNext(url),'/index.html');
 assert.equal(page.auth.safeNext('/lesson.html?lesson=g8-algebraic-equations-01'),'/lesson.html?lesson=g8-algebraic-equations-01');
});

test('sign-in routes new members to the offer and active members to the agreed home',async()=>{
 const fresh=browser(async()=>response(200,{has_access:false}));
 assert.equal(await fresh.auth.afterSignIn(null),'/checkout.html?next=%2Findex.html');
 assert.equal(await fresh.auth.afterSignIn('/dashboard.html'),'/checkout.html?next=%2Findex.html');
 assert.equal(await fresh.auth.afterSignIn('/lesson.html?lesson=g11-es-01'),'/checkout.html?next=%2Flesson.html%3Flesson%3Dg11-es-01');
 const active=browser(async()=>response(200,{has_access:true}));
 assert.equal(await active.auth.afterSignIn(null),'/index.html');
 assert.equal(await active.auth.afterSignIn('/checkout.html'),'/index.html');
 assert.equal(await active.auth.afterSignIn('/dashboard.html'),'/index.html');
 const offline=browser(async()=>{throw new Error('offline');});
 offline.state.setSession({access_token:'kept',user});
 assert.equal(await offline.auth.afterSignIn(null),'/checkout.html?next=%2Findex.html');
 assert.equal(offline.state.accessToken(),'kept');
});

test('every successful email and social sign-in path uses the membership decision',()=>{
 for(const file of ['login.js','signup.js','oauth-onboarding.js']){
  const source=fs.readFileSync(path.join(__dirname,'../js/pages',file),'utf8');
  assert(source.includes('AthenaAuth.afterSignIn('),file);
  assert(!source.includes('location.href = "dashboard.html"'),file);
 }
});
