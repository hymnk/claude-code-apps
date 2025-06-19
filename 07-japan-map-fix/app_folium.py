#!/usr/bin/env python3
"""
Foliumを使用した美しい日本地図ブラウザアプリ
"""

from flask import Flask, render_template, jsonify
import folium
import json
import webbrowser
import threading
import time
import requests

app = Flask(__name__)

class JapanMapGenerator:
    def __init__(self):
        self.prefectures_data = self.load_prefectures_data()
        
    def load_prefectures_data(self):
        """都道府県データの読み込み"""
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
    
    def get_region_color(self, region):
        """地域別モノクロカラーマッピング"""
        colors = {
            "北海道": "#2c3e50",  # 最も濃い
            "東北": "#34495e",
            "関東": "#4a5568", 
            "中部": "#6c757d",
            "近畿": "#8d9498",
            "中国": "#a6aaae",
            "四国": "#bfc0c4",
            "九州": "#d8d9db",
            "沖縄": "#f1f2f3"   # 最も薄い
        }
        return colors.get(region, "#888888")
    
    def create_beautiful_map(self):
        """美しい日本地図を作成"""
        # 日本の中心座標
        japan_center = [36.2048, 138.2529]
        
        # Folium地図の作成（モノクロテーマ）
        m = folium.Map(
            location=japan_center,
            zoom_start=6,
            tiles=None,  # デフォルトタイルを無効化
            prefer_canvas=True
        )
        
        # モノクロベースマップを追加
        folium.TileLayer(
            tiles='cartodbpositron',  # 明るいモノクロテーマ
            name='Light Map',
            overlay=False,
            control=True
        ).add_to(m)
        
        # 各都道府県にマーカーを追加
        for pref in self.prefectures_data:
            color = self.get_region_color(pref['region'])
            
            # 円形マーカー（県庁所在地）
            folium.CircleMarker(
                location=[pref['lat'], pref['lng']],
                radius=8,
                popup=folium.Popup(
                    f"""
                    <div style='font-family: Arial; min-width: 200px;'>
                        <h4 style='margin: 0; color: #2c3e50;'>{pref['name']}</h4>
                        <hr style='margin: 5px 0;'>
                        <p style='margin: 2px 0;'><strong>地域:</strong> {pref['region']}地方</p>
                        <p style='margin: 2px 0;'><strong>コード:</strong> {pref['code']}</p>
                        <p style='margin: 2px 0; font-size: 12px; color: #666;'>
                            座標: {pref['lat']:.3f}, {pref['lng']:.3f}
                        </p>
                    </div>
                    """,
                    max_width=250
                ),
                tooltip=f"{pref['name']} ({pref['region']}地方)",
                color='white',
                weight=2,
                fill=True,
                fillColor=color,
                fillOpacity=0.8
            ).add_to(m)
            
            # 都道府県名のラベル
            folium.Marker(
                location=[pref['lat'], pref['lng']],
                icon=folium.DivIcon(
                    html=f"""
                    <div style='
                        font-size: 10px; 
                        color: white; 
                        font-weight: bold; 
                        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
                        text-align: center;
                        margin-top: -15px;
                        pointer-events: none;
                    '>
                        {pref['name'].replace('県', '').replace('府', '').replace('都', '')}
                    </div>
                    """,
                    class_name="prefecture-label"
                )
            ).add_to(m)
        
        # 凡例を追加
        legend_html = """
        <div style='
            position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 180px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:14px; padding: 10px; border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        '>
        <h4 style='margin-top: 0; color: #2c3e50;'>🗾 地域凡例</h4>
        """
        
        for region in ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州", "沖縄"]:
            color = self.get_region_color(region)
            legend_html += f"""
            <p style='margin: 3px 0;'>
                <span style='
                    display: inline-block; 
                    width: 12px; 
                    height: 12px; 
                    background-color: {color}; 
                    border: 1px solid #666;
                    margin-right: 5px;
                '></span>
                {region}
            </p>
            """
        
        legend_html += "</div>"
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m

@app.route('/')
def index():
    """Folium地図を表示するメインページ"""
    generator = JapanMapGenerator()
    japan_map = generator.create_beautiful_map()
    
    # HTMLテンプレートに地図を埋め込み
    map_html = japan_map._repr_html_()
    
    return f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🗾 美しい日本地図ブラウザ (Folium版)</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f8f9fa;
            }}
            .header {{
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header h1 {{
                margin: 0;
                font-size: 2rem;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
                font-size: 1.1rem;
            }}
            .map-container {{
                height: calc(100vh - 120px);
                width: 100%;
                border: none;
            }}
            .footer {{
                background: #2c3e50;
                color: white;
                text-align: center;
                padding: 15px;
                font-size: 0.9rem;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🗾 美しい日本地図ブラウザ</h1>
            <p>Foliumライブラリで作成された高品質インタラクティブ地図</p>
        </div>
        <div class="map-container">
            {map_html}
        </div>
        <div class="footer">
            © 2024 日本地図ブラウザ (Powered by Folium) | 
            各マーカーをクリックして詳細情報を表示
        </div>
    </body>
    </html>
    """

@app.route('/api/prefectures')
def get_prefectures():
    """都道府県データAPI（既存のAPIとの互換性維持）"""
    generator = JapanMapGenerator()
    return jsonify(generator.prefectures_data)

def open_browser():
    """ブラウザを自動で開く"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🗾 美しい日本地図ブラウザアプリ (Folium版) を起動しています...")
    print("=" * 60)
    print("📍 URL: http://localhost:5000")
    print("📱 ブラウザが自動で開きます")
    print("🎨 Foliumライブラリによる高品質地図表示")
    print("🛑 終了するには Ctrl+C を押してください")
    print("=" * 60)
    
    # ブラウザを自動で開く
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Flaskアプリを起動
    app.run(host='0.0.0.0', port=5000, debug=False)