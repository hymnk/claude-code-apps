#!/usr/bin/env python3
"""
Flask + Socket.IO AIM Trainer
リアルタイムなブラウザベースAIMトレーニングゲーム
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random
import time
import math
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aim_trainer_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# ゲーム設定
GAME_TIME = 30  # 秒
CANVAS_WIDTH = 700
CANVAS_HEIGHT = 500
TARGET_RADIUS = 30
TARGET_CENTER_RADIUS = 8
TARGET_INNER_RADIUS = 15
TARGET_OUTER_RADIUS = 30

# ゲーム状態を管理する辞書
game_sessions = {}

def generate_target_position():
    """新しいターゲット位置を生成"""
    margin = TARGET_OUTER_RADIUS + 10
    x = random.randint(margin, CANVAS_WIDTH - margin)
    y = random.randint(margin, CANVAS_HEIGHT - margin)
    return x, y

def calculate_distance(x1, y1, x2, y2):
    """2点間の距離を計算"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_hit_score(target_x, target_y, click_x, click_y):
    """クリック位置から得点を計算（グラデーション得点システム）"""
    distance = calculate_distance(target_x, target_y, click_x, click_y)
    
    if distance <= TARGET_CENTER_RADIUS:  # 白い中心エリア（8px以内）
        return 100  # 中心は満点
    elif distance <= TARGET_INNER_RADIUS:  # 内側リング（15px以内）
        # 100点から70点までグラデーション
        ratio = (distance - TARGET_CENTER_RADIUS) / (TARGET_INNER_RADIUS - TARGET_CENTER_RADIUS)
        return int(100 - (ratio * 30))  # 100 -> 70
    elif distance <= TARGET_OUTER_RADIUS:  # 外側リング（30px以内）
        # 70点から20点までグラデーション
        ratio = (distance - TARGET_INNER_RADIUS) / (TARGET_OUTER_RADIUS - TARGET_INNER_RADIUS)
        return int(70 - (ratio * 50))  # 70 -> 20
    else:
        return 0  # Miss

def is_target_hit(target_x, target_y, click_x, click_y):
    """ターゲットがヒットしたかチェック"""
    distance = calculate_distance(target_x, target_y, click_x, click_y)
    return distance <= TARGET_OUTER_RADIUS

@app.route('/')
def index():
    """メインページ"""
    return render_template('aim_trainer.html')

@socketio.on('connect')
def handle_connect():
    """クライアント接続時"""
    print(f'Client connected: {request.sid}')
    emit('connected', {'message': 'Connected to AIM Trainer server'})

@socketio.on('disconnect')
def handle_disconnect():
    """クライアント切断時"""
    print(f'Client disconnected: {request.sid}')
    if request.sid in game_sessions:
        del game_sessions[request.sid]

@socketio.on('start_game')
def handle_start_game():
    """ゲーム開始"""
    session_id = request.sid
    target_x, target_y = generate_target_position()
    
    game_sessions[session_id] = {
        'start_time': time.time(),
        'score': 0,
        'hits': 0,
        'total_clicks': 0,
        'hit_scores': [],
        'target_x': target_x,
        'target_y': target_y,
        'game_active': True
    }
    
    emit('game_started', {
        'target_x': target_x,
        'target_y': target_y,
        'game_time': GAME_TIME
    })
    
    print(f'Game started for {session_id}')

