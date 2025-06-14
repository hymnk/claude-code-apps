"""
Tetromino class for ZEN Tetris v2.
"""

import pygame
from typing import List, Tuple

from ..constants import TETROMINO_SHAPES, COLORS, BLOCK_SIZE


class Tetromino:
    """Represents a tetromino piece with earth-tone colors."""
    
    def __init__(self, shape_type: str):
        """Initialize a tetromino.
        
        Args:
            shape_type: One of 'I', 'O', 'T', 'S', 'Z', 'J', 'L'
        """
        self.shape_type = shape_type
        self.shape = [list(row) for row in TETROMINO_SHAPES[shape_type]]
        self.color = COLORS[shape_type]
        self.x = 0
        self.y = 0
    
    def rotate(self):
        """Rotate the tetromino 90 degrees clockwise."""
        # Get dimensions
        rows = len(self.shape)
        cols = len(self.shape[0])
        
        # Create rotated shape
        rotated = [['0'] * rows for _ in range(cols)]
        
        for i in range(rows):
            for j in range(cols):
                rotated[j][rows - 1 - i] = self.shape[i][j]
        
        self.shape = rotated
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """Get list of block positions relative to tetromino position.
        
        Returns:
            List of (x, y) tuples for each block
        """
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == '1':
                    blocks.append((self.x + x, self.y + y))
        return blocks
    
    def draw(self, surface: pygame.Surface, offset_x: int, offset_y: int):
        """Draw the tetromino on the surface.
        
        Args:
            surface: Pygame surface to draw on
            offset_x: X offset for drawing position
            offset_y: Y offset for drawing position
        """
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == '1':
                    # Calculate screen position
                    screen_x = offset_x + (self.x + x) * BLOCK_SIZE
                    screen_y = offset_y + (self.y + y) * BLOCK_SIZE
                    
                    # Draw block with earth-tone color
                    block_rect = pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)
                    
                    # Main block color
                    pygame.draw.rect(surface, self.color, block_rect)
                    
                    # Add subtle shadow for depth
                    shadow_color = tuple(max(0, c - 30) for c in self.color)
                    pygame.draw.rect(surface, shadow_color, block_rect, 2)
                    
                    # Add highlight for 3D effect
                    highlight_color = tuple(min(255, c + 20) for c in self.color)
                    highlight_rect = pygame.Rect(screen_x + 2, screen_y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4)
                    pygame.draw.rect(surface, highlight_color, highlight_rect, 1)
    
    def copy(self) -> 'Tetromino':
        """Create a copy of this tetromino.
        
        Returns:
            New Tetromino instance with same properties
        """
        new_tetromino = Tetromino(self.shape_type)
        new_tetromino.shape = [row.copy() for row in self.shape]
        new_tetromino.x = self.x
        new_tetromino.y = self.y
        return new_tetromino