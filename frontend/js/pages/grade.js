document.addEventListener("DOMContentLoaded", async () => {
  renderNav("Learn");
  const requested = new URLSearchParams(location.search).get("grade") || "grade-12";
  if (!/^grade-(8|9|10|11|12)$/.test(requested)) return showError("This grade route is not available.");
  const url = `/api/v1/curriculum/grades/${encodeURIComponent(requested)}`;
  const response = await fetch(url);
  if (!response.ok) return showError(`Curriculum could not be loaded. Request: ${url} · Status: ${response.status}`);
  const grade = await response.json(), state = AthenaState.get();
  const usable = grade.topics.reduce((total, topic) => total + (topic.interactive_lesson_count || 0), 0);
  const complete = state.completedLessons.filter(id => id.startsWith(`g${grade.grade}-`)).length;
  const progress = usable ? Math.min(100, Math.round(complete / usable * 100)) : 0;
  document.title = `Grade ${grade.grade} Mathematics — Project Athena`;
  document.getElementById("grade-title").textContent = `Grade ${grade.grade} Mathematics`;
  document.getElementById("grade-progress-pct").textContent = `${progress}%`;
  document.getElementById("term-track").innerHTML = `<div class="card term-card"><div class="label">Published lessons</div><strong>${grade.topics.reduce((sum, topic) => sum + (topic.published_interactive_lesson_count || 0), 0)}</strong></div><div class="card term-card"><div class="label">Verified previews</div><strong>${grade.topics.reduce((sum, topic) => sum + (topic.verified_lesson_count || 0), 0)}</strong></div><div class="card term-card"><div class="label">Topics registered</div><strong>${grade.topics.length}</strong></div><div class="card term-card"><div class="label">Evidence status</div><strong>${grade.topics.length ? "Catalogue loaded" : "Source blocked"}</strong></div>`;
  if (!grade.topics.length) {
    document.getElementById("paper-switcher").hidden = true;
    document.getElementById("topics-list").innerHTML = '<section class="card empty-state"><span class="badge status-roadmap">Source blocked</span><h3>Authoritative curriculum source required</h3><p>Athena will not manufacture this grade’s topic structure or lesson counts.</p></section>';
    return;
  }
  const card = topic => `<article class="topic-row"><div class="topic-row__index">${topic.product_order}</div><div class="topic-row__body"><strong>Topic ${topic.product_order}: ${escapeHtml(topic.title)}</strong><div class="topic-row__meta">${topic.paper ? `<span class="badge">${escapeHtml(topic.paper)}</span> ` : ""}${topic.lesson_count} expected · ${topic.published_interactive_lesson_count} published · ${topic.verified_lesson_count} verified</div><div class="progress-track" aria-label="Topic progress"><div class="progress-fill" style="width:0%"></div></div></div><a class="btn ${topic.availability === "available" ? "btn-primary" : "btn-ghost"}" href="topic.html?grade=${grade.id}&topic=${encodeURIComponent(topic.id)}">${topic.availability === "available" ? "View topic" : "View roadmap"}</a></article>`;
  const groups = grade.id === "grade-12" ? ["Paper 1", "Paper 2"] : [null];
  document.getElementById("paper-switcher").hidden = grade.id !== "grade-12";
  document.getElementById("topics-list").innerHTML = groups.map(paper => {
    const topics = grade.id === "grade-12" ? grade.topics.filter(topic => topic.paper === paper) : grade.topics;
    return topics.length ? `<section class="paper-section"${paper ? ` id="${paper.toLowerCase().replaceAll(" ", "-")}"` : ""}>${paper ? `<p class="eyebrow">${escapeHtml(paper)}</p><h3>${escapeHtml(paper)} topics</h3>` : ""}${topics.map(card).join("")}</section>` : "";
  }).join("");
});

function showError(message) {
  document.getElementById("topics-list").innerHTML = `<section class="card" role="alert"><strong>${escapeHtml(message)}</strong></section>`;
}
