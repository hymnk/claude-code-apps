# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**1st ZEN Tetris** - A browser-based Tetris game built with HTML5 Canvas, CSS, and vanilla JavaScript. Features classic Tetris gameplay with calming earth-tone colors, particle effects, and a zen-like aesthetic designed for relaxation and mindfulness.

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Graphics**: HTML5 Canvas API
- **No build tools required** - runs directly in browser

## Architecture

### Core Files
- `index.html` - Main HTML structure and game layout
- `style.css` - Game styling with gradient backgrounds and responsive design
- `tetris.js` - Complete game logic implementation

### Game Structure
- **TetrisGame class** - Main game controller handling all game logic
- **Tetromino system** - 7 standard pieces (I, O, T, S, Z, J, L) with rotation
- **Board management** - 10x20 grid with collision detection
- **Scoring system** - Standard Tetris scoring with levels and line clearing

## Development Commands

```bash
# Serve locally (any simple HTTP server)
python -m http.server 8000
# or
npx serve .

# View in browser
open http://localhost:8000
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