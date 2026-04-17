import sqlite3
import pandas as pd

conn = sqlite3.connect('safeway.db')
tables = ['lampposts', 'cctv', 'emergency_bell', 'police']

print("\n" + "="*30)
print("   [ 데이터베이스 통합 현황 ]")
print("="*30)

for table in tables:
    try:
        count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {table}", conn).iloc[0, 0]
        print(f"📍 {table:15} | {count:,}개 확인")
    except Exception:
        print(f"❌ {table:15} | 데이터 없음 (확인 필요)")

conn.close()
print("="*30)
