#!/usr/bin/env python3
"""
Folium版日本地図ブラウザの起動スクリプト
"""

import sys
import os

# アプリケーションのディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_folium import app, open_browser
import threading

def main():
    """メイン関数"""
    print("🗾 美しい日本地図ブラウザ (Folium版) を起動します...")
    print("=" * 60)
    print("📍 URL: http://localhost:5000")
    print("📱 ブラウザが自動で開きます")
    print("🎨 Foliumライブラリによる高品質地図表示")
    print("✨ 特徴:")
    print("   - 47都道府県の正確な位置表示")
    print("   - モノクロデザインテーマ")
    print("   - インタラクティブなポップアップ")
    print("   - 地域別色分け凡例")
    print("   - レスポンシブデザイン")
    print("🛑 終了するには Ctrl+C を押してください")
    print("=" * 60)
    
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