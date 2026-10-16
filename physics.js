(function(root){
 const WORLD=3200;
 function platforms(i){
  const offset=[0,28,-18,10,-30,0,20,-12][i];
  return [{x:0,y:690,w:720},{x:830,y:665+offset,w:530},{x:1480,y:690,w:620},{x:2240,y:660,w:960},{x:490,y:570,w:165},{x:1110,y:510,w:180},{x:1790,y:535,w:190},{x:2460,y:505,w:190}];
 }
 function spawn(){return {x:100,y:660,vx:0,vy:0,jumps:0,ground:false,coyote:0,buffer:0};}
 function step(p,input,dt,terrain){
  p.coyote=p.ground?.13:Math.max(0,p.coyote-dt);p.buffer=Math.max(0,p.buffer-dt);
  if(input.jump)p.buffer=.14;
  const target=input.move*250;p.vx+=(target-p.vx)*Math.min(1,dt*(input.move?8:11));
  if(p.buffer>0&&(p.coyote>0||p.jumps<2)){p.vy=-470;p.jumps=p.coyote>0?1:p.jumps+1;p.buffer=0;p.coyote=0;p.ground=false;}
  p.vy+=input.fly?-1100*dt:1150*dt;
  p.vy=Math.max(input.fly?-175:-700,Math.min(p.vy,input.fly?90:650));
  const old=p.y;p.x=Math.max(18,Math.min(WORLD-18,p.x+p.vx*dt));p.y=Math.max(50,p.y+p.vy*dt);p.ground=false;
  for(const s of terrain)if(p.vy>=0&&old<=s.y&&p.y>=s.y&&p.x+12>s.x&&p.x-12<s.x+s.w){p.y=s.y;p.vy=0;p.ground=true;p.jumps=0;break;}
  if(p.y>980){Object.assign(p,spawn());return 'respawn';}
  return p.x>WORLD-70?'exit':null;
 }
 const api={WORLD,platforms,spawn,step};if(typeof module!=='undefined')module.exports=api;else root.WorldPhysics=api;
})(typeof window!=='undefined'?window:globalThis);
