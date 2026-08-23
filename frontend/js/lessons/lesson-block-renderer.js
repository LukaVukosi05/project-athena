class LessonBlockRenderer {
  constructor(mount, lesson) { this.mount = mount; this.lesson = lesson; }
  render() {
    this.mount.innerHTML = `<section class="lesson-introduction card"><h3>Learning objective</h3><p>${escapeWhiteboardHtml(this.lesson.objective)}</p><h4>Why this matters</h4><p>${escapeWhiteboardHtml(this.lesson.why_it_matters)}</p><h4>Intuition first</h4><p>${escapeWhiteboardHtml(this.lesson.intuition)}</p></section><div data-role="blocks"></div>`;
    const blocks = this.mount.querySelector('[data-role="blocks"]');
    this.lesson.blocks.forEach(block => {
      const host = document.createElement("div");
      host.className = `lesson-block lesson-block--${block.type}`;
      blocks.appendChild(host);
      if (block.type === "whiteboard") new StatefulWhiteboard(host, block).mountBoard();
      else if (block.type === "past_paper_question") host.innerHTML = this.renderPastPaperBlock(block);
      else {
        host.innerHTML = this.renderContentBlock(block);
        this.wireContentBlock(host, block);
      }
    });
  }

  renderContentBlock(block) {
    const data = block.data || {};
    const choices = data.options ? `<div class="practice-choices">${data.options.map((option, index) => `<button type="button" class="btn btn-ghost" data-choice="${index}">${escapeWhiteboardHtml(option)}</button>`).join("")}</div><p class="checkpoint-feedback" hidden></p>` : "";
    const hints = data.hints ? `<details><summary>Show hints</summary><ol>${data.hints.map(hint => `<li>${escapeWhiteboardHtml(hint)}</li>`).join("")}</ol></details>` : "";
    const worked = data.worked_answer ? `<details><summary>Show worked answer</summary><ol>${data.worked_answer.map(line => `<li class="eq">${escapeWhiteboardHtml(line)}</li>`).join("")}</ol></details>` : "";
    const questions = data.questions ? `<div class="practice-question-list">${data.questions.map((item, index) => {
      const question = typeof item === "string" ? item : item.question;
      const difficulty = typeof item === "string" ? "Practice" : item.difficulty;
      const answer = typeof item === "string" ? null : item.answer;
      const textbookSolution = typeof item !== "string" && item.solution_steps ? `<details class="textbook-solution"><summary>Show textbook solution</summary><div class="solution-paper"><h4>Worked solution</h4><ol>${item.solution_steps.map(step => `<li>${escapeWhiteboardHtml(step)}</li>`).join("")}</ol><p><strong>Answer:</strong> ${escapeWhiteboardHtml(item.answer)}</p></div></details>` : "";
      const paperPractice = data.assessment_mode === "paper_multiple_choice";
      const options = typeof item !== "string" && item.options && !paperPractice ? `<p class="paper-instruction">${escapeWhiteboardHtml(item.instruction || "Work on paper first.")}</p><div class="question-options">${item.options.map((option, optionIndex) => `<button type="button" class="quiz-option" data-question-index="${index}" data-option-index="${optionIndex}">${escapeWhiteboardHtml(option)}</button>`).join("")}</div><p class="question-feedback" hidden></p>` : "";
      return `<article class="practice-question" data-question="${index}"><span class="badge">${escapeWhiteboardHtml(difficulty)}</span><strong>Question ${index + 1}</strong><p>${escapeWhiteboardHtml(question)}</p>${paperPractice ? `<p class="paper-instruction">${escapeWhiteboardHtml(item.instruction)}</p>${textbookSolution}` : (options || textbookSolution || (answer ? `<details><summary>Check answer</summary><p>${escapeWhiteboardHtml(answer)}</p></details>` : ""))}</article>`;
    }).join("")}</div>` : "";
    const markup = `<section class="card"><h3>${escapeWhiteboardHtml(block.title)}</h3><p>${escapeWhiteboardHtml(block.content)}</p>${choices}${hints}${worked}${questions}</section>`;
    return markup;
  }

  renderPastPaperBlock(block) {
    const data = block.data || {};
    return `<section class="card past-paper-block"><div class="past-paper-heading"><div><span class="badge">Exact DBE question</span><h3>${escapeWhiteboardHtml(block.title)}</h3></div><strong>${data.marks} marks</strong></div>
      <p>${escapeWhiteboardHtml(block.content)}</p><p class="topic-row__meta">${escapeWhiteboardHtml(data.source)} · Paper pages ${escapeWhiteboardHtml(data.pages)}</p>
      <iframe src="${escapeWhiteboardHtml(data.source_url)}" title="${escapeWhiteboardHtml(block.title)}" loading="lazy"></iframe>
      <p><a class="btn btn-secondary" href="${escapeWhiteboardHtml(data.source_url)}" target="_blank" rel="noopener">Open exact paper in a new tab</a></p>
      ${data.memorandum_status === "required" ? '<p class="watch-out"><strong>MARKING NOTE:</strong> Official memorandum not found in the supplied folder. Do not treat an unverified generated solution as an official answer.</p>' : ""}</section>`;
  }

  wireContentBlock(host, block) {
    const data = block.data || {};
    host.querySelectorAll(`[data-choice]`).forEach(button => button.onclick = () => {
        const panel = button.closest("section").querySelector(".checkpoint-feedback");
        const correct = Number(button.dataset.choice) === data.correct_index;
        panel.hidden = false;
        panel.textContent = correct ? `Correct. ${data.feedback || ""}` : "Not yet. Review the lesson idea and try again.";
        panel.className = `checkpoint-feedback quiz-feedback ${correct ? "correct" : "incorrect"}`;
    });
    const selected = new Map();
    host.querySelectorAll("[data-option-index]").forEach(button => button.onclick = () => {
      const questionIndex = Number(button.dataset.questionIndex);
      if (selected.has(questionIndex)) return;
      const question = data.questions[questionIndex];
      const optionIndex = Number(button.dataset.optionIndex);
      const correct = optionIndex === question.correct_index;
      selected.set(questionIndex, correct);
      const article = button.closest(".practice-question");
      article.querySelectorAll("[data-option-index]").forEach(option => {
        option.disabled = true;
        if (Number(option.dataset.optionIndex) === question.correct_index) option.classList.add("correct");
        else if (option === button) option.classList.add("incorrect");
      });
      const feedback = article.querySelector(".question-feedback");
      feedback.hidden = false;
      feedback.className = `question-feedback quiz-feedback ${correct ? "correct" : "incorrect"}`;
      feedback.textContent = `${correct ? "Correct." : "Not yet."} ${question.explanation}`;
      if (data.assessment_mode === "scored_multiple_choice" && selected.size === data.questions.length) {
        const score = [...selected.values()].filter(Boolean).length;
        const passed = score / data.questions.length >= (data.pass_mark || 0.7);
        const result = document.createElement("p");
        result.className = `quiz-feedback ${passed ? "correct" : "incorrect"}`;
        result.textContent = `${score} of ${data.questions.length} correct. ${passed ? "Mastery check passed." : "Review your written methods and try the lesson again."}`;
        host.querySelector("section").appendChild(result);
      }
    });
  }
}
