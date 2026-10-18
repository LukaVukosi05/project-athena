class NarrationProvider {
  speak(){ return Promise.resolve("silent"); }
  pause(){} resume(){} stop(){} setMuted(){}
}

class BrowserNarrationProvider extends NarrationProvider {
  constructor(options={}) {
    super(); this.muted=false; this.generation=0; this.active=null;
    this.setTimer=options.setTimer || setTimeout; this.clearTimer=options.clearTimer || clearTimeout;
    this.now=options.now || (()=>Date.now());
    this.fallbackPollMs=Math.max(100,Number(options.fallbackPollMs)||500);
    this.maxSpeechMs=Math.max(30000,Number(options.maxSpeechMs)||300000);
  }
  synthesis(){ return typeof globalThis !== "undefined" ? globalThis.speechSynthesis : undefined; }
  finish(generation, reason) {
    if (!this.active || this.active.generation !== generation) return;
    const active=this.active; this.active=null;
    if(active.timer!==undefined)this.clearTimer(active.timer);
    active.resolve(reason);
  }
  handleFallback(generation) {
    if (!this.active || this.active.generation !== generation) return;
    const active=this.active,synthesis=this.synthesis(),now=this.now();
    active.timer=undefined;
    if (synthesis?.speaking && now < active.hardDeadlineAt) {
      this.armFallback(active,Math.min(this.fallbackPollMs,Math.max(100,active.hardDeadlineAt-now)));
      return;
    }
    this.finish(generation,now >= active.hardDeadlineAt ? "speech-timeout" : "fallback");
  }
  armFallback(active, delay) {
    active.remaining=Math.max(100,delay);active.timerStarted=this.now();
    active.timer=this.setTimer(()=>this.handleFallback(active.generation),active.remaining);
  }
  speak(text, rate=1) {
    this.stop();
    const synthesis=this.synthesis();
    if(this.muted || !synthesis || typeof SpeechSynthesisUtterance==="undefined")return Promise.resolve("unavailable");
    const generation=++this.generation;
    return new Promise(resolve=>{
      const utterance=new SpeechSynthesisUtterance(text);utterance.lang="en-ZA";utterance.rate=rate;
      const estimated=Math.min(this.maxSpeechMs,Math.max(5000,String(text).trim().split(/\s+/).length*700/rate+2500));
      const startedAt=this.now();
      const active={generation,resolve,utterance,timer:undefined,remaining:estimated,startedAt,hardDeadlineAt:startedAt+this.maxSpeechMs};
      this.active=active;
      utterance.onend=()=>this.finish(generation,"ended");utterance.onerror=()=>this.finish(generation,"error");
      this.armFallback(active,active.remaining);
      try{synthesis.speak(utterance);}catch(_){this.finish(generation,"error");}
    });
  }
  pause(){
    const synthesis=this.synthesis();if(!this.active)return;
    if(this.active.timer!==undefined){this.clearTimer(this.active.timer);this.active.timer=undefined;this.active.remaining=Math.max(250,this.active.remaining-(this.now()-this.active.timerStarted));}
    synthesis?.pause?.();
  }
  resume(){const synthesis=this.synthesis();if(!this.active)return;synthesis?.resume?.();if(this.active.timer===undefined)this.armFallback(this.active,this.active.remaining);}
  stop(){
    const active=this.active;this.generation+=1;this.active=null;
    if(active?.timer!==undefined)this.clearTimer(active.timer);
    try{this.synthesis()?.cancel?.();}catch(_){}
    active?.resolve("stopped");
  }
  setMuted(muted){this.muted=muted;if(muted)this.stop();}
}

