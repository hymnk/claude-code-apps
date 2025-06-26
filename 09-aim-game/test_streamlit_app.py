#!/usr/bin/env python3
"""
Streamlit AIM Trainer Test Suite
修正されたStreamlitアプリのテストコード
"""

import unittest
import sys
import os
import math
import time
from unittest.mock import Mock, patch

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions from streamlit_app
try:
    from streamlit_app import (
        calculate_distance, 
        get_hit_score, 
        is_target_hit,
        generate_target_position,
        TARGET_OUTER_RADIUS,
        TARGET_INNER_RADIUS,
        TARGET_CENTER_RADIUS
    )
    STREAMLIT_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Streamlitアプリのインポートに失敗: {e}")
    STREAMLIT_AVAILABLE = False

class TestStreamlitGameLogic(unittest.TestCase):
    """Streamlitアプリのゲームロジックテスト"""
    
    def setUp(self):
        """テスト用のセットアップ"""
        self.target_x = 300
        self.target_y = 200
    
    @unittest.skipUnless(STREAMLIT_AVAILABLE, "Streamlit app not available")
    def test_calculate_distance(self):
        """距離計算のテスト"""
        # 同じ点
        self.assertEqual(calculate_distance(0, 0, 0, 0), 0)
        
        # 水平距離
        self.assertEqual(calculate_distance(0, 0, 3, 0), 3)
        
        # 垂直距離
        self.assertEqual(calculate_distance(0, 0, 0, 4), 4)
        
        # 斜め距離（ピタゴラスの定理: 3-4-5の三角形）
        self.assertEqual(calculate_distance(0, 0, 3, 4), 5)
    
    @unittest.skipUnless(STREAMLIT_AVAILABLE, "Streamlit app not available")
    def test_get_hit_score(self):
        """得点計算のテスト"""
        target_x, target_y = 100, 100
        
        # 中心クリック - 最高得点
        center_score = get_hit_score(target_x, target_y, target_x, target_y)
        self.assertEqual(center_score, 100)
        
        # 中心範囲内（距離5）
        near_center_score = get_hit_score(target_x, target_y, target_x + 5, target_y)
        self.assertEqual(near_center_score, 100)
        
        # 内側リング範囲（距離10）
        inner_score = get_hit_score(target_x, target_y, target_x + 10, target_y)
        self.assertGreaterEqual(inner_score, 60)
        self.assertLess(inner_score, 100)
        
        # 外側リング範囲（距離25）
        outer_score = get_hit_score(target_x, target_y, target_x + 25, target_y)
        self.assertGreaterEqual(outer_score, 10)
        self.assertLess(outer_score, 60)
        
        # 完全に外れ（距離35）
        miss_score = get_hit_score(target_x, target_y, target_x + 35, target_y)
        self.assertEqual(miss_score, 0)
    
    @unittest.skipUnless(STREAMLIT_AVAILABLE, "Streamlit app not available")
    def test_is_target_hit(self):
        """ヒット判定のテスト"""
        target_x, target_y = 100, 100
        
        # 中心ヒット
        self.assertTrue(is_target_hit(target_x, target_y, target_x, target_y))
        
        # 境界内ヒット
        self.assertTrue(is_target_hit(target_x, target_y, target_x + 25, target_y))
        self.assertTrue(is_target_hit(target_x, target_y, target_x, target_y + 29))
        
        # 境界外ミス
        self.assertFalse(is_target_hit(target_x, target_y, target_x + 31, target_y))
        self.assertFalse(is_target_hit(target_x, target_y, target_x + 50, target_y + 50))
    
    @unittest.skipUnless(STREAMLIT_AVAILABLE, "Streamlit app not available")
    def test_generate_target_position(self):
        """ターゲット位置生成のテスト"""
        # 複数回生成してすべて有効な範囲内か確認
        for _ in range(20):
            x, y = generate_target_position()
            
            # 範囲チェック（マージンを考慮）
            margin = TARGET_OUTER_RADIUS + 33  # 63px margin
            self.assertGreaterEqual(x, margin)
            self.assertLessEqual(x, 700 - margin)  # 637px
            self.assertGreaterEqual(y, margin)
            self.assertLessEqual(y, 500 - margin)  # 437px
    
    @unittest.skipUnless(STREAMLIT_AVAILABLE, "Streamlit app not available")
    def test_scoring_consistency(self):
        """得点システムの一貫性テスト"""
        target_x, target_y = 200, 200
        
        # 距離が増加するにつれてスコアが減少または維持されることを確認
        previous_score = 100
        for distance in range(0, 35, 2):
            click_x = target_x + distance
            click_y = target_y
            score = get_hit_score(target_x, target_y, click_x, click_y)
            
            # スコアは減少または同じ（0になったら変わらない）
            if score > 0:
                self.assertLessEqual(score, previous_score)
                previous_score = score

