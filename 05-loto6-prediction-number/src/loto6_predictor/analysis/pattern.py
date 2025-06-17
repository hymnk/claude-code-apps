"""
パターン分析モジュール
"""

import statistics
from typing import List, Dict


class PatternAnalyzer:
    """パターン分析クラス"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
    
    def analyze_patterns(self) -> Dict:
        """パターン分析（連続番号、奇偶バランス等）"""
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
        
        return {
            "consecutive_avg": statistics.mean(consecutive_patterns) if consecutive_patterns else 0,
            "consecutive_patterns": consecutive_patterns,
            "odd_even_distribution": {
                "avg_odd": statistics.mean([p["odd"] for p in odd_even_patterns]) if odd_even_patterns else 3,
                "avg_even": statistics.mean([p["even"] for p in odd_even_patterns]) if odd_even_patterns else 3
            },
            "sum_stats": {
                "avg": statistics.mean(sum_patterns) if sum_patterns else 132,
                "min": min(sum_patterns) if sum_patterns else 21,
                "max": max(sum_patterns) if sum_patterns else 258,
                "median": statistics.median(sum_patterns) if sum_patterns else 132
            }
        }