// シンプルで確実に動作する日本地図

class SimpleWorkingMap {
    constructor() {
        this.width = 800;
        this.height = 600;
        this.prefecturesData = [];
        this.selectedPrefecture = null;
        
        this.init();
    }
    
    async init() {
        console.log('Starting map initialization...');
        try {
            await this.loadPrefecturesData();
            this.setupMap();
            this.drawMap();
            this.setupTooltip();
            console.log('Map initialization complete!');
        } catch (error) {
            console.error('Map initialization failed:', error);
        }
    }
    
    async loadPrefecturesData() {
        try {
            console.log('Loading prefecture data...');
            const response = await fetch('/api/prefectures');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.prefecturesData = await response.json();
            console.log('Loaded prefecture data:', this.prefecturesData.length, 'prefectures');
        } catch (error) {
            console.error('都道府県データの読み込みに失敗しました:', error);
            // フォールバック: 基本的なデータを設定
            this.prefecturesData = [
                {name: "北海道", code: "01", region: "北海道"},
                {name: "東京都", code: "13", region: "関東"}
            ];
        }
    }
    
    setupMap() {
        console.log('Setting up SVG map...');
        const svg = d3.select('#japan-map')
            .attr('width', this.width)
            .attr('height', this.height)
            .attr('viewBox', `0 0 ${this.width} ${this.height}`)
            .style('border', '1px solid #ccc');
        
        console.log('SVG setup complete');
    }
    
    drawMap() {
        console.log('Drawing map...');
        const svg = d3.select('#japan-map');
        
        // シンプルな地図データ - 基本的な形状
        const mapData = [
            // 北海道
            { 
                name: '北海道', 
                x: 350, y: 50, width: 120, height: 80,
                path: 'M350,50 L470,50 Q480,60 480,80 L470,130 Q460,140 440,135 L380,125 Q360,120 350,100 Q340,80 350,60 Z'
            },
            // 本州（簡略化）
            { 
                name: '東京都', 
                x: 430, y: 270, width: 20, height: 20,
                path: 'M430,270 L450,270 L450,290 L430,290 Z'
            },
            {
                name: '群馬県',
                x: 380, y: 240, width: 40, height: 30,
                path: 'M380,240 Q390,235 405,240 Q415,250 420,260 Q425,270 415,275 L395,270 Q385,260 380,250 Z'
            },
            {
                name: '千葉県',
                x: 450, y: 230, width: 40, height: 50,
                path: 'M450,230 Q470,225 485,235 Q495,250 490,265 Q485,280 470,275 L450,270 Q445,250 450,230 Z'
            }
        ];
        
        // 都道府県を描画
        svg.selectAll('.prefecture')
            .data(mapData)
            .enter()
            .append('path')
            .attr('class', d => `prefecture ${this.getRegionClass(d.name)}`)
            .attr('d', d => d.path)
            .attr('stroke', '#ffffff')
            .attr('stroke-width', 2)
            .attr('fill', d => this.getRegionColor(d.name))
            .style('cursor', 'pointer')
            .on('click', (event, d) => {
                console.log('Prefecture clicked:', d.name);
                this.onPrefectureClick(d);
            })
            .on('mouseover', (event, d) => this.showTooltip(event, d))
            .on('mouseout', () => this.hideTooltip());
        
        // ラベルを追加
        svg.selectAll('.prefecture-label')
            .data(mapData)
            .enter()
            .append('text')
            .attr('class', 'prefecture-label')
            .attr('x', d => d.x + d.width / 2)
            .attr('y', d => d.y + d.height / 2)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .style('font-size', '10px')
            .style('font-weight', 'bold')
            .style('fill', '#333333')
            .style('pointer-events', 'none')
            .text(d => this.getShortName(d.name));
        
        console.log('Map drawn with', mapData.length, 'prefectures');
    }
    
    getRegionClass(prefectureName) {
        const prefecture = this.prefecturesData.find(p => p.name === prefectureName);
        if (!prefecture) return 'unknown';
        
        const regionMap = {
            '北海道': 'hokkaido',
            '東北': 'tohoku',
            '関東': 'kanto',
            '中部': 'chubu',
            '近畿': 'kinki',
            '中国': 'chugoku',
            '四国': 'shikoku',
            '九州': 'kyushu',
            '沖縄': 'okinawa'
        };
        
        return regionMap[prefecture.region] || 'unknown';
    }
    
