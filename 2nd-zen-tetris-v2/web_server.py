#!/usr/bin/env python3
"""
ZEN Tetris v2 Web Server
FastAPI server with WebSocket support for browser-based gameplay.
"""

import sys
import os
import json
import asyncio
import uuid
from typing import Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from zen_tetris.web_game import WebZenTetrisGame

app = FastAPI(title="ZEN Tetris v2", description="Browser-based zen tetris game")

# Templates and static files
templates = Jinja2Templates(directory="web_templates")
app.mount("/static", StaticFiles(directory="web_static"), name="static")

# Active game sessions
active_games: Dict[str, WebZenTetrisGame] = {}
active_connections: Dict[str, WebSocket] = {}


class ConnectionManager:
    """Manages WebSocket connections for game sessions."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept WebSocket connection and create game session."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        
        # Create new game instance
        active_games[session_id] = WebZenTetrisGame()
        print(f"🎋 New game session created: {session_id}")
    
    def disconnect(self, session_id: str):
        """Remove connection and clean up game session."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
        if session_id in active_games:
            del active_games[session_id]
        print(f"🎋 Game session ended: {session_id}")
    
    async def send_game_state(self, session_id: str, game_state: Dict[str, Any]):
        """Send game state to client."""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(game_state))
            except Exception as e:
                print(f"Error sending game state: {e}")
                self.disconnect(session_id)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get_game(request: Request):
    """Serve the main game page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "active_sessions": len(active_games),
        "version": "2.0.0"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for game communication."""
    session_id = str(uuid.uuid4())
    
    try:
        await manager.connect(websocket, session_id)
        game = active_games[session_id]
        
        # Send initial game state
        await manager.send_game_state(session_id, game.get_state())
        
        # Main game loop
        while True:
            try:
                # Handle incoming messages (user input)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.016)  # ~60 FPS
                message = json.loads(data)
                
                if message["type"] == "input":
                    game.handle_input(message["action"])
                elif message["type"] == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                    
            except asyncio.TimeoutError:
                # No input received, continue game loop
                pass
            except Exception as e:
                print(f"Input handling error: {e}")
                continue
            
            # Update game state
            game.update()
            
            # Send updated state to client
            await manager.send_game_state(session_id, game.get_state())
            
            # Control game speed (60 FPS)
            await asyncio.sleep(1/60)
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(session_id)


if __name__ == "__main__":
    print("🎋 Starting ZEN Tetris v2 Web Server...")
    print("🌐 Access the game at: http://localhost:8000")
    print("📊 Health check at: http://localhost:8000/health")
    print("\n🎮 Game Controls:")
    print("   Arrow Keys: Move and rotate")
    print("   Space: Hard drop")
    print("   P: Pause")
    print("   R: Restart")
    print("\n🧘‍♀️ Enjoy the zen experience!")
    
    uvicorn.run(
        "web_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )