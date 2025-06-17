#!/usr/bin/env python3
"""
日本地図ブラウザアプリ - メイン起動スクリプト
"""

import sys
import os

# アプリケーションのディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, open_browser
import threading

def main():
    """メイン関数"""
    print("🗾 日本地図ブラウザアプリを起動します...")
    print("=" * 50)
    print("📍 URL: http://localhost:5000")
    print("📱 ブラウザが自動で開きます")
    print("🛑 終了するには Ctrl+C を押してください")
    print("=" * 50)
    
    try:
        # ブラウザを自動で開く
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Flaskアプリを起動
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except KeyboardInterrupt:
        print("\n👋 アプリケーションを終了します...")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()