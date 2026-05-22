import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario Adventure", layout="wide")

st.title("🍄 Super Mario Adventure")
st.markdown("Use ⬅️ ➡️ to move and SPACE to jump")

html_code = """
<!DOCTYPE html>
<html>

<head>

<style>

body {
    margin: 0;
    overflow: hidden;
    font-family: Arial, sans-serif;
}

#game {
    position: relative;
    width: 100%;
    height: 700px;
    overflow: hidden;
    border: 5px solid black;
    background: linear-gradient(#5c94fc, #d6f0ff);
}

#ground {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 100px;
    background: #8B5A2B;
    border-top: 10px solid green;
}

#mario {
    position: absolute;

    width: 70px;
    height: 70px;

    left: 100px;
    bottom: 100px;

    font-size: 60px;

    display: flex;
    align-items: center;
    justify-content: center;
}

.coin {
    position: absolute;

    width: 30px;
    height: 30px;

    border-radius: 50%;

    background: gold;
    border: 3px solid yellow;

    animation: spin 1s linear infinite;
}

.enemy {
    position: absolute;

    width: 60px;
    height: 60px;

    bottom: 100px;

    font-size: 50px;

    display: flex;
    align-items: center;
    justify-content: center;
}

.platform {
    position: absolute;

    background: #a0522d;

    border: 4px solid #5d2f0a;

    border-radius: 10px;
}

#scoreboard {
    position: absolute;

    top: 10px;
    left: 20px;

    color: white;
    font-size: 28px;
    font-weight: bold;

    text-shadow: 2px 2px 5px black;

    z-index: 999;
}

#message {
    position: absolute;

    top: 45%;
    left: 50%;

    transform: translate(-50%, -50%);

    color: white;
    font-size: 50px;
    font-weight: bold;

    text-align: center;

    text-shadow: 3px 3px 8px black;

    z-index: 999;

    display: none;
}

#goal {
    position: absolute;

    right: 60px;
    bottom: 100px;

    font-size: 70px;
}

@keyframes spin {
    from {
        transform: rotateY(0deg);
    }

    to {
        transform: rotateY(360deg);
    }
}

</style>

</head>

<body>

<div id="game">

    <div id="scoreboard">
        Level: 1 | Score: 0
    </div>

    <div id="message"></div>

    <div id="mario">🍄</div>

    <div id="goal">🚩</div>

    <div id="ground"></div>

</div>

<script>

const mario = document.getElementById('mario');
const game = document.getElementById('game');
const scoreboard = document.getElementById('scoreboard');
const message = document.getElementById('message');

let marioX = 100;
let marioY = 100;

let velocityY = 0;

let gravity = 0.8;

let jumping = false;

let score = 0;

let currentLevel = 0;

let gameOver = false;

const keys = {
    left: false,
    right: false
};

let coins = [];
let enemies = [];
let platforms = [];

const levels = [

    {
        background: 'linear-gradient(#5c94fc, #d6f0ff)',

        enemySpeed: 2,

        platforms: [
            {x: 300, y: 220, w: 180},
            {x: 650, y: 320, w: 180}
        ],

        coins: [
            {x: 340, y: 280},
            {x: 720, y: 380},
            {x: 950, y: 180}
        ]
    },

    {
        background: 'linear-gradient(#673ab7, #311b92)',

        enemySpeed: 4,

        platforms: [
            {x: 250, y: 220, w: 140},
            {x: 500, y: 340, w: 160},
            {x: 850, y: 250, w: 180}
        ],

        coins: [
            {x: 280, y: 280},
            {x: 560, y: 400},
            {x: 920, y: 310},
            {x: 1200, y: 180}
        ]
    },

    {
        background: 'linear-gradient(#ff9800, #ff5722)',

        enemySpeed: 6,

        platforms: [
            {x: 250, y: 240, w: 140},
            {x: 450, y: 380, w: 140},
            {x: 700, y: 280, w: 140},
            {x: 1000, y: 420, w: 180}
        ],

        coins: [
            {x: 280, y: 300},
            {x: 480, y: 440},
            {x: 740, y: 340},
            {x: 1050, y: 480},
            {x: 1350, y: 200}
        ]
    }

];

function clearLevel() {

    coins.forEach(c => c.el.remove());

    enemies.forEach(e => e.el.remove());

    platforms.forEach(p => p.el.remove());

    coins = [];

    enemies = [];

    platforms = [];
}

function createPlatform(x, y, width) {

    const platform = document.createElement('div');

    platform.classList.add('platform');

    platform.style.left = x + 'px';

    platform.style.bottom = y + 'px';

    platform.style.width = width + 'px';

    platform.style.height = '20px';

    game.appendChild(platform);

    platforms.push({
        el: platform,
        x,
        y,
        w: width
    });
}

function createCoin(x, y) {

    const coin = document.createElement('div');

    coin.classList.add('coin');

    coin.style.left = x + 'px';

    coin.style.bottom = y + 'px';

    game.appendChild(coin);

    coins.push({
        el: coin,
        x,
        y,
        collected: false
    });
}

function createEnemy(x, speed) {

    const enemy = document.createElement('div');

    enemy.classList.add('enemy');

    enemy.innerHTML = '👾';

    enemy.style.left = x + 'px';

    game.appendChild(enemy);

    enemies.push({
        el: enemy,
        x,
        dir: -1,
        speed
    });
}

function loadLevel(index) {

    clearLevel();

    const level = levels[index];

    game.style.background = level.background;

    level.platforms.forEach(p => {
        createPlatform(p.x, p.y, p.w);
    });

    level.coins.forEach(c => {
        createCoin(c.x, c.y);
    });

    createEnemy(800, level.enemySpeed);

    createEnemy(1200, level.enemySpeed);

    marioX = 100;

    marioY = 100;

    updateScoreboard();
}

function updateScoreboard() {

    scoreboard.innerHTML =
        'Level: ' + (currentLevel + 1) +
        ' | Score: ' + score;
}

function updateMario() {

    if (keys.left) marioX -= 6;

    if (keys.right) marioX += 6;

    velocityY -= gravity;

    marioY += velocityY;

    if (marioY <= 100) {

        marioY = 100;

        velocityY = 0;

        jumping = false;
    }

    platforms.forEach(p => {

        if (
            marioX + 50 > p.x &&
            marioX < p.x + p.w &&
            marioY >= p.y &&
            marioY <= p.y + 25 &&
            velocityY <= 0
        ) {

            marioY = p.y + 20;

            velocityY = 0;

            jumping = false;
        }
    });

    mario.style.left = marioX + 'px';

    mario.style.bottom = marioY + 'px';

    checkCoins();

    checkEnemies();

    checkGoal();
}

function checkCoins() {

    coins.forEach(c => {

        if (c.collected) return;

        const dx = marioX - c.x;

        const dy = marioY - c.y;

        if (
            Math.abs(dx) < 40 &&
            Math.abs(dy) < 40
        ) {

            c.collected = true;

            c.el.remove();

            score += 10;

            updateScoreboard();
        }
    });
}

function checkEnemies() {

    enemies.forEach(e => {

        e.x += e.dir * e.speed;

        if (
            e.x < 200 ||
            e.x > 1450
        ) {

            e.dir *= -1;
        }

        e.el.style.left = e.x + 'px';

        const dx = marioX - e.x;

        if (
            Math.abs(dx) < 45 &&
            Math.abs(marioY - 100) < 50
        ) {

            loseGame();
        }
    });
}

function checkGoal() {

    if (marioX > 1450) {

        nextLevel();
    }
}

function nextLevel() {

    currentLevel++;

    if (currentLevel >= levels.length) {

        winGame();

        return;
    }

    message.style.display = 'block';

    message.innerHTML =
        'LEVEL ' + (currentLevel + 1);

    setTimeout(() => {

        message.style.display = 'none';

        loadLevel(currentLevel);

    }, 1500);
}

function restartGame() {

    location.reload();
}

function winGame() {

    gameOver = true;

    message.style.display = 'block';

    message.innerHTML = `
        🏆 YOU WON THE GAME
        <br><br>

        <button onclick="restartGame()"
        style="
            padding:15px 30px;
            font-size:24px;
            border:none;
            border-radius:10px;
            background:gold;
            cursor:pointer;
            font-weight:bold;
        ">
            🔄 Restart Game
        </button>
    `;
}

function loseGame() {

    gameOver = true;

    message.style.display = 'block';

    message.innerHTML = `
        ☠️ GAME OVER
        <br><br>

        <button onclick="restartGame()"
        style="
            padding:15px 30px;
            font-size:24px;
            border:none;
            border-radius:10px;
            background:red;
            color:white;
            cursor:pointer;
            font-weight:bold;
        ">
            🔄 Restart Game
        </button>
    `;
}

window.addEventListener('keydown', (e) => {

    if (e.code === 'ArrowLeft') {
        keys.left = true;
    }

    if (e.code === 'ArrowRight') {
        keys.right = true;
    }

    if (
        e.code === 'Space' &&
        !jumping
    ) {

        velocityY = 24;

        jumping = true;
    }
});

window.addEventListener('keyup', (e) => {

    if (e.code === 'ArrowLeft') {
        keys.left = false;
    }

    if (e.code === 'ArrowRight') {
        keys.right = false;
    }
});

function gameLoop() {

    if (!gameOver) {

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

components.html(html_code, height=720)
