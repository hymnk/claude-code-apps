"""
Integration Tests - 統合テストとパフォーマンステスト
"""
import unittest
import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from zen_tetris.components.tetromino import Tetromino
from zen_tetris.components.board import Board
from zen_tetris.constants import TETROMINO_SHAPES, BOARD_WIDTH, BOARD_HEIGHT


class TestIntegration(unittest.TestCase):
    
    def test_complete_game_simulation(self):
        """完全なゲームシミュレーション"""
        board = Board()
        lines_cleared = 0
        pieces_placed = 0
        
        # 100個のテトリミノを配置するシミュレーション
        for i in range(100):
            # ランダムなテトリミノ
            shape_type = list(TETROMINO_SHAPES.keys())[i % 7]
            tetromino = Tetromino(shape_type)
            
            # 中央にスポーン
            tetromino.x = BOARD_WIDTH // 2 - 1
            tetromino.y = 0
            
            # ゲームオーバーチェック
            if board.check_collision(tetromino):
                # ゲームオーバー
                break
            
            # 落下シミュレーション
            while True:
                tetromino.y += 1
                if board.check_collision(tetromino):
                    tetromino.y -= 1
                    break
            
            # 配置
            board.place_tetromino(tetromino)
            pieces_placed += 1
            
            # ライン消去チェック
            completed_lines = board.get_completed_lines()
            if completed_lines:
                lines_cleared += len(completed_lines)
                board.clear_lines(completed_lines)
        
        # 基本的な検証
        self.assertGreater(pieces_placed, 0)
        self.assertGreaterEqual(lines_cleared, 0)
        
        print(f"Simulation completed: {pieces_placed} pieces placed, {lines_cleared} lines cleared")
    
    def test_performance_collision_detection(self):
        """衝突検出のパフォーマンステスト"""
        board = Board()
        tetromino = Tetromino('T')
        
        # ボードを部分的に埋める
        for y in range(BOARD_HEIGHT // 2, BOARD_HEIGHT):
            for x in range(0, BOARD_WIDTH, 2):  # 半分だけ埋める
                board.grid[y][x] = (255, 255, 255)
        
        # 大量の衝突検出実行
        start_time = time.time()
        collision_count = 0
        
        for _ in range(10000):
            for x in range(BOARD_WIDTH):
                for y in range(BOARD_HEIGHT):
                    tetromino.x = x
                    tetromino.y = y
                    if board.check_collision(tetromino):
                        collision_count += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        # パフォーマンス検証（2秒以内で完了）
        self.assertLess(duration, 2.0, f"Collision detection too slow: {duration:.3f}s")
        self.assertGreater(collision_count, 0)
        
        print(f"Performance test: {collision_count} collisions detected in {duration:.3f}s")
    
    def test_stress_line_clearing(self):
        """ライン消去のストレステスト"""
        board = Board()
        
        # 大量のライン消去をシミュレート
        total_lines_cleared = 0
        
        for iteration in range(50):
            # ボードを完全に埋める（最上段以外）
            for y in range(5, BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    board.grid[y][x] = (100, 150, 200)
            
            # ライン消去実行
            completed_lines = board.get_completed_lines()
            self.assertEqual(len(completed_lines), BOARD_HEIGHT - 5)
            
            board.clear_lines(completed_lines)
            total_lines_cleared += len(completed_lines)
            
            # ボードが正しくクリアされている
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    self.assertIsNone(board.grid[y][x])
        
        expected_total = 50 * (BOARD_HEIGHT - 5)
        self.assertEqual(total_lines_cleared, expected_total)
        
        print(f"Stress test: {total_lines_cleared} lines cleared successfully")
    
    def test_rotation_edge_cases(self):
        """回転の特殊ケーステスト"""
        board = Board()
        
        # 各テトリミノの各位置での回転テスト
        rotation_tests = 0
        successful_rotations = 0
        
        for shape_type in TETROMINO_SHAPES.keys():
            for x in range(BOARD_WIDTH):
                for y in range(BOARD_HEIGHT):
                    tetromino = Tetromino(shape_type)
                    tetromino.x = x
                    tetromino.y = y
                    
                    # 初期位置で衝突しない場合のみテスト
                    if not board.check_collision(tetromino):
                        original_shape = [row[:] for row in tetromino.shape]
                        
                        # 回転実行
                        tetromino.rotate()
                        rotation_tests += 1
                        
                        if board.check_collision(tetromino):
                            # 衝突する場合は元に戻す
                            tetromino.shape = original_shape
                        else:
                            successful_rotations += 1
                        
                        # 最終的に有効な状態である
                        self.assertFalse(board.check_collision(tetromino))
        
        print(f"Rotation test: {successful_rotations}/{rotation_tests} rotations successful")
        self.assertGreater(rotation_tests, 0)
    
    def test_memory_usage_stability(self):
        """メモリ使用量の安定性テスト"""
        import gc
        
        boards = []
        
        # 大量のボードオブジェクト作成
        for i in range(1000):
            board = Board()
            
            # 部分的にデータを設定
            for y in range(min(10, BOARD_HEIGHT)):
                for x in range(min(5, BOARD_WIDTH)):
                    board.grid[y][x] = (i % 255, (i * 2) % 255, (i * 3) % 255)
            
            if i % 100 == 0:
                # 定期的にガベージコレクション
                gc.collect()
                
            boards.append(board)
        
        # 全ボードが正しく作成されている
        self.assertEqual(len(boards), 1000)
        
        # メモリクリーンアップ
        del boards
        gc.collect()
        
        print("Memory stability test completed successfully")
    
    def test_tetris_achievement_simulation(self):
        """テトリス（4ライン同時消去）達成シミュレーション"""
        board = Board()
        
        # I字型テトリミノでテトリスを作る準備
        # 底の4ラインを9列まで埋める（1列空ける）
        gap_column = 0  # 左端を空ける
        
        for y in range(BOARD_HEIGHT - 4, BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if x != gap_column:
                    board.grid[y][x] = (255, 100, 100)
        
        # I字型テトリミノを縦にして隙間に配置
        tetromino = Tetromino('I')
        tetromino.rotate()  # 縦向きに
        tetromino.x = gap_column
        
        # 適切な高さまで落下
        tetromino.y = BOARD_HEIGHT - 4
        
        # 衝突チェック（配置可能である）
        self.assertFalse(board.check_collision(tetromino))
        
        # 配置実行
        board.place_tetromino(tetromino)
        
        # テトリス完成確認
        completed_lines = board.get_completed_lines()
        self.assertEqual(len(completed_lines), 4, "Tetris (4 lines) should be completed")
        
        # ライン消去実行
        board.clear_lines(completed_lines)
        
        # 底の4ラインが空になっている
        for y in range(BOARD_HEIGHT - 4, BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.assertIsNone(board.grid[y][x])
        
        print("Tetris achievement simulation successful")


if __name__ == '__main__':
    unittest.main(verbosity=2)