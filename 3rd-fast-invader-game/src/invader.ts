import { GameObject } from './types.js';

export class Invader implements GameObject {
  public x: number;
  public y: number;
  public width: number = 40;
  public height: number = 30;
  public type: number;
  public points: number;
  private animationFrame: number = 0;
  private animationSpeed: number = 60;
  private animationTimer: number = 0;

  constructor(x: number, y: number, type: number = 1) {
    this.x = x;
    this.y = y;
    this.type = type;
    this.points = type * 10;
  }

  public update(deltaTime: number): void {
    this.animationTimer++;
    if (this.animationTimer >= this.animationSpeed) {
      this.animationFrame = (this.animationFrame + 1) % 2;
      this.animationTimer = 0;
    }
  }

  public render(ctx: CanvasRenderingContext2D): void {
    const colors = ['#ff0000', '#ffff00', '#ff00ff'];
    ctx.fillStyle = colors[this.type - 1] || '#ff0000';
    
    if (this.type === 1) {
      this.renderType1(ctx);
    } else if (this.type === 2) {
      this.renderType2(ctx);
    } else {
      this.renderType3(ctx);
    }
  }

  private renderType1(ctx: CanvasRenderingContext2D): void {
    // Simple square invader
    const offset = this.animationFrame * 2;
    ctx.fillRect(this.x + offset, this.y, this.width - offset * 2, this.height);
    
    // Eyes
    ctx.fillStyle = '#000';
    ctx.fillRect(this.x + 8 + offset, this.y + 8, 6, 6);
    ctx.fillRect(this.x + 26 - offset, this.y + 8, 6, 6);
  }

  private renderType2(ctx: CanvasRenderingContext2D): void {
    // Diamond-shaped invader
    const centerX = this.x + this.width / 2;
    const centerY = this.y + this.height / 2;
    
    ctx.beginPath();
    ctx.moveTo(centerX, this.y);
    ctx.lineTo(this.x + this.width, centerY);
    ctx.lineTo(centerX, this.y + this.height);
    ctx.lineTo(this.x, centerY);
    ctx.closePath();
    ctx.fill();
    
    // Inner diamond
    ctx.fillStyle = '#000';
    ctx.beginPath();
    ctx.moveTo(centerX, this.y + 8);
    ctx.lineTo(this.x + this.width - 8, centerY);
    ctx.lineTo(centerX, this.y + this.height - 8);
    ctx.lineTo(this.x + 8, centerY);
    ctx.closePath();
    ctx.fill();
  }

  private renderType3(ctx: CanvasRenderingContext2D): void {
    // Cross-shaped invader
    const armLength = 12 + this.animationFrame * 3;
    const centerX = this.x + this.width / 2;
    const centerY = this.y + this.height / 2;
    
    // Vertical bar
    ctx.fillRect(centerX - 4, this.y, 8, this.height);
    
    // Horizontal bar
    ctx.fillRect(centerX - armLength, centerY - 4, armLength * 2, 8);
    
    // Center circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, 6, 0, Math.PI * 2);
    ctx.fill();
  }
}