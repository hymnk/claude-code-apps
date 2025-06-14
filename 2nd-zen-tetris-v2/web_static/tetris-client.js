/**
 * ZEN Tetris v2 Web Client
 * JavaScript client for browser-based gameplay with WebSocket communication.
 */

class ZenTetrisClient {
    constructor() {
        this.ws = null;
        this.connected = false;
        this.gameState = null;
        this.blockSize = 30;
        this.boardOffsetX = 0;
        this.boardOffsetY = 0;
        
        // Canvas elements
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.nextCanvas = document.getElementById('nextCanvas');
        this.nextCtx = this.nextCanvas.getContext('2d');
        
        // UI elements
        this.connectionStatus = document.getElementById('connectionStatus');
        this.scoreValue = document.getElementById('scoreValue');
        this.linesValue = document.getElementById('linesValue');
        this.levelValue = document.getElementById('levelValue');
        this.playersValue = document.getElementById('playersValue');
        this.gameOverOverlay = document.getElementById('gameOverOverlay');
        this.pauseOverlay = document.getElementById('pauseOverlay');
        
        // Input handling
        this.setupEventListeners();
        
        // Connect to server
        this.connect();
        
        // Start render loop
        this.lastRenderTime = 0;
        requestAnimationFrame((time) => this.render(time));
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        console.log('🎋 Connecting to ZEN Tetris server...');
        this.updateConnectionStatus('接続中...', false);
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('🎋 Connected to ZEN Tetris server!');
            this.connected = true;
            this.updateConnectionStatus('接続済み', true);
        };
        
        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'game_state') {
                    this.gameState = data;
                    this.updateUI();
                }
            } catch (error) {
                console.error('Message parsing error:', error);
            }
        };
        
        this.ws.onclose = () => {
            console.log('🎋 Disconnected from server');
            this.connected = false;
            this.updateConnectionStatus('切断', false);
            
            // Attempt to reconnect after 3 seconds
            setTimeout(() => {
                if (!this.connected) {
                    this.connect();
                }
            }, 3000);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus('接続エラー', false);
        };
    }
    
    updateConnectionStatus(text, connected) {
        this.connectionStatus.textContent = text;
        this.connectionStatus.className = connected ? 'status-connected' : 'status-disconnected';
    }
    
    setupEventListeners() {
        document.addEventListener('keydown', (event) => {
            if (!this.connected) return;
            
            let action = null;
            
            switch (event.code) {
                case 'ArrowLeft':
                    action = 'move_left';
                    event.preventDefault();
                    break;
                case 'ArrowRight':
                    action = 'move_right';
                    event.preventDefault();
                    break;
                case 'ArrowDown':
                    action = 'move_down';
                    event.preventDefault();
                    break;
                case 'ArrowUp':
                    action = 'rotate';
                    event.preventDefault();
                    break;
                case 'Space':
                    action = 'hard_drop';
                    event.preventDefault();
                    break;
                case 'KeyP':
                    action = 'pause';
                    event.preventDefault();
                    break;
                case 'KeyR':
                    action = 'restart';
                    event.preventDefault();
                    break;
            }
            
            if (action && this.ws.readyState === WebSocket.OPEN) {
                this.sendInput(action);
            }
        });
        
        // Prevent context menu on canvas
        this.canvas.addEventListener('contextmenu', (e) => e.preventDefault());
        this.nextCanvas.addEventListener('contextmenu', (e) => e.preventDefault());
    }
    
    sendInput(action) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'input',
                action: action
            }));
        }
    }
    
    updateUI() {
        if (!this.gameState) return;
        
        // Update score display
        this.scoreValue.textContent = this.gameState.score.toLocaleString();
        this.linesValue.textContent = this.gameState.lines;
        this.levelValue.textContent = this.gameState.level;
        
        // Update game state overlays
        if (this.gameState.game_over) {
            this.gameOverOverlay.style.display = 'flex';
        } else {
            this.gameOverOverlay.style.display = 'none';
        }
        
        if (this.gameState.paused && !this.gameState.game_over) {
            this.pauseOverlay.style.display = 'flex';
        } else {
            this.pauseOverlay.style.display = 'none';
        }
    }
    
    render(currentTime) {
        if (!this.gameState) {
            requestAnimationFrame((time) => this.render(time));
            return;
        }
        
        this.clearCanvas();
        this.drawBoard();
        this.drawCurrentPiece();
        this.drawFlashEffect();
        this.drawParticles();
        this.drawNextPiece();
        
        this.lastRenderTime = currentTime;
        requestAnimationFrame((time) => this.render(time));
    }
    
    clearCanvas() {
        // Clear main canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw background with subtle grid
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw grid lines
        this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        this.ctx.lineWidth = 1;
        
        for (let x = 0; x <= 10; x++) {
            const xPos = x * this.blockSize;
            this.ctx.beginPath();
            this.ctx.moveTo(xPos, 0);
            this.ctx.lineTo(xPos, this.canvas.height);
            this.ctx.stroke();
        }
        
        for (let y = 0; y <= 20; y++) {
            const yPos = y * this.blockSize;
            this.ctx.beginPath();
            this.ctx.moveTo(0, yPos);
            this.ctx.lineTo(this.canvas.width, yPos);
            this.ctx.stroke();
        }
        
        // Clear next piece canvas
        this.nextCtx.clearRect(0, 0, this.nextCanvas.width, this.nextCanvas.height);
    }
    
    drawBoard() {
        if (!this.gameState.board) return;
        
        for (let y = 0; y < this.gameState.board.length; y++) {
            for (let x = 0; x < this.gameState.board[y].length; x++) {
                const cell = this.gameState.board[y][x];
                if (cell.filled) {
                    this.drawBlock(x, y, cell.color, this.ctx);
                }
            }
        }
    }
    
    drawCurrentPiece() {
        if (!this.gameState.current_piece) return;
        
        for (const block of this.gameState.current_piece) {
            this.drawBlock(block.x, block.y, block.color, this.ctx);
        }
    }
    
    drawFlashEffect() {
        if (!this.gameState.flash_lines || this.gameState.flash_lines.length === 0) return;
        
        // Flash effect for clearing lines
        const flashAlpha = Math.sin(Date.now() * 0.02) * 0.5 + 0.5;
        this.ctx.fillStyle = `rgba(255, 255, 255, ${flashAlpha * 0.6})`;
        
        for (const lineY of this.gameState.flash_lines) {
            const y = lineY * this.blockSize;
            this.ctx.fillRect(0, y, this.canvas.width, this.blockSize);
        }
    }
    
    drawParticles() {
        if (!this.gameState.particles) return;
        
        for (const particle of this.gameState.particles) {
            this.drawParticle(particle);
        }
    }
    
    drawParticle(particle) {
        const ctx = this.ctx;
        const alpha = particle.alpha / 255;
        
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.translate(particle.x, particle.y);
        ctx.rotate(particle.rotation * Math.PI / 180);
        
        // Draw star shape
        const spikes = 5;
        const outerRadius = particle.size;
        const innerRadius = outerRadius * 0.4;
        
        ctx.beginPath();
        for (let i = 0; i < spikes * 2; i++) {
            const radius = i % 2 === 0 ? outerRadius : innerRadius;
            const angle = (i * Math.PI) / spikes;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;
            
            if (i === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        }
        ctx.closePath();
        
        // Fill with color
        const [r, g, b] = particle.color;
        ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${alpha})`;
        ctx.fill();
        
        // Add glow effect
        ctx.shadowColor = `rgba(${r}, ${g}, ${b}, ${alpha * 0.8})`;
        ctx.shadowBlur = particle.size * 0.5;
        ctx.fill();
        
        ctx.restore();
    }
    
    drawNextPiece() {
        if (!this.gameState.next_piece) return;
        
        this.nextCtx.clearRect(0, 0, this.nextCanvas.width, this.nextCanvas.height);
        
        // Calculate center position
        const centerX = this.nextCanvas.width / 2;
        const centerY = this.nextCanvas.height / 2;
        const blockSize = 20;
        
        // Find bounds of the piece
        let minX = Infinity, maxX = -Infinity;
        let minY = Infinity, maxY = -Infinity;
        
        for (const block of this.gameState.next_piece) {
            minX = Math.min(minX, block.x);
            maxX = Math.max(maxX, block.x);
            minY = Math.min(minY, block.y);
            maxY = Math.max(maxY, block.y);
        }
        
        const pieceWidth = (maxX - minX + 1) * blockSize;
        const pieceHeight = (maxY - minY + 1) * blockSize;
        const offsetX = centerX - pieceWidth / 2 - minX * blockSize;
        const offsetY = centerY - pieceHeight / 2 - minY * blockSize;
        
        // Draw the piece
        for (const block of this.gameState.next_piece) {
            const x = offsetX + block.x * blockSize;
            const y = offsetY + block.y * blockSize;
            this.drawNextBlock(x, y, blockSize, block.color);
        }
    }
    
    drawBlock(gridX, gridY, color, ctx) {
        const x = gridX * this.blockSize;
        const y = gridY * this.blockSize;
        const size = this.blockSize;
        
        if (!color) return;
        
        const [r, g, b] = color;
        
        // Main block fill
        ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
        ctx.fillRect(x, y, size, size);
        
        // Add 3D effect with gradients
        const gradient = ctx.createLinearGradient(x, y, x + size, y + size);
        gradient.addColorStop(0, `rgba(255, 255, 255, 0.3)`);
        gradient.addColorStop(0.5, `rgba(255, 255, 255, 0.1)`);
        gradient.addColorStop(1, `rgba(0, 0, 0, 0.3)`);
        
        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, size, size);
        
        // Border
        ctx.strokeStyle = `rgba(255, 255, 255, 0.4)`;
        ctx.lineWidth = 1;
        ctx.strokeRect(x + 0.5, y + 0.5, size - 1, size - 1);
        
        // Inner border for depth
        ctx.strokeStyle = `rgba(0, 0, 0, 0.3)`;
        ctx.strokeRect(x + 1.5, y + 1.5, size - 3, size - 3);
    }
    
    drawNextBlock(x, y, size, color) {
        if (!color) return;
        
        const [r, g, b] = color;
        
        // Main block fill
        this.nextCtx.fillStyle = `rgb(${r}, ${g}, ${b})`;
        this.nextCtx.fillRect(x, y, size, size);
        
        // Add 3D effect
        const gradient = this.nextCtx.createLinearGradient(x, y, x + size, y + size);
        gradient.addColorStop(0, `rgba(255, 255, 255, 0.3)`);
        gradient.addColorStop(1, `rgba(0, 0, 0, 0.3)`);
        
        this.nextCtx.fillStyle = gradient;
        this.nextCtx.fillRect(x, y, size, size);
        
        // Border
        this.nextCtx.strokeStyle = `rgba(255, 255, 255, 0.6)`;
        this.nextCtx.lineWidth = 1;
        this.nextCtx.strokeRect(x + 0.5, y + 0.5, size - 1, size - 1);
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('🎋 Initializing ZEN Tetris v2 Web Client...');
    window.tetrisClient = new ZenTetrisClient();
});