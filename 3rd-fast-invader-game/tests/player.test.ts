import { Player } from '../src/player';
import { Bullet } from '../src/bullet';

describe('Player', () => {
  let player: Player;

  beforeEach(() => {
    player = new Player(100, 200);
  });

  describe('constructor', () => {
    it('should initialize with correct position and default values', () => {
      expect(player.x).toBe(100);
      expect(player.y).toBe(200);
      expect(player.width).toBe(40);
      expect(player.height).toBe(30);
      expect(player.speed).toBe(5);
    });
  });

  describe('moveLeft', () => {
    it('should move player left by speed amount', () => {
      const initialX = player.x;
      player.moveLeft();
      expect(player.x).toBe(initialX - player.speed);
    });

    it('should not move beyond left boundary (x = 0)', () => {
      player.x = 0;
      player.moveLeft();
      expect(player.x).toBe(0);
    });

    it('should not move if already at left boundary', () => {
      player.x = -5;
      player.moveLeft();
      expect(player.x).toBe(-5);
    });
  });

  describe('moveRight', () => {
    it('should move player right by speed amount', () => {
      const canvasWidth = 800;
      const initialX = player.x;
      player.moveRight(canvasWidth);
      expect(player.x).toBe(initialX + player.speed);
    });

    it('should not move beyond right boundary', () => {
      const canvasWidth = 800;
      player.x = canvasWidth - player.width;
      player.moveRight(canvasWidth);
      expect(player.x).toBe(canvasWidth - player.width);
    });

    it('should not move if already at right boundary', () => {
      const canvasWidth = 800;
      player.x = canvasWidth - player.width + 10;
      player.moveRight(canvasWidth);
      expect(player.x).toBe(canvasWidth - player.width + 10);
    });
  });

  describe('canShoot', () => {
    it('should return true initially', () => {
      expect(player.canShoot()).toBe(true);
    });

    it('should return false immediately after shooting', () => {
      player.shoot();
      expect(player.canShoot()).toBe(false);
    });

    it('should return true after cooldown period', () => {
      player.shoot();
      
      // Mock time passing
      const originalNow = Date.now;
      Date.now = jest.fn(() => originalNow() + 300); // 300ms later
      
      expect(player.canShoot()).toBe(true);
      
      // Restore original Date.now
      Date.now = originalNow;
    });
  });

  describe('shoot', () => {
    it('should return a bullet when able to shoot', () => {
      const bullet = player.shoot();
      expect(bullet).toBeInstanceOf(Bullet);
      expect(bullet?.x).toBe(player.x + player.width / 2);
      expect(bullet?.y).toBe(player.y);
      expect(bullet?.type).toBe('player');
    });

    it('should return null when on cooldown', () => {
      player.shoot(); // First shot
      const secondShot = player.shoot(); // Should be null due to cooldown
      expect(secondShot).toBeNull();
    });

    it('should create bullet with correct speed and direction', () => {
      const bullet = player.shoot();
      expect(bullet?.speed).toBe(-7); // Negative for upward movement
    });
  });

  describe('update', () => {
    it('should exist and not throw errors', () => {
      expect(() => player.update(1)).not.toThrow();
    });
  });

  describe('render', () => {
    it('should render without throwing errors', () => {
      const mockCtx = {
        fillStyle: '',
        fillRect: jest.fn(),
        beginPath: jest.fn(),
        moveTo: jest.fn(),
        lineTo: jest.fn(),
        closePath: jest.fn(),
        fill: jest.fn(),
        createLinearGradient: jest.fn(() => ({
          addColorStop: jest.fn()
        }))
      } as any;

      expect(() => player.render(mockCtx)).not.toThrow();
      expect(mockCtx.fillRect).toHaveBeenCalled();
    });
  });
});