document.addEventListener("DOMContentLoaded", async () => {
  document.querySelectorAll(".lesson-support details").forEach(section => { section.open = false; });
  renderNav("Learn");
  const lessonId = new URLSearchParams(location.search).get("lesson");
  if (!/^g(?:8|9|10|11|12)-[a-z0-9-]+-\d{2}$/.test(lessonId || "")) {
    document.getElementById("lesson-root").innerHTML = '<div class="card"><strong>This lesson is not part of the active approved curriculum.</strong></div>';
    return;
  }
  await renderStructuredLesson(lessonId);
});

async function renderStructuredLesson(lessonId) {
  const root = document.getElementById("lesson-root");
  try {
    const token = AthenaState.accessToken();
    const response = await fetch(`/api/v1/lessons/${encodeURIComponent(lessonId)}`, { headers: token ? { Authorization: `Bearer ${token}` } : {} });
    if (!response.ok) throw new Error(response.status === 401 ? "Please sign in to access this lesson." : response.status === 403 ? "An active subscription is required." : response.status === 409 ? "This lesson is source-authored but not verified for use yet." : "Lesson could not be loaded.");
    const lesson = await response.json();
    document.title = `${lesson.title} — Project Athena`;
    document.getElementById("crumb-topic").textContent = lesson.topic_title;
    document.getElementById("crumb-topic").href = `topic.html?grade=${encodeURIComponent(lesson.grade_id)}&topic=${encodeURIComponent(lesson.topic_id)}`;
    [document.getElementById("crumb-paper"), document.getElementById("lesson-paper")].forEach(element => {
      element.hidden = !lesson.paper;
      if (lesson.paper) element.textContent = lesson.paper;
    });
    document.getElementById("lesson-progress").textContent = `Lesson ${lesson.order} of ${lesson.lesson_count}`;
    document.getElementById("lesson-title").textContent = lesson.title;
    document.getElementById("lesson-why").textContent = lesson.why_it_matters;
    document.getElementById("lesson-prerequisites").textContent = lesson.prerequisites.length ? lesson.prerequisites.join(", ") : "No prerequisite lesson is required.";
    document.getElementById("lesson-duration").textContent = lesson.estimated_minutes ? `${lesson.estimated_minutes} minutes` : "Duration not specified in the source.";
    new LessonBlockRenderer(root, lesson).render();
    document.querySelector(".lesson-introduction")?.setAttribute("id", "lesson-objective");
  } catch (error) {
    root.innerHTML = `<div class="card"><strong>We couldn't load this lesson.</strong><p>${escapeHtml(error.message)}</p></div>`;
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
}
