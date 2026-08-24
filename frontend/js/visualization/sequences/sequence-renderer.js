function sequenceTimelineMarkup(parameters, state, phase) {
  const terms = parameters.terms || [];
  const positions = parameters.positions || terms.map((_, index) => index + 1);
  const differences = parameters.differences || terms.slice(1).map((value, index) => value - terms[index]);
  const ratios = parameters.ratios || [];
  const second = parameters.second_differences || differences.slice(1).map((value, index) => value - differences[index]);
  const width = 620;
  const start = 80;
  const gap = terms.length > 1 ? Math.min(135, 470 / (terms.length - 1)) : 100;
  const row = (values, y, prefix, label, offset = 0) => `<g class="sequence-row sequence-row--${prefix}"><text x="15" y="${y}" class="sequence-row__label">${escapeWhiteboardHtml(label)}</text>${values.map((value,index) => {
    const x=start+(index+offset)*gap;
    return `<g data-object-id="${prefix}-${index+1}" data-x="${x}" data-y="${y}" class="semantic-object is-hidden"><text x="${x}" y="${y}" text-anchor="middle">${escapeWhiteboardHtml(value)}</text></g>`;
  }).join("")}</g>`;
  return `<div class="sequence-visual ${phase}">
    <svg viewBox="0 0 ${width} 330" role="img" aria-labelledby="sequence-title sequence-description">
      <title id="sequence-title">${escapeWhiteboardHtml(parameters.title || "Sequence analysis")}</title>
      <desc id="sequence-description">Positions and terms are aligned. Difference rows are revealed as the timeline explains the pattern.</desc>
      <g class="whiteboard-background"><line x1="10" y1="105" x2="610" y2="105"/></g>
      <g class="mathematical-object-layer">
        ${row(positions,65,"position","n")}${row(terms,115,"term","Tₙ")}
        ${row(ratios.length ? ratios.map(value=>`×${value}`) : differences.map(value => `${value >= 0 ? "+" : ""}${value}`),205,"difference",ratios.length?"Ratio":"ΔT",.5)}
        ${second.length ? row(second.map(value => `${value >= 0 ? "+" : ""}${value}`),285,"second-difference","Δ²T",1) : ""}
        <g data-object-id="goal" class="semantic-object is-hidden"><text x="310" y="25" text-anchor="middle">${escapeWhiteboardHtml(parameters.mode === "nth_term" ? "Explain the n−1 jumps" : "Classify the sequence")}</text></g>
        <g data-object-id="classification" class="semantic-object is-hidden"><text x="500" y="315" text-anchor="end">Pattern identified</text></g>
        <g data-object-id="verification" class="semantic-object is-hidden"><text x="595" y="25" text-anchor="end">✓ Verified</text></g>
        <g data-object-id="predicted-change" class="semantic-object is-hidden"><text x="520" y="205" text-anchor="middle">${escapeWhiteboardHtml(parameters.next_change || "?")}</text></g>
        <g data-object-id="next-term" class="semantic-object is-hidden"><text x="590" y="115" text-anchor="middle">${escapeWhiteboardHtml(parameters.next_term || "?")}</text></g>
      </g>
      <g class="instruction-layer" data-role="instruction-layer"></g>
      <g class="interaction-layer" data-role="interaction-layer"></g>
    </svg>
  </div>`;
}

AthenaVisualizationRegistry.register("sequences", "sequence_timeline", {
  render(parameters, state, phase) { return sequenceTimelineMarkup(parameters, state, phase); },
  destroy() {}
});
