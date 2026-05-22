import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mario Adventure", layout="wide")

st.title("🍄 Super Mario Adventure")

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

    transition:0.05s linear;
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
    z-index:999;
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
    z-index:999;
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

    z-index:9999;
}

</style>

</head>

<body>

<div id="game">

<div id="scoreboard">
Level: 1 | Score: 0
</div>

<button id="restartBtn" onclick="restartGame()">
🔄 Restart
</button>

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

let gravity=0.8;

let jumping=false;

let score=0;

let currentLevel=0;

let gameOver=false;

const keys={
left:false,
right:false
};

let coins=[];
let enemies=[];
let platforms=[];

const levels=[

{
background:"linear-gradient(#5c94fc,#d6f0ff)",

enemySpeed:2,

platforms:[
{x:300,y:220,w:180},
{x:650,y:320,w:180}
],

coins:[
{x:340,y:280},
{x:720,y:380},
{x:1100,y:180}
]
},

{
background:"linear-gradient(#673ab7,#311b92)",

enemySpeed:4,

platforms:[
{x:250,y:220,w:140},
{x:500,y:340,w:160},
{x:850,y:250,w:180}
],

coins:[
{x:280,y:280},
{x:560,y:400},
{x:920,y:310},
{x:1250,y:220}
]
},

{
background:"linear-gradient(#ff9800,#ff5722)",

enemySpeed:6,

platforms:[
{x:250,y:240,w:140},
{x:450,y:380,w:140},
{x:700,y:280,w:140},
{x:1000,y:420,w:180}
],

coins:[
{x:280,y:300},
{x:480,y:440},
{x:740,y:340},
{x:1050,y:480},
{x:1350,y:240}
]
}

];

function clearLevel(){

coins.forEach(c=>c.el.remove());

enemies.forEach(e=>e.el.remove());

platforms.forEach(p=>p.el.remove());

coins=[];
enemies=[];
platforms=[];
}

function createPlatform(x,y,w){

const platform=document.createElement("div");

platform.classList.add("platform");

platform.style.left=x+"px";
platform.style.bottom=y+"px";

platform.style.width=w+"px";
platform.style.height="20px";

game.appendChild(platform);

platforms.push({
el:platform,
x:x,
y:y,
w:w
});
}

function createCoin(x,y){

const coin=document.createElement("div");

coin.classList.add("coin");

coin.style.left=x+"px";
coin.style.bottom=y+"px";

game.appendChild(coin);

coins.push({
el:coin,
x:x,
y:y,
collected:false
});
}

function createEnemy(x,speed){

const enemy=document.createElement("div");

enemy.classList.add("enemy");

enemy.innerHTML="👾";

enemy.style.left=x+"px";

game.appendChild(enemy);

enemies.push({
el:enemy,
x:x,
dir:-1,
speed:speed
});
}

function loadLevel(index){

clearLevel();

const level=levels[index];

game.style.background=level.background;

level.platforms.forEach(p=>{
createPlatform(p.x,p.y,p.w);
});

level.coins.forEach(c=>{
createCoin(c.x,c.y);
});

createEnemy(700,level.enemySpeed);

createEnemy(1200,level.enemySpeed);

marioX=100;
marioY=100;

velocityY=0;

updateScoreboard();

message.style.display="block";

message.innerHTML="LEVEL "+(index+1);

setTimeout(()=>{
message.style.display="none";
},1500);
}

function updateScoreboard(){

scoreboard.innerHTML=
"Level: "+(currentLevel+1)+
" | Score: "+score;
}

function updateMario(){

if(keys.left){
marioX-=7;
}

if(keys.right){
marioX+=7;
}

velocityY-=gravity;

marioY+=velocityY;

if(marioY<=100){

marioY=100;

velocityY=0;

jumping=false;
}

platforms.forEach(p=>{

if(
marioX+50>p.x &&
marioX<p.x+p.w &&
marioY>=p.y &&
marioY<=p.y+25 &&
velocityY<=0
){

marioY=p.y+20;

velocityY=0;

jumping=false;
}
});

mario.style.left=marioX+"px";
mario.style.bottom=marioY+"px";

checkCoins();

checkEnemies();

checkGoal();
}

function checkCoins(){

coins.forEach(c=>{

if(c.collected)return;

const dx=marioX-c.x;
const dy=marioY-c.y;

if(
Math.abs(dx)<40 &&
Math.abs(dy)<40
){

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

if(e.x<200 || e.x>1450){
e.dir*=-1;
}

e.el.style.left=e.x+"px";

const dx=marioX-e.x;

if(
Math.abs(dx)<45 &&
Math.abs(marioY-100)<50
){
loseGame();
}
});
}

function allCoinsCollected(){

for(let i=0;i<coins.length;i++){

if(!coins[i].collected){
return false;
}
}

return true;
}

function checkGoal(){

if(
marioX>1450 &&
allCoinsCollected()
){
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

message.innerHTML=
"🏆 YOU WON ALL LEVELS!";
}

function loseGame(){

gameOver=true;

message.style.display="block";

message.innerHTML=
"☠️ GAME OVER";
}

window.addEventListener("keydown",(e)=>{

if(e.code==="ArrowLeft"){
keys.left=true;
}

if(e.code==="ArrowRight"){
keys.right=true;
}

if(
e.code==="Space" &&
!jumping
){

velocityY=24;

jumping=true;
}
});

window.addEventListener("keyup",(e)=>{

if(e.code==="ArrowLeft"){
keys.left=false;
}

if(e.code==="ArrowRight"){
keys.right=false;
}
});

function gameLoop(){

if(!gameOver){

updateMario();

requestAnimationFrame(gameLoop);
}
}

loadLevel(currentLevel);

gameLoop();

</script>

</body>
</html>
"""

components.html(html_code,height=730)
