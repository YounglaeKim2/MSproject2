# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

한국 전통 운명학 프로젝트:
- `Physiognomy/` - 관상학 관련 (현재 비어있음)
- `SAJU/` - 사주팔자 관련 시스템

## SAJU Directory Structure

```
SAJU/
├── manseryukDB/              # 만세력 데이터베이스 시스템
│   ├── DataMaseryuk.py      # 메인 실행 파일 및 예제
│   ├── README.md            # 만세력 DB 설명
│   └── DB/
│       ├── manseryuk.db     # SQLite 만세력 데이터베이스
│       └── mdbconn.py       # DB 연결 및 쿼리 클래스
└── 사주 해석 로직 자료_.docx  # 사주 해석 알고리즘 문서
```

## 만세력 Database (manseryuk.db)

- **데이터 범위**: 1900년 1월 1일 ~ 2100년 12월 31일 (73,442 레코드)
- **참조 자료**: 고영창님의 "진짜 만세력"
- **테이블**: `calenda_data` (양력↔음력 변환 및 간지 정보)

### 주요 필드
- 양력/음력 날짜: `cd_sy/sm/sd`, `cd_ly/lm/ld`
- 간지 정보: `cd_hyganjee`(년간지), `cd_hmganjee`(월간지), `cd_hdganjee`(일간지)
- 절기: `cd_hterms`(24절기), `cd_terms_time`(절입시간)
- 기타: 요일, 28수, 월령, 윤달, 띠 정보

## Core Classes

### SqliteDB (mdbconn.py)
```python
# 사용 예시
db = SqliteDB('manseryuk.db')
birth_data = db.GetBirth(1970, 1, 1)  # 생년월일로 만세력 조회
time_data = db.GetTime(13)            # 시간을 12지지로 변환
```

## Development Commands

```bash
# 만세력 DB 테스트
cd SAJU/manseryukDB
python DataMaseryuk.py

# DB 스키마 확인
sqlite3 DB/manseryuk.db ".schema"

# 데이터 샘플 조회
sqlite3 DB/manseryuk.db "SELECT * FROM calenda_data LIMIT 5;"
```

## 사주 해석 로직 (사주해석로직.txt)

상세한 명리학 해석 로직이 포함된 전문 문서:

### 핵심 해석 알고리즘
1. **오행 강약 판단**: 일간(日干) 중심의 신강/신약 분석
2. **용신/기신 도출**: 사주 균형을 위한 필요/방해 오행 식별
3. **십성(十星) 계산**: 일간 기준 상대적 관계 (비견, 겁재, 식신, 상관, 편재, 정재, 편관, 정관, 편인, 정인)
4. **천간/지지 상호작용**: 합(合), 충(沖), 형(刑), 파(破), 해(害) 분석
5. **신살(神殺) 판단**: 전통적 길흉 요소 (천을귀인, 도화살, 역마살 등)

### 운세 흐름 분석
- **대운(大運)**: 10년 주기 변화, 순행/역행 계산
- **세운(歲運)**: 연간 운세 분석

### 응용 분야
- 성격/기질 분석
- 건강 운세 (오행-오장육부 연관)
- 직업/재물 운세
- 배우자/대인관계 분석

### 기술 구현 방향
- 규칙 기반 시스템(Rule-Based System)
- AI/빅데이터 융합
- 만세력 API 연동

## 웹 서비스 (saju-web-service/)

완성된 FastAPI + React 기반 사주 웹 서비스:

### 실행 방법
```bash
# 백엔드 실행
cd saju-web-service/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프론트엔드 실행 (새 터미널)
cd saju-web-service/frontend
npm install
npm start
```

### 접속
- 웹 서비스: http://localhost:3000
- API 문서: http://localhost:8000/docs

## Notes

- Python 3 기반, SQLite3 사용
- 입춘을 년간지 기준으로, 절기를 월간지 기준으로 계산
- 전문적인 명리학 해석 로직과 웹 앱 구현 가이드 포함
- 완성된 웹 서비스 포함 (FastAPI + React)