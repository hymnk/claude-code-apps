// 日本地図インタラクティブ機能

class JapanMapViewer {
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
        } catch (error) {
            console.error('都道府県データの読み込みに失敗しました:', error);
        }
    }
    
    setupMap() {
        const svg = d3.select('#japan-map')
            .attr('width', this.width)
            .attr('height', this.height);
            
        // 座標の範囲を計算して適切にフィット
        const bounds = [[127, 25], [146, 46]]; // [西端, 南端], [東端, 北端]
        
        this.projection = d3.geoMercator()
            .fitSize([this.width * 0.9, this.height * 0.9], {
                type: "Polygon",
                coordinates: [[
                    [bounds[0][0], bounds[0][1]],
                    [bounds[1][0], bounds[0][1]], 
                    [bounds[1][0], bounds[1][1]],
                    [bounds[0][0], bounds[1][1]],
                    [bounds[0][0], bounds[0][1]]
                ]]
            })
            .translate([this.width / 2, this.height / 2]);
            
        this.path = d3.geoPath().projection(this.projection);
        
        // デバッグ用：投影法の設定を確認
        console.log('Map projection center:', this.projection.center());
        console.log('Map projection scale:', this.projection.scale());
    }
    
    drawMap() {
        // 簡略化された日本地図データ（実際のプロジェクトではTopoJSONを使用）
        const japanData = this.generateSimplifiedJapanMap();
        console.log('Generated map data features:', japanData.features.length);
        
        const svg = d3.select('#japan-map');
        
        // デバッグ：最初のいくつかの都道府県の座標をチェック
        japanData.features.slice(0, 5).forEach(feature => {
            const coords = feature.geometry.coordinates[0];
            const centroid = this.path.centroid(feature);
            console.log(`${feature.properties.name}: coords=${coords[0]}, centroid=${centroid}`);
        });
        
        // 都道府県パスを描画
        const paths = svg.selectAll('.prefecture')
            .data(japanData.features)
            .enter()
            .append('path')
            .attr('class', d => `prefecture ${this.getRegionClass(d.properties.name)}`)
            .attr('d', this.path)
            .on('click', (event, d) => {
                console.log('Prefecture clicked:', d.properties.name);
                this.onPrefectureClick(d);
            })
            .on('mouseover', (event, d) => this.showTooltip(event, d))
            .on('mouseout', () => this.hideTooltip());
            
        console.log('Drew', paths.size(), 'prefecture paths');
            
        // 都道府県名ラベルを追加
        const labels = svg.selectAll('.prefecture-label')
            .data(japanData.features)
            .enter()
            .append('text')
            .attr('class', 'prefecture-label')
            .attr('x', d => {
                const centroid = this.path.centroid(d);
                return isNaN(centroid[0]) ? 0 : centroid[0];
            })
            .attr('y', d => {
                const centroid = this.path.centroid(d);
                return isNaN(centroid[1]) ? 0 : centroid[1];
            })
            .text(d => this.getShortName(d.properties.name));
            
        console.log('Drew', labels.size(), 'prefecture labels');
    }
    
    generateSimplifiedJapanMap() {
        // 簡略化されたボックス型の日本地図データ（グリッド配置）
        const features = [
            // 北海道エリア（上部大きく）
            { type: 'Feature', properties: { name: '北海道' }, 
              geometry: { type: 'Polygon', coordinates: [[[130, 40], [142, 40], [142, 46], [130, 46], [130, 40]]] }},
            
            // 東北エリア（縦に配置）
            { type: 'Feature', properties: { name: '青森県' }, 
              geometry: { type: 'Polygon', coordinates: [[[139, 38.5], [142, 38.5], [142, 40], [139, 40], [139, 38.5]]] }},
            { type: 'Feature', properties: { name: '岩手県' }, 
              geometry: { type: 'Polygon', coordinates: [[[140, 36.5], [142, 36.5], [142, 38.5], [140, 38.5], [140, 36.5]]] }},
            { type: 'Feature', properties: { name: '宮城県' }, 
              geometry: { type: 'Polygon', coordinates: [[[139, 36.5], [140, 36.5], [140, 37.5], [139, 37.5], [139, 36.5]]] }},
            { type: 'Feature', properties: { name: '秋田県' }, 
              geometry: { type: 'Polygon', coordinates: [[[138, 37.5], [139, 37.5], [139, 39], [138, 39], [138, 37.5]]] }},
            { type: 'Feature', properties: { name: '山形県' }, 
              geometry: { type: 'Polygon', coordinates: [[[138, 36.5], [139, 36.5], [139, 37.5], [138, 37.5], [138, 36.5]]] }},
            { type: 'Feature', properties: { name: '福島県' }, 
              geometry: { type: 'Polygon', coordinates: [[[139, 35], [141, 35], [141, 36.5], [139, 36.5], [139, 35]]] }},
            
            // 関東エリア（中央上部）
            { type: 'Feature', properties: { name: '茨城県' }, 
              geometry: { type: 'Polygon', coordinates: [[[140, 35], [141, 35], [141, 36.5], [140, 36.5], [140, 35]]] }},
            { type: 'Feature', properties: { name: '栃木県' }, 
              geometry: { type: 'Polygon', coordinates: [[[139, 35.5], [140, 35.5], [140, 36.5], [139, 36.5], [139, 35.5]]] }},
            { type: 'Feature', properties: { name: '群馬県' }, 
              geometry: { type: 'Polygon', coordinates: [[[138, 35.5], [139, 35.5], [139, 36.5], [138, 36.5], [138, 35.5]]] }},
            { type: 'Feature', properties: { name: '埼玉県' }, 
              geometry: { type: 'Polygon', coordinates: [[[138.5, 35], [139.5, 35], [139.5, 35.5], [138.5, 35.5], [138.5, 35]]] }},
            { type: 'Feature', properties: { name: '千葉県' }, 
              geometry: { type: 'Polygon', coordinates: [[[139.5, 35], [140.8, 35], [140.8, 35.8], [139.5, 35.8], [139.5, 35]]] }},
            { type: 'Feature', properties: { name: '東京都' }, 
              geometry: { type: 'Polygon', coordinates: [[[139, 35], [139.5, 35], [139.5, 35.5], [139, 35.5], [139, 35]]] }},
            { type: 'Feature', properties: { name: '神奈川県' }, 
              geometry: { type: 'Polygon', coordinates: [[[139, 34.5], [140, 34.5], [140, 35], [139, 35], [139, 34.5]]] }},
            
            // 中部エリア（中央左）
            { type: 'Feature', properties: { name: '新潟県' }, 
              geometry: { type: 'Polygon', coordinates: [[[137, 36.5], [139, 36.5], [139, 38], [137, 38], [137, 36.5]]] }},
            { type: 'Feature', properties: { name: '富山県' }, 
              geometry: { type: 'Polygon', coordinates: [[[136, 36], [137.5, 36], [137.5, 36.8], [136, 36.8], [136, 36]]] }},
            { type: 'Feature', properties: { name: '石川県' }, 
              geometry: { type: 'Polygon', coordinates: [[[135.5, 36], [136.5, 36], [136.5, 37.5], [135.5, 37.5], [135.5, 36]]] }},
            { type: 'Feature', properties: { name: '福井県' }, 
              geometry: { type: 'Polygon', coordinates: [[[135.5, 35.2], [136.5, 35.2], [136.5, 36], [135.5, 36], [135.5, 35.2]]] }},
            { type: 'Feature', properties: { name: '山梨県' }, 
              geometry: { type: 'Polygon', coordinates: [[[138, 35], [139, 35], [139, 35.5], [138, 35.5], [138, 35]]] }},
            { type: 'Feature', properties: { name: '長野県' }, 
              geometry: { type: 'Polygon', coordinates: [[[137, 35], [138.5, 35], [138.5, 36.5], [137, 36.5], [137, 35]]] }},
            { type: 'Feature', properties: { name: '岐阜県' }, 
              geometry: { type: 'Polygon', coordinates: [[[136, 35], [137.5, 35], [137.5, 36], [136, 36], [136, 35]]] }},
            { type: 'Feature', properties: { name: '静岡県' }, 
              geometry: { type: 'Polygon', coordinates: [[[137.5, 34.2], [139, 34.2], [139, 35], [137.5, 35], [137.5, 34.2]]] }},
            { type: 'Feature', properties: { name: '愛知県' }, 
              geometry: { type: 'Polygon', coordinates: [[[136, 34.2], [137.5, 34.2], [137.5, 35.2], [136, 35.2], [136, 34.2]]] }},
            
            // 近畿エリア（中央下）
            { type: 'Feature', properties: { name: '三重県' }, 
              geometry: { type: 'Polygon', coordinates: [[[135.5, 33.5], [136.5, 33.5], [136.5, 34.5], [135.5, 34.5], [135.5, 33.5]]] }},
            { type: 'Feature', properties: { name: '滋賀県' }, 
              geometry: { type: 'Polygon', coordinates: [[[135, 34.5], [136, 34.5], [136, 35.2], [135, 35.2], [135, 34.5]]] }},
            { type: 'Feature', properties: { name: '京都府' }, 
              geometry: { type: 'Polygon', coordinates: [[[134.5, 34.8], [135.8, 34.8], [135.8, 35.8], [134.5, 35.8], [134.5, 34.8]]] }},
            { type: 'Feature', properties: { name: '大阪府' }, 
              geometry: { type: 'Polygon', coordinates: [[[135, 34], [135.8, 34], [135.8, 34.8], [135, 34.8], [135, 34]]] }},
            { type: 'Feature', properties: { name: '兵庫県' }, 
              geometry: { type: 'Polygon', coordinates: [[[134, 34], [135.5, 34], [135.5, 35.2], [134, 35.2], [134, 34]]] }},
            { type: 'Feature', properties: { name: '奈良県' }, 
              geometry: { type: 'Polygon', coordinates: [[[135, 33.5], [136, 33.5], [136, 34.5], [135, 34.5], [135, 33.5]]] }},
            { type: 'Feature', properties: { name: '和歌山県' }, 
              geometry: { type: 'Polygon', coordinates: [[[134.5, 33], [135.8, 33], [135.8, 34], [134.5, 34], [134.5, 33]]] }},
            
            // 中国地方（左下）
            { type: 'Feature', properties: { name: '鳥取県' }, 
              geometry: { type: 'Polygon', coordinates: [[[133, 35], [134.5, 35], [134.5, 35.8], [133, 35.8], [133, 35]]] }},
            { type: 'Feature', properties: { name: '島根県' }, 
              geometry: { type: 'Polygon', coordinates: [[[131, 34.5], [133.5, 34.5], [133.5, 35.5], [131, 35.5], [131, 34.5]]] }},
            { type: 'Feature', properties: { name: '岡山県' }, 
              geometry: { type: 'Polygon', coordinates: [[[133, 34], [134.5, 34], [134.5, 35], [133, 35], [133, 34]]] }},
            { type: 'Feature', properties: { name: '広島県' }, 
              geometry: { type: 'Polygon', coordinates: [[[131.5, 34], [133.5, 34], [133.5, 34.8], [131.5, 34.8], [131.5, 34]]] }},
            { type: 'Feature', properties: { name: '山口県' }, 
              geometry: { type: 'Polygon', coordinates: [[[130, 33.5], [132, 33.5], [132, 34.5], [130, 34.5], [130, 33.5]]] }},
            
            // 四国地方（下中央）
            { type: 'Feature', properties: { name: '徳島県' }, 
              geometry: { type: 'Polygon', coordinates: [[[133.5, 33], [134.8, 33], [134.8, 34], [133.5, 34], [133.5, 33]]] }},
            { type: 'Feature', properties: { name: '香川県' }, 
              geometry: { type: 'Polygon', coordinates: [[[133, 33.5], [134.5, 33.5], [134.5, 34], [133, 34], [133, 33.5]]] }},
            { type: 'Feature', properties: { name: '愛媛県' }, 
              geometry: { type: 'Polygon', coordinates: [[[131.5, 32.8], [133.5, 32.8], [133.5, 33.8], [131.5, 33.8], [131.5, 32.8]]] }},
            { type: 'Feature', properties: { name: '高知県' }, 
              geometry: { type: 'Polygon', coordinates: [[[132, 32], [134.5, 32], [134.5, 33], [132, 33], [132, 32]]] }},
            
            // 九州地方（左下）
            { type: 'Feature', properties: { name: '福岡県' }, 
              geometry: { type: 'Polygon', coordinates: [[[129.5, 33], [131, 33], [131, 34], [129.5, 34], [129.5, 33]]] }},
            { type: 'Feature', properties: { name: '佐賀県' }, 
              geometry: { type: 'Polygon', coordinates: [[[129, 32.5], [130.5, 32.5], [130.5, 33.5], [129, 33.5], [129, 32.5]]] }},
            { type: 'Feature', properties: { name: '長崎県' }, 
              geometry: { type: 'Polygon', coordinates: [[[128, 32], [129.8, 32], [129.8, 33.5], [128, 33.5], [128, 32]]] }},
            { type: 'Feature', properties: { name: '熊本県' }, 
              geometry: { type: 'Polygon', coordinates: [[[129.5, 31.5], [131, 31.5], [131, 33], [129.5, 33], [129.5, 31.5]]] }},
            { type: 'Feature', properties: { name: '大分県' }, 
              geometry: { type: 'Polygon', coordinates: [[[130.5, 32.5], [132, 32.5], [132, 33.8], [130.5, 33.8], [130.5, 32.5]]] }},
            { type: 'Feature', properties: { name: '宮崎県' }, 
              geometry: { type: 'Polygon', coordinates: [[[130.5, 30.5], [131.8, 30.5], [131.8, 32.5], [130.5, 32.5], [130.5, 30.5]]] }},
            { type: 'Feature', properties: { name: '鹿児島県' }, 
              geometry: { type: 'Polygon', coordinates: [[[129, 29.5], [131.5, 29.5], [131.5, 31.8], [129, 31.8], [129, 29.5]]] }},
            
            // 沖縄県（左下隅）
            { type: 'Feature', properties: { name: '沖縄県' }, 
              geometry: { type: 'Polygon', coordinates: [[[127, 25], [129, 25], [129, 27], [127, 27], [127, 25]]] }}
        ];
        
        return { type: 'FeatureCollection', features: features };
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
        d3.select(event.target).classed('selected', true);
        
        this.selectedPrefecture = prefectureData.properties.name;
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
                    この都道府県の詳細情報は今後追加予定です。
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
        const prefecture = this.prefecturesData.find(p => p.name === prefectureData.properties.name);
        
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
    new JapanMapViewer();
});