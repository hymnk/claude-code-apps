#!/usr/bin/env python3
"""
Flask アプリケーションのテスト
"""

import pytest
import json
import sys
import os

# アプリケーションのパスを追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """テスト用Flaskクライアント"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestFlaskRoutes:
    """Flask ルートのテストクラス"""
    
    def test_index_route(self, client):
        """メインページのテスト"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        assert '日本地図ブラウザ'.encode('utf-8') in response.data
        assert b'japan-map' in response.data  # SVG要素のID
    
    def test_index_contains_required_elements(self, client):
        """HTMLに必要な要素が含まれているかテスト"""
        response = client.get('/')
        html_content = response.data.decode('utf-8')
        
        # 必要な要素がHTMLに含まれているかチェック
        assert 'id="japan-map"' in html_content
        assert 'static/css/style.css' in html_content
        assert 'static/js/map.js' in html_content
        assert 'https://d3js.org/d3.v7.min.js' in html_content
        assert 'https://unpkg.com/topojson@3' in html_content
    
    def test_prefectures_api(self, client):
        """都道府県APIのテスト"""
        response = client.get('/api/prefectures')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        # JSONデータの検証
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 47  # 47都道府県
        
        # 最初の都道府県データの構造をチェック
        hokkaido = data[0]
        assert hokkaido['name'] == '北海道'
        assert hokkaido['code'] == '01'
        assert hokkaido['region'] == '北海道'
        
        # 東京都を探してチェック
        tokyo = next((p for p in data if p['name'] == '東京都'), None)
        assert tokyo is not None
        assert tokyo['code'] == '13'
        assert tokyo['region'] == '関東'
        
        # 沖縄県を探してチェック
        okinawa = next((p for p in data if p['name'] == '沖縄県'), None)
        assert okinawa is not None
        assert okinawa['code'] == '47'
        assert okinawa['region'] == '沖縄'
    
    def test_prefectures_api_data_integrity(self, client):
        """都道府県APIデータの整合性テスト"""
        response = client.get('/api/prefectures')
        data = json.loads(response.data)
        
        # 全ての都道府県にname, code, regionが含まれているかチェック
        for prefecture in data:
            assert 'name' in prefecture
            assert 'code' in prefecture
            assert 'region' in prefecture
            assert isinstance(prefecture['name'], str)
            assert isinstance(prefecture['code'], str)
            assert isinstance(prefecture['region'], str)
            assert len(prefecture['name']) > 0
            assert len(prefecture['code']) == 2
            assert len(prefecture['region']) > 0
        
        # コードが01-47の範囲内でユニークかチェック
        codes = [p['code'] for p in data]
        assert len(set(codes)) == 47  # ユニークであること
        assert all(code.isdigit() and 1 <= int(code) <= 47 for code in codes)
    
    def test_nonexistent_route(self, client):
        """存在しないルートのテスト"""
        response = client.get('/nonexistent')
        assert response.status_code == 404


class TestAppConfiguration:
    """アプリケーション設定のテスト"""
    
    def test_app_exists(self):
        """アプリケーションが存在するかテスト"""
        assert app is not None
    
    def test_app_config(self):
        """アプリケーション設定のテスト"""
        assert app.config is not None
        # テスト時以外はDEBUGがFalseであることを確認
        if not app.config.get('TESTING'):
            assert app.config.get('DEBUG') is None or app.config.get('DEBUG') is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])