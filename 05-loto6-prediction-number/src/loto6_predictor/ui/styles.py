"""
UIスタイル定義
"""

def get_custom_css() -> str:
    """カスタムCSSを取得"""
    return """
    <style>
        /* 全体のフォント設定 */
        .main {
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        
        /* 予測カード */
        .prediction-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        /* 最優秀予測カード */
        .prediction-card-best {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 12px 40px rgba(245, 87, 108, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.3);
            transform: scale(1.02);
        }
        
        /* 優秀予測カード */
        .prediction-card-good {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #2c3e50;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 10px 35px rgba(168, 237, 234, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .prediction-card h4 {
            color: white;
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        .prediction-card p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        
        /* 番号表示 */
        .number-display {
            font-size: 2.2rem;
            font-weight: bold;
            color: #2c3e50;
            text-align: center;
            margin: 0.3rem;
            padding: 0.8rem;
            background: white;
            border-radius: 15px;
            border: 3px solid #3498db;
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
            transition: transform 0.2s ease;
        }
        
        .number-display:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
        }
        
        /* 統計カード */
        .stats-card {
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 0.5rem 0;
            text-align: center;
            box-shadow: 0 6px 20px rgba(116, 185, 255, 0.3);
        }
        
        .stats-card h3 {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        .stats-card p {
            font-size: 1rem;
            margin: 0;
            opacity: 0.9;
        }
        
        /* 頻度表示 */
        .frequency-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.5rem 1rem;
            margin: 0.2rem 0;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 500;
        }
        
        /* タブスタイル */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            font-size: 1.1rem;
            font-weight: 600;
        }
        
        /* メトリクス表示 */
        .metric-container {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #e74c3c;
            margin: 0.5rem 0;
        }
        
        /* データフレーム */
        .dataframe {
            font-size: 1rem;
        }
        
        /* 警告メッセージ */
        .stAlert {
            font-size: 1.1rem;
            font-weight: 500;
        }
    </style>
    """