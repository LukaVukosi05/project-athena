const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');

const root=path.resolve(__dirname,'../..');
const page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');
const source=fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8');
const lesson=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade8/generated/functions_relationships_03.json'),'utf8'));

test('the served page requests a fresh registry that resolves every Lesson 3 operation',()=>{
  assert.match(page,/js\/whiteboard\/animation-registry\.js\?v=math-whiteboard-v18/);
  const context=vm.createContext({});
  vm.runInContext(source,context);
  for(const question of lesson.worked_examples){
    for(const step of question.steps){
      const operation=`${question.model.family}_step`;
      assert.equal(vm.runInContext(`AthenaWhiteboardRegistry.resolve(${JSON.stringify(operation)}).render instanceof Function`,context),true,`${question.id}: ${operation}`);
    }
  }
});
