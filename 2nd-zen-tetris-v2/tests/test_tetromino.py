"""
Tests for Tetromino class - 基本的なテトリミノの動作をテスト
"""
import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from zen_tetris.components.tetromino import Tetromino
from zen_tetris.constants import TETROMINO_SHAPES, COLORS


class TestTetromino(unittest.TestCase):
    
    def test_tetromino_initialization(self):
        """テトリミノの初期化テスト"""
        for shape_type in TETROMINO_SHAPES.keys():
            tetromino = Tetromino(shape_type)
            
            # 基本属性の確認
            self.assertEqual(tetromino.shape_type, shape_type)
            self.assertEqual(tetromino.x, 0)
            self.assertEqual(tetromino.y, 0)
            self.assertEqual(tetromino.color, COLORS[shape_type])
            
            # 形状データの確認
            self.assertIsInstance(tetromino.shape, list)
            self.assertTrue(len(tetromino.shape) > 0)
    
    def test_tetromino_shapes_format(self):
        """テトリミノ形状データの正しさをテスト"""
        for shape_type, expected_shape in TETROMINO_SHAPES.items():
            tetromino = Tetromino(shape_type)
            
            # 形状が正しくコピーされているか
            self.assertEqual(len(tetromino.shape), len(expected_shape))
            for i, row in enumerate(tetromino.shape):
                self.assertEqual(len(row), len(expected_shape[i]))
                for j, cell in enumerate(row):
                    self.assertEqual(cell, expected_shape[i][j])
    
    def test_get_blocks(self):
        """get_blocks()メソッドのテスト"""
        # T字型テトリミノのテスト
        tetromino = Tetromino('T')
        tetromino.x = 5
        tetromino.y = 3
        
        blocks = tetromino.get_blocks()
        
        # T字型の期待される座標
        # ['0', '1', '0']  -> (5, 3)
        # ['1', '1', '1']  -> (4, 4), (5, 4), (6, 4)
        expected_blocks = [(6, 3), (5, 4), (6, 4), (7, 4)]
        
        self.assertEqual(len(blocks), 4)
        self.assertEqual(set(blocks), set(expected_blocks))
    
    def test_get_blocks_all_shapes(self):
        """全テトリミノ形状のget_blocksテスト"""
        for shape_type in TETROMINO_SHAPES.keys():
            tetromino = Tetromino(shape_type)
            blocks = tetromino.get_blocks()
            
            # ブロック数の確認（全て4ブロックであるべき）
            self.assertEqual(len(blocks), 4, f"Shape {shape_type} should have 4 blocks")
            
            # 重複なし
            self.assertEqual(len(blocks), len(set(blocks)), f"Shape {shape_type} has duplicate blocks")
    
    def test_rotation(self):
        """回転機能のテスト"""
        # I字型テトリミノの回転テスト
        tetromino = Tetromino('I')
        original_shape = [row[:] for row in tetromino.shape]  # Deep copy
        
        # 回転実行
        tetromino.rotate()
        
        # 形状が変化していることを確認
        self.assertNotEqual(tetromino.shape, original_shape)
        
        # 4回回転すると元に戻る
        tetromino.rotate()
        tetromino.rotate()
        tetromino.rotate()
        self.assertEqual(tetromino.shape, original_shape)
    
    def test_rotation_preserves_block_count(self):
        """回転でブロック数が保持されることをテスト"""
        for shape_type in TETROMINO_SHAPES.keys():
            tetromino = Tetromino(shape_type)
            original_block_count = len(tetromino.get_blocks())
            
            # 4回回転してブロック数を確認
            for _ in range(4):
                tetromino.rotate()
                current_block_count = len(tetromino.get_blocks())
                self.assertEqual(current_block_count, original_block_count, 
                               f"Block count changed after rotation for {shape_type}")
    
    def test_copy(self):
        """copy()メソッドのテスト"""
        original = Tetromino('L')
        original.x = 5
        original.y = 10
        original.rotate()  # 回転させて状態を変更
        
        copy = original.copy()
        
        # 基本属性が正しくコピーされている
        self.assertEqual(copy.shape_type, original.shape_type)
        self.assertEqual(copy.x, original.x)
        self.assertEqual(copy.y, original.y)
        self.assertEqual(copy.color, original.color)
        
        # 形状が正しくコピーされている
        self.assertEqual(copy.shape, original.shape)
        
        # 独立したオブジェクトであることを確認
        copy.x = 99
        self.assertNotEqual(copy.x, original.x)
        
        copy.shape[0][0] = 'X'
        self.assertNotEqual(copy.shape, original.shape)


if __name__ == '__main__':
    unittest.main()