document.addEventListener("DOMContentLoaded", async () => {
  renderNav("");
  const feedback=document.getElementById("profile-feedback"), form=document.getElementById("profile-form");
  let pending;
  try {
    pending=await AthenaAuth.request("/api/v1/auth/oauth/pending");
    document.getElementById("provider-account").textContent=`Signed in with ${pending.provider === "apple" ? "Apple" : "Google"} as ${pending.email}. Choose where to start.`;
    document.getElementById("first-name").value=pending.first_name;
  } catch(error) { feedback.textContent=error.message;form.querySelector('button').disabled=true;return; }
  form.onsubmit=async event=>{
    event.preventDefault();const button=form.querySelector('button');button.disabled=true;
    try{
      const response=await AthenaAuth.fetch("/api/v1/auth/oauth/complete",{method:"POST",headers:{"Content-Type":"application/json","X-CSRF-Token":pending.csrf},body:JSON.stringify({first_name:document.getElementById("first-name").value.trim(),grade:document.getElementById("grade").value,curriculum_mode:document.getElementById("curriculum").value})});
      const session=await response.json();if(!response.ok)throw new Error(typeof session.detail==="string"?session.detail:"Check your details and try again.");
      AthenaState.setSession(session);location.assign(AthenaAuth.safeNext(response.headers.get("X-Athena-Next")));
    }catch(error){feedback.textContent=error.message;button.disabled=false;}
  };
});
