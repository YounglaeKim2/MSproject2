# CLAUDE.md - 개발 가이드

> MSProject2 SAJU 서비스 개발을 위한 Claude Code 가이드

## 🎯 프로젝트 개요

**완전 분리형 마이크로서비스** 웹 플랫폼 - 전통 명리학 + 현대 AI 기술

### 서비스 구조

- **Main App** (`main-app/`) - 랜딩 페이지 (:4000)
- **SAJU Service** (`SAJU/`) - 사주팔자 분석 (:8000/:3000) ✅ **완성**
- **Physiognomy Service** (`Physiognomy/`) - 관상 분석 (:8001/:3001) 📋 개발중

## 🏆 현재 완성 상태 (2025-07-28)

### ✅ SAJU 서비스 (100% 완성)

#### 백엔드 (37개 메서드)

- **기본 분석**: 사주팔자, 오행, 십성 ✅
- **확장 분석**: 13개 메서드 (균형점수, 성격유형, 맞춤추천) ✅
- **대운 분석**: 10년 주기 (2세-81세, 8개 대운) ✅
- **세운 분석**: 연간/월별 운세 ✅

#### API 엔드포인트 (7개)

```
POST /analyze     # 완전한 사주 분석 ✅
GET  /palja-only  # 사주팔자만 ✅
GET  /wuxing-only # 오행 분석만 ✅
POST /daeun       # 대운 분석 ✅
POST /saeun       # 세운 분석 ✅
GET  /test        # API 테스트 ✅
GET  /health      # 헬스 체크 ✅
```

#### 프론트엔드

- React 18 + TypeScript + styled-components ✅
- 기본 분석 + 대운 + 세운 UI 완성 ✅
- 반응형 디자인, 현대적 UI/UX ✅

#### 🔧 최근 버그 수정 (2025.07.28)

- **강점 & 약점 표시 문제** → ✅ 해결
- **성격/건강/대인관계/재물운 고정 문제** → ✅ 해결
- **한글 인코딩 문제** → ✅ 해결
- **API 응답 데이터 구조 개선** → ✅ 완료

## 📊 만세력 데이터베이스

- **경로**: `SAJU/manseryukDB/DB/manseryuk.db`
- **데이터**: 1900-2100년, 73,442 레코드
- **기반**: 고영창님 "진짜 만세력"
- **연결**: `SqliteDB` 클래스 (`mdbconn.py`)

## 🔧 개발 명령어

### 서비스 실행

```bash
# 메인 앱
cd main-app && npm start

# SAJU 백엔드
cd SAJU/backend && uvicorn app.main:app --reload --port 8000

# SAJU 프론트엔드
cd SAJU/frontend && npm start
```

### API 테스트

```bash
# 헬스 체크
curl http://localhost:8000/health

# 사주 분석
curl -X POST http://localhost:8000/api/v1/saju/analyze \
-H "Content-Type: application/json" \
-d '{"year":1990,"month":5,"day":15,"hour":14,"gender":"male","name":"홍길동"}'

# 대운 분석
curl -X POST http://localhost:8000/api/v1/saju/daeun

# 세운 분석 (2025년)
curl -X POST "http://localhost:8000/api/v1/saju/saeun?target_year=2025"
```

## 📁 핵심 파일 구조

```
SAJU/
├── backend/app/
│   ├── main.py                    # FastAPI 앱
│   ├── api/saju.py               # API 엔드포인트
│   ├── services/saju_analyzer.py # 37개 분석 메서드
│   ├── models/saju.py            # Pydantic 모델
│   └── database/connection.py    # DB 연결
├── frontend/src/
│   ├── App.tsx                   # 메인 UI (완성)
│   └── index.tsx                 # React 엔트리
├── manseryukDB/
│   ├── DB/manseryuk.db          # 만세력 DB
│   └── mdbconn.py               # DB 클래스
└── 사주해석로직.txt               # 명리학 문서
```

## 🌐 서비스 접속

| 서비스   | URL                        | 상태 |
| -------- | -------------------------- | ---- |
| 메인     | http://localhost:4000      | ✅   |
| 사주 UI  | http://localhost:3000      | ✅   |
| 사주 API | http://localhost:8000      | ✅   |
| API 문서 | http://localhost:8000/docs | ✅   |

## 🔨 기술 스택

- **백엔드**: FastAPI + Pydantic + SQLite
- **프론트엔드**: React 18 + TypeScript + styled-components
- **데이터**: 73,442개 만세력 레코드

## 📋 개발 가이드라인

### 코드 수정 시

1. **백엔드**: `saju_analyzer.py` 메서드 추가/수정
2. **API**: `saju.py` 엔드포인트 업데이트
3. **프론트엔드**: `App.tsx` UI 컴포넌트 수정
4. **타입 안전성**: TypeScript 인터페이스 동기화

### 포트 관리

- Main: 4000 | SAJU: 8000/3000 | Physiognomy: 8001/3001

### CORS 설정

- 개발환경: 모든 origins 허용
- SAJU: `http://localhost:3000` 허용

## 🎊 현재 프로젝트 상태

**SAJU 서비스: 100% 완성** ✅

- 모든 분석 기능 구현 완료
- 전문가급 정확도의 사주 분석
- 현대적 UI/UX 완성
- 안정적 서비스 실행

**즉시 이용 가능한 완전한 사주 분석 서비스입니다!** 🚀
