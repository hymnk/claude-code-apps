import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_japan_population_data, load_japan_geojson

# Page config
st.set_page_config(
    page_title="日本人口変化マップ",
    page_icon="🗾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    .prefecture-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .population-value {
        font-size: 2rem;
        font-weight: bold;
        color: #e74c3c;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def get_population_data():
    return load_japan_population_data()

@st.cache_data
def get_geojson_data():
    return load_japan_geojson()

# Main app
def main():
    st.title("🗾 日本人口変化マップ (1950-2020)")
    st.markdown("都道府県別の人口変化をインタラクティブに可視化")
    
    # Load data
    population_data = get_population_data()
    geojson_data = get_geojson_data()
    
    # Sidebar controls
    st.sidebar.header("📊 コントロール")
    
    # Year slider
    min_year = int(population_data['year'].min())
    max_year = int(population_data['year'].max())
    selected_year = st.sidebar.slider(
        "年を選択",
        min_value=min_year,
        max_value=max_year,
        value=min_year,
        step=5,
        format="%d年"
    )
    
    # Filter data for selected year
    year_data = population_data[population_data['year'] == selected_year].copy()
    
    # Display mode selection
    display_mode = st.sidebar.radio(
        "表示モード",
        ["地図表示", "グラフ表示", "両方表示"]
    )
    
    # Top prefectures filter
    top_n = st.sidebar.slider("上位都道府県数", 5, 20, 10)
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if display_mode in ["地図表示", "両方表示"]:
            st.subheader(f"📍 {selected_year}年の人口分布")
            
            # Create scatter plot map
            fig_map = px.scatter_geo(
                year_data,
                lat=[feat['geometry']['coordinates'][1] for feat in geojson_data['features']],
                lon=[feat['geometry']['coordinates'][0] for feat in geojson_data['features']],
                size='population',
                color='population',
                hover_name='prefecture',
                hover_data={'population': ':,'},
                title=f"日本の人口分布 ({selected_year}年)",
                color_continuous_scale='Viridis',
                size_max=50
            )
            
            # Update layout for Japan
            fig_map.update_geos(
                showcoastlines=True,
                coastlinecolor="LightBlue",
                showland=True,
                landcolor="LightGray",
                showocean=True,
                oceancolor="LightBlue",
                projection_type="natural earth",
                center={"lat": 36, "lon": 138},
                projection_scale=6
            )
            
            fig_map.update_layout(
                height=600,
                margin={"r": 0, "t": 50, "l": 0, "b": 0}
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
        
        if display_mode in ["グラフ表示", "両方表示"]:
            st.subheader(f"📊 {selected_year}年の人口ランキング")
            
            # Top prefectures bar chart
            top_prefectures = year_data.nlargest(top_n, 'population')
            
            fig_bar = px.bar(
                top_prefectures,
                x='population',
                y='prefecture',
                orientation='h',
                title=f"上位{top_n}都道府県の人口 ({selected_year}年)",
                labels={'population': '人口 (千人)', 'prefecture': '都道府県'},
                color='population',
                color_continuous_scale='Blues'
            )
            
            fig_bar.update_layout(
                height=400,
                yaxis={'categoryorder': 'total ascending'},
                xaxis_tickformat=',',
                showlegend=False
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("📈 統計情報")
        
        # Key statistics
        total_population = year_data['population'].sum()
        avg_population = year_data['population'].mean()
        max_prefecture = year_data.loc[year_data['population'].idxmax()]
        min_prefecture = year_data.loc[year_data['population'].idxmin()]
        
        # Display metrics
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #7f8c8d; font-size: 0.9rem;">総人口</div>
            <div class="population-value">{total_population:,}</div>
            <div style="color: #7f8c8d; font-size: 0.8rem;">千人</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #7f8c8d; font-size: 0.9rem;">平均人口</div>
            <div class="population-value">{avg_population:,.0f}</div>
            <div style="color: #7f8c8d; font-size: 0.8rem;">千人</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #7f8c8d; font-size: 0.9rem;">最多人口</div>
            <div class="prefecture-name">{max_prefecture['prefecture']}</div>
            <div style="color: #e74c3c; font-size: 1.5rem; font-weight: bold;">{max_prefecture['population']:,}千人</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #7f8c8d; font-size: 0.9rem;">最少人口</div>
            <div class="prefecture-name">{min_prefecture['prefecture']}</div>
            <div style="color: #3498db; font-size: 1.5rem; font-weight: bold;">{min_prefecture['population']:,}千人</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Top 5 prefectures list
        st.subheader("🏆 上位5都道府県")
        top_5 = year_data.nlargest(5, 'population')
        for i, (_, row) in enumerate(top_5.iterrows(), 1):
            st.markdown(f"""
            <div style="padding: 0.5rem; border-left: 3px solid #3498db; margin: 0.5rem 0; background: #f8f9fa;">
                <strong>{i}. {row['prefecture']}</strong><br>
                <span style="color: #e74c3c; font-weight: bold;">{row['population']:,}千人</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Time series analysis
    st.subheader("📈 人口推移の分析")
    
    # Prefecture selection for time series
    selected_prefectures = st.multiselect(
        "都道府県を選択して人口推移を確認",
        options=population_data['prefecture'].unique(),
        default=['東京都', '大阪府', '愛知県', '神奈川県', '北海道']
    )
    
    if selected_prefectures:
        time_series_data = population_data[population_data['prefecture'].isin(selected_prefectures)]
        
        fig_line = px.line(
            time_series_data,
            x='year',
            y='population',
            color='prefecture',
            title="選択された都道府県の人口推移",
            labels={'year': '年', 'population': '人口 (千人)', 'prefecture': '都道府県'}
        )
        
        fig_line.update_layout(
            height=400,
            xaxis_title="年",
            yaxis_title="人口 (千人)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.8rem;">
        ※ このアプリのデータは実際の統計データに基づいたシミュレーションです。<br>
        正確な人口データは総務省統計局をご確認ください。
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()