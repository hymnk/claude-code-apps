"""
予測戦略モジュール
"""

import numpy as np
from collections import Counter
from typing import List, Dict


class PredictionStrategies:
    """予測戦略クラス"""
    
    def __init__(self, data: List[Dict], freq_analysis: Dict, pattern_analysis: Dict):
        self.data = data
        self.freq_analysis = freq_analysis
        self.pattern_analysis = pattern_analysis
    
    def predict_numbers(self) -> Dict:
        """複数の手法を組み合わせて次回の当選番号を予測"""
        # 基本パラメータ
        high_freq_numbers = [num for num, _ in self.freq_analysis["most_common"][:20]]
        low_freq_numbers = [num for num, _ in self.freq_analysis["least_common"][:20]]
        target_odd_count = round(self.pattern_analysis["odd_even_distribution"]["avg_odd"])
        target_sum = round(self.pattern_analysis["sum_stats"]["avg"])
        
        # 予測番号生成
        predictions = {}
        
        # 予測1: 高頻度番号重視
        predictions["high_frequency"] = self._generate_balanced_prediction(
            high_freq_numbers, target_odd_count, target_sum
        )
        
        # 予測2: 低頻度番号重視（逆張り）
        predictions["low_frequency"] = self._generate_balanced_prediction(
            low_freq_numbers, target_odd_count, target_sum
        )
        
        # 予測3: バランス重視
        all_numbers = list(range(1, 44))
        predictions["balanced"] = self._generate_balanced_prediction(
            all_numbers, target_odd_count, target_sum
        )
        
        # 予測4: 最新トレンド重視
        recent_numbers = []
        for draw in self.data[-3:]:  # 直近3回
            recent_numbers.extend(draw["numbers"])
        recent_freq = Counter(recent_numbers)
        trending_numbers = [num for num, _ in recent_freq.most_common(20)]
        predictions["trending"] = self._generate_balanced_prediction(
            trending_numbers, target_odd_count, target_sum
        )
        
        return predictions
    
    def _generate_balanced_prediction(self, candidate_numbers: List[int], 
                                    target_odd_count: int, target_sum: int) -> List[int]:
        """バランスを考慮した予測番号を生成"""
        prediction = []
        attempts = 0
        max_attempts = 1000
        
        while len(prediction) < 6 and attempts < max_attempts:
            attempts += 1
            
            # ランダムに候補から選択
            available = [n for n in candidate_numbers if n not in prediction]
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