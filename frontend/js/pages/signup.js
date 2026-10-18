/* ============================================================
   PAGE CONTROLLER — Sign-up (brief section 11, 3 steps)
   Phase 1: writes straight to AthenaState (no real backend
   account yet — see backend/app/api/v1/auth.py).
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  let step = 1;
  const total = 3;
  const answers = { firstName: "", email: "", password: "", grade: "grade-12", mode: "CAPS", goal: "" };
  const root = document.getElementById("signup-root");

  render();

  function render() {
    document.getElementById("step-dots").innerHTML =
      Array.from({ length: total }, (_, i) => `<span class="${i + 1 === step ? "active" : ""}"></span>`).join("");

    if (step === 1) root.innerHTML = step1();
    else if (step === 2) root.innerHTML = step2();
    else root.innerHTML = step3();

    wireStep();
  }

  function step1() {
    return `
      <h2>Create your account</h2>
      <p>Just the basics — you can add more later.</p>
      <div class="field"><label for="firstName">First name</label><input id="firstName" value="${escapeHtml(answers.firstName)}" /></div>
      <div class="field"><label for="email">Email</label><input id="email" type="email" value="${escapeHtml(answers.email)}" /></div>
      <div class="field"><label for="password">Password</label><input id="password" type="password" /></div>
      <button class="btn btn-primary btn-block" data-action="next">Continue</button>
      <div class="divider">or</div>
      <button class="btn btn-ghost btn-block" type="button">Continue with Google</button>`;
  }

  function step2() {
    const grades = ["grade-8", "grade-9", "grade-10", "grade-11", "grade-12"];
    const showMode = true;
    return `
      <h2>Tell us about your learning</h2>
      ${grades.map(g => `<button type="button" class="choice-tile ${answers.grade === g ? "selected" : ""}" data-grade="${g}">${g.replace("grade-", "Grade ")}</button>`).join("")}
      ${showMode ? `
        <p style="margin-top:16px;font-weight:600;font-size:var(--fs-sm);">Curriculum / Assessment</p>
        ${["CAPS", "IEB", "I'm not sure"].map(m => `<button type="button" class="choice-tile ${answers.mode === m ? "selected" : ""}" data-mode="${m}">${m}</button>`).join("")}
      ` : ""}
      <div style="display:flex;gap:12px;margin-top:16px;">
        <button class="btn btn-ghost" data-action="back">Back</button>
        <button class="btn btn-primary btn-block" data-action="next">Continue</button>
      </div>`;
  }

  function step3() {
    const goals = ["Improve my marks", "Prepare for exams", "Understand difficult topics", "Get homework help", "Practise regularly"];
    return `
      <h2>What's your learning goal?</h2>
      ${goals.map(g => `<button type="button" class="choice-tile ${answers.goal === g ? "selected" : ""}" data-goal="${g}">${g}</button>`).join("")}
      <div style="display:flex;gap:12px;margin-top:16px;">
        <button class="btn btn-ghost" data-action="back">Back</button>
        <button class="btn btn-primary btn-block" data-action="finish">Start learning</button>
      </div>`;
  }

  function wireStep() {
    root.querySelectorAll("[data-grade]").forEach(b => b.onclick = () => { answers.grade = b.dataset.grade; render(); });
    root.querySelectorAll("[data-mode]").forEach(b => b.onclick = () => { answers.mode = b.dataset.mode; render(); });
    root.querySelectorAll("[data-goal]").forEach(b => b.onclick = () => { answers.goal = b.dataset.goal; render(); });

    const back = root.querySelector('[data-action="back"]');
    if (back) back.onclick = () => { step--; render(); };

    const next = root.querySelector('[data-action="next"]');
    if (next) next.onclick = () => {
      if (step === 1) {
        const fn = document.getElementById("firstName").value.trim();
        const em = document.getElementById("email").value.trim();
        const pw = document.getElementById("password").value;
        if (!fn || !em || !pw) { alert("Please enter your name, email and password."); return; }
        if (pw.length < 8) { alert("Your password must be at least 8 characters."); return; }
        answers.firstName = fn; answers.email = em; answers.password = pw;
      }
      if (step === 2 && !answers.grade) { alert("Please choose your grade."); return; }
      step++; render();
    };

    const finish = root.querySelector('[data-action="finish"]');
    if (finish) finish.onclick = async () => {
      finish.disabled = true;
      finish.textContent = "Creating account...";
      try {
        await AthenaAuth.signup(answers);
        location.href = "dashboard.html";
      } catch (error) {
        alert(error.message);
        finish.disabled = false;
        finish.textContent = "Start learning";
      }
    };
  }
});

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, s => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[s]));
}
