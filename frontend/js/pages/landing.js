document.addEventListener("DOMContentLoaded",async()=>{
  await AthenaAuth.restoreSession();renderNav("");
  const root=document.getElementById("landing-catalogue");
  try{
    const url="/api/v1/curriculum/grades",response=await fetch(url);
    if(!response.ok)throw new Error(`Request: ${url} · Status: ${response.status}`);
    const grades=await response.json();
    if(!Array.isArray(grades)||!grades.length)throw new Error(`Request: ${url} · Status: 200 · Empty catalogue`);
    root.innerHTML=grades.map(grade=>`<article class="card catalogue-preview-card"><div><span class="badge">${escapeLanding(grade.curriculum)}</span><span class="topic-number">${escapeLanding(grade.availability.replace("_"," "))}</span></div><h3>Grade ${grade.grade}</h3><p>${grade.topic_count} approved topics · ${grade.expected_lesson_count} ordered lessons</p><dl><div><dt>Published</dt><dd>${grade.published_interactive_lesson_count}</dd></div><div><dt>Interactive</dt><dd>${grade.interactive_lesson_count}</dd></div></dl><a class="btn btn-secondary" href="grade.html?grade=${encodeURIComponent(grade.id)}">${grade.topic_count?"View curriculum":"View source status"}</a></article>`).join("");
  }catch(error){root.innerHTML=`<article class="card" role="alert"><h3>Curriculum could not be loaded</h3><p>${escapeLanding(error.message)}</p></article>`;}
});
function escapeLanding(value){return String(value).replace(/[&<>"']/g,char=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char]));}
