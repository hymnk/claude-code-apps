# Claude Code Python Development Container

このプロジェクトは、Claude CodeをVS Codeで最適に実行できるDevContainer環境のテンプレートです。

## 特徴

- Python 3.12環境（最新安定版）
- Claude Code CLI がプリインストール
- uvパッケージマネージャーによる高速依存関係管理
- 一般的なPython開発ライブラリ（pandas, numpy, flask, fastapi等）
- VS Code拡張機能（Python、Black、Flake8、Jupyter等）
- 自動コードフォーマット設定

## 使用方法

1. VS CodeでDevContainer拡張機能をインストール
2. このフォルダをVS Codeで開く
3. コマンドパレット（Ctrl+Shift+P）から「Dev Containers: Reopen in Container」を選択
4. コンテナが起動するのを待つ

## 含まれているツール

- **Python 3.12**: メインの開発言語（最新安定版）
- **uv**: 高速なPythonパッケージマネージャー
- **Claude Code CLI**: Anthropic Claude AIとの統合
- **Jupyter**: ノートブック環境
- **Flask/FastAPI**: Web開発フレームワーク
- **pandas/numpy**: データ分析ライブラリ
- **pytest**: テストフレームワーク
- **Black/Flake8/mypy**: コード品質ツール

## ポート転送

以下のポートが自動的に転送されます：
- 8000: FastAPI開発サーバー
- 8080: 一般的なWebサーバー
- 3000: React等のフロントエンド開発サーバー

## パッケージ管理（uv）

新しいパッケージの追加：
```bash
uv add package-name
```

開発用パッケージの追加：
```bash
uv add --dev package-name
```

依存関係の同期：
```bash
uv sync
```

## Claude Codeの使用

コンテナ内でClaude Code CLIが利用可能です：

```bash
claude-code --help
```

環境変数`ANTHROPIC_API_KEY`を設定してご利用ください。