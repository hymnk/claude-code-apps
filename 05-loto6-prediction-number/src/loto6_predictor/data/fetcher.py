"""
データ取得モジュール
"""

import requests
from typing import List, Dict


class DataFetcher:
    """ロト6データ取得クラス"""
    
    def __init__(self, url: str = "https://loto6.thekyo.jp/data/loto6.csv"):
        self.url = url
    
    def fetch_csv_data(self) -> str:
        """CSVデータを取得"""
        try:
            response = requests.get(self.url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except requests.RequestException as e:
            raise Exception(f"データ取得エラー: {e}")
    
    def parse_csv_to_draw_data(self, csv_data: str, limit: int = 1000) -> List[Dict]:
        """CSVデータを抽選データに変換"""
        lines = csv_data.strip().split('\n')
        data_lines = lines[1:]  # ヘッダーをスキップ
        
        # データを新しい順（最新から古い順）にソート
        data_lines.reverse()
        recent_lines = data_lines[:limit]  # 最新から指定回数分
        
        parsed_data = []
        for line in recent_lines:
            columns = line.split(',')
            if len(columns) >= 8:
                try:
                    draw_date = columns[1]
                    numbers = [
                        int(columns[2]), int(columns[3]), int(columns[4]),
                        int(columns[5]), int(columns[6]), int(columns[7])
                    ]
                    bonus = int(columns[8])
                    
                    parsed_data.append({
                        "draw_date": draw_date,
                        "numbers": sorted(numbers),
                        "bonus": bonus
                    })
                except (ValueError, IndexError):
                    continue
        
        return parsed_data
    
    def get_sample_data(self) -> List[Dict]:
        """フォールバック用サンプルデータ"""
        return [
            {"draw_date": "2024-01-08", "numbers": [3, 12, 18, 25, 31, 42], "bonus": 7},
            {"draw_date": "2024-01-15", "numbers": [5, 14, 22, 28, 35, 41], "bonus": 19},
            {"draw_date": "2024-01-22", "numbers": [1, 9, 16, 24, 33, 43], "bonus": 11},
            {"draw_date": "2024-01-29", "numbers": [7, 15, 21, 29, 36, 40], "bonus": 2},
            {"draw_date": "2024-02-05", "numbers": [4, 11, 19, 26, 32, 39], "bonus": 8},
        ]