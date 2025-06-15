# Fast Invader Game - TypeScript Edition

A modern TypeScript implementation of the classic Space Invaders game using HTML5 Canvas and comprehensive testing.

## 🚀 Features

- **TypeScript Implementation**: Fully typed codebase with strict type checking
- **Modern ES6+ Modules**: Clean import/export structure
- **Comprehensive Testing**: 89 tests with 85.98% coverage
- **Canvas-based Graphics**: Smooth animations and particle effects
- **Responsive Controls**: Keyboard input with proper event handling
- **Progressive Difficulty**: Increasing speed and challenge with each level

## 🎮 Game Controls

| Key | Action |
|-----|--------|
| `←` / `A` | Move player left |
| `→` / `D` | Move player right |
| `Space` | Shoot |
| `P` | Pause/Resume |

## 🛠️ Technical Stack

- **Language**: TypeScript 5.0+
- **Build Tool**: TypeScript Compiler (tsc)
- **Testing**: Jest with ts-jest
- **Environment**: Browser (ES2020+)
- **Graphics**: HTML5 Canvas API

## 📁 Project Structure

```
├── src/                    # TypeScript source files
│   ├── types.ts           # Type definitions and interfaces
│   ├── bullet.ts          # Bullet class implementation
│   ├── player.ts          # Player class implementation
│   ├── invader.ts         # Invader class implementation
│   ├── game.ts            # Main game logic and state management
│   └── main.ts            # Application entry point
├── tests/                 # Test files
│   ├── setup.ts           # Jest test environment setup
│   ├── bullet.test.ts     # Bullet class unit tests
│   ├── player.test.ts     # Player class unit tests
│   ├── invader.test.ts    # Invader class unit tests
│   ├── game.test.ts       # Game class unit tests
│   └── integration.test.ts # Integration tests
├── dist/                  # Compiled JavaScript (generated)
├── coverage/              # Test coverage reports (generated)
├── index.html             # Main game page
├── test.html              # Debug/testing page
├── style.css              # Game styles
├── package.json           # Dependencies and scripts
├── tsconfig.json          # TypeScript configuration
├── jest.config.js         # Jest testing configuration
└── .gitignore             # Git ignore rules
```

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm
- Modern web browser with ES2020+ support

### Installation

```bash
# Clone the repository
git clone https://github.com/hymnk/claude-code-apps.git
cd claude-code-apps/3rd-fast-invader-game

# Install dependencies
npm install

# Build the TypeScript code
npm run build
```

### Development

```bash
# Start development with file watching
npm run dev

# Run tests
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

### Playing the Game

1. Open `index.html` in a web browser
2. Click "Start Game" to begin
3. Use arrow keys or WASD to move
4. Press Space to shoot
5. Destroy all invaders to advance to the next level

## 🏗️ Architecture

### Type System

The game uses a robust type system defined in `src/types.ts`:

```typescript
// Game state management
type GameState = 'menu' | 'playing' | 'paused' | 'gameOver';

// Game object interface
interface GameObject {
  x: number;
  y: number;
  width: number;
  height: number;
}

// Particle system for explosions
interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  color: string;
}
```

### Class Hierarchy

```typescript
// Base game object interface
GameObject
├── Player implements GameObject
├── Invader implements GameObject
└── Bullet implements GameObject

// Main game controller
Game {
  - State management
  - Collision detection
  - Rendering pipeline
  - Event handling
}
```

### Key Classes

#### Player Class
```typescript
class Player implements GameObject {
  public moveLeft(): void
  public moveRight(canvasWidth: number): void
  public canShoot(): boolean
  public shoot(): Bullet | null
  public render(ctx: CanvasRenderingContext2D): void
}
```

#### Invader Class
```typescript
class Invader implements GameObject {
  public type: number        // Determines appearance and points
  public points: number      // Score value when destroyed
  public update(deltaTime: number): void
  public render(ctx: CanvasRenderingContext2D): void
}
```

#### Game Class
```typescript
class Game {
  public isColliding(obj1: GameObject, obj2: GameObject): boolean
  public startGame(): void
  public render(): void
  public gameLoop(currentTime: number): void
}
```

## 🧪 Testing

The project includes comprehensive testing with Jest:

### Test Structure

- **Unit Tests**: Individual class testing with mocked dependencies
- **Integration Tests**: Full game mechanic workflows
- **Coverage Reports**: Detailed analysis of code coverage

### Running Tests

```bash
# Run all tests
npm test

