class VisualizationRegistry {
  constructor() { this.renderers = new Map(); }
  key(type, template) { return `${type}:${template}`; }
  register(type, template, renderer) { const key=this.key(type,template); if(this.renderers.has(key))throw new Error(`Duplicate visualization template: ${key}`); this.renderers.set(key,renderer); }
  resolve(type, template) { const renderer=this.renderers.get(this.key(type,template)); if(!renderer)throw new Error(`Unsupported visualization: ${type}:${template}`); return renderer; }
  manifest() { return [...this.renderers.keys()].sort(); }
}
const AthenaVisualizationRegistry=new VisualizationRegistry();

const AthenaVisualizationDiagnostics={
  emitted:new Set(),
  emit(code,detail={}){const key=`${code}:${detail.block_id||"unknown"}:${detail.template||""}`;if(this.emitted.has(key))return;this.emitted.add(key);const payload={code,...detail};if(typeof document!=="undefined"&&typeof CustomEvent!=="undefined")document.dispatchEvent(new CustomEvent("athena:visualization-error",{detail:payload}));if(typeof console!=="undefined")console.error("Athena visualization diagnostic",payload);}
};

class VisualizationResolver {
  resolve(block, context = {}) {
    if(block.representation!=="visual"&&!block.visualization&&!block.graph_spec)return null;
    let instruction=block.visualization;
    if(!instruction&&block.graph_spec)instruction={type:"function_graph",template:"cartesian_function",parameters:{graph_spec_id:block.id}};
    if(!instruction){AthenaVisualizationDiagnostics.emit("VISUALIZATION_REQUIRED_BUT_MISSING",{...context,block_id:block.id});return this.fallback(block,"Required diagram metadata is missing.");}
    try {
      const renderer=AthenaVisualizationRegistry.resolve(instruction.type,instruction.template);
      const parameters={...instruction.parameters};if(block.graph_spec)parameters.graph_spec=block.graph_spec;
      return {render:(step,phase)=>renderer.render(parameters,step.visualization_state||{},phase),destroy:()=>renderer.destroy?.(),instruction};
    } catch(error) {AthenaVisualizationDiagnostics.emit("VISUALIZATION_TEMPLATE_UNKNOWN",{...context,block_id:block.id,template:`${instruction.type}:${instruction.template}`});return this.fallback(block,error.message);}
  }
  fallback(block,message){return {render:step=>`<div class="visualization-fallback" role="note"><strong>Diagram unavailable.</strong><p>${escapeWhiteboardHtml(step.screen_reader_description||message)}</p></div>`,destroy() {},instruction:null};}
}
const AthenaVisualizationResolver=new VisualizationResolver();
