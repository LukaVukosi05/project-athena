/* ============================================================
   NAVIGATION — renders the shared top nav (brief section 9)
   ------------------------------------------------------------
   Kept deliberately small: five links, logo, and a profile
   slot. Every page calls renderNav("Learn") etc. so the active
   state lives in exactly one place.
   ============================================================ */
function renderNav(activeLabel) {
  const links = ["Learn", "Progress"];
  const state = AthenaState.get();
  const user = state.user;
  const mount = document.getElementById("nav-mount");
  if (!mount) return;

  mount.innerHTML = `
    <nav class="topnav">
      <div class="topnav__inner">
        <a href="index.html" class="topnav__logo"><span class="dot">▲</span> Project Athena</a>
        <div class="topnav__links">
          ${links.map(l => `<a href="${linkFor(l)}" class="${l === activeLabel ? "active" : ""}">${l}</a>`).join("")}
        </div>
        <div class="topnav__actions">
          ${user ? '<span class="badge">Grade 12</span>' : ""}
          <button id="theme-toggle" class="btn btn-ghost" aria-label="Toggle theme" style="padding:8px 10px;">🌙</button>
          ${user ? `<a href="dashboard.html" class="btn btn-ghost" style="padding:8px 14px;">Hi, ${escapeHtml(user.firstName)}</a><button type="button" class="btn btn-ghost" id="logout-btn">Sign out</button>` : `<a href="login.html" class="btn btn-ghost">Sign in</a>`}
        </div>
      </div>
    </nav>`;

  // Initialize theme toggle after mount
  initThemeToggle();
  const logout = document.getElementById("logout-btn");
  if (logout) logout.onclick = () => AthenaAuth.logout();
}
function linkFor(label) {
  switch (label) {
    case "Learn": return "dashboard.html";
    case "Practice": return "dashboard.html#practice";
    case "AI Tutor": return "dashboard.html#tutor";
    case "Past Papers": return "dashboard.html#papers";
    case "Progress": return "dashboard.html#progress";
    default: return "#";
  }
}
function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, s => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[s]));
}

/* Theme toggle helpers (keeps behaviour local to the frontend, non-invasive) */
function applyTheme(theme) {
  const root = document.documentElement;
  if (theme === 'dark') {
    root.setAttribute('data-theme', 'dark');
  } else {
    root.removeAttribute('data-theme');
  }
  try { localStorage.setItem('athena_theme', theme); } catch (e) { /* ignore */ }
  const btn = document.getElementById('theme-toggle');
  if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
}

function initThemeToggle() {
  // ensure toggle exists
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  // apply saved theme or default to light
  let saved = null;
  try { saved = localStorage.getItem('athena_theme'); } catch (e) { saved = null; }
  if (saved === 'dark') applyTheme('dark'); else applyTheme('light');
  // attach handler
  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });
}
