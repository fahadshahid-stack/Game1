import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Super Mario Adventure",
    layout="wide"
)

st.title("🍄 Super Mario Adventure")
st.markdown("### Controls")
st.markdown("""
- ⬅️ Left Arrow = Move Left
- ➡️ Right Arrow = Move Right
- SPACE = Jump
""")

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
    height: 650px;
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

    background-image: url("https://upload.wikimedia.org/wikipedia/en/a/a9/MarioNSMBUDeluxe.png");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
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

    background-image: url("https://i.imgur.com/QZ6XG7D.png");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}

#scoreboard {
    position: absolute;
    top: 10px;
    left: 20px;
    z-index: 999;

    color: white;
    font-size: 28px;
    font-weight: bold;
    text-shadow: 2px 2px 4px black;
}

#message {
    position: absolute;
    top: 45%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 999;

    font-size: 50px;
    color: white;
    font-weight: bold;
    text-shadow: 4px 4px 8px black;

    display: none;
}

.platform {
    position: absolute;
    background: #a0522d;
    border: 4px solid #5d2f0a;
    border-radius: 10px;
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

    <div id="mario"></div>

    <div id="ground"></div>

</div>

<script>

const game = document.getElementById("game");
const mario = document.getElementById("mario");
const scoreboard = document.getElementById("scoreboard");
const message = document.getElementById("message");

let marioX = 100;
let marioY = 100;

let velocityY = 0;
let gravity = 0.8;

let jumping = false;

let score = 0;
let level = 0;
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
        background: "linear-gradient(#5c94fc, #d6f0ff)",
        coins: 5,
        enemies: 1,
        enemySpeed: 2,
        platforms: [
            {x: 300, y: 220, w: 150},
            {x: 650, y: 320, w: 180}
        ]
    },

    {
        background: "linear-gradient(#673ab7, #311b92)",
        coins: 8,
        enemies: 2,
        enemySpeed: 3,
        platforms: [
            {x: 250, y: 220, w: 120},
            {x: 500, y: 320, w: 160},
            {x: 900, y: 250, w: 180}
        ]
    },

    {
        background: "linear-gradient(#ff9800, #ff5722)",
        coins: 12,
        enemies: 4,
        enemySpeed: 5,
        platforms: [
            {x: 250, y: 220, w: 120},
            {x: 450, y: 350, w: 150},
            {x: 800, y: 250, w: 160},
            {x: 1150, y: 380, w: 180}
        ]
    }

];

function clearObjects() {

    coins.forEach(c => c.el.remove());
    enemies.forEach(e => e.el.remove());
    platforms.forEach(p => p.el.remove());

    coins = [];
    enemies = [];
    platforms = [];
}

function createCoin(x, y) {

    const coin = document.createElement("div");

    coin.classList.add("coin");

    coin.style.left = x + "px";
    coin.style.bottom = y + "px";

    game.appendChild(coin);

    coins.push({
        el: coin,
        x: x,
        y: y,
        collected: false
    });
}

function createEnemy(x, speed) {

    const enemy = document.createElement("div");

    enemy.classList.add("enemy");

    enemy.style.left = x + "px";

    game.appendChild(enemy);

    enemies.push({
        el: enemy,
        x: x,
        dir: -1,
        speed: speed
    });
}

function createPlatform(x, y, width) {

    const platform = document.createElement("div");

    platform.classList.add("platform");

    platform.style.left = x + "px";
    platform.style.bottom = y + "px";

    platform.style.width = width + "px";
    platform.style.height = "20px";

    game.appendChild(platform);

    platforms.push({
        el: platform,
        x: x,
        y: y,
        w: width
    });
}

function loadLevel(levelIndex) {

    clearObjects();

    const config = levels[levelIndex];

    game.style.background = config.background;

    for (let i = 0; i < config.coins; i++) {

        createCoin(
            250 + Math.random() * 1200,
            180 + Math.random() * 250
        );
    }

    for (let i = 0; i < config.enemies; i++) {

        createEnemy(
            500 + Math.random() * 900,
            config.enemySpeed
        );
    }

    config.platforms.forEach(p => {
        createPlatform(p.x, p.y, p.w);
    });

    marioX = 100;
    marioY = 100;

    updateScoreboard();
}

function updateScoreboard() {

    scoreboard.innerHTML =
        "Level: " + (level + 1) +
        " | Score: " + score;
}

function updateMario() {

    if (keys.left) {
        marioX -= 6;
    }

    if (keys.right) {
        marioX += 6;
    }

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

    mario.style.left = marioX + "px";
    mario.style.bottom = marioY + "px";

    checkCoins();
    checkEnemies();
}

function checkCoins() {

    let collected = 0;

    coins.forEach(c => {

        if (c.collected) {
            collected++;
            return;
        }

        const dx = marioX - c.x;
        const dy = marioY - c.y;

        if (
            Math.abs(dx) < 40 &&
            Math.abs(dy) < 40
        ) {

            c.collected = true;

            c.el.remove();

            score += 10;

            collected++;
        }
    });

    updateScoreboard();

    if (collected === coins.length) {

        nextLevel();
    }
}

function checkEnemies() {

    enemies.forEach(e => {

        e.x += e.dir * e.speed;

        if (
            e.x < 250 ||
            e.x > 1400
        ) {
            e.dir *= -1;
        }

        e.el.style.left = e.x + "px";

        const dx = marioX - e.x;
        const dy = marioY - 100;

        if (
            Math.abs(dx) < 45 &&
            Math.abs(dy) < 45
        ) {

            loseGame();
        }
    });
}

function nextLevel() {

    level++;

    if (level >= levels.length) {

        winGame();

        return;
    }

    message.style.display = "block";
    message.innerHTML = "LEVEL " + (level + 1);

    setTimeout(() => {

        message.style.display = "none";

        loadLevel(level);

    }, 2000);
}

function winGame() {

    gameOver = true;

    message.style.display = "block";

    message.innerHTML =
        "🏆 YOU FINISHED ALL LEVELS!";
}

function loseGame() {

    gameOver = true;

    message.style.display = "block";

    message.innerHTML =
        "☠️ GAME OVER";
}

window.addEventListener("keydown", (e) => {

    if (e.code === "ArrowLeft") {
        keys.left = true;
    }

    if (e.code === "ArrowRight") {
        keys.right = true;
    }

    if (
        e.code === "Space" &&
        !jumping
    ) {

        velocityY = 15;

        jumping = true;
    }
});

window.addEventListener("keyup", (e) => {

    if (e.code === "ArrowLeft") {
        keys.left = false;
    }

    if (e.code === "ArrowRight") {
        keys.right = false;
    }
});

function gameLoop() {

    if (!gameOver) {

        updateMario();

        requestAnimationFrame(gameLoop);
    }
}

loadLevel(level);

gameLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=700)
