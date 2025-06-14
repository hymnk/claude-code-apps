# 🎋 ZEN Tetris v2 - Web版

## 🌐 概要

ZEN Tetris v2のWeb版は、既存のPython+Pygameゲームをブラウザで楽しめるように変換したバージョンです。FastAPIとWebSocketを使用してリアルタイムゲームプレイを実現しています。

## ✨ 特徴

### 🏗️ 技術スタック
- **バックエンド**: FastAPI + WebSocket (Python)
- **フロントエンド**: HTML5 Canvas + JavaScript
- **通信**: リアルタイムWebSocket通信
- **レンダリング**: 60FPS Hardware Accelerated Canvas

### 🎮 ゲーム機能
- ✅ **完全な機能パリティ**: 元のPygame版の全機能
- ✅ **リアルタイムゲームプレイ**: 60FPS滑らかな操作
- ✅ **パーティクルエフェクト**: ライン消去時のエフェクト
- ✅ **アースカラー美学**: 落ち着いた色調デザイン
- ✅ **マルチセッション対応**: 複数プレイヤー同時プレイ
- ✅ **レスポンシブデザイン**: デスクトップ・モバイル対応

## 🚀 起動方法

### 簡単起動（推奨）
```bash
# 仮想環境を有効化
source venv/bin/activate

# Web版を起動（ブラウザが自動で開きます）
python start_web.py
```

### 手動起動
```bash
# 仮想環境を有効化
source venv/bin/activate

# Webサーバーを起動
python web_server.py

# ブラウザで http://localhost:8000 にアクセス
```

## 🎯 操作方法

| キー | 動作 |
|------|------|
| **← →** | 左右移動 |
| **↓** | 高速落下 |
| **↑** | 回転 |
| **スペース** | 一気に落下 |
| **P** | ポーズ/再開 |
| **R** | リスタート |

## 📁 ファイル構成

```
├── web_server.py              # FastAPIサーバー
├── start_web.py               # 簡単起動スクリプト
├── src/zen_tetris/web_game.py # Web対応ゲームロジック
├── web_templates/
│   └── index.html            # ゲームHTML
└── web_static/
    └── tetris-client.js      # JavaScriptクライアント
```

## 🔧 技術詳細

### アーキテクチャ
- **Backend-Authoritative**: 全ゲームロジックはPython側で実行
- **WebSocket通信**: リアルタイム双方向通信
- **Canvas描画**: ハードウェア加速による高速描画
- **セッション管理**: 独立したゲームセッション

### パフォーマンス
- **60FPS**: 滑らかなゲームプレイ
- **低遅延**: ~20-50ms入力レスポンス
- **メモリ効率**: パーティクル数制限とガベージコレクション
- **接続安定性**: 自動再接続機能

## 🌟 従来版との比較

| 項目 | Pygame版 | Web版 |
|------|----------|-------|
| **インストール** | Python環境必要 | ブラウザのみ |
| **GUI依存** | X11/WSLg必要 | 不要 |
| **アクセス性** | ローカルのみ | どこからでも |
| **マルチプレイ** | 単一セッション | 複数セッション |
| **パフォーマンス** | ネイティブ | ほぼ同等 |

## 🔗 エンドポイント

- `http://localhost:8000/` - ゲーム画面
- `http://localhost:8000/health` - ヘルスチェック
- `ws://localhost:8000/ws` - WebSocket接続

## 🛠️ 開発情報

### 依存関係
```txt
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
websockets>=12.0
jinja2>=3.1.2
python-multipart>=0.0.6
```

### デプロイ
```bash
# 本番環境での起動
uvicorn web_server:app --host 0.0.0.0 --port 8000
```

---

*心を落ち着けて、ブラウザでZENテトリスをお楽しみください* 🧘‍♀️