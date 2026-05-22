import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mario Adventure", layout="wide")

st.title("🍄 Super Mario Adventure (Fixed Platforms + 10 Levels)")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>

body{
    margin:0;
    overflow:hidden;
    font-family:Arial;
}

#game{
    position:relative;
    width:100%;
    height:720px;
    overflow:hidden;
    border:5px solid black;
    background:linear-gradient(#5c94fc,#d6f0ff);
}

#ground{
    position:absolute;
    bottom:0;
    width:100%;
    height:100px;
    background:brown;
    border-top:10px solid green;
}

#mario{
    position:absolute;
    width:70px;
    height:70px;
    left:100px;
    bottom:100px;
    font-size:60px;
    display:flex;
    align-items:center;
    justify-content:center;
}

.platform{
    position:absolute;
    background:#a0522d;
    border:4px solid #5d2f0a;
    border-radius:10px;
}

.coin{
    position:absolute;
    width:30px;
    height:30px;
    background:gold;
    border-radius:50%;
    border:3px solid yellow;
}

.enemy{
    position:absolute;
    width:60px;
    height:60px;
    font-size:50px;
    bottom:100px;
    display:flex;
    align-items:center;
    justify-content:center;
}

#goal{
    position:absolute;
    right:40px;
    bottom:100px;
    font-size:70px;
}

#scoreboard{
    position:absolute;
    top:10px;
    left:20px;
    color:white;
    font-size:28px;
    font-weight:bold;
    text-shadow:2px 2px 5px black;
}

#message{
    position:absolute;
    top:45%;
    left:50%;
    transform:translate(-50%,-50%);
    color:white;
    font-size:50px;
    font-weight:bold;
    text-align:center;
    text-shadow:3px 3px 8px black;
    display:none;
}

#restartBtn{
    position:absolute;
    top:10px;
    right:20px;
    padding:12px 20px;
    font-size:20px;
    font-weight:bold;
    border:none;
    border-radius:10px;
    background:red;
    color:white;
    cursor:pointer;
}

</style>
</head>

<body>

<div id="game">

<div id="scoreboard">Level: 1 | Score: 0</div>

<button id="restartBtn" onclick="restartGame()">🔄 Restart</button>

<div id="message"></div>
<div id="mario">🍄</div>
<div id="goal">🚩</div>
<div id="ground"></div>

</div>

<script>

const mario=document.getElementById("mario");
const game=document.getElementById("game");
const scoreboard=document.getElementById("scoreboard");
const message=document.getElementById("message");

let marioX=100;
let marioY=100;
let velocityY=0;
let gravity=0.6;
let jumping=false;

let score=0;
let currentLevel=0;
let gameOver=false;

const keys={left:false,right:false};

let coins=[], enemies=[], platforms=[];

/* ================= 10 LEVELS ================= */

const levels=[
{
bg:"linear-gradient(#5c94fc,#d6f0ff)", speed:2, enemies:2, goalX:1450,
platforms:[{x:300,y:220,w:180},{x:650,y:320,w:180}],
coins:[{x:340,y:280},{x:720,y:380},{x:1100,y:180}]
},
{
bg:"linear-gradient(#673ab7,#311b92)", speed:3, enemies:2, goalX:1550,
platforms:[{x:250,y:220,w:140},{x:500,y:340,w:160},{x:850,y:250,w:180}],
coins:[{x:280,y:280},{x:560,y:400},{x:920,y:310}]
},
{
bg:"linear-gradient(#ff9800,#ff5722)", speed:4, enemies:3, goalX:1650,
platforms:[{x:250,y:240,w:140},{x:450,y:380,w:140},{x:700,y:280,w:140}],
coins:[{x:280,y:300},{x:480,y:440},{x:740,y:340}]
},
{
bg:"linear-gradient(#1b5e20,#66bb6a)", speed:5, enemies:3, goalX:1750,
platforms:[{x:200,y:240,w:160},{x:500,y:300,w:160},{x:800,y:380,w:160}],
coins:[{x:240,y:300},{x:540,y:360},{x:840,y:440}]
},
{
bg:"linear-gradient(#000,#434343)", speed:6, enemies:3, goalX:1850,
platforms:[{x:300,y:260,w:180},{x:650,y:340,w:180},{x:1000,y:420,w:180}],
coins:[{x:340,y:320},{x:700,y:400},{x:1050,y:480}]
},
{
bg:"linear-gradient(#3f51b5,#1a237e)", speed:6, enemies:4, goalX:1950,
platforms:[{x:200,y:220,w:140},{x:500,y:320,w:140},{x:900,y:360,w:160}],
coins:[{x:240,y:280},{x:540,y:380},{x:950,y:420}]
},
{
bg:"linear-gradient(#e91e63,#880e4f)", speed:7, enemies:4, goalX:2050,
platforms:[{x:200,y:260,w:140},{x:500,y:340,w:140},{x:1100,y:380,w:160}],
coins:[{x:240,y:320},{x:540,y:400},{x:1140,y:440}]
},
{
bg:"linear-gradient(#ffeb3b,#f57f17)", speed:8, enemies:5, goalX:2200,
platforms:[{x:180,y:240,w:120},{x:420,y:320,w:120},{x:900,y:300,w:120}],
coins:[{x:220,y:300},{x:460,y:380},{x:940,y:360},{x:1180,y:440}]
},
{
bg:"linear-gradient(#263238,#000)", speed:9, enemies:6, goalX:2350,
platforms:[{x:200,y:220,w:120},{x:450,y:300,w:120},{x:950,y:260,w:120}],
coins:[{x:240,y:280},{x:490,y:360},{x:990,y:320}]
},
{
bg:"linear-gradient(#4a148c,#000)", speed:10, enemies:7, goalX:2500,
platforms:[{x:180,y:240,w:120},{x:400,y:320,w:120},{x:900,y:280,w:120}],
coins:[{x:220,y:300},{x:440,y:380},{x:880,y:340},{x:1100,y:420}]
}
];

