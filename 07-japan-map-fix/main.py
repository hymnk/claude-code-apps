#!/usr/bin/env python3
"""
高品質日本地図ブラウザアプリ - メイン起動スクリプト（Matplotlib版）
"""

import sys
import os
import threading

# アプリケーションのディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """メイン関数"""
    print("🗾 高品質日本地図ブラウザアプリ（Matplotlib版）")
    print("=" * 60)
    print("📍 URL: http://localhost:5000")
    print("📱 ブラウザが自動で開きます")
    print("🎨 JavaScript不使用の純Python地図表示")
    print("🛑 終了するには Ctrl+C を押してください")
    print("=" * 60)
    
    try:
        from app_matplotlib import app, open_browser
        
        # ブラウザを自動で開く
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Flaskアプリを起動
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except ImportError as e:
        print(f"❌ アプリケーションの起動に失敗しました: {e}")
        print("💡 app_matplotlib.py が存在し、必要なライブラリがインストールされていることを確認してください")
        print("💡 仮想環境を使用している場合は、source venv/bin/activate を実行してください")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 アプリケーションを終了します...")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()