// シンプルな日本地図 - D3.js地理投影を使わない直接SVG描画

class SimpleJapanMap {
    constructor() {
        this.width = 800;
        this.height = 600;
        this.prefecturesData = [];
        this.selectedPrefecture = null;
        
        this.init();
    }
    
    async init() {
        await this.loadPrefecturesData();
        this.setupMap();
        this.drawMap();
        this.setupTooltip();
    }
    
    async loadPrefecturesData() {
        try {
            const response = await fetch('/api/prefectures');
            this.prefecturesData = await response.json();
            console.log('Loaded prefecture data:', this.prefecturesData.length);
        } catch (error) {
            console.error('都道府県データの読み込みに失敗しました:', error);
        }
    }
    
    setupMap() {
        const svg = d3.select('#japan-map')
            .attr('width', this.width)
            .attr('height', this.height)
            .attr('viewBox', `0 0 ${this.width} ${this.height}`);
        
        console.log('Map setup complete');
    }
    
    drawMap() {
        const svg = d3.select('#japan-map');
        const mapData = this.generateGridBasedMap();
        
        console.log('Drawing map with', mapData.length, 'prefectures');
        
        // 都道府県を矩形で描画
        const prefectures = svg.selectAll('.prefecture')
            .data(mapData)
            .enter()
            .append('rect')
            .attr('class', d => `prefecture ${this.getRegionClass(d.name)}`)
            .attr('x', d => d.x)
            .attr('y', d => d.y)
            .attr('width', d => d.width)
            .attr('height', d => d.height)
            .attr('stroke', '#ffffff')
            .attr('stroke-width', 2)
            .style('cursor', 'pointer')
            .on('click', (event, d) => {
                console.log('Prefecture clicked:', d.name);
                this.onPrefectureClick(d);
            })
            .on('mouseover', (event, d) => this.showTooltip(event, d))
            .on('mouseout', () => this.hideTooltip());
        
        // 都道府県名ラベルを追加
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
            .style('fill', '#ffffff')
            .style('pointer-events', 'none')
            .text(d => this.getShortName(d.name));
        
        console.log('Map drawing complete');
    }
    
