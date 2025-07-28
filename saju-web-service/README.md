# 사주 웹 서비스

FastAPI + React 기반의 사주팔자 분석 웹 서비스입니다.

## 프로젝트 구조

```
saju-web-service/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 라우터
│   │   ├── core/           # 설정 및 코어 모듈
│   │   ├── database/       # 데이터베이스 연결
│   │   ├── models/         # Pydantic 모델
│   │   └── services/       # 비즈니스 로직
│   ├── manseryukDB/        # 만세력 데이터베이스
│   ├── requirements.txt    # Python 의존성
│   └── main.py            # FastAPI 앱 진입점
└── frontend/               # React 프론트엔드
    ├── src/
    │   ├── components/     # React 컴포넌트
    │   ├── services/       # API 통신
    │   ├── types/          # TypeScript 타입
    │   └── App.tsx        # 메인 앱 컴포넌트
    ├── public/
    ├── package.json       # npm 의존성
    └── tsconfig.json      # TypeScript 설정
```

## 주요 기능

### 백엔드 (FastAPI)
- **만세력 DB 연동**: SQLite 기반 1900-2100년 만세력 데이터
- **사주팔자 추출**: 출생 정보로부터 정확한 사주팔자 계산
- **종합 분석**: 오행, 십성, 성격, 직업, 건강, 대인관계, 재물운 분석
- **RESTful API**: 표준화된 API 인터페이스 제공

### 프론트엔드 (React)
- **직관적 UI**: 사용자 친화적인 입력 폼
- **반응형 디자인**: 모바일 및 데스크톱 지원
- **실시간 분석**: API 연동을 통한 즉시 결과 제공
- **시각적 표현**: 오행 차트 및 구조화된 결과 화면

## 설치 및 실행

### 백엔드 실행

```bash
# 백엔드 디렉토리로 이동
cd saju-web-service/backend

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프론트엔드 실행

```bash
# 프론트엔드 디렉토리로 이동
cd saju-web-service/frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm start
```

## API 엔드포인트

### 기본 정보
- **Base URL**: `http://localhost:8000`
- **API 버전**: v1
- **문서**: `http://localhost:8000/docs` (Swagger UI)

### 주요 엔드포인트

#### 1. 완전한 사주 분석
```
POST /api/v1/saju/analyze
```

**요청 본문:**
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 14,
  "gender": "male",
  "name": "홍길동"
}
```

**응답:**
```json
{
  "palja": {
    "year_gan": "庚",
    "year_ji": "午",
    "month_gan": "辛",
    "month_ji": "巳",
    "day_gan": "甲",
    "day_ji": "寅",
    "hour_gan": "辛",
    "hour_ji": "未"
  },
  "wuxing": {
    "wood": 2,
    "fire": 2,
    "earth": 1,
    "metal": 3,
    "water": 0,
    "strength": "strong",
    "use_god": "수",
    "avoid_god": "금"
  },
  "personality": {
    "basic_nature": "의지가 강하고 원칙적인 성격",
    "strengths": ["의지력", "원칙성", "결단력"],
    "weaknesses": ["완고함", "융통성 부족"],
    "recommendations": ["수 기운을 보강하여 자신감을 키우세요"]
  },
  // ... 기타 분석 결과
}
```

#### 2. 사주팔자만 추출
```
GET /api/v1/saju/palja-only?year=1990&month=5&day=15&hour=14&gender=male
```

#### 3. 오행 분석만
```
GET /api/v1/saju/wuxing-only?year=1990&month=5&day=15&hour=14&gender=male
```

#### 4. API 테스트
```
GET /api/v1/saju/test
```

#### 5. 헬스 체크
```
GET /health
```

## 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 프레임워크
- **Pydantic**: 데이터 검증 및 시리얼라이제이션
- **SQLite**: 만세력 데이터베이스
- **Python 3.8+**: 런타임 환경

### 프론트엔드
- **React 18**: UI 라이브러리
- **TypeScript**: 타입 안전성
- **Styled Components**: CSS-in-JS 스타일링
- **Axios**: HTTP 클라이언트

## 사주 분석 로직

### 1. 만세력 계산
- 양력 출생일을 음력으로 변환
- 절기 기준 년/월주 계산
- 정확한 시주 도출

### 2. 오행 분석
- 사주팔자 내 오행 분포 계산
- 일간 강약 판단 (신강/신약)
- 용신/기신 도출

### 3. 십성 분석
- 일간 기준 상대적 관계 분석
- 비견, 겁재, 식신, 상관, 재성, 관성, 인성

### 4. 종합 해석
- **성격**: 기본 성향, 장단점, 개선 방향
- **직업**: 적성 분야, 성향, 성공 요인
- **건강**: 강약 장기, 주의사항, 관리법
- **대인관계**: 관계 스타일, 궁합, 사회성
- **재물**: 재물 성향, 수입 패턴, 투자 조언

## 개발 참고사항

### 환경변수
```bash
# .env 파일 (백엔드)
DATABASE_URL=sqlite:///./manseryukDB/DB/manseryuk.db
SECRET_KEY=your-secret-key
DEBUG=True

# .env 파일 (프론트엔드)
REACT_APP_API_URL=http://localhost:8000
```

### CORS 설정
백엔드에서 프론트엔드(localhost:3000)에 대한 CORS가 이미 설정되어 있습니다.

### 에러 처리
- API 요청/응답 로깅
- 사용자 친화적 에러 메시지
- 네트워크 오류 처리

## 라이센스

이 프로젝트는 개인 학습 및 연구 목적으로 개발되었습니다.

## 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request