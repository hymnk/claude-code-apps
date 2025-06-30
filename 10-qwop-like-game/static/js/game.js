class QWOPGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        
        this.gravity = 0.5;
        this.ground = this.height - 50;
        this.friction = 0.95;
        
        this.gameStarted = false;
        this.gameFinished = false;
        this.startTime = 0;
        this.currentTime = 0;
        
        this.keys = {
            q: false,
            w: false,
            o: false,
            p: false
        };
        
        this.initRunner();
        this.bindEvents();
        this.gameLoop();
    }
    
    initRunner() {
        this.runner = {
            body: {
                x: 100,
                y: this.ground - 80,
                vx: 0,
                vy: 0,
                width: 20,
                height: 60,
                angle: 0,
                angularVelocity: 0
            },
            
            leftThigh: {
                x: 100,
                y: this.ground - 40,
                vx: 0,
                vy: 0,
                length: 30,
                angle: -0.3,
                angularVelocity: 0,
                targetAngle: -0.3
            },
            
            rightThigh: {
                x: 100,
                y: this.ground - 40,
                vx: 0,
                vy: 0,
                length: 30,
                angle: 0.3,
                angularVelocity: 0,
                targetAngle: 0.3
            },
            
            leftCalf: {
                x: 100,
                y: this.ground - 10,
                vx: 0,
                vy: 0,
                length: 25,
                angle: 0.8,
                angularVelocity: 0,
                targetAngle: 0.8
            },
            
            rightCalf: {
                x: 100,
                y: this.ground - 10,
                vx: 0,
                vy: 0,
                length: 25,
                angle: -0.8,
                angularVelocity: 0,
                targetAngle: -0.8
            }
        };
        
        this.distance = 0;
        this.speed = 0;
    }
    
    bindEvents() {
        document.addEventListener('keydown', (e) => {
            const key = e.key.toLowerCase();
            if (key in this.keys) {
                this.keys[key] = true;
                if (!this.gameStarted) {
                    this.gameStarted = true;
                    this.startTime = Date.now();
                }
            }
        });
        
        document.addEventListener('keyup', (e) => {
            const key = e.key.toLowerCase();
            if (key in this.keys) {
                this.keys[key] = false;
            }
        });
        
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.reset();
        });
    }
    
    updatePhysics() {
        if (!this.gameStarted || this.gameFinished) return;
        
        const runner = this.runner;
        const strength = 0.15;
        const maxAngle = Math.PI / 2;
        
        if (this.keys.q) {
            runner.leftThigh.targetAngle = Math.max(runner.leftThigh.targetAngle - strength, -maxAngle);
        }
        if (this.keys.w) {
            runner.rightThigh.targetAngle = Math.min(runner.rightThigh.targetAngle + strength, maxAngle);
        }
        if (this.keys.o) {
            runner.leftCalf.targetAngle = Math.max(runner.leftCalf.targetAngle - strength, -maxAngle);
        }
        if (this.keys.p) {
            runner.rightCalf.targetAngle = Math.min(runner.rightCalf.targetAngle + strength, maxAngle);
        }
        
        const springStrength = 0.1;
        const damping = 0.9;
        
        ['leftThigh', 'rightThigh', 'leftCalf', 'rightCalf'].forEach(part => {
            const limb = runner[part];
            const angleDiff = limb.targetAngle - limb.angle;
            limb.angularVelocity += angleDiff * springStrength;
            limb.angularVelocity *= damping;
            limb.angle += limb.angularVelocity;
        });
        
        const bodyX = runner.body.x;
        const bodyY = runner.body.y;
        
        runner.leftThigh.x = bodyX - 5;
        runner.leftThigh.y = bodyY + 20;
        runner.rightThigh.x = bodyX + 5;
        runner.rightThigh.y = bodyY + 20;
        
        const leftThighEndX = runner.leftThigh.x + Math.cos(runner.leftThigh.angle) * runner.leftThigh.length;
        const leftThighEndY = runner.leftThigh.y + Math.sin(runner.leftThigh.angle) * runner.leftThigh.length;
        const rightThighEndX = runner.rightThigh.x + Math.cos(runner.rightThigh.angle) * runner.rightThigh.length;
        const rightThighEndY = runner.rightThigh.y + Math.sin(runner.rightThigh.angle) * runner.rightThigh.length;
        
        runner.leftCalf.x = leftThighEndX;
        runner.leftCalf.y = leftThighEndY;
        runner.rightCalf.x = rightThighEndX;
        runner.rightCalf.y = rightThighEndY;
        
        const leftFootX = runner.leftCalf.x + Math.cos(runner.leftCalf.angle) * runner.leftCalf.length;
        const leftFootY = runner.leftCalf.y + Math.sin(runner.leftCalf.angle) * runner.leftCalf.length;
        const rightFootX = runner.rightCalf.x + Math.cos(runner.rightCalf.angle) * runner.rightCalf.length;
        const rightFootY = runner.rightCalf.y + Math.sin(runner.rightCalf.angle) * runner.rightCalf.length;
        
        let groundForceX = 0;
        let groundForceY = 0;
        
        if (leftFootY >= this.ground - 5) {
            groundForceY += (this.ground - leftFootY) * 0.5;
            groundForceX += Math.cos(runner.leftCalf.angle) * 0.2;
        }
        
        if (rightFootY >= this.ground - 5) {
            groundForceY += (this.ground - rightFootY) * 0.5;
            groundForceX += Math.cos(runner.rightCalf.angle) * 0.2;
        }
        
        runner.body.vx += groundForceX;
        runner.body.vy += groundForceY;
        
        runner.body.vy += this.gravity;
        runner.body.vx *= this.friction;
        runner.body.vy *= 0.98;
        
        runner.body.x += runner.body.vx;
        runner.body.y += runner.body.vy;
        
        if (runner.body.y > this.ground - 80) {
            runner.body.y = this.ground - 80;
            runner.body.vy = 0;
        }
        
        const prevDistance = this.distance;
        this.distance = Math.max(0, (runner.body.x - 100) / 8);
        this.speed = (this.distance - prevDistance) * 60;
        
        if (this.distance >= 100) {
            this.gameFinished = true;
        }
    }
    
    render() {
        this.ctx.fillStyle = '#222';
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        this.ctx.strokeStyle = '#444';
        this.ctx.lineWidth = 1;
        for (let i = 0; i <= 10; i++) {
            const x = (i * 80) - (this.runner.body.x - 100) % 80;
            if (x >= 0 && x <= this.width) {
                this.ctx.beginPath();
                this.ctx.moveTo(x, this.ground);
                this.ctx.lineTo(x, this.ground + 10);
                this.ctx.stroke();
                
                if (i % 5 === 0) {
                    this.ctx.fillStyle = '#666';
                    this.ctx.font = '12px Courier New';
                    this.ctx.fillText(`${Math.floor(this.distance / 10) * 10 + i * 10}m`, x - 15, this.ground + 25);
                }
            }
        }
        
        this.ctx.strokeStyle = '#fff';
        this.ctx.beginPath();
        this.ctx.moveTo(0, this.ground);
        this.ctx.lineTo(this.width, this.ground);
        this.ctx.stroke();
        
        const runner = this.runner;
        const offsetX = this.width / 2 - runner.body.x;
        
        this.ctx.save();
        this.ctx.translate(offsetX, 0);
        
        this.ctx.strokeStyle = '#fff';
        this.ctx.lineWidth = 3;
        
        this.ctx.fillStyle = '#fff';
        this.ctx.fillRect(runner.body.x - 10, runner.body.y - 30, runner.body.width, runner.body.height);
        
        this.ctx.beginPath();
        this.ctx.arc(runner.body.x, runner.body.y - 40, 10, 0, Math.PI * 2);
        this.ctx.fill();
        
        this.drawLimb(runner.leftThigh);
        this.drawLimb(runner.rightThigh);
        this.drawLimb(runner.leftCalf);
        this.drawLimb(runner.rightCalf);
        
        this.ctx.restore();
        
        this.updateUI();
    }
    
    drawLimb(limb) {
        const endX = limb.x + Math.cos(limb.angle) * limb.length;
        const endY = limb.y + Math.sin(limb.angle) * limb.length;
        
        this.ctx.beginPath();
        this.ctx.moveTo(limb.x, limb.y);
        this.ctx.lineTo(endX, endY);
        this.ctx.stroke();
        
        this.ctx.beginPath();
        this.ctx.arc(limb.x, limb.y, 3, 0, Math.PI * 2);
        this.ctx.fill();
        
        this.ctx.beginPath();
        this.ctx.arc(endX, endY, 3, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    updateUI() {
        if (this.gameStarted && !this.gameFinished) {
            this.currentTime = (Date.now() - this.startTime) / 1000;
        }
        
        document.getElementById('distance').textContent = this.distance.toFixed(1);
        document.getElementById('time').textContent = this.currentTime.toFixed(1);
        document.getElementById('speed').textContent = this.speed.toFixed(1);
        
        if (this.gameFinished) {
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            this.ctx.fillRect(0, 0, this.width, this.height);
            
            this.ctx.fillStyle = '#fff';
            this.ctx.font = '48px Courier New';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('GOAL!', this.width / 2, this.height / 2 - 50);
            
            this.ctx.font = '24px Courier New';
            this.ctx.fillText(`Time: ${this.currentTime.toFixed(2)}s`, this.width / 2, this.height / 2);
            this.ctx.fillText('Press Reset to play again', this.width / 2, this.height / 2 + 50);
            this.ctx.textAlign = 'left';
        }
    }
    
    reset() {
        this.gameStarted = false;
        this.gameFinished = false;
        this.currentTime = 0;
        this.initRunner();
        Object.keys(this.keys).forEach(key => {
            this.keys[key] = false;
        });
    }
    
    gameLoop() {
        this.updatePhysics();
        this.render();
        requestAnimationFrame(() => this.gameLoop());
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new QWOPGame();
});