/* ================= CORE ================= */

function clearLevel(){
coins.forEach(c=>c.el.remove());
enemies.forEach(e=>e.el.remove());
platforms.forEach(p=>p.el.remove());
coins=[]; enemies=[]; platforms=[];
}

function createPlatform(x,y,w){
const p=document.createElement("div");
p.className="platform";
p.style.left=x+"px";
p.style.bottom=y+"px";
p.style.width=w+"px";
p.style.height="20px";
game.appendChild(p);
platforms.push({el:p,x,y,w});
}

function createCoin(x,y){
const c=document.createElement("div");
c.className="coin";
c.style.left=x+"px";
c.style.bottom=y+"px";
game.appendChild(c);
coins.push({el:c,x,y,collected:false});
}

function createEnemy(x,speed){
const e=document.createElement("div");
e.className="enemy";
e.innerHTML="👾";
e.style.left=x+"px";
game.appendChild(e);
enemies.push({el:e,x,dir:-1,speed});
}

function loadLevel(i){

clearLevel();

const lvl=levels[i];
game.style.background=lvl.bg;

lvl.platforms.forEach(p=>createPlatform(p.x,p.y,p.w));
lvl.coins.forEach(c=>createCoin(c.x,c.y));

for(let j=0;j<lvl.enemies;j++){
createEnemy(700 + j*300, lvl.speed);
}

marioX=100;
marioY=100;
velocityY=0;
jumping=false;
gameOver=false;

message.style.display="block";
message.innerHTML="LEVEL "+(i+1);
setTimeout(()=>message.style.display="none",1200);

updateScoreboard();
}

function updateScoreboard(){
scoreboard.innerHTML=`Level: ${currentLevel+1} | Score: ${score}`;
}

/* ================= MOVEMENT ================= */

function updateMario(){

if(keys.left) marioX-=7;
if(keys.right) marioX+=7;

velocityY-=gravity;
marioY+=velocityY;

if(marioY<=100){
marioY=100;
velocityY=0;
jumping=false;
}

/* ===== FIXED PLATFORM COLLISION ===== */
platforms.forEach(p=>{

const marioW=60;
const marioH=70;

const onPlatform =
marioX + marioW > p.x &&
marioX < p.x + p.w &&
marioY >= p.y &&
marioY <= p.y + 25 &&
velocityY <= 0;

if(onPlatform){
marioY = p.y + 20;
velocityY = 0;
jumping = false;
}
});

mario.style.left=marioX+"px";
mario.style.bottom=marioY+"px";

checkCoins();
checkEnemies();
checkGoal();
}

/* ================= GAME LOGIC ================= */

function checkCoins(){
coins.forEach(c=>{
if(c.collected) return;
if(Math.abs(marioX-c.x)<40 && Math.abs(marioY-c.y)<40){
c.collected=true;
c.el.remove();
score+=10;
updateScoreboard();
}
});
}

function checkEnemies(){
enemies.forEach(e=>{
e.x+=e.dir*e.speed;
if(e.x<200||e.x>1600) e.dir*=-1;
e.el.style.left=e.x+"px";

if(Math.abs(marioX-e.x)<45 && Math.abs(marioY-100)<50){
loseGame();
}
});
}

function allCoins(){
return coins.every(c=>c.collected);
}

function checkGoal(){
if(marioX>levels[currentLevel].goalX && allCoins()){
nextLevel();
}
}

function nextLevel(){
currentLevel++;
if(currentLevel>=levels.length){
winGame();
return;
}
loadLevel(currentLevel);
}

function restartGame(){
location.reload();
}

function winGame(){
gameOver=true;
message.style.display="block";
message.innerHTML="🏆 YOU WIN ALL 10 LEVELS!";
}

function loseGame(){
gameOver=true;
message.style.display="block";
message.innerHTML="☠️ GAME OVER";
}

/* ================= CONTROLS ================= */

window.addEventListener("keydown",(e)=>{
if(e.code==="ArrowLeft") keys.left=true;
if(e.code==="ArrowRight") keys.right=true;

if(e.code==="Space" && !jumping){
velocityY=22;
jumping=true;
}
});

window.addEventListener("keyup",(e)=>{
if(e.code==="ArrowLeft") keys.left=false;
if(e.code==="ArrowRight") keys.right=false;
});

/* ================= LOOP ================= */

function loop(){
if(!gameOver){
updateMario();
requestAnimationFrame(loop);
}
}

loadLevel(0);
loop();

</script>

</body>
</html>
"""

components.html(html_code, height=730)
