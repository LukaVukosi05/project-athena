/* Two-intersection geometry: every sector and stage comes from the active question. */
(() => {
  const esc = value => escapeWhiteboardHtml(String(value ?? ''));
  const stage = state => Number((state.annotations || []).find(x => /^stage:\d+$/.test(x))?.slice(6) || 0);
  const POSITIONS = {
    corresponding_linear: {given:[183,105],middle:[252,194],target:[251,144]},
    alternate_linear: {given:[183,105],middle:[177,143],target:[251,144]},
    cointerior_vertical: {given:[183,105],middle:[251,144],target:[181,195]}
  };
  function render(parameters, state = {}, phase = 'initial') {
    const scene = JSON.parse(parameters.scene_json), position = POSITIONS[scene.family];
    if (!position || ![3,4,5].includes(scene.lesson)) throw Error('Unsupported angle-chain scene');
    const intermediate = scene.family === 'cointerior_vertical' ? 180 - scene.given : scene.given;
    const targetAngle = scene.family === 'cointerior_vertical' ? intermediate : 180 - intermediate;
    const visible = phase === 'result' ? stage(state) : Math.max(0,stage(state)-1);
    const middleStage = scene.lesson === 5 ? 4 : 3;
    const targetStage = scene.lesson === 5 ? 5 : 4;
    const pair = (id, point, value, extra = '') => `<text data-object-id="${id}" x="${point[0]}" y="${point[1]}" class="${extra}">${esc(value)}</text>`;
    const middle = visible >= middleStage ? `${intermediate}°` : '?';
    const solved = visible >= targetStage ? `${targetAngle}°` : '';
    const claim = scene.lesson === 5 ? `<p data-object-id="learner-claim" class="g8-angle-chain__claim ${visible >= 3 ? 'is-invalid' : ''}">Learner's claim: ${esc(scene.wrong_claim)}${visible >= 3 ? ' — first unsupported claim' : ''}</p>` : '<span data-object-id="learner-claim" hidden></span>';
    const reason = visible >= 2 ? scene.relation : '';
    return `<div class="g8-angle-chain" data-object-id="model" role="group" aria-label="${esc(parameters.prompt)}">
      <span data-object-id="problem" hidden>${esc(parameters.prompt)}</span>
      <svg viewBox="0 0 360 235" role="img" aria-label="Two parallel marked lines and one transversal; angles are positioned by the ${esc(scene.relation)} and second relationship, not drawn to scale">
        <g class="g8-angle-chain__lines"><line x1="25" y1="72" x2="335" y2="72"/><line x1="25" y1="162" x2="335" y2="162"/><line x1="100" y1="5" x2="270" y2="225"/>
          <path d="M78 72 l12 -6 m-12 6 l12 6 M290 162 l12 -6 m-12 6 l12 6" class="g8-angle-chain__parallel"/></g>
        ${pair('angle-given',position.given,`${scene.given}°`)}
        ${pair('angle-intermediate',position.middle,middle,visible >= middleStage ? 'is-revealed' : '')}
        ${pair('angle-target',position.target,scene.target_label,'is-target')}
        ${solved ? `<text class="g8-angle-chain__value" x="235" y="218">target angle = ${esc(solved)}</text>` : ''}
      </svg>
      <p data-object-id="angle-reason" class="g8-angle-chain__reason">${esc(reason)}</p>${claim}
      <p data-object-id="operation" class="g8-angle-chain__operation">${phase === 'operation' || phase === 'result' ? esc(state.working_state || '') : ''}</p>
      <p data-object-id="result" class="g8-angle-chain__result">${phase === 'result' ? esc(state.after_state || '') : ''}</p>
      <p data-object-id="verification" class="g8-angle-chain__check">${phase === 'result' && state.after_state?.startsWith('Verified:') ? esc(state.after_state) : ''}</p>
    </div>`;
  }
  const renderer = {render};
  for (const template of ['grade8_angle_chain','grade8_angle_equation','grade8_angle_error'])
    AthenaVisualizationRegistry.register('geometry',template,renderer);
  if (typeof module !== 'undefined') module.exports = {render};
})();
