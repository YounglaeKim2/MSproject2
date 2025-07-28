# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MSProject2는 전통 한국 운명학과 현대 AI 기술을 결합한 **완전 분리형 마이크로서비스** 웹 플랫폼입니다.

### 🆕 2025-07-28 Major Update: SAJU Service 대대적 기능 향상

- ✅ **13개 새로운 분석 메서드** 추가로 분석 정확도 대폭 향상
- ✅ **오행 균형 점수 시스템** (0-100점) 과학적 측정 완성
- ✅ **6가지 성격 유형 분류** 시스템 구현
- ✅ **맞춤형 조언 시스템** (색상, 방향, 생활습관, 직업, 건강, 인간관계)
- ✅ **현대적 UI/UX** styled-components 기반 완전 리뉴얼
- ✅ **API-프론트엔드 구조** 정합성 완벽 확보

### 서비스 아키텍처

- **Main Landing App** (`main-app/`) - 서비스 선택 랜딩 페이지 (포트: 4000)
- **SAJU Service** (`SAJU/`) - **🆕 확장된 사주팔자 분석 서비스** (백엔드: 8000, 프론트엔드: 3000)
- **Physiognomy Service** (`Physiognomy/`) - AI 기반 관상 분석 서비스 (백엔드: 8001, 프론트엔드: 3001)

각 서비스는 완전히 독립적으로 운영되며, 별도의 데이터베이스, API, 프론트엔드를 가집니다.

## Core Architecture Components

### 1. Main Landing App (`main-app/`)

서비스 선택 랜딩 페이지로, 사주와 관상 서비스로의 진입점 역할

- **기술스택**: React 18 + TypeScript + Styled Components
- **포트**: 4000
- **주요기능**: 서비스 선택 UI, 다른 서비스로의 새 창 네비게이션

### 2. SAJU Service (`SAJU/`) - 🆕 2025-07-28 대대적 확장

전통 명리학 기반 사주팔자 분석 서비스 (2025.07.28 대폭 확장)

```
SAJU/
├── backend/                  # FastAPI 백엔드 (포트: 8000)
│   ├── app/
│   │   ├── main.py          # FastAPI 애플리케이션 엔트리포인트
│   │   ├── api/saju.py      # 주요 API 엔드포인트 (확장 분석 지원)
│   │   ├── services/saju_analyzer.py  # 🆕 핵심 사주 분석 엔진 (13개 새 메서드)
│   │   ├── models/saju.py   # Pydantic 데이터 모델 (확장된 응답 구조)
│   │   └── database/connection.py    # SQLite 연결 관리
│   └── requirements.txt     # Python 의존성
├── frontend/                # React 프론트엔드 (포트: 3000)
│   ├── src/
│   │   ├── App.tsx         # 🆕 메인 UI 컴포넌트 (styled-components 리뉴얼)
│   │   └── index.tsx       # React 엔트리포인트
│   ├── package.json        # Node.js 의존성
│   └── tsconfig.json       # TypeScript 설정 (확장된 인터페이스)
├── manseryukDB/            # 만세력 데이터베이스
│   ├── DB/manseryuk.db     # SQLite 만세력 DB (73,442 레코드)
│   └── mdbconn.py          # 데이터베이스 연결 유틸리티
├── 사주해석로직.txt          # 전통 명리학 해석 로직 문서
└── docker-compose.yml      # Docker 설정
```

#### 🆕 SAJU 서비스 주요 확장 기능 (2025-07-28)

##### A. 확장 분석 엔진 (`saju_analyzer.py`)

**13개 새로운 분석 메서드**:

1. `_perform_extended_wuxing_analysis()` - 확장 오행 분석 총괄
2. `_calculate_wuxing_details()` - 오행별 세부 분석 (개수, 백분율, 강도)
3. `_analyze_wuxing_balance()` - 오행 균형 분석
4. `_calculate_balance_score()` - 0-100점 균형 점수 계산
5. `_get_excessive_elements()` - 과다 오행 탐지
6. `_get_deficient_elements()` - 부족 오행 탐지
7. `_analyze_personality()` - 성격 분석
8. `_determine_personality_type()` - 6가지 성격 유형 분류
9. `_get_personality_strengths()` - 강점 분석
10. `_get_personality_weaknesses()` - 약점 분석
11. `_get_dominant_traits()` - 주요 특성 추출
12. `_generate_balance_recommendations()` - 균형 기반 추천
13. `_get_element_recommendations()` - 오행별 추천

##### B. 맞춤형 추천 시스템

**8가지 추천 카테고리**:

