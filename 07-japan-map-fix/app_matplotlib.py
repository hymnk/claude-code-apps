#!/usr/bin/env python3
"""
Matplotlib/Geopandasを使用した高品質日本地図表示アプリ
JavaScript不使用の純Pythonソリューション
"""

import matplotlib
matplotlib.use('Agg')  # GUI不要のバックエンドを使用
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from flask import Flask, render_template, send_file, jsonify
import io
import base64
import threading
import time
import webbrowser

app = Flask(__name__)

class JapanMapGenerator:
    def __init__(self):
        # プロット用のフォント設定（英語のみ）
        plt.rcParams['font.family'] = ['DejaVu Sans']
        plt.rcParams['font.size'] = 10
        self.prefectures_data = self.load_prefectures_data()
        
    def load_prefectures_data(self):
        """Prefecture data with English names (simplified coordinates)"""
        return [
            {"name": "Hokkaido", "region": "Hokkaido", "x": 0.5, "y": 0.9, "size": 120},
            {"name": "Aomori", "region": "Tohoku", "x": 0.52, "y": 0.75, "size": 60},
            {"name": "Iwate", "region": "Tohoku", "x": 0.55, "y": 0.72, "size": 60},
            {"name": "Miyagi", "region": "Tohoku", "x": 0.53, "y": 0.68, "size": 50},
            {"name": "Akita", "region": "Tohoku", "x": 0.48, "y": 0.70, "size": 55},
            {"name": "Yamagata", "region": "Tohoku", "x": 0.50, "y": 0.67, "size": 50},
            {"name": "Fukushima", "region": "Tohoku", "x": 0.52, "y": 0.64, "size": 65},
            {"name": "Ibaraki", "region": "Kanto", "x": 0.56, "y": 0.58, "size": 55},
            {"name": "Tochigi", "region": "Kanto", "x": 0.53, "y": 0.59, "size": 50},
            {"name": "Gunma", "region": "Kanto", "x": 0.50, "y": 0.60, "size": 45},
            {"name": "Saitama", "region": "Kanto", "x": 0.52, "y": 0.57, "size": 45},
            {"name": "Chiba", "region": "Kanto", "x": 0.57, "y": 0.56, "size": 50},
            {"name": "Tokyo", "region": "Kanto", "x": 0.54, "y": 0.56, "size": 40},
            {"name": "Kanagawa", "region": "Kanto", "x": 0.52, "y": 0.54, "size": 45},
            {"name": "Niigata", "region": "Chubu", "x": 0.45, "y": 0.64, "size": 70},
            {"name": "Toyama", "region": "Chubu", "x": 0.42, "y": 0.58, "size": 40},
            {"name": "Ishikawa", "region": "Chubu", "x": 0.40, "y": 0.57, "size": 40},
            {"name": "Fukui", "region": "Chubu", "x": 0.39, "y": 0.54, "size": 40},
            {"name": "Yamanashi", "region": "Chubu", "x": 0.49, "y": 0.54, "size": 40},
            {"name": "Nagano", "region": "Chubu", "x": 0.46, "y": 0.56, "size": 60},
            {"name": "Gifu", "region": "Chubu", "x": 0.44, "y": 0.53, "size": 50},
            {"name": "Shizuoka", "region": "Chubu", "x": 0.47, "y": 0.51, "size": 55},
            {"name": "Aichi", "region": "Chubu", "x": 0.45, "y": 0.50, "size": 55},
            {"name": "Mie", "region": "Kinki", "x": 0.43, "y": 0.48, "size": 45},
            {"name": "Shiga", "region": "Kinki", "x": 0.41, "y": 0.50, "size": 35},
            {"name": "Kyoto", "region": "Kinki", "x": 0.40, "y": 0.51, "size": 40},
            {"name": "Osaka", "region": "Kinki", "x": 0.39, "y": 0.49, "size": 35},
            {"name": "Hyogo", "region": "Kinki", "x": 0.37, "y": 0.50, "size": 50},
            {"name": "Nara", "region": "Kinki", "x": 0.41, "y": 0.48, "size": 35},
            {"name": "Wakayama", "region": "Kinki", "x": 0.40, "y": 0.46, "size": 40},
            {"name": "Tottori", "region": "Chugoku", "x": 0.35, "y": 0.52, "size": 35},
            {"name": "Shimane", "region": "Chugoku", "x": 0.32, "y": 0.53, "size": 45},
            {"name": "Okayama", "region": "Chugoku", "x": 0.36, "y": 0.49, "size": 45},
            {"name": "Hiroshima", "region": "Chugoku", "x": 0.33, "y": 0.48, "size": 50},
            {"name": "Yamaguchi", "region": "Chugoku", "x": 0.30, "y": 0.46, "size": 45},
            {"name": "Tokushima", "region": "Shikoku", "x": 0.38, "y": 0.44, "size": 35},
            {"name": "Kagawa", "region": "Shikoku", "x": 0.36, "y": 0.45, "size": 30},
            {"name": "Ehime", "region": "Shikoku", "x": 0.33, "y": 0.44, "size": 40},
            {"name": "Kochi", "region": "Shikoku", "x": 0.35, "y": 0.42, "size": 45},
            {"name": "Fukuoka", "region": "Kyushu", "x": 0.27, "y": 0.42, "size": 50},
            {"name": "Saga", "region": "Kyushu", "x": 0.25, "y": 0.42, "size": 30},
            {"name": "Nagasaki", "region": "Kyushu", "x": 0.22, "y": 0.41, "size": 40},
            {"name": "Kumamoto", "region": "Kyushu", "x": 0.26, "y": 0.39, "size": 45},
            {"name": "Oita", "region": "Kyushu", "x": 0.29, "y": 0.40, "size": 40},
            {"name": "Miyazaki", "region": "Kyushu", "x": 0.28, "y": 0.37, "size": 40},
            {"name": "Kagoshima", "region": "Kyushu", "x": 0.26, "y": 0.34, "size": 50},
            {"name": "Okinawa", "region": "Okinawa", "x": 0.15, "y": 0.15, "size": 35}
        ]
    
    def get_region_colors(self):
        """地域別カラーマッピング（美しいグラデーション）"""
        return {
            "北海道": "#1e3a8a",  # 深い青
            "東北": "#3b82f6",    # 青
            "関東": "#06b6d4",    # シアン
            "中部": "#10b981",    # エメラルド
            "近畿": "#f59e0b",    # オレンジ
            "中国": "#ef4444",    # 赤
            "四国": "#a855f7",    # 紫
            "九州": "#ec4899",    # ピンク
            "沖縄": "#14b8a6"     # ティール
        }
    
    def create_beautiful_map(self):
        """高品質な日本地図を生成"""
        # 図のサイズと背景設定
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor('#f8fafc')
        ax.set_facecolor('#f1f5f9')
        
        # 地域色設定
        region_colors = self.get_region_colors()
        
        # 日本の海域を表現（背景の海）
        ocean = patches.Rectangle((0, 0), 1, 1, 
                                facecolor='#3b82f6', alpha=0.1, 
                                zorder=0)
        ax.add_patch(ocean)
        
        # 各都道府県を円で表現
        for pref in self.prefectures_data:
            color = region_colors[pref['region']]
            
            # メイン円（都道府県）
            circle = patches.Circle(
                (pref['x'], pref['y']), 
                pref['size']/2000,  # サイズ調整
                facecolor=color,
                edgecolor='white',
                linewidth=2,
                alpha=0.8,
                zorder=2
            )
            ax.add_patch(circle)
            
            # 県名ラベル
            ax.text(pref['x'], pref['y'], pref['name'], 
                   fontsize=8, ha='center', va='center',
                   color='white', weight='bold',
                   zorder=3)
        
        # 地域境界線の描画（簡略化）
        self.draw_region_boundaries(ax)
        
        # タイトルと装飾
        ax.set_title('Beautiful Japan Map\n47 Prefectures by Region', 
                    fontsize=20, weight='bold', 
                    color='#1e293b', pad=20)
        
        # 凡例の作成
        self.create_legend(ax, region_colors)
        
        # 軸設定
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # グリッドと装飾
        ax.grid(True, alpha=0.1, color='#64748b')
        
        plt.tight_layout()
        return fig
    
    def draw_region_boundaries(self, ax):
        """地域境界線を描画"""
        # 簡略化された地域境界
        boundaries = [
            # 本州の大まかな輪郭
            [(0.3, 0.4), (0.6, 0.4), (0.6, 0.8), (0.3, 0.8), (0.3, 0.4)],
            # 四国
            [(0.32, 0.42), (0.4, 0.42), (0.4, 0.46), (0.32, 0.46), (0.32, 0.42)],
            # 九州
            [(0.22, 0.34), (0.3, 0.34), (0.3, 0.44), (0.22, 0.44), (0.22, 0.34)],
        ]
        
        for boundary in boundaries:
            xs, ys = zip(*boundary)
            ax.plot(xs, ys, color='#475569', alpha=0.3, linewidth=1, zorder=1)
    
    def create_legend(self, ax, region_colors):
        """美しい凡例を作成"""
        legend_x = 0.02
        legend_y = 0.98
        
        # 凡例背景
        legend_bg = patches.Rectangle(
            (legend_x, legend_y-0.32), 0.18, 0.30,
            facecolor='white', edgecolor='#e2e8f0',
            linewidth=2, alpha=0.95, zorder=10
        )
        ax.add_patch(legend_bg)
        
        # 凡例タイトル
        ax.text(legend_x + 0.09, legend_y - 0.03, 'Regions',
               fontsize=12, weight='bold', ha='center',
               color='#1e293b', zorder=11)
        
        # 各地域の凡例項目
        y_offset = 0.06
        for i, (region, color) in enumerate(region_colors.items()):
            y_pos = legend_y - y_offset - (i * 0.03)
            
            # 色サンプル
            color_box = patches.Rectangle(
                (legend_x + 0.01, y_pos - 0.008), 0.02, 0.016,
                facecolor=color, edgecolor='#64748b',
                linewidth=0.5, zorder=11
            )
            ax.add_patch(color_box)
            
            # 地域名
            ax.text(legend_x + 0.04, y_pos, region,
                   fontsize=9, va='center', color='#374151', zorder=11)

