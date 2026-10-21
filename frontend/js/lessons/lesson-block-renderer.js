class LessonBlockRenderer {
  constructor(mount, lesson) { this.mount = mount; this.lesson = lesson; }
  render() {
    this.mount.innerHTML = `<section class="lesson-introduction card"><h3>Learning objective</h3><p>${escapeWhiteboardHtml(this.lesson.objective)}</p><h4>Why this matters</h4><p>${escapeWhiteboardHtml(this.lesson.why_it_matters)}</p><h4>Intuition first</h4><p>${escapeWhiteboardHtml(this.lesson.intuition)}</p></section><div data-role="blocks"></div>`;
    const blocks = this.mount.querySelector('[data-role="blocks"]');
    let questionSetMounted = false;
    this.lesson.blocks.forEach(block => {
      const host = document.createElement("div");
      host.className = `lesson-block lesson-block--${block.type}`;
      blocks.appendChild(host);
      if (block.type === "whiteboard" && !questionSetMounted) {
        questionSetMounted = true;
        const questions = this.lesson.whiteboard_questions?.length ? this.lesson.whiteboard_questions : [{ id: block.id, order: 1, difficulty: this.lesson.difficulty || "foundation", guidance_level: "high", is_core_example: true, whiteboard: block }];
        new WhiteboardQuestionSet(host, questions, { lessonId: this.lesson.id, teachingNotes: { why:this.lesson.why_it_matters, review:this.lesson.intuition }, solutionLoader: async (questionId, diagnosticAnswer, signal) => {
          const token = typeof AthenaState !== "undefined" ? AthenaState.accessToken() : null;
          const diagnosis = this.lesson.id === "g8-algebraic-equations-10";
          const response = await fetch(`/api/v1/lessons/${encodeURIComponent(this.lesson.id)}/questions/${encodeURIComponent(questionId)}/${diagnosis?'diagnose':'reveal'}`, { method: "POST", signal, headers: { ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(diagnosis ? { "Content-Type": "application/json" } : {}) }, ...(diagnosis ? { body: JSON.stringify({ first_error_and_repair: diagnosticAnswer }) } : {}) });
          if (!response.ok) throw new Error(response.status === 401 ? "Please sign in again to load this example." : response.status === 403 ? "This lesson requires access to the full course." : `The worked example could not be loaded (HTTP ${response.status}).`);
          return response.json();
        }, onPractice: () => {
          const practice = this.mount.querySelector(".lesson-block--practice, .lesson-block--checkpoint");
          if (practice) { practice.scrollIntoView({ behavior: "smooth", block: "start" }); practice.querySelector("button")?.focus(); }
        }}).mountSet();
      }
      else if (block.type === "past_paper_question") host.innerHTML = this.renderPastPaperBlock(block);
      else if (block.type === "practice" && block.data?.practice_bank_id) new SelfGuidedPractice(host, block.data.practice_bank_id, { lessonCount: this.lesson.lesson_count }).mountPractice();
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
      const paperPractice = data.assessment_mode === "paper_multiple_choice";
      const textbookSolution = typeof item !== "string" && item.solution_steps ? (paperPractice
        ? `<details class="textbook-solution"><summary>Show textbook solution</summary><div class="solution-paper"><h4>Worked solution</h4><ol>${item.solution_steps.map(step => `<li>${escapeWhiteboardHtml(step)}</li>`).join("")}</ol><p><strong>Answer:</strong> ${escapeWhiteboardHtml(item.answer)}</p></div></details>`
        : `<div class="worked-solution-mount" data-solution="${index}" hidden></div>`) : "";
      const options = typeof item !== "string" && item.options && !paperPractice ? `<p class="paper-instruction">${escapeWhiteboardHtml(item.instruction || "Work on paper first.")}</p><div class="question-options">${item.options.map((option, optionIndex) => `<button type="button" class="quiz-option" data-question-index="${index}" data-option-index="${optionIndex}">${escapeWhiteboardHtml(option)}</button>`).join("")}</div><p class="question-feedback" hidden></p>` : "";
      const answerInput = typeof item !== "string" && item.input_type === "math" ? `<form class="math-answer" data-answer-form="${index}"><label for="answer-${index}">Your answer</label><input id="answer-${index}" inputmode="text" autocomplete="off" aria-describedby="feedback-${index}"><button class="btn btn-primary" type="submit">Submit</button></form><p id="feedback-${index}" class="question-feedback" hidden></p>` : "";
      return `<article class="practice-question" data-question="${index}"><span class="badge">${escapeWhiteboardHtml(difficulty)}</span><strong>Question ${index + 1}</strong><p>${escapeWhiteboardHtml(question)}</p>${paperPractice ? `<p class="paper-instruction">${escapeWhiteboardHtml(item.instruction)}</p>${textbookSolution}` : (answerInput ? answerInput + textbookSolution : options ? options + textbookSolution : textbookSolution || (answer ? `<details><summary>Check answer</summary><p>${escapeWhiteboardHtml(answer)}</p></details>` : ""))}</article>`;
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
    host.querySelectorAll("[data-answer-form]").forEach(form => form.onsubmit = event => {
      event.preventDefault();
      const questionIndex = Number(form.dataset.answerForm);
      const question = data.questions[questionIndex];
      const input = form.querySelector("input");
      const normalise = value => String(value).toLowerCase().replace(/\s+/g, "").replace(/−/g, "-");
      const accepted = question.accepted_answers || [question.answer];
      const correct = accepted.some(answer => normalise(answer) === normalise(input.value));
      selected.set(questionIndex, correct);
      input.disabled = true; form.querySelector("button").disabled = true;
      const feedback = form.parentElement.querySelector(".question-feedback");
      feedback.hidden = false; feedback.className = `question-feedback quiz-feedback ${correct ? "correct" : "incorrect"}`;
      feedback.textContent = correct ? "Correct ✓" : "Not quite.";
      if (!correct) {
        const actions = document.createElement("div"); actions.className = "productive-struggle";
        const retry = document.createElement("button"); retry.type = "button"; retry.className = "btn btn-secondary"; retry.textContent = "Try Again";
        retry.onclick = () => { selected.delete(questionIndex); input.disabled = false; input.value = ""; form.querySelector("button").disabled = false; feedback.hidden = true; actions.remove(); input.focus(); };
        actions.appendChild(retry); feedback.after(actions);
        if (question.hints?.length) {
          const hint = document.createElement("button"); hint.type = "button"; hint.className = "btn btn-ghost"; hint.textContent = "Give Me a Hint"; hint.setAttribute("aria-expanded", "false");
          const hintText = document.createElement("p"); hintText.hidden = true; hintText.textContent = question.hints[0];
          hint.onclick = () => { hintText.hidden = false; hint.setAttribute("aria-expanded", "true"); };
          actions.append(hint, hintText);
        }
      }
      const solutionMount = form.parentElement.querySelector(".worked-solution-mount");
      if (solutionMount) { solutionMount.hidden = false; new WorkedSolution(solutionMount, { steps: question.solution_steps, whyExplanations: question.why_explanations, answer: question.answer }).mountSolution(); }
    });
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
      if (!correct) {
        const struggle = document.createElement("div");
        struggle.className = "productive-struggle";
        struggle.innerHTML = `<button type="button" class="btn btn-secondary" data-action="try-again">Try Again</button>${question.hints?.length ? '<button type="button" class="btn btn-ghost" data-action="hint" aria-expanded="false">Give Me a Hint</button><p data-role="question-hint" hidden></p>' : ""}`;
        feedback.after(struggle);
        struggle.querySelector('[data-action="try-again"]').onclick = () => { selected.delete(questionIndex); article.querySelectorAll("[data-option-index]").forEach(option => { option.disabled = false; option.classList.remove("correct", "incorrect"); }); feedback.hidden = true; struggle.remove(); const solution = article.querySelector(".worked-solution-mount"); if (solution) solution.hidden = true; };
        const hintButton = struggle.querySelector('[data-action="hint"]');
        if (hintButton) hintButton.onclick = () => { const hint = struggle.querySelector('[data-role="question-hint"]'); hint.hidden = false; hint.textContent = question.hints[0]; hintButton.setAttribute("aria-expanded", "true"); };
      }
      const solutionMount = article.querySelector(".worked-solution-mount");
      if (solutionMount) {
        solutionMount.hidden = false;
        new WorkedSolution(solutionMount, { steps: question.solution_steps, whyExplanations: question.why_explanations, answer: question.answer }).mountSolution();
      }
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
