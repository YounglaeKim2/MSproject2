# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MSProject2는 전통 한국 운명학과 현대 AI 기술을 결합한 **완전 분리형 마이크로서비스** 웹 플랫폼입니다.

### 서비스 아키텍처
- **Main Landing App** (`main-app/`) - 서비스 선택 랜딩 페이지 (포트: 4000)
- **SAJU Service** (`SAJU/`) - 사주팔자 분석 서비스 (백엔드: 8000, 프론트엔드: 3000)
- **Physiognomy Service** (`Physiognomy/`) - AI 기반 관상 분석 서비스 (백엔드: 8001, 프론트엔드: 3001)

각 서비스는 완전히 독립적으로 운영되며, 별도의 데이터베이스, API, 프론트엔드를 가집니다.

## Core Architecture Components

### 1. Main Landing App (`main-app/`)
서비스 선택 랜딩 페이지로, 사주와 관상 서비스로의 진입점 역할
- **기술스택**: React 18 + TypeScript + Styled Components
- **포트**: 4000
- **주요기능**: 서비스 선택 UI, 다른 서비스로의 새 창 네비게이션

### 2. SAJU Service (`SAJU/`)
전통 명리학 기반 사주팔자 분석 서비스
```
SAJU/
├── backend/                  # FastAPI 백엔드 (포트: 8000)
│   ├── app/
│   │   ├── main.py          # FastAPI 애플리케이션 엔트리포인트
│   │   ├── api/saju.py      # 주요 API 엔드포인트
│   │   ├── services/saju_analyzer.py  # 핵심 사주 분석 엔진
│   │   ├── models/saju.py   # Pydantic 데이터 모델
│   │   └── database/connection.py    # SQLite 연결 관리
│   └── requirements.txt     # Python 의존성
├── frontend/                # React 프론트엔드 (포트: 3000)
│   ├── src/App.tsx         # 메인 사주 분석 UI
│   ├── package.json        # Node.js 의존성
│   └── tsconfig.json       # TypeScript 설정
├── manseryukDB/            # 만세력 데이터베이스 시스템
│   ├── DataMaseryuk.py     # DB 테스트 및 예제
│   ├── README.md           # 만세력 DB 설명
│   └── DB/
│       ├── manseryuk.db    # SQLite 만세력 데이터 (73,442 레코드)
│       └── mdbconn.py      # DB 연결 및 쿼리 클래스
├── 사주해석로직.txt         # 명리학 해석 알고리즘 문서
└── docker-compose.yml      # Docker 컨테이너 설정
```

### 3. Physiognomy Service (`Physiognomy/`)
AI 기반 관상 분석 서비스 (개발 진행 중)
```
Physiognomy/
├── backend/                # FastAPI + AI 백엔드 (포트: 8001)
│   ├── app/
│   │   ├── main.py        # FastAPI 애플리케이션
│   │   ├── ml/            # 머신러닝 모듈
│   │   └── api/           # API 엔드포인트
│   ├── requirements.txt   # Python + AI 라이브러리 의존성
│   └── uploads/           # 이미지 업로드 처리
├── frontend/              # React 프론트엔드 (포트: 3001)
│   ├── src/App.tsx       # 관상 분석 UI (이미지 업로드 + 웹캠)
│   └── package.json      # react-webcam, react-dropzone 포함
├── models/                # AI 모델 저장소
├── datasets/              # 학습 데이터
└── docker-compose.yml     # PostgreSQL 포함 Docker 설정
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

### 전체 서비스 실행 (로컬 개발)

#### 1. 메인 랜딩 페이지 실행
```bash
cd main-app
npm install
npm start                    # 포트: 4000에서 실행
```

#### 2. 사주 서비스 실행 (두 개 터미널 필요)
```bash
# 터미널 1: 백엔드
cd SAJU/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 터미널 2: 프론트엔드
cd SAJU/frontend
npm install
npm start                    # 포트: 3000에서 실행 (자동 설정됨)
```

#### 3. 관상 서비스 실행 (두 개 터미널 필요)
```bash
# 터미널 1: 백엔드
cd Physiognomy/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# 터미널 2: 프론트엔드
cd Physiognomy/frontend
npm install
npm start                    # 포트: 3001에서 실행 (자동 설정됨)
```

### Docker 실행 (프로덕션 환경)
```bash
# 사주 서비스
cd SAJU
docker-compose up --build

# 관상 서비스
cd Physiognomy
docker-compose up --build
```

### 데이터베이스 관련 명령어
```bash
# 만세력 DB 테스트
cd SAJU/manseryukDB
python DataMaseryuk.py

# DB 스키마 확인
sqlite3 DB/manseryuk.db ".schema"

# 데이터 샘플 조회
sqlite3 DB/manseryuk.db "SELECT * FROM calenda_data LIMIT 5;"

# 특정 날짜 만세력 조회 예시
sqlite3 DB/manseryuk.db "SELECT * FROM calenda_data WHERE cd_sy=1990 AND cd_sm=5 AND cd_sd=15;"
```

### API 테스트 명령어
```bash
# 사주 API 헬스체크
curl http://localhost:8000/health

