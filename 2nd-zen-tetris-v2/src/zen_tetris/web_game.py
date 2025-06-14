"""
Web-compatible ZEN Tetris v2 Game Logic
Pygame-free version for browser gameplay via WebSocket.
"""

import random
import time
from typing import Dict, Any, List, Optional, Tuple

from .components.board import Board
from .components.tetromino import Tetromino
from .constants import (
    TETROMINO_SHAPES, COLORS, BOARD_WIDTH, BOARD_HEIGHT,
    DROP_SPEED, PARTICLE_COUNT, PARTICLE_LIFETIME
)


class WebParticle:
    """Lightweight particle for web rendering."""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        """Initialize web particle."""
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-8, -2)
        self.color = color
        self.size = random.uniform(2, 6)
        self.life = PARTICLE_LIFETIME
        self.max_life = PARTICLE_LIFETIME
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
    
    def update(self):
        """Update particle physics."""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # Gravity
        self.rotation += self.rotation_speed
        self.life -= 1
        self.size = max(0.1, self.size * 0.995)  # Shrink over time
    
    def is_dead(self) -> bool:
        """Check if particle should be removed."""
        return self.life <= 0 or self.size <= 0.1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert particle to dictionary for JSON serialization."""
        alpha = int(255 * (self.life / self.max_life))
        return {
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "size": self.size,
            "rotation": self.rotation,
            "alpha": alpha
        }


class WebParticleSystem:
    """Particle system for web rendering."""
    
    def __init__(self):
        """Initialize particle system."""
        self.particles: List[WebParticle] = []
        self.max_particles = 500
    
    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int], count: int = 15):
        """Create explosion effect at specified position."""
        for _ in range(count):
            particle_x = x + random.uniform(-10, 10)
            particle_y = y + random.uniform(-10, 10)
            self.particles.append(WebParticle(particle_x, particle_y, color))
    
    def create_tetris_effect(self, width: int, height: int):
        """Create special golden effect for Tetris achievement."""
        golden_color = (255, 215, 0)  # Gold
        for _ in range(80):
            x = random.randint(0, width)
            y = random.randint(0, height)
            self.particles.append(WebParticle(x, y, golden_color))
    
    def update(self):
        """Update all particles."""
        for particle in self.particles:
            particle.update()
        
        # Remove dead particles
        self.particles = [p for p in self.particles if not p.is_dead()]
        
        # Enforce particle limit
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[-self.max_particles:]
    
    def get_particles_data(self) -> List[Dict[str, Any]]:
        """Get particle data for web rendering."""
        return [particle.to_dict() for particle in self.particles]
    
    def clear(self):
        """Remove all particles."""
        self.particles.clear()


class WebZenTetrisGame:
    """Web-compatible ZEN Tetris v2 game."""
    
    def __init__(self):
        """Initialize web game."""
        # Game state
        self.board = Board()
        self.current_tetromino: Optional[Tetromino] = None
        self.next_tetromino: Optional[Tetromino] = None
        self.running = True
        self.game_over = False
        self.paused = False
        
        # Score and progression
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.drop_timer = 0
        self.drop_speed = DROP_SPEED
        
        # Effects
        self.flash_lines: List[int] = []
        self.flash_timer = 0
        self.combo_count = 0
        self.timer_active = False
        self.particle_system = WebParticleSystem()
        
        # Timing
        self.last_update = time.time()
        self.clear_timer = 0
        self.clear_delay = 0.2  # 200ms delay
        
        # Initialize first tetrominos
        self.next_tetromino = self._create_random_tetromino()
        self._spawn_new_tetromino()
    
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
    
    def handle_input(self, action: str):
        """Handle user input action."""
        if self.game_over:
            if action == "restart":
                self.restart_game()
            return
        
        if action == "pause":
            self.paused = not self.paused
            return
        
        if action == "restart":
            self.restart_game()
            return
        
        if self.paused:
            return
        
        # Game actions
        if action == "move_left":
            self._move_tetromino(-1, 0)
        elif action == "move_right":
            self._move_tetromino(1, 0)
        elif action == "move_down":
            self._move_tetromino(0, 1)
        elif action == "rotate":
            self._rotate_tetromino()
        elif action == "hard_drop":
            self._hard_drop()
    
    def _move_tetromino(self, dx: int, dy: int) -> bool:
        """Move the current tetromino."""
        if not self.current_tetromino:
            return False
        
        # Store original position
        original_x = self.current_tetromino.x
        original_y = self.current_tetromino.y
        
        # Apply movement
        self.current_tetromino.x += dx
        self.current_tetromino.y += dy
        
        # Check collision
        if self.board.check_collision(self.current_tetromino):
            # Revert movement
            self.current_tetromino.x = original_x
            self.current_tetromino.y = original_y
            return False
        
        return True
    
    def _rotate_tetromino(self):
        """Rotate the current tetromino."""
        if not self.current_tetromino:
            return
        
        # Store original shape
        original_shape = self.current_tetromino.shape
        
        # Rotate
        self.current_tetromino.rotate()
        
        # Check collision
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
        
        # Check for completed lines
        completed_lines = self.board.get_completed_lines()
        if completed_lines:
            self._handle_line_clearing(completed_lines)
        
        # Spawn next tetromino
        self._spawn_new_tetromino()
        
        # Update level based on lines cleared
        self.level = (self.lines_cleared // 10) + 1
        self.drop_speed = max(50, DROP_SPEED - (self.level - 1) * 50)
    
    def _handle_line_clearing(self, completed_lines: List[int]):
        """Handle line clearing with effects."""
        self.flash_lines = completed_lines
        self.flash_timer = 10  # Flash for 10 frames
        self.clear_timer = self.clear_delay
        
        # Create particle effects
        for line_y in completed_lines:
            for x in range(BOARD_WIDTH):
                if self.board.grid[line_y][x] is not None:
                    block_color = COLORS.get(self.board.grid[line_y][x], (255, 255, 255))
                    particle_x = x * 30 + 15  # Block size assumption
                    particle_y = line_y * 30 + 15
                    self.particle_system.create_explosion(
                        particle_x, particle_y, block_color, PARTICLE_COUNT
                    )
        
        # Special effects for Tetris (4 lines)
        if len(completed_lines) >= 4:
            self.particle_system.create_tetris_effect(800, 600)  # Screen size assumption
    
    def _clear_completed_lines(self):
        """Actually clear the completed lines and update score."""
        if not self.flash_lines:
            return
        
        # Calculate score based on lines cleared
        lines_count = len(self.flash_lines)
        base_score = {1: 100, 2: 300, 3: 500, 4: 800}.get(lines_count, 100)
        line_score = base_score * self.level
        
        # Add combo bonus
        if self.combo_count > 0:
            combo_bonus = min(self.combo_count * 50, 500)
            line_score += combo_bonus
        
        self.score += line_score
        self.lines_cleared += lines_count
        self.combo_count += 1
        
        # Clear the lines
        self.board.clear_lines(self.flash_lines)
        self.flash_lines = []
        self.flash_timer = 0
    
    def update(self):
        """Update game state."""
        if not self.running or self.game_over or self.paused:
            # Still update particles for visual effects
            self.particle_system.update()
            return
        
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time
        
        # Handle line clearing timer
        if self.clear_timer > 0:
            self.clear_timer -= dt
            if self.clear_timer <= 0:
                self._clear_completed_lines()
        
        # Update flash timer
        if self.flash_timer > 0:
            self.flash_timer -= 1
        
        # Update particle system
        self.particle_system.update()
        
        # Drop timer
        self.drop_timer += dt * 1000  # Convert to ms
        if self.drop_timer >= self.drop_speed:
            if not self._move_tetromino(0, 1):
                # Tetromino can't move down, place it
                self._place_tetromino()
                self.combo_count = 0  # Reset combo if not clearing lines
            self.drop_timer = 0
    
    def restart_game(self):
        """Restart the game."""
        self.__init__()
    
    def get_state(self) -> Dict[str, Any]:
        """Get current game state for web client."""
        # Get board state
        board_state = []
        for y in range(BOARD_HEIGHT):
            row = []
            for x in range(BOARD_WIDTH):
                cell = self.board.grid[y][x]
                if cell is not None:
                    color = COLORS.get(cell, (255, 255, 255))
                    row.append({"filled": True, "color": color})
                else:
                    row.append({"filled": False, "color": None})
            board_state.append(row)
        
        # Get current tetromino blocks
        current_blocks = []
        if self.current_tetromino:
            for block_x, block_y in self.current_tetromino.get_blocks():
                if 0 <= block_x < BOARD_WIDTH and 0 <= block_y < BOARD_HEIGHT:
                    color = COLORS.get(self.current_tetromino.shape_type, (255, 255, 255))
                    current_blocks.append({
                        "x": block_x,
                        "y": block_y,
                        "color": color
                    })
        
        # Get next tetromino preview
        next_preview = []
        if self.next_tetromino:
            color = COLORS.get(self.next_tetromino.shape_type, (255, 255, 255))
            for y, row in enumerate(self.next_tetromino.shape):
                for x, cell in enumerate(row):
                    if cell == '1':
                        next_preview.append({
                            "x": x,
                            "y": y,
                            "color": color
                        })
        
        return {
            "type": "game_state",
            "board": board_state,
            "current_piece": current_blocks,
            "next_piece": next_preview,
            "score": self.score,
            "lines": self.lines_cleared,
            "level": self.level,
            "game_over": self.game_over,
            "paused": self.paused,
            "flash_lines": self.flash_lines if self.flash_timer > 0 else [],
            "particles": self.particle_system.get_particles_data()
        }