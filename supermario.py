import streamlit as st
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
