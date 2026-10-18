function renderNav(activeLabel) {
  const links = ["Learn", "Practice", "Past Papers", "Progress", "Account"];
  const state = AthenaState.get(), user = state.user, mount = document.getElementById("nav-mount");
  if (!mount) return;
  mount.innerHTML = `<nav class="topnav"><div class="topnav__inner">
    <a href="index.html" class="topnav__logo" aria-label="Project Athena home">Project Athena</a>
    <div class="topnav__links" id="primary-nav">${links.map(label=>`<a href="${linkFor(label)}" class="${label===activeLabel?"active":""}">${label}</a>`).join("")}</div>
    <div class="topnav__actions">${user?`<span class="badge">${escapeHtml(String(user.grade||"grade-12").replace("grade-","Grade "))}</span>`:""}<button id="nav-menu-toggle" class="btn btn-ghost nav-menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">Menu</button>${user?`<a href="account.html" class="btn btn-ghost profile-link">${escapeHtml(user.firstName)}</a>`:`<a href="login.html" class="btn btn-ghost">Sign in</a>`}</div>
  </div></nav>`;
  const menu=document.getElementById("nav-menu-toggle");menu.onclick=()=>{const open=mount.querySelector(".topnav").classList.toggle("is-open");menu.setAttribute("aria-expanded",String(open));};
}
function linkFor(label){return {"Learn":"dashboard.html","Practice":"dashboard.html#practice","Past Papers":"past-papers.html","Progress":"progress.html","Account":"account.html"}[label]||"#";}
function escapeHtml(str){return String(str).replace(/[&<>"']/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[s]));}
