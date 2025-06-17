import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from loto6_predictor import Loto6Predictor
from loto6_predictor.ui.styles import get_custom_css
from loto6_predictor.ui.components import (
    display_prediction_card, 
    display_advanced_prediction_card,
    display_best_prediction_highlight,
    display_stats_card, 
    display_frequency_ranking
)

# ページ設定
st.set_page_config(
    page_title="ロト6予測システム",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# キャッシュ関数
@st.cache_data(ttl=300)  # 5分間キャッシュ
def load_data():
    """データを読み込み（キャッシュ付き）"""
    predictor = Loto6Predictor()
    predictor.fetch_historical_data()
    predictor.analyze_frequency()
    predictor.analyze_patterns()
    return predictor


def main():
    # タイトル
    st.title("🎯 高度AI分析ロト6予測システム")
    st.markdown("**2025年6月最新データ** - 過去1000回分の実データを高度なアルゴリズムで分析")
    
    # サイドバー
    st.sidebar.title("📊 設定")
    
    # データ読み込み
    with st.spinner("データを読み込み中..."):
        predictor = load_data()
    
    # データ更新ボタン
    if st.sidebar.button("🔄 データを更新", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    # データ情報表示
    if predictor.data:
        st.sidebar.success(f"📈 分析データ: {len(predictor.data)}回分")
        st.sidebar.info(f"📅 期間: {predictor.data[-1]['draw_date']} ～ {predictor.data[0]['draw_date']}")
    
    # 最終更新時刻
    st.sidebar.info(f"🕒 最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # メインコンテンツ
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 予測結果", "📊 統計分析", "📈 グラフ", "📋 過去の結果"])
    
    with tab1:
        st.header("🎯 高度AI分析による予測番号")
        
        # 予測実行
        predictions = predictor.predict_numbers()
        
        # 最も信頼度の高い予測をハイライト表示
        best_prediction = predictor.get_best_prediction()
        if best_prediction:
            method_names = {
                "advanced_ensemble": "アンサンブル統合予測",
                "weighted_frequency": "重み付き頻度分析",
                "pattern_similarity": "パターン類似度分析",
                "trend_integration": "トレンド統合分析",
                "statistical_optimization": "統計的最適化",
                "high_frequency": "高頻度重視",
                "low_frequency": "低頻度重視（逆張り）",
                "balanced": "バランス重視",
                "trending": "最新トレンド"
            }
            
            method_display_name = method_names.get(best_prediction["method"], best_prediction["method"])
            display_best_prediction_highlight(
                method_display_name,
                best_prediction["numbers"],
                best_prediction["confidence"]
            )
        
        st.subheader("📊 全予測手法（信頼度順）")
        
        # 各予測手法の結果を信頼度順に表示
        method_descriptions = {
            "advanced_ensemble": "複数の高度アルゴリズムを統合した最先端予測",
            "weighted_frequency": "時期別の重み付きを考慮した頻度分析予測",
            "pattern_similarity": "過去の類似パターンから学習した予測",
            "trend_integration": "短期・中期・長期トレンドを統合した予測",
            "statistical_optimization": "統計的最適化理論に基づく予測",
            "high_frequency": "過去によく出現した番号を重視した予測",
            "low_frequency": "出現頻度が低い番号を重視した逆張り予測",
            "balanced": "奇偶・合計値のバランスを重視した予測",
            "trending": "直近の傾向を重視した予測"
        }
        
        for method, data in predictions.items():
            method_display_name = method_names.get(method, method)
            description = method_descriptions.get(method, "")
            
            display_advanced_prediction_card(
                method_display_name,
                data["numbers"],
                data["confidence"],
                data["rank"],
                description
            )
        
        # 注意事項
        st.info("💡 信頼度は統計分析・パターン認識・トレンド分析・数学的検証を総合して算出されています。")
        st.warning("⚠️ この予測は高度な統計分析に基づく参考値です。実際の当選を保証するものではありません。")
    
    with tab2:
        st.header("📊 統計分析結果")
        
        # 基本統計
        col1, col2, col3 = st.columns(3)
        
        freq_analysis = predictor.analysis_results.get("frequency", {})
        pattern_analysis = predictor.analysis_results.get("patterns", {})
        
        with col1:
            display_stats_card("分析対象回数", str(len(predictor.data)), "分析対象回数")
        
        with col2:
            avg_freq = freq_analysis.get("average_frequency", 0)
            display_stats_card("平均出現頻度", f"{avg_freq:.1f}", "平均出現頻度")
        
        with col3:
            avg_sum = pattern_analysis.get("sum_stats", {}).get("avg", 0)
            display_stats_card("平均合計値", f"{avg_sum:.1f}", "平均合計値")
        
        # 頻度ランキング
        st.subheader("📋 出現頻度ランキング TOP10")
        
        col1, col2 = st.columns(2)
        
        with col1:
            most_common = freq_analysis.get("most_common", [])
            display_frequency_ranking("最頻出番号", most_common)
        
        with col2:
            least_common = freq_analysis.get("least_common", [])
            display_frequency_ranking("最低頻度番号", least_common)
        
        # パターン分析
        st.subheader("🔍 パターン分析")
        
        col1, col2 = st.columns(2)
        
        with col1:
            odd_avg = pattern_analysis.get("odd_even_distribution", {}).get("avg_odd", 3)
            even_avg = pattern_analysis.get("odd_even_distribution", {}).get("avg_even", 3)
            st.write(f"**奇偶バランス**")
            st.write(f"平均奇数: {odd_avg:.1f}個")
            st.write(f"平均偶数: {even_avg:.1f}個")
        
        with col2:
            consecutive_avg = pattern_analysis.get("consecutive_avg", 0)
            st.write(f"**連続番号**")
            st.write(f"平均連続ペア: {consecutive_avg:.2f}")
    
    with tab3:
        st.header("📈 出現頻度グラフ")
        
        # 頻度データ取得
        numbers, frequencies = predictor.get_frequency_data_for_chart()
        
        # 棒グラフ
        fig = px.bar(
            x=numbers, 
            y=frequencies,
            title="各番号の出現頻度",
            labels={"x": "番号", "y": "出現回数"},
            color=frequencies,
            color_continuous_scale="Blues"
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # ヒートマップ
        st.subheader("📊 出現頻度ヒートマップ")
        
        # 7x7のグリッドに配置（1-43番号）
        heatmap_data = []
        for i in range(7):
            row = []
            for j in range(7):
                num = i * 7 + j + 1
                if num <= 43:
                    freq = frequencies[num - 1] if num <= len(frequencies) else 0
                    row.append(freq)
                else:
                    row.append(0)
            heatmap_data.append(row)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            colorscale='Blues',
            showscale=True
        ))
        
        fig_heatmap.update_layout(
            title="番号出現頻度ヒートマップ",
            height=400
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab4:
        st.header("📋 過去の抽選結果")
        
        recent_draws = predictor.get_recent_draws(50)
        
        if recent_draws:
            # データフレーム作成
            df_data = []
            for draw in recent_draws:
                numbers_str = " - ".join([f"{n:02d}" for n in draw["numbers"]])
                df_data.append({
                    "抽選日": draw["draw_date"],
                    "当選番号": numbers_str,
                    "ボーナス": f"{draw['bonus']:02d}",
                    "奇数個数": sum(1 for n in draw["numbers"] if n % 2 == 1),
                    "合計値": sum(draw["numbers"])
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("過去の抽選結果データがありません")

if __name__ == "__main__":
    main()