# 🗾 日本地図ブラウザ

Pythonで動作する日本地図表示ブラウザアプリです。FlaskとD3.jsを使用してインタラクティブな日本地図を表示します。

## 機能

- 📍 47都道府県の地図表示
- 🎨 地域別カラーリング（北海道、東北、関東、中部、近畿、中国、四国、九州、沖縄）
- 🖱️ クリック・ホバーインタラクション
- 📱 レスポンシブデザイン
- ℹ️ 都道府県情報パネル

## インストール

1. 必要なパッケージをインストール：
```bash
pip install -r requirements.txt
```

## 起動方法

メインスクリプトを実行：
```bash
python main.py
```

または直接Flaskアプリを起動：
```bash
python app.py
```

ブラウザが自動で開き、`http://localhost:5000`でアプリにアクセスできます。

## プロジェクト構成

```
06-japan-map-crasher/
├── main.py              # メイン起動スクリプト
├── app.py               # Flaskアプリケーション
├── requirements.txt     # 依存パッケージ
├── templates/
│   └── index.html      # HTMLテンプレート
└── static/
    ├── css/
    │   └── style.css   # スタイルシート
    └── js/
        └── map.js      # JavaScript（地図機能）
```

## 使用技術

- **バックエンド**: Python 3.x, Flask
- **フロントエンド**: HTML5, CSS3, JavaScript
- **地図描画**: D3.js
- **スタイリング**: CSS Grid, Flexbox

## 注意事項

- 地図データは簡略化されています
- 実際のプロジェクトではGeoJSONまたはTopoJSONファイルを使用することを推奨します

## ライセンス

MIT License