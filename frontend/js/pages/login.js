/** Sign-in controller: resumable sessions, explicit providers and accessible feedback. */
document.addEventListener("DOMContentLoaded", async () => {
  renderNav("");
  const form = document.getElementById("login-form"), feedback = document.getElementById("login-feedback");
  const params = new URLSearchParams(location.search), next = AthenaAuth.safeNext(params.get("next"));
  const signup = document.querySelector('a[href="signup.html"]');
  if (signup) signup.href = `signup.html?next=${encodeURIComponent(next)}`;
  const errorMessages = {verification:"We couldn't verify that sign-in. Please try again or use email.", existing_account:"An email account already exists. Sign in with your email and password. Account linking is not available in this test build."};
  if (params.has("oauth_error")) feedback.textContent = errorMessages[params.get("oauth_error")] || "Sign-in was not completed. Please try again.";
  document.getElementById("toggle-password").onclick = event => {
    const password = document.getElementById("password"), visible = password.type === "password";
    password.type = visible ? "text" : "password";
    event.currentTarget.textContent = visible ? "Hide" : "Show";
    event.currentTarget.setAttribute("aria-pressed", String(visible));
  };
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const submit = form.querySelector('[type="submit"]');
    submit.disabled = true; submit.setAttribute("aria-busy", "true"); submit.textContent = "Signing in…";
    feedback.textContent = "Checking your account…";
    try {
      await AthenaAuth.login({email:document.getElementById("email").value.trim(), password:document.getElementById("password").value, rememberMe:document.getElementById("remember-me").checked});
      location.assign(next);
    } catch(error) {
      feedback.textContent = error.message; feedback.focus();
      submit.disabled = false; submit.removeAttribute("aria-busy"); submit.textContent = "Sign in →";
    }
  });
  for (const button of document.querySelectorAll('[data-provider]')) button.onclick = () => {
    const query = new URLSearchParams({next, remember:String(document.getElementById("remember-me").checked)});
    location.assign(`/api/v1/auth/oauth/${button.dataset.provider}/start?${query}`);
  };
  try {
    const providers = await AthenaAuth.request("/api/v1/auth/providers");
    for (const button of document.querySelectorAll('[data-provider]')) button.disabled = !providers[button.dataset.provider];
    document.getElementById("provider-note").textContent = providers.google && providers.apple ? "Choose the sign-in method you used for your account." : "Greyed-out options need setup in this test build. Email sign-in is available.";
  } catch(_) { document.getElementById("provider-note").textContent = "Other sign-in options couldn't load. You can still try email."; }
  if (!params.has("oauth_error")) try {
    const user = await AthenaAuth.restoreSession();
    if (user) location.replace(next);
  } catch(_) { feedback.textContent = "We couldn't reconnect. Your sign-in has been kept. Check your connection and retry."; }
});
