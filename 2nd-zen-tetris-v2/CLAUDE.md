# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**2nd ZEN Tetris v2** - An enhanced Python+Pygame version of the earth-tone Tetris game, now with complete Web support. Features both native Python gameplay and browser-based versions with FastAPI+WebSocket backend for real-time multiplayer sessions.

## Technology Stack

### Python Version (Native)
- **Backend**: Python 3.8+ with Pygame 2.6+
- **Graphics**: Pygame rendering with hardware acceleration
- **Libraries**: NumPy for numerical calculations

### Web Version (Browser)
- **Backend**: FastAPI + WebSocket for real-time communication
- **Frontend**: HTML5 Canvas + JavaScript (ES6+)
- **Communication**: WebSocket bidirectional real-time updates
- **No build tools required** - runs directly in browser

## Architecture

### Python Version Files
- `main.py` - Entry point for native Python version
- `src/zen_tetris/game.py` - Main game controller with Pygame rendering
- `src/zen_tetris/components/` - Core game components (Board, Tetromino)
- `src/zen_tetris/effects/` - Particle system and visual effects
- `tests/` - Comprehensive test suite with 95%+ coverage

### Web Version Files
- `web_server.py` - FastAPI server with WebSocket endpoints
- `src/zen_tetris/web_game.py` - Pygame-free web-compatible game logic
- `web_templates/index.html` - Browser game interface
- `web_static/tetris-client.js` - Canvas rendering and WebSocket client
- `start_web.py` - Quick start script for web version

### Game Structure
- **ZenTetrisGame class** - Main game controller handling all game logic
- **WebZenTetrisGame class** - Web-optimized version without Pygame dependencies
- **Tetromino system** - 7 standard pieces (I, O, T, S, Z, J, L) with rotation
- **Board management** - 10x20 grid with collision detection and line clearing
- **Particle system** - Physics-based star particles for visual effects
- **Scoring system** - Standard Tetris scoring with levels and combo bonuses

## Development Commands

### Python Version
```bash
# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run native Python version
python main.py

# Run tests
python run_tests.py
```

### Web Version
```bash
# Quick start (auto-opens browser)
python start_web.py

# Manual start
python web_server.py
# Then open http://localhost:8000

# Health check
curl http://localhost:8000/health
```

## Game Controls

- **Arrow Keys**: Move and rotate pieces
- **Space**: Hard drop
- **Pause/Resume**: Pause button or game controls
- **Reset**: Start new game

## Key Features Implemented

- **Classic 7-piece Tetromino set** with earth-tone colors
- **Particle effects system** with star-shaped particles and physics
- **Enhanced line clearing** with flash effects and explosions
- **Zen aesthetic** featuring calming earth colors (browns, tans, sage greens)
- **Special Tetris effects** with golden particle explosions and screen flash
- **Progressive difficulty** with increasing speed per level
- **Next piece preview** with styled canvas
- **Responsive design** optimized for desktop and mobile
- **Smooth animations** and visual feedback throughout gameplay