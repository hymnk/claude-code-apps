"""
Game board class for ZEN Tetris v2.
"""

import pygame
from typing import List, Optional, Tuple

from ..constants import BOARD_WIDTH, BOARD_HEIGHT, BLOCK_SIZE, COLORS
from .tetromino import Tetromino


class Board:
    """Represents the game board with earth-tone styling."""
    
    def __init__(self):
        """Initialize an empty board."""
        # Board grid: None for empty, color tuple for filled
        self.grid = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    
    def check_collision(self, tetromino: Tetromino) -> bool:
        """Check if tetromino collides with board or boundaries.
        
        Args:
            tetromino: Tetromino to check
            
        Returns:
            True if collision detected
        """
        for block_x, block_y in tetromino.get_blocks():
            # Check horizontal boundaries
            if block_x < 0 or block_x >= BOARD_WIDTH:
                return True
            
            # Check bottom boundary (critical fix for infinite falling)
            if block_y >= BOARD_HEIGHT:
                return True
            
            # Check collision with existing blocks (but allow negative y for spawning)
            if block_y >= 0 and 0 <= block_x < BOARD_WIDTH and self.grid[block_y][block_x] is not None:
                return True
        
        return False
    
    def place_tetromino(self, tetromino: Tetromino):
        """Place tetromino on the board.
        
        Args:
            tetromino: Tetromino to place
        """
        for block_x, block_y in tetromino.get_blocks():
            if 0 <= block_y < BOARD_HEIGHT and 0 <= block_x < BOARD_WIDTH:
                self.grid[block_y][block_x] = tetromino.color
    
    def get_completed_lines(self) -> List[int]:
        """Get list of completed line indices.
        
        Returns:
            List of y-coordinates of completed lines
        """
        completed_lines = []
        for y in range(BOARD_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(BOARD_WIDTH)):
                completed_lines.append(y)
        return completed_lines
    
    def clear_lines(self, line_indices: List[int]):
        """Clear specified lines and drop blocks above.
        
        Args:
            line_indices: List of line y-coordinates to clear
        """
        if not line_indices:
            return
            
        # Sort in descending order to clear from bottom up
        line_indices.sort(reverse=True)
        
        # Remove completed lines from bottom to top
        for line_y in line_indices:
            if 0 <= line_y < len(self.grid):
                del self.grid[line_y]
        
        # Add empty lines at the top to maintain board height
        lines_to_add = len(line_indices)
        for _ in range(lines_to_add):
            self.grid.insert(0, [None for _ in range(BOARD_WIDTH)])
    
    def get_block_color(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """Get color of block at position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Color tuple or None if empty
        """
        if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
            return self.grid[y][x]
        return None
    
    def draw(self, surface: pygame.Surface, offset_x: int, offset_y: int, 
             flash_lines: List[int] = None, flash_timer: int = 0):
        """Draw the board on the surface.
        
        Args:
            surface: Pygame surface to draw on
            offset_x: X offset for drawing position
            offset_y: Y offset for drawing position
            flash_lines: Lines currently flashing (being cleared)
            flash_timer: Current flash timer value
        """
        flash_lines = flash_lines or []
        
        # Draw board background
        board_rect = pygame.Rect(offset_x, offset_y, 
                                BOARD_WIDTH * BLOCK_SIZE, 
                                BOARD_HEIGHT * BLOCK_SIZE)
        pygame.draw.rect(surface, COLORS['board_bg'], board_rect)
        
        # Draw border with earth-tone accent
        border_color = COLORS['ui_accent']
        pygame.draw.rect(surface, border_color, board_rect, 3)
        
        # Draw grid lines (subtle)
        grid_color = tuple(c + 10 for c in COLORS['board_bg'])
        for x in range(BOARD_WIDTH + 1):
            start_pos = (offset_x + x * BLOCK_SIZE, offset_y)
            end_pos = (offset_x + x * BLOCK_SIZE, offset_y + BOARD_HEIGHT * BLOCK_SIZE)
            pygame.draw.line(surface, grid_color, start_pos, end_pos, 1)
        
        for y in range(BOARD_HEIGHT + 1):
            start_pos = (offset_x, offset_y + y * BLOCK_SIZE)
            end_pos = (offset_x + BOARD_WIDTH * BLOCK_SIZE, offset_y + y * BLOCK_SIZE)
            pygame.draw.line(surface, grid_color, start_pos, end_pos, 1)
        
        # Draw blocks
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                block_color = self.grid[y][x]
                if block_color is not None:
                    screen_x = offset_x + x * BLOCK_SIZE
                    screen_y = offset_y + y * BLOCK_SIZE
                    
                    # Apply flash effect if this line is being cleared
                    if y in flash_lines and flash_timer > 0:
                        flash_intensity = (flash_timer % 8) / 8.0
                        if flash_timer % 16 < 8:
                            # Flash to white/gold
                            flash_color = COLORS['flash_white']
                        else:
                            # Flash to gold
                            flash_color = COLORS['particle_gold']
                        
                        # Blend colors
                        final_color = tuple(
                            int(block_color[i] * (1 - flash_intensity) + 
                                flash_color[i] * flash_intensity)
                            for i in range(3)
                        )
                    else:
                        final_color = block_color
                    
                    # Draw block
                    block_rect = pygame.Rect(screen_x, screen_y, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(surface, final_color, block_rect)
                    
                    # Add shadow for depth
                    shadow_color = tuple(max(0, c - 30) for c in final_color)
                    pygame.draw.rect(surface, shadow_color, block_rect, 2)
                    
                    # Add special glow effect for flashing lines
                    if y in flash_lines and flash_timer > 0:
                        glow_surface = pygame.Surface((BLOCK_SIZE + 4, BLOCK_SIZE + 4))
                        glow_surface.set_alpha(128)
                        glow_surface.fill(COLORS['particle_gold'])
                        surface.blit(glow_surface, (screen_x - 2, screen_y - 2))
    
    def is_empty(self) -> bool:
        """Check if board is completely empty.
        
        Returns:
            True if board has no placed blocks
        """
        for row in self.grid:
            for cell in row:
                if cell is not None:
                    return False
        return True