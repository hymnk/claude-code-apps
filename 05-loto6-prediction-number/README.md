# 🎯 高度AI分析ロト6予測システム

**過去1000回分の実データを高度なアルゴリズムで分析し、最も信頼度の高い予測組み合わせを提案する次世代ロト6予測システム**

## ✨ 主な特徴

### 🧠 高度な分析アルゴリズム
- **時系列トレンド分析**: 短期・中期・長期の傾向を統合
- **パターン類似度検索**: 過去の類似パターンから学習
- **統計的最適化**: 数学的理論に基づく最適解の探索
- **アンサンブル予測**: 複数手法を統合した最先端予測

### 📊 信頼度スコアリング
- **4軸評価**: 頻度・パターン・トレンド・統計的妥当性
- **自動ランキング**: 信頼度に基づく予測順位付け
- **詳細分析**: 各予測の根拠と信頼度を透明化

### 🎨 直感的なWebUI
- **最優秀予測ハイライト**: 最も自信のある組み合わせを強調表示
- **インタラクティブグラフ**: 視覚的な頻度分析とヒートマップ
- **リアルタイム更新**: 最新データの自動取得と分析

## 🚀 クイックスタート

### 環境構築
```bash
# 仮想環境作成・有効化
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 依存関係インストール
pip install -r requirements.txt
```

### Webアプリ起動
```bash
# Streamlitアプリ起動
streamlit run app.py

# またはスクリプト使用
./run_app.sh
```

ブラウザで `http://localhost:8501` にアクセス

### コマンドライン実行
```bash
# 基本予測実行
python main.py

# パッケージとして実行
python -m src.loto6_predictor.core.predictor
```

## 🎯 予測手法

### 基本手法
1. **高頻度重視**: 過去の出現頻度が高い番号を重視
2. **低頻度重視**: 逆張り戦略で低頻度番号を選択
3. **バランス重視**: 奇偶・合計値・分散の最適バランス
4. **最新トレンド**: 直近の傾向を重視した予測

### 高度手法
1. **重み付き頻度分析**: 時期別重み付けによる精密な頻度分析
2. **パターン類似度分析**: 機械学習風の類似パターン検索
3. **トレンド統合分析**: 短期・中期・長期トレンドの統合
4. **統計的最適化**: 数学的最適化理論の適用
5. **アンサンブル統合予測**: 全手法の投票による最終予測

## 📂 プロジェクト構造

```
loto6-predictor/
├── src/
│   └── loto6_predictor/
│       ├── core/           # コア予測クラス
│       ├── data/           # データ取得・処理
│       ├── analysis/       # 分析アルゴリズム
│       ├── prediction/     # 予測エンジン
│       └── ui/             # UIコンポーネント
├── app.py                  # Streamlitアプリ
├── main.py                 # コマンドライン実行
├── requirements.txt        # 依存関係
├── setup.py               # パッケージ設定
└── pyproject.toml         # 現代的な設定ファイル
```

## 🔬 技術仕様

### データソース
- **実データ取得**: https://loto6.thekyo.jp/data/loto6.csv
- **分析対象**: 直近1000回分の当選番号
- **自動更新**: 5分間隔でのデータキャッシュ

### 分析指標
- **頻度分析**: 出現頻度、エントロピー、偏差
- **パターン分析**: 連続性、対称性、区間分布
- **時系列分析**: トレンド変化、周期性、規則性
- **統計分析**: 分散、標準偏差、信頼区間

### 信頼度計算
```
総合信頼度 = 頻度信頼度(25%) + パターン信頼度(30%) + トレンド信頼度(25%) + 統計信頼度(20%)
```

## 📈 使用例

### 最優秀予測の取得
```python
from src.loto6_predictor import Loto6Predictor

predictor = Loto6Predictor()
predictor.fetch_historical_data()

# 最も信頼度の高い予測
best = predictor.get_best_prediction()
print(f"予測番号: {best['numbers']}")
print(f"信頼度: {best['confidence']['overall_confidence']:.1f}%")
```

### 全予測手法の比較
```python
# 全手法の予測と信頼度
predictions = predictor.predict_numbers()
for method, data in predictions.items():
    print(f"{method}: {data['numbers']} (信頼度: {data['confidence']['overall_confidence']:.1f}%)")
```

## ⚖️ 免責事項

- ✅ 本システムは高度な統計分析に基づく**参考値**を提供します
- ❌ 実際の当選を**保証するものではありません**
- 🎲 ギャンブルは自己責任で行ってください
- 📊 予測精度の向上に努めていますが、確率的性質上100%の的中は不可能です

## 🔧 開発・カスタマイズ

### パッケージインストール
```bash
pip install -e .
```

### テスト実行
```bash
python -m pytest tests/
```

### 新しい予測手法の追加
`src/loto6_predictor/prediction/strategies.py` に新しいメソッドを追加

---

**🎯 統計と AI の力で、ロト6予測の新たな可能性を探求しましょう！**