    generateGridBasedMap() {
        // グリッドベースの簡略化日本地図レイアウト
        const gridWidth = 100;
        const gridHeight = 60;
        const startX = 50;
        const startY = 50;
        
        return [
            // 北海道 (大きく上部中央)
            { name: '北海道', x: startX + gridWidth * 3, y: startY, width: gridWidth * 2, height: gridHeight, region: '北海道' },
            
            // 東北 (北海道の下)
            { name: '青森県', x: startX + gridWidth * 3, y: startY + gridHeight, width: gridWidth, height: gridHeight, region: '東北' },
            { name: '秋田県', x: startX + gridWidth * 2, y: startY + gridHeight * 1.5, width: gridWidth, height: gridHeight, region: '東北' },
            { name: '岩手県', x: startX + gridWidth * 4, y: startY + gridHeight * 1.5, width: gridWidth, height: gridHeight, region: '東北' },
            { name: '山形県', x: startX + gridWidth * 2, y: startY + gridHeight * 2.5, width: gridWidth, height: gridHeight, region: '東北' },
            { name: '宮城県', x: startX + gridWidth * 3, y: startY + gridHeight * 2.5, width: gridWidth, height: gridHeight, region: '東北' },
            { name: '福島県', x: startX + gridWidth * 3, y: startY + gridHeight * 3.5, width: gridWidth, height: gridHeight, region: '東北' },
            
            // 関東 (東北の下と右)
            { name: '茨城県', x: startX + gridWidth * 4, y: startY + gridHeight * 3.5, width: gridWidth, height: gridHeight, region: '関東' },
            { name: '栃木県', x: startX + gridWidth * 3, y: startY + gridHeight * 4, width: gridWidth, height: gridHeight * 0.7, region: '関東' },
            { name: '群馬県', x: startX + gridWidth * 2, y: startY + gridHeight * 4, width: gridWidth, height: gridHeight * 0.7, region: '関東' },
            { name: '埼玉県', x: startX + gridWidth * 2.5, y: startY + gridHeight * 4.7, width: gridWidth * 0.8, height: gridHeight * 0.6, region: '関東' },
            { name: '東京都', x: startX + gridWidth * 3.3, y: startY + gridHeight * 4.7, width: gridWidth * 0.7, height: gridHeight * 0.6, region: '関東' },
            { name: '千葉県', x: startX + gridWidth * 4, y: startY + gridHeight * 4.5, width: gridWidth, height: gridHeight * 0.8, region: '関東' },
            { name: '神奈川県', x: startX + gridWidth * 3, y: startY + gridHeight * 5.3, width: gridWidth, height: gridHeight * 0.7, region: '関東' },
            
            // 中部 (関東の左と下)
            { name: '新潟県', x: startX + gridWidth * 1, y: startY + gridHeight * 2, width: gridWidth, height: gridHeight * 1.5, region: '中部' },
            { name: '富山県', x: startX + gridWidth * 1, y: startY + gridHeight * 3.5, width: gridWidth * 0.8, height: gridHeight * 0.6, region: '中部' },
            { name: '石川県', x: startX + gridWidth * 0.5, y: startY + gridHeight * 3, width: gridWidth * 0.7, height: gridHeight * 1.2, region: '中部' },
            { name: '福井県', x: startX + gridWidth * 1, y: startY + gridHeight * 4.1, width: gridWidth * 0.8, height: gridHeight * 0.6, region: '中部' },
            { name: '山梨県', x: startX + gridWidth * 2, y: startY + gridHeight * 4.7, width: gridWidth * 0.8, height: gridWidth * 0.6, region: '中部' },
            { name: '長野県', x: startX + gridWidth * 1.8, y: startY + gridHeight * 3.8, width: gridWidth * 0.9, height: gridHeight * 0.9, region: '中部' },
            { name: '岐阜県', x: startX + gridWidth * 1.5, y: startY + gridHeight * 4.7, width: gridWidth * 0.9, height: gridHeight * 0.8, region: '中部' },
            { name: '静岡県', x: startX + gridWidth * 2.3, y: startY + gridHeight * 5.5, width: gridWidth * 1.2, height: gridHeight * 0.7, region: '中部' },
            { name: '愛知県', x: startX + gridWidth * 1.8, y: startY + gridHeight * 5.5, width: gridWidth * 0.9, height: gridHeight * 0.7, region: '中部' },
            
            // 近畿 (中部の右下)
            { name: '三重県', x: startX + gridWidth * 1.3, y: startY + gridHeight * 6.2, width: gridWidth * 0.7, height: gridHeight * 0.8, region: '近畿' },
            { name: '滋賀県', x: startX + gridWidth * 1.8, y: startY + gridHeight * 6.2, width: gridWidth * 0.6, height: gridHeight * 0.6, region: '近畿' },
            { name: '京都府', x: startX + gridWidth * 2.2, y: startY + gridHeight * 6, width: gridWidth * 0.8, height: gridHeight * 0.7, region: '近畿' },
            { name: '大阪府', x: startX + gridWidth * 2, y: startY + gridHeight * 6.7, width: gridWidth * 0.6, height: gridHeight * 0.5, region: '近畿' },
            { name: '兵庫県', x: startX + gridWidth * 1.2, y: startY + gridHeight * 6.8, width: gridWidth * 1.1, height: gridHeight * 0.7, region: '近畿' },
            { name: '奈良県', x: startX + gridWidth * 2.4, y: startY + gridHeight * 6.7, width: gridWidth * 0.6, height: gridHeight * 0.6, region: '近畿' },
            { name: '和歌山県', x: startX + gridWidth * 2, y: startY + gridHeight * 7.2, width: gridWidth * 0.8, height: gridHeight * 0.8, region: '近畿' },
            
            // 中国 (近畿の左)
            { name: '鳥取県', x: startX + gridWidth * 0.8, y: startY + gridHeight * 6, width: gridWidth * 0.9, height: gridHeight * 0.5, region: '中国' },
            { name: '島根県', x: startX + gridWidth * 0.2, y: startY + gridHeight * 6.2, width: gridWidth * 1.2, height: gridHeight * 0.6, region: '中国' },
            { name: '岡山県', x: startX + gridWidth * 0.8, y: startY + gridHeight * 6.5, width: gridWidth * 0.9, height: gridHeight * 0.6, region: '中国' },
            { name: '広島県', x: startX + gridWidth * 0.2, y: startY + gridHeight * 6.8, width: gridWidth * 1.1, height: gridHeight * 0.6, region: '中国' },
            { name: '山口県', x: startX + gridWidth * 0, y: startY + gridHeight * 7.4, width: gridWidth * 1.2, height: gridHeight * 0.6, region: '中国' },
            
            // 四国 (中国の下)
            { name: '徳島県', x: startX + gridWidth * 1.5, y: startY + gridHeight * 8, width: gridWidth * 0.7, height: gridHeight * 0.5, region: '四国' },
            { name: '香川県', x: startX + gridWidth * 0.8, y: startY + gridHeight * 7.8, width: gridWidth * 0.7, height: gridHeight * 0.4, region: '四国' },
            { name: '愛媛県', x: startX + gridWidth * 0.2, y: startY + gridHeight * 8, width: gridWidth * 0.9, height: gridHeight * 0.6, region: '四国' },
            { name: '高知県', x: startX + gridWidth * 0.5, y: startY + gridHeight * 8.6, width: gridWidth * 1.2, height: gridHeight * 0.5, region: '四国' },
            
            // 九州 (左下)
            { name: '福岡県', x: startX + gridWidth * -1, y: startY + gridHeight * 7.5, width: gridWidth * 0.9, height: gridHeight * 0.8, region: '九州' },
            { name: '佐賀県', x: startX + gridWidth * -1.5, y: startY + gridHeight * 8, width: gridWidth * 0.7, height: gridHeight * 0.6, region: '九州' },
            { name: '長崎県', x: startX + gridWidth * -2.2, y: startY + gridHeight * 7.8, width: gridWidth * 0.8, height: gridHeight * 1, region: '九州' },
            { name: '熊本県', x: startX + gridWidth * -1.3, y: startY + gridHeight * 8.6, width: gridWidth * 0.9, height: gridHeight * 0.8, region: '九州' },
            { name: '大分県', x: startX + gridWidth * -0.3, y: startY + gridHeight * 8.2, width: gridWidth * 0.8, height: gridHeight * 0.7, region: '九州' },
            { name: '宮崎県', x: startX + gridWidth * -0.5, y: startY + gridHeight * 8.9, width: gridWidth * 0.7, height: gridHeight * 0.9, region: '九州' },
            { name: '鹿児島県', x: startX + gridWidth * -1.2, y: startY + gridHeight * 9.4, width: gridWidth * 0.9, height: gridHeight * 1, region: '九州' },
            
            // 沖縄 (左下隅)
            { name: '沖縄県', x: startX + gridWidth * -2.5, y: startY + gridHeight * 10, width: gridWidth * 0.8, height: gridHeight * 0.6, region: '沖縄' }
        ];
    }
    
