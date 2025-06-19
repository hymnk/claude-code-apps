// より現実に近い形状の日本地図

class RealisticJapanMap {
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
        const mapData = this.generateRealisticJapanMap();
        
        console.log('Drawing map with', mapData.length, 'prefectures');
        
        // 都道府県を描画
        const prefectures = svg.selectAll('.prefecture')
            .data(mapData)
            .enter()
            .append('path')
            .attr('class', d => `prefecture ${this.getRegionClass(d.name)}`)
            .attr('d', d => d.path)
            .attr('stroke', '#ffffff')
            .attr('stroke-width', 1.5)
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
            .style('font-size', '9px')
            .style('font-weight', 'bold')
            .style('fill', '#333333')
            .style('pointer-events', 'none')
            .text(d => this.getShortName(d.name));
        
        console.log('Map drawing complete');
    }
    
    generateRealisticJapanMap() {
        // より現実的な形状の日本地図データ
        return [
            // 北海道 - 大きな複雑な形状
            { 
                name: '北海道', 
                path: 'M350,50 Q370,45 390,50 Q420,55 450,60 L480,80 Q485,100 480,120 Q470,130 450,125 L420,115 Q400,110 380,115 L360,120 Q340,115 330,100 Q325,80 340,70 Z',
                labelX: 415, labelY: 85
            },
            
            // 東北地方
            { 
                name: '青森県', 
                path: 'M380,130 Q390,125 410,130 Q430,135 450,140 L450,160 Q440,165 420,160 L400,155 Q385,150 380,145 Z',
                labelX: 415, labelY: 145
            },
            { 
                name: '岩手県', 
                path: 'M450,130 Q465,128 480,135 Q495,145 500,165 L500,200 Q490,205 475,195 Q460,185 450,175 Z',
                labelX: 475, labelY: 165
            },
            { 
                name: '宮城県', 
                path: 'M420,170 Q435,165 450,175 L450,200 Q440,205 430,200 Q420,195 420,185 Z',
                labelX: 435, labelY: 185
            },
            { 
                name: '秋田県', 
                path: 'M350,140 Q365,135 380,145 L380,180 Q370,190 360,185 Q350,180 345,165 Z',
                labelX: 365, labelY: 165
            },
            { 
                name: '山形県', 
                path: 'M350,190 Q365,185 380,195 L380,220 Q370,225 360,220 Q350,215 350,205 Z',
                labelX: 365, labelY: 205
            },
            { 
                name: '福島県', 
                path: 'M380,200 Q395,195 415,205 Q420,220 415,235 L380,240 Q375,225 380,210 Z',
                labelX: 400, labelY: 220
            },
            
            // 関東地方
            { 
                name: '茨城県', 
                path: 'M450,200 Q470,195 490,205 L490,230 Q480,235 465,225 Q450,215 450,210 Z',
                labelX: 470, labelY: 215
            },
            { 
                name: '栃木県', 
                path: 'M420,240 Q435,235 450,245 L450,270 Q440,275 430,265 Q420,255 420,250 Z',
                labelX: 435, labelY: 255
            },
            { 
                name: '群馬県', // 鶴のような形状
                path: 'M380,240 Q390,235 405,240 Q410,250 415,260 Q420,265 415,270 L400,275 Q385,270 380,260 Q375,250 380,245 Z',
                labelX: 400, labelY: 255
            },
            { 
                name: '埼玉県', 
                path: 'M400,270 Q415,265 430,275 L430,290 Q420,295 410,285 Q400,280 400,275 Z',
                labelX: 415, labelY: 280
            },
            { 
                name: '千葉県', // 犬のような形状
                path: 'M450,230 Q470,225 485,235 Q495,250 490,265 Q485,275 480,280 L450,275 Q445,260 450,245 Z',
                labelX: 470, labelY: 255
            },
            { 
                name: '東京都', 
                path: 'M430,270 Q440,265 450,275 L450,290 Q440,295 435,285 Q430,280 430,275 Z',
                labelX: 440, labelY: 280
            },
            { 
                name: '神奈川県', 
                path: 'M420,290 Q440,285 460,295 L460,320 Q445,325 430,315 Q420,305 420,300 Z',
                labelX: 440, labelY: 305
            },
            
            // 中部地方
            { 
                name: '新潟県', // 細長い形状
                path: 'M280,180 Q300,175 330,185 Q350,195 350,220 Q345,235 340,240 L320,235 Q300,225 285,210 Q280,195 280,185 Z',
                labelX: 315, labelY: 210
            },
            { 
                name: '富山県', 
                path: 'M280,240 Q300,235 320,245 L320,270 Q310,275 295,265 Q280,255 280,250 Z',
                labelX: 300, labelY: 255
            },
            { 
                name: '石川県', // 能登半島を意識した形状
                path: 'M250,220 Q260,215 275,225 Q280,240 275,255 Q270,270 265,280 L250,275 Q245,260 250,245 Q248,235 250,225 Z',
                labelX: 265, labelY: 250
            },
            { 
                name: '福井県', 
                path: 'M250,280 Q265,275 280,285 L280,310 Q270,315 260,305 Q250,295 250,290 Z',
                labelX: 265, labelY: 295
            },
            { 
                name: '山梨県', 
                path: 'M360,270 Q380,265 400,275 L400,300 Q385,305 370,295 Q360,285 360,280 Z',
                labelX: 380, labelY: 285
            },
            { 
                name: '長野県', // 細長い形状
                path: 'M320,240 Q340,235 360,245 Q365,265 360,285 Q355,295 350,300 L330,295 Q320,275 320,255 Z',
                labelX: 340, labelY: 270
            },
            { 
                name: '岐阜県', 
                path: 'M280,270 Q300,265 320,275 Q325,295 320,315 L300,320 Q285,315 280,295 Z',
                labelX: 300, labelY: 295
            },
            { 
                name: '静岡県', // 伊豆半島を意識
                path: 'M360,300 Q385,295 410,305 Q420,320 415,335 Q410,340 405,340 L380,335 Q365,325 360,315 Z',
                labelX: 390, labelY: 320
            },
            { 
                name: '愛知県', 
                path: 'M320,320 Q345,315 370,325 L370,360 Q355,365 340,355 Q325,345 320,335 Z',
                labelX: 345, labelY: 340
            },
            
            // 近畿地方
            { 
                name: '三重県', 
                path: 'M280,320 Q300,315 320,325 Q325,345 320,365 Q315,375 310,380 L285,375 Q280,355 280,335 Z',
                labelX: 300, labelY: 350
            },
            { 
                name: '滋賀県', // 琵琶湖を意識した形状
                path: 'M280,310 Q295,305 310,315 L310,340 Q300,345 290,335 Q280,325 280,320 Z',
                labelX: 295, labelY: 325
            },
            { 
                name: '京都府', 
                path: 'M250,310 Q270,305 290,315 L290,340 Q275,345 260,335 Q250,325 250,320 Z',
                labelX: 270, labelY: 325
            },
            { 
                name: '大阪府', 
                path: 'M250,340 Q265,335 280,345 L280,370 Q270,375 260,365 Q250,355 250,350 Z',
                labelX: 265, labelY: 355
            },
            { 
                name: '兵庫県', // 淡路島を含む複雑な形状
                path: 'M210,330 Q230,325 250,335 Q255,355 250,370 Q245,380 240,385 L220,380 Q210,360 210,345 Z',
                labelX: 230, labelY: 355
            },
            { 
                name: '奈良県', 
                path: 'M270,360 Q285,355 300,365 L300,390 Q290,395 280,385 Q270,375 270,370 Z',
                labelX: 285, labelY: 375
            },
            { 
                name: '和歌山県', // 紀伊半島の形状
                path: 'M240,370 Q260,365 280,375 Q285,395 280,410 Q275,420 270,420 L250,415 Q240,395 240,385 Z',
                labelX: 260, labelY: 395
            },
            
            // 中国地方
            { 
                name: '鳥取県', 
                path: 'M180,320 Q200,315 220,325 L220,350 Q210,355 195,345 Q180,335 180,330 Z',
                labelX: 200, labelY: 335
            },
            { 
                name: '島根県', // 出雲地方の形状
                path: 'M120,340 Q150,335 180,345 L180,370 Q165,375 140,365 Q120,355 120,350 Z',
                labelX: 150, labelY: 355
            },
            { 
                name: '岡山県', 
                path: 'M180,350 Q200,345 220,355 L220,380 Q210,385 195,375 Q180,365 180,360 Z',
                labelX: 200, labelY: 365
            },
            { 
                name: '広島県', 
                path: 'M120,370 Q150,365 180,375 L180,400 Q165,405 140,395 Q120,385 120,380 Z',
                labelX: 150, labelY: 385
            },
            { 
                name: '山口県', // 本州最西端の形状
                path: 'M100,400 Q130,395 160,405 L160,430 Q145,435 125,425 Q100,415 100,410 Z',
                labelX: 130, labelY: 415
            },
            
            // 四国地方
            { 
                name: '徳島県', 
                path: 'M200,420 Q220,415 240,425 L240,450 Q225,455 210,445 Q200,435 200,430 Z',
                labelX: 220, labelY: 435
            },
            { 
                name: '香川県', // 小さな形状
                path: 'M170,410 Q185,405 200,415 L200,430 Q190,435 180,425 Q170,420 170,415 Z',
                labelX: 185, labelY: 420
            },
            { 
                name: '愛媛県', // 佐田岬半島を意識
                path: 'M130,420 Q155,415 170,425 Q175,440 170,455 L150,460 Q135,450 130,435 Z',
                labelX: 150, labelY: 440
            },
            { 
                name: '高知県', // 細長い形状
                path: 'M150,460 Q185,455 220,465 L220,490 Q195,495 170,485 Q150,475 150,470 Z',
                labelX: 185, labelY: 475
            },
            
            // 九州地方
            { 
                name: '福岡県', 
                path: 'M60,420 Q80,415 100,425 L100,460 Q85,465 70,455 Q60,445 60,435 Z',
                labelX: 80, labelY: 440
            },
            { 
                name: '佐賀県', 
                path: 'M40,450 Q55,445 70,455 L70,480 Q60,485 50,475 Q40,465 40,460 Z',
                labelX: 55, labelY: 465
            },
            { 
                name: '長崎県', // 複雑な海岸線と島々
                path: 'M10,440 Q25,435 40,445 Q45,465 40,480 Q35,490 30,490 L15,485 Q10,465 10,455 Z',
                labelX: 30, labelY: 465
            },
            { 
                name: '熊本県', 
                path: 'M50,480 Q70,475 90,485 L90,520 Q75,525 60,515 Q50,505 50,495 Z',
                labelX: 70, labelY: 500
            },
            { 
                name: '大分県', 
                path: 'M90,460 Q110,455 130,465 L130,500 Q115,505 100,495 Q90,485 90,475 Z',
                labelX: 110, labelY: 480
            },
            { 
                name: '宮崎県', 
                path: 'M90,500 Q105,495 120,505 L120,550 Q110,555 100,545 Q90,535 90,525 Z',
                labelX: 105, labelY: 525
            },
            { 
                name: '鹿児島県', // 薩摩・大隅半島と離島
                path: 'M60,520 Q80,515 100,525 Q105,545 100,560 Q95,570 90,570 L70,565 Q60,545 60,535 Z',
                labelX: 80, labelY: 545
            },
            
            // 沖縄県 - 島々の形状
            { 
                name: '沖縄県', 
                path: 'M20,540 Q30,535 45,545 Q55,555 50,565 Q45,570 40,570 L25,565 Q20,555 20,550 Z',
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
                    より現実的な形状で表示されています！
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
    console.log('Initializing Realistic Japan Map...');
    new RealisticJapanMap();
});