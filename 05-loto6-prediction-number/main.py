#!/usr/bin/env python3
"""
ロト6予測プログラム
過去の当選番号を分析して次回の当選番号を予測します
"""

import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import Counter
import statistics
from typing import List, Dict, Tuple
import re


class Loto6Predictor:
    def __init__(self):
        self.data = []
        self.analysis_results = {}
        
    def fetch_historical_data(self) -> List[Dict]:
        """
        過去のロト6当選番号データをCSVから取得
        """
        print("過去の当選番号データを取得中...")
        
        try:
            # CSVデータを取得
            url = "https://loto6.thekyo.jp/data/loto6.csv"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            # CSVデータをパース
            csv_data = response.text
            lines = csv_data.strip().split('\n')
            
            # ヘッダーをスキップして最新1000回分を取得
            data_lines = lines[1:]  # ヘッダーをスキップ
            recent_lines = data_lines[:1000]  # 最新1000回分
            
            parsed_data = []
            for line in recent_lines:
                columns = line.split(',')
                if len(columns) >= 8:  # 最低限必要な列数をチェック
                    try:
                        # CSVの形式に合わせて解析
                        draw_date = columns[1]  # 抽選日
                        numbers = [
                            int(columns[2]),  # 本数字1
                            int(columns[3]),  # 本数字2
                            int(columns[4]),  # 本数字3
                            int(columns[5]),  # 本数字4
                            int(columns[6]),  # 本数字5
                            int(columns[7])   # 本数字6
                        ]
                        bonus = int(columns[8])  # ボーナス数字
                        
                        parsed_data.append({
                            "draw_date": draw_date,
                            "numbers": sorted(numbers),
                            "bonus": bonus
                        })
                    except (ValueError, IndexError) as e:
                        print(f"データ解析エラー (行スキップ): {line[:50]}... - {e}")
                        continue
            
            self.data = parsed_data
            print(f"取得完了: {len(self.data)}回分のデータ")
            return self.data
            
        except requests.RequestException as e:
            print(f"データ取得エラー: {e}")
            print("サンプルデータで動作を継続します...")
            
            # フォールバック用サンプルデータ
            sample_data = [
                {"draw_date": "2024-01-08", "numbers": [3, 12, 18, 25, 31, 42], "bonus": 7},
                {"draw_date": "2024-01-15", "numbers": [5, 14, 22, 28, 35, 41], "bonus": 19},
                {"draw_date": "2024-01-22", "numbers": [1, 9, 16, 24, 33, 43], "bonus": 11},
                {"draw_date": "2024-01-29", "numbers": [7, 15, 21, 29, 36, 40], "bonus": 2},
                {"draw_date": "2024-02-05", "numbers": [4, 11, 19, 26, 32, 39], "bonus": 8},
            ]
            
            self.data = sample_data
            print(f"サンプルデータ: {len(self.data)}回分のデータ")
            return self.data
    
    def analyze_frequency(self) -> Dict:
        """
        番号の出現頻度を分析
        """
        print("出現頻度分析中...")
        
        all_numbers = []
        bonus_numbers = []
        
        for draw in self.data:
            all_numbers.extend(draw["numbers"])
            bonus_numbers.append(draw["bonus"])
        
        number_freq = Counter(all_numbers)
        bonus_freq = Counter(bonus_numbers)
        
        # 最頻出と最低頻出番号
        most_common = number_freq.most_common(10)
        least_common = number_freq.most_common()[-10:]
        
        analysis = {
            "number_frequency": dict(number_freq),
            "bonus_frequency": dict(bonus_freq),
            "most_common": most_common,
            "least_common": least_common,
            "average_frequency": statistics.mean(number_freq.values())
        }
        
        self.analysis_results["frequency"] = analysis
        return analysis
    
    def analyze_patterns(self) -> Dict:
        """
        パターン分析（連続番号、奇偶バランス等）
        """
        print("パターン分析中...")
        
        consecutive_patterns = []
        odd_even_patterns = []
        sum_patterns = []
        
        for draw in self.data:
            numbers = sorted(draw["numbers"])
            
            # 連続番号の検出
            consecutive_count = 0
            for i in range(len(numbers) - 1):
                if numbers[i + 1] - numbers[i] == 1:
                    consecutive_count += 1
            consecutive_patterns.append(consecutive_count)
            
            # 奇偶バランス
            odd_count = sum(1 for n in numbers if n % 2 == 1)
            odd_even_patterns.append({"odd": odd_count, "even": 6 - odd_count})
            
            # 合計値
            sum_patterns.append(sum(numbers))
        
        analysis = {
            "consecutive_avg": statistics.mean(consecutive_patterns),
            "consecutive_patterns": consecutive_patterns,
            "odd_even_distribution": {
                "avg_odd": statistics.mean([p["odd"] for p in odd_even_patterns]),
                "avg_even": statistics.mean([p["even"] for p in odd_even_patterns])
            },
            "sum_stats": {
                "avg": statistics.mean(sum_patterns),
                "min": min(sum_patterns),
                "max": max(sum_patterns),
                "median": statistics.median(sum_patterns)
            }
        }
        
        self.analysis_results["patterns"] = analysis
        return analysis
    
    def predict_numbers(self) -> Dict:
        """
        複数の手法を組み合わせて次回の当選番号を予測
        """
        print("予測計算中...")
        
        if not self.analysis_results:
            self.analyze_frequency()
            self.analyze_patterns()
        
        # 手法1: 頻度ベース予測
        freq_analysis = self.analysis_results["frequency"]
        high_freq_numbers = [num for num, _ in freq_analysis["most_common"][:20]]
        low_freq_numbers = [num for num, _ in freq_analysis["least_common"][:20]]
        
        # 手法2: パターンベース予測
        pattern_analysis = self.analysis_results["patterns"]
        target_odd_count = round(pattern_analysis["odd_even_distribution"]["avg_odd"])
        target_sum = round(pattern_analysis["sum_stats"]["avg"])
        
        # 予測番号生成
        predictions = {}
        
        # 予測1: 高頻度番号重視
        pred1 = self._generate_balanced_prediction(high_freq_numbers, target_odd_count, target_sum)
        predictions["high_frequency"] = pred1
        
        # 予測2: 低頻度番号重視（逆張り）
        pred2 = self._generate_balanced_prediction(low_freq_numbers, target_odd_count, target_sum)
        predictions["low_frequency"] = pred2
        
        # 予測3: バランス重視
        all_numbers = list(range(1, 44))
        pred3 = self._generate_balanced_prediction(all_numbers, target_odd_count, target_sum)
        predictions["balanced"] = pred3
        
        # 予測4: 最新トレンド重視
        recent_numbers = []
        for draw in self.data[-3:]:  # 直近3回
            recent_numbers.extend(draw["numbers"])
        recent_freq = Counter(recent_numbers)
        trending_numbers = [num for num, _ in recent_freq.most_common(20)]
        pred4 = self._generate_balanced_prediction(trending_numbers, target_odd_count, target_sum)
        predictions["trending"] = pred4
        
        return predictions
    
    def _generate_balanced_prediction(self, candidate_numbers: List[int], 
                                    target_odd_count: int, target_sum: int) -> List[int]:
        """
        バランスを考慮した予測番号を生成
        """
        prediction = []
        attempts = 0
        max_attempts = 1000
        
        while len(prediction) < 6 and attempts < max_attempts:
            attempts += 1
            temp_prediction = []
            
            # ランダムに候補から選択
            available = [n for n in candidate_numbers if n not in temp_prediction]
            if len(available) < 6:
                available = list(range(1, 44))
            
            temp_prediction = sorted(np.random.choice(available, 6, replace=False))
            
            # 奇偶バランスチェック
            odd_count = sum(1 for n in temp_prediction if n % 2 == 1)
            if abs(odd_count - target_odd_count) <= 1:
                # 合計値チェック
                current_sum = sum(temp_prediction)
                if abs(current_sum - target_sum) <= 30:
                    prediction = temp_prediction
                    break
        
        # バックアップ: 条件を満たせない場合はランダム
        if len(prediction) == 0:
            prediction = sorted(np.random.choice(range(1, 44), 6, replace=False))
        
        return prediction
    
    def generate_report(self, predictions: Dict) -> str:
        """
        分析結果と予測のレポートを生成
        """
        report = []
        report.append("=" * 60)
        report.append("ロト6予測分析レポート")
        report.append("=" * 60)
        report.append(f"分析日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"分析対象: {len(self.data)}回分のデータ")
        report.append("")
        
        # 頻度分析結果
        if "frequency" in self.analysis_results:
            freq = self.analysis_results["frequency"]
            report.append("【頻度分析結果】")
            report.append("出現頻度TOP10:")
            for num, count in freq["most_common"]:
                report.append(f"  {num:2d}番: {count}回")
            report.append("")
        
        # パターン分析結果
        if "patterns" in self.analysis_results:
            patterns = self.analysis_results["patterns"]
            report.append("【パターン分析結果】")
            report.append(f"連続番号平均: {patterns['consecutive_avg']:.2f}ペア")
            report.append(f"奇数平均: {patterns['odd_even_distribution']['avg_odd']:.1f}個")
            report.append(f"偶数平均: {patterns['odd_even_distribution']['avg_even']:.1f}個")
            report.append(f"合計値平均: {patterns['sum_stats']['avg']:.1f}")
            report.append("")
        
        # 予測結果
        report.append("【予測結果】")
        for method, numbers in predictions.items():
            method_name = {
                "high_frequency": "高頻度重視",
                "low_frequency": "低頻度重視",
                "balanced": "バランス重視",
                "trending": "最新トレンド"
            }.get(method, method)
            
            report.append(f"{method_name}: {' - '.join(map(str, numbers))}")
            report.append(f"  (奇数: {sum(1 for n in numbers if n % 2 == 1)}個, "
                         f"合計: {sum(numbers)})")
        
        report.append("")
        report.append("※この予測は統計分析に基づく参考値です。")
        report.append("  実際の当選を保証するものではありません。")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_results(self, predictions: Dict, filename: str = None):
        """
        結果をファイルに保存
        """
        if filename is None:
            filename = f"loto6_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # numpy型をPython標準型に変換
        def convert_numpy_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_numpy_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            return obj
        
        results = {
            "analysis_date": datetime.now().isoformat(),
            "data_count": len(self.data),
            "analysis_results": convert_numpy_types(self.analysis_results),
            "predictions": convert_numpy_types(predictions)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"結果を {filename} に保存しました")


def main():
    """
    メイン実行関数
    """
    predictor = Loto6Predictor()
    
    try:
        # データ取得と分析
        predictor.fetch_historical_data()
        predictor.analyze_frequency()
        predictor.analyze_patterns()
        
        # 予測実行
        predictions = predictor.predict_numbers()
        
        # レポート生成と表示
        report = predictor.generate_report(predictions)
        print(report)
        
        # 結果保存
        predictor.save_results(predictions)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())