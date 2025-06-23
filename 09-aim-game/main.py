#!/usr/bin/env python3
"""
FPS AIM Trainer - Main Entry Point
メインスクリプト
"""

import subprocess
import sys
import os

def install_requirements():
    """必要なパッケージをインストール"""
    print("🎯 FPS AIM Trainer - 依存関係をインストール中...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ パッケージのインストールが完了しました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ パッケージのインストールに失敗しました: {e}")
        print("💡 仮想環境を使用している場合は、まず仮想環境をアクティベートしてください")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt が見つかりません")
        return False

def main():
    """メイン実行関数"""
    print("🎯 FPS AIM Trainer")
    print("=" * 50)
    print("📋 ゲームの準備中...")
    
    # requirements.txtが存在するかチェック
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt が見つかりません")
        return
    
    # 仮想環境チェック
    if 'VIRTUAL_ENV' not in os.environ and 'venv' not in sys.prefix:
        print("⚠️  仮想環境が検出されませんでした")
        print("💡 pip install pygame でpygameを直接インストールしても実行できます")
    
    # パッケージインストール
    if not install_requirements():
        print("💡 手動でインストールしてください: pip install pygame")
        return
    
    print("\n🚀 ゲームを起動中...")
    print("📖 ゲームの説明:")
    print("   • 1280x960解像度の60秒間AIMトレーニング")
    print("   • 中央の的をクリックして開始")
    print("   • 的の中心に近いほど高得点")
    print("   • ESCキーで終了、Rキーでリスタート")
    print("=" * 50)
    
    # ゲーム起動
    try:
        import aim_trainer
        # ゲーム実行は aim_trainer.py の main で行われる
    except ImportError as e:
        print(f"❌ ゲームの起動に失敗しました: {e}")
        print("💡 pygame がインストールされていることを確認してください")
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}")

if __name__ == "__main__":
    main()