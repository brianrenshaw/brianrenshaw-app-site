/* Focused lifecycle checks for the real landing controller, without a browser. */
const {readFileSync} = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
class Target {
  constructor() { this.listeners = {}; this.attrs = {}; this.textContent = ''; }
  addEventListener(name, fn) { (this.listeners[name] ||= []).push(fn); }
  emit(name) { for (const fn of this.listeners[name] || []) fn({}); }
  setAttribute(key, value) { this.attrs[key] = value; }
}
const flush = async () => { for (let i=0; i<8; i++) await Promise.resolve(); };
function setup(reduced=false) {
  const video=new Target(), toggle=new Target(), restart=new Target(), full=new Target(), status=new Target(), controls=new Target();
  Object.assign(video,{paused:true,ended:false,currentTime:0,loads:0,plays:0,loop:false, reject:false});
  video.load=()=>video.loads++;
  video.play=async()=>{video.plays++;if(video.reject)throw Error('blocked');video.paused=false;queueMicrotask(()=>video.emit('play'));};
  video.pause=()=>{if(!video.paused){video.paused=true;queueMicrotask(()=>video.emit('pause'));}};
  video.requestFullscreen=async()=>{video.fullscreen=true;};
  const fields={'video':video,'[data-video-toggle]':toggle,'[data-video-status]':status,'[data-video-restart]':restart,'[data-video-fullscreen]':full,'[data-video-controls]':controls};
  const demo={querySelector:s=>fields[s]}, doc=new Target();
  doc.hidden=false;doc.querySelectorAll=s=>s==='[data-metadata-demo]'?[demo]:[];
  const motion=new Target();motion.matches=reduced;
  const observers=[];
  class Observer {constructor(cb,opts){this.cb=cb;this.opts=opts;observers.push(this);} observe(){} disconnect(){}}
  vm.runInNewContext(readFileSync('site/ingest/assets/landing.js','utf8'),{document:doc,window:{IntersectionObserver:Observer},IntersectionObserver:Observer,matchMedia:()=>motion,console});
  return {video,toggle,restart,full,status,doc,motion,near:()=>observers[0].cb([{isIntersecting:true}]),view:r=>observers[1].cb([{isIntersecting:r>0,intersectionRatio:r}])};
}
(async()=>{
  let t=setup();assert.equal(t.video.loads,0);t.near();assert.equal(t.video.loads,1);
  t.view(.49);await flush();assert(t.video.paused);t.view(.5);await flush();assert(!t.video.paused&&t.video.loop);
  t.toggle.emit('click');await flush();assert(t.video.paused);t.view(0);t.view(1);await flush();assert(t.video.paused,'manual pause survives reentry');
  t.toggle.emit('click');await flush();assert(!t.video.paused);t.doc.hidden=true;t.doc.emit('visibilitychange');await flush();assert(t.video.paused);
  t.doc.hidden=false;t.doc.emit('visibilitychange');await flush();assert(!t.video.paused);
  t.view(0);await flush();assert(t.video.paused&&!t.video.loop);t.view(1);await flush();assert(!t.video.paused);
  t.video.pause();await flush();t.view(0);t.view(1);await flush();assert(t.video.paused,'native pause survives reentry');
  t.video.currentTime=20;t.restart.emit('click');await flush();assert.equal(t.video.currentTime,0);assert(!t.video.paused);
  t.full.emit('click');await flush();assert(t.video.fullscreen);
  t.motion.matches=true;t.motion.emit('change');await flush();assert(t.video.paused&&!t.video.loop);t.toggle.emit('click');await flush();assert(!t.video.paused&&!t.video.loop);
  t=setup(true);t.view(1);await flush();assert(t.video.paused&&!t.video.loop);t.toggle.emit('click');await flush();assert(!t.video.paused&&!t.video.loop);t.video.ended=true;t.video.paused=true;t.video.emit('ended');t.view(0);t.view(1);await flush();assert(t.video.paused);
  t=setup();t.video.reject=true;t.view(1);await flush();assert.equal(t.toggle.textContent,'Play');assert.match(t.status.textContent,/Press Play/);t.video.reject=false;t.toggle.emit('click');await flush();assert(!t.video.paused);
  t.video.emit('error');await flush();assert.equal(t.toggle.textContent,'Play');assert.match(t.status.textContent,/couldn’t load/);
  t=setup();t.view(1);t.view(0);await flush();assert(t.video.paused,'in-flight autoplay cannot continue offscreen');
  console.log('PASS: video visibility, looping, native/custom pause persistence, restart, fullscreen, reduced motion, autoplay rejection, load failure, and pending-play race.');
})().catch(error=>{console.error(error);process.exitCode=1;});
