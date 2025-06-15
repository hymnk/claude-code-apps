class Bullet {
    constructor(x, y, speed, type = 'player') {
        this.x = x;
        this.y = y;
        this.width = 4;
        this.height = 12;
        this.speed = speed;
        this.type = type;
    }
    
    update(deltaTime) {
        this.y += this.speed * deltaTime;
    }
    
    render(ctx) {
        if (this.type === 'player') {
            // Player bullet - bright green laser
            const gradient = ctx.createLinearGradient(this.x, this.y, this.x, this.y + this.height);
            gradient.addColorStop(0, '#00ff00');
            gradient.addColorStop(0.5, '#00ff00');
            gradient.addColorStop(1, 'transparent');
            ctx.fillStyle = gradient;
            ctx.fillRect(this.x - this.width / 2, this.y, this.width, this.height);
            
            // Glow effect
            ctx.shadowColor = '#00ff00';
            ctx.shadowBlur = 10;
            ctx.fillRect(this.x - 1, this.y, 2, this.height);
            ctx.shadowBlur = 0;
        } else {
            // Enemy bullet - red plasma
            const gradient = ctx.createLinearGradient(this.x, this.y, this.x, this.y + this.height);
            gradient.addColorStop(0, 'transparent');
            gradient.addColorStop(0.5, '#ff0000');
            gradient.addColorStop(1, '#ff0000');
            ctx.fillStyle = gradient;
            ctx.fillRect(this.x - this.width / 2, this.y, this.width, this.height);
            
            // Glow effect
            ctx.shadowColor = '#ff0000';
            ctx.shadowBlur = 8;
            ctx.fillRect(this.x - 1, this.y, 2, this.height);
            ctx.shadowBlur = 0;
        }
    }
}