- 🎨 **색상 추천**: 개인별 도움되는 색상
- 🧭 **방향 추천**: 풍수 기반 유리한 방위
- 🍽️ **음식 추천**: 오행 보완 음식
- 🏃 **활동 추천**: 건강과 성장을 위한 활동
- 🏠 **라이프스타일**: 생활습관 개선 조언
- 💼 **직업 조언**: 적성에 맞는 직업 분야
- 💊 **건강 관리**: 개인별 건강 유지 방법
- 💑 **인간관계**: 대인관계 개선 방법

##### C. 확장된 API 응답 구조

```json
{
  "extended_analysis": {
    "wuxing_details": {
      "목": {"count": 2, "percentage": 25.0, "strength": "보통", ...}
    },
    "balance_analysis": {
      "balance_score": 85.3,
      "excessive_elements": ["금"],
      "deficient_elements": ["목"],
      "dominant_element": "금",
      "weakest_element": "목"
    },
    "personality_analysis": {
      "personality_type": "완벽주의자",
      "strengths": ["결단력", "체계성"],
      "weaknesses": ["융통성 부족"],
      "dominant_traits": ["신중함", "분석적"],
      "advice": "균형잡힌 접근이 필요합니다"
    },
    "recommendations": {
      "colors": ["검정색", "남색"],
      "directions": ["북쪽", "동쪽"],
      "lifestyle": ["규칙적인 생활"],
      "foods": ["짠맛 음식"],
      "activities": ["독서", "명상"],
      "career_advice": ["상담 업무", "환경 관련"],
      "health_advice": ["간 기능 관리", "스트레스 해소"],
      "relationship_advice": ["지혜로운 조언", "따뜻한 배려"]
    }
  }
}
```

##### D. 현대적 UI/UX (React + styled-components)

- **오행 균형 점수**: 원형 프로그레스 차트 시각화
- **성격 분석 카드**: 직관적인 정보 표시
- **추천 그리드**: 8가지 카테고리별 맞춤 추천
- **반응형 디자인**: 모든 디바이스 최적화
  │ ├── src/App.tsx # 🆕 현대적 UI/UX로 완전 리뉴얼된 메인 분석 화면
  │ ├── package.json # Node.js 의존성 (styled-components 추가)
  │ └── tsconfig.json # TypeScript 설정
  ├── manseryukDB/ # 만세력 데이터베이스 시스템
  │ ├── DataMaseryuk.py # DB 테스트 및 예제
  │ ├── README.md # 만세력 DB 설명
  │ └── DB/
  │ ├── manseryuk.db # SQLite 만세력 데이터 (73,442 레코드)
  │ └── mdbconn.py # DB 연결 및 쿼리 클래스
  ├── 사주해석로직.txt # 전통 명리학 해석 로직 (400+ 줄)
  └── docker-compose.yml # Docker 컨테이너 설정

```

#### 🆕 확장된 분석 시스템 (saju_analyzer.py)

## 🆕 2025-07-28 최신 업데이트 완료 사항

### 직업 조언 출력 문제 해결 ✅

**문제**: 프론트엔드에서 직업 조언, 건강 조언, 인간관계 조언이 표시되지 않음

**해결 과정**:
1. **백엔드 수정** (`saju_analyzer.py`):
   - `_generate_balance_recommendations()` 메서드에 새로운 필드 추가
   - `_get_element_recommendations()` 메서드 확장
   - `career_advice`, `health_advice`, `relationship_advice` 필드 구현

2. **프론트엔드 수정** (`App.tsx`):
   - TypeScript 인터페이스 업데이트 (SajuResult)
   - 새로운 추천 카드 컴포넌트 정상 작동 확인

3. **검증 완료**:
   - API 응답에 모든 조언 카테고리 포함 확인
   - 브라우저에서 정상 렌더링 확인
   - TypeScript 컴파일 에러 없음

### 현재 서비스 상태

- ✅ **메인 앱**: http://localhost:4000 (정상 실행)
- ✅ **SAJU 백엔드**: http://localhost:8000 (정상 실행)
- ✅ **SAJU 프론트엔드**: http://localhost:3000 (정상 실행)

모든 확장 분석 기능이 정상 작동하며, 8가지 추천 카테고리가 완벽하게 표시됩니다.

### 3. Physiognomy Service (`Physiognomy/`)

AI 기반 관상 분석 서비스 (개발 진행 중)

```

