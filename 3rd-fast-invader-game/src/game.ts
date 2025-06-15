import { GameState, KeyState, Particle } from './types.js';
import { Player } from './player.js';
import { Invader } from './invader.js';
import { Bullet } from './bullet.js';

export class Game {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private width: number;
  private height: number;
  
  private gameState: GameState = 'menu';
  private score: number = 0;
  private lives: number = 3;
  private level: number = 1;
  private lastTime: number = 0;
  
  private player: Player | null = null;
  private invaders: Invader[] = [];
  private playerBullets: Bullet[] = [];
  private invaderBullets: Bullet[] = [];
  private particles: Particle[] = [];
  
  private keys: KeyState = {};
  private invaderDirection: number = 1;
  private invaderSpeed: number = 1;
  private invaderShootTimer: number = 0;
  private invaderShootInterval: number = 120;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    const context = canvas.getContext('2d');
    if (!context) {
      throw new Error('Could not get 2D context from canvas');
    }
    this.ctx = context;
    this.width = canvas.width;
    this.height = canvas.height;
    
    this.bindEvents();
  }

  private init(): void {
    this.player = new Player(this.width / 2, this.height - 50);
    this.createInvaders();
    this.gameState = 'playing';
    this.updateUI();
  }

  private createInvaders(): void {
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

  private bindEvents(): void {
    document.addEventListener('keydown', (e: KeyboardEvent) => {
      this.keys[e.code] = true;
      
      if (e.code === 'Space') {
        e.preventDefault();
        this.handleShoot();
      }
      
      if (e.code === 'KeyP') {
        this.togglePause();
      }
    });
    
    document.addEventListener('keyup', (e: KeyboardEvent) => {
      this.keys[e.code] = false;
    });
    
    const startBtn = document.getElementById('startBtn');
    const pauseBtn = document.getElementById('pauseBtn');
    const resetBtn = document.getElementById('resetBtn');
    const restartBtn = document.getElementById('restartBtn');
    
    if (startBtn) {
      startBtn.addEventListener('click', () => {
        this.startGame();
      });
    }
    
    if (pauseBtn) {
      pauseBtn.addEventListener('click', () => {
        this.togglePause();
      });
    }
    
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        this.resetGame();
      });
    }
    
    if (restartBtn) {
      restartBtn.addEventListener('click', () => {
        this.restartGame();
      });
    }
  }

  public startGame(): void {
    this.init();
    this.gameLoop();
  }

  private togglePause(): void {
    if (this.gameState === 'playing') {
      this.gameState = 'paused';
    } else if (this.gameState === 'paused') {
      this.gameState = 'playing';
    }
  }

  private resetGame(): void {
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

  private restartGame(): void {
    const gameOverScreen = document.getElementById('gameOverScreen');
    if (gameOverScreen) {
      gameOverScreen.classList.add('hidden');
    }
    this.resetGame();
    this.startGame();
  }

  private handleShoot(): void {
    if (this.gameState === 'playing' && this.player && this.player.canShoot()) {
      const bullet = this.player.shoot();
      if (bullet) {
        this.playerBullets.push(bullet);
      }
    }
  }

  private update(deltaTime: number): void {
    if (this.gameState !== 'playing') return;
    
    this.updatePlayer(deltaTime);
    this.updateInvaders(deltaTime);
    this.updateBullets(deltaTime);
    this.updateParticles(deltaTime);
    this.checkCollisions();
    this.checkGameState();
  }

  private updatePlayer(deltaTime: number): void {
    if (!this.player) return;
    
    if (this.keys['ArrowLeft'] || this.keys['KeyA']) {
      this.player.moveLeft();
    }
    if (this.keys['ArrowRight'] || this.keys['KeyD']) {
      this.player.moveRight(this.width);
    }
    
    this.player.update(deltaTime);
  }

  private updateInvaders(deltaTime: number): void {
    let shouldMoveDown = false;
    
    for (const invader of this.invaders) {
      invader.update(deltaTime);
      invader.x += this.invaderDirection * this.invaderSpeed;
      
      if (invader.x <= 0 || invader.x >= this.width - invader.width) {
        shouldMoveDown = true;
      }
    }
    
    if (shouldMoveDown) {
      this.invaderDirection *= -1;
      for (const invader of this.invaders) {
        invader.y += 20;
      }
    }
    
    this.invaderShootTimer++;
    if (this.invaderShootTimer >= this.invaderShootInterval) {
      this.invaderShoot();
      this.invaderShootTimer = 0;
    }
  }

  private invaderShoot(): void {
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

  private updateBullets(deltaTime: number): void {
    this.playerBullets = this.playerBullets.filter(bullet => {
      bullet.update(deltaTime);
      return bullet.y > 0;
    });
    
    this.invaderBullets = this.invaderBullets.filter(bullet => {
      bullet.update(deltaTime);
      return bullet.y < this.height;
    });
  }

  private updateParticles(deltaTime: number): void {
    this.particles = this.particles.filter(particle => {
      particle.x += particle.vx * deltaTime;
      particle.y += particle.vy * deltaTime;
      particle.life -= deltaTime;
      return particle.life > 0;
    });
  }

  private checkCollisions(): void {
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
    for (const invader of this.invaders) {
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

  public isColliding(obj1: { x: number; y: number; width: number; height: number }, 
                     obj2: { x: number; y: number; width: number; height: number }): boolean {
    return obj1.x < obj2.x + obj2.width &&
           obj1.x + obj1.width > obj2.x &&
           obj1.y < obj2.y + obj2.height &&
           obj1.y + obj1.height > obj2.y;
  }

  private createExplosion(x: number, y: number): void {
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

  private checkGameState(): void {
    if (this.invaders.length === 0) {
      this.nextLevel();
    }
  }

  private nextLevel(): void {
    this.level++;
    this.invaderSpeed += 0.5;
    this.invaderShootInterval = Math.max(60, this.invaderShootInterval - 10);
    this.createInvaders();
    this.updateUI();
  }

  private gameOver(): void {
    this.gameState = 'gameOver';
    const finalScore = document.getElementById('finalScore');
    const gameOverScreen = document.getElementById('gameOverScreen');
    
    if (finalScore) {
      finalScore.textContent = this.score.toString();
    }
    if (gameOverScreen) {
      gameOverScreen.classList.remove('hidden');
    }
  }

  public render(): void {
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

  private clear(): void {
    this.ctx.fillStyle = '#000';
    this.ctx.fillRect(0, 0, this.width, this.height);
  }

  private renderMenu(): void {
    this.ctx.fillStyle = '#00ff00';
    this.ctx.font = '48px Courier New';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('FAST INVADER', this.width / 2, this.height / 2 - 50);
    
    this.ctx.font = '24px Courier New';
    this.ctx.fillText('Press Start to Begin', this.width / 2, this.height / 2 + 50);
  }

  private renderGame(): void {
    if (this.player) this.player.render(this.ctx);
    
    for (const invader of this.invaders) {
      invader.render(this.ctx);
    }
    
    for (const bullet of this.playerBullets) {
      bullet.render(this.ctx);
    }
    
    for (const bullet of this.invaderBullets) {
      bullet.render(this.ctx);
    }
    
    for (const particle of this.particles) {
      this.renderParticle(particle);
    }
  }

  private renderParticle(particle: Particle): void {
    const alpha = particle.life / particle.maxLife;
    this.ctx.save();
    this.ctx.globalAlpha = alpha;
    this.ctx.fillStyle = particle.color;
    this.ctx.fillRect(particle.x - 2, particle.y - 2, 4, 4);
    this.ctx.restore();
  }

  private renderPause(): void {
    this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    this.ctx.fillRect(0, 0, this.width, this.height);
    
    this.ctx.fillStyle = '#00ff00';
    this.ctx.font = '48px Courier New';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('PAUSED', this.width / 2, this.height / 2);
  }

  private updateUI(): void {
    const scoreElement = document.getElementById('score');
    const livesElement = document.getElementById('lives');
    const levelElement = document.getElementById('level');
    
    if (scoreElement) scoreElement.textContent = this.score.toString();
    if (livesElement) livesElement.textContent = this.lives.toString();
    if (levelElement) levelElement.textContent = this.level.toString();
  }

  public gameLoop(currentTime: number = 0): void {
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