    getRegionColor(prefectureName) {
        const regionClass = this.getRegionClass(prefectureName);
        const colorMap = {
            'hokkaido': '#f0f0f0',
            'tohoku': '#e0e0e0',
            'kanto': '#d0d0d0',
            'chubu': '#c0c0c0',
            'kinki': '#b0b0b0',
            'chugoku': '#a0a0a0',
            'shikoku': '#909090',
            'kyushu': '#808080',
            'okinawa': '#707070',
            'unknown': '#cccccc'
        };
        return colorMap[regionClass] || '#cccccc';
    }
    
    getShortName(name) {
        return name.replace(/[都道府県]/g, '').substring(0, 2);
    }
    
    onPrefectureClick(prefectureData) {
        console.log('Click handler called for:', prefectureData.name);
        
        // 以前の選択を解除
        d3.selectAll('.prefecture').classed('selected', false);
        
        // 新しい選択を設定
        d3.selectAll('.prefecture').filter(d => d.name === prefectureData.name).classed('selected', true);
        
        this.selectedPrefecture = prefectureData.name;
        this.updateInfoPanel();
    }
    
    updateInfoPanel() {
        console.log('Updating info panel for:', this.selectedPrefecture);
        const prefecture = this.prefecturesData.find(p => p.name === this.selectedPrefecture);
        
        if (!prefecture) {
            console.log('Prefecture not found in data');
            return;
        }
        
        const infoHtml = `
            <div style="text-align: center; margin-bottom: 15px;">
                <h3 style="color: #2d3748; font-size: 1.5rem; margin-bottom: 5px;">${prefecture.name}</h3>
                <span style="background: #e2e8f0; padding: 4px 12px; border-radius: 15px; font-size: 0.9rem; color: #4a5568;">
                    ${prefecture.region}地方
                </span>
            </div>
            <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #4299e1;">
                <p><strong>都道府県コード:</strong> ${prefecture.code}</p>
                <p><strong>地域:</strong> ${prefecture.region}地方</p>
                <p style="margin-top: 10px; font-size: 0.9rem; color: #718096;">
                    シンプル版地図が動作中です！
                </p>
            </div>
        `;
        
        const infoElement = document.getElementById('prefecture-info');
        if (infoElement) {
            infoElement.innerHTML = infoHtml;
            console.log('Info panel updated successfully');
        } else {
            console.error('prefecture-info element not found');
        }
    }
    
    setupTooltip() {
        console.log('Setting up tooltip...');
        // ツールチップ要素を作成
        this.tooltip = d3.select('body')
            .append('div')
            .attr('class', 'tooltip')
            .style('position', 'absolute')
            .style('background', 'rgba(0,0,0,0.8)')
            .style('color', 'white')
            .style('padding', '8px')
            .style('border-radius', '4px')
            .style('pointer-events', 'none')
            .style('opacity', 0);
        console.log('Tooltip setup complete');
    }
    
    showTooltip(event, prefectureData) {
        const prefecture = this.prefecturesData.find(p => p.name === prefectureData.name);
        
        if (!prefecture) return;
        
        this.tooltip
            .style('opacity', 1)
            .html(`<strong>${prefecture.name}</strong><br/>${prefecture.region}地方`)
            .style('left', (event.pageX + 10) + 'px')
            .style('top', (event.pageY - 10) + 'px');
    }
    
    hideTooltip() {
        this.tooltip.style('opacity', 0);
    }
}

// ページ読み込み完了後に地図を初期化
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing Simple Working Map...');
    
    // D3.jsが読み込まれているかチェック
    if (typeof d3 === 'undefined') {
        console.error('D3.js is not loaded!');
        return;
    }
    
    // SVG要素が存在するかチェック
    const mapElement = document.getElementById('japan-map');
    if (!mapElement) {
        console.error('Map element (#japan-map) not found!');
        return;
    }
    
    console.log('All dependencies are ready, creating map...');
    new SimpleWorkingMap();
});