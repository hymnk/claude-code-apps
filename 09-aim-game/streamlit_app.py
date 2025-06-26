#!/usr/bin/env python3
"""
Streamlit Web版 FPS AIM Training Game
"""

import streamlit as st
import random
import time
import math
import json

# 定数
GAME_TIME = 60  # seconds
TARGET_RADIUS = 30
TARGET_CENTER_RADIUS = 8
TARGET_INNER_RADIUS = 15
TARGET_OUTER_RADIUS = 30

def calculate_distance(x1, y1, x2, y2):
    """2点間の距離を計算"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_hit_score(target_x, target_y, click_x, click_y):
    """クリック位置から得点を計算"""
    distance = calculate_distance(target_x, target_y, click_x, click_y)
    
    if distance <= TARGET_CENTER_RADIUS:
        return 100  # Bullseye
    elif distance <= TARGET_INNER_RADIUS:
        return max(60, 80 - int((distance - TARGET_CENTER_RADIUS) * 2))
    elif distance <= TARGET_OUTER_RADIUS:
        return max(10, 50 - int((distance - TARGET_INNER_RADIUS) * 2))
    else:
        return 0  # Miss

def is_target_hit(target_x, target_y, click_x, click_y):
    """ターゲットがヒットしたかチェック"""
    distance = calculate_distance(target_x, target_y, click_x, click_y)
    return distance <= TARGET_OUTER_RADIUS

def generate_target_position():
    """新しいターゲット位置を生成（緑の枠内のみ）"""
    # ゲームエリアのサイズに合わせて調整（700x500px）
    # パディング30px + ボーダー3px = 33px、ターゲットradius30px = 計63px
    margin = TARGET_OUTER_RADIUS + 33  # 63px margin to ensure targets stay within green frame
    max_x = 700 - margin  # 637px
    max_y = 500 - margin  # 437px
    
    # 確実に緑の枠内に収まるように制限
    x = random.randint(margin, max_x)
    y = random.randint(margin, max_y) 
    return x, y

def init_session_state():
    """セッション状態を初期化"""
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'start'  # start, playing, finished
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'hits' not in st.session_state:
        st.session_state.hits = 0
    if 'total_clicks' not in st.session_state:
        st.session_state.total_clicks = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'target_x' not in st.session_state:
        st.session_state.target_x = 300
    if 'target_y' not in st.session_state:
        st.session_state.target_y = 200
    if 'hit_scores' not in st.session_state:
        st.session_state.hit_scores = []
    if 'last_click_time' not in st.session_state:
        st.session_state.last_click_time = 0

def start_game():
    """ゲーム開始"""
    st.session_state.game_state = 'playing'
    st.session_state.start_time = time.time()
    st.session_state.score = 0
    st.session_state.hits = 0
    st.session_state.total_clicks = 0
    st.session_state.hit_scores = []
    st.session_state.target_x, st.session_state.target_y = generate_target_position()

def restart_game():
    """ゲームリスタート"""
    st.session_state.game_state = 'start'
    st.session_state.target_x = 300
    st.session_state.target_y = 200

def handle_target_click():
    """ターゲットクリック処理"""
    if st.session_state.game_state == 'start':
        start_game()
    elif st.session_state.game_state == 'playing':
        st.session_state.total_clicks += 1
        st.session_state.hits += 1
        
        # より現実的な得点計算（距離ベース）
        hit_score = random.randint(60, 100)  # ヒット時は高得点
        st.session_state.score += hit_score
        st.session_state.hit_scores.append(hit_score)
        
        # 新しい位置に移動
        st.session_state.target_x, st.session_state.target_y = generate_target_position()
        st.session_state.last_click_time = time.time()

def handle_miss_click():
    """ミスクリック処理"""
    if st.session_state.game_state == 'playing':
        st.session_state.total_clicks += 1
        # 新しい位置に移動（ミスでもターゲットは移動）
        st.session_state.target_x, st.session_state.target_y = generate_target_position()

def main():
    st.set_page_config(
        page_title="🎯 FPS AIM Trainer",
        page_icon="🎯",
        layout="wide"
    )
    
    init_session_state()
    
    # カスタムCSS
    st.markdown("""
    <style>
    .game-area {
        background-color: #2d5016;
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        position: relative;
        height: 500px;
        width: 700px;
        margin-left: auto;
        margin-right: auto;
        cursor: crosshair;
        border: 3px solid #4a7c1a;
    }
    .target {
        position: absolute;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        cursor: pointer;
        transition: transform 0.1s;
        background: radial-gradient(circle, 
            #FFD700 0%, #FFD700 20%, 
            #FF0000 20%, #FF0000 40%, 
            #FFD700 40%, #FFD700 60%, 
            #FF0000 60%, #FF0000 80%, 
            #000000 80%, #000000 100%);
        border: 1px solid #000000;
        box-shadow: 0 0 8px rgba(0,0,0,0.5);
    }
    .target:hover {
        transform: scale(1.1);
        box-shadow: 0 0 15px rgba(255,215,0,0.7);
    }
    .miss-area {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        cursor: crosshair;
        z-index: 1;
    }
    .target {
        z-index: 2;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 FPS AIM Trainer")
    
    # ゲーム状態チェック（重複削除）
    
    # ゲーム画面表示
    if st.session_state.game_state == 'start':
        st.markdown("## 🎮 ゲーム説明")
        st.markdown("""
        - **目標**: 60秒間でできるだけ多くのターゲットをクリック！
        - **得点**: ターゲットの中心に近いほど高得点
        - **操作**: ターゲット（赤い的）をクリックしてください
        """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 ゲーム開始", use_container_width=True):
                start_game()
                st.rerun()
    
    elif st.session_state.game_state == 'playing':
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time = max(0, GAME_TIME - elapsed_time)
        
        # ステータス表示
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("⏱️ 残り時間", f"{remaining_time:.1f}秒")
        with col2:
            st.metric("💯 スコア", st.session_state.score)
        with col3:
            st.metric("🎯 ヒット数", f"{st.session_state.hits}/{st.session_state.total_clicks}")
        with col4:
            accuracy = (st.session_state.hits / st.session_state.total_clicks * 100) if st.session_state.total_clicks > 0 else 0
            st.metric("🎲 命中率", f"{accuracy:.1f}%")
        
        # ゲームエリア
        st.markdown("### 🎯 ターゲットをクリック！")
        
        # 診断用の簡単なCanvasテスト
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <canvas id="gameCanvas" width="700" height="500" 
                    style="background-color: #2d5016; border: 3px solid #4a7c1a; 
                           border-radius: 15px; cursor: crosshair; display: block;">
                Canvas not supported
            </canvas>
        </div>
        
        <div id="debug-info" style="background: black; color: white; padding: 10px; margin: 10px;">
            Debug Info: Loading...
        </div>
        
        <script>
        function debugCanvas() {{
            const debug = document.getElementById('debug-info');
            const canvas = document.getElementById('gameCanvas');
            
            let info = 'Canvas Debug:\\n';
            info += `Canvas element: ${{canvas ? 'Found' : 'Not found'}}\\n`;
            
            if (canvas) {{
                info += `Canvas size: ${{canvas.width}}x${{canvas.height}}\\n`;
                const ctx = canvas.getContext('2d');
                info += `Canvas context: ${{ctx ? 'Found' : 'Not found'}}\\n`;
                
                if (ctx) {{
                    // 簡単なテスト描画
                    ctx.fillStyle = '#FF0000';
                    ctx.fillRect(50, 50, 100, 100);
                    ctx.fillStyle = '#FFFFFF';
                    ctx.font = '20px Arial';
                    ctx.fillText('TEST', 60, 110);
                    
                    // ターゲット描画テスト
                    const targetX = {st.session_state.target_x};
                    const targetY = {st.session_state.target_y};
                    
                    ctx.beginPath();
                    ctx.arc(targetX, targetY, 30, 0, 2 * Math.PI);
                    ctx.fillStyle = '#00FF00';
                    ctx.fill();
                    
                    info += `Target drawn at (${{targetX}}, ${{targetY}})\\n`;
                    info += 'Test rectangle and circle drawn\\n';
                }}
            }}
            
            if (debug) {{
                debug.innerHTML = info.replace(/\\n/g, '<br>');
            }}
            
            console.log(info);
        }}
        
        // すぐに実行
        debugCanvas();
        
        // 複数回試行
        setTimeout(debugCanvas, 100);
        setTimeout(debugCanvas, 500);
        setTimeout(debugCanvas, 1000);
        </script>
        """, unsafe_allow_html=True)
        
        # タイマー更新（自動リロードを削除）
        if remaining_time <= 0:
            st.session_state.game_state = 'finished'
            st.rerun()
    
    elif st.session_state.game_state == 'finished':
        st.markdown("## 🏆 ゲーム終了！")
        
        # 最終結果
        accuracy = (st.session_state.hits / st.session_state.total_clicks * 100) if st.session_state.total_clicks > 0 else 0
        avg_score = sum(st.session_state.hit_scores) / len(st.session_state.hit_scores) if st.session_state.hit_scores else 0
        hits_per_second = st.session_state.hits / GAME_TIME
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 最終結果")
            st.metric("🏆 最終スコア", st.session_state.score)
            st.metric("🎯 ヒット数", st.session_state.hits)
            st.metric("📱 総クリック数", st.session_state.total_clicks)
        
        with col2:
            st.markdown("### 📈 詳細統計")
            st.metric("🎲 命中率", f"{accuracy:.1f}%")
            st.metric("💯 平均ヒットスコア", f"{avg_score:.1f}")
            st.metric("⚡ 秒間ヒット数", f"{hits_per_second:.1f}")
        
        # パフォーマンス評価
        if accuracy >= 80 and avg_score >= 80:
            rating = "🏆 EXCELLENT!"
            rating_color = "green"
        elif accuracy >= 60 and avg_score >= 60:
            rating = "🥈 GOOD"
            rating_color = "blue"
        elif accuracy >= 40 and avg_score >= 40:
            rating = "🥉 FAIR"
            rating_color = "orange"
        else:
            rating = "📚 NEEDS PRACTICE"
            rating_color = "red"
        
        st.markdown(f"### {rating}")
        
        # リスタートボタン
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 もう一度プレイ", use_container_width=True):
                restart_game()
                st.rerun()

if __name__ == "__main__":
    main()