/* Native Grade 8 straight-line diagrams. The supplied question defines every label. */
(() => {
  const escape = value => escapeWhiteboardHtml(String(value ?? ''));
  const stageOf = state => {
    const marker = (state.annotations || []).find(x => /^stage:\d+$/.test(x));
    return marker ? Number(marker.slice(6)) : 0;
  };
  function render(parameters, state, phase) {
    const scene = JSON.parse(parameters.scene_json);
    const stage = stageOf(state);
    const reveal = phase === 'result' ? stage : Math.max(0, stage - 1);
    const given = escape(scene.given_label);
    const target = escape(scene.target_label);
    const active = reveal >= 2 ? 'g8-angles-active' : '';
    let drawing;
    if (scene.diagram === 'transversal') {
      const upper = scene.relationship === 'corresponding' ? [112,105] : [195,105];
      const lower = scene.relationship === 'corresponding' ? [185,192] : scene.relationship === 'alternate' ? [190,135] : [260,135];
      drawing = `<line x1="30" y1="70" x2="330" y2="70"/><line x1="30" y1="160" x2="330" y2="160"/>
        <path d="M145 70l13 -8m-13 8l13 8M230 160l13 -8m-13 8l13 8" class="g8-angles-parallel"/>
        <line x1="120" y1="25" x2="265" y2="205"/>
        <circle cx="156" cy="70" r="4"/><circle cx="229" cy="160" r="4"/>
        <text data-object-id="angle-given" x="${upper[0]}" y="${upper[1]}">${given}</text>
        <text data-object-id="angle-target" x="${lower[0]}" y="${lower[1]}">${target}</text>`;
    } else if (scene.diagram === 'perpendicular') {
      drawing = `<line x1="55" y1="150" x2="305" y2="150"/><line x1="180" y1="150" x2="180" y2="25"/>
        <line x1="180" y1="150" x2="260" y2="40"/><path d="M180 138h12v12" class="g8-angles-right"/>
        <text data-object-id="angle-given" x="195" y="98">${given}</text>
        <text data-object-id="angle-target" x="245" y="130">${target}</text>`;
    } else if (scene.diagram === 'intersection') {
      drawing = `<line x1="45" y1="185" x2="315" y2="35"/><line x1="45" y1="35" x2="315" y2="185"/>
        <circle cx="180" cy="110" r="4"/>
        <text data-object-id="angle-given" x="165" y="75">${given}</text>
        <text data-object-id="angle-target" x="${scene.relationship === 'vertical' ? 165 : 235}" y="${scene.relationship === 'vertical' ? 160 : 115}">${target}</text>`;
    } else throw new Error(`Unknown Grade 8 line diagram: ${scene.diagram}`);
    const reason = reveal >= 2 ? escape(scene.reason) : '';
    const operation = phase === 'operation' || phase === 'result' ? escape(state.working_state || '') : '';
    const result = phase === 'result' ? escape(state.after_state || '') : '';
    return `<div class="g8-angle-stage ${active}" data-object-id="model" role="group" aria-label="${escape(parameters.prompt)}">
      <svg viewBox="0 0 360 220" role="img" aria-label="${escape(scene.diagram)} angle diagram with ${given} and ${target}; not drawn to scale"><g class="g8-angle-lines">${drawing}</g></svg>
      <p data-object-id="angle-reason" class="g8-angle-reason">${reason}</p>
      <p data-object-id="operation" class="g8-angle-operation">${operation}</p>
      <p data-object-id="result" class="g8-angle-result">${result}</p>
      <p data-object-id="verification" class="g8-angle-check">${phase === 'result' && state.after_state?.startsWith('Verified:') ? result : ''}</p></div>`;
  }
  const renderer = {render};
  AthenaVisualizationRegistry.register('geometry','grade8_intersecting_angles',renderer);
  AthenaVisualizationRegistry.register('geometry','grade8_parallel_angles',renderer);
  if (typeof module !== 'undefined') module.exports = {render};
})();
