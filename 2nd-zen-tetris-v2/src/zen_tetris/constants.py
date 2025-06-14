"""
Constants for ZEN Tetris v2 - Earth-tone colors and game settings.
"""

# Game dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30

# Colors - Earth tone palette inspired by nature
COLORS = {
    # Background colors
    'background': (139, 115, 85),  # Warm brown
    'board_bg': (26, 26, 26),      # Dark charcoal
    'ui_bg': (245, 245, 220),      # Beige
    'ui_accent': (107, 91, 115),   # Dusty purple
    
    # Tetromino colors (earth tones)
    'I': (139, 115, 85),   # Warm brown
    'O': (210, 180, 140),  # Tan
    'T': (107, 91, 115),   # Dusty purple
    'S': (156, 175, 136),  # Sage green
    'Z': (160, 132, 92),   # Mocha
    'J': (125, 132, 113),  # Olive gray
    'L': (184, 146, 106),  # Honey brown
    
    # Effect colors
    'particle_gold': (212, 175, 55),
    'particle_light': (245, 245, 220),
    'flash_white': (255, 255, 255),
    'shadow': (46, 62, 45),
    
    # UI text colors
    'text_primary': (60, 79, 61),
    'text_light': (245, 245, 220),
    'text_accent': (212, 175, 55),
}

# Tetromino shapes
TETROMINO_SHAPES = {
    'I': [
        ['1', '1', '1', '1']
    ],
    'O': [
        ['1', '1'],
        ['1', '1']
    ],
    'T': [
        ['0', '1', '0'],
        ['1', '1', '1']
    ],
    'S': [
        ['0', '1', '1'],
        ['1', '1', '0']
    ],
    'Z': [
        ['1', '1', '0'],
        ['0', '1', '1']
    ],
    'J': [
        ['1', '0', '0'],
        ['1', '1', '1']
    ],
    'L': [
        ['0', '0', '1'],
        ['1', '1', '1']
    ]
}

# Game settings
FPS = 60
DROP_SPEED = 500  # milliseconds (faster for testing)
LINES_PER_LEVEL = 10
SPEED_INCREASE_PER_LEVEL = 50  # milliseconds faster

# Scoring
SCORE_VALUES = {
    1: 100,   # Single
    2: 300,   # Double
    3: 500,   # Triple
    4: 800,   # Tetris
}

# Particle settings
PARTICLE_COUNT = 15
PARTICLE_LIFETIME = 60
PARTICLE_GRAVITY = 0.3
PARTICLE_SIZE_RANGE = (2, 6)
PARTICLE_SPEED_RANGE = (-8, 8)

# UI layout
UI_MARGIN = 20
SIDEBAR_WIDTH = 200
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 100