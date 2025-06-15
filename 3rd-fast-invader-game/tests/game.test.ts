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

describe('Game', () => {
  let game: Game;

  beforeEach(() => {
    // Reset mocks
    jest.clearAllMocks();
    
    game = new Game(mockCanvas);
  });

  describe('constructor', () => {
    it('should initialize with correct canvas dimensions', () => {
      expect(game['width']).toBe(800);
      expect(game['height']).toBe(600);
    });

    it('should initialize in menu state', () => {
      expect(game['gameState']).toBe('menu');
    });

    it('should initialize with default values', () => {
      expect(game['score']).toBe(0);
      expect(game['lives']).toBe(3);
      expect(game['level']).toBe(1);
    });

    it('should throw error if canvas context is null', () => {
      const badCanvas = {
        width: 800,
        height: 600,
        getContext: jest.fn(() => null)
      } as any;

      expect(() => new Game(badCanvas)).toThrow('Could not get 2D context from canvas');
    });
  });

  describe('isColliding', () => {
    it('should detect collision when objects overlap', () => {
      const obj1 = { x: 10, y: 10, width: 20, height: 20 };
      const obj2 = { x: 15, y: 15, width: 20, height: 20 };
      
      expect(game.isColliding(obj1, obj2)).toBe(true);
    });

    it('should detect no collision when objects are separate', () => {
      const obj1 = { x: 10, y: 10, width: 20, height: 20 };
      const obj2 = { x: 50, y: 50, width: 20, height: 20 };
      
      expect(game.isColliding(obj1, obj2)).toBe(false);
    });

    it('should detect no collision when objects touch but do not overlap', () => {
      const obj1 = { x: 10, y: 10, width: 20, height: 20 };
      const obj2 = { x: 30, y: 10, width: 20, height: 20 };
      
      expect(game.isColliding(obj1, obj2)).toBe(false);
    });

    it('should handle edge case collisions correctly', () => {
      const obj1 = { x: 0, y: 0, width: 10, height: 10 };
      const obj2 = { x: 9, y: 9, width: 10, height: 10 };
      
      expect(game.isColliding(obj1, obj2)).toBe(true);
    });
  });

  describe('createInvaders', () => {
    beforeEach(() => {
      game['createInvaders']();
    });

    it('should create 50 invaders (5 rows × 10 columns)', () => {
      expect(game['invaders']).toHaveLength(50);
    });

    it('should create invaders with correct types based on row', () => {
      const invaders = game['invaders'];
      
      // First two rows should be type 1
      for (let i = 0; i < 20; i++) {
        expect(invaders[i].type).toBe(1);
      }
      
      // Next two rows should be type 2
      for (let i = 20; i < 40; i++) {
        expect(invaders[i].type).toBe(2);
      }
      
      // Last row should be type 3
      for (let i = 40; i < 50; i++) {
        expect(invaders[i].type).toBe(3);
      }
    });

    it('should position invaders in grid formation', () => {
      const invaders = game['invaders'];
      
      // Check first invader position
      expect(invaders[0].x).toBeGreaterThan(0);
      expect(invaders[0].y).toBe(80);
      
      // Check that invaders are spaced properly
      expect(invaders[1].x).toBeGreaterThan(invaders[0].x);
    });
  });

  describe('startGame', () => {
    it('should initialize player and invaders', () => {
      game.startGame();
      
      expect(game['player']).toBeInstanceOf(Player);
      expect(game['invaders']).toHaveLength(50);
      expect(game['gameState']).toBe('playing');
    });
  });

  describe('nextLevel', () => {
    beforeEach(() => {
      game['level'] = 1;
      game['invaderSpeed'] = 1;
      game['invaderShootInterval'] = 120;
    });

    it('should increment level', () => {
      game['nextLevel']();
      expect(game['level']).toBe(2);
    });

    it('should increase invader speed', () => {
      const initialSpeed = game['invaderSpeed'];
      game['nextLevel']();
      expect(game['invaderSpeed']).toBe(initialSpeed + 0.5);
    });

    it('should decrease shoot interval but not below minimum', () => {
      game['nextLevel']();
      expect(game['invaderShootInterval']).toBe(110);
      
      // Test minimum threshold
      game['invaderShootInterval'] = 65;
      game['nextLevel']();
      expect(game['invaderShootInterval']).toBe(60); // Should not go below 60
    });

    it('should create new invaders', () => {
      game['invaders'] = []; // Clear invaders
      game['nextLevel']();
      expect(game['invaders']).toHaveLength(50);
    });
  });

  describe('createExplosion', () => {
    it('should create 8 particles', () => {
      game['createExplosion'](100, 100);
      expect(game['particles']).toHaveLength(8);
    });

    it('should create particles with correct properties', () => {
      game['createExplosion'](100, 100);
      const particles = game['particles'];
      
      particles.forEach(particle => {
        expect(particle.x).toBe(100);
        expect(particle.y).toBe(100);
        expect(particle.life).toBe(30);
        expect(particle.maxLife).toBe(30);
        expect(particle.color).toMatch(/^hsl\(\d+\.?\d*, 100%, 50%\)$/);
        expect(typeof particle.vx).toBe('number');
        expect(typeof particle.vy).toBe('number');
      });
    });
  });

  describe('updateBullets', () => {
    beforeEach(() => {
      game['playerBullets'] = [
        new Bullet(100, 50, -5, 'player'),
        new Bullet(200, -10, -5, 'player'), // Should be filtered out
        new Bullet(300, 100, -5, 'player')
      ];
      
      game['invaderBullets'] = [
        new Bullet(100, 500, 5, 'enemy'),
        new Bullet(200, 650, 5, 'enemy'), // Should be filtered out
        new Bullet(300, 400, 5, 'enemy')
      ];
    });

    it('should update all bullets', () => {
      const initialPlayerY = game['playerBullets'][0].y;
      const initialEnemyY = game['invaderBullets'][0].y;
      
      game['updateBullets'](1);
      
      expect(game['playerBullets'][0].y).not.toBe(initialPlayerY);
      expect(game['invaderBullets'][0].y).not.toBe(initialEnemyY);
    });

    it('should filter out bullets that are off-screen', () => {
      game['updateBullets'](1);
      
      // Player bullets with y <= 0 should be removed
      expect(game['playerBullets']).toHaveLength(2);
      
      // Enemy bullets with y >= canvas height should be removed
      expect(game['invaderBullets']).toHaveLength(2);
    });
  });

  describe('updateParticles', () => {
    beforeEach(() => {
      game['particles'] = [
        { x: 100, y: 100, vx: 1, vy: 1, life: 10, maxLife: 30, color: 'red' },
        { x: 200, y: 200, vx: -1, vy: -1, life: 0, maxLife: 30, color: 'blue' }, // Should be filtered out
        { x: 300, y: 300, vx: 2, vy: -2, life: 5, maxLife: 30, color: 'green' }
      ];
    });

    it('should update particle positions based on velocity', () => {
      const deltaTime = 2;
      const initialParticle = { ...game['particles'][0] };
      
      game['updateParticles'](deltaTime);
      
      expect(game['particles'][0].x).toBe(initialParticle.x + initialParticle.vx * deltaTime);
      expect(game['particles'][0].y).toBe(initialParticle.y + initialParticle.vy * deltaTime);
    });

    it('should decrease particle life', () => {
      const deltaTime = 1;
      const initialLife = game['particles'][0].life;
      
      game['updateParticles'](deltaTime);
      
      expect(game['particles'][0].life).toBe(initialLife - deltaTime);
    });

    it('should filter out particles with no life remaining', () => {
      game['updateParticles'](1);
      
      expect(game['particles']).toHaveLength(2);
      expect(game['particles'].every(p => p.life > 0)).toBe(true);
    });
  });

  describe('checkGameState', () => {
    it('should call nextLevel when no invaders remain', () => {
      const nextLevelSpy = jest.spyOn(game as any, 'nextLevel');
      game['invaders'] = [];
      
      game['checkGameState']();
      
      expect(nextLevelSpy).toHaveBeenCalled();
    });

    it('should not call nextLevel when invaders remain', () => {
      const nextLevelSpy = jest.spyOn(game as any, 'nextLevel');
      game['invaders'] = [new Invader(0, 0, 1)];
      
      game['checkGameState']();
      
      expect(nextLevelSpy).not.toHaveBeenCalled();
    });
  });

  describe('render', () => {
    it('should render without throwing errors', () => {
      expect(() => game.render()).not.toThrow();
    });

    it('should clear canvas before rendering', () => {
      const clearSpy = jest.spyOn(game as any, 'clear');
      game.render();
      expect(clearSpy).toHaveBeenCalled();
    });
  });
});