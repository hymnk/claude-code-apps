"""
Tests for Game Logic - ゲーム全体のロジックをテスト（UIなし）
"""
import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from zen_tetris.components.tetromino import Tetromino
from zen_tetris.components.board import Board
from zen_tetris.constants import BOARD_WIDTH, BOARD_HEIGHT, TETROMINO_SHAPES


class TestGameLogic(unittest.TestCase):
    
    def setUp(self):
        """各テストの前に実行される初期化"""
        self.board = Board()
    
    def test_tetromino_movement_logic(self):
        """テトリミノ移動ロジックのテスト"""
        tetromino = Tetromino('I')
        tetromino.x = 5
        tetromino.y = 10
        
        # 移動前の位置を記録
        old_x, old_y = tetromino.x, tetromino.y
        
        # 右移動をシミュレート
        tetromino.x += 1
        if not self.board.check_collision(tetromino):
            # 移動成功
            self.assertEqual(tetromino.x, old_x + 1)
        else:
            # 移動失敗、元に戻す
            tetromino.x = old_x
            self.assertEqual(tetromino.x, old_x)
    
    def test_tetromino_drop_logic(self):
        """テトリミノ落下ロジックのテスト"""
        tetromino = Tetromino('O')
        tetromino.x = 5
        tetromino.y = 0
        
        # 落下可能な限り落下させる
        drop_count = 0
        while True:
            tetromino.y += 1
            if self.board.check_collision(tetromino):
                tetromino.y -= 1  # 一つ戻す
                break
            drop_count += 1
            
            # 無限ループ防止
            if drop_count > BOARD_HEIGHT:
                self.fail("Tetromino fell infinitely")
        
        # 適切な位置で停止していることを確認
        self.assertGreaterEqual(tetromino.y, 0)
        self.assertLess(tetromino.y, BOARD_HEIGHT)
        
        # この位置では衝突しない
        self.assertFalse(self.board.check_collision(tetromino))
        
        # 一つ下では衝突する
        tetromino.y += 1
        self.assertTrue(self.board.check_collision(tetromino))
    
    def test_hard_drop_logic(self):
        """ハードドロップロジックのテスト"""
        tetromino = Tetromino('T')
        tetromino.x = 5
        tetromino.y = 0
        
        original_y = tetromino.y
        
        # ハードドロップをシミュレート
        while True:
            tetromino.y += 1
            if self.board.check_collision(tetromino):
                tetromino.y -= 1
                break
        
        final_y = tetromino.y
        
        # 実際に下に移動した
        self.assertGreater(final_y, original_y)
        
        # 最終位置で衝突しない
        self.assertFalse(self.board.check_collision(tetromino))
    
    def test_rotation_with_collision(self):
        """衝突を考慮した回転テスト"""
        # 壁際での回転テスト
        tetromino = Tetromino('I')
        tetromino.x = 0  # 左端
        tetromino.y = 10
        
        original_shape = [row[:] for row in tetromino.shape]
        
        # 回転を試行
        tetromino.rotate()
        
        if self.board.check_collision(tetromino):
            # 衝突する場合は元に戻す
            tetromino.shape = original_shape
        
        # 最終的に有効な状態である
        self.assertFalse(self.board.check_collision(tetromino))
    
    def test_line_clear_scoring_logic(self):
        """ライン消去とスコアリングロジックのテスト"""
        # 1ライン完成
        bottom_line = BOARD_HEIGHT - 1
        for x in range(BOARD_WIDTH):
            self.board.grid[bottom_line][x] = (255, 255, 255)
        
        completed_lines = self.board.get_completed_lines()
        self.assertEqual(len(completed_lines), 1)
        
        # 複数ライン完成
        for line in range(BOARD_HEIGHT - 3, BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.board.grid[line][x] = (255, 255, 255)
        
        completed_lines = self.board.get_completed_lines()
        self.assertEqual(len(completed_lines), 3)
        
        # テトリス（4ライン）完成
        for line in range(BOARD_HEIGHT - 4, BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.board.grid[line][x] = (255, 255, 255)
        
        completed_lines = self.board.get_completed_lines()
        self.assertEqual(len(completed_lines), 4)
    
    def test_game_over_condition(self):
        """ゲームオーバー条件のテスト"""
        # スポーン位置付近を埋める
        for x in range(BOARD_WIDTH):
            self.board.grid[0][x] = (255, 0, 0)
            self.board.grid[1][x] = (255, 0, 0)
        
        # 新しいテトリミノをスポーン位置に配置
        tetromino = Tetromino('T')
        tetromino.x = BOARD_WIDTH // 2 - 1
        tetromino.y = 0
        
        # ゲームオーバー条件（スポーン位置で衝突）
        game_over = self.board.check_collision(tetromino)
        self.assertTrue(game_over)
    
    def test_all_tetrominos_can_be_placed(self):
        """全テトリミノが配置可能であることをテスト"""
        for shape_type in TETROMINO_SHAPES.keys():
            with self.subTest(shape_type=shape_type):
                board = Board()  # 新しい空ボード
                tetromino = Tetromino(shape_type)
                
                # 中央付近に配置
                tetromino.x = BOARD_WIDTH // 2 - 1
                tetromino.y = 5
                
                # 空のボードでは衝突しない
                self.assertFalse(board.check_collision(tetromino))
                
                # 配置可能
                board.place_tetromino(tetromino)
                
                # 配置後、ボードが空でない
                self.assertFalse(board.is_empty())
    
    def test_boundary_edge_cases(self):
        """境界での特殊ケーステスト"""
        # 各テトリミノを境界近くに配置してテスト
        test_positions = [
            (0, 0),  # 左上
            (BOARD_WIDTH - 1, 0),  # 右上
            (0, BOARD_HEIGHT - 1),  # 左下
            (BOARD_WIDTH - 1, BOARD_HEIGHT - 1),  # 右下
        ]
        
        for shape_type in ['I', 'O', 'T']:  # 代表的な形状
            for x, y in test_positions:
                with self.subTest(shape_type=shape_type, x=x, y=y):
                    tetromino = Tetromino(shape_type)
                    tetromino.x = x
                    tetromino.y = y
                    
                    # 衝突検出が正しく動作する（クラッシュしない）
                    collision = self.board.check_collision(tetromino)
                    self.assertIsInstance(collision, bool)
    
    def test_tetromino_stacking(self):
        """テトリミノの積み重ねテスト"""
        # 最初のテトリミノを底に配置
        tetromino1 = Tetromino('O')
        tetromino1.x = 4
        tetromino1.y = BOARD_HEIGHT - 2  # O字型は2ブロック高
        self.board.place_tetromino(tetromino1)
        
        # 2番目のテトリミノをその上に配置
        tetromino2 = Tetromino('O')
        tetromino2.x = 4
        tetromino2.y = BOARD_HEIGHT - 4
        
        # 衝突チェック（同じ位置では衝突する）
        tetromino2.y = BOARD_HEIGHT - 2
        self.assertTrue(self.board.check_collision(tetromino2))
        
        # 適切な位置では衝突しない
        tetromino2.y = BOARD_HEIGHT - 4
        self.assertFalse(self.board.check_collision(tetromino2))


if __name__ == '__main__':
    unittest.main()