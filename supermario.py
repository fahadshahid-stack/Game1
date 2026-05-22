import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mario Game", layout="wide")

st.title("🍄 Super Mario Adventure")

html_code = """
<!DOCTYPE html>
<html>

<head>

<style>

body {
    margin: 0;
    overflow: hidden;
    font-family: Arial;
}

#game {
    position: relative;
    width: 100%;
    height: 650px;
    overflow: hidden;

    background: linear-gradient(#5c94fc, #d6f0ff);

    border: 5px solid black;

    outline: none;
}

#ground {
    position: absolute;
    bottom: 0;

    width: 100%;
    height: 100px;

    background: brown;
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

#score {
    position: absolute;

    top: 10px;
    left: 20px;

    color: white;
    font-size: 28px;
    font-weight: bold;

    z-index: 999;
}

#message {
    position: absolute;

    top: 45%;
    left: 50%;

    transform: translate(-50%, -50%);

    font-size: 50px;
    color: white;
    font-weight: bold;

    display: none;

    z-index: 999;
}

</style>

</head>

<body>

<div id="game" tabindex="0">

    <div id="score">
        Level: 1 | Score: 0
    </div>

    <div id="message"></div>

    <div id="mario">🍄</div>

    <div id="ground"></div>

</div>

<script>

const game = document.getElementById("game");

const mario = document.getElementById("mario");

const scoreText = document.getElementById("score");

const message = document.getElementById("message");

let marioX = 100;
let marioY = 100;

let velocityY = 0;

let gravity = 0.8;

let jumping = false;

let score = 0;

let level = 1;

let gameOver = false;

let keys = {
    left: false,
    right: false
};

let coins = [];
let enemies = [];

game.focus();

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
        taken: false
    });
}

function createEnemy(x) {

    const enemy = document.createElement("div");

    enemy.classList.add("enemy");

    enemy.innerHTML = "👾";

    enemy.style.left = x + "px";

    game.appendChild(enemy);

    enemies.push({
        el: enemy,
        x: x,
        dir: -1
    });
}

for (let i = 0; i < 6; i++) {

    createCoin(
        300 + i * 180,
        200 + (i % 2) * 100
    );
}

createEnemy(700);

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

    mario.style.left = marioX + "px";
    mario.style.bottom = marioY + "px";

    checkCoins();

    checkEnemies();
}

function checkCoins() {

    let collected = 0;

    coins.forEach(c => {

        if (c.taken) {
            collected++;
            return;
        }

        let dx = marioX - c.x;
        let dy = marioY - c.y;

        if (
            Math.abs(dx) < 40 &&
            Math.abs(dy) < 40
        ) {

            c.taken = true;

            c.el.remove();

            score += 10;

            collected++;
        }
    });

    scoreText.innerHTML =
        "Level: " + level +
        " | Score: " + score;

    if (collected === coins.length) {

        winGame();
    }
}

function checkEnemies() {

    enemies.forEach(e => {

        e.x += e.dir * 3;

        if (
            e.x < 400 ||
            e.x > 1300
        ) {

            e.dir *= -1;
        }

        e.el.style.left = e.x + "px";

        let dx = marioX - e.x;

        if (Math.abs(dx) < 50) {

            loseGame();
        }
    });
}

function winGame() {

    gameOver = true;

    message.style.display = "block";

    message.innerHTML = "🏆 YOU WIN!";
}

function loseGame() {

    gameOver = true;

    message.style.display = "block";

    message.innerHTML = "☠️ GAME OVER";
}

game.addEventListener("keydown", (e) => {

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

game.addEventListener("keyup", (e) => {

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

gameLoop();

</script>

</body>

</html>
"""

components.html(html_code, height=700)
