/* Safe display-only notation for authored powers. Answers remain plain data for marking. */
const AthenaMathNotation = (() => {
  const escape = value => String(value).replace(/[&<>"']/g, char => (
    {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));
  const power = /([A-Za-z]|\d+(?:\.\d+)?|\))\^\(([-+]?\d+)\/([1-9]\d*)\)|([A-Za-z]|\d+(?:\.\d+)?|\))\^\(?([+-]?\d+)\)?/g;
  function html(value) {
    const source = String(value ?? "");
    let output = "", cursor = 0;
    for (const match of source.matchAll(power)) {
      output += escape(source.slice(cursor, match.index));
      const base = match[1] || match[4];
      if (match[1]) {
        const numerator = match[2], denominator = match[3];
        output += `<span class="athena-power" role="math" aria-label="${escape(base)} to the power of ${escape(numerator)} over ${escape(denominator)}">${escape(base)}<sup><span class="athena-power-fraction" aria-hidden="true"><span>${escape(numerator)}</span><span>${escape(denominator)}</span></span></sup></span>`;
      } else {
        const exponent = match[5];
        output += `<span class="athena-power" role="math" aria-label="${escape(base)} to the power of ${escape(exponent)}">${escape(base)}<sup aria-hidden="true">${escape(exponent)}</sup></span>`;
      }
      cursor = match.index + match[0].length;
    }
    return output + escape(source.slice(cursor));
  }
  return { html };
})();