@socketio.on('target_click')
def handle_target_click(data):
    """ターゲットクリック処理"""
    session_id = request.sid
    if session_id not in game_sessions:
        return
    
    session = game_sessions[session_id]
    if not session['game_active']:
        return
    
    # ゲーム時間チェック（より正確な判定）
    elapsed_time = time.time() - session['start_time']
    if elapsed_time > GAME_TIME:
        handle_game_end(session_id)
        return
    
    click_x = data['click_x']
    click_y = data['click_y']
    target_x = session['target_x']
    target_y = session['target_y']
    
    session['total_clicks'] += 1
    
    # ヒット判定
    if is_target_hit(target_x, target_y, click_x, click_y):
        # ヒット！
        session['hits'] += 1
        hit_score = get_hit_score(target_x, target_y, click_x, click_y)
        session['score'] += hit_score
        session['hit_scores'].append(hit_score)
        
        # 新しいターゲット位置
        new_target_x, new_target_y = generate_target_position()
        session['target_x'] = new_target_x
        session['target_y'] = new_target_y
        
        # クライアントに結果送信
        emit('target_hit', {
            'hit_score': hit_score,
            'total_score': session['score'],
            'hits': session['hits'],
            'total_clicks': session['total_clicks'],
            'new_target_x': new_target_x,
            'new_target_y': new_target_y,
            'click_x': click_x,
            'click_y': click_y
        })
        
        print(f'HIT! Score: {hit_score}, Total: {session["score"]}')
    else:
        # ミス
        new_target_x, new_target_y = generate_target_position()
        session['target_x'] = new_target_x
        session['target_y'] = new_target_y
        
        emit('target_miss', {
            'total_score': session['score'],
            'hits': session['hits'],
            'total_clicks': session['total_clicks'],
            'new_target_x': new_target_x,
            'new_target_y': new_target_y,
            'click_x': click_x,
            'click_y': click_y
        })
        
        print(f'MISS! Total clicks: {session["total_clicks"]}')

def handle_game_end(session_id):
    """ゲーム終了処理"""
    if session_id not in game_sessions:
        return
    
    session = game_sessions[session_id]
    session['game_active'] = False
    
    # 最終統計計算
    elapsed_time = time.time() - session['start_time']
    accuracy = (session['hits'] / session['total_clicks'] * 100) if session['total_clicks'] > 0 else 0
    avg_score = sum(session['hit_scores']) / len(session['hit_scores']) if session['hit_scores'] else 0
    hits_per_second = session['hits'] / elapsed_time if elapsed_time > 0 else 0
    
    # パフォーマンス評価
    if accuracy >= 80 and avg_score >= 80:
        rating = "EXCELLENT!"
        rating_color = "#00FF00"
    elif accuracy >= 60 and avg_score >= 60:
        rating = "GOOD"
        rating_color = "#FFFF00"
    elif accuracy >= 40 and avg_score >= 40:
        rating = "FAIR"
        rating_color = "#FFA500"
    else:
        rating = "NEEDS PRACTICE"
        rating_color = "#FF0000"
    
    emit('game_ended', {
        'final_score': session['score'],
        'hits': session['hits'],
        'total_clicks': session['total_clicks'],
        'accuracy': round(accuracy, 1),
        'avg_score': round(avg_score, 1),
        'hits_per_second': round(hits_per_second, 1),
        'rating': rating,
        'rating_color': rating_color,
        'elapsed_time': round(elapsed_time, 1)
    })
    
    print(f'Game ended for {session_id}. Final score: {session["score"]}')

@socketio.on('get_game_status')
def handle_get_game_status():
    """ゲーム状態取得"""
    session_id = request.sid
    if session_id not in game_sessions:
        emit('game_status', {'game_active': False})
        return
    
    session = game_sessions[session_id]
    elapsed_time = time.time() - session['start_time']
    remaining_time = max(0, GAME_TIME - elapsed_time)
    
    if elapsed_time >= GAME_TIME and session['game_active']:
        handle_game_end(session_id)
        return
    
    accuracy = (session['hits'] / session['total_clicks'] * 100) if session['total_clicks'] > 0 else 0
    
    emit('game_status', {
        'game_active': session['game_active'],
        'remaining_time': round(remaining_time, 1),
        'score': session['score'],
        'hits': session['hits'],
        'total_clicks': session['total_clicks'],
        'accuracy': round(accuracy, 1),
        'target_x': session['target_x'],
        'target_y': session['target_y']
    })

if __name__ == '__main__':
    print("🎯 Flask AIM Trainer Server Starting...")
    print("Access the game at: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)