"""
Tests for Board class - ボードの衝突検出、配置、ライン消去機能をテスト
"""
import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from zen_tetris.components.board import Board
from zen_tetris.components.tetromino import Tetromino
from zen_tetris.constants import BOARD_WIDTH, BOARD_HEIGHT, COLORS


class TestBoard(unittest.TestCase):
    
    def setUp(self):
        """各テストの前に実行される初期化"""
        self.board = Board()
    
    def test_board_initialization(self):
        """ボードの初期化テスト"""
        # 正しいサイズで初期化されている
        self.assertEqual(len(self.board.grid), BOARD_HEIGHT)
        self.assertEqual(len(self.board.grid[0]), BOARD_WIDTH)
        
        # 全セルが空である
        for row in self.board.grid:
            for cell in row:
                self.assertIsNone(cell)
        
        # 空ボードの確認
        self.assertTrue(self.board.is_empty())
    
    def test_collision_detection_boundaries(self):
        """境界での衝突検出テスト"""
        tetromino = Tetromino('I')
        
        # 左境界テスト
        tetromino.x = -1
        tetromino.y = 0
        self.assertTrue(self.board.check_collision(tetromino))
        
        # 右境界テスト
        tetromino.x = BOARD_WIDTH - 3  # I字型は4ブロック幅
        tetromino.y = 0
        self.assertTrue(self.board.check_collision(tetromino))
        
        # 下境界テスト
        tetromino.x = 0
        tetromino.y = BOARD_HEIGHT
        self.assertTrue(self.board.check_collision(tetromino))
        
        # 正常な位置テスト
        tetromino.x = 5
        tetromino.y = 10
        self.assertFalse(self.board.check_collision(tetromino))
    
    def test_collision_detection_with_blocks(self):
        """既存ブロックとの衝突検出テスト"""
        # ボードの底に手動でブロックを配置
        self.board.grid[BOARD_HEIGHT - 1][5] = COLORS['I']
        
        tetromino = Tetromino('I')
        tetromino.x = 2  # I字型が位置5にブロックを持つように配置
        tetromino.y = BOARD_HEIGHT - 1
        
        # 衝突が検出されるべき
        self.assertTrue(self.board.check_collision(tetromino))
        
        # 違う位置なら衝突しない
        tetromino.x = 0
        self.assertFalse(self.board.check_collision(tetromino))
    
    def test_tetromino_placement(self):
        """テトリミノ配置テスト"""
        tetromino = Tetromino('O')  # 2x2の正方形
        tetromino.x = 5
        tetromino.y = 18  # 底近く
        
        # 配置前は空
        self.assertTrue(self.board.is_empty())
        
        # 配置実行
        self.board.place_tetromino(tetromino)
        
        # 配置後は空でない
        self.assertFalse(self.board.is_empty())
        
        # 正しい位置にブロックが配置されている
        expected_blocks = tetromino.get_blocks()
        for x, y in expected_blocks:
            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                self.assertEqual(self.board.grid[y][x], tetromino.color)
    
    def test_line_completion_detection(self):
        """ライン完成検出テスト"""
        # 一番下のラインを手動で埋める（1つ空けて）
        bottom_line = BOARD_HEIGHT - 1
        for x in range(BOARD_WIDTH - 1):
            self.board.grid[bottom_line][x] = COLORS['I']
        
        # まだ完成していない
        completed_lines = self.board.get_completed_lines()
        self.assertEqual(len(completed_lines), 0)
        
        # 最後のセルを埋める
        self.board.grid[bottom_line][BOARD_WIDTH - 1] = COLORS['I']
        
        # 完成が検出される
        completed_lines = self.board.get_completed_lines()
        self.assertEqual(len(completed_lines), 1)
        self.assertEqual(completed_lines[0], bottom_line)
    
    def test_multiple_line_completion(self):
        """複数ライン完成検出テスト"""
        # 下の2ラインを完成させる
        for line in [BOARD_HEIGHT - 2, BOARD_HEIGHT - 1]:
            for x in range(BOARD_WIDTH):
                self.board.grid[line][x] = COLORS['T']
        
        completed_lines = self.board.get_completed_lines()
        self.assertEqual(len(completed_lines), 2)
        self.assertIn(BOARD_HEIGHT - 2, completed_lines)
        self.assertIn(BOARD_HEIGHT - 1, completed_lines)
    
    def test_line_clearing(self):
        """ライン消去テスト"""
        # テストデータの準備：3ライン作成（上2つは不完全、下1つは完成）
        # ライン18: 不完全
        for x in range(BOARD_WIDTH - 1):
            self.board.grid[18][x] = COLORS['I']
        
        # ライン19: 完成
        for x in range(BOARD_WIDTH):
            self.board.grid[19][x] = COLORS['T']
        
        # ライン17: 完成
        for x in range(BOARD_WIDTH):
            self.board.grid[17][x] = COLORS['L']
        
        # 完成ライン検出
        completed_lines = self.board.get_completed_lines()
        self.assertEqual(len(completed_lines), 2)
        
        # ライン消去実行
        self.board.clear_lines(completed_lines)
        
        # 底のラインが空になっている
        for x in range(BOARD_WIDTH):
            self.assertIsNone(self.board.grid[19][x])
        
        # 不完全だったライン18が下に落ちて19になっている
        for x in range(BOARD_WIDTH - 1):
            self.assertEqual(self.board.grid[19][x], COLORS['I'])
        self.assertIsNone(self.board.grid[19][BOARD_WIDTH - 1])
    
    def test_get_block_color(self):
        """ブロック色取得テスト"""
        # 範囲外テスト
        self.assertIsNone(self.board.get_block_color(-1, 0))
        self.assertIsNone(self.board.get_block_color(0, -1))
        self.assertIsNone(self.board.get_block_color(BOARD_WIDTH, 0))
        self.assertIsNone(self.board.get_block_color(0, BOARD_HEIGHT))
        
        # 空セルテスト
        self.assertIsNone(self.board.get_block_color(5, 10))
        
        # ブロック配置後のテスト
        test_color = COLORS['Z']
        self.board.grid[10][5] = test_color
        self.assertEqual(self.board.get_block_color(5, 10), test_color)
    
    def test_spawn_collision(self):
        """スポーン位置での衝突テスト"""
        # スポーン位置付近にブロックを配置
        self.board.grid[0][5] = COLORS['I']
        
        # T字型テトリミノを中央にスポーン
        tetromino = Tetromino('T')
        tetromino.x = BOARD_WIDTH // 2 - 1
        tetromino.y = 0
        
        # 衝突が検出されるかテスト
        collision = self.board.check_collision(tetromino)
        
        # この場合、T字型の位置によって衝突するかが決まる
        blocks = tetromino.get_blocks()
        should_collide = any(
            0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT and 
            self.board.grid[y][x] is not None
            for x, y in blocks
        )
        
        self.assertEqual(collision, should_collide)


if __name__ == '__main__':
    unittest.main()