class Game {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        
        this.gameState = 'menu'; // 'menu', 'playing', 'paused', 'gameOver'
        this.score = 0;
        this.lives = 3;
        this.level = 1;
        this.lastTime = 0;
        
        this.player = null;
        this.invaders = [];
        this.playerBullets = [];
        this.invaderBullets = [];
        this.particles = [];
        
        this.keys = {};
        this.invaderDirection = 1;
        this.invaderSpeed = 1;
        this.invaderShootTimer = 0;
        this.invaderShootInterval = 120;
        
        this.bindEvents();
    }
    
    init() {
        this.player = new Player(this.width / 2, this.height - 50);
        this.createInvaders();
        this.gameState = 'playing';
        this.updateUI();
    }
    
    createInvaders() {
        this.invaders = [];
        const rows = 5;
        const cols = 10;
        const invaderWidth = 40;
        const invaderHeight = 30;
        const spacing = 10;
        
        const startX = (this.width - (cols * (invaderWidth + spacing))) / 2;
        const startY = 80;
        
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
                const x = startX + col * (invaderWidth + spacing);
                const y = startY + row * (invaderHeight + spacing);
                const type = Math.floor(row / 2) + 1;
                this.invaders.push(new Invader(x, y, type));
            }
        }
    }
    
    bindEvents() {
        document.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
            
            if (e.code === 'Space') {
                e.preventDefault();
                this.handleShoot();
            }
            
            if (e.code === 'KeyP') {
                this.togglePause();
            }
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
        
        document.getElementById('startBtn').addEventListener('click', () => {
            this.startGame();
        });
        
        document.getElementById('pauseBtn').addEventListener('click', () => {
            this.togglePause();
        });
        
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetGame();
        });
        
        document.getElementById('restartBtn').addEventListener('click', () => {
            this.restartGame();
        });
    }
    
    startGame() {
        this.init();
        this.gameLoop();
    }
    
    togglePause() {
        if (this.gameState === 'playing') {
            this.gameState = 'paused';
        } else if (this.gameState === 'paused') {
            this.gameState = 'playing';
        }
    }
    
    resetGame() {
        this.score = 0;
        this.lives = 3;
        this.level = 1;
        this.gameState = 'menu';
        this.playerBullets = [];
        this.invaderBullets = [];
        this.particles = [];
        this.updateUI();
        this.clear();
    }
    
    restartGame() {
        document.getElementById('gameOverScreen').classList.add('hidden');
        this.resetGame();
        this.startGame();
    }
    
    handleShoot() {
        if (this.gameState === 'playing' && this.player && this.player.canShoot()) {
            const bullet = this.player.shoot();
            if (bullet) {
                this.playerBullets.push(bullet);
            }
        }
    }
    
    update(deltaTime) {
        if (this.gameState !== 'playing') return;
        
        this.updatePlayer(deltaTime);
        this.updateInvaders(deltaTime);
        this.updateBullets(deltaTime);
        this.updateParticles(deltaTime);
        this.checkCollisions();
        this.checkGameState();
    }
    
    updatePlayer(deltaTime) {
        if (!this.player) return;
        
        if (this.keys['ArrowLeft'] || this.keys['KeyA']) {
            this.player.moveLeft();
        }
        if (this.keys['ArrowRight'] || this.keys['KeyD']) {
            this.player.moveRight(this.width);
        }
        
        this.player.update(deltaTime);
    }
    
    updateInvaders(deltaTime) {
        let shouldMoveDown = false;
        
        for (let invader of this.invaders) {
            invader.update(deltaTime); // Add invader animation update
            invader.x += this.invaderDirection * this.invaderSpeed;
            
            if (invader.x <= 0 || invader.x >= this.width - invader.width) {
                shouldMoveDown = true;
            }
        }
        
        if (shouldMoveDown) {
            this.invaderDirection *= -1;
            for (let invader of this.invaders) {
                invader.y += 20;
            }
        }
        
        this.invaderShootTimer++;
        if (this.invaderShootTimer >= this.invaderShootInterval) {
            this.invaderShoot();
            this.invaderShootTimer = 0;
        }
    }
    
    invaderShoot() {
        if (this.invaders.length === 0) return;
        
        const shootingInvader = this.invaders[Math.floor(Math.random() * this.invaders.length)];
        const bullet = new Bullet(
            shootingInvader.x + shootingInvader.width / 2,
            shootingInvader.y + shootingInvader.height,
            5,
            'enemy'
        );
        this.invaderBullets.push(bullet);
    }
    
    updateBullets(deltaTime) {
        this.playerBullets = this.playerBullets.filter(bullet => {
            bullet.update(deltaTime);
            return bullet.y > 0;
        });
        
        this.invaderBullets = this.invaderBullets.filter(bullet => {
            bullet.update(deltaTime);
            return bullet.y < this.height;
        });
    }
    
    updateParticles(deltaTime) {
        this.particles = this.particles.filter(particle => {
            particle.x += particle.vx * deltaTime;
            particle.y += particle.vy * deltaTime;
            particle.life -= deltaTime;
            return particle.life > 0;
        });
    }
    
    checkCollisions() {
        // Player bullets vs invaders
        for (let i = this.playerBullets.length - 1; i >= 0; i--) {
            const bullet = this.playerBullets[i];
            
            for (let j = this.invaders.length - 1; j >= 0; j--) {
                const invader = this.invaders[j];
                
                if (this.isColliding(bullet, invader)) {
                    this.createExplosion(invader.x + invader.width / 2, invader.y + invader.height / 2);
                    this.score += invader.points;
                    this.invaders.splice(j, 1);
                    this.playerBullets.splice(i, 1);
                    this.updateUI();
                    break;
                }
            }
        }
        
        // Invader bullets vs player
        for (let i = this.invaderBullets.length - 1; i >= 0; i--) {
            const bullet = this.invaderBullets[i];
            
            if (this.player && this.isColliding(bullet, this.player)) {
                this.createExplosion(this.player.x + this.player.width / 2, this.player.y + this.player.height / 2);
                this.lives--;
                this.invaderBullets.splice(i, 1);
                this.updateUI();
                
                if (this.lives <= 0) {
                    this.gameOver();
                }
                break;
            }
        }
        
        // Invaders vs player
        for (let invader of this.invaders) {
            if (this.player && this.isColliding(invader, this.player)) {
                this.gameOver();
                break;
            }
            
            if (invader.y + invader.height >= this.height - 60) {
                this.gameOver();
                break;
            }
        }
    }
    
    isColliding(obj1, obj2) {
        return obj1.x < obj2.x + obj2.width &&
               obj1.x + obj1.width > obj2.x &&
               obj1.y < obj2.y + obj2.height &&
               obj1.y + obj1.height > obj2.y;
    }
    
    createExplosion(x, y) {
        for (let i = 0; i < 8; i++) {
            const angle = (Math.PI * 2 * i) / 8;
            const speed = Math.random() * 3 + 2;
            this.particles.push({
                x: x,
                y: y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 30,
                maxLife: 30,
                color: `hsl(${Math.random() * 60 + 15}, 100%, 50%)`
            });
        }
    }
    
    checkGameState() {
        if (this.invaders.length === 0) {
            this.nextLevel();
        }
    }
    
    nextLevel() {
        this.level++;
        this.invaderSpeed += 0.5;
        this.invaderShootInterval = Math.max(60, this.invaderShootInterval - 10);
        this.createInvaders();
        this.updateUI();
    }
    
    gameOver() {
        this.gameState = 'gameOver';
        document.getElementById('finalScore').textContent = this.score;
        document.getElementById('gameOverScreen').classList.remove('hidden');
    }
    
    render() {
        this.clear();
        
        if (this.gameState === 'menu') {
            this.renderMenu();
        } else if (this.gameState === 'playing' || this.gameState === 'paused') {
            this.renderGame();
            
            if (this.gameState === 'paused') {
                this.renderPause();
            }
        }
    }
    
    clear() {
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.width, this.height);
    }
    
    renderMenu() {
        this.ctx.fillStyle = '#00ff00';
        this.ctx.font = '48px Courier New';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('FAST INVADER', this.width / 2, this.height / 2 - 50);
        
        this.ctx.font = '24px Courier New';
        this.ctx.fillText('Press Start to Begin', this.width / 2, this.height / 2 + 50);
    }
    
    renderGame() {
        if (this.player) this.player.render(this.ctx);
        
        for (let invader of this.invaders) {
            invader.render(this.ctx);
        }
        
        for (let bullet of this.playerBullets) {
            bullet.render(this.ctx);
        }
        
        for (let bullet of this.invaderBullets) {
            bullet.render(this.ctx);
        }
        
        for (let particle of this.particles) {
            this.renderParticle(particle);
        }
    }
    
    renderParticle(particle) {
        const alpha = particle.life / particle.maxLife;
        this.ctx.save();
        this.ctx.globalAlpha = alpha;
        this.ctx.fillStyle = particle.color;
        this.ctx.fillRect(particle.x - 2, particle.y - 2, 4, 4);
        this.ctx.restore();
    }
    
    renderPause() {
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.ctx.fillStyle = '#00ff00';
        this.ctx.font = '48px Courier New';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('PAUSED', this.width / 2, this.height / 2);
    }
    
    updateUI() {
        document.getElementById('score').textContent = this.score;
        document.getElementById('lives').textContent = this.lives;
        document.getElementById('level').textContent = this.level;
    }
    
    gameLoop(currentTime = 0) {
        try {
            const deltaTime = (currentTime - this.lastTime) / 16.67; // Normalize to 60fps
            this.lastTime = currentTime;
            
            this.update(deltaTime);
            this.render();
            
            if (this.gameState !== 'gameOver') {
                requestAnimationFrame((time) => this.gameLoop(time));
            }
        } catch (error) {
            console.error('Game loop error:', error);
            // Continue the game loop even if there's an error
            if (this.gameState !== 'gameOver') {
                requestAnimationFrame((time) => this.gameLoop(time));
            }
        }
    }
}