Physiognomy/
├── backend/ # FastAPI + AI 백엔드 (포트: 8001)
│ ├── app/
│ │ ├── main.py # FastAPI 애플리케이션
│ │ ├── ml/ # 머신러닝 모듈
│ │ └── api/ # API 엔드포인트
│ ├── requirements.txt # Python + AI 라이브러리 의존성
│ └── uploads/ # 이미지 업로드 처리
├── frontend/ # React 프론트엔드 (포트: 3001)
│ ├── src/App.tsx # 관상 분석 UI (이미지 업로드 + 웹캠)
│ └── package.json # react-webcam, react-dropzone 포함
├── models/ # AI 모델 저장소
├── datasets/ # 학습 데이터
└── docker-compose.yml # PostgreSQL 포함 Docker 설정

````

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
````

## Development Commands

### 🆕 전체 서비스 실행 (로컬 개발 - 2025-07-28 업그레이드)

#### 1. 메인 랜딩 페이지 실행

```bash
cd main-app
npm install
npm start                    # 포트: 4000에서 실행
```

#### 2. 🆕 확장된 사주 서비스 실행 (두 개 터미널 필요)

```bash
# 터미널 1: 백엔드 (13개 새로운 분석 메서드 포함)
cd SAJU/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 터미널 2: 프론트엔드 (현대적 UI/UX로 리뉴얼)
cd SAJU/frontend
npm install
npm start                    # 포트: 3000에서 실행 (자동 설정됨)
```

✅ **확인**: http://localhost:3000에서 **오행 균형 점수, 성격 유형, 맞춤형 조언** 등 새로운 기능 체험

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

## 🎯 사주 분석 엔진 확장 기능 (2025.07.28 업데이트)

### SajuAnalyzer 클래스 새로운 메서드

```python
# services/saju_analyzer.py의 새로운 확장 메서드들

def _perform_extended_wuxing_analysis(self, wuxing_count, day_gan_wuxing, strength, use_god, avoid_god):
    """확장된 오행 분석 수행"""
    # 오행별 강도 및 백분율 계산
    # 오행 균형 분석
    # 성격 분석
    # 보완 방법 제안

def _analyze_wuxing_balance(self, wuxing_count, day_gan_wuxing):
    """오행 균형 분석 - 균형도 점수 (0-100) 계산"""
    # 과다/부족 오행 식별
    # 균형도 점수 계산
    # 주도적 오행/가장 약한 오행 파악

def _analyze_personality_by_wuxing(self, wuxing_count, day_gan_wuxing):
    """오행 분포에 따른 성격 분석"""
    # 주요 성격 특성 도출
    # 성격 유형 판단 (5가지 타입)
    # 강점/약점 분석

def _generate_balance_recommendations(self, wuxing_count, day_gan_wuxing, use_god, avoid_god):
    """오행 보완 방법 제안"""
    # 생활습관, 색상, 방향, 음식, 활동 가이드
```

### 확장된 분석 결과 구조

