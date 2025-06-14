// パーティクルシステム
class Particle {
    constructor(x, y, color) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 8;
        this.vy = Math.random() * -8 - 2;
        this.gravity = 0.3;
        this.life = 60;
        this.maxLife = 60;
        this.color = color;
        this.size = Math.random() * 4 + 2;
        this.rotation = Math.random() * Math.PI * 2;
        this.rotationSpeed = (Math.random() - 0.5) * 0.2;
    }
    
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += this.gravity;
        this.rotation += this.rotationSpeed;
        this.life--;
        this.size *= 0.98;
    }
    
    draw(ctx) {
        const alpha = this.life / this.maxLife;
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        
        // 星形パーティクル
        ctx.fillStyle = this.color;
        ctx.beginPath();
        for (let i = 0; i < 5; i++) {
            const angle = (i * 2 * Math.PI) / 5;
            const x = Math.cos(angle) * this.size;
            const y = Math.sin(angle) * this.size;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
            
            const innerAngle = ((i + 0.5) * 2 * Math.PI) / 5;
            const innerX = Math.cos(innerAngle) * this.size * 0.4;
            const innerY = Math.sin(innerAngle) * this.size * 0.4;
            ctx.lineTo(innerX, innerY);
        }
        ctx.closePath();
        ctx.fill();
        
        // 光るエフェクト
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;
        ctx.fill();
        
        ctx.restore();
    }
    
    isDead() {
        return this.life <= 0;
    }
}

class ParticleSystem {
    constructor() {
        this.particles = [];
    }
    
    addExplosion(x, y, color, count = 15) {
        for (let i = 0; i < count; i++) {
            this.particles.push(new Particle(x, y, color));
        }
    }
    
    update() {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            this.particles[i].update();
            if (this.particles[i].isDead()) {
                this.particles.splice(i, 1);
            }
        }
    }
    
    draw(ctx) {
        this.particles.forEach(particle => particle.draw(ctx));
    }
}

