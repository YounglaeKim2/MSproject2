# Compatibility - 궁합 분석 서비스

🔮 전통 명리학 기반 사주팔자 궁합 분석 서비스

## 🎯 서비스 개요

- **포트**: 백엔드 8002, 프론트엔드 3002
- **기술 스택**: FastAPI + React + TypeScript + AI
- **분석 방식**: 사주팔자 + 오행 + 십성 + AI 해석

## 🚀 실행 방법

### 백엔드 실행
```bash
cd Compatibility/backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

### 프론트엔드 실행
```bash
cd Compatibility/frontend
npm install
npm start
```

## 🔗 접속

- **웹 서비스**: http://localhost:3002
- **API 문서**: http://localhost:8002/docs

## 📊 주요 기능

- 두 사람의 사주팔자 비교 분석
- 오행 상생상극 궁합 계산
- 십성 배합 궁합 분석
- AI 기반 종합 해석
- 분야별 궁합 (연애/결혼/사업/우정)

## 🎭 궁합 분석 요소

### 1. 사주팔자 궁합
- 년주/월주/일주/시주 상호 작용
- 천간지지 상성 분석

### 2. 오행 궁합
- 오행 균형 및 상생상극
- 부족한 오행 보완 관계

### 3. 십성 궁합
- 십성 배합 조화도
- 성격 및 기질 호환성

### 4. AI 종합 해석
- 전문 명리학자 수준 분석
- 실용적 관계 조언 제공

## 🏗️ 서비스 구조

```
Compatibility/
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── api/           # API 라우터
│   │   ├── models/        # 데이터 모델
│   │   ├── services/      # 궁합 분석 로직
│   │   └── main.py        # FastAPI 앱
│   └── requirements.txt
└── frontend/              # React 프론트엔드
    ├── src/
    │   ├── components/    # UI 컴포넌트
    │   ├── services/      # API 통신
    │   └── types/         # 타입 정의
    └── package.json
```

## 🎯 개발 상태

- ✅ 프로젝트 구조 생성
- 🔄 백엔드 궁합 분석 로직 구현 중
- ⏳ 프론트엔드 UI 개발 예정
- ⏳ AI 해석 시스템 통합 예정