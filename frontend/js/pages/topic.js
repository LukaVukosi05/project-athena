/* ============================================================
   PAGE CONTROLLER — Topic page (brief section 15)
   URL contract: topic.html?grade=<gradeId>&topic=<topicId>
   ============================================================ */
document.addEventListener("DOMContentLoaded", async () => {
  renderNav("Learn");
  const params = new URLSearchParams(location.search);
  const gradeId = params.get("grade");
  const topicId = params.get("topic");
  const legacyTopic = CurriculumAPI.getTopic(gradeId, topicId);
  let topic = legacyTopic;
  if (gradeId === "grade-12") {
    const response = await fetch(`/api/v1/curriculum/grades/${gradeId}/topics/${encodeURIComponent(topicId)}`);
    if (response.ok) topic = await response.json();
  }

  if (!topic) {
    document.getElementById("topic-root").innerHTML = `<p>We couldn't find that topic. <a href="dashboard.html">Back to dashboard</a></p>`;
    return;
  }

  document.title = `${topic.title} — Project Athena`;
  document.getElementById("crumb-grade").textContent = gradeId === "grade-12" ? "Grade 12" : CurriculumAPI.getGrade(gradeId).label;
  document.getElementById("crumb-grade").href = `grade.html?grade=${gradeId}`;
  document.getElementById("topic-title").textContent = topic.title;
  document.getElementById("topic-caps-ref").textContent = topic.caps_reference || topic.capsRef || "Teacher review required";

  if (topic.subtopics) {
    document.getElementById("learn-list").innerHTML = topic.subtopics.map(item => `<li>${escapeHtml(item.title)}</li>`).join("");
    document.querySelector("#lessons-list").previousElementSibling.textContent = "Available lessons";
    const availableSubtopics = topic.subtopics.filter(subtopic => subtopic.lessons.length);
    document.getElementById("lessons-list").innerHTML = availableSubtopics.map(subtopic => `
      <section class="card" style="margin-bottom:var(--space-3);"><h4>${subtopic.order}. ${escapeHtml(subtopic.title)}</h4>
      ${subtopic.lessons.map(lesson => `<a class="topic-row" href="lesson.html?grade=${gradeId}&topic=${topicId}&lesson=${lesson.id}" style="text-decoration:none;color:inherit;"><div class="topic-row__body"><strong>${escapeHtml(lesson.title)}</strong><div class="topic-row__meta">${escapeHtml(lesson.difficulty)} · Unlocked · ${lesson.estimated_minutes || "—"} min</div></div><span class="badge">Start</span></a>`).join("")}
      </section>`).join("") + (ATHENA_UNLOCK_ALL_LESSONS && topic.subtopics.every(item => item.lessons.length === 0) && legacyTopic?.lessons?.length ? `
      <section class="card" style="margin-bottom:var(--space-3);border:2px solid var(--color-primary);"><h4>Differential Calculus lessons — unlocked testing</h4>
      ${legacyTopic.lessons.map(lesson => `<a class="topic-row" href="lesson.html?grade=${gradeId}&topic=${topicId}&lesson=${lesson.id}" style="text-decoration:none;color:inherit;"><div class="topic-row__body"><strong>${escapeHtml(lesson.title)}</strong><div class="topic-row__meta">Temporarily unlocked for curriculum testing</div></div><span class="badge">Test</span></a>`).join("")}</section>` : "");
    return;
  }

  document.getElementById("learn-list").innerHTML = topic.whatYoullLearn.map(x => `<li>${escapeHtml(x)}</li>`).join("");

  document.getElementById("lessons-list").innerHTML = topic.lessons.map((lesson, i) => {
    const unlocked = AthenaState.isLessonUnlocked(topic, lesson.id);
    const complete = AthenaState.isLessonComplete(lesson.id);
    const rowClasses = `topic-row ${!unlocked ? "locked" : ""} ${complete ? "mastered" : ""}`;
    const inner = `
        <div class="topic-row__index">${complete ? "✓" : i + 1}</div>
        <div class="topic-row__body">
          <strong>Lesson ${i + 1}: ${escapeHtml(lesson.title)}</strong>
          <div class="topic-row__meta">${escapeHtml(lesson.summary)}${lesson.free ? "" : " · Premium"}</div>
        </div>
        <span class="badge ${!unlocked ? "badge-locked" : complete ? "badge-mastered" : ""}">${!unlocked ? "Locked" : complete ? "Complete" : "Start"}</span>`;

    return unlocked
      ? `<a class="${rowClasses}" href="lesson.html?grade=${gradeId}&topic=${topicId}&lesson=${lesson.id}" style="text-decoration:none;color:inherit;">${inner}</a>`
      : `<div class="${rowClasses}" aria-disabled="true">${inner}</div>`;
  }).join("");
});

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, s => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[s]));
}
