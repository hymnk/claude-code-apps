class Player {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.width = 40;
        this.height = 30;
        this.speed = 5;
        this.lastShot = 0;
        this.shootCooldown = 250; // milliseconds
    }
    
    moveLeft() {
        if (this.x > 0) {
            this.x -= this.speed;
        }
    }
    
    moveRight(canvasWidth) {
        if (this.x < canvasWidth - this.width) {
            this.x += this.speed;
        }
    }
    
    canShoot() {
        const now = Date.now();
        return now - this.lastShot > this.shootCooldown;
    }
    
    shoot() {
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
    
    update(deltaTime) {
        // Player update logic if needed
    }
    
    render(ctx) {
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