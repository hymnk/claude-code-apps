import pandas as pd
import requests
import json
from io import StringIO

def load_japan_population_data():
    """Load Japan population data by prefecture from 1950 to present"""
    
    # Create synthetic data for demonstration (in a real app, you'd load from official sources)
    # This simulates population data for all 47 prefectures
    prefectures = [
        "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県", 
        "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
        "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
        "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
        "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
        "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
        "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
    ]
    
    # Base populations (in thousands) - roughly based on actual 1950 data
    base_populations = {
        "北海道": 4200, "青森県": 1400, "岩手県": 1300, "宮城県": 1600,
        "秋田県": 1200, "山形県": 1100, "福島県": 1800, "茨城県": 2000,
        "栃木県": 1400, "群馬県": 1500, "埼玉県": 2100, "千葉県": 1800,
        "東京都": 6200, "神奈川県": 2400, "新潟県": 2100, "富山県": 900,
        "石川県": 800, "福井県": 700, "山梨県": 700, "長野県": 1700,
        "岐阜県": 1400, "静岡県": 2200, "愛知県": 3200, "三重県": 1300,
        "滋賀県": 700, "京都府": 1700, "大阪府": 3800, "兵庫県": 3100,
        "奈良県": 700, "和歌山県": 800, "鳥取県": 500, "島根県": 700,
        "岡山県": 1600, "広島県": 1800, "山口県": 1300, "徳島県": 700,
        "香川県": 700, "愛媛県": 1200, "高知県": 800, "福岡県": 3200,
        "佐賀県": 800, "長崎県": 1300, "熊本県": 1600, "大分県": 1000,
        "宮崎県": 900, "鹿児島県": 1600, "沖縄県": 460
    }
    
    years = range(1950, 2025, 5)  # Every 5 years
    data = []
    
    for year in years:
        for prefecture in prefectures:
            # Simulate population growth/decline patterns
            base_pop = base_populations[prefecture]
            
            # Different growth patterns for different prefectures
            if prefecture in ["東京都", "神奈川県", "埼玉県", "千葉県", "愛知県", "大阪府", "兵庫県", "福岡県"]:
                # Urban areas: steady growth until 2000s, then stabilization
                if year <= 2000:
                    growth_rate = 0.8 + (year - 1950) * 0.01
                else:
                    growth_rate = 1.5 - (year - 2000) * 0.005
            else:
                # Rural areas: growth until 1980s, then decline
                if year <= 1980:
                    growth_rate = 0.6 + (year - 1950) * 0.008
                else:
                    growth_rate = 1.2 - (year - 1980) * 0.008
            
            population = int(base_pop * growth_rate)
            data.append({
                'year': year,
                'prefecture': prefecture,
                'population': population
            })
    
    return pd.DataFrame(data)

def load_japan_geojson():
    """Load Japan prefecture boundaries as GeoJSON"""
    
    # Simplified GeoJSON for Japanese prefectures
    # In a real application, you'd load from a proper geospatial data source
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }
    
    # This is a simplified representation - in reality you'd need proper geometric data
    # For demonstration, we'll create placeholder geometries
    prefectures = [
        {"name": "北海道", "center": [143.2, 43.2]},
        {"name": "青森県", "center": [140.7, 40.8]},
        {"name": "岩手県", "center": [141.1, 39.7]},
        {"name": "宮城県", "center": [140.9, 38.3]},
        {"name": "秋田県", "center": [140.1, 39.7]},
        {"name": "山形県", "center": [140.3, 38.2]},
        {"name": "福島県", "center": [140.5, 37.4]},
        {"name": "茨城県", "center": [140.4, 36.3]},
        {"name": "栃木県", "center": [139.9, 36.6]},
        {"name": "群馬県", "center": [139.1, 36.4]},
        {"name": "埼玉県", "center": [139.6, 35.9]},
        {"name": "千葉県", "center": [140.1, 35.6]},
        {"name": "東京都", "center": [139.7, 35.7]},
        {"name": "神奈川県", "center": [139.4, 35.4]},
        {"name": "新潟県", "center": [139.0, 37.9]},
        {"name": "富山県", "center": [137.2, 36.7]},
        {"name": "石川県", "center": [136.6, 36.6]},
        {"name": "福井県", "center": [136.2, 36.1]},
        {"name": "山梨県", "center": [138.6, 35.7]},
        {"name": "長野県", "center": [138.2, 36.2]},
        {"name": "岐阜県", "center": [137.0, 35.4]},
        {"name": "静岡県", "center": [138.4, 34.9]},
        {"name": "愛知県", "center": [137.0, 35.2]},
        {"name": "三重県", "center": [136.5, 34.7]},
        {"name": "滋賀県", "center": [136.0, 35.0]},
        {"name": "京都府", "center": [135.8, 35.0]},
        {"name": "大阪府", "center": [135.5, 34.7]},
        {"name": "兵庫県", "center": [135.2, 34.7]},
        {"name": "奈良県", "center": [135.8, 34.4]},
        {"name": "和歌山県", "center": [135.2, 34.0]},
        {"name": "鳥取県", "center": [134.2, 35.5]},
        {"name": "島根県", "center": [132.6, 35.5]},
        {"name": "岡山県", "center": [133.9, 34.7]},
        {"name": "広島県", "center": [132.5, 34.4]},
        {"name": "山口県", "center": [131.5, 34.2]},
        {"name": "徳島県", "center": [134.6, 34.1]},
        {"name": "香川県", "center": [134.0, 34.3]},
        {"name": "愛媛県", "center": [132.8, 33.8]},
        {"name": "高知県", "center": [133.5, 33.6]},
        {"name": "福岡県", "center": [130.4, 33.6]},
        {"name": "佐賀県", "center": [130.3, 33.2]},
        {"name": "長崎県", "center": [129.9, 32.8]},
        {"name": "熊本県", "center": [130.7, 32.8]},
        {"name": "大分県", "center": [131.6, 33.2]},
        {"name": "宮崎県", "center": [131.4, 32.0]},
        {"name": "鹿児島県", "center": [130.6, 31.6]},
        {"name": "沖縄県", "center": [127.7, 26.2]}
    ]
    
    for pref in prefectures:
        feature = {
            "type": "Feature",
            "properties": {"name": pref["name"]},
            "geometry": {
                "type": "Point",
                "coordinates": pref["center"]
            }
        }
        geojson_data["features"].append(feature)
    
    return geojson_data