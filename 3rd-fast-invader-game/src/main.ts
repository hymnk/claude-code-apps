import { Game } from './game.js';

document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('gameCanvas') as HTMLCanvasElement;
  if (!canvas) {
    throw new Error('Could not find canvas element with id "gameCanvas"');
  }
  
  const game = new Game(canvas);
  
  // Initialize the game in menu state
  game.render();
  
  // Prevent space bar from scrolling the page
  window.addEventListener('keydown', (e: KeyboardEvent) => {
    if (e.code === 'Space') {
      e.preventDefault();
    }
  });
  
  // Handle window resize
  window.addEventListener('resize', () => {
    // Optional: Handle canvas resize here if needed
  });
  
  console.log('Fast Invader Game loaded successfully!');
});