    getRegionClass(prefectureName) {
        const prefecture = this.prefecturesData.find(p => p.name === prefectureName);
        if (!prefecture) return '';
        
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
        
        return regionMap[prefecture.region] || '';
    }
    
    getShortName(name) {
        return name.replace(/[都道府県]/g, '').substring(0, 2);
    }
    
    onPrefectureClick(prefectureData) {
        // 以前の選択を解除
        d3.selectAll('.prefecture').classed('selected', false);
        
        // 新しい選択を設定
        d3.selectAll('.prefecture').filter(d => d.name === prefectureData.name).classed('selected', true);
        
        this.selectedPrefecture = prefectureData.name;
        this.updateInfoPanel();
    }
    
    updateInfoPanel() {
        const prefecture = this.prefecturesData.find(p => p.name === this.selectedPrefecture);
        
        if (!prefecture) return;
        
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
                    クリック機能が正常に動作しています！
                </p>
            </div>
        `;
        
        document.getElementById('prefecture-info').innerHTML = infoHtml;
    }
    
    setupTooltip() {
        // ツールチップ要素を作成
        this.tooltip = d3.select('body')
            .append('div')
            .attr('class', 'tooltip');
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
    console.log('Initializing Simple Japan Map...');
    new SimpleJapanMap();
});