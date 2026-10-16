'use strict';
const terrainStone=new Image();terrainStone.src='blender/assets/rabdentse_ruins_wall_diff_1k.jpg';
function drawTerrainPlatform(s){ctx.save();ctx.beginPath();ctx.moveTo(s.x,s.y);ctx.lineTo(s.x+s.w,s.y);ctx.lineTo(s.x+s.w-8,s.y+14);ctx.lineTo(s.x+s.w-18,s.y+25);ctx.lineTo(s.x+14,s.y+29);ctx.lineTo(s.x+5,s.y+15);ctx.closePath();ctx.clip();ctx.fillStyle=realm===6?'#b6aa8e':'#344136';ctx.fillRect(s.x,s.y,s.w,32);if(terrainStone.complete&&terrainStone.naturalWidth){const pat=ctx.createPattern(terrainStone,'repeat');pat.setTransform(new DOMMatrix().scale(.22));ctx.fillStyle=pat;ctx.fillRect(s.x,s.y,s.w,32);ctx.fillStyle=realm===6?'#ecdab455':'#0b26236b';ctx.fillRect(s.x,s.y,s.w,32);}let shade=ctx.createLinearGradient(0,s.y,0,s.y+30);shade.addColorStop(0,'#0000');shade.addColorStop(1,'#061b15cc');ctx.fillStyle=shade;ctx.fillRect(s.x,s.y,s.w,32);ctx.restore();ctx.strokeStyle=places[realm].color+'80';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(s.x+3,s.y+1);ctx.lineTo(s.x+s.w-3,s.y+1);ctx.stroke();for(let j=0;j<s.w;j+=35){ctx.fillStyle=j%3?'#637050':'#9b995f';ctx.globalAlpha=.55;ctx.beginPath();ctx.ellipse(s.x+j+7,s.y+1,6,1.5,0,0,7);ctx.fill()}ctx.globalAlpha=1;}
function drawLivingBackdrop(im,w,h,vw){
 if(!im.complete||!im.naturalWidth)return;
 const s=Math.max(w/im.width,h/im.height)*1.06,iw=im.width*s,ih=im.height*s;
 const ox=(w-iw)/2-camera/Math.max(1,P.WORLD-vw)*Math.max(0,iw-w)*.5,oy=(h-ih)/2;
 ctx.drawImage(im,ox,oy,iw,ih);
 if(reduced)return;
 // Refracted water uses only a water-region sample; masonry stays rigid.
 const water=[.84,.8,.79,.76,-1,-1,-1,-1][realm];
 if(water>0){ctx.save();ctx.beginPath();ctx.rect(0,Math.max(0,oy+ih*water),w,h);ctx.clip();for(let y=water*im.height;y<im.height;y+=5){let wave=Math.sin(y*.1+time*1.3)*1.3+Math.sin(y*.04-time*.7)*1.8;ctx.drawImage(im,0,y,im.width,5,ox+wave*s,oy+y*s,iw,5*s+.5)}ctx.restore();}
 // Soft depth-banded mist drifts independently of the stone backdrop.
 for(let j=0;j<5;j++){let mx=((j*.31+time*.006*(j%2?1:-1))%1+1)%1*w,my=h*(.48+j*.075);let fog=ctx.createRadialGradient(mx,my,0,mx,my,w*.37);fog.addColorStop(0,`rgba(${realm===2?'160,177,214':'221,225,204'},${.022+resonance*.018})`);fog.addColorStop(1,'#ffffff00');ctx.fillStyle=fog;ctx.fillRect(0,my-h*.15,w,h*.3);}
 // Sun shafts open as the place answers the player's listening.
 if([0,4,7].includes(realm)){ctx.save();ctx.globalCompositeOperation='screen';for(let i=0;i<4;i++){ctx.globalAlpha=.025+resonance*.035+Math.sin(time*.3+i)*.008;ctx.fillStyle='#ffe5a4';ctx.beginPath();ctx.moveTo(w*(.62+i*.08),0);ctx.lineTo(w*(.27+i*.1),h);ctx.lineTo(w*(.34+i*.1),h);ctx.lineTo(w*(.65+i*.08),0);ctx.fill()}ctx.restore();}
 // Foreground branches use a different parallax rate and respond to flight/wind.
 ctx.save();ctx.strokeStyle=realm===6?'#8a754155':'#142d25bb';ctx.lineWidth=Math.max(1,w/700);for(let side of [0,1]){let bx=side?w+10:-10;for(let j=0;j<5;j++){let sway=Math.sin(time*.65+j)*9*(1+Math.abs(player.vx)/250);ctx.beginPath();ctx.moveTo(bx,h);ctx.quadraticCurveTo(bx+(side?-1:1)*(50+j*12),h*.87,bx+(side?-1:1)*(75+j*18)+sway,h*(.65+j*.035));ctx.stroke();for(let k=1;k<6;k++){let px=bx+(side?-1:1)*(10+j*3)*k+sway*k/6,py=h*(1-k*.042);ctx.save();ctx.translate(px,py);ctx.rotate((side?-.7:.7)+Math.sin(time*.5+j+k)*.08);ctx.fillStyle=realm===6?'#a88e4b80':'#173d32aa';ctx.beginPath();ctx.ellipse(0,0,3+w*.002,12+w*.004,0,0,7);ctx.fill();ctx.restore()}}}ctx.restore();
 // Petals, seedheads and small moths follow several depth/speed bands.
 for(let i=0;i<32;i++){let depth=.4+i%3*.35,px=(((i*173.7+time*(9+i%5)*depth-camera*.08*depth)%vw+vw)%vw)/vw*w,py=((i*91+time*(realm===2?-3:2)+Math.sin(time*.45+i)*20)%h+h)%h;ctx.save();ctx.translate(px,py);ctx.rotate(time*.3+i);ctx.fillStyle=realm===2?'#c699f5':places[realm].color;ctx.globalAlpha=.18+i%4*.07;ctx.beginPath();ctx.ellipse(0,0,(realm===4?3:1.4)*depth,3*depth,0,0,7);ctx.fill();ctx.restore();}
}
