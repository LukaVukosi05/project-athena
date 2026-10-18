document.addEventListener("DOMContentLoaded", async () => {
  const authenticatedUser = await AthenaAuth.requireSession();
  if (!authenticatedUser) return;
  renderNav("Learn");
  const state = AthenaState.get(), selected = state.user?.grade || "grade-12", picker = document.getElementById("dashboard-grade");
  picker.value = selected;
  picker.onchange = () => { location.href = `grade.html?grade=${encodeURIComponent(picker.value)}`; };
  const greeting = typeof greetingWord === "function" ? greetingWord() : "Welcome";
  document.getElementById("greeting").textContent = `${greeting}, ${state.user.firstName}`;
  await loadGrade(selected, state);
});

async function loadGrade(gradeId, state) {
  const url = `/api/v1/curriculum/grades/${encodeURIComponent(gradeId)}`, response = await fetch(url, { headers: AthenaState.accessToken() ? { Authorization: `Bearer ${AthenaState.accessToken()}` } : {} });
  if (!response.ok) { document.getElementById("topics-list").innerHTML = `<div class="card" role="alert"><strong>Curriculum could not be loaded.</strong><p>Request: ${escapeDashboardHtml(url)} · Status: ${response.status}</p></div>`; return; }
  const grade = await response.json(), usable = grade.topics.reduce((sum, topic) => sum + (topic.interactive_lesson_count || 0), 0), complete = state.completedLessons.filter(id => id.startsWith(`g${grade.grade}-`)).length, progress = usable ? Math.min(100, Math.round(complete / usable * 100)) : 0;
  document.getElementById("grade-label").textContent = `Grade ${grade.grade} Mathematics`;
  document.getElementById("progress-pct").textContent = `${progress}%`;
  document.getElementById("progress-fill").style.width = `${progress}%`;
  document.getElementById("catalogue-summary").textContent = `${grade.topics.length} topics · ${usable} usable lessons`;
  if (!grade.topics.length) { document.getElementById("topics-list").innerHTML = '<div class="card empty-state"><h3>Choose your grade to begin</h3><p>The approved curriculum source for this grade is not registered yet.</p></div>'; return; }
  const first = grade.topics.find(topic => (topic.published_interactive_lesson_count || 0) > 0) || grade.topics[0];
  document.getElementById("continue-link-label").textContent = first.title;
  document.getElementById("continue-detail").textContent = `${first.paper ? `${first.paper} · ` : ""}${first.published_interactive_lesson_count || 0} published · ${first.verified_lesson_count || 0} verified`;
  document.getElementById("continue-link").href = `topic.html?grade=${grade.id}&topic=${encodeURIComponent(first.id)}`;
  document.getElementById("continue-link").textContent = complete ? "Continue" : "Start";
  const card = topic => `<a class="topic-row" href="topic.html?grade=${grade.id}&topic=${encodeURIComponent(topic.id)}"><div class="topic-row__index">${topic.product_order}</div><div class="topic-row__body"><strong>Topic ${topic.product_order}: ${escapeDashboardHtml(topic.title)}</strong><div class="topic-row__meta">${topic.paper ? `<span class="badge">${escapeDashboardHtml(topic.paper)}</span> ` : ""}${topic.lesson_count || 0} expected · ${topic.published_interactive_lesson_count || 0} published · ${topic.verified_lesson_count || 0} verified</div></div><span class="badge ${topic.availability === "available" ? "status-published" : "status-roadmap"}">${topic.availability === "available" ? "Available" : "Roadmap"}</span></a>`;
  const groups = grade.id === "grade-12" ? ["Paper 1", "Paper 2"] : [null];
  document.getElementById("topics-list").innerHTML = groups.map(paper => { const topics = grade.id === "grade-12" ? grade.topics.filter(topic => topic.paper === paper) : grade.topics; return topics.length ? `<section class="paper-section">${paper ? `<h3>${escapeDashboardHtml(paper)}</h3>` : ""}${topics.map(card).join("")}</section>` : ""; }).join("");
}

function escapeDashboardHtml(value) { return String(value).replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char])); }
