const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const root=path.resolve(__dirname,"..");
const src=fs.readFileSync(path.join(root,"js/math/math-notation.js"),"utf8");
const notation=vm.runInNewContext(src+"\nAthenaMathNotation");
const first=notation.html("Evaluate 27^(1/3) using the positive third root.");
assert.match(first, /27<sup><span class="athena-power-fraction"/);
assert.match(first, /<span>1<\/span><span>3<\/span>/);
assert.doesNotMatch(first, /\^/);
assert.match(notation.html("Check 3^3 = 27"), /3<sup aria-hidden="true">3<\/sup>/);
assert.match(notation.html("x^(2/3) × x^(-1)"), /class="athena-power-fraction"/);
assert.match(notation.html("<img src=x onerror=1>^2"), /&lt;img/);
assert.doesNotMatch(notation.html("<img src=x onerror=1>^2"), /<img/);
for(let n=1;n<=6;n++){
  const bank=JSON.parse(fs.readFileSync(path.join(root,`../backend/app/curriculum/grade11/generated/exponents_surds_${String(n).padStart(2,"0")}.json`),"utf8"));
  for(const scene of bank.worked){
    assert.doesNotMatch(notation.html(scene.problem),/\^/,scene.id);
    for(const action of scene.actions)assert.doesNotMatch(notation.html(action),/\^/,scene.id);
  }
  for(const section of ["practice","mastery","reassessment"]){
    for(const item of bank[section]){
      assert.doesNotMatch(notation.html(item.prompt),/\^/,item.id);
      for(const option of item.options)assert.doesNotMatch(notation.html(option),/\^/,item.id);
    }
  }
}
const lesson=fs.readFileSync(path.join(root,"lesson.html"),"utf8");
assert.match(lesson,/js\/math\/math-notation\.js\?v=g11-math-v1/);
console.log("Grade 11 powers render with superscripts throughout teaching and assessment");
