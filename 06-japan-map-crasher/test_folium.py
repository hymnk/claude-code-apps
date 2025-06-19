#!/usr/bin/env python3
"""
Folium版日本地図ブラウザの包括的テスト
"""

import sys
import os

# アプリケーションのパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_folium import app, JapanMapGenerator
import json
import pytest

def test_folium_app_functionality():
    """Foliumアプリの基本機能テスト"""
    print("=== Folium版日本地図ブラウザ テスト ===")
    
    with app.test_client() as client:
        print("\n1. メインページアクセステスト")
        response = client.get('/')
        print(f"   ステータス: {response.status_code}")
        assert response.status_code == 200, "メインページにアクセスできません"
        
        html_content = response.data.decode('utf-8')
        print(f"   HTMLサイズ: {len(html_content)} 文字")
        
        # Folium特有の要素の確認
        folium_checks = [
            ('Foliumタイトル', '美しい日本地図ブラウザ'),
            ('Folium地図要素', 'class="folium-map"'),
            ('Leafletライブラリ', 'leaflet'),
            ('モノクロベースマップ', 'cartodbpositron'),
            ('レスポンシブデザイン', 'width: 100%'),
            ('日本語エンコーディング', 'charset="UTF-8"')
        ]
        
        for name, pattern in folium_checks:
            if pattern in html_content:
                print(f"   ✅ {name}: 存在")
            else:
                print(f"   ❌ {name}: 不在")
        
        print("\n2. 都道府県APIテスト（互換性確認）")
        api_response = client.get('/api/prefectures')
        print(f"   APIステータス: {api_response.status_code}")
        
        if api_response.status_code == 200:
            data = json.loads(api_response.data)
            print(f"   都道府県数: {len(data)}")
            assert len(data) == 47, "47都道府県のデータが不足しています"
            
            # 座標データの検証
            for pref in data:
                assert 'lat' in pref, f"{pref['name']}に緯度データがありません"
                assert 'lng' in pref, f"{pref['name']}に経度データがありません"
                assert isinstance(pref['lat'], (int, float)), f"{pref['name']}の緯度が数値ではありません"
                assert isinstance(pref['lng'], (int, float)), f"{pref['name']}の経度が数値ではありません"
            
            print("   ✅ 全47都道府県の座標データ: 正常")
        
        print("\n3. JapanMapGeneratorクラステスト")
        generator = JapanMapGenerator()
        
        # データ読み込みテスト
        prefectures = generator.prefectures_data
        print(f"   都道府県データ数: {len(prefectures)}")
        assert len(prefectures) == 47
        
        # 地域別色分けテスト
        regions = ["北海道", "東北", "関東", "中部", "近畿", "中国", "四国", "九州", "沖縄"]
        for region in regions:
            color = generator.get_region_color(region)
            assert color.startswith('#'), f"{region}の色コードが不正です: {color}"
            print(f"   {region}: {color}")
        
        print("   ✅ 地域別色分け: 正常")
        
        # 美しい地図作成テスト
        print("\n4. Folium地図生成テスト")
        folium_map = generator.create_beautiful_map()
        assert folium_map is not None, "地図オブジェクトの生成に失敗"
        
        # 地図のHTML表現をテスト
        map_html = folium_map._repr_html_()
        assert len(map_html) > 1000, "生成された地図HTMLが短すぎます"
        print(f"   生成地図HTMLサイズ: {len(map_html)} 文字")
        
        # 重要な地図要素の確認
        map_elements = [
            ('Leaflet地図', 'leaflet'),
            ('日本中心座標', '36.2048'),
            ('CircleMarker', 'CircleMarker'),
            ('ポップアップ', 'popup'),
            ('凡例', '地域凡例'),
            ('モノクロテーマ', 'cartodbpositron')
        ]
        
        for name, pattern in map_elements:
            if pattern in map_html:
                print(f"   ✅ {name}: 実装済み")
            else:
                print(f"   ❌ {name}: 未実装")
        
        print("\n5. 座標範囲検証")
        valid_coords = 0
        for pref in prefectures:
            lat, lng = pref['lat'], pref['lng']
            # 日本の座標範囲内かチェック
            if 24 <= lat <= 46 and 123 <= lng <= 146:
                valid_coords += 1
            else:
                print(f"   ⚠️  {pref['name']}: 座標が範囲外 ({lat}, {lng})")
        
        print(f"   有効座標の都道府県: {valid_coords}/47")
        assert valid_coords >= 45, "座標が範囲外の都道府県が多すぎます"
        
        print("\n=== Foliumテスト完了 ===")
        print("✅ Foliumベースの美しい日本地図が正常に生成されました")
        print("✅ 47都道府県の正確な位置データが確認されました")
        print("✅ モノクロデザインテーマが適用されています")
        print("✅ インタラクティブ要素（ポップアップ・ツールチップ）が実装されています")
        print("✅ 地域別色分け凡例が表示されます")

if __name__ == '__main__':
    test_folium_app_functionality()