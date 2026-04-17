from flask import Flask, request
import sqlite3
import pandas as pd
import folium
import os

app = Flask(__name__)

@app.route('/')
def index():
    lang = request.args.get('lang', 'ko')
    city = request.args.get('city', '경주')
    
    # 기본 지도 설정
    m = folium.Map(location=[35.7812, 129.4705], zoom_start=15)
    
    # DB 연결 및 데이터 표시
    if os.path.exists('safeway.db'):
        try:
            conn = sqlite3.connect('safeway.db')
            # 가로등 데이터 (경주 데이터 예시 기준 4, 5번 컬럼)
            df = pd.read_sql("SELECT * FROM lampposts LIMIT 1000", conn)
            for _, r in df.iterrows():
                folium.RegularPolygonMarker([r.iloc[4], r.iloc[5]], number_of_sides=3, radius=10, color='orange', fill=True).add_to(m)
            conn.close()
        except: pass

    return f"<h1>SafeWay Map</h1>{m._repr_html_()}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
