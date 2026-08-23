/* ============================================================
   PAGE CONTROLLER — Grade page (brief section 14)
   URL contract: grade.html?grade=<gradeId>
   ============================================================ */
document.addEventListener("DOMContentLoaded", async () => {
  renderNav("Learn");
  const params = new URLSearchParams(location.search);
  const gradeId = params.get("grade") || AthenaState.get().user.grade;
  let grade = CurriculumAPI.getGrade(gradeId);
  if (gradeId === "grade-12") {
    const response = await fetch(`/api/v1/curriculum/grades/${gradeId}`);
    if (response.ok) grade = await response.json();
  }

  if (!grade) {
    document.getElementById("grade-root").innerHTML = `<p>We couldn't find that grade. <a href="dashboard.html">Back to dashboard</a></p>`;
    return;
  }

  const gradeLabel = grade.label || `Grade ${grade.grade}`;
  document.title = `${gradeLabel} Mathematics — Project Athena`;
  document.getElementById("grade-title").textContent = `${gradeLabel} Mathematics`;

  if (gradeId === "grade-12" && grade.grade) {
    document.getElementById("grade-progress-pct").textContent = "0%";
    const terms = [...new Set(grade.topics.map(topic => topic.term).filter(Boolean))];
    document.getElementById("term-track").innerHTML = terms.map(term => `<div class="card term-card"><div class="label">Term ${term}</div><div class="progress-track"><div class="progress-fill" style="width:0"></div></div></div>`).join("");
    document.getElementById("topics-list").innerHTML = grade.topics.map((topic, index) => `
      <a class="topic-row" href="topic.html?grade=${grade.id}&topic=${topic.id}" style="text-decoration:none;color:inherit;">
        <div class="topic-row__index">${index === 0 ? "R" : index}</div><div class="topic-row__body"><strong>${escapeHtml(topic.title)}</strong>
        <div class="topic-row__meta">${escapeHtml(topic.paper)} · ${topic.subtopic_count} subtopics · ${escapeHtml(topic.status)}</div></div>
        <span class="badge">Explore</span></a>`).join("");
    return;
  }

  const overallProgress = grade.topics.length
    ? grade.topics.reduce((sum, t) => sum + AthenaState.topicProgress(t), 0) / grade.topics.length
    : 0;
  document.getElementById("grade-progress-pct").textContent = `${Math.round(overallProgress * 100)}%`;

  document.getElementById("term-track").innerHTML = grade.terms.map(t => `
    <div class="card term-card">
      <div class="label">${escapeHtml(t.label)}</div>
      <div class="progress-track"><div class="progress-fill" style="width:${Math.round(t.progress * 100)}%"></div></div>
    </div>`).join("");

  document.getElementById("topics-list").innerHTML = grade.topics.map((t, i) => {
    const progress = AthenaState.topicProgress(t);
    const mastered = progress === 1;
    return `
      <a class="topic-row ${mastered ? "mastered" : ""}" href="topic.html?grade=${grade.id}&topic=${t.id}" style="text-decoration:none;color:inherit;">
        <div class="topic-row__index">${i + 1}</div>
        <div class="topic-row__body">
          <strong>${escapeHtml(t.title)}</strong>
          <div class="topic-row__meta">${t.capsRef} · ${t.lessons.length} lessons</div>
        </div>
        <span class="badge ${mastered ? "badge-mastered" : ""}">${mastered ? "Mastered" : Math.round(progress * 100) + "%"}</span>
      </a>`;
  }).join("");
});

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, s => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[s]));
}
