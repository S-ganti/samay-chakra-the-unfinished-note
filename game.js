'use strict';
const canvas=document.querySelector('#world'),ctx=canvas.getContext('2d'),menu=document.querySelector('#menu');
const P=WorldPhysics,keys=new Set(),images=places.map(p=>{let im=new Image();im.src=`art/clean/${p.file}.png`;return im;});
let realm=0,player=P.spawn(),terrain=P.platforms(0),camera=0,last=0,time=0,paused=true,changing=false,jump=false,sound=true,ambience=null,toastTimer;
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function resize(){canvas.width=Math.round(innerWidth*Math.min(devicePixelRatio,2));canvas.height=Math.round(innerHeight*Math.min(devicePixelRatio,2));}addEventListener('resize',resize);resize();
function notify(t){const el=document.querySelector('#toast');el.textContent=t;el.style.opacity=1;clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.style.opacity=0,3500);}
function audio(){if(sound&&!paused){if(!ambience)ambience=new Ambience();ambience.volume=.22;ambience.start(places[realm]).catch(()=>notify('Sound unavailable in this browser'));}else ambience?.stop();}
function choose(i){listening=0;resonance=0;silentTime=0;nearShrine=-1;document.querySelector('#memory').classList.remove('show');realm=(i+8)%8;player=P.spawn();terrain=P.platforms(realm);camera=0;document.querySelector('#title').textContent=places[realm].title;document.querySelector('#period').textContent=places[realm].time+' · '+places[realm].raga;document.querySelectorAll('#chapters button').forEach((b,n)=>b.classList.toggle('active',n===realm));try{localStorage.setItem('samay-place',realm)}catch{}audio();}
function pause(){paused=true;keys.clear();jump=false;ambience?.stop();menu.showModal();document.querySelector('#begin').textContent='Continue the journey';}
function resume(){menu.close();paused=false;keys.clear();last=performance.now();audio();}
async function transition(dir){if(changing)return;changing=true;keys.clear();document.querySelector('#curtain').classList.add('dark');await new Promise(r=>setTimeout(r,850));choose(realm+dir);document.querySelector('#curtain').classList.remove('dark');notify(places[realm].mood);setTimeout(()=>changing=false,850);}
document.querySelector('#begin').onclick=resume;document.querySelector('#pause').onclick=pause;menu.addEventListener('cancel',e=>{e.preventDefault();resume()});document.querySelector('#sound').onclick=()=>{sound=!sound;document.querySelector('#sound').textContent=sound?'Sound on':'Sound off';audio()};
places.forEach((p,i)=>{let b=document.createElement('button');let img=document.createElement('img');img.src=images[i].src;img.alt='';b.append(img);let s=document.createElement('span');s.textContent=`${String(i+1).padStart(2,'0')} ${p.title}`;b.append(s);b.onclick=()=>{choose(i);resume();notify(p.mood)};document.querySelector('#chapters').append(b)});
addEventListener('keydown',e=>{if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();if(e.code==='Escape'&&!paused){e.preventDefault();pause();return;}if(e.code==='KeyJ'&&!paused){pause();document.querySelector('#journal-pages').scrollIntoView({behavior:'smooth'});return;}if(paused)return;if(e.code==='Space'&&!e.repeat)jump=true;keys.add(e.code)});addEventListener('keyup',e=>keys.delete(e.code));addEventListener('blur',()=>{if(!paused)pause()});document.addEventListener('visibilitychange',()=>{if(document.hidden&&!paused)pause()});
document.querySelectorAll('[data-key]').forEach(b=>{b.onpointerdown=e=>{e.preventDefault();b.setPointerCapture(e.pointerId);keys.add(b.dataset.key);if(b.dataset.key==='Space')jump=true};b.onpointerup=b.onpointercancel=()=>keys.delete(b.dataset.key)});
function draw(){
 const w=canvas.width,h=canvas.height,scale=Math.min(w/1500,h/820),vw=w/scale,vh=h/scale,groundY=vh*.81;
 ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#15221f';ctx.fillRect(0,0,w,h);
 drawLivingBackdrop(images[realm],w,h,vw);
 const wash=ctx.createLinearGradient(0,h*.5,0,h);wash.addColorStop(0,'#0b191400');wash.addColorStop(1,'#09161199');ctx.fillStyle=wash;ctx.fillRect(0,0,w,h);
 ctx.setTransform(scale,0,0,scale,-camera*scale,(groundY-690)*scale);
 for(const s of terrain)drawTerrainPlatform(s);
 drawShrines();
 // Original luminous traveler: cloth silhouette and a trailing ribbon.
 const x=player.x,y=player.y,dir=player.vx< -5?-1:1;ctx.save();ctx.translate(x,y);ctx.scale(dir,1);ctx.shadowColor='#fff4cf';ctx.shadowBlur=14;ctx.fillStyle='#f2e8cd';ctx.beginPath();ctx.moveTo(0,-32);ctx.quadraticCurveTo(7,-18,13,-3);ctx.quadraticCurveTo(0,2,-11,-3);ctx.closePath();ctx.fill();ctx.beginPath();ctx.arc(0,-36,4,0,7);ctx.fill();ctx.shadowBlur=0;ctx.strokeStyle='#dfa65e';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(-2,-29);ctx.bezierCurveTo(-18,-24,-26,-40+Math.sin(time*3)*5,-42,-27);ctx.stroke();ctx.restore();
 ctx.strokeStyle='#e8c89180';ctx.lineWidth=1;ctx.beginPath();ctx.arc(P.WORLD-38,620,37,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.arc(P.WORLD-38,620,28,0,Math.PI*2);ctx.stroke();
 ctx.setTransform(1,0,0,1,0,0);

 const vignette=ctx.createRadialGradient(w/2,h/2,h*.2,w/2,h/2,Math.max(w,h)*.7);vignette.addColorStop(0,'#0000');vignette.addColorStop(1,'#06100e88');ctx.fillStyle=vignette;ctx.fillRect(0,0,w,h);
}
function frame(now){let dt=Math.min((now-last)/1000,.033);last=now;if(!paused&&!changing){time+=dt;updateListening(dt);const result=P.step(player,{move:(keys.has('KeyD')||keys.has('ArrowRight')?1:0)-(keys.has('KeyA')||keys.has('ArrowLeft')?1:0),jump,fly:keys.has('KeyW')||keys.has('ArrowUp')},dt,terrain);jump=false;const vw=canvas.width/Math.min(canvas.width/1500,canvas.height/820);camera+=(Math.max(0,Math.min(P.WORLD-vw,player.x-vw*.35))-camera)*Math.min(1,dt*3);if(result==='exit')transition(1);if(result==='respawn')notify('The path welcomes you back. Hold flight to cross the water.');}draw();requestAnimationFrame(frame);}
let saved=0;try{saved=Number(localStorage.getItem('samay-place'))||0}catch{}choose(Math.max(0,Math.min(7,saved)));updateJournal();menu.showModal();requestAnimationFrame(frame);
