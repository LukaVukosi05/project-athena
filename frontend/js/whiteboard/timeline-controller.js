class NarrationProvider {
  speak(){} pause(){} resume(){} stop(){} setMuted(){}
}

class BrowserNarrationProvider extends NarrationProvider {
  constructor() { super(); this.muted=false; }
  speak(text, rate=1) {
    if(this.muted || typeof window==="undefined" || !("speechSynthesis" in window)) return;
    const utterance=new SpeechSynthesisUtterance(text);utterance.lang="en-ZA";utterance.rate=rate;
    speechSynthesis.cancel();speechSynthesis.speak(utterance);
  }
  pause(){if(typeof speechSynthesis!=="undefined")speechSynthesis.pause();}
  resume(){if(typeof speechSynthesis!=="undefined")speechSynthesis.resume();}
  stop(){if(typeof speechSynthesis!=="undefined")speechSynthesis.cancel();}
  setMuted(muted){this.muted=muted;if(muted)this.stop();}
}

class PrerecordedNarrationProvider extends NarrationProvider {
  constructor(audioUrl,fallback=new BrowserNarrationProvider()){super();this.audioUrl=audioUrl;this.fallback=fallback;this.audio=null;this.muted=false;}
  speak(text,rate=1){if(this.muted)return;if(!this.audioUrl||typeof Audio==="undefined"){this.fallback.speak(text,rate);return;}this.stop();this.audio=new Audio(this.audioUrl);this.audio.playbackRate=rate;this.audio.muted=this.muted;this.audio.addEventListener("error",()=>this.fallback.speak(text,rate),{once:true});const result=this.audio.play();if(result?.catch)result.catch(()=>this.fallback.speak(text,rate));}
  pause(){this.audio?.pause();this.fallback.pause();}
  resume(){if(this.audio?.paused)this.audio.play().catch(()=>{});else this.fallback.resume();}
  stop(){if(this.audio){this.audio.pause();this.audio.currentTime=0;this.audio=null;}this.fallback.stop();}
  setMuted(muted){this.muted=muted;if(this.audio)this.audio.muted=muted;this.fallback.setMuted(muted);}
}

class TimelineController {
  constructor(stage, step, options={}) {
    this.stage=stage;this.step=step;this.caption=options.caption;
    this.narration=options.narration || new BrowserNarrationProvider();
    this.onStateChange=options.onStateChange || function(){};
    this.onCheckpoint=options.onCheckpoint || function(){};
    this.now=options.now || (()=>performance.now());
    this.requestFrame=options.requestFrame || (callback=>requestAnimationFrame(callback));
    this.cancelFrame=options.cancelFrame || (id=>cancelAnimationFrame(id));
    this.speed=1;this.position=0;this.cursor=0;this.playing=false;this.captions=true;this.destroyed=false;
  }
  play(){if(this.destroyed||this.playing)return;this.playing=true;this.startedAt=this.now()-this.position/this.speed;this.narration.resume();this.onStateChange(this);this.frame=this.requestFrame(time=>this.tick(time));}
  pause(){if(!this.playing)return;this.position=Math.min(this.step.duration_ms,(this.now()-this.startedAt)*this.speed);this.playing=false;if(this.frame!==undefined)this.cancelFrame(this.frame);this.narration.pause();this.onStateChange(this);}
  tick(time){if(!this.playing||this.destroyed)return;this.position=Math.min(this.step.duration_ms,(time-this.startedAt)*this.speed);while(this.cursor<this.step.events.length&&this.step.events[this.cursor].at_ms<=this.position){const event=this.step.events[this.cursor++];this.apply(event);if(event.type==="checkpoint"){this.pause();this.onCheckpoint(event,this);return;}}if(this.position>=this.step.duration_ms){this.playing=false;this.onStateChange(this);return;}this.frame=this.requestFrame(next=>this.tick(next));}
  apply(event){
    const nodes=(event.targets||[]).map(id=>this.stage.querySelector(`[data-object-id="${id}"]`)).filter(Boolean);
    if(event.type==="focus"){nodes.forEach(node=>{node.classList.remove("is-dimmed");node.classList.add("is-visible","is-focused");});}
    else if(event.type==="dim"){nodes.forEach(node=>node.classList.add("is-dimmed"));}
    else if(["reveal","write","replace","substitute","align","group","compare","verify"].includes(event.type)){nodes.forEach(node=>{node.classList.add("is-visible",`event-${event.type}`);if(event.style)node.classList.add(`meaning-${event.style}`);});}
    else if(["show_operation","calculate_difference","calculate_ratio"].includes(event.type))this.showCalculation(event,nodes);
    else if(event.type==="draw_arrow")this.drawArrow(event);
    else if(event.type==="caption"&&this.captions&&this.caption){this.caption.hidden=false;this.caption.textContent=event.text;}
    else if(event.type==="narration")this.narration.speak(event.text,this.speed);
    this.onStateChange(this,event);
  }
  drawArrow(event){const from=this.stage.querySelector(`[data-object-id="${event.from_target}"]`),to=this.stage.querySelector(`[data-object-id="${event.to_target}"]`),layer=this.stage.querySelector('[data-role="instruction-layer"]');if(!from||!to||!layer)return;const x1=Number(from.dataset.x),x2=Number(to.dataset.x),y=Number(from.dataset.y)+25;layer.insertAdjacentHTML("beforeend",`<g class="timeline-arrow" data-timeline-artifact><path d="M ${x1} ${y} Q ${(x1+x2)/2} ${y+30} ${x2} ${y}"/><text x="${(x1+x2)/2}" y="${y+38}" text-anchor="middle">${escapeWhiteboardHtml(event.label||"")}</text></g>`);(event.targets||[]).forEach(id=>this.stage.querySelector(`[data-object-id="${id}"]`)?.classList.add("is-visible"));}
  showCalculation(event,nodes){const layer=this.stage.querySelector('[data-role="instruction-layer"]');if(!layer)return;layer.querySelectorAll('[data-current-calculation]').forEach(node=>node.remove());layer.insertAdjacentHTML("beforeend",`<text data-current-calculation data-timeline-artifact x="310" y="165" text-anchor="middle" class="timeline-calculation">${escapeWhiteboardHtml(event.label||"")}</text>`);nodes.forEach(node=>node.classList.add("is-focused"));}
  setSpeed(speed){const wasPlaying=this.playing;if(wasPlaying)this.pause();this.speed=speed;if(wasPlaying)this.play();}
  setCaptions(enabled){this.captions=enabled;if(this.caption)this.caption.hidden=!enabled;}
  setMuted(muted){this.narration.setMuted(muted);}
  reset(){this.pause();this.narration.stop();this.position=0;this.cursor=0;this.stage.querySelectorAll("[data-timeline-artifact]").forEach(node=>node.remove());this.stage.querySelectorAll(".semantic-object").forEach(node=>node.setAttribute("class","semantic-object is-hidden"));if(this.caption){this.caption.textContent="";this.caption.hidden=!this.captions;}this.onStateChange(this);}
  replay(){this.reset();this.play();}
  completeReducedMotion(){this.reset();for(const event of this.step.events){if(event.type!=="checkpoint"&&event.type!=="narration")this.apply(event);}this.position=this.step.duration_ms;this.cursor=this.step.events.length;this.onStateChange(this);}
  destroy(){if(this.destroyed)return;this.pause();this.destroyed=true;this.narration.stop();this.stage.querySelectorAll("[data-timeline-artifact]").forEach(node=>node.remove());}
}
