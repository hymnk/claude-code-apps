# Fast Invader Game - API Documentation

Comprehensive API documentation for the TypeScript implementation of Fast Invader Game.

## Table of Contents

- [Core Types](#core-types)
- [Game Class](#game-class)
- [Player Class](#player-class)
- [Invader Class](#invader-class)
- [Bullet Class](#bullet-class)
- [Interfaces](#interfaces)
- [Enums and Types](#enums-and-types)

## Core Types

### GameState
```typescript
type GameState = 'menu' | 'playing' | 'paused' | 'gameOver';
```
Represents the current state of the game.

### BulletType
```typescript
type BulletType = 'player' | 'enemy';
```
Distinguishes between player and enemy bullets for rendering and behavior.

### KeyState
```typescript
interface KeyState {
  [key: string]: boolean;
}
```
Tracks the pressed state of keyboard keys.

## Interfaces

### GameObject
Base interface for all game entities with position and dimensions.

```typescript
interface GameObject {
  x: number;        // X coordinate in pixels
  y: number;        // Y coordinate in pixels
  width: number;    // Width in pixels
  height: number;   // Height in pixels
}
```

### Particle
Represents explosion particles in the particle system.

```typescript
interface Particle {
  x: number;        // Current X position
  y: number;        // Current Y position
  vx: number;       // X velocity per frame
  vy: number;       // Y velocity per frame
  life: number;     // Remaining life frames
  maxLife: number;  // Initial life frames
  color: string;    // HSL color string
}
```

## Game Class

The main game controller managing state, rendering, and game loop.

### Constructor
```typescript
constructor(canvas: HTMLCanvasElement)
```
Initializes the game with a canvas element.

**Parameters:**
- `canvas: HTMLCanvasElement` - The canvas element for rendering

**Throws:**
- `Error` - If canvas 2D context cannot be obtained

### Public Methods

#### isColliding
```typescript
public isColliding(
  obj1: { x: number; y: number; width: number; height: number }, 
  obj2: { x: number; y: number; width: number; height: number }
): boolean
```
Detects collision between two rectangular objects using AABB.

**Parameters:**
- `obj1` - First object with position and dimensions
- `obj2` - Second object with position and dimensions

**Returns:**
- `boolean` - True if objects are colliding

**Example:**
```typescript
const collision = game.isColliding(player, invader);
if (collision) {
  // Handle collision
}
```

#### startGame
```typescript
public startGame(): void
```
Initializes and starts a new game session.

**Effects:**
- Creates player instance
- Spawns invader formation
- Sets game state to 'playing'
- Starts game loop

#### render
```typescript
public render(): void
```
Renders the current frame based on game state.

**Behavior:**
- Clears canvas
- Renders appropriate screen (menu/game/pause)
- Updates visual elements

#### gameLoop
```typescript
public gameLoop(currentTime: number = 0): void
```
Main game loop handling updates and rendering.

**Parameters:**
- `currentTime: number` - Current timestamp from requestAnimationFrame

**Features:**
- Frame rate normalization
- Error handling with recovery
- Automatic loop continuation

### Private Methods

#### createInvaders
```typescript
private createInvaders(): void
```
Creates the initial invader formation.

**Formation:**
- 5 rows × 10 columns = 50 invaders
- Different types based on row (1-3)
- Centered grid layout

#### updatePlayer
```typescript
private updatePlayer(deltaTime: number): void
```
Updates player state based on input and time.

#### updateInvaders
```typescript
private updateInvaders(deltaTime: number): void
```
Updates all invaders' positions and AI behavior.

#### checkCollisions
```typescript
private checkCollisions(): void
```
Processes all collision detection and responses.

#### createExplosion
```typescript
private createExplosion(x: number, y: number): void
```
Creates particle explosion at specified coordinates.

## Player Class

Represents the player's ship with movement and shooting capabilities.

### Constructor
```typescript
constructor(x: number, y: number)
```
Creates a player at the specified position.

**Parameters:**
- `x: number` - Initial X coordinate
- `y: number` - Initial Y coordinate

### Properties
```typescript
public x: number;           // Current X position
public y: number;           // Current Y position
public width: number = 40;  // Ship width in pixels
public height: number = 30; // Ship height in pixels
public speed: number = 5;   // Movement speed per frame
```

### Public Methods

#### moveLeft
```typescript
public moveLeft(): void
```
Moves player left within screen boundaries.

**Behavior:**
- Decreases X position by speed
- Prevents movement beyond left edge (x < 0)

#### moveRight
```typescript
public moveRight(canvasWidth: number): void
```
Moves player right within screen boundaries.

**Parameters:**
- `canvasWidth: number` - Canvas width for boundary checking

**Behavior:**
- Increases X position by speed
- Prevents movement beyond right edge

#### canShoot
```typescript
public canShoot(): boolean
```
Checks if player can shoot based on cooldown.

**Returns:**
- `boolean` - True if enough time has passed since last shot

**Cooldown:**
- 250 milliseconds between shots

#### shoot
```typescript
public shoot(): Bullet | null
```
Creates a bullet if shooting is allowed.

**Returns:**
- `Bullet` - New bullet instance if successful
- `null` - If still on cooldown

**Bullet Properties:**
- Spawns at player center
- Moves upward with speed -7
- Type: 'player'

#### update
```typescript
public update(deltaTime: number): void
```
Updates player state (currently placeholder).

#### render
```typescript
public render(ctx: CanvasRenderingContext2D): void
```
Renders the player ship with visual effects.

**Visual Elements:**
- Ship body (rectangle)
- Triangular nose
- Side wings
- Engine glow effect (gradient)

## Invader Class

Represents enemy invaders with different types and behaviors.

### Constructor
```typescript
constructor(x: number, y: number, type: number = 1)
```
Creates an invader of specified type.

**Parameters:**
- `x: number` - Initial X coordinate
- `y: number` - Initial Y coordinate
- `type: number` - Invader type (1-3), defaults to 1

### Properties
```typescript
public x: number;           // Current X position
public y: number;           // Current Y position
public width: number = 40;  // Invader width
public height: number = 30; // Invader height
public type: number;        // Visual type (1-3)
public points: number;      // Score value (type * 10)
```

### Public Methods

#### update
```typescript
public update(deltaTime: number): void
```
Updates animation frame for visual effects.

**Animation:**
- 60-frame cycle between two animation states
- Affects visual appearance during rendering

#### render
```typescript
public render(ctx: CanvasRenderingContext2D): void
```
Renders invader based on type with animations.

**Type Colors:**
- Type 1: Red (#ff0000)
- Type 2: Yellow (#ffff00)
- Type 3: Magenta (#ff00ff)

**Visual Styles:**
- Type 1: Square with animated size and eyes
- Type 2: Diamond shape with inner pattern
- Type 3: Cross shape with variable arm length

### Private Methods

#### renderType1, renderType2, renderType3
```typescript
private renderType1(ctx: CanvasRenderingContext2D): void
private renderType2(ctx: CanvasRenderingContext2D): void
private renderType3(ctx: CanvasRenderingContext2D): void
```
Type-specific rendering methods with unique animations.

## Bullet Class

Represents projectiles fired by players and enemies.

### Constructor
```typescript
constructor(x: number, y: number, speed: number, type: BulletType = 'player')
```
Creates a bullet with specified properties.

**Parameters:**
- `x: number` - Initial X coordinate
- `y: number` - Initial Y coordinate
- `speed: number` - Movement speed per frame (negative = upward)
- `type: BulletType` - 'player' or 'enemy'

### Properties
```typescript
public x: number;           // Current X position
public y: number;           // Current Y position
public width: number = 4;   // Bullet width
public height: number = 12; // Bullet height
public speed: number;       // Movement speed
public type: BulletType;    // Bullet type
```

### Public Methods

#### update
```typescript
public update(deltaTime: number): void
```
Updates bullet position based on speed and time.

**Movement:**
- Y position changes by `speed * deltaTime`
- Negative speed moves upward (player bullets)
- Positive speed moves downward (enemy bullets)

#### render
```typescript
public render(ctx: CanvasRenderingContext2D): void
```
Renders bullet with type-specific visual effects.

**Player Bullets:**
- Green gradient (#00ff00)
- Bright green glow effect
- 10px shadow blur

**Enemy Bullets:**
- Red gradient (#ff0000)
- Red glow effect
- 8px shadow blur

## Usage Examples

### Basic Game Setup
```typescript
// Get canvas element
const canvas = document.getElementById('gameCanvas') as HTMLCanvasElement;

// Create game instance
const game = new Game(canvas);

// Start the game
game.startGame();
```

### Custom Player Movement
```typescript
// Create player
const player = new Player(400, 550);

// Handle input
if (keys['ArrowLeft']) {
  player.moveLeft();
}
if (keys['ArrowRight']) {
  player.moveRight(800);
}

// Shooting
if (keys['Space'] && player.canShoot()) {
  const bullet = player.shoot();
  if (bullet) {
    bullets.push(bullet);
  }
}
```

### Collision Detection
```typescript
// Check bullet vs invader collision
for (let bullet of playerBullets) {
  for (let invader of invaders) {
    if (game.isColliding(bullet, invader)) {
      // Remove both objects
      // Add score
      // Create explosion
    }
  }
}
```

### Creating Explosions
```typescript
// Create explosion at invader position
game.createExplosion(
  invader.x + invader.width / 2,
  invader.y + invader.height / 2
);
```

## Error Handling

### Canvas Context Errors
```typescript
try {
  const game = new Game(canvas);
} catch (error) {
  console.error('Failed to initialize game:', error.message);
  // Fallback to alternative rendering or error page
}
```

### Game Loop Errors
The game loop includes built-in error recovery:
```typescript
try {
  this.update(deltaTime);
  this.render();
} catch (error) {
  console.error('Game loop error:', error);
  // Game continues running
}
```

## Performance Considerations

### Frame Rate Optimization
- Delta time normalization for consistent 60fps
- Efficient collision detection with early exits
- Object pooling for bullets and particles

### Memory Management
- Automatic cleanup of off-screen bullets
- Particle lifecycle management
- Event listener cleanup

### Rendering Optimization
- Canvas state saving/restoring
- Minimal draw calls
- Efficient gradient creation

---

This API documentation provides complete reference for integrating with and extending the Fast Invader Game TypeScript implementation.