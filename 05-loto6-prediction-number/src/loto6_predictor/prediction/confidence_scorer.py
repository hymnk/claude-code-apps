"""
信頼度スコアリングシステム
"""

import numpy as np
import statistics
from collections import Counter
from typing import List, Dict, Tuple
import math


class ConfidenceScorer:
    """信頼度スコアリングクラス"""
    
    def __init__(self, data: List[Dict], advanced_features: Dict):
        self.data = data
        self.features = advanced_features
        self.method_weights = {
            "frequency_analysis": 0.25,
            "pattern_matching": 0.30,
            "trend_analysis": 0.25,
            "statistical_validation": 0.20
        }
    
    def calculate_prediction_confidence(self, prediction: List[int], method: str) -> Dict:
        """予測の信頼度を計算"""
        confidence_score = 0.0
        details = {}
        
        # 1. 頻度分析ベースの信頼度
        freq_confidence = self._calculate_frequency_confidence(prediction)
        details["frequency_confidence"] = freq_confidence
        
        # 2. パターンマッチング信頼度
        pattern_confidence = self._calculate_pattern_confidence(prediction)
        details["pattern_confidence"] = pattern_confidence
        
        # 3. トレンド分析信頼度
        trend_confidence = self._calculate_trend_confidence(prediction)
        details["trend_confidence"] = trend_confidence
        
        # 4. 統計的妥当性
        statistical_confidence = self._calculate_statistical_confidence(prediction)
        details["statistical_confidence"] = statistical_confidence
        
        # 総合信頼度計算
        confidence_score = (
            freq_confidence * self.method_weights["frequency_analysis"] +
            pattern_confidence * self.method_weights["pattern_matching"] +
            trend_confidence * self.method_weights["trend_analysis"] +
            statistical_confidence * self.method_weights["statistical_validation"]
        )
        
        # メソッド固有の調整
        method_bonus = self._get_method_bonus(method)
        confidence_score += method_bonus
        
        # スコア正規化 (0-100)
        confidence_score = max(0, min(100, confidence_score * 100))
        
        return {
            "overall_confidence": confidence_score,
            "details": details,
            "method_bonus": method_bonus,
            "interpretation": self._interpret_confidence(confidence_score)
        }
    
    def _calculate_frequency_confidence(self, prediction: List[int]) -> float:
        """頻度分析ベースの信頼度"""
        all_numbers = [num for draw in self.data for num in draw["numbers"]]
        freq_counter = Counter(all_numbers)
        total_draws = len(self.data)
        
        # 予測番号の出現頻度分析
        freq_scores = []
        for num in prediction:
            actual_freq = freq_counter.get(num, 0)
            expected_freq = total_draws * 6 / 43  # 理論上の期待出現回数
            
            # 頻度の妥当性（適度に出現している番号が高スコア）
            if expected_freq > 0:
                freq_ratio = actual_freq / expected_freq
                # 0.7-1.3の範囲で高スコア
                if 0.7 <= freq_ratio <= 1.3:
                    score = 1.0 - abs(freq_ratio - 1.0) / 0.3
                else:
                    score = max(0, 1.0 - abs(freq_ratio - 1.0) / 2.0)
            else:
                score = 0.0
            
            freq_scores.append(score)
        
        return statistics.mean(freq_scores)
    
    def _calculate_pattern_confidence(self, prediction: List[int]) -> float:
        """パターンマッチング信頼度"""
        pattern_scores = []
        
        # 1. 奇偶バランス
        odd_count = sum(1 for num in prediction if num % 2 == 1)
        ideal_odd = 3  # 理想的な奇数の数
        odd_score = 1.0 - abs(odd_count - ideal_odd) / 3.0
        pattern_scores.append(odd_score)
        
        # 2. 合計値の妥当性
        total_sum = sum(prediction)
        # 過去の合計値の統計
        past_sums = [sum(draw["numbers"]) for draw in self.data]
        avg_sum = statistics.mean(past_sums)
        std_sum = statistics.stdev(past_sums) if len(past_sums) > 1 else 1
        
        # 1.5標準偏差以内なら高スコア
        sum_deviation = abs(total_sum - avg_sum) / std_sum
        sum_score = max(0, 1.0 - sum_deviation / 1.5)
        pattern_scores.append(sum_score)
        
        # 3. 数字間隔の妥当性
        sorted_pred = sorted(prediction)
        distances = [sorted_pred[i+1] - sorted_pred[i] for i in range(5)]
        avg_distance = statistics.mean(distances)
        ideal_distance = 42 / 6  # 理論上の平均間隔
        distance_score = max(0, 1.0 - abs(avg_distance - ideal_distance) / ideal_distance)
        pattern_scores.append(distance_score)
        
        # 4. 連続番号の適切性
        consecutive_count = sum(1 for i in range(5) if distances[i] == 1)
        # 0-1個の連続番号が理想的
        consecutive_score = 1.0 if consecutive_count <= 1 else max(0, 1.0 - (consecutive_count - 1) * 0.3)
        pattern_scores.append(consecutive_score)
        
        return statistics.mean(pattern_scores)
    
    def _calculate_trend_confidence(self, prediction: List[int]) -> float:
        """トレンド分析信頼度"""
        if "trend_changes" not in self.features:
            return 0.5  # デフォルト値
        
        trend_scores = []
        trend_changes = self.features["trend_changes"]
        
        for num in prediction:
            if num in trend_changes:
                change_data = trend_changes[num]
                
                # 短期トレンドの上昇傾向があれば高スコア
                short_medium = change_data["short_medium"]
                medium_long = change_data["medium_long"]
                
                # 上昇トレンドは正のスコア、下降は負のスコア
                trend_score = 0.5 + (short_medium + medium_long) / 4.0
                trend_score = max(0, min(1, trend_score))
            else:
                trend_score = 0.5
            
            trend_scores.append(trend_score)
        
        return statistics.mean(trend_scores)
    
    def _calculate_statistical_confidence(self, prediction: List[int]) -> float:
        """統計的妥当性の信頼度"""
        stat_scores = []
        
        # 1. カイ二乗検定ベースのスコア
        if "deviation_from_uniform" in self.features:
            # 予測が均等分布からどれくらい離れているか
            deviation = self.features["deviation_from_uniform"]
            # 適度な偏差（完全に均等でも、極端に偏っていてもダメ）
            ideal_deviation = 50  # 調整可能な閾値
            deviation_score = max(0, 1.0 - abs(deviation - ideal_deviation) / ideal_deviation)
            stat_scores.append(deviation_score)
        
        # 2. エントロピーベースのスコア
        if "entropy" in self.features:
            entropy = self.features["entropy"]
            # 情報エントロピーが高いほど良い（予測困難だが、偏りが少ない）
            max_entropy = math.log2(43)  # 43個の数字の最大エントロピー
            entropy_score = entropy / max_entropy
            stat_scores.append(entropy_score)
        
        # 3. 予測番号の分散
        variance = statistics.variance(prediction)
        # 適度な分散が理想的
        ideal_variance = 150  # 調整可能
        variance_score = max(0, 1.0 - abs(variance - ideal_variance) / ideal_variance)
        stat_scores.append(variance_score)
        
        return statistics.mean(stat_scores) if stat_scores else 0.5
    
    def _get_method_bonus(self, method: str) -> float:
        """メソッド固有のボーナス"""
        bonuses = {
            "high_frequency": 0.0,     # 標準
            "low_frequency": -0.05,    # やや不利（逆張りリスク）
            "balanced": 0.05,          # やや有利（バランス重視）
            "trending": 0.03,          # やや有利（最新トレンド）
            "advanced_ensemble": 0.10, # 最も有利（高度な統合手法）
        }
        return bonuses.get(method, 0.0)
    
    def _interpret_confidence(self, score: float) -> str:
        """信頼度の解釈"""
        if score >= 80:
            return "非常に高い信頼度"
        elif score >= 70:
            return "高い信頼度"
        elif score >= 60:
            return "中程度の信頼度"
        elif score >= 50:
            return "やや低い信頼度"
        else:
            return "低い信頼度"
    
    def rank_predictions(self, predictions: Dict[str, List[int]]) -> List[Tuple[str, List[int], Dict]]:
        """予測を信頼度順にランキング"""
        ranked_predictions = []
        
        for method, numbers in predictions.items():
            confidence_data = self.calculate_prediction_confidence(numbers, method)
            ranked_predictions.append((method, numbers, confidence_data))
        
        # 信頼度順にソート
        ranked_predictions.sort(key=lambda x: x[2]["overall_confidence"], reverse=True)
        
        return ranked_predictions