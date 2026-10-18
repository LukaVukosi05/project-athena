/* ============================================================
   PAGE CONTROLLER — Login (brief section 12)
   Phase 1 stub: any submitted email/password "logs in" as the
   locally stored learner. Real auth is backend/app/api/v1/auth.py.
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const submit = e.currentTarget.querySelector('button[type="submit"]');
    submit.disabled = true;
    submit.textContent = "Signing in...";
    document.getElementById("login-feedback").textContent = "Checking your account…";
    try {
      await AthenaAuth.login({
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value
      });
      const next = new URLSearchParams(location.search).get("next");
      location.href = next && next.startsWith("/") ? next : "dashboard.html";
    } catch (error) {
      document.getElementById("login-feedback").textContent = error.message;
      submit.disabled = false;
      submit.textContent = "Sign in";
    }
  });
});
