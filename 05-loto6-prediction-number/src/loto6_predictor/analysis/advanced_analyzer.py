"""
高度な分析アルゴリズムモジュール
"""

import numpy as np
import statistics
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import math


class AdvancedAnalyzer:
    """高度な分析アルゴリズムクラス"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
        self.features = {}
    
    def extract_advanced_features(self) -> Dict:
        """高度な特徴量を抽出"""
        features = {}
        
        # 基本特徴量
        features.update(self._extract_temporal_features())
        features.update(self._extract_numerical_features())
        features.update(self._extract_pattern_features())
        features.update(self._extract_statistical_features())
        
        self.features = features
        return features
    
    def _extract_temporal_features(self) -> Dict:
        """時系列特徴量を抽出"""
        features = {}
        
        # 短期トレンド (直近10回)
        recent_data = self.data[:10]
        recent_numbers = [num for draw in recent_data for num in draw["numbers"]]
        recent_freq = Counter(recent_numbers)
        
        # 中期トレンド (直近50回)
        medium_data = self.data[:50] if len(self.data) >= 50 else self.data
        medium_numbers = [num for draw in medium_data for num in draw["numbers"]]
        medium_freq = Counter(medium_numbers)
        
        # 長期トレンド (全データ)
        all_numbers = [num for draw in self.data for num in draw["numbers"]]
        long_freq = Counter(all_numbers)
        
        features["short_term_trend"] = dict(recent_freq)
        features["medium_term_trend"] = dict(medium_freq)
        features["long_term_trend"] = dict(long_freq)
        
        # トレンド変化率
        features["trend_changes"] = self._calculate_trend_changes(recent_freq, medium_freq, long_freq)
        
        return features
    
    def _extract_numerical_features(self) -> Dict:
        """数値的特徴量を抽出"""
        features = {}
        
        number_distances = []
        sum_variations = []
        range_variations = []
        
        for draw in self.data:
            numbers = sorted(draw["numbers"])
            
            # 数字間の距離
            distances = [numbers[i+1] - numbers[i] for i in range(5)]
            number_distances.extend(distances)
            
            # 合計値の変動
            sum_variations.append(sum(numbers))
            
            # 数値範囲の変動
            range_variations.append(max(numbers) - min(numbers))
        
        features["avg_distance"] = statistics.mean(number_distances)
        features["distance_variance"] = statistics.variance(number_distances) if len(number_distances) > 1 else 0
        features["sum_trend"] = self._calculate_moving_average(sum_variations, 5)
        features["range_trend"] = self._calculate_moving_average(range_variations, 5)
        
        return features
    
    def _extract_pattern_features(self) -> Dict:
        """パターン特徴量を抽出"""
        features = {}
        
        # 連続性パターン
        consecutive_patterns = []
        # 対称性パターン
        symmetry_scores = []
        # 区間分布パターン
        zone_distributions = []
        
        for draw in self.data:
            numbers = sorted(draw["numbers"])
            
            # 連続番号のパターン
            consecutive_count = sum(1 for i in range(5) if numbers[i+1] - numbers[i] == 1)
            consecutive_patterns.append(consecutive_count)
            
            # 対称性スコア (1-43の中心からの偏差)
            center = 22
            symmetry = sum(abs(num - center) for num in numbers) / 6
            symmetry_scores.append(symmetry)
            
            # 区間分布 (1-10, 11-20, 21-30, 31-43)
            zones = [0, 0, 0, 0]
            for num in numbers:
                if num <= 10:
                    zones[0] += 1
                elif num <= 20:
                    zones[1] += 1
                elif num <= 30:
                    zones[2] += 1
                else:
                    zones[3] += 1
            zone_distributions.append(zones)
        
        features["consecutive_frequency"] = statistics.mean(consecutive_patterns)
        features["symmetry_score"] = statistics.mean(symmetry_scores)
        features["zone_balance"] = self._calculate_zone_balance(zone_distributions)
        
        return features
    
    def _extract_statistical_features(self) -> Dict:
        """統計的特徴量を抽出"""
        features = {}
        
        # 各番号の統計的指標
        number_stats = defaultdict(list)
        
        for i, draw in enumerate(self.data):
            for num in draw["numbers"]:
                number_stats[num].append(i)  # 出現位置（時間軸）
        
        # エントロピー計算
        all_numbers = [num for draw in self.data for num in draw["numbers"]]
        freq_dist = Counter(all_numbers)
        total = sum(freq_dist.values())
        entropy = -sum((count/total) * math.log2(count/total) for count in freq_dist.values())
        
        features["entropy"] = entropy
        features["number_regularity"] = self._calculate_regularity(number_stats)
        features["deviation_from_uniform"] = self._calculate_deviation_from_uniform(freq_dist)
        
        return features
    
    def _calculate_trend_changes(self, recent: Counter, medium: Counter, long: Counter) -> Dict:
        """トレンド変化率を計算"""
        changes = {}
        
        for num in range(1, 44):
            recent_freq = recent.get(num, 0)
            medium_freq = medium.get(num, 0) / min(50, len(self.data)) * 10  # 正規化
            long_freq = long.get(num, 0) / len(self.data) * 10  # 正規化
            
            # 短期vs中期の変化率
            if medium_freq > 0:
                short_medium_change = (recent_freq - medium_freq) / medium_freq
            else:
                short_medium_change = 0
            
            # 中期vs長期の変化率
            if long_freq > 0:
                medium_long_change = (medium_freq - long_freq) / long_freq
            else:
                medium_long_change = 0
            
            changes[num] = {
                "short_medium": short_medium_change,
                "medium_long": medium_long_change
            }
        
        return changes
    
    def _calculate_moving_average(self, values: List[float], window: int) -> List[float]:
        """移動平均を計算"""
        if len(values) < window:
            return values
        
        moving_avg = []
        for i in range(len(values) - window + 1):
            avg = sum(values[i:i+window]) / window
            moving_avg.append(avg)
        
        return moving_avg
    
    def _calculate_zone_balance(self, zone_distributions: List[List[int]]) -> Dict:
        """区間バランスを計算"""
        avg_zones = [statistics.mean(zone) for zone in zip(*zone_distributions)]
        variance_zones = [statistics.variance(zone) if len(zone) > 1 else 0 
                         for zone in zip(*zone_distributions)]
        
        return {
            "average_distribution": avg_zones,
            "variance_distribution": variance_zones,
            "balance_score": 1.0 / (1.0 + sum(variance_zones))  # 低い分散 = 高いバランス
        }
    
    def _calculate_regularity(self, number_stats: Dict) -> Dict:
        """数字の規則性を計算"""
        regularity_scores = {}
        
        for num, positions in number_stats.items():
            if len(positions) > 1:
                # 出現間隔の分散
                intervals = [positions[i] - positions[i+1] for i in range(len(positions)-1)]
                if intervals:
                    regularity_scores[num] = 1.0 / (1.0 + statistics.variance(intervals))
                else:
                    regularity_scores[num] = 0.0
            else:
                regularity_scores[num] = 0.0
        
        return regularity_scores
    
    def _calculate_deviation_from_uniform(self, freq_dist: Counter) -> float:
        """均等分布からの偏差を計算"""
        expected_freq = sum(freq_dist.values()) / 43  # 43個の数字
        chi_square = sum((freq - expected_freq) ** 2 / expected_freq 
                        for freq in freq_dist.values())
        return chi_square
    
    def calculate_pattern_similarity(self, pattern1: List[int], pattern2: List[int]) -> float:
        """パターン類似度を計算"""
        if len(pattern1) != len(pattern2):
            return 0.0
        
        # ユークリッド距離の逆数
        distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(pattern1, pattern2)))
        similarity = 1.0 / (1.0 + distance)
        
        return similarity
    
    def find_similar_patterns(self, target_pattern: List[int], top_k: int = 10) -> List[Tuple[int, float]]:
        """類似パターンを検索"""
        similarities = []
        
        for i, draw in enumerate(self.data):
            similarity = self.calculate_pattern_similarity(target_pattern, draw["numbers"])
            similarities.append((i, similarity))
        
        # 類似度順にソート
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]