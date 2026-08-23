class VisualizationRegistry {
  constructor() { this.renderers = new Map(); }
  key(type, template) { return `${type}:${template}`; }
  register(type, template, renderer) { const key=this.key(type,template); if(this.renderers.has(key)) throw new Error(`Duplicate visualization template: ${key}`); this.renderers.set(key,renderer); }
  render(instruction, step, phase) { const renderer=this.renderers.get(this.key(instruction.type,instruction.template)); if(!renderer) throw new Error(`Unsupported visualization: ${instruction.type}:${instruction.template}`); return renderer.render(instruction.parameters,step.visualization_state||{},phase); }
}
const AthenaVisualizationRegistry = new VisualizationRegistry();
const GeometryPrimitives = {
  point(p,label,c=""){return `<g class="geometry-point ${c}"><circle cx="${p.x}" cy="${p.y}" r="5"/><text x="${p.x+8}" y="${p.y-8}">${label}</text></g>`;},
  segment(a,b,c=""){return `<line class="geometry-segment ${c}" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"/>`;},
  circle(o,r){return `<circle class="geometry-circle" cx="${o.x}" cy="${o.y}" r="${r}"/>`;},
  arc(o,r,startDegrees,endDegrees,c=""){const p=d=>({x:o.x+r*Math.cos(d*Math.PI/180),y:o.y-r*Math.sin(d*Math.PI/180)}),a=p(startDegrees),b=p(endDegrees),large=Math.abs(endDegrees-startDegrees)>180?1:0;return `<path class="geometry-arc ${c}" d="M ${a.x} ${a.y} A ${r} ${r} 0 ${large} 0 ${b.x} ${b.y}"/>`;},
  angle(o,from,to,r,label,c=""){return `<g class="geometry-angle ${c}">${this.arc(o,r,from,to,"angle-mark")}<text x="${o.x}" y="${o.y-r-8}" text-anchor="middle">${label}</text></g>`;}
};
AthenaVisualizationRegistry.register("geometry","central_angle_theorem",{render(parameters,state,phase){
  const central=Number(parameters.central_angle),target=central/2,O={x:210,y:145},r=105,on=d=>({x:O.x+r*Math.cos(d*Math.PI/180),y:O.y-r*Math.sin(d*Math.PI/180)}),A=on(140),B=on(40),C=on(270),visible=new Set(state.objects||[]),high=new Set(state.highlights||[]),notes=new Set(state.annotations||[]),active=n=>high.has(n)?"is-highlighted":"";
  const objects=[];
  if(visible.has("circle"))objects.push(GeometryPrimitives.circle(O,r));
  if(visible.has("radii"))objects.push(GeometryPrimitives.segment(O,A,active("central_angle")),GeometryPrimitives.segment(O,B,active("central_angle")));
  if(visible.has("chords"))objects.push(GeometryPrimitives.segment(C,A,active("target_angle")),GeometryPrimitives.segment(C,B,active("target_angle")));
  if(visible.has("arc"))objects.push(GeometryPrimitives.arc(O,r,40,140,active("arc_ab")));
  if(visible.has("points"))objects.push(GeometryPrimitives.point(A,"A"),GeometryPrimitives.point(B,"B"),GeometryPrimitives.point(C,"C"),GeometryPrimitives.point(O,"O"));
  if(notes.has("central_angle"))objects.push(GeometryPrimitives.angle(O,40,140,38,`${central}°`,active("central_angle")));
  if(notes.has("target_x"))objects.push(GeometryPrimitives.angle(C,65,115,34,notes.has("answer")?`${target}°`:"x",active("target_angle")));
  const theorem=notes.has("theorem")?`<div class="geometry-reasoning"><strong>Angle at centre = 2 × angle at circumference</strong><span>${central}° = 2x</span>${notes.has("solution")?`<span>${central}° ÷ 2 = x</span><strong>x = ${target}°</strong>`:""}</div>`:"";
  return `<div class="geometry-visual ${phase}"><svg viewBox="0 0 420 290" role="img" aria-labelledby="geometry-title geometry-desc"><title id="geometry-title">Central angle theorem diagram</title><desc id="geometry-desc">Circle with centre O, central angle A O B of ${central} degrees, and circumference angle A C B on the same arc.</desc>${objects.join("")}</svg>${theorem}</div>`;
}});
AthenaVisualizationRegistry.register("function_graph","cartesian_function",{render(parameters,state,phase){
  return renderGraphSpec(parameters.spec, state, phase);
}});
