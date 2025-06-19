// 改善された日本地図表示 - SVG座標系での直接描画

class JapanMapFixed {
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
        const mapData = this.generateFixedJapanMap();
        
        console.log('Drawing map with', mapData.length, 'prefectures');
        
        // 都道府県を描画
        const prefectures = svg.selectAll('.prefecture')
            .data(mapData)
            .enter()
            .append('path')
            .attr('class', d => `prefecture ${this.getRegionClass(d.name)}`)
            .attr('d', d => d.path)
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
            .attr('x', d => d.labelX)
            .attr('y', d => d.labelY)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .style('font-size', '10px')
            .style('font-weight', 'bold')
            .style('fill', '#333333')
            .style('pointer-events', 'none')
            .text(d => this.getShortName(d.name));
        
        console.log('Map drawing complete');
    }
    
    generateFixedJapanMap() {
        // より適切な位置関係の日本地図データ（SVGパス形式）
        return [
            // 北海道
            { 
                name: '北海道', 
                path: 'M350,50 L480,50 L480,120 L350,120 Z',
                labelX: 415, labelY: 85
            },
            
            // 東北地方
            { 
                name: '青森県', 
                path: 'M380,130 L450,130 L450,160 L380,160 Z',
                labelX: 415, labelY: 145
            },
            { 
                name: '岩手県', 
                path: 'M450,130 L500,130 L500,200 L450,200 Z',
                labelX: 475, labelY: 165
            },
            { 
                name: '宮城県', 
                path: 'M420,170 L450,170 L450,200 L420,200 Z',
                labelX: 435, labelY: 185
            },
            { 
                name: '秋田県', 
                path: 'M350,140 L380,140 L380,190 L350,190 Z',
                labelX: 365, labelY: 165
            },
            { 
                name: '山形県', 
                path: 'M350,190 L380,190 L380,220 L350,220 Z',
                labelX: 365, labelY: 205
            },
            { 
                name: '福島県', 
                path: 'M380,200 L420,200 L420,240 L380,240 Z',
                labelX: 400, labelY: 220
            },
            
            // 関東地方
            { 
                name: '茨城県', 
                path: 'M450,200 L490,200 L490,230 L450,230 Z',
                labelX: 470, labelY: 215
            },
            { 
                name: '栃木県', 
                path: 'M420,240 L450,240 L450,270 L420,270 Z',
                labelX: 435, labelY: 255
            },
            { 
                name: '群馬県', 
                path: 'M380,240 L420,240 L420,270 L380,270 Z',
                labelX: 400, labelY: 255
            },
            { 
                name: '埼玉県', 
                path: 'M400,270 L430,270 L430,290 L400,290 Z',
                labelX: 415, labelY: 280
            },
            { 
                name: '千葉県', 
                path: 'M450,230 L490,230 L490,280 L450,280 Z',
                labelX: 470, labelY: 255
            },
            { 
                name: '東京都', 
                path: 'M430,270 L450,270 L450,290 L430,290 Z',
                labelX: 440, labelY: 280
            },
            { 
                name: '神奈川県', 
                path: 'M420,290 L460,290 L460,320 L420,320 Z',
                labelX: 440, labelY: 305
            },
            
            // 中部地方
            { 
                name: '新潟県', 
                path: 'M280,180 L350,180 L350,240 L280,240 Z',
                labelX: 315, labelY: 210
            },
            { 
                name: '富山県', 
                path: 'M280,240 L320,240 L320,270 L280,270 Z',
                labelX: 300, labelY: 255
            },
            { 
                name: '石川県', 
                path: 'M250,220 L280,220 L280,280 L250,280 Z',
                labelX: 265, labelY: 250
            },
            { 
                name: '福井県', 
                path: 'M250,280 L280,280 L280,310 L250,310 Z',
                labelX: 265, labelY: 295
            },
            { 
                name: '山梨県', 
                path: 'M360,270 L400,270 L400,300 L360,300 Z',
                labelX: 380, labelY: 285
            },
            { 
                name: '長野県', 
                path: 'M320,240 L360,240 L360,300 L320,300 Z',
                labelX: 340, labelY: 270
            },
            { 
                name: '岐阜県', 
                path: 'M280,270 L320,270 L320,320 L280,320 Z',
                labelX: 300, labelY: 295
            },
            { 
                name: '静岡県', 
                path: 'M360,300 L420,300 L420,340 L360,340 Z',
                labelX: 390, labelY: 320
            },
            { 
                name: '愛知県', 
                path: 'M320,320 L370,320 L370,360 L320,360 Z',
                labelX: 345, labelY: 340
            },
            
            // 近畿地方
            { 
                name: '三重県', 
                path: 'M280,320 L320,320 L320,380 L280,380 Z',
                labelX: 300, labelY: 350
            },
            { 
                name: '滋賀県', 
                path: 'M280,310 L310,310 L310,340 L280,340 Z',
                labelX: 295, labelY: 325
            },
            { 
                name: '京都府', 
                path: 'M250,310 L290,310 L290,340 L250,340 Z',
                labelX: 270, labelY: 325
            },
            { 
                name: '大阪府', 
                path: 'M250,340 L280,340 L280,370 L250,370 Z',
                labelX: 265, labelY: 355
            },
            { 
                name: '兵庫県', 
                path: 'M210,330 L250,330 L250,380 L210,380 Z',
                labelX: 230, labelY: 355
            },
            { 
                name: '奈良県', 
                path: 'M270,360 L300,360 L300,390 L270,390 Z',
                labelX: 285, labelY: 375
            },
            { 
                name: '和歌山県', 
                path: 'M240,370 L280,370 L280,420 L240,420 Z',
                labelX: 260, labelY: 395
            },
            
            // 中国地方
            { 
                name: '鳥取県', 
                path: 'M180,320 L220,320 L220,350 L180,350 Z',
                labelX: 200, labelY: 335
            },
            { 
                name: '島根県', 
                path: 'M120,340 L180,340 L180,370 L120,370 Z',
                labelX: 150, labelY: 355
            },
            { 
                name: '岡山県', 
                path: 'M180,350 L220,350 L220,380 L180,380 Z',
                labelX: 200, labelY: 365
            },
            { 
                name: '広島県', 
                path: 'M120,370 L180,370 L180,400 L120,400 Z',
                labelX: 150, labelY: 385
            },
            { 
                name: '山口県', 
                path: 'M100,400 L160,400 L160,430 L100,430 Z',
                labelX: 130, labelY: 415
            },
            
            // 四国地方
            { 
                name: '徳島県', 
                path: 'M200,420 L240,420 L240,450 L200,450 Z',
                labelX: 220, labelY: 435
            },
            { 
                name: '香川県', 
                path: 'M170,410 L200,410 L200,430 L170,430 Z',
                labelX: 185, labelY: 420
            },
            { 
                name: '愛媛県', 
                path: 'M130,420 L170,420 L170,460 L130,460 Z',
                labelX: 150, labelY: 440
            },
            { 
                name: '高知県', 
                path: 'M150,460 L220,460 L220,490 L150,490 Z',
                labelX: 185, labelY: 475
            },
            
            // 九州地方
            { 
                name: '福岡県', 
                path: 'M60,420 L100,420 L100,460 L60,460 Z',
                labelX: 80, labelY: 440
            },
            { 
                name: '佐賀県', 
                path: 'M40,450 L70,450 L70,480 L40,480 Z',
                labelX: 55, labelY: 465
            },
            { 
                name: '長崎県', 
                path: 'M10,440 L50,440 L50,490 L10,490 Z',
                labelX: 30, labelY: 465
            },
            { 
                name: '熊本県', 
                path: 'M50,480 L90,480 L90,520 L50,520 Z',
                labelX: 70, labelY: 500
            },
            { 
                name: '大分県', 
                path: 'M90,460 L130,460 L130,500 L90,500 Z',
                labelX: 110, labelY: 480
            },
            { 
                name: '宮崎県', 
                path: 'M90,500 L120,500 L120,550 L90,550 Z',
                labelX: 105, labelY: 525
            },
            { 
                name: '鹿児島県', 
                path: 'M60,520 L100,520 L100,570 L60,570 Z',
                labelX: 80, labelY: 545
            },
            
            // 沖縄県
            { 
                name: '沖縄県', 
                path: 'M20,540 L60,540 L60,570 L20,570 Z',
                labelX: 40, labelY: 555
            }
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
    console.log('Initializing Fixed Japan Map...');
    new JapanMapFixed();
});