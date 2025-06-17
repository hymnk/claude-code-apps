"""
メイン予測クラス
"""

from typing import List, Dict
from ..data.fetcher import DataFetcher
from ..analysis.frequency import FrequencyAnalyzer
from ..analysis.pattern import PatternAnalyzer
from ..prediction.strategies import PredictionStrategies
from ..prediction.advanced_engine import AdvancedPredictionEngine


class Loto6Predictor:
    """ロト6予測メインクラス"""
    
    def __init__(self):
        self.data = []
        self.analysis_results = {}
        self.data_fetcher = DataFetcher()
        self.advanced_engine = None
    
    def fetch_historical_data(self) -> List[Dict]:
        """過去のロト6当選番号データをCSVから取得"""
        try:
            csv_data = self.data_fetcher.fetch_csv_data()
            self.data = self.data_fetcher.parse_csv_to_draw_data(csv_data)
            return self.data
        except Exception:
            # フォールバック
            self.data = self.data_fetcher.get_sample_data()
            return self.data
    
    def analyze_frequency(self) -> Dict:
        """番号の出現頻度を分析"""
        analyzer = FrequencyAnalyzer(self.data)
        analysis = analyzer.analyze_frequency()
        self.analysis_results["frequency"] = analysis
        return analysis
    
    def analyze_patterns(self) -> Dict:
        """パターン分析"""
        analyzer = PatternAnalyzer(self.data)
        analysis = analyzer.analyze_patterns()
        self.analysis_results["patterns"] = analysis
        return analysis
    
    def predict_numbers(self) -> Dict:
        """高度な予測番号を生成（信頼度順）"""
        if not self.analysis_results:
            self.analyze_frequency()
            self.analyze_patterns()
        
        # 高度な予測エンジンを初期化
        self.advanced_engine = AdvancedPredictionEngine(
            self.data,
            self.analysis_results["frequency"],
            self.analysis_results["patterns"]
        )
        
        # 高度な予測を実行
        return self.advanced_engine.generate_predictions()
    
    def get_best_prediction(self) -> Dict:
        """最も信頼度の高い予測を取得"""
        predictions = self.predict_numbers()
        
        # 信頼度が最も高い予測を選択
        best_method = None
        best_confidence = -1
        
        for method, data in predictions.items():
            confidence = data["confidence"]["overall_confidence"]
            if confidence > best_confidence:
                best_confidence = confidence
                best_method = method
        
        if best_method:
            return {
                "method": best_method,
                "numbers": predictions[best_method]["numbers"],
                "confidence": predictions[best_method]["confidence"],
                "rank": 1
            }
        else:
            return None
    
    def get_frequency_data_for_chart(self):
        """チャート表示用の頻度データを取得"""
        if "frequency" not in self.analysis_results:
            self.analyze_frequency()
        
        analyzer = FrequencyAnalyzer(self.data)
        return analyzer.get_frequency_data_for_chart()
    
    def get_recent_draws(self, count: int = 10) -> List[Dict]:
        """直近の抽選結果を取得"""
        return self.data[:count] if self.data else []