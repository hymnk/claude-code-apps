#!/usr/bin/env python3
"""
ワイヤーフレーム版日本地図ブラウザの起動スクリプト
"""

import sys
import os

# アプリケーションのディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app_wireframe import app, open_browser
import threading

def main():
    """メイン関数"""
    print("🗾 ワイヤーフレーム日本地図ブラウザを起動します...")
    print("=" * 60)
    print("📍 URL: http://localhost:5000")
    print("📱 ブラウザが自動で開きます")
    print("🎨 Geoplot + Matplotlib によるワイヤーフレームデザイン")
    print("✨ 特徴:")
    print("   - ミニマルなワイヤーフレーム表示")
    print("   - 47都道府県の正確な位置データ")
    print("   - モノクロ設計図風デザイン")
    print("   - 高解像度PNG画像生成")
    print("   - 地域別グループ線表示")
    print("   - 技術仕様詳細表示")
    print("🔗 追加機能:")
    print("   - /map/download で高解像度版ダウンロード")
    print("   - /api/prefectures で都道府県データAPI")
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