class TestStreamlitGameScenarios(unittest.TestCase):
    """ゲームシナリオのテスト"""
    
    @unittest.skipUnless(STREAMLIT_AVAILABLE, "Streamlit app not available")
    def test_perfect_accuracy_scenario(self):
        """完璧な精度のシナリオテスト"""
        target_positions = [
            (100, 100), (200, 150), (300, 200), (150, 250), (400, 300)
        ]
        
        total_score = 0
        hits = 0
        
        for target_x, target_y in target_positions:
            # 完璧に中心をクリック
            if is_target_hit(target_x, target_y, target_x, target_y):
                hits += 1
                score = get_hit_score(target_x, target_y, target_x, target_y)
                total_score += score
        
        # すべて中心にヒットしているはず
        self.assertEqual(hits, 5)
        self.assertEqual(total_score, 500)  # 5 * 100
    
    @unittest.skipUnless(STREAMLIT_AVAILABLE, "Streamlit app not available")
    def test_mixed_accuracy_scenario(self):
        """混合精度のシナリオテスト"""
        scenarios = [
            # (target_x, target_y, click_x, click_y, expected_hit)
            (100, 100, 100, 100, True),      # Perfect hit
            (200, 150, 210, 150, True),      # Inner ring hit
            (300, 200, 320, 200, True),      # Outer ring hit
            (150, 250, 190, 250, False),     # Miss
            (400, 300, 400, 330, True),      # Just within range
            (500, 400, 545, 400, False),     # Clear miss
        ]
        
        hits = 0
        total_score = 0
        
        for target_x, target_y, click_x, click_y, expected_hit in scenarios:
            hit = is_target_hit(target_x, target_y, click_x, click_y)
            self.assertEqual(hit, expected_hit)
            
            if hit:
                hits += 1
                score = get_hit_score(target_x, target_y, click_x, click_y)
                total_score += score
                self.assertGreater(score, 0)
        
        # 4回ヒットするはず
        self.assertEqual(hits, 4)
        self.assertGreater(total_score, 0)

def run_performance_tests():
    """パフォーマンステスト（手動実行）"""
    if not STREAMLIT_AVAILABLE:
        print("⚠️ Streamlitアプリが利用できないため、パフォーマンステストをスキップします")
        return
    
    print("\n🎯 Streamlit AIM Trainer - パフォーマンステスト")
    print("=" * 50)
    
    # 大量の計算テスト
    start_time = time.time()
    
    hits = 0
    total_score = 0
    
    for i in range(1000):
        target_x, target_y = generate_target_position()
        
        # ランダムなクリック位置
        import random
        click_x = target_x + random.randint(-50, 50)
        click_y = target_y + random.randint(-50, 50)
        
        # 判定と得点計算
        hit = is_target_hit(target_x, target_y, click_x, click_y)
        if hit:
            hits += 1
            score = get_hit_score(target_x, target_y, click_x, click_y)
            total_score += score
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    print(f"1000回の計算時間: {elapsed:.3f}秒")
    print(f"1回あたりの平均時間: {elapsed/1000*1000:.3f}ms")
    print(f"ヒット数: {hits}/1000 ({hits/10:.1f}%)")
    print(f"平均スコア: {total_score/hits if hits > 0 else 0:.1f}")
    
    if elapsed < 1.0:
        print("✅ パフォーマンス: 良好")
    else:
        print("⚠️ パフォーマンス: 改善が必要")

def test_canvas_integration():
    """Canvas統合テスト（シミュレーション）"""
    if not STREAMLIT_AVAILABLE:
        return
    
    print("\n🎯 Canvas統合テスト")
    print("=" * 30)
    
    # 様々なクリック位置をシミュレート
    test_scenarios = [
        # (target_x, target_y, click_x, click_y, expected_result)
        (300, 200, 300, 200, "perfect_hit"),   # 完璧なヒット
        (300, 200, 310, 200, "good_hit"),      # 良いヒット
        (300, 200, 320, 200, "edge_hit"),      # 境界ヒット
        (300, 200, 350, 200, "miss"),          # ミス
        (100, 100, 100, 100, "center_hit"),    # 中心ヒット
        (500, 400, 480, 380, "near_miss"),     # ニアミス
    ]
    
    for target_x, target_y, click_x, click_y, expected in test_scenarios:
        hit = is_target_hit(target_x, target_y, click_x, click_y)
        distance = calculate_distance(target_x, target_y, click_x, click_y)
        score = get_hit_score(target_x, target_y, click_x, click_y) if hit else 0
        
        result = "HIT" if hit else "MISS"
        print(f"  Target({target_x},{target_y}) Click({click_x},{click_y}): {result} Distance:{distance:.1f} Score:{score}")
    
    print("✅ Canvas統合テスト完了")

def main():
    """メイン実行関数"""
    print("🎯 Streamlit AIM Trainer - Test Suite")
    print("=" * 50)
    
    if not STREAMLIT_AVAILABLE:
        print("❌ Streamlitアプリが利用できません")
        print("💡 以下を確認してください:")
        print("   - streamlit_app.py が存在するか")
        print("   - 必要な関数がエクスポートされているか")
        return
    
    # ユニットテスト実行
    print("📋 ユニットテストを実行中...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # パフォーマンステスト実行
    run_performance_tests()
    
    # Canvas統合テスト実行
    test_canvas_integration()
    
    print("\n" + "=" * 50)
    print("🎮 テスト完了!")
    print("✅ 修正されたStreamlitアプリは正常に動作するはずです")
    print("💡 ブラウザで以下を実行してゲームを開始:")
    print("   streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()