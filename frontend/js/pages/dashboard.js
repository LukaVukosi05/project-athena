/* ============================================================
   PAGE CONTROLLER — Dashboard (brief section 13)
   ============================================================ */
document.addEventListener("DOMContentLoaded", async () => {
  const authenticatedUser = await AthenaAuth.requireSession();
  if (!authenticatedUser) return;
  renderNav("Learn");
  const state = AthenaState.get();
  let grade = CurriculumAPI.getGrade(state.user.grade);
  if (state.user.grade === "grade-12") {
    const response = await fetch("/api/v1/curriculum/grades/grade-12", {
      headers: { Authorization: `Bearer ${AthenaState.accessToken()}` }
    });
    if (!response.ok) {
      document.getElementById("topics-list").innerHTML = `<div class="card"><strong>Grade 12 curriculum could not be loaded.</strong><p>Please refresh or sign in again.</p></div>`;
      return;
    }
    grade = await response.json();
  }

  document.getElementById("greeting").textContent = `${greetingWord()}, ${state.user.firstName} \uD83D\uDC4B`;
  document.getElementById("grade-label").innerHTML = `${state.user.grade.replace("grade-", "Grade ")} Mathematics <button class="btn btn-ghost" id="change-grade-btn" style="margin-left:8px;padding:6px 10px;">Change grade</button>`;
  document.getElementById("change-grade-btn").onclick = renderGradeEditor;

  if (state.user.grade === "grade-12" && grade?.topics?.[0]?.subtopic_count !== undefined) {
    renderGrade12Dashboard(grade, state);
    return;
  }

  if (!grade) {
    document.getElementById("topics-list").innerHTML = `<div class="card"><p>Curriculum content for ${escapeHtml(state.user.grade.replace("grade-", "Grade "))} is being prepared.</p><a class="btn btn-primary" href="grade.html?grade=${state.user.grade}">View grade</a></div>`;
    document.getElementById("continue-link").href = `grade.html?grade=${state.user.grade}`;
    document.getElementById("continue-link-label").textContent = "Explore your grade";
    document.getElementById("stat-plan").textContent = state.isPremium ? "Premium" : "Free";
    return;
  }

  const overallProgress = grade.topics.length
    ? grade.topics.reduce((sum, t) => sum + AthenaState.topicProgress(t), 0) / grade.topics.length
    : 0;
  document.getElementById("progress-pct").textContent = `${Math.round(overallProgress * 100)}%`;
  document.getElementById("progress-fill").style.width = `${Math.round(overallProgress * 100)}%`;

  const continueTopic = grade.topics[0];
  const nextLesson = continueTopic.lessons.find(l => !AthenaState.isLessonComplete(l.id)) || continueTopic.lessons[0];
  document.getElementById("continue-link-label").textContent = continueTopic.title;
  const continueLink = document.getElementById("continue-link");
  continueLink.href = `lesson.html?grade=${grade.id}&topic=${continueTopic.id}&lesson=${nextLesson.id}`;

  const topicsList = document.getElementById("topics-list");
  topicsList.innerHTML = grade.topics.map((t, i) => {
    const progress = AthenaState.topicProgress(t);
    const mastered = progress === 1;
    return `
      <a class="topic-row ${mastered ? "mastered" : ""}" href="topic.html?grade=${grade.id}&topic=${t.id}" style="text-decoration:none;color:inherit;">
        <div class="topic-row__index">${i + 1}</div>
        <div class="topic-row__body">
          <strong>${escapeHtml(t.title)}</strong>
          <div class="topic-row__meta">${t.lessons.length} lessons · ${Math.round(progress * 100)}% complete</div>
        </div>
        <span class="badge ${mastered ? "badge-mastered" : ""}">${mastered ? "Mastered" : t.difficulty}</span>
      </a>`;
  }).join("");

  document.getElementById("stat-progress").textContent = `${Math.round(overallProgress * 100)}%`;
  document.getElementById("stat-lessons").textContent = AthenaState.get().completedLessons.length;
  document.getElementById("stat-plan").textContent = state.isPremium ? "Premium" : "Free";
});

function renderGrade12Dashboard(grade, state) {
  document.getElementById("progress-pct").textContent = "0%";
  document.getElementById("progress-fill").style.width = "0%";
  document.getElementById("continue-link-label").textContent = "Browse the complete Grade 12 curriculum";
  document.getElementById("continue-link").href = "grade.html?grade=grade-12";

  const paper2Ids = new Set(["statistics", "analytical-geometry", "trigonometry", "euclidean-geometry"]);
  const renderTopic = (topic, index) => `
    <a class="topic-row" href="topic.html?grade=grade-12&topic=${topic.id}" style="text-decoration:none;color:inherit;">
      <div class="topic-row__index">${topic.product_order === 0 ? "R" : topic.product_order}</div>
      <div class="topic-row__body"><strong>${escapeHtml(topic.title)}</strong>
      <div class="topic-row__meta">${escapeHtml(topic.paper)} · ${topic.subtopic_count} subtopics${paper2Ids.has(topic.id) ? " · 4 unlocked lessons" : ""}</div></div>
      <span class="badge">${paper2Ids.has(topic.id) ? "Paper 2" : "Explore"}</span>
    </a>`;

  const paper2 = grade.topics.filter(topic => paper2Ids.has(topic.id));
  const other = grade.topics.filter(topic => !paper2Ids.has(topic.id));
  document.getElementById("topics-list").innerHTML = `
    <div class="card" style="margin-bottom:var(--space-5);border:2px solid var(--color-primary);">
      <h3>Paper 2 lessons</h3><p>Foundation practice, standard practice, comprehensive mastery quizzes and exact DBE exam questions are unlocked.</p>
      ${paper2.map(renderTopic).join("")}
    </div>
    <h3>All Grade 12 modules</h3>${other.map(renderTopic).join("")}`;
  document.getElementById("stat-progress").textContent = "0%";
  document.getElementById("stat-lessons").textContent = state.completedLessons.length;
  document.getElementById("stat-plan").textContent = state.isPremium ? "Premium" : "Free";
}

function renderGradeEditor() {
  const label = document.getElementById("grade-label");
  const selected = AthenaState.get().user.grade;
  label.innerHTML = `<label for="profile-grade">Your grade</label> <select id="profile-grade">${[8,9,10,11,12].map(number => `<option value="grade-${number}" ${selected === `grade-${number}` ? "selected" : ""}>Grade ${number}</option>`).join("")}</select> <button class="btn btn-primary" id="save-grade-btn">Save</button>`;
  document.getElementById("save-grade-btn").onclick = async event => {
    event.currentTarget.disabled = true;
    try {
      await AthenaAuth.updateProfile({ grade: document.getElementById("profile-grade").value });
      location.reload();
    } catch (error) {
      alert(error.message);
      event.currentTarget.disabled = false;
    }
  };
}

function greetingWord() {
  const h = new Date().getHours();
  if (h < 12) return "Good morning";
  if (h < 18) return "Good afternoon";
  return "Good evening";
}
function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, s => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[s]));
}
