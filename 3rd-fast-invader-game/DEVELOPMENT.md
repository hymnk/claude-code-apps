# Development Guide - Fast Invader Game

Complete development guide for contributing to and extending the Fast Invader Game TypeScript implementation.

## Table of Contents

- [Development Environment](#development-environment)
- [Code Architecture](#code-architecture)
- [Testing Strategy](#testing-strategy)
- [Build Process](#build-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Debugging](#debugging)
- [Performance Optimization](#performance-optimization)
- [Extending the Game](#extending-the-game)

## Development Environment

### Prerequisites

```bash
# Required versions
Node.js >= 16.0.0
npm >= 7.0.0
TypeScript >= 5.0.0
```

### Setup

```bash
# Clone repository
git clone https://github.com/hymnk/claude-code-apps.git
cd claude-code-apps/3rd-fast-invader-game

# Install dependencies
npm install

# Initial build
npm run build

# Start development mode
npm run dev
```

### Development Scripts

```json
{
  "scripts": {
    "build": "tsc",                    // Compile TypeScript
    "watch": "tsc --watch",            // Watch mode compilation
    "dev": "tsc --watch",              // Development alias
    "clean": "rm -rf dist",            // Clean build artifacts
    "test": "jest",                    // Run tests
    "test:watch": "jest --watch",      // Watch mode testing
    "test:coverage": "jest --coverage" // Coverage reporting
  }
}
```

### VS Code Configuration

Recommended `.vscode/settings.json`:

```json
{
  "typescript.preferences.noSemicolons": "off",
  "typescript.preferences.quoteStyle": "single",
  "typescript.format.insertSpaceAfterOpeningAndBeforeClosingNonemptyBrackets": false,
  "typescript.format.placeOpenBraceOnNewLineForControlBlocks": false,
  "typescript.format.placeOpenBraceOnNewLineForFunctions": false,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true,
    "source.fixAll": true
  }
}
```

## Code Architecture

### Module System

The game uses ES6 modules with TypeScript compilation:

```typescript
// Import syntax
import { GameState, Particle } from './types.js';
import { Player } from './player.js';

// Export syntax
export class Game { ... }
export interface GameObject { ... }
export type GameState = 'menu' | 'playing';
```

### Directory Structure

```
src/
├── types.ts        # Core type definitions
├── main.ts         # Application entry point
├── game.ts         # Game controller and state
├── player.ts       # Player class
├── invader.ts      # Invader class
└── bullet.ts       # Bullet class

tests/
├── setup.ts        # Test environment setup
├── *.test.ts       # Individual test files
└── integration.test.ts  # End-to-end tests
```

### Dependency Graph

```
main.ts
  └── game.ts
      ├── types.ts
      ├── player.ts
      │   ├── types.ts
      │   └── bullet.ts
      ├── invader.ts
      │   └── types.ts
      └── bullet.ts
          └── types.ts
```

### Design Patterns

#### Component Pattern
Each game object (Player, Invader, Bullet) implements the GameObject interface:

```typescript
interface GameObject {
  x: number;
  y: number;
  width: number;
  height: number;
}

class Player implements GameObject {
  // Implementation
}
```

#### State Pattern
Game state management:

```typescript
type GameState = 'menu' | 'playing' | 'paused' | 'gameOver';

class Game {
  private gameState: GameState = 'menu';
  
  update() {
    switch (this.gameState) {
      case 'playing': this.updateGame(); break;
      case 'paused': break;
      // ...
    }
  }
}
```

#### Object Pool Pattern (Future Enhancement)
For performance optimization with bullets and particles:

```typescript
class ObjectPool<T> {
  private pool: T[] = [];
  private createFn: () => T;
  
  get(): T {
    return this.pool.pop() || this.createFn();
  }
  
  release(obj: T): void {
    this.pool.push(obj);
  }
}
```

## Testing Strategy

### Test Types

1. **Unit Tests**: Individual class testing
2. **Integration Tests**: Multi-component workflows
3. **Mock Testing**: DOM and Canvas API simulation

### Test Structure

```typescript
describe('ClassName', () => {
  let instance: ClassName;
  
  beforeEach(() => {
    // Setup before each test
    instance = new ClassName();
  });
  
  describe('methodName', () => {
    it('should perform expected behavior', () => {
      // Arrange
      const input = 'test';
      
      // Act
      const result = instance.methodName(input);
      
      // Assert
      expect(result).toBe('expected');
    });
  });
});
```

### Mock Setup

Canvas API mocking in `tests/setup.ts`:

```typescript
class MockCanvasRenderingContext2D {
  fillStyle: string = '#000';
  // ... other properties
  
  fillRect() {}
  beginPath() {}
  // ... other methods
}

global.HTMLCanvasElement = MockHTMLCanvasElement;
```

### Writing New Tests

1. **Create test file**: `tests/new-feature.test.ts`
2. **Import dependencies**:
   ```typescript
   import { NewFeature } from '../src/new-feature';
   ```
3. **Follow AAA pattern**: Arrange, Act, Assert
4. **Test edge cases**: Boundaries, null values, errors
5. **Mock external dependencies**: DOM, timers, random

### Test Coverage Goals

- **Statements**: >85%
- **Branches**: >70%
- **Functions**: >80%
- **Lines**: >85%

## Build Process

### TypeScript Configuration

Key `tsconfig.json` settings:

```json
{
  "compilerOptions": {
    "target": "ES2020",           // Modern JavaScript features
    "module": "ES6",              // ES6 modules
    "lib": ["ES2020", "DOM"],     // Available APIs
    "outDir": "./dist",           // Output directory
    "rootDir": "./src",           // Source directory
    "strict": true,               // Strict type checking
    "sourceMap": true,            // Debug maps
    "declaration": true,          // .d.ts files
    "removeComments": false,      // Keep comments
    "noImplicitAny": true,        // Explicit types
    "strictNullChecks": true      // Null safety
  }
}
```

### Build Pipeline

1. **TypeScript Compilation**:
   ```bash
   tsc --project tsconfig.json
   ```

2. **Output Verification**:
   ```bash
   # Check generated files
   ls -la dist/
   ```

3. **Testing**:
   ```bash
   npm test
   ```

4. **Manual Testing**:
   - Open `index.html` in browser
   - Verify game functionality

### Watch Mode Development

```bash
# Terminal 1: Build watching
npm run watch

# Terminal 2: Test watching
npm run test:watch

# Terminal 3: Local server (optional)
npx http-server . -p 8080
```

## Code Style Guidelines

### TypeScript Style

```typescript
// Use explicit types for public APIs
public movePlayer(direction: 'left' | 'right'): void

// Use type inference for obvious cases
const speed = 5; // inferred as number

// Prefer interfaces over types for objects
interface GameConfig {
  width: number;
  height: number;
}

// Use readonly for immutable data
interface ReadonlyConfig {
  readonly maxLives: number;
}
```

### Naming Conventions

```typescript
// Classes: PascalCase
class GameController { }

// Methods and variables: camelCase
public moveLeft(): void
private playerSpeed: number

// Constants: UPPER_SNAKE_CASE
const MAX_BULLETS = 10;

// Types and interfaces: PascalCase
type GameState = 'playing';
interface GameObject { }

// Private members: prefix with underscore
private _internalState: boolean;
```

### Method Organization

```typescript
class Player {
  // 1. Public properties
  public x: number;
  public y: number;
  
  // 2. Private properties
  private speed: number;
  
  // 3. Constructor
  constructor(x: number, y: number) { }
  
  // 4. Public methods
  public moveLeft(): void { }
  public shoot(): Bullet | null { }
  
  // 5. Private methods
  private canShoot(): boolean { }
}
```

### Error Handling

```typescript
// Explicit error types
class GameError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = 'GameError';
  }
}

// Validation with early returns
public movePlayer(direction: string): void {
  if (!direction) {
    throw new GameError('Direction is required', 'INVALID_INPUT');
  }
  
  if (!this.player) {
    return; // Graceful degradation
  }
  
  // Main logic
}
```

## Debugging

### Browser DevTools

1. **Source Maps**: Enable in TypeScript for debugging original code
2. **Breakpoints**: Set in TypeScript files, not compiled JavaScript
3. **Console**: Use `console.log`, `console.warn`, `console.error`

### Debug Mode

Use `test.html` for enhanced debugging:

```html
<!-- Debug display -->
<div id="debugInfo">
  <div id="gameState">Game State: </div>
  <div id="invaderCount">Invaders: </div>
  <div id="bulletCount">Bullets: </div>
</div>
```

### Debug Utilities

```typescript
// Debug logging helper
class Debug {
  static log(component: string, message: string, data?: any): void {
    if (process.env.NODE_ENV === 'development') {
      console.log(`[${component}] ${message}`, data);
    }
  }
}

// Usage
Debug.log('Player', 'Shot fired', { x: player.x, y: player.y });
```

### Common Issues

1. **Module Import Errors**:
   ```bash
   # Rebuild TypeScript
   npm run clean && npm run build
   ```

2. **Test Failures**:
   ```bash
   # Clear Jest cache
   npx jest --clearCache
   ```

3. **Canvas Issues**:
   ```javascript
   // Check context availability
   const ctx = canvas.getContext('2d');
   if (!ctx) {
     throw new Error('Canvas 2D context not supported');
   }
   ```

## Performance Optimization

### Frame Rate Management

```typescript
class Game {
  private lastTime: number = 0;
  
  gameLoop(currentTime: number): void {
    const deltaTime = (currentTime - this.lastTime) / 16.67; // Normalize to 60fps
    this.lastTime = currentTime;
    
    this.update(deltaTime);
    this.render();
    
    requestAnimationFrame((time) => this.gameLoop(time));
  }
}
```

### Collision Detection Optimization

```typescript
// Spatial partitioning for large numbers of objects
class SpatialGrid {
  private grid: Map<string, GameObject[]> = new Map();
  private cellSize: number = 64;
  
  insert(obj: GameObject): void {
    const key = this.getGridKey(obj.x, obj.y);
    if (!this.grid.has(key)) {
      this.grid.set(key, []);
    }
    this.grid.get(key)!.push(obj);
  }
  
  getNearby(obj: GameObject): GameObject[] {
    // Return only objects in same or adjacent cells
  }
}
```

### Memory Management

```typescript
// Object pooling for frequently created/destroyed objects
class BulletPool {
  private pool: Bullet[] = [];
  
  getBullet(): Bullet {
    return this.pool.pop() || new Bullet(0, 0, 0);
  }
  
  releaseBullet(bullet: Bullet): void {
    // Reset bullet state
    bullet.x = 0;
    bullet.y = 0;
    this.pool.push(bullet);
  }
}
```

### Rendering Optimization

```typescript
// Batch rendering operations
class Renderer {
  render(objects: GameObject[]): void {
    this.ctx.save();
    
    // Group by rendering state
    const playerObjects = objects.filter(obj => obj.type === 'player');
    const enemyObjects = objects.filter(obj => obj.type === 'enemy');
    
    // Render groups together
    this.renderGroup(playerObjects, '#00ff00');
    this.renderGroup(enemyObjects, '#ff0000');
    
    this.ctx.restore();
  }
}
```

## Extending the Game

### Adding New Enemy Types

1. **Extend Invader class**:
   ```typescript
   class BossInvader extends Invader {
     private health: number = 5;
     
     takeDamage(): boolean {
       this.health--;
       return this.health <= 0;
     }
   }
   ```

2. **Update type system**:
   ```typescript
   type InvaderType = 1 | 2 | 3 | 'boss';
   ```

3. **Add rendering**:
   ```typescript
   renderBoss(ctx: CanvasRenderingContext2D): void {
     // Custom boss rendering
   }
   ```

### Adding Power-ups

1. **Create PowerUp class**:
   ```typescript
   class PowerUp implements GameObject {
     constructor(
       public x: number,
       public y: number,
       public type: 'speed' | 'multishot' | 'shield'
     ) {}
   }
   ```

2. **Collision detection**:
   ```typescript
   checkPowerUpCollisions(): void {
     for (const powerUp of this.powerUps) {
       if (this.isColliding(this.player, powerUp)) {
         this.applyPowerUp(powerUp.type);
         this.removePowerUp(powerUp);
       }
     }
   }
   ```

### Adding Sound Effects

1. **Audio manager**:
   ```typescript
   class AudioManager {
     private sounds: Map<string, HTMLAudioElement> = new Map();
     
     load(name: string, url: string): void {
       const audio = new Audio(url);
       this.sounds.set(name, audio);
     }
     
     play(name: string): void {
       const sound = this.sounds.get(name);
       if (sound) {
         sound.currentTime = 0;
         sound.play();
       }
     }
   }
   ```

2. **Integration**:
   ```typescript
   // In collision detection
   if (bulletHitsInvader) {
     audioManager.play('explosion');
   }
   ```

### Adding Particle Effects

1. **Enhanced particle system**:
   ```typescript
   interface EnhancedParticle extends Particle {
     type: 'explosion' | 'trail' | 'pickup';
     size: number;
     rotation: number;
     rotationSpeed: number;
   }
   ```

2. **Particle behaviors**:
   ```typescript
   updateParticles(deltaTime: number): void {
     this.particles.forEach(particle => {
       // Position update
       particle.x += particle.vx * deltaTime;
       particle.y += particle.vy * deltaTime;
       
       // Rotation update
       particle.rotation += particle.rotationSpeed * deltaTime;
       
       // Life update
       particle.life -= deltaTime;
     });
   }
   ```

### Testing New Features

1. **Unit tests for new classes**
2. **Integration tests for feature workflows**
3. **Performance testing for impact**
4. **Cross-browser compatibility testing**

### Documentation Updates

When adding features:

1. **Update API.md** with new methods and classes
2. **Update README.md** with new game features
3. **Add inline JSDoc comments**
4. **Update test documentation**

---

This development guide provides comprehensive information for contributing to and extending the Fast Invader Game. Follow these guidelines to maintain code quality and consistency across the project.