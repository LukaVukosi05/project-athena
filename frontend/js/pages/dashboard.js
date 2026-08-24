document.addEventListener("DOMContentLoaded", async () => {
  const authenticatedUser=await AthenaAuth.requireSession();if(!authenticatedUser)return;renderNav("Learn");const state=AthenaState.get();
  const response=await fetch("/api/v1/curriculum/grades/grade-12",{headers:AthenaState.accessToken()?{Authorization:`Bearer ${AthenaState.accessToken()}`}:{}});
  if(!response.ok){document.getElementById("topics-list").innerHTML='<div class="card"><strong>Grade 12 curriculum could not be loaded.</strong></div>';return;}
  const grade=await response.json();document.getElementById("greeting").textContent=`${greetingWord()}, ${state.user.firstName} 👋`;document.getElementById("grade-label").textContent="Grade 12 Mathematics";
  document.getElementById("continue-link-label").textContent="Sequences and Series";document.getElementById("continue-link").href="topic.html?grade=grade-12&topic=sequences-series";document.getElementById("progress-pct").textContent="0%";document.getElementById("progress-fill").style.width="0%";
  document.getElementById("topics-list").innerHTML=grade.topics.map(topic=>`<a class="topic-row" href="topic.html?grade=grade-12&topic=${topic.id}" style="text-decoration:none;color:inherit;"><div class="topic-row__index">1</div><div class="topic-row__body"><strong>${escapeHtml(topic.title)}</strong><div class="topic-row__meta">${escapeHtml(topic.paper)} · ${topic.subtopic_count} learning path</div></div><span class="badge">Start</span></a>`).join("");
  document.getElementById("stat-progress").textContent="0%";document.getElementById("stat-lessons").textContent=state.completedLessons.length;document.getElementById("stat-plan").textContent=state.isPremium?"Premium":"Free";
});
function greetingWord(){const hour=new Date().getHours();return hour<12?"Good morning":hour<18?"Good afternoon":"Good evening";}
function escapeHtml(value){return String(value).replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));}