@app.route('/')
def index():
    """メインページ"""
    return render_template('map_matplotlib.html')

@app.route('/map.png')
def generate_map():
    """地図画像を生成して返す"""
    generator = JapanMapGenerator()
    fig = generator.create_beautiful_map()
    
    # PNG形式で画像を生成
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png', dpi=150, 
                bbox_inches='tight', facecolor='#f8fafc')
    img_buffer.seek(0)
    plt.close(fig)  # メモリリークを防ぐ
    
    return send_file(img_buffer, mimetype='image/png')

@app.route('/api/prefectures')
def get_prefectures():
    """都道府県データAPI"""
    generator = JapanMapGenerator()
    return jsonify(generator.prefectures_data)

def open_browser():
    """ブラウザを自動で開く"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🗾 高品質日本地図ブラウザアプリ（Matplotlib版）を起動しています...")
    print("=" * 70)
    print("📍 URL: http://localhost:5000")
    print("📱 ブラウザが自動で開きます")
    print("🎨 Matplotlib/Pythonによる純粋なPython地図表示")
    print("🚫 JavaScript不使用のクリーンな実装")
    print("🛑 終了するには Ctrl+C を押してください")
    print("=" * 70)
    
    # ブラウザを自動で開く
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Flaskアプリを起動
    app.run(host='0.0.0.0', port=5000, debug=False)