// テトリスゲームの実装
class TetrisGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.nextCanvas = document.getElementById('nextCanvas');
        this.nextCtx = this.nextCanvas.getContext('2d');
        
        // ゲーム設定
        this.BOARD_WIDTH = 10;
        this.BOARD_HEIGHT = 20;
        this.BLOCK_SIZE = 30;
        
        // ゲーム状態
        this.board = [];
        this.currentPiece = null;
        this.nextPiece = null;
        this.score = 0;
        this.lines = 0;
        this.level = 1;
        this.gameOver = false;
        this.paused = false;
        this.dropTimer = 0;
        this.dropInterval = 1000; // 1秒
        
        // エフェクト関連
        this.particleSystem = new ParticleSystem();
        this.lineFlashTimer = 0;
        this.flashingLines = [];
        this.comboCount = 0;
        
        // テトリミノの定義（アースカラー基調）
        this.tetrominoes = {
            I: {
                shape: [
                    [1, 1, 1, 1]
                ],
                color: '#8B7355' // ウォームブラウン
            },
            O: {
                shape: [
                    [1, 1],
                    [1, 1]
                ],
                color: '#D2B48C' // タン
            },
            T: {
                shape: [
                    [0, 1, 0],
                    [1, 1, 1]
                ],
                color: '#6B5B73' // ダスティパープル
            },
            S: {
                shape: [
                    [0, 1, 1],
                    [1, 1, 0]
                ],
                color: '#9CAF88' // セージグリーン
            },
            Z: {
                shape: [
                    [1, 1, 0],
                    [0, 1, 1]
                ],
                color: '#A0845C' // モカ
            },
            J: {
                shape: [
                    [1, 0, 0],
                    [1, 1, 1]
                ],
                color: '#7D8471' // オリーブグレー
            },
            L: {
                shape: [
                    [0, 0, 1],
                    [1, 1, 1]
                ],
                color: '#B8926A' // ハニーブラウン
            }
        };
        
        this.init();
    }
    
    init() {
        // ボードの初期化
        this.board = Array(this.BOARD_HEIGHT).fill().map(() => Array(this.BOARD_WIDTH).fill(0));
        
        // 最初のピースを生成
        this.nextPiece = this.getRandomPiece();
        this.spawnNewPiece();
        
        // イベントリスナーの設定
        this.setupEventListeners();
        
        // ゲームループ開始
        this.gameLoop();
    }
    
    setupEventListeners() {
        document.addEventListener('keydown', (e) => {
            if (this.gameOver || this.paused) return;
            
            switch(e.code) {
                case 'ArrowLeft':
                    e.preventDefault();
                    this.movePiece(-1, 0);
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    this.movePiece(1, 0);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.movePiece(0, 1);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.rotatePiece();
                    break;
                case 'Space':
                    e.preventDefault();
                    this.hardDrop();
                    break;
            }
        });
        
        // ボタンイベント
        document.getElementById('pauseBtn').addEventListener('click', () => {
            this.togglePause();
        });
        
        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetGame();
        });
        
        document.getElementById('restartBtn').addEventListener('click', () => {
            this.resetGame();
        });
    }
    
    getRandomPiece() {
        const pieces = Object.keys(this.tetrominoes);
        const randomPiece = pieces[Math.floor(Math.random() * pieces.length)];
        return {
            type: randomPiece,
            shape: this.tetrominoes[randomPiece].shape,
            color: this.tetrominoes[randomPiece].color,
            x: Math.floor(this.BOARD_WIDTH / 2) - Math.floor(this.tetrominoes[randomPiece].shape[0].length / 2),
            y: 0
        };
    }
    
    spawnNewPiece() {
        this.currentPiece = this.nextPiece;
        this.nextPiece = this.getRandomPiece();
        
        // ゲームオーバーチェック
        if (this.isCollision(this.currentPiece, 0, 0)) {
            this.gameOver = true;
            this.showGameOver();
        }
    }
    
    movePiece(dx, dy) {
        if (this.isCollision(this.currentPiece, dx, dy)) {
            if (dy > 0) {
                // 下に移動できない場合、ピースを固定
                this.placePiece();
                this.clearLines();
                this.spawnNewPiece();
                this.comboCount = 0; // コンボリセット
            }
            return false;
        }
        
        this.currentPiece.x += dx;
        this.currentPiece.y += dy;
        return true;
    }
    
    rotatePiece() {
        const rotated = this.rotateMatrix(this.currentPiece.shape);
        const originalShape = this.currentPiece.shape;
        this.currentPiece.shape = rotated;
        
        if (this.isCollision(this.currentPiece, 0, 0)) {
            // 回転できない場合は元に戻す
            this.currentPiece.shape = originalShape;
        }
    }
    
    rotateMatrix(matrix) {
        const N = matrix.length;
        const M = matrix[0].length;
        const rotated = Array(M).fill().map(() => Array(N).fill(0));
        
        for (let i = 0; i < N; i++) {
            for (let j = 0; j < M; j++) {
                rotated[j][N - 1 - i] = matrix[i][j];
            }
        }
        
        return rotated;
    }
    
    hardDrop() {
        while (this.movePiece(0, 1)) {
            // 何もしない、移動できる限り下に移動
        }
    }
    
    isCollision(piece, dx, dy) {
        const newX = piece.x + dx;
        const newY = piece.y + dy;
        
        for (let y = 0; y < piece.shape.length; y++) {
            for (let x = 0; x < piece.shape[y].length; x++) {
                if (piece.shape[y][x]) {
                    const boardX = newX + x;
                    const boardY = newY + y;
                    
                    // 境界チェック
                    if (boardX < 0 || boardX >= this.BOARD_WIDTH || 
                        boardY >= this.BOARD_HEIGHT) {
                        return true;
                    }
                    
                    // ボード上のブロックとの衝突チェック
                    if (boardY >= 0 && this.board[boardY][boardX]) {
                        return true;
                    }
                }
            }
        }
        
        return false;
    }
    
    placePiece() {
        for (let y = 0; y < this.currentPiece.shape.length; y++) {
            for (let x = 0; x < this.currentPiece.shape[y].length; x++) {
                if (this.currentPiece.shape[y][x]) {
                    const boardX = this.currentPiece.x + x;
                    const boardY = this.currentPiece.y + y;
                    
                    if (boardY >= 0) {
                        this.board[boardY][boardX] = this.currentPiece.color;
                    }
                }
            }
        }
    }
    
    clearLines() {
        let linesToClear = [];
        
        // 消去する行を特定
        for (let y = this.BOARD_HEIGHT - 1; y >= 0; y--) {
            if (this.board[y].every(cell => cell !== 0)) {
                linesToClear.push(y);
            }
        }
        
        if (linesToClear.length > 0) {
            // フラッシュエフェクトの開始
            this.flashingLines = linesToClear;
            this.lineFlashTimer = 30; // 30フレーム点滅
            this.comboCount++;
            
            // パーティクルエフェクト
            linesToClear.forEach(lineY => {
                for (let x = 0; x < this.BOARD_WIDTH; x++) {
                    const pixelX = x * this.BLOCK_SIZE + this.BLOCK_SIZE / 2;
                    const pixelY = lineY * this.BLOCK_SIZE + this.BLOCK_SIZE / 2;
                    const color = this.board[lineY][x];
                    
                    // 各ブロックから複数のパーティクルを発生
                    this.particleSystem.addExplosion(pixelX, pixelY, color, 8);
                    
                    // 追加の光るパーティクル（アースカラー）
                    this.particleSystem.addExplosion(pixelX, pixelY, '#F5F5DC', 5);
                    this.particleSystem.addExplosion(pixelX, pixelY, '#D4AF37', 3);
                }
            });
            
            // ライン数に応じて追加エフェクト
            if (linesToClear.length >= 4) {
                // テトリス達成時の特別エフェクト
                for (let i = 0; i < 80; i++) {
                    const x = Math.random() * this.canvas.width;
                    const y = Math.random() * this.canvas.height;
                    // ゴールドとアースカラーのパーティクル
                    const colors = ['#D4AF37', '#DAA520', '#B8860B', '#8B7355', '#D2B48C'];
                    const color = colors[Math.floor(Math.random() * colors.length)];
                    this.particleSystem.addExplosion(x, y, color, 1);
                }
                
                // 画面フラッシュエフェクト
                this.createScreenFlash();
            } else if (linesToClear.length >= 2) {
                // 複数ライン消去時のエフェクト
                for (let i = 0; i < 30; i++) {
                    const x = Math.random() * this.canvas.width;
                    const y = Math.random() * this.canvas.height;
                    this.particleSystem.addExplosion(x, y, '#9CAF88', 1);
                }
            }
            
            // 実際のライン消去は少し遅らせる
            setTimeout(() => {
                this.performLineClear(linesToClear);
            }, 200);
        }
    }
    
    performLineClear(linesToClear) {
        // 行を削除
        linesToClear.sort((a, b) => b - a); // 下から順に削除
        linesToClear.forEach(lineY => {
            this.board.splice(lineY, 1);
            this.board.unshift(Array(this.BOARD_WIDTH).fill(0));
        });
        
        // スコア計算
        this.lines += linesToClear.length;
        const baseScore = this.calculateScore(linesToClear.length);
        const comboBonus = Math.min(this.comboCount * 50, 500);
        this.score += baseScore + comboBonus;
        
        this.level = Math.floor(this.lines / 10) + 1;
        this.dropInterval = Math.max(100, 1000 - (this.level - 1) * 100);
        this.updateDisplay();
        
        // フラッシュリセット
        this.flashingLines = [];
        this.lineFlashTimer = 0;
    }
    
    calculateScore(linesCleared) {
        const baseScore = [0, 100, 300, 500, 800];
        return baseScore[linesCleared] * this.level;
    }
    
    updateDisplay() {
        // スコア更新時のアニメーション
        const scoreElement = document.getElementById('score');
        const linesElement = document.getElementById('lines');
        const levelElement = document.getElementById('level');
        
        if (scoreElement.textContent !== this.score.toString()) {
            scoreElement.textContent = this.score;
            scoreElement.parentElement.classList.add('score-popup');
            setTimeout(() => {
                scoreElement.parentElement.classList.remove('score-popup');
            }, 300);
        }
        
        linesElement.textContent = this.lines;
        levelElement.textContent = this.level;
    }
    
    createScreenFlash() {
        // 画面全体のフラッシュエフェクト
        const flash = document.createElement('div');
        flash.style.position = 'fixed';
        flash.style.top = '0';
        flash.style.left = '0';
        flash.style.width = '100%';
        flash.style.height = '100%';
        flash.style.background = 'radial-gradient(circle, rgba(212, 175, 55, 0.3) 0%, rgba(218, 165, 32, 0.1) 100%)';
        flash.style.pointerEvents = 'none';
        flash.style.zIndex = '9999';
        flash.style.opacity = '0';
        flash.style.transition = 'opacity 0.1s ease-in-out';
        
        document.body.appendChild(flash);
        
        // フラッシュアニメーション
        setTimeout(() => {
            flash.style.opacity = '1';
        }, 10);
        
        setTimeout(() => {
            flash.style.opacity = '0';
        }, 150);
        
        setTimeout(() => {
            document.body.removeChild(flash);
        }, 300);
    }
    
    togglePause() {
        this.paused = !this.paused;
        document.getElementById('pauseBtn').textContent = this.paused ? '再開' : '一時停止';
    }
    
    resetGame() {
        this.board = Array(this.BOARD_HEIGHT).fill().map(() => Array(this.BOARD_WIDTH).fill(0));
        this.score = 0;
        this.lines = 0;
        this.level = 1;
        this.gameOver = false;
        this.paused = false;
        this.dropInterval = 1000;
        this.dropTimer = 0;
        
        // エフェクト関連のリセット
        this.particleSystem = new ParticleSystem();
        this.lineFlashTimer = 0;
        this.flashingLines = [];
        this.comboCount = 0;
        
        this.nextPiece = this.getRandomPiece();
        this.spawnNewPiece();
        
        document.getElementById('gameOver').classList.add('hidden');
        document.getElementById('pauseBtn').textContent = '一時停止';
        this.updateDisplay();
    }
    
    showGameOver() {
        document.getElementById('finalScore').textContent = this.score;
        document.getElementById('gameOver').classList.remove('hidden');
    }
    
    draw() {
        // メインボードのクリア
        this.ctx.fillStyle = '#000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // ボードの描画
        this.drawBoard();
        
        // 現在のピースの描画
        if (this.currentPiece && !this.gameOver) {
            this.drawPiece(this.ctx, this.currentPiece, this.currentPiece.x, this.currentPiece.y);
        }
        
        // パーティクルエフェクトの描画
        this.particleSystem.draw(this.ctx);
        
        // 次のピースの描画
        this.drawNextPiece();
    }
    
    drawBoard() {
        for (let y = 0; y < this.BOARD_HEIGHT; y++) {
            for (let x = 0; x < this.BOARD_WIDTH; x++) {
                if (this.board[y][x]) {
                    let color = this.board[y][x];
                    
                    // フラッシュエフェクト
                    if (this.flashingLines.includes(y) && this.lineFlashTimer > 0) {
                        const flashIntensity = Math.sin(this.lineFlashTimer * 0.8) * 0.5 + 0.5;
                        if (this.lineFlashTimer % 8 < 4) {
                            color = '#ffffff';
                        } else {
                            color = `hsl(${60 + flashIntensity * 60}, 100%, ${70 + flashIntensity * 30}%)`;
                        }
                        
                        // 光るエフェクト
                        this.ctx.save();
                        this.ctx.shadowColor = color;
                        this.ctx.shadowBlur = 20;
                        this.ctx.fillStyle = color;
                        this.ctx.fillRect(x * this.BLOCK_SIZE, y * this.BLOCK_SIZE, 
                                        this.BLOCK_SIZE, this.BLOCK_SIZE);
                        this.ctx.restore();
                    } else {
                        this.ctx.fillStyle = color;
                        this.ctx.fillRect(x * this.BLOCK_SIZE, y * this.BLOCK_SIZE, 
                                        this.BLOCK_SIZE, this.BLOCK_SIZE);
                    }
                    
                    this.ctx.strokeStyle = '#333';
                    this.ctx.lineWidth = 1;
                    this.ctx.strokeRect(x * this.BLOCK_SIZE, y * this.BLOCK_SIZE, 
                                      this.BLOCK_SIZE, this.BLOCK_SIZE);
                }
            }
        }
    }
    
    drawPiece(ctx, piece, offsetX, offsetY) {
        ctx.fillStyle = piece.color;
        
        for (let y = 0; y < piece.shape.length; y++) {
            for (let x = 0; x < piece.shape[y].length; x++) {
                if (piece.shape[y][x]) {
                    const drawX = (offsetX + x) * this.BLOCK_SIZE;
                    const drawY = (offsetY + y) * this.BLOCK_SIZE;
                    
                    ctx.fillRect(drawX, drawY, this.BLOCK_SIZE, this.BLOCK_SIZE);
                    ctx.strokeStyle = '#333';
                    ctx.lineWidth = 1;
                    ctx.strokeRect(drawX, drawY, this.BLOCK_SIZE, this.BLOCK_SIZE);
                }
            }
        }
    }
    
    drawNextPiece() {
        this.nextCtx.fillStyle = '#000';
        this.nextCtx.fillRect(0, 0, this.nextCanvas.width, this.nextCanvas.height);
        
        if (this.nextPiece) {
            const blockSize = 20;
            const offsetX = (this.nextCanvas.width - this.nextPiece.shape[0].length * blockSize) / 2;
            const offsetY = (this.nextCanvas.height - this.nextPiece.shape.length * blockSize) / 2;
            
            this.nextCtx.fillStyle = this.nextPiece.color;
            
            for (let y = 0; y < this.nextPiece.shape.length; y++) {
                for (let x = 0; x < this.nextPiece.shape[y].length; x++) {
                    if (this.nextPiece.shape[y][x]) {
                        const drawX = offsetX + x * blockSize;
                        const drawY = offsetY + y * blockSize;
                        
                        this.nextCtx.fillRect(drawX, drawY, blockSize, blockSize);
                        this.nextCtx.strokeStyle = '#333';
                        this.nextCtx.lineWidth = 1;
                        this.nextCtx.strokeRect(drawX, drawY, blockSize, blockSize);
                    }
                }
            }
        }
    }
    
    update(deltaTime) {
        if (this.gameOver || this.paused) return;
        
        // パーティクルシステムの更新
        this.particleSystem.update();
        
        // フラッシュエフェクトの更新
        if (this.lineFlashTimer > 0) {
            this.lineFlashTimer--;
        }
        
        this.dropTimer += deltaTime;
        
        if (this.dropTimer >= this.dropInterval) {
            this.movePiece(0, 1);
            this.dropTimer = 0;
        }
    }
    
    gameLoop() {
        let lastTime = 0;
        
        const loop = (currentTime) => {
            const deltaTime = currentTime - lastTime;
            lastTime = currentTime;
            
            this.update(deltaTime);
            this.draw();
            
            requestAnimationFrame(loop);
        };
        
        requestAnimationFrame(loop);
    }
}

// ゲーム開始
window.addEventListener('load', () => {
    new TetrisGame();
});