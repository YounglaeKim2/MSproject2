"""
SAJU 만세력 데이터베이스 연동
기존 SAJU 서비스의 데이터베이스를 재사용
"""
from app.database.mdbconn import SqliteDB

try:
    manseryuk_db = SqliteDB()
    print("SAJU 만세력 DB 연결 성공")
except Exception as e:
    print(f"DB 초기화 오류: {e}")
    manseryuk_db = None

def get_manseryuk_db():
    """만세력 데이터베이스 인스턴스 반환"""
    if manseryuk_db is None:
        raise Exception("만세력 데이터베이스에 연결할 수 없습니다.")
    return manseryuk_db