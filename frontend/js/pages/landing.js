document.addEventListener("DOMContentLoaded",async()=>{
  let user = null;
  try { user = await AthenaAuth.restoreSession(); } catch (_) {}
  renderNav("Learn");
  if (user) {
    const account = document.getElementById("landing-account-link");
    if (account) { account.textContent="Your account"; account.href="account.html"; }
    try {
      const membership = await AthenaAuth.request("/api/v1/payments/status");
      const cta=document.getElementById("landing-primary-cta");
      if (cta) { cta.textContent=membership.has_access ? "Continue learning" : "Start my 14-day free trial"; cta.href=membership.has_access ? `grade.html?grade=${encodeURIComponent(user.grade)}` : "checkout.html"; }
    } catch (_) { /* Keep the existing offer and allow the learner to retry. */ }
  }
});
