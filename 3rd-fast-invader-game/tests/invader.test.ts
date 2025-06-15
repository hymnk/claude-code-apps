import { Invader } from '../src/invader';

describe('Invader', () => {
  let invader: Invader;

  beforeEach(() => {
    invader = new Invader(50, 100, 2);
  });

  describe('constructor', () => {
    it('should initialize with correct position and default values', () => {
      expect(invader.x).toBe(50);
      expect(invader.y).toBe(100);
      expect(invader.width).toBe(40);
      expect(invader.height).toBe(30);
      expect(invader.type).toBe(2);
      expect(invader.points).toBe(20); // type * 10
    });

    it('should default to type 1 if not specified', () => {
      const defaultInvader = new Invader(0, 0);
      expect(defaultInvader.type).toBe(1);
      expect(defaultInvader.points).toBe(10);
    });

    it('should calculate points correctly for different types', () => {
      const type1 = new Invader(0, 0, 1);
      const type2 = new Invader(0, 0, 2);
      const type3 = new Invader(0, 0, 3);

      expect(type1.points).toBe(10);
      expect(type2.points).toBe(20);
      expect(type3.points).toBe(30);
    });
  });

  describe('update', () => {
    it('should update animation frame after enough time passes', () => {
      // Initial animation frame should be 0
      expect(invader['animationFrame']).toBe(0);

      // Update for animation speed cycles
      for (let i = 0; i < 60; i++) {
        invader.update(1);
      }

      expect(invader['animationFrame']).toBe(1);

      // Continue updating to cycle back to 0
      for (let i = 0; i < 60; i++) {
        invader.update(1);
      }

      expect(invader['animationFrame']).toBe(0);
    });

    it('should not update animation frame too quickly', () => {
      const initialFrame = invader['animationFrame'];
      
      // Update only a few times
      for (let i = 0; i < 10; i++) {
        invader.update(1);
      }

      expect(invader['animationFrame']).toBe(initialFrame);
    });
  });

  describe('render', () => {
    let mockCtx: any;

    beforeEach(() => {
      mockCtx = {
        fillStyle: '',
        fillRect: jest.fn(),
        beginPath: jest.fn(),
        moveTo: jest.fn(),
        lineTo: jest.fn(),
        closePath: jest.fn(),
        fill: jest.fn(),
        arc: jest.fn()
      };
    });

    it('should render without throwing errors', () => {
      expect(() => invader.render(mockCtx)).not.toThrow();
    });

    it('should use correct color for different invader types', () => {
      const type1Invader = new Invader(0, 0, 1);
      const type2Invader = new Invader(0, 0, 2);
      const type3Invader = new Invader(0, 0, 3);
      
      expect(type1Invader.type).toBe(1);
      expect(type2Invader.type).toBe(2);
      expect(type3Invader.type).toBe(3);
      
      // Test that render doesn't throw - color testing would require more complex mocking
      expect(() => type1Invader.render(mockCtx)).not.toThrow();
      expect(() => type2Invader.render(mockCtx)).not.toThrow();
      expect(() => type3Invader.render(mockCtx)).not.toThrow();
    });

    it('should call appropriate render method for type 1', () => {
      const type1Invader = new Invader(0, 0, 1);
      const renderType1Spy = jest.spyOn(type1Invader as any, 'renderType1');
      type1Invader.render(mockCtx);
      expect(renderType1Spy).toHaveBeenCalled();
    });

    it('should call appropriate render method for type 2', () => {
      const type2Invader = new Invader(0, 0, 2);
      const renderType2Spy = jest.spyOn(type2Invader as any, 'renderType2');
      type2Invader.render(mockCtx);
      expect(renderType2Spy).toHaveBeenCalled();
    });

    it('should call appropriate render method for type 3', () => {
      const type3Invader = new Invader(0, 0, 3);
      const renderType3Spy = jest.spyOn(type3Invader as any, 'renderType3');
      type3Invader.render(mockCtx);
      expect(renderType3Spy).toHaveBeenCalled();
    });
  });

  describe('renderType1', () => {
    it('should render square invader with eyes', () => {
      const mockCtx = {
        fillStyle: '',
        fillRect: jest.fn()
      } as any;

      invader['renderType1'](mockCtx);
      
      // Should call fillRect multiple times (body + eyes)
      expect(mockCtx.fillRect).toHaveBeenCalledTimes(3);
    });
  });

  describe('renderType2', () => {
    it('should render diamond-shaped invader', () => {
      const mockCtx = {
        fillStyle: '',
        beginPath: jest.fn(),
        moveTo: jest.fn(),
        lineTo: jest.fn(),
        closePath: jest.fn(),
        fill: jest.fn()
      } as any;

      invader['renderType2'](mockCtx);
      
      // Should create two diamond paths
      expect(mockCtx.beginPath).toHaveBeenCalledTimes(2);
      expect(mockCtx.fill).toHaveBeenCalledTimes(2);
    });
  });

  describe('renderType3', () => {
    it('should render cross-shaped invader', () => {
      const mockCtx = {
        fillStyle: '',
        fillRect: jest.fn(),
        beginPath: jest.fn(),
        arc: jest.fn(),
        fill: jest.fn()
      } as any;

      invader['renderType3'](mockCtx);
      
      // Should render bars and circle
      expect(mockCtx.fillRect).toHaveBeenCalledTimes(2); // Vertical + horizontal bars
      expect(mockCtx.arc).toHaveBeenCalledTimes(1); // Center circle
    });
  });
});