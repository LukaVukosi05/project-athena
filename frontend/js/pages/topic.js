document.addEventListener("DOMContentLoaded", async () => {
  renderNav("Learn");
  const params = new URLSearchParams(location.search), gradeId = params.get("grade") || "grade-12", topicId = params.get("topic") || "sequences-series";
  if (!/^grade-(8|9|10|11|12)$/.test(gradeId) || !/^[-a-z0-9]+$/.test(topicId)) return showError("This curriculum route is not available.");
  const url = `/api/v1/curriculum/grades/${encodeURIComponent(gradeId)}/topics/${encodeURIComponent(topicId)}`;
  const response = await fetch(url);
  if (!response.ok) return showError(response.status === 404 ? "This topic is not registered from an available source document." : "The topic could not be loaded.");
  const topic = await response.json(), lessons = topic.subtopics.flatMap(subtopic => subtopic.lessons);
  const published = lessons.filter(lesson => lesson.readiness === "published").length, verified = lessons.filter(lesson => lesson.readiness === "verified").length;
  document.title = `${topic.title} — Project Athena`;
  document.getElementById("crumb-grade").textContent = `Grade ${gradeId.replace("grade-", "")}`;
  document.getElementById("crumb-grade").href = `grade.html?grade=${gradeId}`;
  document.getElementById("topic-title").textContent = `Topic ${topic.product_order}: ${topic.title}`;
  [document.getElementById("topic-paper"), document.getElementById("crumb-paper")].forEach(element => { element.hidden = !topic.paper; if (topic.paper) element.textContent = topic.paper; });
  document.getElementById("topic-caps-ref").textContent = topic.caps_reference || "CAPS curriculum";
  document.getElementById("topic-exam-relevance").textContent = topic.exam_relevance || "Examination relevance is not specified in the available source.";
  document.getElementById("topic-counts").textContent = `${lessons.length} expected lessons · ${published} published · ${verified} verified previews`;
  document.getElementById("learn-list").innerHTML = lessons.slice(0, 6).map(lesson => `<li>${escapeHtml(lesson.title)}</li>`).join("");
  document.getElementById("lessons-list").innerHTML = lessons.map(lesson => {
    const usable = Boolean(lesson.usable), status = lesson.status === "coming_soon" ? "coming soon" : lesson.readiness.replace("_", " ");
    const reason = lesson.readiness === "authored" ? "Approved document content; runtime conversion and verification remain." : lesson.readiness === "specified" ? "Teaching contract exists; question bank is incomplete." : lesson.readiness === "anchored" ? "Representative storyboards only." : lesson.readiness === "roadmap" ? "Named and ordered only." : "Ready to open.";
    const body = `<div class="topic-row__index">${lesson.order}</div><div class="topic-row__body"><strong>Lesson ${lesson.order}: ${escapeHtml(lesson.title)}</strong><div class="topic-row__meta">${lesson.estimated_minutes || "Duration not specified"}${lesson.estimated_minutes ? " min" : ""} · ${lesson.worked_example_count || 0} worked examples · ${lesson.practice_count || 0} practice questions</div><small>${escapeHtml(reason)}</small></div><span class="badge status-${lesson.readiness}">${escapeHtml(status)}</span>`;
    return usable ? `<a class="topic-row" href="lesson.html?grade=${encodeURIComponent(gradeId)}&topic=${encodeURIComponent(topicId)}&lesson=${encodeURIComponent(lesson.id)}">${body}</a>` : `<div class="topic-row" aria-disabled="true">${body}</div>`;
  }).join("");
});

function showError(message) {
  document.getElementById("lessons-list").innerHTML = `<section class="card" role="alert"><strong>${escapeHtml(message)}</strong></section>`;
}
