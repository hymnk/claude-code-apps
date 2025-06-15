// Mock Canvas API for testing
class MockCanvasRenderingContext2D {
  fillStyle: string = '#000';
  font: string = '';
  textAlign: string = '';
  shadowColor: string = '';
  shadowBlur: number = 0;
  globalAlpha: number = 1;

  fillRect() {}
  beginPath() {}
  moveTo() {}
  lineTo() {}
  closePath() {}
  fill() {}
  createLinearGradient() {
    return {
      addColorStop: () => {}
    };
  }
  fillText() {}
  arc() {}
  save() {}
  restore() {}
}

class MockHTMLCanvasElement {
  width: number = 800;
  height: number = 600;
  
  getContext(contextId: string): MockCanvasRenderingContext2D | null {
    if (contextId === '2d') {
      return new MockCanvasRenderingContext2D();
    }
    return null;
  }
}

// Mock DOM elements
Object.defineProperty(global, 'HTMLCanvasElement', {
  value: MockHTMLCanvasElement,
  configurable: true
});

// Mock requestAnimationFrame
global.requestAnimationFrame = jest.fn((callback) => {
  setTimeout(callback, 16);
  return 1;
});

// Mock Date.now for consistent testing
const mockNow = 1000000;
jest.spyOn(Date, 'now').mockReturnValue(mockNow);

// Mock document.getElementById
const mockGetElementById = jest.fn((id: string) => ({
  textContent: '',
  classList: {
    add: jest.fn(),
    remove: jest.fn()
  },
  addEventListener: jest.fn()
}));

global.document = {
  getElementById: mockGetElementById,
  addEventListener: jest.fn()
} as any;

// Mock console to avoid noise in tests
global.console = {
  ...console,
  log: jest.fn(),
  error: jest.fn()
};