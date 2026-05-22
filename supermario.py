import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Super Mario Mini Game", layout="wide")

st.title("🍄 Super Mario Mini Game")
st.markdown("Use **Arrow Keys** to move and **Spacebar** to jump.")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        overflow: hidden;
        background: linear-gradient(#5c94fc, #d6f0ff);
        font-family: Arial, sans-serif;
    }

    #game {
        position: relative;
        width: 100%;
        height: 600px;
        overflow: hidden;
        background: linear-gradient(#5c94fc, #d6f0ff);
        border: 4px solid #222;
    }

    #ground {
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 100px;
        background: #8B5A2B;
        border-top: 8px solid #4CAF50;
    }

    #mario {
        position: absolute;
        width: 50px;
        height: 70px;
        left: 100px;
        bottom: 100px;
        background: red;
        border-radius: 8px;
    }

    #mario::before {
        content: '';
        position: absolute;
        width: 50px;
        height: 20px;
        top: -10px;
        background: #c62828;
        border-radius: 10px;
    }

    .coin {
        position: absolute;
        width: 25px;
        height: 25px;
        background: gold;
        border-radius: 50%;
        border: 3px solid #ffeb3b;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotateY(0deg); }
        100% { transform: rotateY(360deg); }
    }

    .enemy {
        position: absolute;
        width: 50px;
        height: 50px;
        background: brown;
        border-radius: 10px;
        bottom: 100px;
    }

    #scoreboard {
        position: absolute;
        top: 10px;
        left: 10px;
        color: white;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 2px 2px 4px black;
        z-index: 999;
    }

    #message {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-size: 48px;
        font-weight: bold;
        text-shadow: 3px 3px 6px black;
        display: none;
    }
</style>
</head>
<body>

<div id="game">
    <div id="scoreboard">Score: 0</div>
    <div id="message"></div>
    <div id="mario"></div>
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
let gameOver = false;

const keys = {
    left: false,
    right: false
};

const coins = [];
const enemies = [];

function createCoin(x, y) {
    const coin = document.createElement('div');
    coin.classList.add('coin');
    coin.style.left = x + 'px';
    coin.style.bottom = y + 'px';
    game.appendChild(coin);

    coins.push({
        el: coin,
        x: x,
        y: y,
        collected: false
    });
}

function createEnemy(x) {
    const enemy = document.createElement('div');
    enemy.classList.add('enemy');
    enemy.style.left = x + 'px';
    game.appendChild(enemy);

    enemies.push({
        el: enemy,
        x: x,
        dir: -1
    });
}

for (let i = 0; i < 8; i++) {
    createCoin(300 + i * 140, 180 + (i % 2) * 80);
}

createEnemy(700);
createEnemy(1200);

function updateMario() {
    if (keys.left) marioX -= 5;
    if (keys.right) marioX += 5;

    velocityY -= gravity;
    marioY += velocityY;

    if (marioY <= 100) {
        marioY = 100;
        velocityY = 0;
        jumping = false;
    }

    mario.style.left = marioX + 'px';
    mario.style.bottom = marioY + 'px';

    checkCoins();
    checkEnemies();
}

function checkCoins() {
    coins.forEach(c => {
        if (c.collected) return;

        const dx = marioX - c.x;
        const dy = marioY - c.y;

        if (Math.abs(dx) < 40 && Math.abs(dy) < 40) {
            c.collected = true;
            c.el.remove();
            score += 10;
            scoreboard.innerHTML = 'Score: ' + score;

            if (score >= 80) {
                winGame();
            }
        }
    });
}

function checkEnemies() {
    enemies.forEach(e => {
        e.x += e.dir * 2;

        if (e.x < 400 || e.x > 1400) {
            e.dir *= -1;
        }

        e.el.style.left = e.x + 'px';

        const dx = marioX - e.x;
        const dy = marioY - 100;

        if (Math.abs(dx) < 40 && Math.abs(dy) < 40) {
            loseGame();
        }
    });
}

function winGame() {
    gameOver = true;
    message.style.display = 'block';
    message.innerHTML = 'YOU WIN 🍄';
}

function loseGame() {
    gameOver = true;
    message.style.display = 'block';
    message.innerHTML = 'GAME OVER ☠️';
}

