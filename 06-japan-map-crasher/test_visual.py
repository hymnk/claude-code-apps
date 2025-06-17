#!/usr/bin/env python3
"""
視覚的動作確認テスト
"""

import sys
import os

# アプリケーションのパスを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
import json

def test_visual_functionality():
    """視覚的機能の確認テスト"""
    print("=== 日本地図ブラウザ 視覚的動作確認 ===")
    
    with app.test_client() as client:
        print("\n1. メインページのアクセステスト")
        response = client.get('/')
        print(f"   ステータス: {response.status_code}")
        assert response.status_code == 200, "メインページにアクセスできません"
        
        html_content = response.data.decode('utf-8')
        print(f"   HTMLサイズ: {len(html_content)} 文字")
        
        # 重要な要素の確認
        checks = [
            ('SVG地図要素', 'id="japan-map"'),
            ('新しいJSファイル', 'simple_map.js'),
            ('CSSファイル', 'style.css'),
            ('D3.jsライブラリ', 'd3js.org'),
            ('情報パネル', 'prefecture-info'),
            ('凡例', 'legend')
        ]
        
        for name, pattern in checks:
            if pattern in html_content:
                print(f"   ✅ {name}: 存在")
            else:
                print(f"   ❌ {name}: 不在")
        
        print("\n2. 都道府県APIテスト")
        api_response = client.get('/api/prefectures')
        print(f"   APIステータス: {api_response.status_code}")
        
        if api_response.status_code == 200:
            data = json.loads(api_response.data)
            print(f"   都道府県数: {len(data)}")
            
            # 地域別集計
            regions = {}
            for pref in data:
                region = pref['region']
                regions[region] = regions.get(region, 0) + 1
            
            print("   地域別都道府県数:")
            for region, count in regions.items():
                print(f"     {region}: {count}件")
        
        print("\n3. 静的ファイルテスト")
        static_files = [
            ('/static/css/style.css', 'CSS'),
            ('/static/js/simple_map.js', '新JavaScript'),
            ('/static/js/map.js', '旧JavaScript')
        ]
        
        for url, name in static_files:
            response = client.get(url)
            if response.status_code == 200:
                print(f"   ✅ {name}: 正常 ({len(response.data)} bytes)")
            else:
                print(f"   ❌ {name}: エラー ({response.status_code})")
        
        print("\n4. 新しいJavaScriptファイルの内容確認")
        js_response = client.get('/static/js/simple_map.js')
        if js_response.status_code == 200:
            js_content = js_response.data.decode('utf-8')
            
            # 重要な関数とクラスの存在確認
            js_checks = [
                ('SimpleJapanMapクラス', 'class SimpleJapanMap'),
                ('generateGridBasedMap関数', 'generateGridBasedMap'),
                ('onPrefectureClick関数', 'onPrefectureClick'),
                ('47都道府県の定義', '沖縄県'),
                ('クリックイベント', 'on(\'click\''),
                ('ツールチップ機能', 'showTooltip')
            ]
            
            for name, pattern in js_checks:
                if pattern in js_content:
                    print(f"   ✅ {name}: 実装済み")
                else:
                    print(f"   ❌ {name}: 未実装")
        
        print("\n=== テスト完了 ===")
        print("ブラウザで http://localhost:5000 にアクセスして地図を確認してください")
        print("- 47都道府県すべてが表示されているか")
        print("- 都道府県をクリックして情報が表示されるか")
        print("- ホバー時にツールチップが表示されるか")
        print("- モノクロデザインが適用されているか")

if __name__ == '__main__':
    test_visual_functionality()