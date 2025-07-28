# SAJU - 사주팔자 분석 서비스

전통 명리학 기반의 사주팔자 분석 독립 서비스입니다.

## 🎯 서비스 개요

- **포트**: 백엔드 8000, 프론트엔드 3000
- **데이터베이스**: SQLite (만세력 DB)
- **기술 스택**: FastAPI + React + TypeScript

## 📁 디렉토리 구조

```
SAJU/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 라우터
│   │   ├── core/           # 설정
│   │   ├── database/       # DB 연결
│   │   ├── models/         # 데이터 모델
│   │   └── services/       # 사주 분석 엔진
│   ├── manseryukDB/        # 만세력 데이터베이스
│   └── requirements.txt
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/     # 컴포넌트
│   │   ├── services/       # API 통신
│   │   └── types/          # 타입 정의
│   └── package.json
├── docker-compose.yml      # 컨테이너 설정
├── .env.example           # 환경 설정 예시
└── README.md              # 이 파일
```

## 🚀 실행 방법

### 백엔드 실행
```bash
cd SAJU/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프론트엔드 실행
```bash
cd SAJU/frontend
npm install
npm start
```

### Docker로 실행
```bash
cd SAJU
docker-compose up
```

## 🔗 접속

- **웹 서비스**: http://localhost:3000
- **API 문서**: http://localhost:8000/docs

## 📊 주요 기능

- 정확한 사주팔자 계산 (1900-2100년)
- 오행 분석 및 용신/기신 도출
- 성격, 직업, 건강, 대인관계, 재물운 해석
- 시각적 오행 차트 제공

## 🔧 개발 환경

- Python 3.8+
- Node.js 14+
- SQLite 3

## 📝 API 엔드포인트

- `POST /api/v1/saju/analyze` - 완전한 사주 분석
- `GET /api/v1/saju/palja-only` - 사주팔자만 추출
- `GET /api/v1/saju/wuxing-only` - 오행 분석만