class PrerecordedNarrationProvider extends NarrationProvider {
  constructor(audioUrl,fallback=new BrowserNarrationProvider()){super();this.audioUrl=audioUrl;this.fallback=fallback;this.audio=null;this.muted=false;this.generation=0;this.resolve=null;}
  speak(text,rate=1){
    this.stop();if(this.muted)return Promise.resolve("muted");
    if(!this.audioUrl||typeof Audio==="undefined")return this.fallback.speak(text,rate);
    const generation=++this.generation;
    return new Promise(resolve=>{this.resolve=resolve;this.audio=new Audio(this.audioUrl);this.audio.playbackRate=rate;this.audio.muted=this.muted;
      const finish=reason=>{if(generation!==this.generation)return;this.resolve=null;resolve(reason);};
      this.audio.addEventListener("ended",()=>finish("ended"),{once:true});
      this.audio.addEventListener("error",()=>{this.fallback.speak(text,rate).then(finish);},{once:true});
      const result=this.audio.play();if(result?.catch)result.catch(()=>this.fallback.speak(text,rate).then(finish));
    });
  }
  pause(){this.audio?.pause();this.fallback.pause();}
  resume(){if(this.audio?.paused)this.audio.play().catch(()=>{});else this.fallback.resume();}
  stop(){this.generation+=1;if(this.audio){this.audio.pause();this.audio.currentTime=0;this.audio=null;}this.fallback.stop();if(this.resolve){const resolve=this.resolve;this.resolve=null;resolve("stopped");}}
  setMuted(muted){this.muted=muted;if(muted)this.stop();this.fallback.setMuted(muted);}
}

