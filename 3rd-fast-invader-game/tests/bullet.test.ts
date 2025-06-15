import { Bullet } from '../src/bullet';

describe('Bullet', () => {
  let bullet: Bullet;

  beforeEach(() => {
    bullet = new Bullet(100, 200, -5, 'player');
  });

  describe('constructor', () => {
    it('should initialize with correct position and values', () => {
      expect(bullet.x).toBe(100);
      expect(bullet.y).toBe(200);
      expect(bullet.width).toBe(4);
      expect(bullet.height).toBe(12);
      expect(bullet.speed).toBe(-5);
      expect(bullet.type).toBe('player');
    });

    it('should default to player type if not specified', () => {
      const defaultBullet = new Bullet(0, 0, 5);
      expect(defaultBullet.type).toBe('player');
    });

    it('should handle enemy type correctly', () => {
      const enemyBullet = new Bullet(0, 0, 5, 'enemy');
      expect(enemyBullet.type).toBe('enemy');
    });
  });

  describe('update', () => {
    it('should move bullet by speed * deltaTime', () => {
      const initialY = bullet.y;
      const deltaTime = 2;
      const expectedNewY = initialY + (bullet.speed * deltaTime);

      bullet.update(deltaTime);
      expect(bullet.y).toBe(expectedNewY);
    });

    it('should move upward for negative speed (player bullets)', () => {
      const playerBullet = new Bullet(100, 200, -7, 'player');
      const initialY = playerBullet.y;
      
      playerBullet.update(1);
      expect(playerBullet.y).toBeLessThan(initialY);
    });

    it('should move downward for positive speed (enemy bullets)', () => {
      const enemyBullet = new Bullet(100, 200, 5, 'enemy');
      const initialY = enemyBullet.y;
      
      enemyBullet.update(1);
      expect(enemyBullet.y).toBeGreaterThan(initialY);
    });

    it('should handle fractional deltaTime correctly', () => {
      const initialY = bullet.y;
      const deltaTime = 0.5;
      const expectedNewY = initialY + (bullet.speed * deltaTime);

      bullet.update(deltaTime);
      expect(bullet.y).toBe(expectedNewY);
    });
  });

  describe('render', () => {
    let mockCtx: any;

    beforeEach(() => {
      mockCtx = {
        fillStyle: '',
        shadowColor: '',
        shadowBlur: 0,
        fillRect: jest.fn(),
        createLinearGradient: jest.fn(() => ({
          addColorStop: jest.fn()
        }))
      };
    });

    it('should render without throwing errors', () => {
      expect(() => bullet.render(mockCtx)).not.toThrow();
    });

    it('should create gradient for player bullets', () => {
      const playerBullet = new Bullet(100, 100, -5, 'player');
      playerBullet.render(mockCtx);
      
      expect(mockCtx.createLinearGradient).toHaveBeenCalled();
      expect(mockCtx.fillRect).toHaveBeenCalled();
    });

    it('should create gradient for enemy bullets', () => {
      const enemyBullet = new Bullet(100, 100, 5, 'enemy');
      enemyBullet.render(mockCtx);
      
      expect(mockCtx.createLinearGradient).toHaveBeenCalled();
      expect(mockCtx.fillRect).toHaveBeenCalled();
    });

    it('should set green glow for player bullets', () => {
      const playerBullet = new Bullet(100, 100, -5, 'player');
      playerBullet.render(mockCtx);
      
      expect(mockCtx.shadowColor).toBe('#00ff00');
      // Note: shadowBlur will be reset to 0 at the end of render method
    });

    it('should set red glow for enemy bullets', () => {
      const enemyBullet = new Bullet(100, 100, 5, 'enemy');
      enemyBullet.render(mockCtx);
      
      expect(mockCtx.shadowColor).toBe('#ff0000');
      // Note: shadowBlur will be reset to 0 at the end of render method
    });

    it('should render bullet at correct position', () => {
      bullet.render(mockCtx);
      
      // Should render main bullet body
      expect(mockCtx.fillRect).toHaveBeenCalledWith(
        bullet.x - bullet.width / 2, 
        bullet.y, 
        bullet.width, 
        bullet.height
      );
      
      // Should render glow effect
      expect(mockCtx.fillRect).toHaveBeenCalledWith(
        bullet.x - 1, 
        bullet.y, 
        2, 
        bullet.height
      );
    });

    it('should reset shadow blur after rendering', () => {
      bullet.render(mockCtx);
      expect(mockCtx.shadowBlur).toBe(0);
    });
  });

  describe('properties', () => {
    it('should have public access to position properties', () => {
      expect(typeof bullet.x).toBe('number');
      expect(typeof bullet.y).toBe('number');
      expect(typeof bullet.width).toBe('number');
      expect(typeof bullet.height).toBe('number');
    });

    it('should allow position modification', () => {
      bullet.x = 150;
      bullet.y = 250;
      
      expect(bullet.x).toBe(150);
      expect(bullet.y).toBe(250);
    });
  });
});