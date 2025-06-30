class SeededRandom {
    constructor(seed) {
        this.seed = seed;
    }
    
    next() {
        this.seed = (this.seed * 9301 + 49297) % 233280;
        return this.seed / 233280;
    }
    
    range(min, max) {
        return min + this.next() * (max - min);
    }
    
    choice(arr) {
        return arr[Math.floor(this.next() * arr.length)];
    }
}

class BonsaiGenerator {
    constructor(canvas, seed) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        this.random = new SeededRandom(seed);
        this.season = this.random.choice(['spring', 'summer', 'autumn', 'winter']);
        
        this.init();
    }
    
    init() {
        this.clearCanvas();
        this.drawBackground();
        this.drawPot();
        this.drawSoil();
        this.drawTree();
        this.drawEnvironment();
    }
    
    clearCanvas() {
        this.ctx.clearRect(0, 0, this.width, this.height);
    }
    
    drawBackground() {
        // ベースの背景グラデーション
        const baseGradient = this.ctx.createLinearGradient(0, 0, 0, this.height);
        
        // 季節による背景色の変化
        const backgroundColors = this.getSeasonalBackground();
        backgroundColors.forEach((color, index) => {
            baseGradient.addColorStop(index / (backgroundColors.length - 1), color);
        });
        
        this.ctx.fillStyle = baseGradient;
        this.ctx.fillRect(0, 0, this.width, this.height);
        
        // 大気遠近法効果
        this.drawAtmosphericPerspective();
        
        // ボケた背景要素
        this.drawBlurredBackground();
        
        // 光の効果
        this.drawLightingEffects();
    }
    
    getSeasonalBackground() {
        switch (this.season) {
            case 'spring':
                return ['#e8f5e8', '#f0f8ff', '#f8f8f8', '#fff5ee'];
            case 'summer':
                return ['#e6f3ff', '#f0f8ff', '#f8f8f8', '#fffacd'];
            case 'autumn':
                return ['#ffebcd', '#faf0e6', '#f8f8f8', '#fff8dc'];
            case 'winter':
                return ['#f0f8ff', '#f5f5f5', '#f8f8f8', '#fffafa'];
            default:
                return ['#e6f3ff', '#f0f8ff', '#f8f8f8'];
        }
    }
    
    drawAtmosphericPerspective() {
        // 距離感を演出する薄い霧のような効果
        for (let i = 0; i < 3; i++) {
            const y = this.height * (0.3 + i * 0.2);
            const opacity = 0.1 - i * 0.03;
            
            const fogGradient = this.ctx.createLinearGradient(0, y, 0, y + 50);
            fogGradient.addColorStop(0, `rgba(255, 255, 255, 0)`);
            fogGradient.addColorStop(0.5, `rgba(255, 255, 255, ${opacity})`);
            fogGradient.addColorStop(1, `rgba(255, 255, 255, 0)`);
            
            this.ctx.fillStyle = fogGradient;
            this.ctx.fillRect(0, y, this.width, 50);
        }
    }
    
    drawBlurredBackground() {
        // ボケた遠景の表現
        this.ctx.globalAlpha = 0.3;
        
        // 遠くの山や丘の表現
        this.drawDistantHills();
        
        // 雲の表現
        this.drawClouds();
        
        this.ctx.globalAlpha = 1.0;
    }
    
    drawDistantHills() {
        const hillCount = 3;
        
        for (let i = 0; i < hillCount; i++) {
            const hillHeight = this.random.range(30, 80);
            const hillY = this.height * 0.4 + i * 20;
            const points = [];
            
            // 丘の輪郭を生成
            for (let x = 0; x <= this.width; x += 20) {
                const variation = Math.sin(x * 0.01 + i) * hillHeight * 0.3;
                points.push({
                    x: x,
                    y: hillY + variation
                });
            }
            
            // 丘の色（距離による色の変化）
            const hillColor = `rgba(${120 + i * 20}, ${140 + i * 20}, ${160 + i * 20}, ${0.4 - i * 0.1})`;
            
            this.ctx.fillStyle = hillColor;
            this.ctx.beginPath();
            this.ctx.moveTo(0, this.height);
            
            points.forEach(point => {
                this.ctx.lineTo(point.x, point.y);
            });
            
            this.ctx.lineTo(this.width, this.height);
            this.ctx.closePath();
            this.ctx.fill();
        }
    }
    
    drawClouds() {
        const cloudCount = this.random.range(2, 5);
        
        for (let i = 0; i < cloudCount; i++) {
            const cloudX = this.random.range(-50, this.width + 50);
            const cloudY = this.random.range(50, this.height * 0.4);
            const cloudSize = this.random.range(40, 100);
            
            this.drawSingleCloud(cloudX, cloudY, cloudSize);
        }
    }
    
    drawSingleCloud(x, y, size) {
        const puffCount = Math.floor(this.random.range(3, 8));
        
        for (let i = 0; i < puffCount; i++) {
            const puffX = x + this.random.range(-size * 0.5, size * 0.5);
            const puffY = y + this.random.range(-size * 0.3, size * 0.3);
            const puffSize = this.random.range(size * 0.3, size * 0.8);
            
            const cloudGradient = this.ctx.createRadialGradient(
                puffX, puffY, 0,
                puffX, puffY, puffSize
            );
            cloudGradient.addColorStop(0, 'rgba(255, 255, 255, 0.6)');
            cloudGradient.addColorStop(1, 'rgba(255, 255, 255, 0.1)');
            
            this.ctx.fillStyle = cloudGradient;
            this.ctx.beginPath();
            this.ctx.arc(puffX, puffY, puffSize, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }
    
    drawLightingEffects() {
        // 柔らかい光の演出
        const lightSource = {
            x: this.width * 0.7,
            y: this.height * 0.2
        };
        
        // 光の暈
        const lightGradient = this.ctx.createRadialGradient(
            lightSource.x, lightSource.y, 0,
            lightSource.x, lightSource.y, 200
        );
        lightGradient.addColorStop(0, 'rgba(255, 255, 224, 0.15)');
        lightGradient.addColorStop(0.5, 'rgba(255, 255, 224, 0.05)');
        lightGradient.addColorStop(1, 'rgba(255, 255, 224, 0)');
        
        this.ctx.fillStyle = lightGradient;
        this.ctx.beginPath();
        this.ctx.arc(lightSource.x, lightSource.y, 200, 0, Math.PI * 2);
        this.ctx.fill();
        
        // 光の粒子効果
        this.drawLightParticles(lightSource);
    }
    
    drawLightParticles(lightSource) {
        const particleCount = this.random.range(8, 15);
        
        for (let i = 0; i < particleCount; i++) {
            const angle = this.random.range(0, Math.PI * 2);
            const distance = this.random.range(50, 150);
            const particleX = lightSource.x + Math.cos(angle) * distance;
            const particleY = lightSource.y + Math.sin(angle) * distance;
            const particleSize = this.random.range(1, 3);
            
            this.ctx.fillStyle = `rgba(255, 255, 224, ${this.random.range(0.1, 0.3)})`;
            this.ctx.beginPath();
            this.ctx.arc(particleX, particleY, particleSize, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }
    
    drawPot() {
        const potY = this.height - 120;
        const potWidth = this.random.range(220, 300);
        const potHeight = this.random.range(70, 100);
        const potX = (this.width - potWidth) / 2;
        
        // 鉢のスタイルを選択
        const potStyle = this.random.choice(['traditional', 'modern', 'rustic', 'glazed']);
        
        // 鉢の影（より自然な影）
        this.drawPotShadow(potX, potY, potWidth, potHeight);
        
        // 鉢の本体
        this.drawPotBody(potX, potY, potWidth, potHeight, potStyle);
        
        // 鉢の縁
        this.drawPotRim(potX, potY, potWidth, potHeight, potStyle);
        
        // 装飾
        this.drawPotDecoration(potX, potY, potWidth, potHeight, potStyle);
        
        // 鉢の足
        this.drawPotFeet(potX, potY, potWidth, potHeight, potStyle);
        
        this.potData = { x: potX, y: potY, width: potWidth, height: potHeight, style: potStyle };
    }
    
    drawPotShadow(potX, potY, potWidth, potHeight) {
        // より自然な楕円の影
        const shadowOffsetX = 8;
        const shadowOffsetY = 8;
        const shadowWidth = potWidth + 10;
        const shadowHeight = 15;
        
        const shadowGradient = this.ctx.createRadialGradient(
            potX + potWidth / 2, potY + potHeight + shadowOffsetY,
            0,
            potX + potWidth / 2, potY + potHeight + shadowOffsetY,
            shadowWidth / 2
        );
        shadowGradient.addColorStop(0, 'rgba(0, 0, 0, 0.3)');
        shadowGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        
        this.ctx.fillStyle = shadowGradient;
        this.ctx.beginPath();
        this.ctx.ellipse(
            potX + potWidth / 2 + shadowOffsetX / 2,
            potY + potHeight + shadowOffsetY,
            shadowWidth / 2, shadowHeight / 2,
            0, 0, Math.PI * 2
        );
        this.ctx.fill();
    }
    
    drawPotBody(potX, potY, potWidth, potHeight, style) {
        const potColors = this.getPotColors(style);
        
        // 鉢の形状（より多様な形状）
        this.ctx.beginPath();
        if (style === 'modern') {
            // 直方体の現代的な鉢
            this.ctx.rect(potX + 5, potY, potWidth - 10, potHeight);
        } else if (style === 'rustic') {
            // 不規則な形の素朴な鉢
            this.drawIrregularPot(potX, potY, potWidth, potHeight);
        } else {
            // 伝統的な台形
            this.ctx.moveTo(potX + 15, potY);
            this.ctx.lineTo(potX + potWidth - 15, potY);
            this.ctx.lineTo(potX + potWidth - 5, potY + potHeight);
            this.ctx.lineTo(potX + 5, potY + potHeight);
            this.ctx.closePath();
        }
        
        // 鉢の質感
        if (style === 'glazed') {
            this.drawGlazedPot(potX, potY, potWidth, potHeight, potColors);
        } else {
            this.drawMattePot(potX, potY, potWidth, potHeight, potColors);
        }
        
        this.ctx.fill();
        
        // 鉢の輪郭
        this.ctx.strokeStyle = this.darkenColor(potColors.primary, 0.3);
        this.ctx.lineWidth = 1.5;
        this.ctx.stroke();
    }
    
    drawIrregularPot(potX, potY, potWidth, potHeight) {
        const points = [];
        const segments = 12;
        
        for (let i = 0; i < segments; i++) {
            const angle = (i / segments) * Math.PI * 2;
            const radiusVariation = this.random.range(0.9, 1.1);
            const x = potX + potWidth / 2 + Math.cos(angle) * (potWidth / 2 - 10) * radiusVariation;
            const y = potY + potHeight / 2 + Math.sin(angle) * (potHeight / 2) * radiusVariation;
            points.push({ x, y });
        }
        
        this.ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
            this.ctx.lineTo(points[i].x, points[i].y);
        }
        this.ctx.closePath();
    }
    
    drawGlazedPot(potX, potY, potWidth, potHeight, colors) {
        // 釉薬効果のグラデーション
        const glazeGradient = this.ctx.createLinearGradient(potX, potY, potX + potWidth, potY + potHeight);
        glazeGradient.addColorStop(0, this.lightenColor(colors.primary, 0.4));
        glazeGradient.addColorStop(0.3, colors.primary);
        glazeGradient.addColorStop(0.7, colors.secondary);
        glazeGradient.addColorStop(1, this.darkenColor(colors.secondary, 0.2));
        
        this.ctx.fillStyle = glazeGradient;
    }
    
    drawMattePot(potX, potY, potWidth, potHeight, colors) {
        // マットな質感
        const matteGradient = this.ctx.createLinearGradient(potX, potY, potX, potY + potHeight);
        matteGradient.addColorStop(0, colors.primary);
        matteGradient.addColorStop(1, colors.secondary);
        
        this.ctx.fillStyle = matteGradient;
    }
    
    drawPotRim(potX, potY, potWidth, potHeight, style) {
        const rimHeight = 6;
        const rimGradient = this.ctx.createLinearGradient(potX, potY - rimHeight, potX, potY);
        const colors = this.getPotColors(style);
        
        rimGradient.addColorStop(0, this.lightenColor(colors.primary, 0.3));
        rimGradient.addColorStop(1, colors.primary);
        
        this.ctx.fillStyle = rimGradient;
        this.ctx.beginPath();
        
        if (style === 'modern') {
            this.ctx.rect(potX, potY - rimHeight, potWidth, rimHeight);
        } else {
            this.ctx.moveTo(potX + 10, potY - rimHeight);
            this.ctx.lineTo(potX + potWidth - 10, potY - rimHeight);
            this.ctx.lineTo(potX + 15, potY);
            this.ctx.lineTo(potX + potWidth - 15, potY);
            this.ctx.closePath();
        }
        
        this.ctx.fill();
        this.ctx.strokeStyle = this.darkenColor(colors.primary, 0.2);
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    }
    
    drawPotDecoration(potX, potY, potWidth, potHeight, style) {
        const colors = this.getPotColors(style);
        
        if (style === 'traditional') {
            // 伝統的な波模様
            this.drawWavePattern(potX, potY, potWidth, potHeight, colors);
        } else if (style === 'glazed') {
            // 釉薬の流れ
            this.drawGlazeDrops(potX, potY, potWidth, potHeight, colors);
        } else if (style === 'rustic') {
            // 素朴な線模様
            this.drawRusticLines(potX, potY, potWidth, potHeight, colors);
        }
    }
    
    drawWavePattern(potX, potY, potWidth, potHeight, colors) {
        this.ctx.strokeStyle = `rgba(255, 255, 255, 0.3)`;
        this.ctx.lineWidth = 1;
        
        for (let i = 0; i < 2; i++) {
            const y = potY + (i + 1) * (potHeight / 3);
            this.ctx.beginPath();
            
            for (let x = potX + 20; x < potX + potWidth - 20; x += 10) {
                const waveY = y + Math.sin((x - potX) * 0.1) * 3;
                if (x === potX + 20) {
                    this.ctx.moveTo(x, waveY);
                } else {
                    this.ctx.lineTo(x, waveY);
                }
            }
            this.ctx.stroke();
        }
    }
    
    drawGlazeDrops(potX, potY, potWidth, potHeight, colors) {
        const dropCount = Math.floor(this.random.range(3, 8));
        
        for (let i = 0; i < dropCount; i++) {
            const x = potX + this.random.range(20, potWidth - 20);
            const startY = potY + this.random.range(10, 30);
            const endY = startY + this.random.range(20, 40);
            
            const dropGradient = this.ctx.createLinearGradient(x, startY, x, endY);
            dropGradient.addColorStop(0, `rgba(255, 255, 255, 0.4)`);
            dropGradient.addColorStop(1, `rgba(255, 255, 255, 0.1)`);
            
            this.ctx.strokeStyle = dropGradient;
            this.ctx.lineWidth = this.random.range(2, 4);
            this.ctx.beginPath();
            this.ctx.moveTo(x, startY);
            this.ctx.lineTo(x + this.random.range(-2, 2), endY);
            this.ctx.stroke();
        }
    }
    
    drawRusticLines(potX, potY, potWidth, potHeight, colors) {
        this.ctx.strokeStyle = `rgba(0, 0, 0, 0.2)`;
        this.ctx.lineWidth = 0.5;
        
        for (let i = 0; i < 5; i++) {
            const y = potY + this.random.range(10, potHeight - 10);
            const startX = potX + this.random.range(10, 30);
            const endX = potX + potWidth - this.random.range(10, 30);
            
            this.ctx.beginPath();
            this.ctx.moveTo(startX, y);
            this.ctx.lineTo(endX, y + this.random.range(-3, 3));
            this.ctx.stroke();
        }
    }
    
    drawPotFeet(potX, potY, potWidth, potHeight, style) {
        if (style === 'modern') return; // モダンスタイルには足がない
        
        const footCount = 3;
        const footWidth = 8;
        const footHeight = 4;
        const colors = this.getPotColors(style);
        
        for (let i = 0; i < footCount; i++) {
            const footX = potX + (i + 1) * (potWidth / (footCount + 1)) - footWidth / 2;
            const footY = potY + potHeight;
            
            this.ctx.fillStyle = this.darkenColor(colors.primary, 0.2);
            this.ctx.fillRect(footX, footY, footWidth, footHeight);
            
            this.ctx.strokeStyle = this.darkenColor(colors.primary, 0.4);
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(footX, footY, footWidth, footHeight);
        }
    }
    
    getPotColors(style) {
        const colorSets = {
            traditional: {
                primary: '#8B4513',
                secondary: '#A0522D'
            },
            modern: {
                primary: '#424242',
                secondary: '#616161'
            },
            rustic: {
                primary: '#5D4037',
                secondary: '#795548'
            },
            glazed: {
                primary: '#2E7D32',
                secondary: '#388E3C'
            }
        };
        
        return colorSets[style] || colorSets.traditional;
    }
    
    drawSoil() {
        const { x, y, width, height, style } = this.potData;
        const soilHeight = this.random.range(18, 25);
        const soilY = y + height - soilHeight;
        
        // 土の基本層を描画
        this.drawSoilLayers(x, soilY, width, soilHeight);
        
        // 土の質感とテクスチャ
        this.drawSoilTexture(x, soilY, width, soilHeight);
        
        // 苔を描画
        this.drawMoss(x, soilY, width, soilHeight);
        
        // 小石を描画
        this.drawPebbles(x, soilY, width, soilHeight);
        
        // 小さな植物
        this.drawSmallPlants(x, soilY, width, soilHeight);
        
        // 根の一部が見える効果
        this.drawVisibleRoots(x, soilY, width, soilHeight);
        
        this.soilY = soilY;
    }
    
    drawSoilLayers(x, soilY, width, soilHeight) {
        // 複数の土の層を描画
        const layers = [
            { color: '#5D4E37', height: 0.4 },  // 上層土
            { color: '#4A4A4A', height: 0.3 },  // 中層土
            { color: '#2C2C2C', height: 0.3 }   // 下層土
        ];
        
        let currentY = soilY;
        
        layers.forEach(layer => {
            const layerHeight = soilHeight * layer.height;
            
            const layerGradient = this.ctx.createLinearGradient(x, currentY, x, currentY + layerHeight);
            layerGradient.addColorStop(0, this.lightenColor(layer.color, 0.1));
            layerGradient.addColorStop(1, this.darkenColor(layer.color, 0.1));
            
            this.ctx.fillStyle = layerGradient;
            this.ctx.fillRect(x + 5, currentY, width - 10, layerHeight);
            
            currentY += layerHeight;
        });
    }
    
    drawSoilTexture(x, soilY, width, soilHeight) {
        // 土粒の表現
        for (let i = 0; i < 80; i++) {
            const px = x + this.random.range(5, width - 5);
            const py = soilY + this.random.range(0, soilHeight);
            const size = this.random.range(0.5, 2);
            
            this.ctx.fillStyle = `rgba(${this.random.range(60, 100)}, ${this.random.range(45, 75)}, ${this.random.range(30, 50)}, ${this.random.range(0.3, 0.8)})`;
            this.ctx.beginPath();
            this.ctx.arc(px, py, size, 0, Math.PI * 2);
            this.ctx.fill();
        }
        
        // 土の亀裂
        for (let i = 0; i < 5; i++) {
            const startX = x + this.random.range(10, width - 10);
            const startY = soilY + this.random.range(2, 8);
            const endX = startX + this.random.range(-15, 15);
            const endY = startY + this.random.range(5, 12);
            
            this.ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
            this.ctx.lineWidth = this.random.range(0.5, 1.5);
            this.ctx.beginPath();
            this.ctx.moveTo(startX, startY);
            this.ctx.lineTo(endX, endY);
            this.ctx.stroke();
        }
    }
    
    drawMoss(x, soilY, width, soilHeight) {
        const mossPatches = Math.floor(this.random.range(3, 8));
        
        for (let i = 0; i < mossPatches; i++) {
            const mossX = x + this.random.range(10, width - 20);
            const mossY = soilY + this.random.range(0, soilHeight * 0.5);
            const mossSize = this.random.range(8, 20);
            
            // 苔の基盤
            const mossGradient = this.ctx.createRadialGradient(mossX, mossY, 0, mossX, mossY, mossSize);
            mossGradient.addColorStop(0, 'rgba(34, 139, 34, 0.6)');
            mossGradient.addColorStop(1, 'rgba(34, 139, 34, 0.2)');
            
            this.ctx.fillStyle = mossGradient;
            this.ctx.beginPath();
            this.ctx.arc(mossX, mossY, mossSize, 0, Math.PI * 2);
            this.ctx.fill();
            
            // 苔の細かい部分
            for (let j = 0; j < 15; j++) {
                const dotX = mossX + this.random.range(-mossSize * 0.7, mossSize * 0.7);
                const dotY = mossY + this.random.range(-mossSize * 0.7, mossSize * 0.7);
                const dotSize = this.random.range(0.5, 2);
                
                this.ctx.fillStyle = `rgba(${this.random.range(20, 60)}, ${this.random.range(100, 140)}, ${this.random.range(20, 60)}, 0.7)`;
                this.ctx.beginPath();
                this.ctx.arc(dotX, dotY, dotSize, 0, Math.PI * 2);
                this.ctx.fill();
            }
        }
    }
    
    drawPebbles(x, soilY, width, soilHeight) {
        const pebbleCount = Math.floor(this.random.range(8, 15));
        
        for (let i = 0; i < pebbleCount; i++) {
            const pebbleX = x + this.random.range(8, width - 8);
            const pebbleY = soilY + this.random.range(2, soilHeight - 2);
            const pebbleSize = this.random.range(2, 6);
            
            // 小石の影
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            this.ctx.beginPath();
            this.ctx.ellipse(pebbleX + 1, pebbleY + 1, pebbleSize, pebbleSize * 0.6, 0, 0, Math.PI * 2);
            this.ctx.fill();
            
            // 小石本体
            const pebbleColors = ['#8B8B8B', '#A9A9A9', '#696969', '#778899'];
            const pebbleColor = this.random.choice(pebbleColors);
            
            const pebbleGradient = this.ctx.createRadialGradient(
                pebbleX - pebbleSize * 0.3, pebbleY - pebbleSize * 0.3, 0,
                pebbleX, pebbleY, pebbleSize
            );
            pebbleGradient.addColorStop(0, this.lightenColor(pebbleColor, 0.3));
            pebbleGradient.addColorStop(1, pebbleColor);
            
            this.ctx.fillStyle = pebbleGradient;
            this.ctx.beginPath();
            this.ctx.ellipse(pebbleX, pebbleY, pebbleSize, pebbleSize * 0.8, this.random.range(0, Math.PI), 0, Math.PI * 2);
            this.ctx.fill();
        }
    }
    
    drawSmallPlants(x, soilY, width, soilHeight) {
        const plantCount = Math.floor(this.random.range(2, 6));
        
        for (let i = 0; i < plantCount; i++) {
            const plantX = x + this.random.range(15, width - 15);
            const plantY = soilY + this.random.range(0, 5);
            
            // 小さな草の茎
            this.ctx.strokeStyle = `rgba(${this.random.range(60, 100)}, ${this.random.range(120, 160)}, ${this.random.range(60, 100)}, 0.7)`;
            this.ctx.lineWidth = 0.8;
            
            const stemCount = Math.floor(this.random.range(2, 5));
            for (let j = 0; j < stemCount; j++) {
                const stemX = plantX + this.random.range(-3, 3);
                const stemHeight = this.random.range(5, 12);
                
                this.ctx.beginPath();
                this.ctx.moveTo(stemX, plantY);
                this.ctx.lineTo(stemX + this.random.range(-2, 2), plantY - stemHeight);
                this.ctx.stroke();
                
                // 小さな葉
                if (this.random.next() > 0.5) {
                    const leafX = stemX + this.random.range(-1, 1);
                    const leafY = plantY - stemHeight * 0.7;
                    
                    this.ctx.fillStyle = `rgba(${this.random.range(80, 120)}, ${this.random.range(140, 180)}, ${this.random.range(80, 120)}, 0.6)`;
                    this.ctx.beginPath();
                    this.ctx.arc(leafX, leafY, 1, 0, Math.PI * 2);
                    this.ctx.fill();
                }
            }
        }
    }
    
    drawVisibleRoots(x, soilY, width, soilHeight) {
        const rootCount = Math.floor(this.random.range(2, 5));
        
        for (let i = 0; i < rootCount; i++) {
            const rootX = x + this.random.range(width * 0.3, width * 0.7);
            const rootY = soilY + this.random.range(soilHeight * 0.3, soilHeight);
            
            this.ctx.strokeStyle = `rgba(${this.random.range(80, 120)}, ${this.random.range(60, 100)}, ${this.random.range(40, 80)}, 0.5)`;
            this.ctx.lineWidth = this.random.range(1, 3);
            
            // 曲がりくねった根
            const segments = 3;
            let currentX = rootX;
            let currentY = rootY;
            
            this.ctx.beginPath();
            this.ctx.moveTo(currentX, currentY);
            
            for (let j = 0; j < segments; j++) {
                const nextX = currentX + this.random.range(-8, 8);
                const nextY = currentY + this.random.range(3, 8);
                
                this.ctx.lineTo(nextX, nextY);
                currentX = nextX;
                currentY = nextY;
            }
            
            this.ctx.stroke();
        }
    }
    
    drawTree() {
        const startX = this.width / 2 + this.random.range(-20, 20);
        const startY = this.soilY;
        const baseThickness = this.random.range(12, 18);
        const treeHeight = this.random.range(150, 250);
        
        this.drawBranch(startX, startY, -Math.PI / 2, baseThickness, treeHeight, 0, 6);
    }
    
    drawBranch(x, y, angle, thickness, length, generation, maxGeneration) {
        if (generation > maxGeneration || thickness < 0.8) return;
        
        const endX = x + Math.cos(angle) * length;
        const endY = y + Math.sin(angle) * length;
        
        // より自然な太さの変化
        const segments = Math.max(3, Math.floor(length / 15));
        const segmentLength = length / segments;
        
        for (let i = 0; i < segments; i++) {
            const segStart = i / segments;
            const segEnd = (i + 1) / segments;
            
            const startX = x + Math.cos(angle) * length * segStart;
            const startY = y + Math.sin(angle) * length * segStart;
            const segEndX = x + Math.cos(angle) * length * segEnd;
            const segEndY = y + Math.sin(angle) * length * segEnd;
            
            // 太さの自然な減少
            const thicknessStart = thickness * (1 - segStart * 0.3);
            const thicknessEnd = thickness * (1 - segEnd * 0.3);
            
            // 基本の幹を描画
            this.drawBarkSegment(startX, startY, segEndX, segEndY, thicknessStart, thicknessEnd, generation);
        }
        
        // 節を描画
        if (generation <= 2 && thickness > 4) {
            this.drawBarkNodes(x, y, endX, endY, thickness, generation);
        }
        
        // 盆栽特有の剪定された枝の形状
        if (generation < maxGeneration) {
            const numBranches = this.getBranchCount(generation, thickness);
            
            for (let i = 0; i < numBranches; i++) {
                // 盆栽らしい分岐位置
                const branchPoint = this.getBonsaiBranchPoint(generation);
                const branchX = x + Math.cos(angle) * length * branchPoint;
                const branchY = y + Math.sin(angle) * length * branchPoint;
                
                // 盆栽らしい角度制御
                const angleVariation = this.getBonsaiAngleVariation(generation, i, numBranches);
                const newAngle = angle + angleVariation;
                const newThickness = thickness * this.random.range(0.55, 0.75);
                const newLength = length * this.random.range(0.45, 0.75);
                
                this.drawBranch(branchX, branchY, newAngle, newThickness, newLength, generation + 1, maxGeneration);
            }
        }
        
        // より密集した葉を描画
        if (generation >= 2 && thickness < 8) {
            this.drawDenseLeaves(endX, endY, angle, generation, thickness);
        }
    }
    
    drawBarkSegment(startX, startY, endX, endY, thicknessStart, thicknessEnd, generation) {
        // 基本の幹色
        const baseColor = this.getBranchColor(generation);
        
        // グラデーションで立体感を表現
        const gradient = this.ctx.createLinearGradient(startX - thicknessStart/2, startY, startX + thicknessStart/2, startY);
        const darkColor = this.darkenColor(baseColor, 0.3);
        const lightColor = this.lightenColor(baseColor, 0.2);
        
        gradient.addColorStop(0, darkColor);
        gradient.addColorStop(0.3, baseColor);
        gradient.addColorStop(0.7, lightColor);
        gradient.addColorStop(1, darkColor);
        
        // メインの幹を描画
        this.ctx.strokeStyle = gradient;
        this.ctx.lineWidth = thicknessStart;
        this.ctx.lineCap = 'round';
        
        this.ctx.beginPath();
        this.ctx.moveTo(startX, startY);
        this.ctx.lineTo(endX, endY);
        this.ctx.stroke();
        
        // 樹皮のテクスチャを追加
        this.addBarkTexture(startX, startY, endX, endY, thicknessStart, generation);
    }
    
    addBarkTexture(startX, startY, endX, endY, thickness, generation) {
        if (thickness < 3) return;
        
        const length = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
        const angle = Math.atan2(endY - startY, endX - startX);
        const textureCount = Math.floor(length / 5) + Math.floor(thickness / 2);
        
        for (let i = 0; i < textureCount; i++) {
            const progress = this.random.next();
            const currentX = startX + (endX - startX) * progress;
            const currentY = startY + (endY - startY) * progress;
            const currentThickness = thickness * (1 - progress * 0.2);
            
            // 縦方向の樹皮の線
            const perpAngle = angle + Math.PI / 2;
            const offset = this.random.range(-currentThickness / 3, currentThickness / 3);
            const lineLength = this.random.range(2, 6);
            
            const lineStartX = currentX + Math.cos(perpAngle) * offset;
            const lineStartY = currentY + Math.sin(perpAngle) * offset;
            const lineEndX = lineStartX + Math.cos(angle) * lineLength;
            const lineEndY = lineStartY + Math.sin(angle) * lineLength;
            
            this.ctx.strokeStyle = `rgba(0, 0, 0, ${this.random.range(0.1, 0.3)})`;
            this.ctx.lineWidth = 0.5;
            this.ctx.beginPath();
            this.ctx.moveTo(lineStartX, lineStartY);
            this.ctx.lineTo(lineEndX, lineEndY);
            this.ctx.stroke();
            
            // 樹皮の小さな斑点
            if (this.random.next() > 0.7) {
                this.ctx.fillStyle = `rgba(${this.random.range(20, 40)}, ${this.random.range(15, 30)}, ${this.random.range(10, 25)}, 0.4)`;
                this.ctx.beginPath();
                this.ctx.arc(currentX + this.random.range(-2, 2), currentY + this.random.range(-2, 2), 0.5, 0, Math.PI * 2);
                this.ctx.fill();
            }
        }
    }
    
    drawBarkNodes(startX, startY, endX, endY, thickness, generation) {
        const nodeCount = Math.floor(this.random.range(1, 4));
        
        for (let i = 0; i < nodeCount; i++) {
            const progress = this.random.range(0.2, 0.8);
            const nodeX = startX + (endX - startX) * progress;
            const nodeY = startY + (endY - startY) * progress;
            const nodeSize = thickness * this.random.range(0.3, 0.6);
            
            // 節の影
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
            this.ctx.beginPath();
            this.ctx.arc(nodeX + 1, nodeY + 1, nodeSize, 0, Math.PI * 2);
            this.ctx.fill();
            
            // 節本体
            const nodeGradient = this.ctx.createRadialGradient(nodeX, nodeY, 0, nodeX, nodeY, nodeSize);
            const nodeColor = this.getBranchColor(generation);
            nodeGradient.addColorStop(0, this.lightenColor(nodeColor, 0.1));
            nodeGradient.addColorStop(1, this.darkenColor(nodeColor, 0.2));
            
            this.ctx.fillStyle = nodeGradient;
            this.ctx.beginPath();
            this.ctx.arc(nodeX, nodeY, nodeSize, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }
    
    getBranchCount(generation, thickness) {
        if (generation === 0) return Math.floor(this.random.range(2, 4));
        if (generation === 1) return Math.floor(this.random.range(2, 5));
        if (generation === 2) return Math.floor(this.random.range(1, 4));
        return Math.floor(this.random.range(1, 3));
    }
    
    getBonsaiBranchPoint(generation) {
        if (generation === 0) return this.random.range(0.3, 0.7);
        if (generation === 1) return this.random.range(0.4, 0.8);
        return this.random.range(0.5, 0.9);
    }
    
    getBonsaiAngleVariation(generation, branchIndex, totalBranches) {
        const baseVariation = Math.PI / (generation + 2);
        
        if (generation === 0) {
            // 主幹から伸びる主要な枝
            const side = branchIndex % 2 === 0 ? -1 : 1;
            return side * this.random.range(baseVariation * 0.5, baseVariation);
        } else {
            // より自然な分散
            return this.random.range(-baseVariation, baseVariation);
        }
    }
    
    darkenColor(color, amount) {
        const rgb = this.hexToRgb(color);
        if (!rgb) return color;
        
        const r = Math.max(0, Math.floor(rgb.r * (1 - amount)));
        const g = Math.max(0, Math.floor(rgb.g * (1 - amount)));
        const b = Math.max(0, Math.floor(rgb.b * (1 - amount)));
        
        return `rgb(${r}, ${g}, ${b})`;
    }
    
    lightenColor(color, amount) {
        const rgb = this.hexToRgb(color);
        if (!rgb) return color;
        
        const r = Math.min(255, Math.floor(rgb.r + (255 - rgb.r) * amount));
        const g = Math.min(255, Math.floor(rgb.g + (255 - rgb.g) * amount));
        const b = Math.min(255, Math.floor(rgb.b + (255 - rgb.b) * amount));
        
        return `rgb(${r}, ${g}, ${b})`;
    }
    
    hexToRgb(color) {
        // RGB形式の色を処理
        if (color.startsWith('rgb')) {
            const match = color.match(/\d+/g);
            if (match && match.length >= 3) {
                return {
                    r: parseInt(match[0]),
                    g: parseInt(match[1]),
                    b: parseInt(match[2])
                };
            }
        }
        
        // Hex形式の色を処理
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(color);
        if (result) {
            return {
                r: parseInt(result[1], 16),
                g: parseInt(result[2], 16),
                b: parseInt(result[3], 16)
            };
        }
        
        // 既知の色名を処理
        const colorMap = {
            '#3E2723': { r: 62, g: 39, b: 35 },
            '#4A4A4A': { r: 74, g: 74, b: 74 },
            '#2C2C2C': { r: 44, g: 44, b: 44 },
            '#4A7C59': { r: 74, g: 124, b: 89 },
            '#6B8E23': { r: 107, g: 142, b: 35 },
            '#8B7355': { r: 139, g: 115, b: 85 }
        };
        
        return colorMap[color] || { r: 100, g: 80, b: 60 };
    }
    
    getBranchColor(generation) {
        const baseColors = ['#3E2723', '#4A4A4A', '#2C2C2C'];
        const youngColors = ['#4A7C59', '#6B8E23', '#8B7355'];
        
        if (generation < 2) {
            return baseColors[Math.floor(this.random.next() * baseColors.length)];
        } else {
            return youngColors[Math.floor(this.random.next() * youngColors.length)];
        }
    }
    
    drawDenseLeaves(x, y, angle, generation, thickness) {
        const leafDensity = Math.max(5, Math.floor(thickness * 2));
        const leafClusterCount = Math.floor(this.random.range(2, 5));
        const leafColors = this.getSeasonalColors();
        
        for (let cluster = 0; cluster < leafClusterCount; cluster++) {
            const clusterAngle = angle + this.random.range(-Math.PI / 2, Math.PI / 2);
            const clusterDistance = this.random.range(3, 8);
            const clusterX = x + Math.cos(clusterAngle) * clusterDistance;
            const clusterY = y + Math.sin(clusterAngle) * clusterDistance;
            
            // クラスター内の密集した葉
            for (let i = 0; i < leafDensity; i++) {
                const leafAngle = clusterAngle + this.random.range(-Math.PI / 4, Math.PI / 4);
                const leafDistance = this.random.range(1, 4);
                const leafX = clusterX + Math.cos(leafAngle) * leafDistance;
                const leafY = clusterY + Math.sin(leafAngle) * leafDistance;
                
                const leafColor = this.random.choice(leafColors);
                const leafSize = this.random.range(1.5, 3.5);
                
                // より自然な葉の形状
                this.drawNaturalLeaf(leafX, leafY, leafAngle, leafSize, leafColor);
            }
        }
    }
    
    drawNaturalLeaf(x, y, angle, size, color) {
        const leafType = this.random.next();
        
        // 葉の影
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.beginPath();
        if (leafType > 0.6) {
            // 針葉
            this.drawNeedleLeaf(x + 0.5, y + 0.5, angle, size);
        } else if (leafType > 0.3) {
            // 小さな円形葉
            this.ctx.arc(x + 0.5, y + 0.5, size, 0, Math.PI * 2);
        } else {
            // 楕円葉
            this.ctx.ellipse(x + 0.5, y + 0.5, size, size * 0.6, angle, 0, Math.PI * 2);
        }
        this.ctx.fill();
        
        // 葉本体
        const leafGradient = this.ctx.createRadialGradient(x, y, 0, x, y, size);
        leafGradient.addColorStop(0, this.lightenColor(color, 0.2));
        leafGradient.addColorStop(1, color);
        
        this.ctx.fillStyle = leafGradient;
        this.ctx.beginPath();
        
        if (leafType > 0.6) {
            // 針葉
            this.drawNeedleLeaf(x, y, angle, size);
        } else if (leafType > 0.3) {
            // 小さな円形葉
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
        } else {
            // 楕円葉
            this.ctx.ellipse(x, y, size, size * 0.6, angle, 0, Math.PI * 2);
        }
        this.ctx.fill();
        
        // 葉脈
        if (size > 2) {
            this.ctx.strokeStyle = `rgba(0, 0, 0, 0.2)`;
            this.ctx.lineWidth = 0.3;
            this.ctx.beginPath();
            this.ctx.moveTo(x, y);
            this.ctx.lineTo(x + Math.cos(angle) * size * 0.7, y + Math.sin(angle) * size * 0.7);
            this.ctx.stroke();
        }
    }
    
    drawNeedleLeaf(x, y, angle, size) {
        const length = size * 2;
        const width = size * 0.3;
        
        this.ctx.save();
        this.ctx.translate(x, y);
        this.ctx.rotate(angle);
        this.ctx.beginPath();
        this.ctx.ellipse(0, 0, length, width, 0, 0, Math.PI * 2);
        this.ctx.restore();
    }
    
    getSeasonalColors() {
        switch (this.season) {
            case 'spring':
                return ['#90EE90', '#7CFC00', '#98FB98', '#32CD32', '#00FF7F'];
            case 'summer':
                return ['#228B22', '#006400', '#32CD32', '#2E8B57', '#008B00'];
            case 'autumn':
                return ['#FF6347', '#FF4500', '#FFD700', '#FFA500', '#DC143C'];
            case 'winter':
                return ['#556B2F', '#6B8E23', '#8FBC8F', '#9ACD32', '#A0522D'];
            default:
                return ['#228B22', '#006400', '#32CD32'];
        }
    }
    
    drawEnvironment() {
        // 地面の装飾
        this.drawGround();
        
        // 季節的な要素
        if (this.season === 'autumn') {
            this.drawFallingLeaves();
        } else if (this.season === 'winter') {
            this.drawSnow();
        } else if (this.season === 'spring') {
            this.drawPetals();
        }
    }
    
    drawGround() {
        const groundY = this.height - 20;
        
        // 地面のグラデーション
        const groundGradient = this.ctx.createLinearGradient(0, groundY, 0, this.height);
        groundGradient.addColorStop(0, '#8B7355');
        groundGradient.addColorStop(1, '#654321');
        
        this.ctx.fillStyle = groundGradient;
        this.ctx.fillRect(0, groundY, this.width, 20);
        
        // 小石や草
        for (let i = 0; i < 20; i++) {
            const x = this.random.range(0, this.width);
            const y = this.random.range(groundY, this.height);
            
            if (this.random.next() > 0.5) {
                // 小石
                this.ctx.fillStyle = `rgba(${this.random.range(80, 120)}, ${this.random.range(80, 120)}, ${this.random.range(80, 120)}, 0.8)`;
                this.ctx.beginPath();
                this.ctx.arc(x, y, this.random.range(1, 3), 0, Math.PI * 2);
                this.ctx.fill();
            } else {
                // 草
                this.ctx.strokeStyle = `rgba(${this.random.range(60, 100)}, ${this.random.range(120, 160)}, ${this.random.range(60, 100)}, 0.6)`;
                this.ctx.lineWidth = 1;
                this.ctx.beginPath();
                this.ctx.moveTo(x, y);
                this.ctx.lineTo(x + this.random.range(-2, 2), y - this.random.range(3, 8));
                this.ctx.stroke();
            }
        }
    }
    
    drawFallingLeaves() {
        const leafCount = this.random.range(5, 12);
        const colors = ['#FF6347', '#FF4500', '#FFD700', '#FFA500'];
        
        for (let i = 0; i < leafCount; i++) {
            const x = this.random.range(0, this.width);
            const y = this.random.range(0, this.height * 0.7);
            const size = this.random.range(2, 5);
            const color = this.random.choice(colors);
            
            this.ctx.fillStyle = color;
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }
    
    drawSnow() {
        const snowCount = this.random.range(10, 20);
        
        for (let i = 0; i < snowCount; i++) {
            const x = this.random.range(0, this.width);
            const y = this.random.range(0, this.height * 0.8);
            const size = this.random.range(1, 3);
            
            this.ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }
    
    drawPetals() {
        const petalCount = this.random.range(8, 15);
        const colors = ['#FFB6C1', '#FFC0CB', '#FFCCCB', '#F0E68C'];
        
        for (let i = 0; i < petalCount; i++) {
            const x = this.random.range(0, this.width);
            const y = this.random.range(0, this.height * 0.6);
            const size = this.random.range(2, 4);
            const color = this.random.choice(colors);
            
            this.ctx.fillStyle = color;
            this.ctx.beginPath();
            this.ctx.arc(x, y, size, 0, Math.PI * 2);
            this.ctx.fill();
        }
    }
}

// 初期化
document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('bonsaiCanvas');
    const generateBtn = document.getElementById('generateBtn');
    const seedDisplay = document.getElementById('seedValue');
    
    let currentSeed = window.bonsaiSeed || Math.floor(Math.random() * 1000000);
    
    function generateBonsai() {
        const bonsai = new BonsaiGenerator(canvas, currentSeed);
        seedDisplay.textContent = currentSeed;
    }
    
    generateBtn.addEventListener('click', function() {
        currentSeed = Math.floor(Math.random() * 1000000);
        generateBonsai();
    });
    
    // 初回生成
    generateBonsai();
});