class TimelineController {
  constructor(stage, step, options={}) {
    this.stage=stage;this.step=step;this.caption=options.caption;
    this.narration=options.narration || new BrowserNarrationProvider();
    this.onStateChange=options.onStateChange || function(){};this.onCheckpoint=options.onCheckpoint || function(){};
    this.now=options.now || (()=>performance.now());this.requestFrame=options.requestFrame || (callback=>requestAnimationFrame(callback));this.cancelFrame=options.cancelFrame || (id=>cancelAnimationFrame(id));
    this.speed=1;this.position=0;this.cursor=0;this.playing=false;this.captions=true;this.destroyed=false;this.visualComplete=false;this.narrationPending=0;this.session=1;
  }
  play(){
    if(this.destroyed||this.playing)return;this.playing=true;this.startedAt=this.now()-this.position/this.speed;this.narration.resume();this.onStateChange(this);
    if(this.visualComplete){this.maybeFinish();return;}
    this.frame=this.requestFrame(time=>this.tick(time));
  }
  pause(){if(!this.playing)return;this.position=Math.min(this.step.duration_ms,(this.now()-this.startedAt)*this.speed);this.playing=false;if(this.frame!==undefined)this.cancelFrame(this.frame);this.narration.pause();this.onStateChange(this);}
  tick(time){
    if(!this.playing||this.destroyed)return;this.position=Math.min(this.step.duration_ms,(time-this.startedAt)*this.speed);
    while(this.cursor<this.step.events.length&&this.step.events[this.cursor].at_ms<=this.position){const event=this.step.events[this.cursor++];this.apply(event);if(event.type==="checkpoint"){this.pause();this.onCheckpoint(event,this);return;}}
    if(this.position>=this.step.duration_ms){this.visualComplete=true;this.maybeFinish();return;}
    this.frame=this.requestFrame(next=>this.tick(next));
  }
  trackNarration(result){
    const session=this.session;this.narrationPending+=1;
    Promise.resolve(result).catch(()=>"error").then(()=>{if(this.destroyed||session!==this.session)return;this.narrationPending=Math.max(0,this.narrationPending-1);this.maybeFinish();});
  }
  maybeFinish(){if(!this.playing||!this.visualComplete||this.narrationPending>0)return;this.playing=false;this.position=this.step.duration_ms;this.onStateChange(this);}
  nodes(event){return (event.targets||[]).flatMap(id=>Array.from(this.stage.querySelectorAll(`[data-object-id="${id}"]`)));}
  reveal(nodes,eventType){nodes.forEach(node=>{node.classList.remove("is-hidden");node.classList.add("is-visible",`event-${eventType.replaceAll("_","-")}`);});}
  apply(event){
    const nodes=this.nodes(event);
    if(["focus","focus_object"].includes(event.type))nodes.forEach(node=>{node.classList.remove("is-dimmed");node.classList.add("is-visible","is-focused","event-focus-object");});
    else if(event.type==="dim")nodes.forEach(node=>node.classList.add("is-dimmed"));
    else if(event.type==="reveal"){
      this.stage.querySelectorAll('[data-object-id="operation"],[data-object-id="verification"]').forEach(node=>node.classList.add("is-hidden"));this.reveal(nodes,event.type);this.settleModel();
    }
    else if(["write","replace","simplify","substitute","align","group","compare","complete","show_question","set_goal","factor_expression","split_zero_product","calculate_discriminant","branch_roots","mark_number_line","shade_interval","reject_candidate","back_substitute","pair_solutions","preserve_restriction"].includes(event.type))this.reveal(nodes,event.type);
    else if(event.type==="apply_both_sides"){
      const affected=nodes.length?nodes:[
        this.stage.querySelector('[data-object-id="left-expression"]') || this.stage.querySelector('[data-object-id="left-side"]'),
        this.stage.querySelector('[data-object-id="right-expression"]') || this.stage.querySelector('[data-object-id="right-side"]'),
      ].filter(Boolean);
      affected.forEach(node=>node.classList.add("is-visible","is-focused","event-apply-both-sides"));
      this.stage.querySelectorAll('[data-object-id="left-operation"],[data-object-id="right-operation"]').forEach(node=>node.classList.add("is-visible","event-apply-both-sides"));
      this.stage.querySelectorAll(".equation-operation span").forEach(node=>node.classList.add("is-visible","event-apply-both-sides"));
    }
    else if(event.type==="cancel"){this.reveal(nodes,"cancel");this.stage.querySelectorAll('[data-object-id="cancellation"]').forEach(node=>node.classList.add("is-visible","event-cancel"));this.stage.querySelectorAll(".cancellation-label").forEach(node=>node.classList.add("is-visible","event-cancel"));}
    else if(["show_operation","calculate_difference","calculate_ratio"].includes(event.type))this.showCalculation(event,nodes);
    else if(event.type==="draw_arrow")this.drawArrow(event);
    else if(event.type==="caption"&&this.captions&&this.caption){this.caption.hidden=false;this.caption.textContent=event.text;}
    else if(event.type==="narration")this.trackNarration(this.narration.speak(event.text,this.speed));
    else if(event.type==="evaluate_expression"){this.reveal(nodes,event.type);nodes.forEach(node=>node.classList.add("is-transforming"));}
    else if(event.type==="introduce_inverse")this.reveal(nodes,event.type);
    else if(event.type==="apply_to_both_sides"){this.reveal(nodes,event.type);nodes.forEach(node=>node.classList.add("event-apply-both-sides"));}
    else if(event.type==="cancel_inverse_pair")this.reveal(nodes,event.type);
    else if(event.type==="simplify_expression")this.reveal(nodes,event.type);
    else if(event.type==="substitute_value"){this.reveal(nodes,event.type);nodes.forEach(node=>node.classList.add("is-substituting"));}
    else if(event.type==="replace_unknown")this.reveal(nodes,event.type);
    else if(event.type==="reverse_equality"){this.reveal(nodes,event.type);this.stage.querySelector(".g8-state--before")?.classList.add("is-reversing");}
    else if(event.type==="compare_both_sides")this.reveal(nodes,event.type);
    else if(event.type==="tilt_balance")this.setBalance("right-heavy",nodes);
    else if(event.type==="restore_balance")this.setBalance("level",nodes);
    else if(event.type==="mark_incorrect_step"){this.reveal(nodes,event.type);nodes.forEach(node=>node.classList.add("is-incorrect"));}
    else if(event.type==="repair_incorrect_step"){this.reveal(nodes,event.type);nodes.forEach(node=>node.classList.add("is-repaired"));}
    else if(event.type==="verify_original")this.reveal(nodes,event.type);
    else if(event.type==="show_conclusion")this.reveal(nodes,event.type);
    else if(event.type==="verify"){
      this.stage.querySelectorAll('[data-object-id="operation"],[data-object-id="result"]').forEach(node=>{node.classList.remove("is-visible");node.classList.add("is-hidden");});this.reveal(nodes,event.type);
    }
    this.onStateChange(this,event);
  }
  setBalance(state,nodes){const beams=nodes.length?nodes:Array.from(this.stage.querySelectorAll('[data-object-id="balance-beam"]'));beams.forEach(node=>{node.classList.remove("is-level","is-left-heavy","is-right-heavy");node.classList.add(`is-${state}`,"is-visible",`event-${state}`);node.dataset.balanceState=state;});}
  settleModel(){this.stage.querySelectorAll("[data-after-label]").forEach(node=>{node.textContent=node.dataset.afterLabel;node.classList.add("is-transforming");});this.stage.querySelectorAll('[data-object-id="balance-beam"][data-after-balance]').forEach(node=>this.setBalance(node.dataset.afterBalance,[node]));}
  drawArrow(event){const from=this.stage.querySelector(`[data-object-id="${event.from_target}"]`),to=this.stage.querySelector(`[data-object-id="${event.to_target}"]`),layer=this.stage.querySelector('[data-role="instruction-layer"]');if(!from||!to||!layer)return;const x1=Number(from.dataset.x),x2=Number(to.dataset.x),y=Number(from.dataset.y)+25;layer.insertAdjacentHTML("beforeend",`<g class="timeline-arrow" data-timeline-artifact><path d="M ${x1} ${y} Q ${(x1+x2)/2} ${y+30} ${x2} ${y}"/><text x="${(x1+x2)/2}" y="${y+38}" text-anchor="middle">${escapeWhiteboardHtml(event.label||"")}</text></g>`);}
  showCalculation(event,nodes){this.reveal(nodes,"show-operation");const strong=nodes[0]?.querySelector?.("strong");if(strong&&event.label)strong.textContent=event.label;}
  setSpeed(speed){const wasPlaying=this.playing;if(wasPlaying)this.pause();this.speed=speed;if(wasPlaying)this.play();}
  setCaptions(enabled){this.captions=enabled;if(this.caption)this.caption.hidden=!enabled;}
  setMuted(muted){this.narration.setMuted(muted);}
  reset(){
    if(this.playing)this.pause();this.session+=1;this.narration.stop();this.position=0;this.cursor=0;this.visualComplete=false;this.narrationPending=0;
    this.stage.querySelectorAll("[data-timeline-artifact]").forEach(node=>node.remove());
    this.stage.querySelectorAll(".is-focused,.is-dimmed,.is-visible,.is-transforming,.is-substituting,.is-reversing,.is-incorrect,.is-repaired").forEach(node=>node.classList.remove("is-focused","is-dimmed","is-visible","is-transforming","is-substituting","is-reversing","is-incorrect","is-repaired"));
    this.stage.querySelectorAll(".g8-timeline-object,.g8-conclusion,.g8-operation-path i").forEach(node=>node.classList.add("is-hidden"));
    if(this.caption){this.caption.textContent="";this.caption.hidden=!this.captions;}this.onStateChange(this);
  }
  replay(){this.reset();this.play();}
  completeReducedMotion(){this.reset();for(const event of this.step.events){if(event.type!=="checkpoint"&&event.type!=="narration")this.apply(event);}this.position=this.step.duration_ms;this.cursor=this.step.events.length;this.visualComplete=true;this.onStateChange(this);}
  destroy(){if(this.destroyed)return;this.session+=1;if(this.playing)this.pause();this.destroyed=true;this.narration.stop();this.stage.querySelectorAll("[data-timeline-artifact]").forEach(node=>node.remove());}
}
