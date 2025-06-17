"""
高度な予測エンジン
"""

import numpy as np
import statistics
from collections import Counter, defaultdict
from typing import List, Dict, Tuple
from .strategies import PredictionStrategies
from .confidence_scorer import ConfidenceScorer
from ..analysis.advanced_analyzer import AdvancedAnalyzer


class AdvancedPredictionEngine:
    """高度な予測エンジンクラス"""
    
    def __init__(self, data: List[Dict], freq_analysis: Dict, pattern_analysis: Dict):
        self.data = data
        self.freq_analysis = freq_analysis
        self.pattern_analysis = pattern_analysis
        
        # 高度な分析器
        self.advanced_analyzer = AdvancedAnalyzer(data)
        self.advanced_features = self.advanced_analyzer.extract_advanced_features()
        
        # 基本戦略エンジン
        self.basic_strategies = PredictionStrategies(data, freq_analysis, pattern_analysis)
        
        # 信頼度スコアラー
        self.confidence_scorer = ConfidenceScorer(data, self.advanced_features)
    
    def generate_predictions(self) -> Dict[str, Dict]:
        """全予測手法を実行して結果を生成"""
        predictions = {}
        
        # 1. 基本予測手法
        basic_predictions = self.basic_strategies.predict_numbers()
        
        # 2. 高度な予測手法
        advanced_predictions = self._generate_advanced_predictions()
        
        # 3. アンサンブル予測
        ensemble_prediction = self._generate_ensemble_prediction(basic_predictions, advanced_predictions)
        
        # 全予測を統合
        all_predictions = {**basic_predictions, **advanced_predictions}
        all_predictions["advanced_ensemble"] = ensemble_prediction
        
        # 4. 信頼度スコアリング
        ranked_predictions = self.confidence_scorer.rank_predictions(all_predictions)
        
        # 結果をフォーマット
        for i, (method, numbers, confidence_data) in enumerate(ranked_predictions):
            predictions[method] = {
                "numbers": numbers,
                "confidence": confidence_data,
                "rank": i + 1
            }
        
        return predictions
    
    def _generate_advanced_predictions(self) -> Dict[str, List[int]]:
        """高度な予測手法を実行"""
        predictions = {}
        
        # 1. 重み付き頻度予測
        predictions["weighted_frequency"] = self._weighted_frequency_prediction()
        
        # 2. パターン類似度予測
        predictions["pattern_similarity"] = self._pattern_similarity_prediction()
        
        # 3. トレンド統合予測
        predictions["trend_integration"] = self._trend_integration_prediction()
        
        # 4. 統計的最適化予測
        predictions["statistical_optimization"] = self._statistical_optimization_prediction()
        
        return predictions
    
    def _weighted_frequency_prediction(self) -> List[int]:
        """重み付き頻度ベース予測"""
        # 時期別の重み設定
        weights = {
            "recent": 0.5,    # 直近の重み
            "medium": 0.3,    # 中期の重み
            "long": 0.2       # 長期の重み
        }
        
        weighted_scores = defaultdict(float)
        
        # 各時期のトレンドに重みを適用
        for num in range(1, 44):
            recent_score = self.advanced_features["short_term_trend"].get(num, 0)
            medium_score = self.advanced_features["medium_term_trend"].get(num, 0)
            long_score = self.advanced_features["long_term_trend"].get(num, 0)
            
            # 正規化（回数あたりの出現頻度に変換）
            recent_normalized = recent_score / min(10, len(self.data))
            medium_normalized = medium_score / min(50, len(self.data))
            long_normalized = long_score / len(self.data)
            
            weighted_score = (
                recent_normalized * weights["recent"] +
                medium_normalized * weights["medium"] +
                long_normalized * weights["long"]
            )
            
            weighted_scores[num] = weighted_score
        
        # 上位候補から選択
        candidates = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)[:20]
        candidate_numbers = [num for num, score in candidates]
        
        return self._generate_balanced_selection(candidate_numbers)
    
    def _pattern_similarity_prediction(self) -> List[int]:
        """パターン類似度ベース予測"""
        if len(self.data) < 10:
            return self._fallback_prediction()
        
        # 直近の3回の平均パターン
        recent_patterns = self.data[:3]
        avg_pattern = []
        for i in range(6):
            avg_num = statistics.mean([draw["numbers"][i] for draw in recent_patterns])
            avg_pattern.append(int(round(avg_num)))
        
        # 類似パターンを検索
        similar_patterns = self.advanced_analyzer.find_similar_patterns(avg_pattern, top_k=10)
        
        # 類似パターンの次回抽選結果から学習
        next_numbers = []
        for pattern_index, similarity in similar_patterns:
            if pattern_index > 0:  # 最初のパターンは次がない
                next_draw = self.data[pattern_index - 1]
                next_numbers.extend(next_draw["numbers"])
        
        if not next_numbers:
            return self._fallback_prediction()
        
        # 頻度ベースで候補選択
        next_freq = Counter(next_numbers)
        candidates = [num for num, count in next_freq.most_common(20)]
        
        return self._generate_balanced_selection(candidates)
    
    def _trend_integration_prediction(self) -> List[int]:
        """トレンド統合予測"""
        trend_scores = defaultdict(float)
        
        if "trend_changes" not in self.advanced_features:
            return self._fallback_prediction()
        
        trend_changes = self.advanced_features["trend_changes"]
        
        for num, change_data in trend_changes.items():
            # 短期・中期トレンドを統合
            short_medium = change_data["short_medium"]
            medium_long = change_data["medium_long"]
            
            # トレンドスコア計算（上昇傾向を高く評価）
            trend_score = (short_medium * 0.6 + medium_long * 0.4)
            
            # 規則性も考慮
            if "number_regularity" in self.advanced_features:
                regularity = self.advanced_features["number_regularity"].get(num, 0)
                trend_score += regularity * 0.2
            
            trend_scores[num] = trend_score
        
        # 上位候補を選択
        candidates = sorted(trend_scores.items(), key=lambda x: x[1], reverse=True)[:20]
        candidate_numbers = [num for num, score in candidates]
        
        return self._generate_balanced_selection(candidate_numbers)
    
    def _statistical_optimization_prediction(self) -> List[int]:
        """統計的最適化予測"""
        # 統計的に最適な組み合わせを探索
        optimization_scores = defaultdict(float)
        
        # 基本統計指標
        all_numbers = [num for draw in self.data for num in draw["numbers"]]
        freq_counter = Counter(all_numbers)
        
        for num in range(1, 44):
            score = 0.0
            
            # 1. 期待頻度との乖離
            actual_freq = freq_counter.get(num, 0)
            expected_freq = len(self.data) * 6 / 43
            deviation_score = 1.0 - abs(actual_freq - expected_freq) / expected_freq
            score += deviation_score * 0.3
            
            # 2. エントロピー寄与度
            if self.advanced_features.get("entropy", 0) > 0:
                entropy_contribution = freq_counter.get(num, 0) / sum(freq_counter.values())
                score += entropy_contribution * 0.2
            
            # 3. 分散最適化
            recent_appearances = []
            for i, draw in enumerate(self.data[:20]):  # 直近20回
                if num in draw["numbers"]:
                    recent_appearances.append(i)
            
            if len(recent_appearances) > 1:
                variance = statistics.variance(recent_appearances)
                # 適度な分散が良い
                variance_score = 1.0 / (1.0 + abs(variance - 7.0))  # 理想分散7.0
                score += variance_score * 0.2
            
            # 4. 周期性評価
            if len(recent_appearances) > 0:
                last_appearance = recent_appearances[0]
                # 適度な間隔で出現しているか
                if 2 <= last_appearance <= 8:
                    score += 0.3
            
            optimization_scores[num] = score
        
        # 上位候補選択
        candidates = sorted(optimization_scores.items(), key=lambda x: x[1], reverse=True)[:20]
        candidate_numbers = [num for num, score in candidates]
        
        return self._generate_balanced_selection(candidate_numbers)
    
    def _generate_ensemble_prediction(self, basic_predictions: Dict, advanced_predictions: Dict) -> List[int]:
        """アンサンブル予測を生成"""
        # 全予測手法の投票
        vote_counter = Counter()
        
        # 基本手法の投票（重み1.0）
        for method, numbers in basic_predictions.items():
            for num in numbers:
                vote_counter[num] += 1.0
        
        # 高度手法の投票（重み1.5）
        for method, numbers in advanced_predictions.items():
            for num in numbers:
                vote_counter[num] += 1.5
        
        # 上位候補選択
        candidates = [num for num, votes in vote_counter.most_common(20)]
        
        return self._generate_balanced_selection(candidates)
    
    def _generate_balanced_selection(self, candidates: List[int]) -> List[int]:
        """バランスを考慮した6数字選択"""
        best_combination = None
        best_score = -1
        
        # 複数の組み合わせを試行
        for _ in range(1000):
            # ランダムに6つ選択
            if len(candidates) >= 6:
                selected = sorted(np.random.choice(candidates, 6, replace=False))
            else:
                # 候補が少ない場合は全体から選択
                selected = sorted(np.random.choice(range(1, 44), 6, replace=False))
            
            # バランススコア計算
            score = self._calculate_balance_score(selected)
            
            if score > best_score:
                best_score = score
                best_combination = selected
        
        return best_combination if best_combination else sorted(np.random.choice(range(1, 44), 6, replace=False))
    
    def _calculate_balance_score(self, numbers: List[int]) -> float:
        """組み合わせのバランススコア"""
        score = 0.0
        
        # 1. 奇偶バランス
        odd_count = sum(1 for num in numbers if num % 2 == 1)
        if 2 <= odd_count <= 4:
            score += 1.0
        
        # 2. 合計値
        total_sum = sum(numbers)
        if 120 <= total_sum <= 150:
            score += 1.0
        
        # 3. 分散
        variance = statistics.variance(numbers)
        if 100 <= variance <= 200:
            score += 1.0
        
        # 4. 連続番号
        consecutive_count = sum(1 for i in range(5) if numbers[i+1] - numbers[i] == 1)
        if consecutive_count <= 1:
            score += 1.0
        
        # 5. 区間分布
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
        
        # 各区間に最低1つずつあれば高スコア
        if all(zone > 0 for zone in zones):
            score += 1.0
        
        return score
    
    def _fallback_prediction(self) -> List[int]:
        """フォールバック予測"""
        return sorted(np.random.choice(range(1, 44), 6, replace=False))