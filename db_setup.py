import pandas as pd
import sqlite3
import os

print("--- [수정본] DB 구축 시작 ---")
conn = sqlite3.connect('safeway.db')

files = {
    'lampposts': 'lamps.csv',
    'cctv': 'cctv.csv',
    'emergency_bell': 'bell.csv',
    'police': 'police.csv'
}

for table, file in files.items():
    if os.path.exists(file):
        print(f"[{file}] 처리 중...")
        try:
            # 1. 인코딩 무시(errors='ignore') 및 구분자 자동 추정
            # 2. on_bad_lines='skip'으로 줄 안맞는 데이터는 그냥 건너뛰기
            df = pd.read_csv(file, encoding='cp949', on_bad_lines='skip', low_memory=False)
        except:
            try:
                df = pd.read_csv(file, encoding='utf-8', on_bad_lines='skip', low_memory=False)
            except:
                # 최후의 수단: latin1 인코딩 사용
                df = pd.read_csv(file, encoding='latin1', on_bad_lines='skip', low_memory=False)
        
        df.to_sql(table, conn, if_exists='replace', index=False)
        print(f"   ✅ {table} 완료: {len(df)}건")
    else:
        print(f"   ❌ {file} 없음")

conn.close()
print("--- 모든 작업 완료 ---")
