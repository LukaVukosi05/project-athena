/* Question-specific exponents and surds stages; preserve earlier mathematical marks. */
(() => {
  const esc = value => escapeWhiteboardHtml(String(value ?? ""));
  const math = value => typeof AthenaMathNotation !== "undefined" ? AthenaMathNotation.html(value) : esc(value);
  const text = (id,x,y,value,css="g11-label") =>
    `<text data-object-id="${id}" x="${x}" y="${y}" class="${css}">${esc(value)}</text>`;
  const rect = (id,x,y,w,css="g11-card") =>
    `<rect data-object-id="${id}" x="${x}" y="${y}" width="${w}" height="64" rx="10" class="${css}"/>`;
  const card = (id,x,y,label,w=126,css="g11-card") =>
    rect(id,x,y,w,css)+text(id+"-label",x+10,y+39,label);
  function stage(state,phase) {
    const tag=(state.annotations||[]).find(item=>/^stage:\d+$/.test(item));
    const n=Number(tag?.slice(6)||0);
    return phase==="result" ? n : Math.max(0,n-1);
  }
  function diagram(v,n,s) {
    let out = "";
    if(n===1) {
      out += card("base",15,55,String(v.base),110);
      if(s>=1)out+=text("index",155,91,`root index ${v.index}`);
      if(s>=2)out+=`<path d="M123 88 H135" class="g11-connector"/>`+card("root",220,55,s>=3?String(v.root):"?",100,"g11-card g11-active");
      if(s>=4)out+=card("power",360,55,`power ${v.power}`,110);
      if(s>=5)out+=`<text data-object-id="check" x="25" y="205" class="g11-label">Check: ${esc(v.root)}<tspan baseline-shift="super" font-size="12">${esc(v.index)}</tspan><tspan baseline-shift="baseline"> = ${esc(v.base)}</tspan></text>`;
    } else if(n===2) {
      out+=card("first",10,50,`+${v.a}/${v.denominator}`);
      out+=card("second",180,50,`+${v.b}/${v.denominator}`);
      out+=card("third",350,50,`−${v.c}/${v.denominator}`);
      if(s>=2)out+=text("sum",25,177,`Multiply: add ${v.a} + ${v.b}`);
      if(s>=3)out+=text("subtract",25,213,`Divide: subtract ${v.c}`);
      if(s>=5)out+=text("domain",25,259,"Domain: x > 0");
    } else if(n===3) {
      out+=card("radicand",25,45,`√${v.radicand}`);
      if(s>=1)out+=card("square",186,45,String(v.square),"110","g11-card g11-active");
      if(s>=2)out+=card("remainder",355,45,`√${v.remainder}`,110);
      if(s>=3)out+=text("pair",35,172,`√${v.square} = ${v.outside}`);
      if(s>=5)out+=text("check",35,213,`Square: (${v.outside}√${v.remainder})² = ${v.radicand}`);
    } else if(n===4) {
      out+=card("first",12,48,`${v.a}√${v.factor*v.factor*v.radicand}`,185);
      out+=card("second",295,48,`${v.subtract?"−":"+"} ${v.b}√${v.radicand}`,185);
      if(s>=2)out+=text("factor",24,174,`√${v.factor*v.factor*v.radicand} = ${v.factor}√${v.radicand}`);
      if(s>=3)out+=text("coefficient",24,215,`${v.a} × ${v.factor} = ${v.a*v.factor}`);
      if(s>=4)out+=text("combine",24,256,`Combine like √${v.radicand} terms`);
    } else if(n===5) {
      out+=card("numerator",135,20,String(v.numerator),230);
      out+=`<path d="M135 105 H365" class="g11-connector"/>`;
      out+=card("denominator",135,115,`√${v.radicand}`,230);
      if(s>=2)out+=text("multiply",25,225,`Multiply top and bottom by √${v.radicand}`);
      if(s>=4)out+=text("denominator-square",25,264,`(√${v.radicand})² = ${v.radicand}`);
    } else {
      out+=card("left",10,62,`√(x + ${v.offset})`,208);
      out+=text("equals",245,101,"=");
      out+=card("right",290,62,`x − ${v.rhs_offset}`,195);
      if(s>=1)out+=text("domain",20,171,`x ≥ ${v.rhs_offset}`);
      if(s>=2)out+=text("square",20,213,"Square both sides; keep the original equation.");
      if(s>=3)out+=text("candidates",20,254,"Test both quadratic candidates in the original.");
      if(s>=5)out+=text("valid",20,291,`Accept ${v.valid}; reject ${v.rejected}`);
    }
    return out;
  }
  function render(parameters,state,phase,n) {
    const scene=JSON.parse(parameters.scene_json),v=scene.visual?.values;
    if(!v || scene.id!==parameters.question_id || scene.lesson!==n || v.lesson!==n ||
       scene.problem!==parameters.prompt)throw Error("Grade 11 visual belongs to another question");
    const s=stage(state,phase);
    return `<section class="g11-board" data-managed-visibility="true" data-question-id="${esc(scene.id)}">
      <p data-object-id="problem">${math(scene.problem)}</p>
      <div class="g11-model" data-object-id="model"><svg viewBox="0 0 500 315" role="img" aria-label="${esc(scene.problem)}">
        <title>Exponents and surds, stage ${s} of 5</title>${diagram(v,n,s)}</svg></div>
      <p data-object-id="operation">${phase==="operation"?math(state.working_state):""}</p>
      <p data-object-id="result">${phase==="result" && s<5?math(state.after_state):""}</p>
      <p data-object-id="verification">${phase==="result" && s===5?math(state.after_state):""}</p>
    </section>`;
  }
  for(let n=1;n<=6;n++)AthenaVisualizationRegistry.register("algebra",`grade11_es_${n}`,
    {render:(p,s,phase)=>render(p,s,phase,n),destroy(){}});
})();
