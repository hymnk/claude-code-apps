"""
UIコンポーネント
"""

import streamlit as st
from typing import List, Dict


def display_advanced_prediction_card(method_name: str, numbers: List[int], confidence_data: Dict, rank: int, description: str = ""):
    """高度な予測結果カードを表示"""
    confidence_score = confidence_data["overall_confidence"]
    interpretation = confidence_data["interpretation"]
    
    # ランクに応じたカード色設定
    if rank == 1:
        card_class = "prediction-card-best"
        rank_emoji = "🏆"
    elif rank <= 3:
        card_class = "prediction-card-good"
        rank_emoji = "🥈"
    else:
        card_class = "prediction-card"
        rank_emoji = "📊"
    
    st.markdown(f"""
    <div class="{card_class}">
        <h4>{rank_emoji} {method_name} (信頼度: {confidence_score:.1f}%)</h4>
        <p>{interpretation}</p>
        {f'<p style="font-size: 0.9em; opacity: 0.8;">{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # 番号を横並びで表示
    cols = st.columns(6)
    for i, num in enumerate(numbers):
        with cols[i]:
            st.markdown(f'<div class="number-display">{num:02d}</div>', unsafe_allow_html=True)
    
    # 統計情報と詳細
    col1, col2, col3, col4 = st.columns(4)
    
    odd_count = sum(1 for n in numbers if n % 2 == 1)
    total_sum = sum(numbers)
    
    with col1:
        st.metric("奇数", f"{odd_count}個")
    with col2:
        st.metric("偶数", f"{6-odd_count}個")
    with col3:
        st.metric("合計", f"{total_sum}")
    with col4:
        st.metric("ランク", f"{rank}位")
    
    # 詳細情報をエクスパンダーで表示
    with st.expander("🔍 詳細分析"):
        details = confidence_data["details"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**分析項目別スコア**")
            st.write(f"• 頻度分析: {details['frequency_confidence']:.2f}")
            st.write(f"• パターン分析: {details['pattern_confidence']:.2f}")
        
        with col2:
            st.write("**　**")  # 空白でスペーシング
            st.write(f"• トレンド分析: {details['trend_confidence']:.2f}")
            st.write(f"• 統計的妥当性: {details['statistical_confidence']:.2f}")


def display_prediction_card(method_name: str, numbers: List[int], description: str):
    """基本予測結果カードを表示（後方互換性）"""
    st.markdown(f"""
    <div class="prediction-card">
        <h4>{method_name}</h4>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 番号を横並びで表示
    cols = st.columns(6)
    for i, num in enumerate(numbers):
        with cols[i]:
            st.markdown(f'<div class="number-display">{num:02d}</div>', unsafe_allow_html=True)
    
    # 統計情報
    odd_count = sum(1 for n in numbers if n % 2 == 1)
    total_sum = sum(numbers)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("奇数", f"{odd_count}個")
    with col2:
        st.metric("偶数", f"{6-odd_count}個")
    with col3:
        st.metric("合計", f"{total_sum}")


def display_stats_card(title: str, value: str, description: str):
    """統計カードを表示"""
    st.markdown(f"""
    <div class="stats-card">
        <h3>{value}</h3>
        <p>{description}</p>
    </div>
    """, unsafe_allow_html=True)


def display_frequency_ranking(title: str, data: List[tuple]):
    """頻度ランキングを表示"""
    st.write(f"**{title}**")
    for i, (num, count) in enumerate(data[:10], 1):
        st.markdown(f"""
        <div class="frequency-item">
            {i:2d}. {num:2d}番: {count}回
        </div>
        """, unsafe_allow_html=True)


def display_best_prediction_highlight(method_name: str, numbers: List[int], confidence_data: Dict):
    """最も自信のある予測をハイライト表示"""
    confidence_score = confidence_data["overall_confidence"]
    interpretation = confidence_data["interpretation"]
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 12px 40px rgba(245, 87, 108, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
    ">
        <h2>🎯 最も自信のある予測</h2>
        <h3>{method_name}</h3>
        <p style="font-size: 1.2rem; margin: 1rem 0;">信頼度: {confidence_score:.1f}% ({interpretation})</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 番号を大きく表示
    cols = st.columns(6)
    for i, num in enumerate(numbers):
        with cols[i]:
            st.markdown(f"""
            <div style="
                font-size: 3rem;
                font-weight: bold;
                color: #2c3e50;
                text-align: center;
                margin: 0.5rem;
                padding: 1rem;
                background: white;
                border-radius: 20px;
                border: 4px solid #f5576c;
                box-shadow: 0 8px 24px rgba(245, 87, 108, 0.3);
                transform: scale(1.1);
            ">
                {num:02d}
            </div>
            """, unsafe_allow_html=True)