/* Grade 8 Functions topic check. The API owns all answers and scoring. */
const AthenaTopicDiagnostic = (() => {
  const url = '/api/v1/practice/topics/grade-8/functions-relationships/diagnostic';
  const key = 'athena:grade-8:functions-relationships:check-v1';
  const safe = value => escapeHtml(String(value));
  const lessonLink = id => `lesson.html?grade=grade-8&topic=functions-relationships&lesson=${encodeURIComponent(id)}`;
  let button, panel, summary;
  async function start() {
    button.disabled = true;
    panel.hidden = false;
    panel.innerHTML = '<p role="status">Loading the topic check…</p>';
    try {
      const response = await fetch(url);
      if (!response.ok) throw Error('The topic check is unavailable. Please try again.');
      const data = await response.json();
      panel.innerHTML = `<h3>Check your understanding</h3><p>Try all nine questions independently. You will see the worked review after submitting.</p><form id="topic-diagnostic-form">${data.questions.map((q, i) => `<label class="topic-diagnostic__question"><span>${i + 1}. ${safe(q.prompt)}</span><input name="${safe(q.id)}" type="text" autocomplete="off" maxlength="100" required aria-label="Answer to question ${i + 1}"></label>`).join('')}<button class="btn btn-primary" type="submit">Submit all nine answers</button></form><p class="topic-diagnostic__error" role="alert" hidden></p>`;
      panel.querySelector('form').addEventListener('submit', event => submit(event, data.questions));
      panel.scrollIntoView({behavior: 'smooth', block: 'start'});
    } catch (error) {
      panel.innerHTML = `<p role="alert">${safe(error.message)}</p>`;
      button.disabled = false;
    }
  }
  async function submit(event, questions) {
    event.preventDefault();
    const form = event.currentTarget, send = form.querySelector('button[type=submit]');
    const answers = Object.fromEntries(questions.map(q => [q.id, form.elements.namedItem(q.id).value.trim()]));
    send.disabled = true;
    const errorBox = panel.querySelector('.topic-diagnostic__error');
    errorBox.hidden = true;
    try {
      const response = await fetch(url, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({answers})});
      if (!response.ok) throw Error('Your answers could not be checked. Try submitting again.');
      const result = await response.json();
      // Only the summary is retained on this device; answers and worked reviews are not.
      try { localStorage.setItem(key, JSON.stringify({score: result.score, total: result.total, areas: result.areas})); } catch (_) {}
      showSummary(result);
      panel.innerHTML = `<h3>Worked review</h3><p>${result.score} of ${result.total} correct. ${safe(result.note)}</p>${result.review.map((row, i) => `<article class="topic-diagnostic__review"><strong>${i + 1}. ${row.correct ? 'Correct' : 'Review this answer'}</strong><p>Answer: ${safe(row.answer)}. ${safe(row.explanation)}</p></article>`).join('')}<button class="btn btn-secondary" id="topic-diagnostic-retry" type="button">Try a fresh check</button>`;
      // A repeat is useful for revision, but these nine items are fixed. Do not call it a parallel reassessment.
      panel.querySelector('#topic-diagnostic-retry').textContent = 'Repeat this check';
      panel.querySelector('#topic-diagnostic-retry').onclick = start;
      button.disabled = false;
    } catch (error) {
      errorBox.textContent = error.message;
      errorBox.hidden = false;
      send.disabled = false;
    }
  }
  function showSummary(result) {
    const needs = result.areas.filter(area => area.needs_review);
    summary.innerHTML = needs.length ? `Topic check: ${result.score}/${result.total}. Start with ${needs.map(area => `<a href="${lessonLink(area.lesson_id)}">${safe(area.title)}</a> (${area.correct}/${area.total})`).join('; ')}.` : `Topic check: ${result.score}/${result.total}. No weak area was detected by this short check. Complete each lesson’s mastery assessment.`;
  }
  function init() {
    button = document.getElementById('topic-diagnostic-button');
    panel = document.getElementById('topic-diagnostic');
    summary = document.getElementById('topic-weaknesses');
    button.disabled = false;
    button.textContent = 'Start topic check';
    button.onclick = start;
    try {
      const stored = JSON.parse(localStorage.getItem(key));
      if (stored && Array.isArray(stored.areas) && Number.isInteger(stored.score)) showSummary(stored);
    } catch (_) {}
  }
  return {init};
})();