```python
# models/saju.py의 확장된 WuXingAnalysis
class WuXingAnalysis(BaseModel):
    wood: int                    # 기본 오행 개수
    fire: int
    earth: int
    metal: int
    water: int
    strength: str               # 일간 강약
    use_god: str               # 용신
    avoid_god: str             # 기신
    extended_analysis: Dict    # 새로운 확장 분석 데이터

# extended_analysis 내부 구조:
{
    "wuxing_details": {
        "목": {
            "count": 2,
            "percentage": 25.0,
            "strength": "보통",
            "meaning": "성장, 창조, 유연성, 인자함",
            "characteristics": ["창의적", "성장지향적", "유연한", "협력적"]
        }
        # ... 각 오행별 상세 정보
    },
    "balance_analysis": {
        "balance_score": 75.2,          # 균형도 점수 (0-100)
        "excessive_elements": ["목"],    # 과다한 오행
        "deficient_elements": ["화"],    # 부족한 오행
        "dominant_element": "목",        # 주도적 오행
        "weakest_element": "화"          # 가장 약한 오행
    },
    "personality_analysis": {
        "dominant_traits": ["창의적", "성장지향적", "유연한"],
        "personality_type": "성장형 - 끊임없이 발전을 추구하는 창의적 성격",
        "strengths": ["창의력과 성장 잠재력이 뛰어남"],
        "weaknesses": ["열정이나 표현력이 부족할 수 있음"],
        "advice": "창의적 재능을 발휘할 수 있는 분야에서 활동하시면 좋겠습니다."
    },
    "recommendations": {
        "lifestyle": ["동쪽 방향 활동", "아침 시간 활용", "식물 기르기"],
        "colors": ["빨간색", "주황색", "분홍색"],        # 부족한 화 보강
        "directions": ["남쪽"],
        "foods": ["쓴맛 음식", "따뜻한 음식"],
        "activities": ["운동", "사회 활동", "예술 활동"]
    }
}
```

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
  "gender": "male", // "male" 또는 "female"
  "name": "홍길동"
}
```

#### 사주 분석 응답 형식 (2025.07.28 확장)

```json
{
  "basic_info": { "name": "홍길동", "birth_date": "...", "gender": "male" },
  "saju_palja": {
    "year_pillar": { "stem": "경", "branch": "오" },
    "month_pillar": { "stem": "신", "branch": "사" },
    "day_pillar": { "stem": "무", "branch": "진" },
    "hour_pillar": { "stem": "기", "branch": "미" }
  },
  "wuxing_analysis": {
    "목": 1,
    "화": 3,
    "토": 2,
    "금": 2,
    "수": 0,
    "strength": "strong",
    "use_god": "수",
    "avoid_god": "화",
    "extended_analysis": {
      "wuxing_details": {
        "목": {
          "count": 1,
          "percentage": 12.5,
          "strength": "약함",
          "meaning": "성장, 창조, 유연성, 인자함",
          "characteristics": ["창의적", "성장지향적", "유연한", "협력적"]
        }
        // ... 각 오행별 상세 정보
      },
      "balance_analysis": {
        "balance_score": 65.3,
        "excessive_elements": ["화"],
        "deficient_elements": ["수"],
        "dominant_element": "화",
        "weakest_element": "수"
      },
      "personality_analysis": {
        "dominant_traits": ["열정적", "표현력이 풍부한", "사교적"],
        "personality_type": "열정형 - 활력이 넘치고 표현력이 풍부한 외향적 성격",
        "strengths": [
          "열정과 표현력이 풍부함",
          "창의력과 성장 잠재력이 뛰어남"
        ],
        "weaknesses": ["지혜나 적응력이 부족할 수 있음"],
        "advice": "열정을 바탕으로 적극적인 도전을 통해 성과를 이루시길 바랍니다."
      },
      "recommendations": {
        "lifestyle": ["북쪽 방향 활동", "밤 시간 활용", "조용한 환경"],
        "colors": ["검은색", "남색", "진청색"],
        "directions": ["북쪽"],
        "foods": ["짠맛 음식", "신장에 좋은 음식", "해산물"],
        "activities": ["수영", "독서", "깊이 있는 사고"]
      }
    }
  },
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

#### 🆕 SAJU 서비스 핵심 파일들 (2025-07-28 최신)

- **`SAJU/backend/app/services/saju_analyzer.py`**: 확장 분석 엔진 (13개 새 메서드)
- **`SAJU/backend/app/api/saju.py`**: API 엔드포인트 (확장 응답 구조)
- **`SAJU/frontend/src/App.tsx`**: React UI (styled-components 리뉴얼)
- **`SAJU/manseryukDB/DB/manseryuk.db`**: 만세력 데이터베이스

#### 기타 중요 파일들

- **`main-app/frontend/src/App.tsx`**: 메인 랜딩 페이지
- **`Physiognomy/backend/app/main.py`**: 관상 서비스 (개발 진행 중)

---

## 🎯 개발 가이드라인

### SAJU 서비스 확장 시 주의사항

1. **분석 메서드 추가**: `saju_analyzer.py`에 새 메서드 구현
2. **API 응답 확장**: `saju.py`의 응답 구조 업데이트
3. **프론트엔드 인터페이스**: TypeScript 인터페이스 동기화
4. **UI 컴포넌트**: styled-components 일관성 유지

### 성능 최적화

- 확장 분석은 옵션으로 실행 (기본 분석과 분리)
- 데이터베이스 쿼리 최적화
- React 컴포넌트 메모이제이션

### 코드 품질

- TypeScript 타입 안전성 유지
- ESLint/Prettier 코드 스타일 일관성
- FastAPI의 자동 문서화 활용

---

## 🏆 프로젝트 현재 상태 (2025-07-28)

### ✅ 완성된 기능

- **사주 분석 엔진**: 13개 확장 메서드로 정밀 분석
- **균형 점수 시스템**: 0-100점 과학적 측정
- **8가지 추천 카테고리**: 맞춤형 조언 시스템
- **현대적 UI/UX**: 직관적이고 아름다운 인터페이스
- **완벽한 API**: RESTful 설계와 자동 문서화

### 🚀 즉시 이용 가능

모든 서비스가 정상 실행 중이며, 사주 분석의 모든 확장 기능을 즉시 체험할 수 있습니다.

**서비스 접속 주소**:

- 메인: http://localhost:4000
- 사주 분석: http://localhost:3000
- API 문서: http://localhost:8000/docs

**최신 해결 완료**: 직업 조언, 건강 조언, 인간관계 조언 모두 정상 출력 ✅

- `SAJU/backend/app/services/saju_analyzer.py`: 핵심 사주 분석 로직
- `SAJU/manseryukDB/DB/mdbconn.py`: 만세력 DB 연결 및 쿼리
- `main-app/frontend/src/App.tsx`: 서비스 선택 랜딩 페이지
- `사주해석로직.txt`: 전통 명리학 해석 알고리즘 문서

### Development Best Practices

- **절기 계산**: 입춘을 년간지 기준, 24절기를 월간지 기준으로 계산
- **데이터 정확성**: 고영창의 "진짜 만세력" 기준 데이터 사용
- **API 설계**: RESTful 원칙 준수, 명확한 엔드포인트 분리
- **CORS 설정**: 개발/프로덕션 환경별 적절한 설정

### Port Allocation Table

| 서비스      | 백엔드 | 프론트엔드 | 설명                    |
| ----------- | ------ | ---------- | ----------------------- |
| Main        | -      | 4000       | 서비스 선택 랜딩 페이지 |
| SAJU        | 8000   | 3000       | 사주팔자 분석 서비스    |
| Physiognomy | 8001   | 3001       | 관상 분석 서비스        |

### Core File Paths

```
MSproject2_SAJU/
├── main-app/frontend/src/App.tsx          # 메인 랜딩 페이지
├── SAJU/backend/app/main.py               # 사주 API 서버
├── SAJU/frontend/src/App.tsx              # 사주 분석 UI
├── SAJU/backend/app/services/saju_analyzer.py  # 사주 분석 엔진
├── SAJU/manseryukDB/DB/manseryuk.db       # 만세력 데이터베이스
└── 사주해석로직.txt                        # 명리학 해석 로직
```

### Common Issues & Solutions

- **Pydantic v2 호환성**: `regex` → `pattern`, BaseSettings 별도 import
- **포트 충돌**: 각 서비스별 고정 포트 사용으로 해결
- **만세력 DB 접근**: SQLite 파일 권한 및 경로 확인 필요
- **CORS 설정**: 필요시 추가 도메인 허용 설정 필요
- **Docker 환경**: 각 서비스별 독립적인 docker-compose.yml 사용

## 🎯 최신 개발 현황 (2025.07.28)

### ✅ 완료된 작업

#### 프로젝트 구조 및 서비스

- ✅ 마이크로서비스 아키텍처 완성 (Main + SAJU + Physiognomy)
- ✅ 전체 서비스 테스트 완료 (모든 포트 정상 작동)
- ✅ 파일 시스템 정리 완료 (불필요한 디렉토리 삭제)
- ✅ 문서 통합 완료 (README.md, CLAUDE.md)

#### 사주 분석 서비스 확장

- ✅ **확장된 오행 분석**: 상세 강도 계산, 균형도 점수 (0-100)
- ✅ **성격 분석**: 5가지 성격 유형, 강점/약점 분석
- ✅ **오행 보완법**: 생활습관, 색상, 방향, 음식, 활동 가이드
- ✅ **새로운 분석 메서드들**: 13개 신규 메서드 구현
- ✅ **확장 데이터 모델**: WuXingAnalysis에 extended_analysis 필드 추가

#### 데이터베이스 및 백엔드

- ✅ 만세력 DB (73,442 레코드) 정상 작동
- ✅ FastAPI 서버 정상 운영 (포트 8000)
- ✅ API 엔드포인트 업데이트 완료

### 🔄 작업 진행 중

- 🔄 프론트엔드 UI 업데이트 (확장 분석 결과 표시)
- 🔄 API 응답 최적화

### 📋 다음 작업 계획

1. **프론트엔드 UI 개선**

   - 확장된 오행 분석 결과 표시
   - 성격 분석 섹션 추가
   - 오행 보완 방법 가이드 UI

2. **사용자 경험 향상**

   - 결과 해석 설명 추가
   - 인터랙티브 차트/그래프
   - PDF 결과 다운로드 기능

3. **관상 서비스 개발** (동료 개발자 담당)
   - AI 모델 통합
   - 이미지 처리 파이프라인
   - 관상 분석 알고리즘

### 🎉 주요 성과

**MSProject2는 이제 전문가급 사주 분석 서비스를 제공합니다:**

- 전통 명리학 기반의 정확한 사주팔자 계산
- 상세한 오행 분석 및 균형도 평가
- 개인 맞춤형 성격 분석 및 실용적 조언
- 과학적 데이터 기반의 보완 방법 제안
