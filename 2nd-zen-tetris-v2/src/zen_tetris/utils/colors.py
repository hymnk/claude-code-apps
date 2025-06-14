"""
Color utilities for ZEN Tetris v2 earth-tone aesthetic.
"""

import pygame
from typing import Tuple

from ..constants import COLORS


def apply_earth_tone_gradient(surface: pygame.Surface, width: int, height: int):
    """Apply earth-tone gradient background.
    
    Args:
        surface: Pygame surface to draw on
        width: Surface width
        height: Surface height
    """
    # Create gradient from warm brown to dusty purple to olive
    start_color = (139, 115, 85)    # Warm brown
    mid_color = (107, 91, 115)      # Dusty purple  
    end_color = (74, 93, 35)        # Olive
    
    for y in range(height):
        # Calculate position in gradient (0.0 to 1.0)
        pos = y / height
        
        if pos < 0.5:
            # First half: brown to purple
            blend = pos * 2
            r = int(start_color[0] * (1 - blend) + mid_color[0] * blend)
            g = int(start_color[1] * (1 - blend) + mid_color[1] * blend)
            b = int(start_color[2] * (1 - blend) + mid_color[2] * blend)
        else:
            # Second half: purple to olive
            blend = (pos - 0.5) * 2
            r = int(mid_color[0] * (1 - blend) + end_color[0] * blend)
            g = int(mid_color[1] * (1 - blend) + end_color[1] * blend)
            b = int(mid_color[2] * (1 - blend) + end_color[2] * blend)
        
        color = (r, g, b)
        pygame.draw.line(surface, color, (0, y), (width, y))


def blend_colors(color1: Tuple[int, int, int], color2: Tuple[int, int, int], 
                 factor: float) -> Tuple[int, int, int]:
    """Blend two colors together.
    
    Args:
        color1: First RGB color
        color2: Second RGB color
        factor: Blend factor (0.0 = color1, 1.0 = color2)
        
    Returns:
        Blended RGB color
    """
    factor = max(0.0, min(1.0, factor))  # Clamp to [0, 1]
    
    r = int(color1[0] * (1 - factor) + color2[0] * factor)
    g = int(color1[1] * (1 - factor) + color2[1] * factor)
    b = int(color1[2] * (1 - factor) + color2[2] * factor)
    
    return (r, g, b)


def darken_color(color: Tuple[int, int, int], amount: int = 30) -> Tuple[int, int, int]:
    """Darken a color by specified amount.
    
    Args:
        color: RGB color to darken
        amount: Amount to darken (0-255)
        
    Returns:
        Darkened RGB color
    """
    return tuple(max(0, c - amount) for c in color)


def lighten_color(color: Tuple[int, int, int], amount: int = 20) -> Tuple[int, int, int]:
    """Lighten a color by specified amount.
    
    Args:
        color: RGB color to lighten
        amount: Amount to lighten (0-255)
        
    Returns:
        Lightened RGB color
    """
    return tuple(min(255, c + amount) for c in color)


def get_zen_palette() -> dict:
    """Get the complete ZEN earth-tone color palette.
    
    Returns:
        Dictionary of named colors
    """
    return COLORS.copy()


def create_glow_effect(surface: pygame.Surface, color: Tuple[int, int, int], 
                      rect: pygame.Rect, intensity: float = 0.5):
    """Create a glow effect around a rectangle.
    
    Args:
        surface: Pygame surface to draw on
        color: Glow color
        rect: Rectangle to glow around
        intensity: Glow intensity (0.0 to 1.0)
    """
    # Create glow surface
    glow_size = 10
    glow_surface = pygame.Surface((rect.width + glow_size * 2, 
                                  rect.height + glow_size * 2), 
                                 pygame.SRCALPHA)
    
    # Draw multiple layers for glow effect
    alpha = int(255 * intensity)
    for i in range(glow_size):
        glow_alpha = alpha // (i + 1)
        glow_color = (*color, glow_alpha)
        
        glow_rect = pygame.Rect(glow_size - i, glow_size - i,
                               rect.width + i * 2, rect.height + i * 2)
        pygame.draw.rect(glow_surface, glow_color, glow_rect, 2)
    
    # Blit glow to main surface
    surface.blit(glow_surface, (rect.x - glow_size, rect.y - glow_size))