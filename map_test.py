import sqlite3
import pandas as pd
import folium
import os

print("--- 지도 생성 프로세스 시작 ---")

# 1. DB 연결 및 데이터 확인
if not os.path.exists('safeway.db'):
    print("❌ 에러: safeway.db 파일이 없습니다! db_setup.py를 먼저 실행하세요.")
else:
    conn = sqlite3.connect('safeway.db')
    try:
        # 가로등(lampposts) 테이블에서 데이터 가져오기
        # 컬럼명이 다를 수 있으니 주의!
        query = "SELECT * FROM lampposts LIMIT 100"
        df = pd.read_sql(query, conn)
        
        if df.empty:
            print("⚠️ 데이터가 비어있습니다.")
        else:
            # 보통 공공데이터의 위도/경도 컬럼명을 찾아서 지도 생성
            # 만약 에러나면 '설치위치_위도' 등으로 바꿔야 할 수도 있음
            lat_col = '위도' if '위도' in df.columns else df.columns[0]
            lon_col = '경도' if '경도' in df.columns else df.columns[1]
            
            print(f"데이터 {len(df)}건을 불러왔습니다. 지도를 그립니다...")
            
            # 지도 중심점 (데이터의 첫 번째 지점으로 설정)
            m = folium.Map(location=[df[lat_col].iloc[0], df[lon_col].iloc[0]], zoom_start=14)
            
            for i, row in df.iterrows():
                folium.Marker(
                    location=[row[lat_col], row[lon_col]],
                    popup="보안등 위치"
                ).add_to(m)
            
            m.save('my_map.html')
            print("✅ 성공: my_map.html 파일이 생성되었습니다!")
            
    except Exception as e:
        print(f"❌ 에러 발생: {e}")
    finally:
        conn.close()
