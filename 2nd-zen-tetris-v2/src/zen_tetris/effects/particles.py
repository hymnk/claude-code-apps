"""
Particle system for ZEN Tetris v2 with earth-tone effects.
"""

import pygame
import random
import math
from typing import List, Tuple

from ..constants import COLORS, PARTICLE_LIFETIME, PARTICLE_GRAVITY, PARTICLE_SIZE_RANGE, PARTICLE_SPEED_RANGE


class Particle:
    """Individual particle with physics and earth-tone styling."""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        """Initialize a particle.
        
        Args:
            x: Initial X position
            y: Initial Y position
            color: RGB color tuple
        """
        self.x = x
        self.y = y
        self.vx = random.uniform(*PARTICLE_SPEED_RANGE)
        self.vy = random.uniform(-8, -2)  # Initial upward velocity
        self.color = color
        self.size = random.uniform(*PARTICLE_SIZE_RANGE)
        self.life = PARTICLE_LIFETIME
        self.max_life = PARTICLE_LIFETIME
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.2, 0.2)
    
    def update(self):
        """Update particle physics."""
        # Apply velocity
        self.x += self.vx
        self.y += self.vy
        
        # Apply gravity
        self.vy += PARTICLE_GRAVITY
        
        # Update rotation
        self.rotation += self.rotation_speed
        
        # Decrease life
        self.life -= 1
        
        # Shrink over time
        self.size *= 0.98
    
    def draw(self, surface: pygame.Surface):
        """Draw the particle as a star shape.
        
        Args:
            surface: Pygame surface to draw on
        """
        if self.life <= 0 or self.size <= 0:
            return
        
        # Calculate alpha based on remaining life
        alpha = int(255 * (self.life / self.max_life))
        
        # Create star points
        points = []
        for i in range(5):
            # Outer points
            angle = self.rotation + (i * 2 * math.pi) / 5
            x = self.x + math.cos(angle) * self.size
            y = self.y + math.sin(angle) * self.size
            points.append((x, y))
            
            # Inner points
            inner_angle = self.rotation + ((i + 0.5) * 2 * math.pi) / 5
            inner_x = self.x + math.cos(inner_angle) * self.size * 0.4
            inner_y = self.y + math.sin(inner_angle) * self.size * 0.4
            points.append((inner_x, inner_y))
        
        # Create surface for particle with alpha and size limits
        surface_size = min(int(self.size * 4), 200)  # Limit surface size to prevent memory issues
        if surface_size <= 0:
            return  # Skip if size is invalid
        particle_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        
        # Adjust points relative to particle surface
        adjusted_points = [
            (p[0] - self.x + self.size * 2, p[1] - self.y + self.size * 2)
            for p in points
        ]
        
        # Draw star with alpha
        color_with_alpha = (*self.color, alpha)
        pygame.draw.polygon(particle_surface, color_with_alpha, adjusted_points)
        
        # Add glow effect for earth-tone particles
        if self.color in [COLORS['particle_gold'], COLORS['particle_light']]:
            glow_points = [
                (p[0] * 1.5 - self.size, p[1] * 1.5 - self.size)
                for p in adjusted_points
            ]
            glow_color = (*self.color, alpha // 4)
            pygame.draw.polygon(particle_surface, glow_color, glow_points)
        
        # Blit to main surface with bounds checking
        blit_x = max(0, min(surface.get_width() - particle_surface.get_width(), self.x - self.size * 2))
        blit_y = max(0, min(surface.get_height() - particle_surface.get_height(), self.y - self.size * 2))
        surface.blit(particle_surface, (blit_x, blit_y))
    
    def is_dead(self) -> bool:
        """Check if particle should be removed.
        
        Returns:
            True if particle is dead
        """
        return self.life <= 0 or self.size <= 0.1


class ParticleSystem:
    """Manages all particles with earth-tone aesthetic."""
    
    def __init__(self):
        """Initialize empty particle system."""
        self.particles: List[Particle] = []
        self.max_particles = 500  # Prevent memory issues
    
    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int], count: int = 15):
        """Create an explosion of particles.
        
        Args:
            x: Explosion center X
            y: Explosion center Y
            color: Base color for particles
            count: Number of particles to create
        """
        for _ in range(count):
            particle = Particle(x, y, color)
            self.particles.append(particle)
    
    def create_tetris_effect(self, screen_width: int, screen_height: int):
        """Create special effect for Tetris achievement.
        
        Args:
            screen_width: Screen width for random positioning
            screen_height: Screen height for random positioning
        """
        # Create golden rain effect
        gold_colors = [
            COLORS['particle_gold'],
            (218, 165, 32),  # Golden rod
            (184, 134, 11),  # Dark golden rod
        ]
        
        for _ in range(80):
            x = random.uniform(0, screen_width)
            y = random.uniform(0, screen_height)
            color = random.choice(gold_colors)
            self.create_explosion(x, y, color, 1)
    
    def update(self):
        """Update all particles."""
        # Update existing particles
        for particle in self.particles:
            particle.update()
        
        # Remove dead particles
        self.particles = [p for p in self.particles if not p.is_dead()]
        
        # Enforce particle limit to prevent memory issues
        if len(self.particles) > self.max_particles:
            # Keep the newest particles
            self.particles = self.particles[-self.max_particles:]
    
    def draw(self, surface: pygame.Surface):
        """Draw all particles.
        
        Args:
            surface: Pygame surface to draw on
        """
        for particle in self.particles:
            particle.draw(surface)
    
    def clear(self):
        """Remove all particles."""
        self.particles.clear()
    
    def get_particle_count(self) -> int:
        """Get current number of active particles.
        
        Returns:
            Number of active particles
        """
        return len(self.particles)