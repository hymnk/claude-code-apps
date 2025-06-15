import { Game } from '../src/game';
import { Player } from '../src/player';
import { Invader } from '../src/invader';
import { Bullet } from '../src/bullet';

// Mock DOM elements
const mockElement = {
  textContent: '',
  classList: {
    add: jest.fn(),
    remove: jest.fn()
  },
  addEventListener: jest.fn()
};

const mockCanvas = {
  width: 800,
  height: 600,
  getContext: jest.fn(() => ({
    fillStyle: '',
    font: '',
    textAlign: '',
    shadowColor: '',
    shadowBlur: 0,
    globalAlpha: 1,
    fillRect: jest.fn(),
    beginPath: jest.fn(),
    moveTo: jest.fn(),
    lineTo: jest.fn(),
    closePath: jest.fn(),
    fill: jest.fn(),
    createLinearGradient: jest.fn(() => ({
      addColorStop: jest.fn()
    })),
    fillText: jest.fn(),
    arc: jest.fn(),
    save: jest.fn(),
    restore: jest.fn()
  }))
} as any;

describe('Integration Tests - Game Mechanics', () => {
  let game: Game;

  beforeEach(() => {
    jest.clearAllMocks();
    game = new Game(mockCanvas);
  });

  describe('Complete Game Flow', () => {
    it('should start game and initialize all components', () => {
      game.startGame();

      expect(game['gameState']).toBe('playing');
      expect(game['player']).toBeInstanceOf(Player);
      expect(game['invaders']).toHaveLength(50);
      expect(game['score']).toBe(0);
      expect(game['lives']).toBe(3);
      expect(game['level']).toBe(1);
    });

    it('should handle player shooting and bullet creation', () => {
      game.startGame();
      
      // Simulate player shooting
      game['handleShoot']();
      
      expect(game['playerBullets']).toHaveLength(1);
      expect(game['playerBullets'][0]).toBeInstanceOf(Bullet);
      expect(game['playerBullets'][0].type).toBe('player');
    });

    it('should prevent rapid firing due to cooldown', () => {
      game.startGame();
      
      // First shot should work
      game['handleShoot']();
      expect(game['playerBullets']).toHaveLength(1);
      
      // Second shot immediately should not create another bullet
      game['handleShoot']();
      expect(game['playerBullets']).toHaveLength(1);
    });
  });

  describe('Collision Detection Integration', () => {
    beforeEach(() => {
      game.startGame();
    });

    it('should detect player bullet hitting invader', () => {
      // Place a bullet at an invader's position
      const invader = game['invaders'][0];
      const bullet = new Bullet(
        invader.x + invader.width / 2,
        invader.y + invader.height / 2,
        -5,
        'player'
      );
      game['playerBullets'] = [bullet];
      
      const initialScore = game['score'];
      const initialInvaderCount = game['invaders'].length;
      
      game['checkCollisions']();
      
      expect(game['score']).toBeGreaterThan(initialScore);
      expect(game['invaders']).toHaveLength(initialInvaderCount - 1);
      expect(game['playerBullets']).toHaveLength(0); // Bullet should be removed
      expect(game['particles'].length).toBeGreaterThan(0); // Explosion particles
    });

    it('should detect enemy bullet hitting player', () => {
      // Place an enemy bullet at player's position
      const player = game['player']!;
      const bullet = new Bullet(
        player.x + player.width / 2,
        player.y + player.height / 2,
        5,
        'enemy'
      );
      game['invaderBullets'] = [bullet];
      
      const initialLives = game['lives'];
      
      game['checkCollisions']();
      
      expect(game['lives']).toBe(initialLives - 1);
      expect(game['invaderBullets']).toHaveLength(0); // Bullet should be removed
      expect(game['particles'].length).toBeGreaterThan(0); // Explosion particles
    });

    it('should trigger game over when player loses all lives', () => {
      const player = game['player']!;
      game['lives'] = 1; // Set to 1 life remaining
      
      const bullet = new Bullet(
        player.x + player.width / 2,
        player.y + player.height / 2,
        5,
        'enemy'
      );
      game['invaderBullets'] = [bullet];
      
      const gameOverSpy = jest.spyOn(game as any, 'gameOver');
      
      game['checkCollisions']();
      
      expect(game['lives']).toBe(0);
      expect(gameOverSpy).toHaveBeenCalled();
    });

    it('should trigger game over when invaders reach bottom', () => {
      // Move an invader to the bottom
      const invader = game['invaders'][0];
      invader.y = game['height'] - 50; // Near bottom
      
      const gameOverSpy = jest.spyOn(game as any, 'gameOver');
      
      game['checkCollisions']();
      
      expect(gameOverSpy).toHaveBeenCalled();
    });
  });

  describe('Level Progression', () => {
    beforeEach(() => {
      game.startGame();
    });

    it('should advance to next level when all invaders destroyed', () => {
      const initialLevel = game['level'];
      const initialSpeed = game['invaderSpeed'];
      
      // Remove all invaders
      game['invaders'] = [];
      
      game['checkGameState']();
      
      expect(game['level']).toBe(initialLevel + 1);
      expect(game['invaderSpeed']).toBeGreaterThan(initialSpeed);
      expect(game['invaders']).toHaveLength(50); // New invaders created
    });

    it('should increase difficulty with each level', () => {
      game['level'] = 1;
      game['invaderSpeed'] = 1;
      game['invaderShootInterval'] = 120;
      
      game['nextLevel']();
      
      expect(game['level']).toBe(2);
      expect(game['invaderSpeed']).toBe(1.5);
      expect(game['invaderShootInterval']).toBe(110);
    });
  });

  describe('Player Movement and Boundaries', () => {
    beforeEach(() => {
      game.startGame();
    });

    it('should handle player movement within boundaries', () => {
      const player = game['player']!;
      const canvasWidth = game['width'];
      
      // Test left movement
      player.x = 100;
      game['keys'] = { 'ArrowLeft': true };
      game['updatePlayer'](1);
      expect(player.x).toBe(95); // 100 - 5 (speed)
      
      // Test right movement
      game['keys'] = { 'ArrowRight': true };
      game['updatePlayer'](1);
      expect(player.x).toBe(100); // 95 + 5 (speed)
      
      // Test boundary prevention
      player.x = 0;
      game['keys'] = { 'ArrowLeft': true };
      game['updatePlayer'](1);
      expect(player.x).toBe(0); // Should not move past left boundary
      
      player.x = canvasWidth - player.width;
      game['keys'] = { 'ArrowRight': true };
      game['updatePlayer'](1);
      expect(player.x).toBe(canvasWidth - player.width); // Should not move past right boundary
    });
  });

  describe('Invader Movement Patterns', () => {
    beforeEach(() => {
      game.startGame();
    });

    it('should move invaders horizontally and drop down at edges', () => {
      const invader = game['invaders'][0];
      const initialY = invader.y;
      
      // Move invader to left edge
      invader.x = -5;
      
      game['updateInvaders'](1);
      
      // Should have moved down and changed direction
      expect(invader.y).toBe(initialY + 20);
      expect(game['invaderDirection']).toBe(-1); // Direction should reverse
    });

    it('should generate invader shots randomly', () => {
      const initialBulletCount = game['invaderBullets'].length;
      
      // Force invader shooting by setting timer to threshold
      game['invaderShootTimer'] = game['invaderShootInterval'];
      
      game['updateInvaders'](1);
      
      expect(game['invaderBullets'].length).toBeGreaterThan(initialBulletCount);
    });
  });

  describe('Particle System Integration', () => {
    beforeEach(() => {
      game.startGame();
    });

    it('should create and update explosion particles', () => {
      game['createExplosion'](100, 100);
      
      expect(game['particles']).toHaveLength(8);
      
      const initialParticle = { ...game['particles'][0] };
      
      game['updateParticles'](1);
      
      // Particles should have lost life
      expect(game['particles'][0].life).toBeLessThan(initialParticle.life);
      // Position might change depending on velocity (which could be 0)
      expect(game['particles'].length).toBe(8);
    });

    it('should remove expired particles', () => {
      game['particles'] = [
        { x: 0, y: 0, vx: 0, vy: 0, life: 0, maxLife: 30, color: 'red' },
        { x: 0, y: 0, vx: 0, vy: 0, life: 10, maxLife: 30, color: 'blue' }
      ];
      
      game['updateParticles'](1);
      
      expect(game['particles']).toHaveLength(1);
      expect(game['particles'][0].color).toBe('blue');
    });
  });

  describe('Game State Management', () => {
    it('should handle pause and resume correctly', () => {
      game.startGame();
      expect(game['gameState']).toBe('playing');
      
      game['togglePause']();
      expect(game['gameState']).toBe('paused');
      
      game['togglePause']();
      expect(game['gameState']).toBe('playing');
    });

    it('should reset game state correctly', () => {
      game.startGame();
      game['score'] = 1000;
      game['lives'] = 1;
      game['level'] = 3;
      game['playerBullets'] = [new Bullet(0, 0, 0)];
      
      game['resetGame']();
      
      expect(game['score']).toBe(0);
      expect(game['lives']).toBe(3);
      expect(game['level']).toBe(1);
      expect(game['gameState']).toBe('menu');
      expect(game['playerBullets']).toHaveLength(0);
    });
  });

  describe('Score System Integration', () => {
    beforeEach(() => {
      game.startGame();
    });

    it('should award correct points for different invader types', () => {
      const type1Invader = new Invader(0, 0, 1);
      const type2Invader = new Invader(0, 0, 2);
      const type3Invader = new Invader(0, 0, 3);
      
      expect(type1Invader.points).toBe(10);
      expect(type2Invader.points).toBe(20);
      expect(type3Invader.points).toBe(30);
    });

    it('should update score when invaders are destroyed', () => {
      const invader = game['invaders'][0];
      const bullet = new Bullet(
        invader.x + invader.width / 2,
        invader.y + invader.height / 2,
        -5,
        'player'
      );
      game['playerBullets'] = [bullet];
      
      const initialScore = game['score'];
      
      game['checkCollisions']();
      
      expect(game['score']).toBe(initialScore + invader.points);
    });
  });
});