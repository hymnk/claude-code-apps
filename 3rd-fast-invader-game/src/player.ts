import { GameObject } from './types.js';
import { Bullet } from './bullet.js';

export class Player implements GameObject {
  public x: number;
  public y: number;
  public width: number = 40;
  public height: number = 30;
  public speed: number = 5;
  private lastShot: number = 0;
  private shootCooldown: number = 250; // milliseconds

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }

  public moveLeft(): void {
    if (this.x > 0) {
      this.x -= this.speed;
    }
  }

  public moveRight(canvasWidth: number): void {
    if (this.x < canvasWidth - this.width) {
      this.x += this.speed;
    }
  }

  public canShoot(): boolean {
    const now = Date.now();
    return now - this.lastShot > this.shootCooldown;
  }

  public shoot(): Bullet | null {
    if (this.canShoot()) {
      this.lastShot = Date.now();
      return new Bullet(
        this.x + this.width / 2,
        this.y,
        -7,
        'player'
      );
    }
    return null;
  }

  public update(deltaTime: number): void {
    // Player update logic if needed
  }

  public render(ctx: CanvasRenderingContext2D): void {
    // Draw player ship
    ctx.fillStyle = '#00ff00';
    
    // Ship body
    ctx.fillRect(this.x + 10, this.y + 20, 20, 10);
    
    // Ship nose
    ctx.beginPath();
    ctx.moveTo(this.x + 20, this.y);
    ctx.lineTo(this.x + 10, this.y + 20);
    ctx.lineTo(this.x + 30, this.y + 20);
    ctx.closePath();
    ctx.fill();
    
    // Ship wings
    ctx.fillRect(this.x, this.y + 15, 10, 8);
    ctx.fillRect(this.x + 30, this.y + 15, 10, 8);
    
    // Engine glow effect
    const gradient = ctx.createLinearGradient(this.x + 15, this.y + 30, this.x + 25, this.y + 35);
    gradient.addColorStop(0, '#00ff00');
    gradient.addColorStop(1, 'transparent');
    ctx.fillStyle = gradient;
    ctx.fillRect(this.x + 15, this.y + 30, 10, 5);
  }
}