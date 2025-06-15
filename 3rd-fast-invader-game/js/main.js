document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    const game = new Game(canvas);
    
    // Initialize the game in menu state
    game.render();
    
    // Prevent space bar from scrolling the page
    window.addEventListener('keydown', (e) => {
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