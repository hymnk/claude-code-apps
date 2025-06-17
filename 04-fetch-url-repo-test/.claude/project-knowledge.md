# プロジェクト知識

## アーキテクチャの決定

### ナレッジ管理システムの採用
- **決定**: `.claude/`ディレクトリでのナレッジ管理システムを導入
- **理由**: プロジェクトの知識継承と効率的な開発のため
- **実装**: Zenn記事（https://zenn.dev/driller/articles/2a23ef94f1d603）を参考にした構成

## 実装パターン

### ファイル構成パターン
```
project-root/
├── CLAUDE.md
└── .claude/
    ├── context.md
    ├── project-knowledge.md
    ├── project-improvements.md
    ├── common-patterns.md
    ├── debug-log.md
    └── debug/
        ├── sessions/
        ├── temp-logs/
        └── archive/
```

## 避けるべきパターン
- 未定（開発進行とともに追加）

## ライブラリ・技術選択
- 未定（開発開始時に記録）

## パフォーマンス考慮事項
- 未定（実装時に追加）