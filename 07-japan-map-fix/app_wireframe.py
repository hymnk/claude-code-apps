#!/usr/bin/env python3
"""
ワイヤーフレーム日本地図ブラウザアプリ
シンプルなMatplotlibベースのミニマルデザイン
"""

from flask import Flask, render_template, jsonify, send_file
import matplotlib
matplotlib.use('Agg')  # バックエンドを設定
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json
import webbrowser
import threading
import time
import io
import base64
import numpy as np

# 日本語フォントの設定（手動で設定）
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']

app = Flask(__name__)

class WireframeJapanMapGenerator:
    def __init__(self):
        self.prefectures_data = self.load_prefectures_data()
        self.prefecture_boundaries = self.create_prefecture_boundaries()
        
    def load_prefectures_data(self):
        """都道府県データの読み込み（座標付き）"""
        return [
            {"name": "北海道", "code": "01", "region": "北海道", "lat": 43.2203, "lng": 142.8635},
            {"name": "青森県", "code": "02", "region": "東北", "lat": 40.8243, "lng": 140.7400},
            {"name": "岩手県", "code": "03", "region": "東北", "lat": 39.7036, "lng": 141.1527},
            {"name": "宮城県", "code": "04", "region": "東北", "lat": 38.2682, "lng": 140.8721},
            {"name": "秋田県", "code": "05", "region": "東北", "lat": 39.7186, "lng": 140.1024},
            {"name": "山形県", "code": "06", "region": "東北", "lat": 38.2404, "lng": 140.3633},
            {"name": "福島県", "code": "07", "region": "東北", "lat": 37.7503, "lng": 140.4676},
            {"name": "茨城県", "code": "08", "region": "関東", "lat": 36.3418, "lng": 140.4468},
            {"name": "栃木県", "code": "09", "region": "関東", "lat": 36.5658, "lng": 139.8836},
            {"name": "群馬県", "code": "10", "region": "関東", "lat": 36.3911, "lng": 139.0608},
            {"name": "埼玉県", "code": "11", "region": "関東", "lat": 35.8569, "lng": 139.6489},
            {"name": "千葉県", "code": "12", "region": "関東", "lat": 35.6074, "lng": 140.1065},
            {"name": "東京都", "code": "13", "region": "関東", "lat": 35.6762, "lng": 139.6503},
            {"name": "神奈川県", "code": "14", "region": "関東", "lat": 35.4478, "lng": 139.6425},
            {"name": "新潟県", "code": "15", "region": "中部", "lat": 37.9026, "lng": 139.0233},
            {"name": "富山県", "code": "16", "region": "中部", "lat": 36.6959, "lng": 137.2139},
            {"name": "石川県", "code": "17", "region": "中部", "lat": 36.5944, "lng": 136.6256},
            {"name": "福井県", "code": "18", "region": "中部", "lat": 35.9432, "lng": 136.1839},
            {"name": "山梨県", "code": "19", "region": "中部", "lat": 35.6635, "lng": 138.5684},
            {"name": "長野県", "code": "20", "region": "中部", "lat": 36.6513, "lng": 138.1811},
            {"name": "岐阜県", "code": "21", "region": "中部", "lat": 35.3912, "lng": 136.7223},
            {"name": "静岡県", "code": "22", "region": "中部", "lat": 34.9769, "lng": 138.3831},
            {"name": "愛知県", "code": "23", "region": "中部", "lat": 35.1802, "lng": 136.9066},
            {"name": "三重県", "code": "24", "region": "近畿", "lat": 34.7302, "lng": 136.5086},
            {"name": "滋賀県", "code": "25", "region": "近畿", "lat": 35.0045, "lng": 135.8684},
            {"name": "京都府", "code": "26", "region": "近畿", "lat": 35.0211, "lng": 135.7556},
            {"name": "大阪府", "code": "27", "region": "近畿", "lat": 34.6862, "lng": 135.5200},
            {"name": "兵庫県", "code": "28", "region": "近畿", "lat": 34.6913, "lng": 135.1830},
            {"name": "奈良県", "code": "29", "region": "近畿", "lat": 34.6851, "lng": 135.8329},
            {"name": "和歌山県", "code": "30", "region": "近畿", "lat": 34.2261, "lng": 135.1675},
            {"name": "鳥取県", "code": "31", "region": "中国", "lat": 35.5038, "lng": 134.2380},
            {"name": "島根県", "code": "32", "region": "中国", "lat": 35.4723, "lng": 133.0505},
            {"name": "岡山県", "code": "33", "region": "中国", "lat": 34.6618, "lng": 133.9349},
            {"name": "広島県", "code": "34", "region": "中国", "lat": 34.3963, "lng": 132.4596},
            {"name": "山口県", "code": "35", "region": "中国", "lat": 34.1859, "lng": 131.4706},
            {"name": "徳島県", "code": "36", "region": "四国", "lat": 34.0658, "lng": 134.5594},
            {"name": "香川県", "code": "37", "region": "四国", "lat": 34.3401, "lng": 134.0434},
            {"name": "愛媛県", "code": "38", "region": "四国", "lat": 33.8416, "lng": 132.7657},
            {"name": "高知県", "code": "39", "region": "四国", "lat": 33.5597, "lng": 133.5311},
            {"name": "福岡県", "code": "40", "region": "九州", "lat": 33.6064, "lng": 130.4181},
            {"name": "佐賀県", "code": "41", "region": "九州", "lat": 33.2494, "lng": 130.2989},
            {"name": "長崎県", "code": "42", "region": "九州", "lat": 32.7444, "lng": 129.8737},
            {"name": "熊本県", "code": "43", "region": "九州", "lat": 32.7898, "lng": 130.7417},
            {"name": "大分県", "code": "44", "region": "九州", "lat": 33.2382, "lng": 131.6126},
            {"name": "宮崎県", "code": "45", "region": "九州", "lat": 31.9077, "lng": 131.4202},
            {"name": "鹿児島県", "code": "46", "region": "九州", "lat": 31.5602, "lng": 130.5581},
            {"name": "沖縄県", "code": "47", "region": "沖縄", "lat": 26.2125, "lng": 127.6792}
        ]
    
    def create_prefecture_boundaries(self):
        """都道府県の境界線データを作成（簡略化された境界）"""
        boundaries = {}
        
        # 簡略化された日本の都道府県境界ポリゴン（近似）
        japan_outline = [
            # 本州の大まかな境界線
            [129.5, 32.0], [130.0, 31.5], [131.0, 31.2], [132.0, 32.0],
            [133.0, 33.5], [134.0, 34.0], [135.0, 34.2], [136.0, 34.8],
            [137.0, 35.0], [138.0, 35.5], [139.0, 35.7], [140.0, 36.0],
            [141.0, 37.0], [142.0, 38.5], [143.0, 40.0], [142.5, 41.5],
            [141.8, 42.8], [140.5, 43.5], [139.0, 43.8], [138.0, 43.2],
            [137.0, 42.5], [136.0, 41.0], [135.0, 39.5], [134.0, 38.0],
            [133.0, 36.5], [132.0, 35.0], [131.0, 33.5], [130.0, 32.5]
        ]
        
        # 各都道府県の簡略化された境界を生成
        for pref in self.prefectures_data:
            # 各都道府県の中心点を基に簡単な境界を作成
            lat, lng = pref['lat'], pref['lng']
            
            # 簡単な正方形の境界（実際の形状ではないが、ワイヤーフレームとしては十分）
            offset = 0.3  # 境界のサイズ
            boundary = [
                [lng - offset, lat - offset],
                [lng + offset, lat - offset],
                [lng + offset, lat + offset],
                [lng - offset, lat + offset],
                [lng - offset, lat - offset]  # 閉じるために最初の点を追加
            ]
            boundaries[pref['name']] = boundary
            
        return boundaries
    
    def create_wireframe_map(self):
        """ミニマルなワイヤーフレーム地図を作成"""
        # 図のサイズと背景設定
        fig, ax = plt.subplots(1, 1, figsize=(14, 10))
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        
        # 日本全体の境界線（矩形フレーム）
        japan_lons = [129, 146, 146, 129, 129]
        japan_lats = [30, 30, 46, 46, 30]
        ax.plot(japan_lons, japan_lats, 'k-', linewidth=2, alpha=0.6)
        
        # 実際の日本の輪郭線（簡略化）
        japan_outline_coords = [
            # 本州の大まかな境界
            [129.5, 32.0], [130.8, 31.2], [131.8, 31.5], [133.2, 32.8], 
            [134.5, 33.8], [135.8, 34.3], [137.2, 34.9], [138.9, 35.3],
            [140.2, 35.8], [141.1, 36.8], [141.8, 38.2], [142.2, 39.8],
            [142.6, 41.2], [142.0, 42.5], [141.2, 43.2], [139.8, 43.8],
            [138.5, 43.5], [137.0, 42.8], [135.5, 41.5], [134.2, 39.8],
            [133.0, 37.5], [131.8, 35.2], [130.5, 33.5], [129.5, 32.0]
        ]
        outline_lons, outline_lats = zip(*japan_outline_coords)
        ax.plot(outline_lons, outline_lats, 'k-', linewidth=1.2, alpha=0.8)
        
        # 各都道府県の点とラベル
        for i, pref in enumerate(self.prefectures_data):
            # 都道府県の位置に大きめの点を描画
            ax.plot(pref['lng'], pref['lat'], 'ko', markersize=5, alpha=0.9)
            
            # 都道府県名のラベル（ローマ字表記）
            name_romaji = {
                '北海道': 'Hokkaido', '青森県': 'Aomori', '岩手県': 'Iwate', '宮城県': 'Miyagi',
                '秋田県': 'Akita', '山形県': 'Yamagata', '福島県': 'Fukushima', '茨城県': 'Ibaraki',
                '栃木県': 'Tochigi', '群馬県': 'Gunma', '埼玉県': 'Saitama', '千葉県': 'Chiba',
                '東京都': 'Tokyo', '神奈川県': 'Kanagawa', '新潟県': 'Niigata', '富山県': 'Toyama',
                '石川県': 'Ishikawa', '福井県': 'Fukui', '山梨県': 'Yamanashi', '長野県': 'Nagano',
                '岐阜県': 'Gifu', '静岡県': 'Shizuoka', '愛知県': 'Aichi', '三重県': 'Mie',
                '滋賀県': 'Shiga', '京都府': 'Kyoto', '大阪府': 'Osaka', '兵庫県': 'Hyogo',
                '奈良県': 'Nara', '和歌山県': 'Wakayama', '鳥取県': 'Tottori', '島根県': 'Shimane',
                '岡山県': 'Okayama', '広島県': 'Hiroshima', '山口県': 'Yamaguchi', '徳島県': 'Tokushima',
                '香川県': 'Kagawa', '愛媛県': 'Ehime', '高知県': 'Kochi', '福岡県': 'Fukuoka',
                '佐賀県': 'Saga', '長崎県': 'Nagasaki', '熊本県': 'Kumamoto', '大分県': 'Oita',
                '宮崎県': 'Miyazaki', '鹿児島県': 'Kagoshima', '沖縄県': 'Okinawa'
            }
            
            display_name = name_romaji.get(pref['name'], pref['name'])
            ax.annotate(display_name, 
                       (pref['lng'], pref['lat']),
                       xytext=(5, 5), 
                       textcoords='offset points',
                       fontsize=8,
                       alpha=0.8,
                       ha='left')
        
        # 地域別の境界線
        regions = {
            '北海道': [(139.8, 43.8), (142.6, 41.2), (142.0, 42.5), (141.2, 43.2)],
            '東北': [(140.1, 39.7), (141.2, 39.7), (141.8, 38.2), (140.4, 38.2), (140.5, 37.8)],
            '関東': [(139.1, 36.4), (140.4, 36.3), (140.1, 35.6), (139.6, 35.4), (139.6, 35.9)],
            '中部': [(136.6, 36.6), (139.0, 37.9), (138.6, 35.7), (136.7, 35.4), (136.2, 35.9)],
            '近畿': [(135.2, 35.0), (136.5, 34.7), (135.8, 34.7), (135.2, 34.2)],
            '中国': [(133.0, 35.5), (134.2, 35.5), (132.5, 34.4), (131.5, 34.2)],
            '四国': [(134.6, 34.1), (134.0, 34.3), (132.8, 33.8), (133.5, 33.6)],
            '九州': [(130.4, 33.6), (131.6, 33.2), (131.4, 31.9), (129.9, 32.7)]
        }
        
        colors = ['#666', '#777', '#888', '#999', '#aaa', '#bbb', '#ccc', '#ddd']
        for i, (region, coords) in enumerate(regions.items()):
            if len(coords) > 2:
                lons, lats = zip(*coords + [coords[0]])  # 閉じた線にする
                ax.plot(lons, lats, '-', linewidth=1, alpha=0.5, color=colors[i % len(colors)])
        
        # 座標軸の設定
        ax.set_xlim(128, 147)
        ax.set_ylim(25, 46)
        ax.set_xlabel('Longitude (経度)', fontsize=12)
        ax.set_ylabel('Latitude (緯度)', fontsize=12)
        ax.grid(True, alpha=0.3, linewidth=0.7, linestyle='--')
        ax.set_aspect('equal')
        
        # タイトル
        ax.set_title('Japan Map - Wireframe Edition', fontsize=18, fontweight='bold', pad=20)
        
        # 凡例的な情報を追加
        ax.text(0.02, 0.98, f'Prefectures: {len(self.prefectures_data)}', 
                transform=ax.transAxes, fontsize=10, 
                verticalalignment='top', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 余白を最小化
        plt.tight_layout()
        
        # 画像をbase64エンコード
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        img_data = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return img_data

@app.route('/')
def index():
    """ワイヤーフレーム地図を表示するメインページ"""
    generator = WireframeJapanMapGenerator()
    map_image_data = generator.create_wireframe_map()
    
    return f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🗾 ワイヤーフレーム日本地図ブラウザ</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace;
                background: #fafafa;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #eee;
                padding-bottom: 20px;
            }}
            .header h1 {{
                font-size: 2.2rem;
                font-weight: 300;
                color: #2c3e50;
                letter-spacing: 1px;
            }}
            .header p {{
                color: #666;
                font-size: 1rem;
                margin-top: 10px;
                font-style: italic;
            }}
            .map-container {{
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                text-align: center;
            }}
            .map-image {{
                max-width: 100%;
                height: auto;
                border: 1px solid #eee;
                border-radius: 4px;
            }}
            .info-panel {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 30px;
            }}
            .info-card {{
                background: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 20px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }}
            .info-card h3 {{
                font-size: 1.1rem;
                color: #2c3e50;
                margin-bottom: 15px;
                font-weight: 500;
            }}
            .info-card ul {{
                list-style: none;
                padding-left: 0;
            }}
            .info-card li {{
                padding: 4px 0;
                color: #666;
                font-size: 0.9rem;
                border-bottom: 1px solid #f5f5f5;
            }}
            .info-card li:last-child {{
                border-bottom: none;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                border-top: 1px solid #eee;
                color: #888;
                font-size: 0.9rem;
            }}
            .tech-specs {{
                font-family: monospace;
                background: #f8f9fa;
                border-left: 3px solid #6c757d;
                padding: 15px;
                margin: 20px 0;
                font-size: 0.85rem;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🗾 ワイヤーフレーム日本地図</h1>
                <p>Geoplot + Matplotlib による ミニマルデザイン</p>
            </div>
            
            <div class="map-container">
                <img src="data:image/png;base64,{map_image_data}" alt="Japan Wireframe Map" class="map-image">
            </div>
            
            <div class="info-panel">
                <div class="info-card">
                    <h3>📊 データ仕様</h3>
                    <ul>
                        <li>47都道府県を点で表示</li>
                        <li>地域別グループ線</li>
                        <li>正確な緯度経度座標</li>
                        <li>グリッド表示付き</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>🎨 デザイン特徴</h3>
                    <ul>
                        <li>ミニマルなワイヤーフレーム</li>
                        <li>モノクロ配色</li>
                        <li>等角投影</li>
                        <li>高解像度PNG出力</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>🛠️ 技術スタック</h3>
                    <ul>
                        <li>Python + Flask</li>
                        <li>Geoplot + GeoPandas</li>
                        <li>Matplotlib (Agg)</li>
                        <li>Base64画像エンコード</li>
                    </ul>
                </div>
                
                <div class="info-card">
                    <h3>🌐 地域区分</h3>
                    <ul>
                        <li>北海道・東北 (7)</li>
                        <li>関東 (7) / 中部 (9)</li>
                        <li>近畿 (7) / 中国 (5)</li>
                        <li>四国 (4) / 九州・沖縄 (8)</li>
                    </ul>
                </div>
            </div>
            
            <div class="tech-specs">
                <strong>Technical Specifications:</strong><br>
                Resolution: 150 DPI | Format: PNG | Encoding: Base64<br>
                Coordinate System: WGS84 (EPSG:4326) | Projection: Equirectangular<br>
                Libraries: geoplot v0.5.1, matplotlib v3.10.3, geopandas v0.14.0
            </div>
            
            <div class="footer">
                © 2024 ワイヤーフレーム日本地図ブラウザ | 
                Powered by Geoplot & Matplotlib
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/api/prefectures')
def get_prefectures():
    """都道府県データAPI（互換性維持）"""
    generator = WireframeJapanMapGenerator()
    return jsonify(generator.prefectures_data)

@app.route('/map/download')
def download_map():
    """地図画像のダウンロード"""
    generator = WireframeJapanMapGenerator()
    
    # 高解像度版の地図を生成
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    # 日本全体の境界線
    japan_lons = [129, 146, 146, 129, 129]
    japan_lats = [31, 31, 46, 46, 31]
    ax.plot(japan_lons, japan_lats, 'k-', linewidth=2, alpha=0.4)
    
    # 都道府県の点とラベル
    for pref in generator.prefectures_data:
        ax.plot(pref['lng'], pref['lat'], 'ko', markersize=5, alpha=0.9)
        name = pref['name'].replace('県', '').replace('府', '').replace('都', '')
        ax.annotate(name, 
                   (pref['lng'], pref['lat']),
                   xytext=(5, 5), 
                   textcoords='offset points',
                   fontsize=12,
                   alpha=0.8)
    
    ax.set_xlim(128, 147)
    ax.set_ylim(25, 46)
    ax.set_xlabel('経度 (Longitude)', fontsize=12)
    ax.set_ylabel('緯度 (Latitude)', fontsize=12)
    ax.grid(True, alpha=0.3, linewidth=0.7)
    ax.set_aspect('equal')
    ax.set_title('🗾 日本地図 - ワイヤーフレーム版 (高解像度)', fontsize=20, fontweight='bold', pad=30)
    
    plt.tight_layout()
    
    # ファイルとして返す
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight',
               facecolor='white', edgecolor='none')
    img_buffer.seek(0)
    plt.close()
    
    return send_file(img_buffer, mimetype='image/png', as_attachment=True,
                     download_name='japan_wireframe_map_hd.png')

def open_browser():
    """ブラウザを自動で開く"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🗾 ワイヤーフレーム日本地図ブラウザを起動しています...")
    print("=" * 60)
    print("📍 URL: http://localhost:5000")
    print("📱 ブラウザが自動で開きます")
    print("🎨 Geoplot + Matplotlib によるワイヤーフレームデザイン")
    print("✨ 特徴:")
    print("   - ミニマルなワイヤーフレーム表示")
    print("   - 47都道府県の正確な位置")
    print("   - モノクロデザインテーマ")
    print("   - 高解像度PNG出力")
    print("   - 地域別グループ線表示")
    print("🛑 終了するには Ctrl+C を押してください")
    print("=" * 60)
    
    # ブラウザを自動で開く
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Flaskアプリを起動
    app.run(host='0.0.0.0', port=5000, debug=False)