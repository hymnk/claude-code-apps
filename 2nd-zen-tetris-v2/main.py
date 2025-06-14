#!/usr/bin/env python3
"""
ZEN Tetris v2 - Main entry point.
A calming earth-tone Tetris game built with Pygame.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from zen_tetris.game import ZenTetrisGame


def main():
    """Main entry point for ZEN Tetris v2."""
    try:
        print("🎋 ZEN Tetris v2 starting...")
        print("Enjoy the calming earth-tone puzzle experience 🧘‍♀️")
        print("\n📋 Controls:")
        print("   Arrow Keys: Move and rotate")
        print("   Space: Hard drop")
        print("   P: Pause")
        print("   R: Restart")
        print("\n🎮 Game should start automatically with falling tetrominos...")
        
        game = ZenTetrisGame()
        game.run()
        
    except KeyboardInterrupt:
        print("\n🎋 Thanks for playing ZEN Tetris v2!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()