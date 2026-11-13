const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
const source=fs.readFileSync(path.join(root,'frontend/js/whiteboard/animation-registry.js'),'utf8');
const page=fs.readFileSync(path.join(root,'frontend/lesson.html'),'utf8');
const context=vm.createContext({});
vm.runInContext(source,context);

test('all 90 Grade 9 Topic 7 examples resolve their actual whiteboard operation',()=>{
  assert.match(page,/animation-registry\.js\?v=math-whiteboard-v22/);
  assert.match(page,/grade9-equation-renderers\.js/);
  for(let lesson=1;lesson<=6;lesson++){
    const data=JSON.parse(fs.readFileSync(path.join(root,'backend/app/curriculum/grade9/generated',
      `equations_${String(lesson).padStart(2,'0')}.json`),'utf8'));
    assert.equal(data.worked.length,15);
    const operation=`grade9_equation_${lesson}_step`;
    const renderer=vm.runInContext(`AthenaWhiteboardRegistry.resolve(${JSON.stringify(operation)})`,context);
    for(const example of data.worked)for(let index=0;index<example.actions.length;index++){
      const step={operation:{type:operation,value:example.actions[index]},
        before_expression:index?example.actions[index-1]:example.problem,
        working_expression:example.actions[index],after_expression:example.actions[index]};
      assert.equal(renderer.render(step,'ready',{hasVisualization:true}), '',example.id);
      assert.equal(renderer.render(step,'operation',{hasVisualization:true}), '',example.id);
      assert.equal(renderer.render(step,'result',{hasVisualization:true}), '',example.id);
    }
  }
});
