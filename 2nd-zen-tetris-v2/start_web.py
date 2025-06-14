#!/usr/bin/env python3
"""
ZEN Tetris v2 - Web Version Launcher
Quick start script for the browser version.
"""

import sys
import os
import webbrowser
import time
import threading

def main():
    """Launch the web version of ZEN Tetris v2."""
    print("🎋 ZEN Tetris v2 - Web Version Launcher")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists("web_server.py"):
        print("❌ Error: Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check if uvicorn is available
    try:
        import uvicorn
    except ImportError:
        print("❌ Error: uvicorn not installed.")
        print("Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    print("✅ Starting ZEN Tetris v2 Web Server...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📊 Health check at: http://localhost:8000/health")
    print()
    print("🎮 Game Controls:")
    print("   Arrow Keys: Move and rotate pieces")
    print("   Space: Hard drop")
    print("   P: Pause/Resume")
    print("   R: Restart game")
    print()
    print("🧘‍♀️ Enjoy the zen tetris experience!")
    print("="*50)
    print()
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)  # Wait for server to start
        print("🔗 Opening browser...")
        webbrowser.open("http://localhost:8000")
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the web server
    try:
        import uvicorn
        uvicorn.run(
            "web_server:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🎋 Shutting down ZEN Tetris v2 Web Server...")
        print("Thanks for playing! 🧘‍♀️")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()