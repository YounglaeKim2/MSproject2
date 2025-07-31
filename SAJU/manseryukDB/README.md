# 만세력 데이터베이스

> 1900-2100년 완전한 만세력 데이터 (73,442 레코드)

## 📊 데이터 정보

- **파일**: `DB/manseryuk.db` (SQLite)
- **기간**: 1900.1.1 ~ 2100.12.31
- **레코드**: 73,442개
- **기반**: 고영창님 "진짜 만세력"

## 🔧 사용법

```python
from DB.mdbconn import SqliteDB

db = SqliteDB('manseryuk.db')
birth_data = db.GetBirth(1990, 5, 15)  # 생년월일 조회
time_data = db.GetTime(14)             # 시간을 지지로 변환
```

## 📋 주요 필드

- **양력/음력**: `cd_sy/sm/sd`, `cd_ly/lm/ld`
- **간지**: `cd_hyganjee`(년), `cd_hmganjee`(월), `cd_hdganjee`(일)
- **절기**: `cd_hterms`, `cd_terms_time`
- **기타**: 요일, 28수, 월령, 윤달, 띠

---

**정확한 사주 계산의 핵심 데이터입니다!** 📅