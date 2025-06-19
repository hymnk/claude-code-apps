// TopoJSONを使用した本格的な日本地図

class TopoJSONJapanMap {
    constructor() {
        this.width = 800;
        this.height = 600;
        this.prefecturesData = [];
        this.selectedPrefecture = null;
        this.japanTopoData = null;
        
        this.init();
    }
    
    async init() {
        await this.loadPrefecturesData();
        await this.loadJapanTopoData();
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
    
    async loadJapanTopoData() {
        try {
            // 実際のプロジェクトでは外部のTopoJSONファイルを読み込みますが、
            // ここでは簡略化したデータを直接定義します
            this.japanTopoData = this.createSimplifiedJapanTopo();
            console.log('Japan topo data loaded');
        } catch (error) {
            console.error('日本地図データの読み込みに失敗しました:', error);
        }
    }
    
    createSimplifiedJapanTopo() {
        // 実際の日本地図に近い形状のGeoJSONデータ
        return {
            type: "FeatureCollection",
            features: [
                {
                    type: "Feature",
                    properties: { name: "北海道" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [140.5, 45.5], [143.0, 45.0], [145.5, 43.5], [145.0, 42.0], 
                            [143.5, 41.0], [141.5, 41.5], [139.5, 43.0], [140.0, 45.0], [140.5, 45.5]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "青森県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [140.0, 41.5], [141.5, 41.0], [141.0, 40.0], [140.0, 40.2], [140.0, 41.5]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "岩手県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [141.0, 40.0], [142.0, 39.8], [142.0, 38.5], [141.0, 38.8], [140.5, 39.5], [141.0, 40.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "宮城県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [140.5, 38.8], [141.5, 38.5], [141.0, 37.8], [140.5, 38.0], [140.5, 38.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "秋田県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [139.8, 40.0], [140.5, 39.8], [140.2, 39.0], [139.5, 39.2], [139.8, 40.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "山形県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [139.5, 39.0], [140.2, 38.8], [140.0, 38.0], [139.3, 38.2], [139.5, 39.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "福島県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [139.3, 37.8], [140.8, 37.5], [140.5, 36.8], [139.0, 37.0], [139.3, 37.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "茨城県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [140.0, 36.8], [140.8, 36.5], [140.5, 35.8], [139.8, 36.0], [140.0, 36.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "栃木県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [139.3, 36.8], [140.0, 36.5], [139.8, 36.0], [139.0, 36.2], [139.3, 36.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "群馬県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [138.5, 36.8], [139.3, 36.5], [139.0, 36.0], [138.3, 36.2], [138.5, 36.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "埼玉県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [138.8, 36.0], [139.8, 35.8], [139.5, 35.5], [138.5, 35.7], [138.8, 36.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "千葉県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [139.8, 35.8], [140.8, 35.5], [140.5, 35.0], [140.0, 34.8], [139.5, 35.2], [139.8, 35.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "東京都" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [139.3, 35.7], [139.8, 35.5], [139.5, 35.2], [139.0, 35.4], [139.3, 35.7]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "神奈川県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [139.0, 35.4], [139.8, 35.2], [139.5, 34.8], [138.8, 35.0], [139.0, 35.4]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "新潟県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [137.5, 38.0], [139.0, 37.8], [138.8, 37.0], [137.0, 37.2], [137.5, 38.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "富山県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [136.8, 36.8], [137.8, 36.5], [137.5, 36.2], [136.5, 36.4], [136.8, 36.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "石川県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [136.0, 37.5], [137.0, 37.2], [136.8, 36.2], [135.8, 36.0], [135.5, 37.0], [136.0, 37.5]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "福井県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [135.8, 36.0], [136.5, 35.8], [136.2, 35.4], [135.5, 35.6], [135.8, 36.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "山梨県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [138.3, 35.8], [139.0, 35.5], [138.8, 35.2], [138.0, 35.4], [138.3, 35.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "長野県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [137.5, 36.5], [138.5, 36.2], [138.3, 35.4], [137.0, 35.6], [137.5, 36.5]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "岐阜県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [136.5, 36.0], [137.5, 35.8], [137.2, 35.2], [136.0, 35.4], [136.5, 36.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "静岡県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [137.8, 35.2], [139.0, 35.0], [138.5, 34.6], [137.5, 34.8], [137.8, 35.2]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "愛知県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [136.5, 35.2], [137.8, 35.0], [137.5, 34.6], [136.2, 34.8], [136.5, 35.2]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "三重県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [135.8, 35.0], [136.8, 34.8], [136.5, 34.2], [135.5, 34.4], [135.8, 35.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "滋賀県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [135.5, 35.4], [136.2, 35.2], [136.0, 34.8], [135.2, 35.0], [135.5, 35.4]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "京都府" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [135.0, 35.6], [136.0, 35.4], [135.8, 35.0], [134.8, 35.2], [135.0, 35.6]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "大阪府" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [135.0, 34.8], [135.8, 34.6], [135.6, 34.3], [134.8, 34.5], [135.0, 34.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "兵庫県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [134.2, 35.2], [135.2, 35.0], [135.0, 34.4], [134.0, 34.6], [134.2, 35.2]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "奈良県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [135.2, 34.6], [136.0, 34.4], [135.8, 34.0], [135.0, 34.2], [135.2, 34.6]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "和歌山県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [135.0, 34.2], [135.8, 34.0], [135.5, 33.4], [134.8, 33.6], [135.0, 34.2]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "鳥取県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [133.5, 35.4], [134.5, 35.2], [134.2, 34.8], [133.2, 35.0], [133.5, 35.4]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "島根県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [131.8, 35.2], [133.5, 35.0], [133.2, 34.6], [131.5, 34.8], [131.8, 35.2]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "岡山県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [133.2, 34.8], [134.2, 34.6], [134.0, 34.2], [133.0, 34.4], [133.2, 34.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "広島県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [132.0, 34.6], [133.2, 34.4], [133.0, 34.0], [131.8, 34.2], [132.0, 34.6]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "山口県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [130.8, 34.4], [132.0, 34.2], [131.8, 33.8], [130.5, 34.0], [130.8, 34.4]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "徳島県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [133.8, 34.0], [134.6, 33.8], [134.4, 33.4], [133.6, 33.6], [133.8, 34.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "香川県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [133.5, 34.2], [134.2, 34.0], [134.0, 33.8], [133.3, 34.0], [133.5, 34.2]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "愛媛県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [132.2, 33.8], [133.5, 33.6], [133.3, 33.0], [132.0, 33.2], [132.2, 33.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "高知県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [132.8, 33.4], [134.0, 33.2], [133.8, 32.8], [132.6, 33.0], [132.8, 33.4]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "福岡県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [130.0, 33.8], [131.0, 33.6], [130.8, 33.2], [129.8, 33.4], [130.0, 33.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "佐賀県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [129.5, 33.4], [130.2, 33.2], [130.0, 32.8], [129.3, 33.0], [129.5, 33.4]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "長崎県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [129.0, 33.2], [130.0, 33.0], [129.8, 32.4], [128.8, 32.6], [129.0, 33.2]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "熊本県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [130.2, 32.8], [131.2, 32.6], [131.0, 32.2], [130.0, 32.4], [130.2, 32.8]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "大分県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [131.0, 33.4], [132.0, 33.2], [131.8, 32.8], [130.8, 33.0], [131.0, 33.4]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "宮崎県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [131.0, 32.4], [131.8, 32.2], [131.6, 31.4], [130.8, 31.6], [131.0, 32.4]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "鹿児島県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [129.8, 32.0], [131.2, 31.8], [131.0, 30.8], [129.6, 31.0], [129.8, 32.0]
                        ]]
                    }
                },
                {
                    type: "Feature",
                    properties: { name: "沖縄県" },
                    geometry: {
                        type: "Polygon",
                        coordinates: [[
                            [127.0, 26.5], [128.5, 26.3], [128.3, 25.8], [126.8, 26.0], [127.0, 26.5]
                        ]]
                    }
                }
            ]
        };
    }
    
    setupMap() {
        const svg = d3.select('#japan-map')
            .attr('width', this.width)
            .attr('height', this.height)
            .attr('viewBox', `0 0 ${this.width} ${this.height}`);
        
        // 地理的境界を設定（日本の経度・緯度範囲）
        const bounds = [[125, 24], [146, 46]]; // [西端, 南端], [東端, 北端]
        
        // Mercator投影法を設定
        this.projection = d3.geoMercator()
            .fitSize([this.width * 0.8, this.height * 0.8], this.japanTopoData)
            .translate([this.width / 2, this.height / 2]);
            
        this.path = d3.geoPath().projection(this.projection);
        
        console.log('Map projection setup complete');
    }
    
    drawMap() {
        const svg = d3.select('#japan-map');
        
        console.log('Drawing map with', this.japanTopoData.features.length, 'prefectures');
        
        // 都道府県を描画
        const prefectures = svg.selectAll('.prefecture')
            .data(this.japanTopoData.features)
            .enter()
            .append('path')
            .attr('class', d => `prefecture ${this.getRegionClass(d.properties.name)}`)
            .attr('d', this.path)
            .attr('stroke', '#ffffff')
            .attr('stroke-width', 1)
            .style('cursor', 'pointer')
            .on('click', (event, d) => {
                console.log('Prefecture clicked:', d.properties.name);
                this.onPrefectureClick(d);
            })
            .on('mouseover', (event, d) => this.showTooltip(event, d))
            .on('mouseout', () => this.hideTooltip());
        
        // 都道府県名ラベルを追加
        const labels = svg.selectAll('.prefecture-label')
            .data(this.japanTopoData.features)
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
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .style('font-size', '9px')
            .style('font-weight', 'bold')
            .style('fill', '#333333')
            .style('pointer-events', 'none')
            .text(d => this.getShortName(d.properties.name));
        
        console.log('Map drawing complete');
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
        d3.selectAll('.prefecture').filter(d => d.properties.name === prefectureData.properties.name).classed('selected', true);
        
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
                    D3.js + 地理データによる正確な形状表示！
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
    console.log('Initializing TopoJSON Japan Map...');
    new TopoJSONJapanMap();
});