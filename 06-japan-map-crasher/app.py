#!/usr/bin/env python3
"""
日本地図表示ブラウザアプリ
FlaskとD3.jsを使用して日本地図を表示する
"""

from flask import Flask, render_template, jsonify
import webbrowser
import threading
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    """メインページ"""
    return render_template('index.html')

@app.route('/api/prefectures')
def get_prefectures():
    """都道府県データAPI"""
    prefectures = [
        {"name": "北海道", "code": "01", "region": "北海道"},
        {"name": "青森県", "code": "02", "region": "東北"},
        {"name": "岩手県", "code": "03", "region": "東北"},
        {"name": "宮城県", "code": "04", "region": "東北"},
        {"name": "秋田県", "code": "05", "region": "東北"},
        {"name": "山形県", "code": "06", "region": "東北"},
        {"name": "福島県", "code": "07", "region": "東北"},
        {"name": "茨城県", "code": "08", "region": "関東"},
        {"name": "栃木県", "code": "09", "region": "関東"},
        {"name": "群馬県", "code": "10", "region": "関東"},
        {"name": "埼玉県", "code": "11", "region": "関東"},
        {"name": "千葉県", "code": "12", "region": "関東"},
        {"name": "東京都", "code": "13", "region": "関東"},
        {"name": "神奈川県", "code": "14", "region": "関東"},
        {"name": "新潟県", "code": "15", "region": "中部"},
        {"name": "富山県", "code": "16", "region": "中部"},
        {"name": "石川県", "code": "17", "region": "中部"},
        {"name": "福井県", "code": "18", "region": "中部"},
        {"name": "山梨県", "code": "19", "region": "中部"},
        {"name": "長野県", "code": "20", "region": "中部"},
        {"name": "岐阜県", "code": "21", "region": "中部"},
        {"name": "静岡県", "code": "22", "region": "中部"},
        {"name": "愛知県", "code": "23", "region": "中部"},
        {"name": "三重県", "code": "24", "region": "近畿"},
        {"name": "滋賀県", "code": "25", "region": "近畿"},
        {"name": "京都府", "code": "26", "region": "近畿"},
        {"name": "大阪府", "code": "27", "region": "近畿"},
        {"name": "兵庫県", "code": "28", "region": "近畿"},
        {"name": "奈良県", "code": "29", "region": "近畿"},
        {"name": "和歌山県", "code": "30", "region": "近畿"},
        {"name": "鳥取県", "code": "31", "region": "中国"},
        {"name": "島根県", "code": "32", "region": "中国"},
        {"name": "岡山県", "code": "33", "region": "中国"},
        {"name": "広島県", "code": "34", "region": "中国"},
        {"name": "山口県", "code": "35", "region": "中国"},
        {"name": "徳島県", "code": "36", "region": "四国"},
        {"name": "香川県", "code": "37", "region": "四国"},
        {"name": "愛媛県", "code": "38", "region": "四国"},
        {"name": "高知県", "code": "39", "region": "四国"},
        {"name": "福岡県", "code": "40", "region": "九州"},
        {"name": "佐賀県", "code": "41", "region": "九州"},
        {"name": "長崎県", "code": "42", "region": "九州"},
        {"name": "熊本県", "code": "43", "region": "九州"},
        {"name": "大分県", "code": "44", "region": "九州"},
        {"name": "宮崎県", "code": "45", "region": "九州"},
        {"name": "鹿児島県", "code": "46", "region": "九州"},
        {"name": "沖縄県", "code": "47", "region": "沖縄"}
    ]
    return jsonify(prefectures)

def open_browser():
    """ブラウザを自動で開く"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("日本地図ブラウザアプリを起動しています...")
    print("URL: http://localhost:5000")
    
    # ブラウザを自動で開く
    threading.Thread(target=open_browser).start()
    
    # Flaskアプリを起動（全てのインターフェースからアクセス可能）
    app.run(host='0.0.0.0', port=5000, debug=False)