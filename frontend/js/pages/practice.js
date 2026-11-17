/* Navigation only: authored questions and scoring remain in the existing engine. */
const PracticeHub = {
  catalogue: null, requestNumber: 0,
  async init() {
    if (!await AthenaAuth.requireSession()) return;
    renderNav("Practice");
    const params = new URLSearchParams(location.search);
    const grade = params.get("grade") || AthenaState.get().user?.grade || "grade-12";
    this.grade = document.getElementById("practice-grade");
    this.topic = document.getElementById("practice-topic");
    this.grade.value = /^grade-(8|9|10|11|12)$/.test(grade) ? grade : "grade-12";
    this.grade.onchange = () => this.loadGrade();
    this.topic.onchange = () => this.renderTopic();
    document.getElementById("practice-back").onclick = () => { this.renderTopic(); document.getElementById("practice-topic-title").focus(); };
    await this.loadGrade(params.get("topic"), params.get("lesson"));
  },
  clearWorkspace() {
    document.getElementById("practice-workspace").hidden = true;
    document.getElementById("practice-library").hidden = false;
    document.getElementById("practice-question-root").replaceChildren();
  },
  updateUrl(lesson) {
    const params = new URLSearchParams({ grade: this.grade.value });
    if (this.topic.value) params.set("topic", this.topic.value);
    if (lesson) params.set("lesson", lesson);
    history.replaceState(null, "", `practice.html?${params}`);
  },
  async loadGrade(selectedTopic, selectedLesson) {
    const request = ++this.requestNumber;
    this.clearWorkspace(); this.catalogue = null; this.topic.disabled = true;
    this.topic.innerHTML = '<option value="">Loading topics…</option>';
    document.getElementById("practice-lessons").replaceChildren();
    document.getElementById("practice-topic-title").textContent = "Choose a topic";
    document.getElementById("practice-count").textContent = "";
    document.getElementById("practice-status").textContent = "Loading practice…";
    try {
      const response = await AthenaAuth.fetch(`/api/v1/practice/catalogue/grades/${encodeURIComponent(this.grade.value)}`);
      if (!response.ok) throw new Error("Practice could not be loaded. Please try again.");
      const catalogue = await response.json();
      if (request !== this.requestNumber) return;
      this.catalogue = catalogue;
      this.topic.innerHTML = catalogue.topics.map(t => `<option value="${escapeHtml(t.id)}">Topic ${t.order}: ${escapeHtml(t.title)}</option>`).join("");
      this.topic.disabled = !catalogue.topics.length;
      if (catalogue.topics.some(t => t.id === selectedTopic)) this.topic.value = selectedTopic;
      this.renderTopic();
      const topic = this.currentTopic();
      const lesson = topic?.lessons.find(l => l.id === selectedLesson && l.question_count);
      if (lesson) await this.startLesson(lesson);
    } catch (error) {
      if (request !== this.requestNumber) return;
      this.topic.innerHTML = '<option value="">Topics unavailable</option>';
      const status = document.getElementById("practice-status");
      status.textContent = error.message + " ";
      const retry = document.createElement("button"); retry.className = "btn btn-secondary";
      retry.type = "button"; retry.textContent = "Retry"; retry.onclick = () => this.loadGrade(); status.append(retry);
    }
  },
  currentTopic() { return this.catalogue?.topics.find(t => t.id === this.topic.value); },
  renderTopic() {
    this.clearWorkspace(); this.updateUrl();
    const topic = this.currentTopic(), lessons = topic?.lessons || [];
    const available = lessons.filter(l => l.question_count > 0);
    document.getElementById("practice-topic-title").textContent = topic ? topic.title : "No topics available";
    document.getElementById("practice-count").textContent = `${available.length} lesson sets`;
    document.getElementById("practice-status").textContent = available.length
      ? `Grade ${this.catalogue.grade} · ${topic.paper ? topic.paper + " · " : ""}Choose a lesson below.`
      : "No self-guided practice is available for this topic yet. Choose another topic or review its lessons.";
    document.getElementById("practice-lessons").innerHTML = lessons.map(l => `<article class="card practice-lesson-row"><div><h3>Lesson ${l.order}: ${escapeHtml(l.title)}</h3><p>${l.question_count ? `${l.question_count} questions · ${l.choice_count} multiple-choice · ${l.question_count - l.choice_count} written-answer` : "Practice set not available yet"}</p></div>${l.question_count ? `<button class="btn btn-primary" type="button" data-practice-lesson="${escapeHtml(l.id)}">Start practice</button>` : `<a class="btn btn-ghost" href="lesson.html?lesson=${encodeURIComponent(l.id)}">Review lesson</a>`}</article>`).join("");
    document.querySelectorAll("[data-practice-lesson]").forEach(button => {
      button.onclick = () => this.startLesson(lessons.find(l => l.id === button.dataset.practiceLesson));
    });
  },
  async startLesson(lesson) {
    if (!lesson) return;
    this.updateUrl(lesson.id);
    document.getElementById("practice-status").textContent = `Grade ${this.catalogue.grade} · Practising: ${lesson.title}`;
    document.getElementById("practice-workspace").hidden = false;
    document.getElementById("practice-library").hidden = true;
    const title = document.getElementById("practice-lesson-title");
    title.textContent = lesson.title; title.focus();
    document.getElementById("practice-teaching-link").href = `lesson.html?lesson=${encodeURIComponent(lesson.id)}`;
    // A fresh mount detaches previous sessions safely when switching lessons.
    const host = document.createElement("div");
    document.getElementById("practice-question-root").replaceChildren(host);
    await new SelfGuidedPractice(host, lesson.id).mountPractice();
  }
};
document.addEventListener("DOMContentLoaded", () => PracticeHub.init());
