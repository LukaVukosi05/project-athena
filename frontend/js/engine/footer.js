// One footer for every customer page; independent of authentication and page data.
document.addEventListener("DOMContentLoaded", () => {
  const mount = document.getElementById("site-footer");
  if (!mount) return;
  mount.innerHTML = `<div class="container">
    <div class="site-footer__main">
      <div class="site-footer__brand">
        <a class="site-footer__logo" href="index.html">Project Athena</a>
        <p>Maths, one step at a time.</p>
        <span>CAPS-aligned Mathematics · Grades 8–12</span>
      </div>
      <nav class="site-footer__nav" aria-label="Footer learning">
        <h2>Learning</h2>
        <a href="index.html">Learn</a>
        <a href="practice.html">Practice</a>
        <a href="past-papers.html">Past papers</a>
      </nav>
      <nav class="site-footer__nav" aria-label="Footer account">
        <h2>Your Athena</h2>
        <a href="account.html">Your account</a>
        <a href="checkout.html">Membership and billing</a>
      </nav>
    </div>
    <div class="site-footer__bottom">
      <span>© ${new Date().getFullYear()} Project Athena. All rights reserved.</span>
      <span>For South African learners.</span>
    </div>
  </div>`;
});
