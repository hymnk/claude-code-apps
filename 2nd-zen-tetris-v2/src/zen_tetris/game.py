"""
Main game class for ZEN Tetris v2.
"""

import pygame
import sys
import random
from typing import List, Tuple, Optional

from .constants import *
from .components.tetromino import Tetromino
from .components.board import Board
from .effects.particles import ParticleSystem
from .utils.colors import apply_earth_tone_gradient


class ZenTetrisGame:
    """Main game class that orchestrates the ZEN Tetris experience."""
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        
        # Display setup
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("ZEN Tetris v2 - Calming Earth-tone Puzzle Game")
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.game_over = False
        
        # Game components
        self.board = Board()
        self.particle_system = ParticleSystem()
        
        # Current and next tetrominos
        self.current_tetromino: Optional[Tetromino] = None
        self.next_tetromino: Optional[Tetromino] = None
        
        # Game stats
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.drop_timer = 0
        self.drop_speed = DROP_SPEED
        
        # Effects
        self.flash_lines = []
        self.flash_timer = 0
        self.combo_count = 0
        self.timer_active = False  # Track timer state to prevent conflicts
        
        # Fonts - Use system font for Japanese support
        try:
            # Try to use system font that supports Japanese
            self.font_large = pygame.font.SysFont("notosanscjk, hiragino, meiryo, msgothic", 48)
            self.font_medium = pygame.font.SysFont("notosanscjk, hiragino, meiryo, msgothic", 32)
            self.font_small = pygame.font.SysFont("notosanscjk, hiragino, meiryo, msgothic", 24)
        except Exception:
            # Fallback to default font with additional error handling
            try:
                self.font_large = pygame.font.Font(None, 48)
                self.font_medium = pygame.font.Font(None, 32)
                self.font_small = pygame.font.Font(None, 24)
            except Exception:
                # Ultimate fallback - create minimal font objects
                self.font_large = pygame.font.Font(pygame.font.get_default_font(), 48)
                self.font_medium = pygame.font.Font(pygame.font.get_default_font(), 32)
                self.font_small = pygame.font.Font(pygame.font.get_default_font(), 24)
        
        # Initialize first tetrominos
        self.next_tetromino = self._create_random_tetromino()
        self._spawn_new_tetromino()
        
        print(f"🎮 Game initialized - Current: {self.current_tetromino.shape_type if self.current_tetromino else 'None'}")
    
    def _create_random_tetromino(self) -> Tetromino:
        """Create a random tetromino."""
        shape_type = random.choice(list(TETROMINO_SHAPES.keys()))
        return Tetromino(shape_type)
    
    def _spawn_new_tetromino(self):
        """Spawn a new tetromino at the top of the board."""
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = self._create_random_tetromino()
        
        # Position at top center with null check
        if self.current_tetromino and self.current_tetromino.shape:
            self.current_tetromino.x = BOARD_WIDTH // 2 - len(self.current_tetromino.shape[0]) // 2
            self.current_tetromino.y = 0
        else:
            # Fallback: create new tetromino if current is invalid
            self.current_tetromino = self._create_random_tetromino()
            self.current_tetromino.x = BOARD_WIDTH // 2 - 2
            self.current_tetromino.y = 0
        
        # Check for game over
        if self.board.check_collision(self.current_tetromino):
            self.game_over = True
    
    def handle_events(self):
        """Handle all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.USEREVENT + 1:
                # Handle line clearing timer
                self._clear_completed_lines()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
                self.timer_active = False  # Reset timer state
            
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    continue
                
                if self.paused:
                    if event.key == pygame.K_p:
                        self.paused = False
                    continue
                
                # Game controls
                if event.key == pygame.K_LEFT:
                    self._move_tetromino(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self._move_tetromino(1, 0)
                elif event.key == pygame.K_DOWN:
                    self._move_tetromino(0, 1)
                elif event.key == pygame.K_UP:
                    self._rotate_tetromino()
                elif event.key == pygame.K_SPACE:
                    self._hard_drop()
                elif event.key == pygame.K_p:
                    self.paused = True
                elif event.key == pygame.K_r:
                    self.restart_game()
    
    def _move_tetromino(self, dx: int, dy: int) -> bool:
        """Move the current tetromino and handle placement."""
        if not self.current_tetromino:
            return False
        
        old_x, old_y = self.current_tetromino.x, self.current_tetromino.y
        
        # Try to move
        self.current_tetromino.x += dx
        self.current_tetromino.y += dy
        
        # Check collision
        if self.board.check_collision(self.current_tetromino):
            # Undo move
            self.current_tetromino.x -= dx
            self.current_tetromino.y -= dy
            
            # If moving down failed, place the tetromino
            if dy > 0:
                self._place_tetromino()
                return False
            
            return False
        
        return True
    
    def _rotate_tetromino(self):
        """Rotate the current tetromino."""
        if not self.current_tetromino:
            return
        
        original_shape = self.current_tetromino.shape
        self.current_tetromino.rotate()
        
        # Check if rotation is valid
        if self.board.check_collision(self.current_tetromino):
            # Revert rotation
            self.current_tetromino.shape = original_shape
    
    def _hard_drop(self):
        """Drop the tetromino all the way down."""
        if not self.current_tetromino:
            return
        
        # Prevent infinite loop with counter limit
        max_drops = 25  # Board height is 20, so this is safe
        drops = 0
        while self._move_tetromino(0, 1) and drops < max_drops:
            drops += 1
    
    def _place_tetromino(self):
        """Place the current tetromino on the board."""
        if not self.current_tetromino:
            return
        
        self.board.place_tetromino(self.current_tetromino)
        self._check_lines()
        self._spawn_new_tetromino()
        self.combo_count = 0
    
    def _check_lines(self):
        """Check for completed lines and handle clearing."""
        completed_lines = self.board.get_completed_lines()
        
        if completed_lines:
            # Start flash effect
            self.flash_lines = completed_lines
            self.flash_timer = 30
            self.combo_count += 1
            
            # Create particles for each cleared block
            for line_y in completed_lines:
                for x in range(BOARD_WIDTH):
                    particle_x = BOARD_OFFSET_X + x * BLOCK_SIZE + BLOCK_SIZE // 2
                    particle_y = BOARD_OFFSET_Y + line_y * BLOCK_SIZE + BLOCK_SIZE // 2
                    
                    # Get block color
                    block_color = self.board.get_block_color(x, line_y)
                    if block_color:
                        self.particle_system.create_explosion(
                            particle_x, particle_y, block_color, PARTICLE_COUNT
                        )
            
            # Special effects for Tetris (4 lines)
            if len(completed_lines) >= 4:
                self._create_tetris_effect()
            
            # Clear lines after a delay (will be handled in update)
            # Only set timer if one isn't already active
            if not self.timer_active:
                self.timer_active = True
                pygame.time.set_timer(pygame.USEREVENT + 1, 200)  # 200ms delay
    
    def _create_tetris_effect(self):
        """Create special effects for Tetris achievement."""
        # Screen-wide golden particles
        for _ in range(80):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.particle_system.create_explosion(
                x, y, COLORS['particle_gold'], 1
            )
    
    def _clear_completed_lines(self):
        """Actually remove the completed lines from the board."""
        lines_count = len(self.flash_lines)
        self.board.clear_lines(self.flash_lines)
        
        # Update score and stats
        self.lines_cleared += lines_count
        base_score = SCORE_VALUES.get(lines_count, 0)
        combo_bonus = min(self.combo_count * 50, 500)
        self.score += (base_score + combo_bonus) * self.level
        
        # Update level and speed
        self.level = self.lines_cleared // LINES_PER_LEVEL + 1
        self.drop_speed = max(100, DROP_SPEED - (self.level - 1) * SPEED_INCREASE_PER_LEVEL)
        
        # Reset flash effect
        self.flash_lines = []
        self.flash_timer = 0
    
    def update(self, dt: float):
        """Update game state."""
        if self.game_over or self.paused:
            return
        
        # Update particle system
        self.particle_system.update()
        
        # Update flash effect
        if self.flash_timer > 0:
            self.flash_timer -= 1
        
        # Handle drop timer (dt is in milliseconds from clock.tick())
        self.drop_timer += dt
        
        if self.drop_timer >= self.drop_speed:
            self._move_tetromino(0, 1)
            self.drop_timer = 0
        
        # Line clearing timer is handled in main event loop now
    
    def render(self):
        """Render the game."""
        # Clear screen with earth-tone gradient
        self._draw_background()
        
        # Draw UI
        self._draw_ui()
        
        # Draw game board
        self.board.draw(self.screen, BOARD_OFFSET_X, BOARD_OFFSET_Y, self.flash_lines, self.flash_timer)
        
        # Draw current tetromino
        if self.current_tetromino and not self.game_over:
            self.current_tetromino.draw(self.screen, BOARD_OFFSET_X, BOARD_OFFSET_Y)
        
        # Draw next tetromino preview
        self._draw_next_tetromino()
        
        # Draw particles
        self.particle_system.draw(self.screen)
        
        # Draw overlays
        if self.paused:
            self._draw_pause_overlay()
        elif self.game_over:
            self._draw_game_over_overlay()
        
        pygame.display.flip()
    
    def _draw_background(self):
        """Draw the earth-tone gradient background."""
        apply_earth_tone_gradient(self.screen, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    def _draw_ui(self):
        """Draw the user interface."""
        # Title
        title_surface = self.font_large.render("ZEN Tetris v2", True, COLORS['text_primary'])
        title_rect = title_surface.get_rect(centerx=WINDOW_WIDTH // 2, y=20)
        self.screen.blit(title_surface, title_rect)
        
        # Score panel
        panel_x = BOARD_OFFSET_X + BOARD_WIDTH * BLOCK_SIZE + 40
        panel_y = BOARD_OFFSET_Y
        
        score_text = self.font_medium.render(f"Score: {self.score}", True, COLORS['text_primary'])
        lines_text = self.font_medium.render(f"Lines: {self.lines_cleared}", True, COLORS['text_primary'])
        level_text = self.font_medium.render(f"Level: {self.level}", True, COLORS['text_primary'])
        
        self.screen.blit(score_text, (panel_x, panel_y))
        self.screen.blit(lines_text, (panel_x, panel_y + 40))
        self.screen.blit(level_text, (panel_x, panel_y + 80))
        
        # Controls
        controls_y = panel_y + 200
        controls = [
            "Controls:",
            "Left/Right: Move",
            "Down: Soft Drop",
            "Up: Rotate",
            "Space: Hard Drop",
            "P: Pause",
            "R: Restart"
        ]
        
        for i, control in enumerate(controls):
            color = COLORS['text_accent'] if i == 0 else COLORS['text_primary']
            font = self.font_medium if i == 0 else self.font_small
            text = font.render(control, True, color)
            self.screen.blit(text, (panel_x, controls_y + i * 25))
    
    def _draw_next_tetromino(self):
        """Draw the next tetromino preview."""
        if not self.next_tetromino:
            return
        
        preview_x = BOARD_OFFSET_X + BOARD_WIDTH * BLOCK_SIZE + 40
        preview_y = BOARD_OFFSET_Y + 120
        
        # Draw preview background
        preview_bg = pygame.Rect(preview_x, preview_y, 120, 80)
        pygame.draw.rect(self.screen, COLORS['board_bg'], preview_bg)
        pygame.draw.rect(self.screen, COLORS['ui_accent'], preview_bg, 2)
        
        # Draw label
        label = self.font_small.render("Next Piece", True, COLORS['text_primary'])
        self.screen.blit(label, (preview_x, preview_y - 25))
        
        # Draw tetromino
        shape = self.next_tetromino.shape
        start_x = preview_x + (120 - len(shape[0]) * 20) // 2
        start_y = preview_y + (80 - len(shape) * 20) // 2
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '1':
                    block_rect = pygame.Rect(
                        start_x + x * 20,
                        start_y + y * 20,
                        18, 18
                    )
                    pygame.draw.rect(self.screen, COLORS[self.next_tetromino.shape_type], block_rect)
                    pygame.draw.rect(self.screen, COLORS['shadow'], block_rect, 1)
    
    def _draw_pause_overlay(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_large.render("PAUSED", True, COLORS['text_light'])
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.font_medium.render("Press P to Resume", True, COLORS['text_light'])
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(continue_text, continue_rect)
    
    def _draw_game_over_overlay(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, COLORS['text_light'])
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_medium.render(f"Final Score: {self.score}", True, COLORS['text_light'])
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font_medium.render("Press R to Restart", True, COLORS['text_accent'])
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        """Restart the game."""
        self.game_over = False
        self.paused = False
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.drop_timer = 0
        self.drop_speed = DROP_SPEED
        self.flash_lines = []
        self.flash_timer = 0
        self.combo_count = 0
        
        self.board = Board()
        self.particle_system = ParticleSystem()
        
        self.next_tetromino = self._create_random_tetromino()
        self._spawn_new_tetromino()
    
    def run(self):
        """Main game loop with exception handling for stability."""
        while self.running:
            try:
                dt = self.clock.tick(FPS)
                
                self.handle_events()
                self.update(dt)
                self.render()
            except pygame.error as e:
                print(f"Pygame error: {e}")
                # Try to continue, but break if display is lost
                if "display" in str(e).lower():
                    break
            except Exception as e:
                print(f"Game error: {e}")
                # Continue for most errors to maintain stability
                continue
        
        # Clean up timers before exit
        pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        pygame.quit()
        sys.exit()