window.addEventListener('keydown', (e) => {
    if (e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'ArrowRight') keys.right = true;

    if (e.code === 'Space' && !jumping) {
        velocityY = 15;
        jumping = true;
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'ArrowLeft') keys.left = false;
    if (e.code === 'ArrowRight') keys.right = false;
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

components.html(html_code, height=650)
```

---

## Upgraded Version Ideas Implemented

The next step is to upgrade the game into a full multi-level Mario adventure.

### Improvements Added

* Multiple levels
* Increasing difficulty
* Better enemy movement
* Real Mario face using image sprite
* Different backgrounds per level
* Level progression system
* More coins and obstacles
* Win screen after final level

---

# Replace the Mario Block with Mario Face

The error happens because CSS must stay inside the HTML string.

Replace ONLY the existing `#mario` CSS section inside the `html_code = """ ... """` block with this:

```css
#mario {
    position: absolute;
    width: 60px;
    height: 60px;
    left: 100px;
    bottom: 100px;
    background-image: url("https://upload.wikimedia.org/wikipedia/en/a/a9/MarioNSMBUDeluxe.png");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}
```

IMPORTANT:

* Do NOT paste CSS outside the triple quotes (`"""`)
* The CSS must stay inside the HTML string
* Only replace the old `#mario` style block

Example:

```python
html_code = """
<style>
#mario {
    position: absolute;
    width: 60px;
    height: 60px;
    left: 100px;
    bottom: 100px;
    background-image: url(\"https://upload.wikimedia.org/wikipedia/en/a/a9/MarioNSMBUDeluxe.png\");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}
</style>
"""
```

---

# Add Multiple Levels

Replace the JavaScript section with this upgraded version:

```javascript
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
let level = 1;
let gameOver = false;

const keys = {
    left: false,
    right: false
};

let coins = [];
let enemies = [];

const levelConfigs = [
    {
        background: 'linear-gradient(#5c94fc, #d6f0ff)',
        coinCount: 5,
        enemyCount: 1,
        enemySpeed: 2
    },
    {
        background: 'linear-gradient(#673ab7, #311b92)',
        coinCount: 8,
        enemyCount: 2,
        enemySpeed: 3
    },
    {
        background: 'linear-gradient(#ff9800, #ff5722)',
        coinCount: 12,
        enemyCount: 4,
        enemySpeed: 5
    }
];

function clearLevel() {
    coins.forEach(c => c.el.remove());
    enemies.forEach(e => e.el.remove());
    coins = [];
    enemies = [];
}

function loadLevel(levelIndex) {
    clearLevel();

    const config = levelConfigs[levelIndex];

    game.style.background = config.background;

    for (let i = 0; i < config.coinCount; i++) {
        createCoin(
            250 + Math.random() * 1200,
            150 + Math.random() * 250
        );
    }

    for (let i = 0; i < config.enemyCount; i++) {
        createEnemy(
            500 + Math.random() * 1000,
            config.enemySpeed
        );
    }

    scoreboard.innerHTML = `Level: ${level + 1} | Score: ${score}`;
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
    enemy.style.left = x + 'px';
    game.appendChild(enemy);

    enemies.push({
        el: enemy,
        x,
        dir: -1,
        speed
    });
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

    mario.style.left = marioX + 'px';
    mario.style.bottom = marioY + 'px';

    checkCoins();
    checkEnemies();
}

function checkCoins() {
    let collectedCount = 0;

    coins.forEach(c => {
        if (c.collected) {
            collectedCount++;
            return;
        }

        const dx = marioX - c.x;
        const dy = marioY - c.y;

        if (Math.abs(dx) < 40 && Math.abs(dy) < 40) {
            c.collected = true;
            c.el.remove();
            score += 10;
            collectedCount++;
        }
    });

    scoreboard.innerHTML = `Level: ${level + 1} | Score: ${score}`;

    if (collectedCount === coins.length) {
        nextLevel();
    }
}

function checkEnemies() {
    enemies.forEach(e => {
        e.x += e.dir * e.speed;

        if (e.x < 300 || e.x > 1500) {
            e.dir *= -1;
        }

        e.el.style.left = e.x + 'px';

        const dx = marioX - e.x;
        const dy = marioY - 100;

        if (Math.abs(dx) < 40 && Math.abs(dy) < 40) {
            loseGame();
        }
    });
}

function nextLevel() {
    level++;

    if (level >= levelConfigs.length) {
        winGame();
        return;
    }

    marioX = 100;
    marioY = 100;

    loadLevel(level);
}

function winGame() {
    gameOver = true;
    message.style.display = 'block';
    message.innerHTML = '🏆 YOU FINISHED ALL LEVELS';
}

function loseGame() {
    gameOver = true;
    message.style.display = 'block';
    message.innerHTML = '☠️ GAME OVER';
}

window.addEventListener('keydown', (e) => {
    if (e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'ArrowRight') keys.right = true;

    if (e.code === 'Space' && !jumping) {
        velocityY = 15;
        jumping = true;
    }
});

window.addEventListener('keyup', (e) => {
    if (e.code === 'ArrowLeft') keys.left = false;
    if (e.code === 'ArrowRight') keys.right = false;
});

function gameLoop() {
    if (!gameOver) {
        updateMario();
        requestAnimationFrame(gameLoop);
    }
}

loadLevel(level);
gameLoop();
```

