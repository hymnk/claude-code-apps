"""
頻度分析モジュール
"""

import statistics
from collections import Counter
from typing import List, Dict


class FrequencyAnalyzer:
    """頻度分析クラス"""
    
    def __init__(self, data: List[Dict]):
        self.data = data
    
    def analyze_frequency(self) -> Dict:
        """番号の出現頻度を分析"""
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
        
        return {
            "number_frequency": dict(number_freq),
            "bonus_frequency": dict(bonus_freq),
            "most_common": most_common,
            "least_common": least_common,
            "average_frequency": statistics.mean(number_freq.values()) if number_freq else 0
        }
    
    def get_frequency_data_for_chart(self) -> tuple:
        """チャート表示用の頻度データを取得"""
        freq_analysis = self.analyze_frequency()
        freq_data = freq_analysis["number_frequency"]
        numbers = list(range(1, 44))
        frequencies = [freq_data.get(num, 0) for num in numbers]
        return numbers, frequencies