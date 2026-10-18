(function () {
  const statisticsFamilies = ["balance_and_rank","spread_number_line","five_number_ribbon","ogive_builder","box_plot_builder","outlier_fence_lab","deviation_calculator_lab","scatter_builder","least_squares_fit","regression_calculator","interpolation_trace","extrapolation_risk_zone","influence_lab","integrated_statistics_dashboard","question_first_assessment"];

  function semanticCards(parameters, phase, kind) {
    const ids=parameters.objects;
    const answerVisible=phase==="result";
    const decoration=kind==="statistics"
      ? '<svg viewBox="0 0 560 150" role="img" aria-label="Statistical representation"><line x1="35" y1="125" x2="535" y2="125" class="axis"/><rect x="75" y="80" width="60" height="45"/><rect x="170" y="55" width="60" height="70"/><rect x="265" y="25" width="60" height="100"/><circle cx="405" cy="65" r="7"/><circle cx="460" cy="40" r="7"/><line x1="405" y1="65" x2="460" y2="40"/></svg>'
      : '<svg viewBox="0 0 560 180" role="img" aria-label="Coordinate geometry construction"><line x1="30" y1="90" x2="530" y2="90" class="axis"/><line x1="280" y1="15" x2="280" y2="165" class="axis"/><line x1="105" y1="140" x2="455" y2="35" class="construction"/><circle cx="105" cy="140" r="7"/><circle cx="455" cy="35" r="7"/><path d="M280 88 h18 v-18" class="right-angle"/></svg>';
    return `<figure class="curriculum-board curriculum-board--${kind} ${phase}" data-family="${escapeWhiteboardHtml(parameters.family)}">${decoration}<figcaption>${escapeWhiteboardHtml(parameters.family.replaceAll("_"," "))}</figcaption><div class="curriculum-board__cards"><p data-object-id="${ids[0]}">${escapeWhiteboardHtml(parameters.prompt)}</p><p data-object-id="${ids[1]}" class="curriculum-board__method">${escapeWhiteboardHtml(parameters.method||"Choose and apply a valid method")}</p><p data-object-id="${ids[2]}" class="curriculum-board__answer" ${answerVisible?"":"hidden"}>${escapeWhiteboardHtml(parameters.answer)}</p></div></figure>`;
  }

  function sequenceBoard(parameters, phase) {
    const ids=parameters.objects, answerVisible=phase==="result";
    return `<figure class="curriculum-board curriculum-board--sequence ${phase}"><div class="sequence-workbench"><p data-object-id="${ids[0]}">${escapeWhiteboardHtml(parameters.prompt)}</p><span data-object-id="${ids[1]}">=</span><p data-object-id="${ids[2]}">${escapeWhiteboardHtml(parameters.method||"Select the sequence or series structure")}</p><p data-object-id="${ids[3]}" class="curriculum-board__method">one legal operation</p><p data-object-id="${ids[4]}" class="curriculum-board__answer" ${answerVisible?"":"hidden"}>${escapeWhiteboardHtml(parameters.answer)}</p><p data-object-id="${ids[5]}" ${answerVisible?"":"hidden"}>Verified against the original information.</p></div><figcaption>Sequence and series reasoning board</figcaption></figure>`;
  }
  AthenaVisualizationRegistry.register("sequences","sequence_reasoning",{render:sequenceBoard});
  statisticsFamilies.forEach(family=>AthenaVisualizationRegistry.register("statistics",family,{render:(p,s,phase)=>semanticCards(p,phase,"statistics")}));
})();