# Generate coverage report
npm run test:coverage

# Watch mode for development
npm run test:watch
```

### Test Coverage

Current coverage metrics:

| File | Statements | Branches | Functions | Lines |
|------|------------|----------|-----------|-------|
| **Overall** | **85.98%** | **72.6%** | **80.35%** | **87.67%** |
| bullet.ts | 100% | 100% | 100% | 100% |
| player.ts | 100% | 100% | 100% | 100% |
| invader.ts | 100% | 87.5% | 100% | 100% |
| game.ts | 79.6% | 67.79% | 72.5% | 81.7% |

### Writing Tests

Example unit test structure:

```typescript
import { Player } from '../src/player';

describe('Player', () => {
  let player: Player;

  beforeEach(() => {
    player = new Player(100, 200);
  });

  it('should move left correctly', () => {
    const initialX = player.x;
    player.moveLeft();
    expect(player.x).toBe(initialX - player.speed);
  });
});
```

## 🎯 Game Mechanics

### Collision Detection

The game uses AABB (Axis-Aligned Bounding Box) collision detection:

```typescript
public isColliding(obj1: GameObject, obj2: GameObject): boolean {
  return obj1.x < obj2.x + obj2.width &&
         obj1.x + obj1.width > obj2.x &&
         obj1.y < obj2.y + obj2.height &&
         obj1.y + obj1.height > obj2.y;
}
```

### Particle System

Explosion effects use a simple particle system:

```typescript
interface Particle {
  x: number;      // Position
  y: number;
  vx: number;     // Velocity
  vy: number;
  life: number;   // Remaining life
  maxLife: number;
  color: string;  // HSL color
}
```

### Level Progression

Each level increases difficulty:
- Invader movement speed increases by 0.5
- Shooting frequency increases (interval decreases by 10, min 60)
- New invader formation spawns

## 🔧 Configuration

### TypeScript Configuration

Key settings in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES6",
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "sourceMap": true
  }
}
```

### Jest Configuration

Test setup in `jest.config.js`:

```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  moduleNameMapper: {
    '^(\\.{1,2}/.*)\\.js$': '$1'
  }
};
```

## 🚀 Deployment

### Production Build

```bash
# Clean previous builds
npm run clean

# Build for production
npm run build

# Serve the files
# Open index.html in a web browser
```

### File Structure for Deployment

Required files for deployment:
- `index.html` - Main game page
- `style.css` - Game styles
- `dist/` - Compiled JavaScript files
- Assets (if any)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes with TypeScript
4. Add/update tests for new functionality
5. Ensure all tests pass: `npm test`
6. Check code coverage: `npm run test:coverage`
7. Commit changes: `git commit -m "Description"`
8. Push to branch: `git push origin feature-name`
9. Create a Pull Request

### Code Style Guidelines

- Use TypeScript strict mode
- Follow existing naming conventions
- Add JSDoc comments for public methods
- Maintain test coverage above 80%
- Use meaningful variable and function names

## 📄 License

MIT License - see LICENSE file for details

## 🎮 Game Features

### Player Mechanics
- Smooth movement with boundary checking
- Shooting with cooldown system
- Visual feedback and animations

### Enemy AI
- Coordinated movement patterns
- Progressive difficulty scaling
- Random shooting behavior

### Visual Effects
- Particle explosion system
- Smooth animations
- Retro-style graphics
- Dynamic UI updates

## 🐛 Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   # Ensure TypeScript compilation
   npm run build
   ```

2. **Test Failures**
   ```bash
   # Clear Jest cache
   npx jest --clearCache
   npm test
   ```

3. **Canvas Not Rendering**
   - Check browser console for errors
   - Ensure `dist/main.js` exists
   - Verify Canvas API support

### Debug Mode

Use `test.html` for debugging:
- Real-time game state display
- Error logging
- Manual collision simulation

## 📚 Resources

- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Jest Testing Framework](https://jestjs.io/docs/getting-started)
- [HTML5 Canvas API](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)
- [Game Development Patterns](https://gameprogrammingpatterns.com/)

---

**Built with TypeScript and tested comprehensively for a modern gaming experience! 🎮**