# 사주 분석 API 테스트
curl -X POST http://localhost:8000/api/v1/saju/analyze \
  -H "Content-Type: application/json" \
  -d '{"year": 1990, "month": 5, "day": 15, "hour": 14, "gender": "male", "name": "홍길동"}'

# 관상 API 헬스체크
curl http://localhost:8001/health
```

### 접속 URL
- **메인 페이지**: http://localhost:4000
- **사주 서비스**: http://localhost:3000
- **관상 서비스**: http://localhost:3001
- **사주 API 문서**: http://localhost:8000/docs
- **관상 API 문서**: http://localhost:8001/docs

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

## API Architecture & Service Communication

### SAJU Service API Endpoints
기본 경로: `http://localhost:8000/api/v1/saju/`

- **POST `/analyze`** - 완전한 사주 분석 (사주팔자 + 오행 + 해석)
- **GET `/palja-only`** - 사주팔자만 추출 (년주/월주/일주/시주)
- **GET `/wuxing-only`** - 오행 분석만 (목/화/토/금/수 분포)
- **GET `/test`** - API 연결 테스트
- **GET `/health`** - 서비스 헬스 체크

#### 사주 분석 요청 형식
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 14,
  "gender": "male",    // "male" 또는 "female"
  "name": "홍길동"
}
```

#### 사주 분석 응답 형식
```json
{
  "basic_info": { "name": "홍길동", "birth_date": "...", "gender": "male" },
  "saju_palja": {
    "year_pillar": { "stem": "경", "branch": "오" },
    "month_pillar": { "stem": "신", "branch": "사" },
    "day_pillar": { "stem": "무", "branch": "진" },
    "hour_pillar": { "stem": "기", "branch": "미" }
  },
  "wuxing_analysis": { "목": 1, "화": 3, "토": 2, "금": 2, "수": 0 },
  "interpretations": {
    "personality": "성격 해석 텍스트...",
    "career": "직업운 해석 텍스트...",
    "health": "건강운 해석 텍스트...",
    "relationships": "대인관계 해석 텍스트...",
    "wealth": "재물운 해석 텍스트..."
  }
}
```

### CORS 설정
- **SAJU 백엔드**: `http://localhost:3000` 허용
- **Physiognomy 백엔드**: `http://localhost:3001`, `http://localhost:4000` 허용
- **개발 환경**: 모든 origins 허용 (`allow_origins=["*"]`)

### Database Connections
- **SAJU**: SQLite (`manseryuk.db`) - 직접 연결
- **Physiognomy**: PostgreSQL (Docker) - SQLAlchemy ORM

## Technology Stack Details

### Backend Framework
- **FastAPI**: 모든 백엔드 서비스의 기본 프레임워크
- **Pydantic 2.5.0**: 데이터 검증, 주의사항: `regex` → `pattern` 파라미터 사용
- **pydantic-settings**: BaseSettings는 별도 패키지로 분리됨

### Frontend Framework
- **React 18 + TypeScript**: 모든 프론트엔드 서비스
- **Styled Components**: CSS-in-JS 스타일링
- **Axios**: API 통신

### AI/ML Stack (Physiognomy Service)
- **TensorFlow 2.13.0**: 딥러닝 모델
- **PyTorch 2.0.1**: 대안 ML 프레임워크
- **OpenCV 4.8.1**: 컴퓨터 비전
- **MediaPipe 0.10.7**: 얼굴 인식 및 분석

### Database
- **SAJU**: SQLite (`manseryuk.db`) - 73,442개 만세력 레코드
- **Physiognomy**: PostgreSQL (Docker 컨테이너)

## Development Workflow & Architecture Notes

### Service Independence
- 각 서비스는 **완전히 독립적**으로 개발, 배포, 확장 가능
- 서비스 간 통신은 HTTP API를 통해서만 이루어짐
- 데이터베이스, 종속성, 설정이 모두 분리됨

### Port Management
- **포트 충돌 방지**: 각 서비스별 고정 포트 할당
- **개발 환경**: 모든 서비스를 동시에 실행 가능
- **프로덕션**: Docker Compose로 독립 배포

### Key Files to Understand
- `SAJU/backend/app/services/saju_analyzer.py`: 핵심 사주 분석 로직
- `SAJU/manseryukDB/DB/mdbconn.py`: 만세력 DB 연결 및 쿼리
- `main-app/frontend/src/App.tsx`: 서비스 선택 랜딩 페이지
- `사주해석로직.txt`: 전통 명리학 해석 알고리즘 문서

### Development Best Practices
- **절기 계산**: 입춘을 년간지 기준, 24절기를 월간지 기준으로 계산
- **데이터 정확성**: 고영창의 "진짜 만세력" 기준 데이터 사용
- **API 설계**: RESTful 원칙 준수, 명확한 엔드포인트 분리
- **CORS 설정**: 개발/프로덕션 환경별 적절한 설정

### Common Issues & Solutions
- **Pydantic v2 호환성**: `regex` → `pattern`, BaseSettings 별도 import
- **포트 충돌**: 각 서비스별 고정 포트 사용으로 해결
- **만세력 DB 접근**: SQLite 파일 권한 및 경로 확인 필요
- **Docker 환경**: 각 서비스별 독립적인 docker-compose.yml 사용