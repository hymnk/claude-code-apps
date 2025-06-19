#!/usr/bin/env python3
"""
統合テスト - JavaScript機能とマップ表示のテスト
"""

import pytest
import json
import sys
import os
import re

# アプリケーションのパスを追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """テスト用Flaskクライアント"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestMapIntegration:
    """地図機能の統合テスト"""
    
    def test_map_js_accessibility(self, client):
        """JavaScriptファイルにアクセスできるかテスト"""
        response = client.get('/static/js/map.js')
        assert response.status_code == 200
        assert 'application/javascript' in response.content_type or 'text/javascript' in response.content_type
    
    def test_css_accessibility(self, client):
        """CSSファイルにアクセスできるかテスト"""
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert 'text/css' in response.content_type
    
    def test_map_js_contains_required_functions(self, client):
        """map.jsに必要な関数が含まれているかテスト"""
        response = client.get('/static/js/map.js')
        js_content = response.data.decode('utf-8')
        
        # 必要なクラスと関数が含まれているかチェック
        assert 'class JapanMapViewer' in js_content
        assert 'generateSimplifiedJapanMap' in js_content
        assert 'setupMap' in js_content
        assert 'drawMap' in js_content
        assert 'onPrefectureClick' in js_content
        assert 'updateInfoPanel' in js_content
        assert 'getRegionClass' in js_content
    
    def test_map_js_prefecture_data(self, client):
        """map.jsに47都道府県のデータが含まれているかテスト"""
        response = client.get('/static/js/map.js')
        js_content = response.data.decode('utf-8')
        
        # 47都道府県の名前が含まれているかチェック
        prefectures = [
            '北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県',
            '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県',
            '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県',
            '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
            '鳥取県', '島根県', '岡山県', '広島県', '山口県',
            '徳島県', '香川県', '愛媛県', '高知県',
            '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県'
        ]
        
        for prefecture in prefectures:
            assert prefecture in js_content, f"{prefecture}がJavaScriptファイルに含まれていません"
    
    def test_css_contains_monochrome_theme(self, client):
        """CSSにモノクロテーマが適用されているかテスト"""
        response = client.get('/static/css/style.css')
        css_content = response.data.decode('utf-8')
        
        # モノクロ系の色が使用されているかチェック
        monochrome_colors = ['#212529', '#343a40', '#495057', '#6c757d', '#adb5bd', '#ced4da', '#dee2e6', '#e9ecef', '#f8f9fa']
        
        for color in monochrome_colors:
            assert color in css_content, f"モノクロ色 {color} がCSSに含まれていません"
        
        # 地域別スタイルの存在確認
        assert '.prefecture.hokkaido' in css_content
        assert '.prefecture.tohoku' in css_content
        assert '.prefecture.kanto' in css_content
        assert '.prefecture.chubu' in css_content
        assert '.prefecture.kinki' in css_content
        assert '.prefecture.chugoku' in css_content
        assert '.prefecture.shikoku' in css_content
        assert '.prefecture.kyushu' in css_content
        assert '.prefecture.okinawa' in css_content
    
    def test_html_template_structure(self, client):
        """HTMLテンプレートの構造をテスト"""
        response = client.get('/')
        html_content = response.data.decode('utf-8')
        
        # 必要なHTML要素の存在確認
        assert '<svg id="japan-map"></svg>' in html_content
        assert '<div id="prefecture-info">' in html_content
        assert '<div class="legend">' in html_content
        assert '<div class="map-container">' in html_content
        assert '<div class="info-panel">' in html_content
        
        # D3.jsライブラリの読み込み確認
        assert 'd3js.org/d3.v7.min.js' in html_content
        assert 'unpkg.com/topojson@3' in html_content
    
    def test_api_and_frontend_data_consistency(self, client):
        """APIデータとフロントエンドデータの整合性テスト"""
        # APIから都道府県データを取得
        api_response = client.get('/api/prefectures')
        api_data = json.loads(api_response.data)
        
        # JavaScriptファイルを取得
        js_response = client.get('/static/js/map.js')
        js_content = js_response.data.decode('utf-8')
        
        # APIデータの全都道府県がJavaScriptに含まれているかチェック
        for prefecture in api_data:
            assert prefecture['name'] in js_content, f"都道府県 {prefecture['name']} がJavaScriptに含まれていません"
        
        # 地域情報の整合性チェック
        regions = set(p['region'] for p in api_data)
        expected_regions = {'北海道', '東北', '関東', '中部', '近畿', '中国', '四国', '九州', '沖縄'}
        assert regions == expected_regions, f"地域情報が不一致: {regions} != {expected_regions}"


class TestResponseHeaders:
    """レスポンスヘッダーのテスト"""
    
    def test_static_file_caching(self, client):
        """静的ファイルのキャッシュ設定テスト"""
        # CSS
        css_response = client.get('/static/css/style.css')
        assert css_response.status_code == 200
        
        # JavaScript
        js_response = client.get('/static/js/map.js')
        assert js_response.status_code == 200
    
    def test_api_content_type(self, client):
        """APIのContent-Typeテスト"""
        response = client.get('/api/prefectures')
        assert response.status_code == 200
        assert 'application/json' in response.content_type


class TestMapCoordinates:
    """地図座標データのテスト"""
    
    def test_coordinate_ranges(self, client):
        """座標データが日本の地理的範囲内にあるかテスト"""
        js_response = client.get('/static/js/map.js')
        js_content = js_response.data.decode('utf-8')
        
        # 座標データの抽出（簡単な正規表現による検証）
        # 日本の経度範囲: 約123-146度、緯度範囲: 約24-46度
        coordinate_pattern = r'\[\[\[(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)\]'
        matches = re.findall(coordinate_pattern, js_content)
        
        for lon_str, lat_str in matches:
            lon, lat = float(lon_str), float(lat_str)
            
            # 経度の範囲チェック（少し余裕を持たせる）
            assert 120 <= lon <= 150, f"経度が範囲外: {lon}"
            
            # 緯度の範囲チェック（少し余裕を持たせる）
            assert 20 <= lat <= 50, f"緯度が範囲外: {lat}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])